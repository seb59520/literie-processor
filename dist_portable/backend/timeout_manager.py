"""
Gestionnaire de timeouts dynamiques pour l'application Matelas
"""

import time
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict, deque
import statistics

logger = logging.getLogger(__name__)

@dataclass
class TimeoutMetrics:
    """Métriques pour le calcul des timeouts"""
    request_size_chars: int = 0
    file_size_mb: float = 0.0
    provider: str = ""
    model: str = ""
    avg_response_time: float = 0.0
    success_rate: float = 1.0
    last_processing_time: float = 0.0

@dataclass 
class AdaptiveTimeout:
    """Configuration de timeout adaptif"""
    base_timeout: float = 60.0
    min_timeout: float = 30.0
    max_timeout: float = 600.0
    size_factor: float = 0.1  # secondes par MB
    chars_factor: float = 0.001  # secondes par caractère
    provider_multiplier: Dict[str, float] = field(default_factory=lambda: {
        'openrouter': 1.0,
        'openai': 0.8,
        'anthropic': 1.2,
        'ollama': 2.0,  # Local, peut être plus lent
        'mistral': 1.1
    })

class TimeoutManager:
    """Gestionnaire de timeouts adaptatifs basé sur l'historique"""
    
    def __init__(self, config: Optional[AdaptiveTimeout] = None):
        self.config = config or AdaptiveTimeout()
        
        # Historique des performances par provider/model
        self.performance_history = defaultdict(lambda: deque(maxlen=50))
        self.success_history = defaultdict(lambda: deque(maxlen=100))
        
        # Statistiques globales
        self.global_stats = {
            'total_requests': 0,
            'total_timeouts': 0,
            'avg_processing_time': 0.0,
            'last_reset': time.time()
        }
        
        logger.info("Gestionnaire de timeouts dynamiques initialisé")
    
    def calculate_timeout(
        self, 
        provider: str, 
        model: str = "", 
        request_size_chars: int = 0,
        file_size_mb: float = 0.0,
        complexity_factor: float = 1.0
    ) -> float:
        """
        Calcule un timeout adaptatif basé sur différents facteurs
        
        Args:
            provider: Nom du provider LLM
            model: Nom du modèle
            request_size_chars: Taille de la requête en caractères
            file_size_mb: Taille du fichier source en MB
            complexity_factor: Facteur de complexité (1.0 = normal)
            
        Returns:
            Timeout en secondes
        """
        # Timeout de base
        timeout = self.config.base_timeout
        
        # Ajustement selon le provider
        provider_multiplier = self.config.provider_multiplier.get(provider, 1.0)
        timeout *= provider_multiplier
        
        # Ajustement selon la taille
        size_adjustment = (request_size_chars * self.config.chars_factor + 
                          file_size_mb * self.config.size_factor)
        timeout += size_adjustment
        
        # Ajustement selon l'historique de performance
        historical_adjustment = self._calculate_historical_adjustment(provider, model)
        timeout *= historical_adjustment
        
        # Ajustement selon la complexité
        timeout *= complexity_factor
        
        # Application des limites min/max
        timeout = max(self.config.min_timeout, min(timeout, self.config.max_timeout))
        
        logger.debug(
            f"Timeout calculé: {timeout:.1f}s pour {provider}/{model} "
            f"({request_size_chars} chars, {file_size_mb:.1f} MB)"
        )
        
        return timeout
    
    def _calculate_historical_adjustment(self, provider: str, model: str) -> float:
        """Calcule l'ajustement basé sur l'historique"""
        key = f"{provider}:{model}"
        
        # Si pas d'historique, utiliser les stats globales du provider
        perf_history = self.performance_history.get(key)
        if not perf_history:
            provider_history = self.performance_history.get(provider)
            if not provider_history:
                return 1.0
            perf_history = provider_history
        
        if len(perf_history) < 3:
            return 1.0
        
        # Calculer la moyenne et l'écart-type des temps de traitement
        avg_time = statistics.mean(perf_history)
        
        try:
            std_time = statistics.stdev(perf_history)
        except statistics.StatisticsError:
            std_time = 0
        
        # Calculer le taux de succès
        success_key = f"{provider}:{model}"
        success_history = self.success_history.get(success_key, [])
        
        if success_history:
            success_rate = sum(success_history) / len(success_history)
        else:
            success_rate = 1.0
        
        # Ajustement basé sur la performance
        if avg_time > 60:  # Si historiquement lent
            adjustment = 1.2 + (std_time / avg_time)  # Plus de marge
        elif avg_time < 15:  # Si historiquement rapide
            adjustment = 0.8
        else:
            adjustment = 1.0 + (std_time / (avg_time + 1))
        
        # Ajustement selon le taux de succès
        if success_rate < 0.8:
            adjustment *= 1.3  # Plus de temps pour les providers instables
        elif success_rate > 0.95:
            adjustment *= 0.9  # Moins de temps pour les providers fiables
        
        return min(adjustment, 3.0)  # Max 3x le timeout de base
    
    def record_request_start(self, provider: str, model: str, timeout: float) -> str:
        """
        Enregistre le début d'une requête
        
        Returns:
            ID de la requête pour le suivi
        """
        request_id = f"{provider}:{model}:{time.time()}"
        self.global_stats['total_requests'] += 1
        
        logger.debug(f"Requête démarrée: {request_id} (timeout: {timeout:.1f}s)")
        return request_id
    
    def record_request_success(
        self, 
        request_id: str, 
        processing_time: float,
        provider: str,
        model: str
    ):
        """Enregistre une requête réussie"""
        key = f"{provider}:{model}"
        
        # Enregistrer le temps de traitement
        self.performance_history[key].append(processing_time)
        self.performance_history[provider].append(processing_time)
        
        # Enregistrer le succès
        self.success_history[key].append(1)
        
        # Mettre à jour les stats globales
        if self.global_stats['avg_processing_time'] == 0:
            self.global_stats['avg_processing_time'] = processing_time
        else:
            # Moyenne mobile
            self.global_stats['avg_processing_time'] = (
                self.global_stats['avg_processing_time'] * 0.9 + processing_time * 0.1
            )
        
        logger.debug(
            f"Requête réussie: {request_id} en {processing_time:.2f}s"
        )
    
    def record_request_timeout(self, request_id: str, provider: str, model: str):
        """Enregistre un timeout de requête"""
        key = f"{provider}:{model}"
        
        # Enregistrer l'échec
        self.success_history[key].append(0)
        
        # Mettre à jour les stats
        self.global_stats['total_timeouts'] += 1
        
        logger.warning(f"Timeout enregistré: {request_id}")
    
    def record_request_error(self, request_id: str, provider: str, model: str, error: str):
        """Enregistre une erreur de requête"""
        key = f"{provider}:{model}"
        
        # Enregistrer l'échec
        self.success_history[key].append(0)
        
        logger.warning(f"Erreur requête: {request_id} - {error}")
    
    def get_provider_stats(self, provider: str) -> Dict[str, Any]:
        """Obtient les statistiques d'un provider"""
        perf_history = list(self.performance_history.get(provider, []))
        success_history = list(self.success_history.get(provider, []))
        
        if not perf_history:
            return {
                'provider': provider,
                'no_data': True
            }
        
        return {
            'provider': provider,
            'total_requests': len(perf_history),
            'avg_processing_time': statistics.mean(perf_history),
            'min_processing_time': min(perf_history),
            'max_processing_time': max(perf_history),
            'std_processing_time': statistics.stdev(perf_history) if len(perf_history) > 1 else 0,
            'success_rate': sum(success_history) / len(success_history) if success_history else 0,
            'recommended_timeout': self.calculate_timeout(provider)
        }
    
    def get_global_stats(self) -> Dict[str, Any]:
        """Obtient les statistiques globales"""
        uptime = time.time() - self.global_stats['last_reset']
        
        return {
            'uptime_seconds': uptime,
            'total_requests': self.global_stats['total_requests'],
            'total_timeouts': self.global_stats['total_timeouts'],
            'timeout_rate': (self.global_stats['total_timeouts'] / 
                           max(self.global_stats['total_requests'], 1)),
            'avg_processing_time': self.global_stats['avg_processing_time'],
            'providers_tracked': len(self.performance_history)
        }
    
    def reset_stats(self):
        """Remet à zéro toutes les statistiques"""
        self.performance_history.clear()
        self.success_history.clear()
        self.global_stats = {
            'total_requests': 0,
            'total_timeouts': 0,
            'avg_processing_time': 0.0,
            'last_reset': time.time()
        }
        logger.info("Statistiques de timeout remises à zéro")
    
    def optimize_config(self):
        """Optimise automatiquement la configuration basée sur l'historique"""
        global_stats = self.get_global_stats()
        
        # Si trop de timeouts, augmenter les timeouts de base
        if global_stats['timeout_rate'] > 0.1:  # Plus de 10% de timeouts
            self.config.base_timeout *= 1.2
            self.config.min_timeout *= 1.1
            logger.info(f"Timeouts augmentés: base={self.config.base_timeout:.1f}s")
        
        # Si très peu de timeouts et temps moyen faible, réduire
        elif (global_stats['timeout_rate'] < 0.02 and 
              global_stats['avg_processing_time'] < self.config.base_timeout * 0.3):
            self.config.base_timeout *= 0.9
            logger.info(f"Timeouts réduits: base={self.config.base_timeout:.1f}s")
        
        # Respecter les limites
        self.config.base_timeout = max(30, min(self.config.base_timeout, 300))
        self.config.min_timeout = max(15, min(self.config.min_timeout, 120))

# Instance globale
timeout_manager = TimeoutManager()