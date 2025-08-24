#!/usr/bin/env python3
"""
Moteur de workflow automatisé pour traitement par lots
"""

import json
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import queue
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

class WorkflowStatus(Enum):
    """Statut d'un workflow"""
    PENDING = "pending"
    RUNNING = "running" 
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"

class TaskStatus(Enum):
    """Statut d'une tâche"""
    WAITING = "waiting"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class WorkflowTask:
    """Tâche dans un workflow"""
    id: str
    name: str
    function: Callable
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)
    depends_on: List[str] = field(default_factory=list)
    timeout: Optional[int] = None
    retry_count: int = 0
    max_retries: int = 3
    status: TaskStatus = TaskStatus.WAITING
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    result: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Workflow:
    """Définition d'un workflow"""
    id: str
    name: str
    description: str
    tasks: List[WorkflowTask] = field(default_factory=list)
    status: WorkflowStatus = WorkflowStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    priority: int = 0  # Plus élevé = plus prioritaire
    max_concurrent_tasks: int = 3
    auto_retry: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

class WorkflowEngine:
    """Moteur d'exécution de workflows"""
    
    def __init__(self, max_workers: int = 5, log_file: str = "logs/workflows.json"):
        self.max_workers = max_workers
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(exist_ok=True)
        
        # État interne
        self.workflows: Dict[str, Workflow] = {}
        self.workflow_queue = queue.PriorityQueue()
        self.running_workflows: Dict[str, ThreadPoolExecutor] = {}
        
        # Contrôles
        self.is_running = False
        self.lock = threading.Lock()
        
        # Thread principal du moteur
        self.engine_thread: Optional[threading.Thread] = None
        
    def start(self):
        """Démarre le moteur de workflow"""
        if self.is_running:
            return
            
        self.is_running = True
        self.engine_thread = threading.Thread(target=self._run_engine, daemon=True)
        self.engine_thread.start()
        self._log("Moteur de workflow démarré")
    
    def stop(self):
        """Arrête le moteur de workflow"""
        self.is_running = False
        
        # Arrêter tous les workflows en cours
        with self.lock:
            for workflow_id, executor in self.running_workflows.items():
                executor.shutdown(wait=False)
                self._log(f"Workflow {workflow_id} arrêté")
        
        if self.engine_thread and self.engine_thread.is_alive():
            self.engine_thread.join(timeout=5.0)
        
        self._log("Moteur de workflow arrêté")
    
    def submit_workflow(self, workflow: Workflow) -> str:
        """Soumet un workflow pour exécution"""
        with self.lock:
            self.workflows[workflow.id] = workflow
        
        # Ajouter à la queue avec priorité
        priority = -workflow.priority  # Queue utilise min-heap, on inverse
        self.workflow_queue.put((priority, workflow.created_at, workflow.id))
        
        self._log(f"Workflow soumis: {workflow.name} (ID: {workflow.id})")
        return workflow.id
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Récupère le statut d'un workflow"""
        with self.lock:
            if workflow_id not in self.workflows:
                return None
            
            workflow = self.workflows[workflow_id]
            return {
                "id": workflow.id,
                "name": workflow.name,
                "status": workflow.status.value,
                "created_at": workflow.created_at.isoformat(),
                "started_at": workflow.started_at.isoformat() if workflow.started_at else None,
                "completed_at": workflow.completed_at.isoformat() if workflow.completed_at else None,
                "tasks": [
                    {
                        "id": task.id,
                        "name": task.name,
                        "status": task.status.value,
                        "start_time": task.start_time.isoformat() if task.start_time else None,
                        "end_time": task.end_time.isoformat() if task.end_time else None,
                        "error": task.error
                    }
                    for task in workflow.tasks
                ],
                "progress": self._calculate_progress(workflow)
            }
    
    def cancel_workflow(self, workflow_id: str) -> bool:
        """Annule un workflow"""
        with self.lock:
            if workflow_id not in self.workflows:
                return False
            
            workflow = self.workflows[workflow_id]
            
            if workflow.status in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED]:
                return False
            
            workflow.status = WorkflowStatus.CANCELLED
            
            # Arrêter l'exécuteur si en cours
            if workflow_id in self.running_workflows:
                self.running_workflows[workflow_id].shutdown(wait=False)
                del self.running_workflows[workflow_id]
            
            self._log(f"Workflow annulé: {workflow.name}")
            return True
    
    def _run_engine(self):
        """Boucle principale du moteur"""
        while self.is_running:
            try:
                # Récupérer le prochain workflow (timeout pour vérifier is_running)
                try:
                    priority, created_at, workflow_id = self.workflow_queue.get(timeout=1.0)
                except queue.Empty:
                    continue
                
                with self.lock:
                    if workflow_id not in self.workflows:
                        continue
                    
                    workflow = self.workflows[workflow_id]
                    
                    # Vérifier si le workflow peut être exécuté
                    if workflow.status != WorkflowStatus.PENDING:
                        continue
                    
                    # Limiter le nombre de workflows simultanés
                    if len(self.running_workflows) >= self.max_workers:
                        # Remettre en queue
                        self.workflow_queue.put((priority, created_at, workflow_id))
                        time.sleep(0.1)
                        continue
                
                # Démarrer l'exécution du workflow
                self._start_workflow_execution(workflow)
                
            except Exception as e:
                self._log(f"Erreur dans le moteur: {e}")
    
    def _start_workflow_execution(self, workflow: Workflow):
        """Démarre l'exécution d'un workflow"""
        workflow.status = WorkflowStatus.RUNNING
        workflow.started_at = datetime.now()
        
        executor = ThreadPoolExecutor(max_workers=workflow.max_concurrent_tasks)
        
        with self.lock:
            self.running_workflows[workflow.id] = executor
        
        # Lancer l'exécution dans un thread séparé
        execution_thread = threading.Thread(
            target=self._execute_workflow,
            args=(workflow, executor),
            daemon=True
        )
        execution_thread.start()
        
        self._log(f"Exécution démarrée: {workflow.name}")
    
    def _execute_workflow(self, workflow: Workflow, executor: ThreadPoolExecutor):
        """Exécute un workflow complet"""
        try:
            # Créer un graphe de dépendances
            dependency_graph = self._build_dependency_graph(workflow.tasks)
            completed_tasks = set()
            futures = {}
            
            while len(completed_tasks) < len(workflow.tasks) and workflow.status == WorkflowStatus.RUNNING:
                # Trouver les tâches prêtes à être exécutées
                ready_tasks = [
                    task for task in workflow.tasks
                    if (task.status == TaskStatus.WAITING and
                        all(dep_id in completed_tasks for dep_id in task.depends_on) and
                        task.id not in futures)
                ]
                
                # Soumettre les tâches prêtes
                for task in ready_tasks:
                    if len(futures) < workflow.max_concurrent_tasks:
                        future = executor.submit(self._execute_task, task)
                        futures[task.id] = future
                        task.status = TaskStatus.RUNNING
                        task.start_time = datetime.now()
                
                # Vérifier les tâches terminées
                completed_futures = []
                for task_id, future in futures.items():
                    if future.done():
                        completed_futures.append(task_id)
                        task = next(t for t in workflow.tasks if t.id == task_id)
                        
                        try:
                            result = future.result()
                            task.result = result
                            task.status = TaskStatus.COMPLETED
                            task.end_time = datetime.now()
                            completed_tasks.add(task_id)
                            
                        except Exception as e:
                            task.error = str(e)
                            task.end_time = datetime.now()
                            
                            # Retry si configuré
                            if workflow.auto_retry and task.retry_count < task.max_retries:
                                task.retry_count += 1
                                task.status = TaskStatus.WAITING
                                self._log(f"Retry tâche {task.name} (tentative {task.retry_count})")
                            else:
                                task.status = TaskStatus.FAILED
                                # Arrêter le workflow si une tâche critique échoue
                                if not task.metadata.get('optional', False):
                                    workflow.status = WorkflowStatus.FAILED
                                    break
                
                # Nettoyer les futures terminées
                for task_id in completed_futures:
                    del futures[task_id]
                
                time.sleep(0.1)  # Éviter la consommation CPU excessive
            
            # Finaliser le workflow
            if workflow.status == WorkflowStatus.RUNNING:
                if len(completed_tasks) == len(workflow.tasks):
                    workflow.status = WorkflowStatus.COMPLETED
                else:
                    workflow.status = WorkflowStatus.FAILED
            
            workflow.completed_at = datetime.now()
            
        except Exception as e:
            workflow.status = WorkflowStatus.FAILED
            workflow.completed_at = datetime.now()
            self._log(f"Erreur workflow {workflow.name}: {e}")
        
        finally:
            executor.shutdown(wait=True)
            with self.lock:
                if workflow.id in self.running_workflows:
                    del self.running_workflows[workflow.id]
            
            self._log_workflow_completion(workflow)
    
    def _execute_task(self, task: WorkflowTask) -> Any:
        """Exécute une tâche individuelle"""
        try:
            self._log(f"Démarrage tâche: {task.name}")
            result = task.function(*task.args, **task.kwargs)
            self._log(f"Tâche terminée: {task.name}")
            return result
        except Exception as e:
            self._log(f"Erreur tâche {task.name}: {e}")
            raise
    
    def _build_dependency_graph(self, tasks: List[WorkflowTask]) -> Dict[str, List[str]]:
        """Construit le graphe de dépendances"""
        graph = {}
        for task in tasks:
            graph[task.id] = task.depends_on.copy()
        return graph
    
    def _calculate_progress(self, workflow: Workflow) -> float:
        """Calcule le pourcentage de progression"""
        if not workflow.tasks:
            return 0.0
        
        completed = sum(1 for task in workflow.tasks if task.status == TaskStatus.COMPLETED)
        return (completed / len(workflow.tasks)) * 100
    
    def _log(self, message: str):
        """Enregistre un message dans les logs"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "message": message
        }
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except Exception:
            pass  # Éviter les boucles d'erreur dans le logging
    
    def _log_workflow_completion(self, workflow: Workflow):
        """Enregistre la completion d'un workflow"""
        duration = (workflow.completed_at - workflow.started_at).total_seconds()
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "workflow_completed",
            "workflow_id": workflow.id,
            "workflow_name": workflow.name,
            "status": workflow.status.value,
            "duration_seconds": duration,
            "tasks_completed": sum(1 for t in workflow.tasks if t.status == TaskStatus.COMPLETED),
            "tasks_failed": sum(1 for t in workflow.tasks if t.status == TaskStatus.FAILED),
            "total_tasks": len(workflow.tasks)
        }
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except Exception:
            pass

# Instance globale
workflow_engine = None

def get_workflow_engine() -> WorkflowEngine:
    """Retourne l'instance du moteur de workflow"""
    global workflow_engine
    if workflow_engine is None:
        workflow_engine = WorkflowEngine()
    return workflow_engine