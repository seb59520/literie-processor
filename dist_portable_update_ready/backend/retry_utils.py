"""
Utilitaires pour la gestion des retry avec backoff exponentiel
"""

import time
import random
import logging
from typing import Type, Tuple, Callable, Any, Optional
from functools import wraps
import asyncio
import requests

try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False
    aiohttp = None

logger = logging.getLogger(__name__)

class RetryableError(Exception):
    """Exception de base pour les erreurs qui peuvent être retryées"""
    pass

class RateLimitError(RetryableError):
    """Erreur de rate limiting"""
    def __init__(self, retry_after: Optional[float] = None):
        self.retry_after = retry_after
        super().__init__(f"Rate limit hit, retry after {retry_after}s")

class NetworkError(RetryableError):
    """Erreur réseau temporaire"""
    pass

class RetryConfig:
    """Configuration des retry"""
    def __init__(
        self,
        max_attempts: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True,
        retryable_exceptions: Tuple[Type[Exception], ...] = (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
            RetryableError
        ) + ((aiohttp.ClientError,) if AIOHTTP_AVAILABLE else ())
    ):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter
        self.retryable_exceptions = retryable_exceptions
    
    def calculate_delay(self, attempt: int) -> float:
        """Calcule le délai d'attente pour un attempt donné"""
        delay = self.base_delay * (self.exponential_base ** attempt)
        delay = min(delay, self.max_delay)
        
        if self.jitter:
            # Ajouter un jitter pour éviter la synchronisation des retry
            delay += random.uniform(0, delay * 0.1)
        
        return delay

def retry_sync(config: RetryConfig = None):
    """Décorateur pour retry synchrone"""
    if config is None:
        config = RetryConfig()
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(config.max_attempts):
                try:
                    logger.debug(f"Tentative {attempt + 1}/{config.max_attempts} pour {func.__name__}")
                    return func(*args, **kwargs)
                    
                except config.retryable_exceptions as e:
                    last_exception = e
                    
                    # Gestion spéciale pour rate limiting
                    if isinstance(e, RateLimitError) and e.retry_after:
                        delay = e.retry_after
                    elif isinstance(e, requests.exceptions.HTTPError):
                        response = getattr(e, 'response', None)
                        if response and response.status_code == 429:
                            # Rate limit HTTP
                            retry_after = response.headers.get('Retry-After')
                            if retry_after:
                                delay = float(retry_after)
                            else:
                                delay = config.calculate_delay(attempt)
                        elif response and 500 <= response.status_code < 600:
                            # Erreur serveur, on peut retry
                            delay = config.calculate_delay(attempt)
                        else:
                            # Erreur client, pas de retry
                            break
                    else:
                        delay = config.calculate_delay(attempt)
                    
                    if attempt < config.max_attempts - 1:
                        logger.warning(
                            f"Tentative {attempt + 1} échouée pour {func.__name__}: {e}. "
                            f"Retry dans {delay:.2f}s"
                        )
                        time.sleep(delay)
                    else:
                        logger.error(
                            f"Toutes les tentatives échouées pour {func.__name__}: {e}"
                        )
            
            # Relancer la dernière exception si tous les retry ont échoué
            raise last_exception
        
        return wrapper
    return decorator

def retry_async(config: RetryConfig = None):
    """Décorateur pour retry asynchrone"""
    if config is None:
        config = RetryConfig()
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(config.max_attempts):
                try:
                    logger.debug(f"Tentative async {attempt + 1}/{config.max_attempts} pour {func.__name__}")
                    return await func(*args, **kwargs)
                    
                except config.retryable_exceptions as e:
                    last_exception = e
                    
                    # Gestion spéciale pour aiohttp (si disponible)
                    if AIOHTTP_AVAILABLE and hasattr(aiohttp, 'ClientResponseError') and isinstance(e, aiohttp.ClientResponseError):
                        if e.status == 429:
                            # Rate limit
                            retry_after = e.headers.get('Retry-After')
                            if retry_after:
                                delay = float(retry_after)
                            else:
                                delay = config.calculate_delay(attempt)
                        elif 500 <= e.status < 600:
                            # Erreur serveur
                            delay = config.calculate_delay(attempt)
                        else:
                            # Erreur client, pas de retry
                            break
                    elif isinstance(e, RateLimitError) and e.retry_after:
                        delay = e.retry_after
                    else:
                        delay = config.calculate_delay(attempt)
                    
                    if attempt < config.max_attempts - 1:
                        logger.warning(
                            f"Tentative async {attempt + 1} échouée pour {func.__name__}: {e}. "
                            f"Retry dans {delay:.2f}s"
                        )
                        await asyncio.sleep(delay)
                    else:
                        logger.error(
                            f"Toutes les tentatives async échouées pour {func.__name__}: {e}"
                        )
            
            raise last_exception
        
        return wrapper
    return decorator

class CircuitBreaker:
    """Circuit breaker pour éviter les appels répétés vers un service défaillant"""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'closed'  # closed, open, half-open
    
    def can_execute(self) -> bool:
        """Vérifie si l'exécution est autorisée"""
        if self.state == 'closed':
            return True
        elif self.state == 'open':
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = 'half-open'
                return True
            return False
        else:  # half-open
            return True
    
    def record_success(self):
        """Enregistre un succès"""
        self.failure_count = 0
        self.state = 'closed'
    
    def record_failure(self):
        """Enregistre un échec"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = 'open'
            logger.warning(f"Circuit breaker ouvert après {self.failure_count} échecs")

def with_circuit_breaker(circuit_breaker: CircuitBreaker):
    """Décorateur pour circuit breaker"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if not circuit_breaker.can_execute():
                raise RetryableError("Circuit breaker ouvert")
            
            try:
                result = func(*args, **kwargs)
                circuit_breaker.record_success()
                return result
            except Exception as e:
                circuit_breaker.record_failure()
                raise
        
        return wrapper
    return decorator