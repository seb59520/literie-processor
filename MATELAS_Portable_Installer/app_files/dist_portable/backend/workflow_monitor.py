#!/usr/bin/env python3
"""
Système de surveillance et monitoring des workflows
"""

import json
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from pathlib import Path
from collections import deque, defaultdict

from .workflow_engine import WorkflowEngine, WorkflowStatus, TaskStatus
from .advanced_logging import get_advanced_logger

@dataclass
class WorkflowAlert:
    """Alerte de workflow"""
    id: str
    workflow_id: str
    alert_type: str  # "timeout", "failure", "high_memory", "slow_task"
    message: str
    severity: str  # "low", "medium", "high", "critical"
    timestamp: datetime = field(default_factory=datetime.now)
    acknowledged: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class WorkflowMetrics:
    """Métriques d'un workflow"""
    workflow_id: str
    workflow_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: Optional[float] = None
    status: str = ""
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    success_rate: float = 0.0
    avg_task_duration: float = 0.0
    peak_memory_mb: float = 0.0
    cpu_usage_percent: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

class WorkflowMonitor:
    """Moniteur de workflows en temps réel"""
    
    def __init__(self, workflow_engine: WorkflowEngine, 
                 metrics_file: str = "logs/workflow_metrics.json",
                 alerts_file: str = "logs/workflow_alerts.json"):
        self.workflow_engine = workflow_engine
        self.metrics_file = Path(metrics_file)
        self.alerts_file = Path(alerts_file)
        self.metrics_file.parent.mkdir(exist_ok=True)
        self.alerts_file.parent.mkdir(exist_ok=True)
        
        self.advanced_logger = get_advanced_logger()
        
        # État de monitoring
        self.active_workflows: Dict[str, WorkflowMetrics] = {}
        self.completed_workflows: deque = deque(maxlen=100)  # Garde les 100 derniers
        self.alerts: List[WorkflowAlert] = []
        self.alert_handlers: Dict[str, List[Callable]] = defaultdict(list)
        
        # Configuration des seuils
        self.alert_thresholds = {
            "task_timeout_minutes": 30,
            "workflow_timeout_hours": 4,
            "memory_threshold_mb": 1000,
            "cpu_threshold_percent": 80,
            "failure_rate_threshold": 0.2  # 20%
        }
        
        # Thread de monitoring
        self.monitoring_active = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.lock = threading.Lock()
    
    def start_monitoring(self):
        """Démarre le monitoring"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        self.advanced_logger.app_logger.info("Monitoring de workflows démarré")
    
    def stop_monitoring(self):
        """Arrête le monitoring"""
        self.monitoring_active = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5.0)
        
        self.advanced_logger.app_logger.info("Monitoring de workflows arrêté")
    
    def add_alert_handler(self, alert_type: str, handler: Callable[[WorkflowAlert], None]):
        """Ajoute un gestionnaire d'alerte"""
        self.alert_handlers[alert_type].append(handler)
    
    def _monitor_loop(self):
        """Boucle principale de monitoring"""
        while self.monitoring_active:
            try:
                self._update_metrics()
                self._check_alerts()
                self._cleanup_old_data()
                time.sleep(5)  # Vérification toutes les 5 secondes
            except Exception as e:
                self.advanced_logger.error_logger.error(f"Erreur monitoring: {e}")
                time.sleep(10)  # Attendre plus longtemps en cas d'erreur
    
    def _update_metrics(self):
        """Met à jour les métriques des workflows actifs"""
        with self.lock:
            # Récupérer tous les workflows du moteur
            for workflow_id, workflow in self.workflow_engine.workflows.items():
                if workflow_id not in self.active_workflows and workflow.status == WorkflowStatus.RUNNING:
                    # Nouveau workflow actif
                    metrics = WorkflowMetrics(
                        workflow_id=workflow_id,
                        workflow_name=workflow.name,
                        start_time=workflow.started_at or datetime.now(),
                        total_tasks=len(workflow.tasks),
                        metadata=workflow.metadata
                    )
                    self.active_workflows[workflow_id] = metrics
                
                elif workflow_id in self.active_workflows:
                    # Mettre à jour workflow existant
                    metrics = self.active_workflows[workflow_id]
                    metrics.status = workflow.status.value
                    metrics.completed_tasks = sum(1 for t in workflow.tasks if t.status == TaskStatus.COMPLETED)
                    metrics.failed_tasks = sum(1 for t in workflow.tasks if t.status == TaskStatus.FAILED)
                    
                    if metrics.total_tasks > 0:
                        metrics.success_rate = metrics.completed_tasks / metrics.total_tasks
                    
                    # Calculer durée moyenne des tâches
                    completed_task_durations = []
                    for task in workflow.tasks:
                        if task.status == TaskStatus.COMPLETED and task.start_time and task.end_time:
                            duration = (task.end_time - task.start_time).total_seconds()
                            completed_task_durations.append(duration)
                    
                    if completed_task_durations:
                        metrics.avg_task_duration = sum(completed_task_durations) / len(completed_task_durations)
                    
                    # Workflow terminé
                    if workflow.status in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED, WorkflowStatus.CANCELLED]:
                        metrics.end_time = workflow.completed_at or datetime.now()
                        metrics.duration = (metrics.end_time - metrics.start_time).total_seconds()
                        
                        # Déplacer vers les workflows terminés
                        self.completed_workflows.append(metrics)
                        del self.active_workflows[workflow_id]
                        
                        # Logger la completion
                        self._log_workflow_metrics(metrics)
    
    def _check_alerts(self):
        """Vérifie les conditions d'alerte"""
        current_time = datetime.now()
        
        with self.lock:
            for workflow_id, metrics in self.active_workflows.items():
                workflow = self.workflow_engine.workflows.get(workflow_id)
                if not workflow:
                    continue
                
                # Vérifier timeout de workflow
                workflow_duration = (current_time - metrics.start_time).total_seconds() / 3600  # heures
                if workflow_duration > self.alert_thresholds["workflow_timeout_hours"]:
                    self._create_alert(
                        workflow_id=workflow_id,
                        alert_type="workflow_timeout",
                        message=f"Workflow '{metrics.workflow_name}' dépasse {self.alert_thresholds['workflow_timeout_hours']}h",
                        severity="high"
                    )
                
                # Vérifier échecs de tâches
                if metrics.total_tasks > 0 and metrics.failed_tasks / metrics.total_tasks > self.alert_thresholds["failure_rate_threshold"]:
                    self._create_alert(
                        workflow_id=workflow_id,
                        alert_type="high_failure_rate",
                        message=f"Taux d'échec élevé: {metrics.failed_tasks}/{metrics.total_tasks}",
                        severity="medium"
                    )
                
                # Vérifier timeout des tâches individuelles
                for task in workflow.tasks:
                    if (task.status == TaskStatus.RUNNING and 
                        task.start_time and
                        (current_time - task.start_time).total_seconds() > self.alert_thresholds["task_timeout_minutes"] * 60):
                        
                        self._create_alert(
                            workflow_id=workflow_id,
                            alert_type="task_timeout",
                            message=f"Tâche '{task.name}' dépasse {self.alert_thresholds['task_timeout_minutes']} minutes",
                            severity="medium",
                            metadata={"task_id": task.id, "task_name": task.name}
                        )
                
                # Vérifications de performance système (si disponible)
                try:
                    import psutil
                    memory_mb = psutil.virtual_memory().used / 1024 / 1024
                    cpu_percent = psutil.cpu_percent(interval=0.1)
                    
                    metrics.peak_memory_mb = max(metrics.peak_memory_mb, memory_mb)
                    metrics.cpu_usage_percent = cpu_percent
                    
                    if memory_mb > self.alert_thresholds["memory_threshold_mb"]:
                        self._create_alert(
                            workflow_id=workflow_id,
                            alert_type="high_memory",
                            message=f"Utilisation mémoire élevée: {memory_mb:.0f} MB",
                            severity="medium"
                        )
                    
                    if cpu_percent > self.alert_thresholds["cpu_threshold_percent"]:
                        self._create_alert(
                            workflow_id=workflow_id,
                            alert_type="high_cpu",
                            message=f"Utilisation CPU élevée: {cpu_percent:.1f}%",
                            severity="low"
                        )
                
                except ImportError:
                    pass  # psutil non disponible
    
    def _create_alert(self, workflow_id: str, alert_type: str, message: str, 
                     severity: str, metadata: Dict[str, Any] = None):
        """Crée une nouvelle alerte"""
        alert_id = f"{alert_type}_{workflow_id}_{int(time.time())}"
        
        # Vérifier si une alerte similaire existe déjà (éviter le spam)
        recent_alerts = [
            a for a in self.alerts 
            if (a.workflow_id == workflow_id and 
                a.alert_type == alert_type and 
                (datetime.now() - a.timestamp).total_seconds() < 300)  # 5 minutes
        ]
        
        if recent_alerts:
            return  # Éviter les alertes dupliquées
        
        alert = WorkflowAlert(
            id=alert_id,
            workflow_id=workflow_id,
            alert_type=alert_type,
            message=message,
            severity=severity,
            metadata=metadata or {}
        )
        
        self.alerts.append(alert)
        
        # Déclencher les gestionnaires d'alerte
        for handler in self.alert_handlers[alert_type]:
            try:
                handler(alert)
            except Exception as e:
                self.advanced_logger.error_logger.error(f"Erreur gestionnaire alerte: {e}")
        
        # Logger l'alerte
        self.advanced_logger.app_logger.warning(f"Alerte workflow: {message}")
        self._log_alert(alert)
    
    def _log_workflow_metrics(self, metrics: WorkflowMetrics):
        """Enregistre les métriques d'un workflow"""
        try:
            metrics_data = {
                "timestamp": datetime.now().isoformat(),
                "workflow_id": metrics.workflow_id,
                "workflow_name": metrics.workflow_name,
                "duration": metrics.duration,
                "total_tasks": metrics.total_tasks,
                "completed_tasks": metrics.completed_tasks,
                "failed_tasks": metrics.failed_tasks,
                "success_rate": metrics.success_rate,
                "avg_task_duration": metrics.avg_task_duration,
                "peak_memory_mb": metrics.peak_memory_mb,
                "status": metrics.status
            }
            
            with open(self.metrics_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(metrics_data, ensure_ascii=False) + "\n")
        
        except Exception as e:
            self.advanced_logger.error_logger.error(f"Erreur log métriques: {e}")
    
    def _log_alert(self, alert: WorkflowAlert):
        """Enregistre une alerte"""
        try:
            alert_data = {
                "timestamp": alert.timestamp.isoformat(),
                "alert_id": alert.id,
                "workflow_id": alert.workflow_id,
                "alert_type": alert.alert_type,
                "message": alert.message,
                "severity": alert.severity,
                "metadata": alert.metadata
            }
            
            with open(self.alerts_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(alert_data, ensure_ascii=False) + "\n")
        
        except Exception as e:
            self.advanced_logger.error_logger.error(f"Erreur log alerte: {e}")
    
    def _cleanup_old_data(self):
        """Nettoie les anciennes données"""
        cutoff_time = datetime.now() - timedelta(hours=24)
        
        with self.lock:
            # Nettoyer les anciennes alertes
            self.alerts = [
                alert for alert in self.alerts 
                if alert.timestamp > cutoff_time or not alert.acknowledged
            ]
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Retourne les données pour le dashboard"""
        with self.lock:
            # Statistiques globales
            total_workflows_today = len([
                w for w in self.completed_workflows 
                if w.start_time.date() == datetime.now().date()
            ])
            
            successful_workflows_today = len([
                w for w in self.completed_workflows 
                if (w.start_time.date() == datetime.now().date() and 
                    w.status == WorkflowStatus.COMPLETED.value)
            ])
            
            active_alerts = [a for a in self.alerts if not a.acknowledged]
            
            return {
                "timestamp": datetime.now().isoformat(),
                "active_workflows": len(self.active_workflows),
                "workflows_today": total_workflows_today,
                "success_rate_today": (successful_workflows_today / total_workflows_today) if total_workflows_today > 0 else 0,
                "active_alerts": len(active_alerts),
                "critical_alerts": len([a for a in active_alerts if a.severity == "critical"]),
                "workflow_details": [
                    {
                        "id": metrics.workflow_id,
                        "name": metrics.workflow_name,
                        "status": metrics.status,
                        "progress": (metrics.completed_tasks / metrics.total_tasks) * 100 if metrics.total_tasks > 0 else 0,
                        "duration": (datetime.now() - metrics.start_time).total_seconds(),
                        "tasks": f"{metrics.completed_tasks}/{metrics.total_tasks}"
                    }
                    for metrics in self.active_workflows.values()
                ],
                "recent_alerts": [
                    {
                        "type": alert.alert_type,
                        "message": alert.message,
                        "severity": alert.severity,
                        "timestamp": alert.timestamp.isoformat(),
                        "workflow_name": next(
                            (m.workflow_name for m in self.active_workflows.values() if m.workflow_id == alert.workflow_id),
                            "Workflow terminé"
                        )
                    }
                    for alert in sorted(active_alerts, key=lambda a: a.timestamp, reverse=True)[:10]
                ]
            }
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acquitte une alerte"""
        with self.lock:
            for alert in self.alerts:
                if alert.id == alert_id:
                    alert.acknowledged = True
                    self.advanced_logger.app_logger.info(f"Alerte acquittée: {alert_id}")
                    return True
        return False
    
    def get_workflow_history(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Retourne l'historique des workflows"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        with self.lock:
            recent_workflows = [
                {
                    "workflow_id": metrics.workflow_id,
                    "workflow_name": metrics.workflow_name,
                    "status": metrics.status,
                    "start_time": metrics.start_time.isoformat(),
                    "end_time": metrics.end_time.isoformat() if metrics.end_time else None,
                    "duration": metrics.duration,
                    "total_tasks": metrics.total_tasks,
                    "completed_tasks": metrics.completed_tasks,
                    "failed_tasks": metrics.failed_tasks,
                    "success_rate": metrics.success_rate
                }
                for metrics in self.completed_workflows
                if metrics.start_time > cutoff_time
            ]
        
        return sorted(recent_workflows, key=lambda w: w["start_time"], reverse=True)

# Instance globale
workflow_monitor = None

def get_workflow_monitor(workflow_engine: WorkflowEngine = None) -> WorkflowMonitor:
    """Retourne l'instance du moniteur de workflow"""
    global workflow_monitor
    if workflow_monitor is None:
        from .workflow_engine import get_workflow_engine
        engine = workflow_engine or get_workflow_engine()
        workflow_monitor = WorkflowMonitor(engine)
    return workflow_monitor