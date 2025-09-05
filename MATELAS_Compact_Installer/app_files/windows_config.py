#!/usr/bin/env python3
"""
Configuration spécifique Windows pour l'application Matelas
Optimisations et adaptations pour l'environnement Windows
"""

import os
import sys
from pathlib import Path

class WindowsConfig:
    """Configuration et utilitaires spécifiques à Windows"""
    
    def __init__(self):
        self.is_frozen = getattr(sys, 'frozen', False)
        self.bundle_dir = self._get_bundle_dir()
        
    def _get_bundle_dir(self):
        """Obtient le répertoire de l'application (différent si compilée)"""
        if self.is_frozen:
            # Si exécutable PyInstaller
            return Path(sys._MEIPASS)
        else:
            # Si script Python normal
            return Path(__file__).parent
    
    def get_config_path(self):
        """Retourne le chemin du fichier de configuration"""
        if self.is_frozen:
            # Pour l'exécutable, utiliser le dossier utilisateur
            config_dir = Path.home() / "MatelasProcessor"
            config_dir.mkdir(exist_ok=True)
            return config_dir / "matelas_config.json"
        else:
            # Pour le développement, utiliser le dossier local
            return self.bundle_dir / "matelas_config.json"
    
    def get_output_directory(self):
        """Retourne le répertoire de sortie par défaut pour Windows"""
        if self.is_frozen:
            # Pour l'exécutable, utiliser Mes Documents
            docs_dir = Path.home() / "Documents" / "MatelasProcessor"
            docs_dir.mkdir(exist_ok=True)
            return docs_dir
        else:
            # Pour le développement, utiliser output local
            output_dir = self.bundle_dir / "output"
            output_dir.mkdir(exist_ok=True)
            return output_dir
    
    def get_logs_directory(self):
        """Retourne le répertoire des logs pour Windows"""
        if self.is_frozen:
            # Pour l'exécutable, utiliser AppData
            logs_dir = Path.home() / "AppData" / "Local" / "MatelasProcessor" / "logs"
            logs_dir.mkdir(parents=True, exist_ok=True)
            return logs_dir
        else:
            # Pour le développement, utiliser logs local
            logs_dir = self.bundle_dir / "logs"
            logs_dir.mkdir(exist_ok=True)
            return logs_dir
    
    def get_temp_directory(self):
        """Retourne le répertoire temporaire"""
        if self.is_frozen:
            import tempfile
            return Path(tempfile.gettempdir()) / "MatelasProcessor"
        else:
            temp_dir = self.bundle_dir / "temp"
            temp_dir.mkdir(exist_ok=True)
            return temp_dir
    
    def setup_windows_environment(self):
        """Configure l'environnement Windows pour l'application"""
        try:
            # Configurer l'encodage pour Windows
            if sys.platform.startswith('win'):
                import locale
                if hasattr(locale, 'setlocale'):
                    try:
                        locale.setlocale(locale.LC_ALL, 'French_France.UTF-8')
                    except:
                        try:
                            locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
                        except:
                            pass  # Utiliser la locale par défaut
            
            # Créer les répertoires nécessaires
            self.get_config_path().parent.mkdir(parents=True, exist_ok=True)
            self.get_output_directory().mkdir(parents=True, exist_ok=True)
            self.get_logs_directory().mkdir(parents=True, exist_ok=True)
            
            return True
            
        except Exception as e:
            print(f"Avertissement: Configuration Windows partielle - {e}")
            return False
    
    def get_resource_path(self, relative_path):
        """Obtient le chemin d'une ressource (compatible PyInstaller)"""
        return self.bundle_dir / relative_path
    
    def is_admin(self):
        """Vérifie si l'application est exécutée en tant qu'administrateur"""
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def open_folder_windows(self, folder_path):
        """Ouvre un dossier dans l'Explorateur Windows"""
        try:
            import subprocess
            folder_path = Path(folder_path)
            if folder_path.exists():
                subprocess.Popen(f'explorer "{folder_path}"')
                return True
            else:
                print(f"Dossier non trouvé: {folder_path}")
                return False
        except Exception as e:
            print(f"Erreur ouverture dossier: {e}")
            return False
    
    def get_system_info(self):
        """Retourne les informations système Windows"""
        info = {
            "platform": sys.platform,
            "frozen": self.is_frozen,
            "bundle_dir": str(self.bundle_dir),
            "config_path": str(self.get_config_path()),
            "output_dir": str(self.get_output_directory()),
            "logs_dir": str(self.get_logs_directory())
        }
        
        try:
            import platform
            info.update({
                "windows_version": platform.platform(),
                "architecture": platform.architecture()[0],
                "processor": platform.processor(),
            })
        except:
            pass
        
        try:
            import psutil
            info.update({
                "memory_gb": round(psutil.virtual_memory().total / (1024**3), 1),
                "cpu_count": psutil.cpu_count(),
            })
        except:
            pass
        
        return info

# Instance globale pour faciliter l'utilisation
windows_config = WindowsConfig()

def setup_for_windows():
    """Fonction utilitaire pour configurer l'application pour Windows"""
    return windows_config.setup_windows_environment()

def get_windows_paths():
    """Retourne les chemins Windows configurés"""
    return {
        'config': windows_config.get_config_path(),
        'output': windows_config.get_output_directory(), 
        'logs': windows_config.get_logs_directory(),
        'temp': windows_config.get_temp_directory()
    }