#!/usr/bin/env python3
"""
Système de logging avancé pour l'application Matelas
"""

import logging
import logging.handlers
import os
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import json

class MatelasLogger:
    """Système de logging avancé pour l'application"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Configuration des loggers
        self.loggers = {}
        self._setup_loggers()
        
    def _setup_loggers(self):
        """Configure tous les loggers de l'application"""
        
        # Logger principal
        self.app_logger = self._create_logger(
            "matelas_app", 
            self.log_dir / "app.log",
            level=logging.INFO
        )
        
        # Logger pour les erreurs critiques
        self.error_logger = self._create_logger(
            "matelas_errors",
            self.log_dir / "errors.log", 
            level=logging.ERROR
        )
        
        # Logger pour les performances
        self.perf_logger = self._create_logger(
            "matelas_performance",
            self.log_dir / "performance.log",
            level=logging.INFO
        )
        
        # Logger pour les API LLM
        self.llm_logger = self._create_logger(
            "matelas_llm",
            self.log_dir / "llm_calls.log",
            level=logging.INFO
        )
        
        # Logger pour le traitement des fichiers
        self.processing_logger = self._create_logger(
            "matelas_processing",
            self.log_dir / "processing.log",
            level=logging.DEBUG
        )
        
    def _create_logger(self, name: str, file_path: Path, level: int) -> logging.Logger:
        """Crée un logger avec rotation des fichiers"""
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # Éviter les doublons de handlers
        if logger.handlers:
            return logger
            
        # Handler pour fichier avec rotation
        file_handler = logging.handlers.RotatingFileHandler(
            file_path,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        
        # Handler pour console (erreurs uniquement)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.WARNING)
        
        # Format détaillé
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def log_error(self, error: Exception, context: Dict[str, Any] = None):
        """Log une erreur avec contexte complet"""
        error_data = {
            "timestamp": datetime.now().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "context": context or {}
        }
        
        self.error_logger.error(json.dumps(error_data, indent=2, ensure_ascii=False))
        
    def log_performance(self, operation: str, duration: float, details: Dict[str, Any] = None):
        """Log les métriques de performance"""
        perf_data = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "duration_seconds": duration,
            "details": details or {}
        }
        
        self.perf_logger.info(json.dumps(perf_data, ensure_ascii=False))
        
    def log_llm_call(self, provider: str, model: str, input_tokens: int, 
                     output_tokens: int, duration: float, success: bool):
        """Log les appels aux APIs LLM"""
        llm_data = {
            "timestamp": datetime.now().isoformat(),
            "provider": provider,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "duration_seconds": duration,
            "success": success
        }
        
        self.llm_logger.info(json.dumps(llm_data, ensure_ascii=False))
        
    def log_processing_start(self, files: list, config: Dict[str, Any]):
        """Log le début d'un traitement"""
        proc_data = {
            "timestamp": datetime.now().isoformat(),
            "event": "processing_start",
            "file_count": len(files),
            "files": [os.path.basename(f) for f in files],
            "config": config
        }
        
        self.processing_logger.info(json.dumps(proc_data, ensure_ascii=False))
        
    def log_processing_end(self, success: bool, duration: float, results_count: int):
        """Log la fin d'un traitement"""
        proc_data = {
            "timestamp": datetime.now().isoformat(),
            "event": "processing_end", 
            "success": success,
            "duration_seconds": duration,
            "results_count": results_count
        }
        
        self.processing_logger.info(json.dumps(proc_data, ensure_ascii=False))
        
    def get_log_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Retourne un résumé des logs des dernières heures"""
        summary = {
            "period_hours": hours,
            "timestamp": datetime.now().isoformat(),
            "error_count": 0,
            "warning_count": 0,
            "processing_count": 0,
            "llm_calls": 0,
            "avg_processing_time": 0
        }
        
        # Analyser les fichiers de logs récents
        try:
            error_file = self.log_dir / "errors.log"
            if error_file.exists():
                with open(error_file, 'r', encoding='utf-8') as f:
                    summary["error_count"] = len([line for line in f if "ERROR" in line])
                    
            # Ajouter d'autres analyses si nécessaire
            
        except Exception as e:
            self.error_logger.error(f"Erreur lors de la génération du résumé: {e}")
            
        return summary

# Instance globale
advanced_logger = None

def get_advanced_logger() -> MatelasLogger:
    """Retourne l'instance du logger avancé"""
    global advanced_logger
    if advanced_logger is None:
        advanced_logger = MatelasLogger()
    return advanced_logger

def setup_advanced_logging():
    """Configure le système de logging avancé"""
    logger = get_advanced_logger()
    logger.app_logger.info("Système de logging avancé initialisé")
    return logger