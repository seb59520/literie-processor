#!/usr/bin/env python3
"""
Système de recovery automatique d'erreurs
"""

import time
import threading
import json
from typing import Dict, Any, Callable, Optional, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from enum import Enum

class RecoveryStrategy(Enum):
    """Stratégies de récupération d'erreurs"""
    RETRY = "retry"
    FALLBACK = "fallback"
    RESET = "reset"
    NOTIFY = "notify"

@dataclass
class RecoveryRule:
    """Règle de récupération pour un type d'erreur"""
    error_pattern: str  # Pattern regex pour matcher l'erreur
    strategy: RecoveryStrategy
    max_attempts: int = 3
    delay_seconds: float = 1.0
    exponential_backoff: bool = True
    fallback_action: Optional[Callable] = None
    recovery_action: Optional[Callable] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RecoveryAttempt:
    """Tentative de récupération"""
    timestamp: datetime
    error_type: str
    error_message: str
    strategy_used: RecoveryStrategy
    success: bool
    attempt_number: int
    recovery_time: float

class AutoRecoverySystem:
    """Système de récupération automatique d'erreurs"""
    
    def __init__(self, log_file: str = "logs/recovery.json"):
        import sys
        
        # Créer le chemin de log sécurisé
        if getattr(sys, 'frozen', False):
            # Si exécutable PyInstaller
            log_dir = Path.home() / "MatelasApp" / "logs"
            self.log_file = log_dir / "recovery.json"
        else:
            # Si script Python normal, utiliser le chemin relatif depuis le projet
            self.log_file = Path(__file__).parent.parent / log_file
        
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.recovery_rules: List[RecoveryRule] = []
        self.recovery_history: List[RecoveryAttempt] = []
        self.active_recoveries: Dict[str, int] = {}  # operation_id -> attempt_count
        
        self.lock = threading.Lock()
        
        # Règles par défaut
        self._setup_default_rules()
    
    def _setup_default_rules(self):
        """Configure les règles de récupération par défaut"""
        
        # Erreurs réseau - retry avec backoff exponentiel
        self.add_rule(RecoveryRule(
            error_pattern=r"(ConnectionError|TimeoutError|HTTPError|RequestException)",
            strategy=RecoveryStrategy.RETRY,
            max_attempts=3,
            delay_seconds=2.0,
            exponential_backoff=True,
            metadata={"category": "network"}
        ))
        
        # Erreurs API LLM - retry avec délai plus long
        self.add_rule(RecoveryRule(
            error_pattern=r"(RateLimitError|APIError|ServiceUnavailable)",
            strategy=RecoveryStrategy.RETRY,
            max_attempts=5,
            delay_seconds=5.0,
            exponential_backoff=True,
            metadata={"category": "api"}
        ))
        
        # Erreurs de fichier - retry simple
        self.add_rule(RecoveryRule(
            error_pattern=r"(FileNotFoundError|PermissionError|OSError)",
            strategy=RecoveryStrategy.RETRY,
            max_attempts=2,
            delay_seconds=0.5,
            exponential_backoff=False,
            metadata={"category": "file"}
        ))
        
        # Erreurs de mémoire - reset
        self.add_rule(RecoveryRule(
            error_pattern=r"(MemoryError|OutOfMemoryError)",
            strategy=RecoveryStrategy.RESET,
            max_attempts=1,
            metadata={"category": "memory"}
        ))
    
    def add_rule(self, rule: RecoveryRule):
        """Ajoute une règle de récupération"""
        with self.lock:
            self.recovery_rules.append(rule)
    
    def attempt_recovery(self, operation_id: str, error: Exception, 
                        operation_func: Callable, *args, **kwargs) -> Any:
        """Tente de récupérer d'une erreur"""
        import re
        
        error_str = str(error)
        error_type = type(error).__name__
        
        with self.lock:
            current_attempts = self.active_recoveries.get(operation_id, 0)
        
        # Trouver la règle applicable
        applicable_rule = None
        for rule in self.recovery_rules:
            if re.search(rule.error_pattern, error_str) or re.search(rule.error_pattern, error_type):
                applicable_rule = rule
                break
        
        if not applicable_rule:
            # Aucune règle applicable, re-lever l'erreur
            raise error
        
        if current_attempts >= applicable_rule.max_attempts:
            # Trop de tentatives, abandon
            self._log_recovery_failure(operation_id, error, applicable_rule, current_attempts)
            raise error
        
        # Incrémenter le compteur de tentatives
        with self.lock:
            self.active_recoveries[operation_id] = current_attempts + 1
        
        # Calculer le délai d'attente
        delay = applicable_rule.delay_seconds
        if applicable_rule.exponential_backoff:
            delay *= (2 ** current_attempts)
        
        start_time = time.time()
        
        try:
            # Attendre avant la nouvelle tentative
            if delay > 0:
                time.sleep(delay)
            
            # Exécuter l'action de récupération si définie
            if applicable_rule.recovery_action:
                applicable_rule.recovery_action()
            
            # Réessayer l'opération selon la stratégie
            if applicable_rule.strategy == RecoveryStrategy.RETRY:
                result = operation_func(*args, **kwargs)
            elif applicable_rule.strategy == RecoveryStrategy.FALLBACK:
                if applicable_rule.fallback_action:
                    result = applicable_rule.fallback_action(*args, **kwargs)
                else:
                    raise error
            elif applicable_rule.strategy == RecoveryStrategy.RESET:
                # Réinitialiser l'état et réessayer
                self._reset_operation_state(operation_id)
                result = operation_func(*args, **kwargs)
            else:
                raise error
            
            # Succès - nettoyer et logger
            recovery_time = time.time() - start_time
            self._log_recovery_success(operation_id, error, applicable_rule, current_attempts + 1, recovery_time)
            
            with self.lock:
                if operation_id in self.active_recoveries:
                    del self.active_recoveries[operation_id]
            
            return result
            
        except Exception as new_error:
            # Échec de la récupération, réessayer ou abandonner
            return self.attempt_recovery(operation_id, new_error, operation_func, *args, **kwargs)
    
    def _reset_operation_state(self, operation_id: str):
        """Réinitialise l'état d'une opération"""
        # Nettoyer les caches, fermer les connexions, etc.
        try:
            import gc
            gc.collect()
        except:
            pass
    
    def _log_recovery_success(self, operation_id: str, error: Exception, 
                             rule: RecoveryRule, attempt: int, recovery_time: float):
        """Enregistre un succès de récupération"""
        recovery_attempt = RecoveryAttempt(
            timestamp=datetime.now(),
            error_type=type(error).__name__,
            error_message=str(error),
            strategy_used=rule.strategy,
            success=True,
            attempt_number=attempt,
            recovery_time=recovery_time
        )
        
        self.recovery_history.append(recovery_attempt)
        self._write_to_log(recovery_attempt)
    
    def _log_recovery_failure(self, operation_id: str, error: Exception, 
                             rule: RecoveryRule, attempts: int):
        """Enregistre un échec de récupération"""
        recovery_attempt = RecoveryAttempt(
            timestamp=datetime.now(),
            error_type=type(error).__name__,
            error_message=str(error),
            strategy_used=rule.strategy,
            success=False,
            attempt_number=attempts,
            recovery_time=0.0
        )
        
        self.recovery_history.append(recovery_attempt)
        self._write_to_log(recovery_attempt)
    
    def _write_to_log(self, attempt: RecoveryAttempt):
        """Écrit une tentative de récupération dans le log"""
        try:
            log_entry = {
                "timestamp": attempt.timestamp.isoformat(),
                "error_type": attempt.error_type,
                "error_message": attempt.error_message,
                "strategy": attempt.strategy_used.value,
                "success": attempt.success,
                "attempt_number": attempt.attempt_number,
                "recovery_time": attempt.recovery_time
            }
            
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
                
        except Exception as e:
            print(f"Erreur lors de l'écriture du log de récupération: {e}")
    
    def get_recovery_stats(self, hours: int = 24) -> Dict[str, Any]:
        """Retourne les statistiques de récupération"""
        cutoff = datetime.now() - timedelta(hours=hours)
        recent_attempts = [
            a for a in self.recovery_history 
            if a.timestamp > cutoff
        ]
        
        if not recent_attempts:
            return {"period_hours": hours, "total_attempts": 0}
        
        successful = [a for a in recent_attempts if a.success]
        
        return {
            "period_hours": hours,
            "total_attempts": len(recent_attempts),
            "successful_recoveries": len(successful),
            "success_rate": len(successful) / len(recent_attempts),
            "avg_recovery_time": sum(a.recovery_time for a in successful) / len(successful) if successful else 0,
            "most_common_error": max(set(a.error_type for a in recent_attempts), 
                                   key=lambda x: sum(1 for a in recent_attempts if a.error_type == x))
        }

def with_auto_recovery(operation_id: str = None):
    """Décorateur pour ajouter la récupération automatique à une fonction"""
    recovery_system = get_auto_recovery_system()
    
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            op_id = operation_id or f"{func.__name__}_{int(time.time())}"
            
            try:
                return func(*args, **kwargs)
            except Exception as e:
                return recovery_system.attempt_recovery(op_id, e, func, *args, **kwargs)
        
        return wrapper
    return decorator

# Instance globale
auto_recovery_system = None

def get_auto_recovery_system() -> AutoRecoverySystem:
    """Retourne l'instance du système de récupération automatique"""
    global auto_recovery_system
    if auto_recovery_system is None:
        auto_recovery_system = AutoRecoverySystem()
    return auto_recovery_system