#!/usr/bin/env python3
"""
Système de logging pour les opérations d'administration
"""

import logging
import os
from datetime import datetime

def setup_admin_logger():
    """Configure le logger pour les opérations d'administration"""
    # Créer le dossier logs s'il n'existe pas
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configuration du logger d'administration
    admin_logger = logging.getLogger("admin")
    admin_logger.setLevel(logging.INFO)
    
    # Éviter les doublons de handlers
    if not admin_logger.handlers:
        # Handler pour fichier d'administration
        admin_handler = logging.FileHandler(
            os.path.join(log_dir, 'admin_operations.log'),
            encoding='utf-8'
        )
        admin_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        admin_handler.setFormatter(formatter)
        
        # Ajouter le handler
        admin_logger.addHandler(admin_handler)
    
    return admin_logger

def log_admin_operation(operation, details, user="admin"):
    """Enregistre une opération d'administration"""
    logger = setup_admin_logger()
    message = f"Opération: {operation} | Détails: {details} | Utilisateur: {user}"
    logger.info(message)

def log_version_update(old_version, new_version, user="admin"):
    """Enregistre une mise à jour de version"""
    log_admin_operation(
        "Mise à jour de version",
        f"De {old_version} vers {new_version}",
        user
    )

def log_patch_creation(source_version, target_version, description, user="admin"):
    """Enregistre la création d'un patch"""
    log_admin_operation(
        "Création de patch",
        f"De {source_version} vers {target_version} - {description}",
        user
    )

def log_patch_application(patch_file, user="admin"):
    """Enregistre l'application d'un patch"""
    log_admin_operation(
        "Application de patch",
        f"Fichier: {patch_file}",
        user
    )

def log_admin_access(success, user="admin"):
    """Enregistre une tentative d'accès administrateur"""
    status = "Succès" if success else "Échec"
    log_admin_operation(
        "Accès administrateur",
        f"Tentative: {status}",
        user
    )

def get_admin_logs(limit=100):
    """Récupère les derniers logs d'administration"""
    log_file = "logs/admin_operations.log"
    if not os.path.exists(log_file):
        return "Aucun log d'administration disponible"
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Retourner les dernières lignes
            return ''.join(lines[-limit:])
    except Exception as e:
        return f"Erreur lors de la lecture des logs: {str(e)}" 