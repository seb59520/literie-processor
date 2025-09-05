#!/usr/bin/env python3
"""
Système de monitoring des performances
"""

import time
import psutil
import threading
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import json
from pathlib import Path

@dataclass
class PerformanceMetrics:
    """Métriques de performance pour une opération"""
    operation: str
    start_time: float
    end_time: Optional[float] = None
    duration: Optional[float] = None
    memory_start: float = 0
    memory_end: float = 0
    memory_delta: float = 0
    cpu_start: float = 0
    cpu_end: float = 0
    success: bool = True
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class PerformanceMonitor:
    """Moniteur de performances en temps réel"""
    
    def __init__(self, log_file: str = "logs/performance.json"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(exist_ok=True)
        
        self.active_operations = {}
        self.metrics_history = []
        self.lock = threading.Lock()
        
        # Métriques système
        self.process = psutil.Process()
        
    def start_operation(self, operation_id: str, operation_name: str, metadata: Dict[str, Any] = None) -> str:
        """Démarre le monitoring d'une opération"""
        with self.lock:
            metrics = PerformanceMetrics(
                operation=operation_name,
                start_time=time.time(),
                memory_start=self.process.memory_info().rss / 1024 / 1024,  # MB
                cpu_start=self.process.cpu_percent(),
                metadata=metadata or {}
            )
            
            self.active_operations[operation_id] = metrics
            return operation_id
    
    def end_operation(self, operation_id: str, success: bool = True, error: str = None):
        """Termine le monitoring d'une opération"""
        with self.lock:
            if operation_id not in self.active_operations:
                return
                
            metrics = self.active_operations[operation_id]
            metrics.end_time = time.time()
            metrics.duration = metrics.end_time - metrics.start_time
            metrics.memory_end = self.process.memory_info().rss / 1024 / 1024  # MB
            metrics.memory_delta = metrics.memory_end - metrics.memory_start
            metrics.cpu_end = self.process.cpu_percent()
            metrics.success = success
            metrics.error = error
            
            # Ajouter à l'historique
            self.metrics_history.append(metrics)
            
            # Nettoyer les opérations actives
            del self.active_operations[operation_id]
            
            # Logger les métriques
            self._log_metrics(metrics)
    
    def _log_metrics(self, metrics: PerformanceMetrics):
        """Enregistre les métriques dans le fichier de log"""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "operation": metrics.operation,
                "duration": metrics.duration,
                "memory_delta_mb": metrics.memory_delta,
                "memory_end_mb": metrics.memory_end,
                "success": metrics.success,
                "error": metrics.error,
                "metadata": metrics.metadata
            }
            
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
                
        except Exception as e:
            print(f"Erreur lors de l'enregistrement des métriques: {e}")
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Retourne les métriques système actuelles"""
        try:
            return {
                "timestamp": datetime.now().isoformat(),
                "cpu_percent": psutil.cpu_percent(interval=0.1),
                "memory_percent": psutil.virtual_memory().percent,
                "memory_used_mb": self.process.memory_info().rss / 1024 / 1024,
                "disk_usage_percent": psutil.disk_usage('/').percent,
                "active_operations": len(self.active_operations)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_operation_stats(self, operation_name: str = None) -> Dict[str, Any]:
        """Retourne les statistiques d'une opération"""
        with self.lock:
            filtered_metrics = [
                m for m in self.metrics_history 
                if operation_name is None or m.operation == operation_name
            ]
            
            if not filtered_metrics:
                return {"count": 0}
            
            durations = [m.duration for m in filtered_metrics if m.duration]
            memory_deltas = [m.memory_delta for m in filtered_metrics]
            success_count = sum(1 for m in filtered_metrics if m.success)
            
            return {
                "count": len(filtered_metrics),
                "success_rate": success_count / len(filtered_metrics),
                "avg_duration": sum(durations) / len(durations) if durations else 0,
                "min_duration": min(durations) if durations else 0,
                "max_duration": max(durations) if durations else 0,
                "avg_memory_delta": sum(memory_deltas) / len(memory_deltas) if memory_deltas else 0,
                "last_run": max(m.start_time for m in filtered_metrics)
            }

class PerformanceDecorator:
    """Décorateur pour monitorer automatiquement les performances"""
    
    def __init__(self, monitor: PerformanceMonitor, operation_name: str = None):
        self.monitor = monitor
        self.operation_name = operation_name
    
    def __call__(self, func: Callable):
        def wrapper(*args, **kwargs):
            operation_name = self.operation_name or f"{func.__module__}.{func.__name__}"
            operation_id = f"{operation_name}_{int(time.time())}"
            
            self.monitor.start_operation(operation_id, operation_name, {
                "function": func.__name__,
                "args_count": len(args),
                "kwargs_keys": list(kwargs.keys())
            })
            
            try:
                result = func(*args, **kwargs)
                self.monitor.end_operation(operation_id, success=True)
                return result
            except Exception as e:
                self.monitor.end_operation(operation_id, success=False, error=str(e))
                raise
                
        return wrapper

# Instance globale
performance_monitor = None

def get_performance_monitor() -> PerformanceMonitor:
    """Retourne l'instance du moniteur de performance"""
    global performance_monitor
    if performance_monitor is None:
        performance_monitor = PerformanceMonitor()
    return performance_monitor

def monitor_performance(operation_name: str = None):
    """Décorateur pour monitorer les performances d'une fonction"""
    monitor = get_performance_monitor()
    return PerformanceDecorator(monitor, operation_name)

def create_performance_report() -> Dict[str, Any]:
    """Crée un rapport de performance complet"""
    monitor = get_performance_monitor()
    
    return {
        "timestamp": datetime.now().isoformat(),
        "system_metrics": monitor.get_system_metrics(),
        "processing_stats": monitor.get_operation_stats("file_processing"),
        "llm_call_stats": monitor.get_operation_stats("llm_call"),
        "validation_stats": monitor.get_operation_stats("file_validation"),
        "overall_stats": monitor.get_operation_stats()
    }