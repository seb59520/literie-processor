#!/usr/bin/env python3
"""
Utilitaires pour la gestion des assets (images, icônes, etc.)
Compatible avec PyInstaller et le mode développement
"""

import os
import sys
from typing import Optional


def get_asset_path(relative_path: str) -> Optional[str]:
    """
    Retourne le chemin absolu vers un asset, compatible avec PyInstaller et le mode développement.
    
    Args:
        relative_path (str): Chemin relatif depuis le dossier assets (ex: "lit-double.png")
    
    Returns:
        str: Chemin absolu vers l'asset, ou None si non trouvé
    """
    try:
        # Vérifier si on est dans un exécutable PyInstaller
        if hasattr(sys, '_MEIPASS'):
            # Mode exécutable PyInstaller
            base_path = sys._MEIPASS
        else:
            # Mode développement - remonter d'un niveau depuis backend/
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Construire le chemin complet
        asset_path = os.path.join(base_path, 'assets', relative_path)
        
        # Vérifier que le fichier existe
        if os.path.exists(asset_path):
            return asset_path
        
        # Fallback: essayer le chemin relatif direct
        fallback_path = os.path.join('assets', relative_path)
        if os.path.exists(fallback_path):
            return fallback_path
        
        # Fallback: essayer depuis le répertoire courant
        current_path = os.path.join(os.getcwd(), 'assets', relative_path)
        if os.path.exists(current_path):
            return current_path
        
        print(f"⚠️ Asset non trouvé: {relative_path}")
        print(f"   Tentatives: {asset_path}, {fallback_path}, {current_path}")
        return None
        
    except Exception as e:
        print(f"Erreur lors de la résolution du chemin asset '{relative_path}': {e}")
        return None


def get_template_path(relative_path: str) -> Optional[str]:
    """
    Retourne le chemin absolu vers un fichier template, compatible avec PyInstaller.
    
    Args:
        relative_path (str): Chemin relatif depuis le dossier template (ex: "template_matelas.xlsx")
    
    Returns:
        str: Chemin absolu vers le template, ou None si non trouvé
    """
    try:
        # Vérifier si on est dans un exécutable PyInstaller
        if hasattr(sys, '_MEIPASS'):
            # Mode exécutable PyInstaller
            base_path = sys._MEIPASS
        else:
            # Mode développement - remonter d'un niveau depuis backend/
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Construire le chemin complet
        template_path = os.path.join(base_path, 'template', relative_path)
        
        # Vérifier que le fichier existe
        if os.path.exists(template_path):
            return template_path
        
        # Fallback: essayer le chemin relatif direct
        fallback_path = os.path.join('template', relative_path)
        if os.path.exists(fallback_path):
            return fallback_path
        
        print(f"⚠️ Template non trouvé: {relative_path}")
        return None
        
    except Exception as e:
        print(f"Erreur lors de la résolution du chemin template '{relative_path}': {e}")
        return None


def get_config_path(relative_path: str) -> Optional[str]:
    """
    Retourne le chemin absolu vers un fichier de configuration, compatible avec PyInstaller.
    
    Args:
        relative_path (str): Chemin relatif depuis le dossier config (ex: "mappings_matelas.json")
    
    Returns:
        str: Chemin absolu vers le fichier de config, ou None si non trouvé
    """
    try:
        # Vérifier si on est dans un exécutable PyInstaller
        if hasattr(sys, '_MEIPASS'):
            # Mode exécutable PyInstaller
            base_path = sys._MEIPASS
        else:
            # Mode développement - remonter d'un niveau depuis backend/
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Construire le chemin complet
        config_path = os.path.join(base_path, 'config', relative_path)
        
        # Vérifier que le fichier existe
        if os.path.exists(config_path):
            return config_path
        
        # Fallback: essayer le chemin relatif direct
        fallback_path = os.path.join('config', relative_path)
        if os.path.exists(fallback_path):
            return fallback_path
        
        print(f"⚠️ Fichier de config non trouvé: {relative_path}")
        return None
        
    except Exception as e:
        print(f"Erreur lors de la résolution du chemin config '{relative_path}': {e}")
        return None


def get_referentiel_path(relative_path: str) -> Optional[str]:
    """
    Retourne le chemin absolu vers un fichier référentiel, compatible avec PyInstaller.
    
    Args:
        relative_path (str): Chemin relatif depuis le dossier Référentiels (ex: "dimensions_matelas.json")
    
    Returns:
        str: Chemin absolu vers le fichier référentiel, ou None si non trouvé
    """
    try:
        # Vérifier si on est dans un exécutable PyInstaller
        if hasattr(sys, '_MEIPASS'):
            # Mode exécutable PyInstaller
            base_path = sys._MEIPASS
        else:
            # Mode développement - remonter d'un niveau depuis backend/
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Construire le chemin complet (backend/Référentiels/ dans l'exécutable)
        referentiel_path = os.path.join(base_path, 'backend', 'Référentiels', relative_path)
        
        # Vérifier que le fichier existe
        if os.path.exists(referentiel_path):
            return referentiel_path
        
        # Fallback: essayer le chemin relatif direct (pour compatibilité)
        fallback_path = os.path.join('backend', 'Référentiels', relative_path)
        if os.path.exists(fallback_path):
            return fallback_path
        
        # Fallback: essayer depuis le répertoire courant
        current_path = os.path.join(os.getcwd(), 'backend', 'Référentiels', relative_path)
        if os.path.exists(current_path):
            return current_path
        
        print(f"⚠️ Fichier référentiel non trouvé: {relative_path}")
        print(f"   Tentatives: {referentiel_path}, {fallback_path}, {current_path}")
        return None
        
    except Exception as e:
        print(f"Erreur lors de la résolution du chemin référentiel '{relative_path}': {e}")
        return None


def is_pyinstaller_mode() -> bool:
    """
    Vérifie si l'application s'exécute en mode PyInstaller.
    
    Returns:
        bool: True si en mode PyInstaller, False sinon
    """
    return hasattr(sys, '_MEIPASS')


def get_base_path() -> str:
    """
    Retourne le chemin de base de l'application.
    
    Returns:
        str: Chemin de base
    """
    if hasattr(sys, '_MEIPASS'):
        # Mode exécutable PyInstaller
        return sys._MEIPASS
    else:
        # Mode développement - remonter d'un niveau depuis backend/
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 