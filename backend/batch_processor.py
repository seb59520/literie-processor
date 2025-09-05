#!/usr/bin/env python3
"""
Système de traitement par lots pour fichiers PDF
"""

import os
import time
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

from .workflow_engine import Workflow, WorkflowTask, WorkflowEngine, get_workflow_engine
from .advanced_logging import get_advanced_logger

@dataclass
class BatchJob:
    """Travail de traitement par lots"""
    id: str
    name: str
    files: List[str]
    config: Dict[str, Any]
    priority: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    scheduled_at: Optional[datetime] = None
    auto_retry: bool = True
    max_retries: int = 3
    metadata: Dict[str, Any] = field(default_factory=dict)

class BatchProcessor:
    """Processeur de lots pour fichiers PDF"""
    
    def __init__(self):
        self.workflow_engine = get_workflow_engine()
        self.advanced_logger = get_advanced_logger()
        self.batch_jobs: Dict[str, BatchJob] = {}
        self.lock = threading.Lock()
        
        # Démarrer le moteur si pas déjà fait
        if not self.workflow_engine.is_running:
            self.workflow_engine.start()
    
    def create_batch_job(self, job: BatchJob) -> str:
        """Crée un nouveau travail par lots"""
        with self.lock:
            self.batch_jobs[job.id] = job
        
        # Créer le workflow correspondant
        workflow = self._create_workflow_from_batch(job)
        workflow_id = self.workflow_engine.submit_workflow(workflow)
        
        self.advanced_logger.processing_logger.info(
            f"Travail par lots créé: {job.name} ({len(job.files)} fichiers)"
        )
        
        return workflow_id
    
    def create_pdf_processing_batch(self, files: List[str], config: Dict[str, Any], 
                                  job_name: str = None, priority: int = 0) -> str:
        """Crée un lot de traitement PDF"""
        
        job_id = f"batch_{int(time.time())}_{len(files)}"
        job_name = job_name or f"Traitement {len(files)} fichiers PDF"
        
        batch_job = BatchJob(
            id=job_id,
            name=job_name,
            files=files,
            config=config,
            priority=priority,
            metadata={
                "file_count": len(files),
                "estimated_duration": len(files) * 30,  # 30s par fichier estimé
                "batch_type": "pdf_processing"
            }
        )
        
        return self.create_batch_job(batch_job)
    
    def create_scheduled_batch(self, files: List[str], config: Dict[str, Any],
                             schedule_time: datetime, job_name: str = None) -> str:
        """Crée un lot programmé"""
        
        job_id = f"scheduled_{int(time.time())}"
        job_name = job_name or f"Lot programmé - {len(files)} fichiers"
        
        batch_job = BatchJob(
            id=job_id,
            name=job_name,
            files=files,
            config=config,
            scheduled_at=schedule_time,
            metadata={
                "scheduled": True,
                "schedule_time": schedule_time.isoformat()
            }
        )
        
        # Calculer le délai avant exécution
        delay = (schedule_time - datetime.now()).total_seconds()
        
        if delay > 0:
            # Programmer l'exécution
            timer = threading.Timer(delay, self._execute_scheduled_batch, [batch_job])
            timer.daemon = True
            timer.start()
            
            self.advanced_logger.app_logger.info(
                f"Lot programmé pour {schedule_time}: {job_name}"
            )
        else:
            # Exécuter immédiatement si l'heure est dépassée
            return self.create_batch_job(batch_job)
        
        return job_id
    
    def _execute_scheduled_batch(self, batch_job: BatchJob):
        """Exécute un lot programmé"""
        self.advanced_logger.app_logger.info(
            f"Exécution lot programmé: {batch_job.name}"
        )
        self.create_batch_job(batch_job)
    
    def _create_workflow_from_batch(self, batch_job: BatchJob) -> Workflow:
        """Crée un workflow à partir d'un batch job"""
        
        workflow = Workflow(
            id=f"workflow_{batch_job.id}",
            name=batch_job.name,
            description=f"Traitement par lots de {len(batch_job.files)} fichiers",
            priority=batch_job.priority,
            max_concurrent_tasks=min(3, len(batch_job.files)),  # Max 3 fichiers simultanés
            auto_retry=batch_job.auto_retry,
            metadata=batch_job.metadata
        )
        
        # Tâche de préparation
        prep_task = WorkflowTask(
            id="prep_batch",
            name="Préparation du lot",
            function=self._prepare_batch,
            args=(batch_job,),
            metadata={"stage": "preparation"}
        )
        workflow.tasks.append(prep_task)
        
        # Tâches de validation des fichiers
        validation_tasks = []
        for i, file_path in enumerate(batch_job.files):
            task = WorkflowTask(
                id=f"validate_{i}",
                name=f"Validation {os.path.basename(file_path)}",
                function=self._validate_file,
                args=(file_path, batch_job.config),
                depends_on=["prep_batch"],
                metadata={"stage": "validation", "file_index": i, "file_path": file_path}
            )
            validation_tasks.append(task)
            workflow.tasks.append(task)
        
        # Tâche de regroupement des validations
        validation_ids = [task.id for task in validation_tasks]
        consolidation_task = WorkflowTask(
            id="consolidate_validation",
            name="Consolidation validation",
            function=self._consolidate_validation,
            args=(validation_ids,),
            depends_on=validation_ids,
            metadata={"stage": "consolidation"}
        )
        workflow.tasks.append(consolidation_task)
        
        # Tâches de traitement par groupes
        if len(batch_job.files) > 5:
            # Traiter par groupes de 5 fichiers max
            processing_tasks = self._create_group_processing_tasks(batch_job, ["consolidate_validation"])
        else:
            # Traitement individuel
            processing_tasks = self._create_individual_processing_tasks(batch_job, ["consolidate_validation"])
        
        workflow.tasks.extend(processing_tasks)
        
        # Tâche de finalisation
        processing_ids = [task.id for task in processing_tasks]
        finalization_task = WorkflowTask(
            id="finalize_batch",
            name="Finalisation du lot",
            function=self._finalize_batch,
            args=(batch_job, processing_ids),
            depends_on=processing_ids,
            metadata={"stage": "finalization"}
        )
        workflow.tasks.append(finalization_task)
        
        return workflow
    
    def _create_individual_processing_tasks(self, batch_job: BatchJob, dependencies: List[str]) -> List[WorkflowTask]:
        """Crée des tâches de traitement individuelles"""
        tasks = []
        
        for i, file_path in enumerate(batch_job.files):
            task = WorkflowTask(
                id=f"process_{i}",
                name=f"Traitement {os.path.basename(file_path)}",
                function=self._process_single_file,
                args=(file_path, batch_job.config),
                depends_on=dependencies,
                timeout=300,  # 5 minutes max par fichier
                max_retries=batch_job.max_retries,
                metadata={"stage": "processing", "file_index": i, "file_path": file_path}
            )
            tasks.append(task)
        
        return tasks
    
    def _create_group_processing_tasks(self, batch_job: BatchJob, dependencies: List[str]) -> List[WorkflowTask]:
        """Crée des tâches de traitement par groupes"""
        tasks = []
        group_size = 5
        
        for i in range(0, len(batch_job.files), group_size):
            group_files = batch_job.files[i:i + group_size]
            group_id = i // group_size
            
            task = WorkflowTask(
                id=f"process_group_{group_id}",
                name=f"Traitement groupe {group_id + 1} ({len(group_files)} fichiers)",
                function=self._process_file_group,
                args=(group_files, batch_job.config),
                depends_on=dependencies,
                timeout=900,  # 15 minutes max par groupe
                max_retries=batch_job.max_retries,
                metadata={
                    "stage": "processing", 
                    "group_id": group_id, 
                    "group_files": group_files,
                    "group_size": len(group_files)
                }
            )
            tasks.append(task)
        
        return tasks
    
    def _prepare_batch(self, batch_job: BatchJob) -> Dict[str, Any]:
        """Prépare un lot de traitement"""
        self.advanced_logger.processing_logger.info(
            f"Préparation lot: {batch_job.name}"
        )
        
        # Vérifier l'existence des fichiers
        existing_files = []
        missing_files = []
        
        for file_path in batch_job.files:
            if os.path.exists(file_path):
                existing_files.append(file_path)
            else:
                missing_files.append(file_path)
        
        result = {
            "total_files": len(batch_job.files),
            "existing_files": len(existing_files),
            "missing_files": missing_files,
            "preparation_time": datetime.now().isoformat()
        }
        
        if missing_files:
            self.advanced_logger.error_logger.warning(
                f"Fichiers manquants dans le lot {batch_job.name}: {missing_files}"
            )
        
        return result
    
    def _validate_file(self, file_path: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Valide un fichier individual"""
        try:
            from .file_validation import validate_pdf_file
            
            result = validate_pdf_file(file_path)
            
            return {
                "file_path": file_path,
                "is_valid": result.is_valid,
                "file_size_mb": getattr(result, 'file_size_mb', 0),
                "validation_time": datetime.now().isoformat(),
                "error": result.error_message if not result.is_valid else None
            }
            
        except Exception as e:
            self.advanced_logger.error_logger.error(
                f"Erreur validation {file_path}: {e}"
            )
            return {
                "file_path": file_path,
                "is_valid": False,
                "error": str(e),
                "validation_time": datetime.now().isoformat()
            }
    
    def _consolidate_validation(self, validation_task_ids: List[str]) -> Dict[str, Any]:
        """Consolide les résultats de validation"""
        # Cette méthode recevra les résultats via le workflow engine
        # Pour l'instant, on simule la consolidation
        
        result = {
            "consolidation_time": datetime.now().isoformat(),
            "validation_tasks_count": len(validation_task_ids),
            "status": "consolidated"
        }
        
        self.advanced_logger.processing_logger.info(
            f"Validation consolidée pour {len(validation_task_ids)} tâches"
        )
        
        return result
    
    def _process_single_file(self, file_path: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Traite un fichier individual"""
        start_time = time.time()
        
        try:
            # Simuler le traitement (à remplacer par la vraie logique)
            self.advanced_logger.processing_logger.info(
                f"Début traitement fichier: {os.path.basename(file_path)}"
            )
            
            # Ici on intégrerait avec ProcessingThread ou logique similaire
            time.sleep(2)  # Simulation
            
            duration = time.time() - start_time
            
            result = {
                "file_path": file_path,
                "processed": True,
                "duration": duration,
                "processing_time": datetime.now().isoformat(),
                "result_data": {"status": "success", "recommendations": []}
            }
            
            self.advanced_logger.processing_logger.info(
                f"Fichier traité avec succès: {os.path.basename(file_path)} ({duration:.2f}s)"
            )
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            error_msg = str(e)
            
            self.advanced_logger.error_logger.error(
                f"Erreur traitement {file_path}: {error_msg}"
            )
            
            return {
                "file_path": file_path,
                "processed": False,
                "duration": duration,
                "error": error_msg,
                "processing_time": datetime.now().isoformat()
            }
    
    def _process_file_group(self, files: List[str], config: Dict[str, Any]) -> Dict[str, Any]:
        """Traite un groupe de fichiers"""
        start_time = time.time()
        results = []
        
        self.advanced_logger.processing_logger.info(
            f"Début traitement groupe de {len(files)} fichiers"
        )
        
        for file_path in files:
            file_result = self._process_single_file(file_path, config)
            results.append(file_result)
        
        duration = time.time() - start_time
        successful = sum(1 for r in results if r.get("processed", False))
        
        group_result = {
            "group_size": len(files),
            "successful_files": successful,
            "failed_files": len(files) - successful,
            "duration": duration,
            "processing_time": datetime.now().isoformat(),
            "individual_results": results
        }
        
        self.advanced_logger.processing_logger.info(
            f"Groupe traité: {successful}/{len(files)} succès ({duration:.2f}s)"
        )
        
        return group_result
    
    def _finalize_batch(self, batch_job: BatchJob, processing_task_ids: List[str]) -> Dict[str, Any]:
        """Finalise un lot de traitement"""
        end_time = datetime.now()
        duration = (end_time - batch_job.created_at).total_seconds()
        
        result = {
            "batch_id": batch_job.id,
            "batch_name": batch_job.name,
            "total_files": len(batch_job.files),
            "processing_tasks": len(processing_task_ids),
            "duration": duration,
            "finalized_at": end_time.isoformat(),
            "status": "completed"
        }
        
        self.advanced_logger.processing_logger.info(
            f"Lot finalisé: {batch_job.name} ({duration:.2f}s, {len(batch_job.files)} fichiers)"
        )
        
        return result
    
    def get_batch_status(self, batch_id: str) -> Optional[Dict[str, Any]]:
        """Récupère le statut d'un lot"""
        with self.lock:
            if batch_id not in self.batch_jobs:
                return None
            
            batch_job = self.batch_jobs[batch_id]
        
        # Récupérer le statut du workflow correspondant
        workflow_id = f"workflow_{batch_id}"
        workflow_status = self.workflow_engine.get_workflow_status(workflow_id)
        
        return {
            "batch_id": batch_id,
            "batch_name": batch_job.name,
            "file_count": len(batch_job.files),
            "created_at": batch_job.created_at.isoformat(),
            "scheduled_at": batch_job.scheduled_at.isoformat() if batch_job.scheduled_at else None,
            "workflow_status": workflow_status,
            "metadata": batch_job.metadata
        }

# Instance globale
batch_processor = None

def get_batch_processor() -> BatchProcessor:
    """Retourne l'instance du processeur de lots"""
    global batch_processor
    if batch_processor is None:
        batch_processor = BatchProcessor()
    return batch_processor