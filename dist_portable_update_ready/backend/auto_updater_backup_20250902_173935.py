#!/usr/bin/env python3
"""
Client de mise à jour automatique pour l'application MATELAS_FINAL
Vérifie, télécharge et installe automatiquement les mises à jour
"""

import os
import sys
import json
import time
import shutil
import zipfile
import tempfile
import threading
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Callable
from urllib.parse import urlparse

import httpx
from PyQt6.QtCore import QObject, QThread, pyqtSignal, QTimer
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QProgressBar, QTextEdit, QCheckBox,
                           QMessageBox, QApplication)

# Import du gestionnaire d'EXE
try:
    from exe_updater import create_executable_update_dialog, ExecutableUpdateManager
    EXE_UPDATER_AVAILABLE = True
except ImportError:
    EXE_UPDATER_AVAILABLE = False
    print("⚠️ Gestionnaire d'EXE non disponible")

class UpdateInfo:
    """Information sur une mise à jour"""
    
    def __init__(self, data: Dict):
        self.available = data.get("update_available", False)
        self.current_version = data.get("current_version", "")
        self.latest_version = data.get("latest_version", "")
        self.release_date = data.get("release_date", "")
        self.description = data.get("description", "")
        self.download_url = data.get("download_url", "")
        self.file_size = data.get("file_size", 0)
        self.changelog = data.get("changelog", "")

class UpdateDownloader(QThread):
    """Thread pour télécharger les mises à jour"""
    
    progress_updated = pyqtSignal(int)
    status_updated = pyqtSignal(str)
    download_completed = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, url: str, output_path: str):
        super().__init__()
        self.url = url
        self.output_path = Path(output_path)
        self.cancelled = False
    
    def run(self):
        """Télécharge le fichier de mise à jour"""
        try:
            self.status_updated.emit("Connexion au serveur...")
            
            with httpx.stream("GET", self.url, timeout=300.0) as response:
                response.raise_for_status()
                
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                self.status_updated.emit(f"Téléchargement... (0/{self._format_size(total_size)})")
                
                with open(self.output_path, 'wb') as f:
                    for chunk in response.iter_bytes(chunk_size=8192):
                        if self.cancelled:
                            self.error_occurred.emit("Téléchargement annulé")
                            return
                        
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            progress = int((downloaded / total_size) * 100)
                            self.progress_updated.emit(progress)
                            self.status_updated.emit(
                                f"Téléchargement... ({self._format_size(downloaded)}/{self._format_size(total_size)})"
                            )
            
            self.status_updated.emit("Téléchargement terminé")
            self.download_completed.emit(str(self.output_path))
            
        except Exception as e:
            self.error_occurred.emit(f"Erreur de téléchargement: {str(e)}")
    
    def cancel(self):
        """Annule le téléchargement"""
        self.cancelled = True
    
    def _format_size(self, size: int) -> str:
        """Formate une taille en bytes en format lisible"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

class UpdateDialog(QDialog):
    """Dialog pour afficher et contrôler les mises à jour"""
    
    def __init__(self, update_info: UpdateInfo, parent=None):
        super().__init__(parent)
        self.update_info = update_info
        self.downloader = None
        self.temp_file = None
        
        self.setWindowTitle("Mise à jour disponible")
        self.setFixedSize(500, 400)
        self.setModal(True)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Configure l'interface utilisateur"""
        layout = QVBoxLayout()
        
        # Titre
        title_label = QLabel(f"🎉 Nouvelle version disponible: {self.update_info.latest_version}")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #2196F3;")
        layout.addWidget(title_label)
        
        # Informations sur la version
        info_layout = QVBoxLayout()
        
        current_label = QLabel(f"Version actuelle: {self.update_info.current_version}")
        info_layout.addWidget(current_label)
        
        latest_label = QLabel(f"Nouvelle version: {self.update_info.latest_version}")
        info_layout.addWidget(latest_label)
        
        if self.update_info.release_date:
            date_label = QLabel(f"Date de sortie: {self.update_info.release_date}")
            info_layout.addWidget(date_label)
        
        if self.update_info.file_size > 0:
            size_label = QLabel(f"Taille: {self._format_size(self.update_info.file_size)}")
            info_layout.addWidget(size_label)
        
        layout.addLayout(info_layout)
        
        # Description
        if self.update_info.description:
            desc_label = QLabel("Description:")
            desc_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
            layout.addWidget(desc_label)
            
            desc_text = QLabel(self.update_info.description)
            desc_text.setWordWrap(True)
            layout.addWidget(desc_text)
        
        # Changelog
        if self.update_info.changelog:
            changelog_label = QLabel("Nouveautés:")
            changelog_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
            layout.addWidget(changelog_label)
            
            self.changelog_text = QTextEdit()
            self.changelog_text.setPlainText(self.update_info.changelog)
            self.changelog_text.setMaximumHeight(100)
            self.changelog_text.setReadOnly(True)
            layout.addWidget(self.changelog_text)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status
        self.status_label = QLabel("")
        self.status_label.setVisible(False)
        layout.addWidget(self.status_label)
        
        # Boutons
        button_layout = QHBoxLayout()
        
        self.download_button = QPushButton("📥 Télécharger et installer")
        self.download_button.clicked.connect(self._start_download)
        self.download_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 8px; }")
        
        self.cancel_button = QPushButton("❌ Annuler")
        self.cancel_button.clicked.connect(self.reject)
        
        self.later_button = QPushButton("⏰ Plus tard")
        self.later_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.download_button)
        button_layout.addWidget(self.later_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        # Checkbox pour les mises à jour automatiques
        self.auto_update_cb = QCheckBox("Installer automatiquement les prochaines mises à jour")
        layout.addWidget(self.auto_update_cb)
        
        self.setLayout(layout)
    
    def _start_download(self):
        """Démarre le téléchargement de la mise à jour"""
        if not self.update_info.download_url:
            QMessageBox.warning(self, "Erreur", "URL de téléchargement non disponible")
            return
        
        # Créer un fichier temporaire
        with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as f:
            self.temp_file = f.name
        
        # Configurer l'UI pour le téléchargement
        self.download_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.status_label.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Démarrer le téléchargement
        self.downloader = UpdateDownloader(self.update_info.download_url, self.temp_file)
        self.downloader.progress_updated.connect(self.progress_bar.setValue)
        self.downloader.status_updated.connect(self.status_label.setText)
        self.downloader.download_completed.connect(self._on_download_completed)
        self.downloader.error_occurred.connect(self._on_download_error)
        self.downloader.start()
    
    def _on_download_completed(self, file_path: str):
        """Appelé quand le téléchargement est terminé"""
        self.status_label.setText("Installation en cours...")
        
        try:
            # Installer la mise à jour
            success = self._install_update(file_path)
            
            if success:
                QMessageBox.information(
                    self, 
                    "Mise à jour réussie", 
                    "La mise à jour a été installée avec succès. L'application va redémarrer."
                )
                self._restart_application()
            else:
                QMessageBox.warning(
                    self, 
                    "Erreur d'installation", 
                    "La mise à jour n'a pas pu être installée. Veuillez réessayer."
                )
        
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Erreur", 
                f"Erreur lors de l'installation: {str(e)}"
            )
        
        finally:
            # Nettoyer le fichier temporaire
            if os.path.exists(file_path):
                os.unlink(file_path)
    
    def _on_download_error(self, error_msg: str):
        """Appelé en cas d'erreur de téléchargement"""
        QMessageBox.critical(self, "Erreur de téléchargement", error_msg)
        self.download_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setVisible(False)
    
    def _install_update(self, zip_path: str) -> bool:
        """Installe la mise à jour depuis un fichier ZIP"""
        try:
            # Obtenir le répertoire de l'application
            is_exe = getattr(sys, 'frozen', False)
            app_dir = Path(sys.executable).parent if is_exe else Path.cwd()
            
            print(f"🔧 Mode: {'EXE' if is_exe else 'DEV'}")
            print(f"📁 Répertoire app: {app_dir}")
            
            # Créer un dossier de sauvegarde
            backup_dir = app_dir / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            backup_dir.mkdir(exist_ok=True)
            
            # Fichiers critiques à sauvegarder (différents selon le mode)
            if is_exe:
                # Mode EXE: sauvegarder les configs + l'exe principal si nécessaire
                critical_files = [
                    "config/secure_keys.dat", 
                    "matelas_config.json", 
                    "notion_config.json",
                    "updater_config.json"
                ]
                # Note: L'exe principal ne peut pas être remplacé pendant qu'il s'exécute
                # Il sera mis à jour via un processus spécial après redémarrage
            else:
                # Mode DEV: sauvegarder les configs seulement
                critical_files = [
                    "config/secure_keys.dat", 
                    "matelas_config.json", 
                    "notion_config.json",
                    "updater_config.json"
                ]
            
            # Sauvegarder les fichiers critiques
            for file_name in critical_files:
                file_path = app_dir / file_name
                if file_path.exists():
                    backup_file_path = backup_dir / file_name
                    # Créer le répertoire parent si nécessaire
                    backup_file_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file_path, backup_file_path)
                    print(f"✅ Sauvegardé: {file_name}")
                else:
                    print(f"⏭️ Ignoré (n'existe pas): {file_name}")
            
            # Extraire la mise à jour avec gestion spéciale EXE
            print("📦 Extraction de la mise à jour...")
            
            if is_exe:
                # Mode EXE: Extraction intelligente pour éviter les fichiers verrouillés
                self._extract_for_exe(zip_path, app_dir)
            else:
                # Mode DEV: Extraction simple
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(app_dir)
                print("✅ Extraction DEV terminée")
            
            # Restaurer les fichiers de configuration
            for file_name in critical_files:
                backup_file = backup_dir / file_name
                target_file = app_dir / file_name
                if backup_file.exists():
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(backup_file, target_file)
                    print(f"🔄 Restauré: {file_name}")
            
            # Mettre à jour le fichier de version
            if hasattr(self, 'update_info') and self.update_info:
                success = self._update_version_file(app_dir, self.update_info.latest_version)
                if success:
                    print(f"✅ Version mise à jour: {self.update_info.latest_version}")
                else:
                    print("⚠️ Impossible de mettre à jour version.py (pas critique)")
            
            return True
            
        except Exception as e:
            print(f"Erreur installation: {e}")
            return False
    
    def _update_version_file(self, app_dir: Path, new_version: str) -> bool:
        """Met à jour le fichier version.py avec la nouvelle version"""
        try:
            import re
            
            version_file = app_dir / "version.py"
            if not version_file.exists():
                return False
            
            # Lire le fichier actuel
            with open(version_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Obtenir la date actuelle
            build_date = datetime.now().strftime("%Y-%m-%d")
            build_number = datetime.now().strftime("%Y%m%d")
            
            # Remplacer la version
            content = re.sub(
                r'VERSION = "[^"]*"',
                f'VERSION = "{new_version}"',
                content
            )
            
            # Remplacer la date de build
            content = re.sub(
                r'BUILD_DATE = "[^"]*"',
                f'BUILD_DATE = "{build_date}"',
                content
            )
            
            # Remplacer le numéro de build
            content = re.sub(
                r'BUILD_NUMBER = "[^"]*"',
                f'BUILD_NUMBER = "{build_number}"',
                content
            )
            
            # Sauvegarder le fichier mis à jour
            with open(version_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
            
        except Exception as e:
            print(f"Erreur mise à jour version.py: {e}")
            return False
    
    def _extract_for_exe(self, zip_path: str, app_dir: Path):
        """Extraction spécialisée pour mode EXE"""
        try:
            exe_name = Path(sys.executable).name
            print(f"🔒 Mode EXE détecté, exe principal: {exe_name}")
            
            files_updated = 0
            files_skipped = 0
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for file_info in zip_ref.filelist:
                    if file_info.is_dir():
                        continue
                        
                    file_name = file_info.filename
                    target_path = app_dir / file_name
                    
                    # Skip l'exe principal qui ne peut pas être remplacé pendant l'exécution
                    if file_name == exe_name or file_name.endswith('.exe'):
                        files_skipped += 1
                        print(f"⏭️ Ignoré (exe): {file_name}")
                        continue
                    
                    # Créer le répertoire parent
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Extraire le fichier
                    try:
                        with zip_ref.open(file_info) as source, open(target_path, 'wb') as target:
                            shutil.copyfileobj(source, target)
                        files_updated += 1
                        
                        if files_updated <= 5:
                            print(f"✅ Mis à jour: {file_name}")
                        elif files_updated == 6:
                            print("... (mise à jour en cours)")
                            
                    except PermissionError as e:
                        files_skipped += 1
                        print(f"⏭️ Ignoré (permission): {file_name}")
                        continue
                    except Exception as e:
                        print(f"⚠️ Erreur {file_name}: {e}")
                        continue
            
            print(f"✅ EXE: {files_updated} fichiers mis à jour, {files_skipped} ignorés")
            
        except Exception as e:
            print(f"❌ Erreur extraction EXE: {e}")
            raise
    
    def _restart_application(self):
        """Redémarre l'application"""
        try:
            if getattr(sys, 'frozen', False):
                # Application compilée
                subprocess.Popen([sys.executable])
            else:
                # Mode développement
                subprocess.Popen([sys.executable] + sys.argv)
            
            # Fermer l'application actuelle
            QApplication.quit()
            
        except Exception as e:
            print(f"Erreur redémarrage: {e}")
    
    def _format_size(self, size: int) -> str:
        """Formate une taille en bytes"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def closeEvent(self, event):
        """Intercepte la fermeture du dialog"""
        if self.downloader and self.downloader.isRunning():
            self.downloader.cancel()
            self.downloader.wait()
        
        if self.temp_file and os.path.exists(self.temp_file):
            os.unlink(self.temp_file)
        
        event.accept()

class AutoUpdater(QObject):
    """Service de mise à jour automatique"""
    
    update_available = pyqtSignal(UpdateInfo)
    update_checked = pyqtSignal(bool)
    
    def __init__(self, server_url: str = "http://72.60.47.183", current_version: str = "1.0.0"):
        super().__init__()
        self.server_url = server_url.rstrip('/')
        self.current_version = current_version
        self.check_interval = 3600  # 1 heure par défaut
        
        # Configuration
        self.config_file = Path("updater_config.json")
        self.config = self._load_config()
        
        # Timer pour les vérifications automatiques
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_for_updates)
        
        # Démarrer les vérifications automatiques si activées
        if self.config.get("auto_check", True):
            self.start_periodic_check()
    
    def _load_config(self) -> Dict:
        """Charge la configuration du système de mise à jour"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        
        return {
            "auto_check": True,
            "auto_install": False,
            "check_interval": 3600,
            "last_check": "",
            "skip_versions": []
        }
    
    def _save_config(self):
        """Sauvegarde la configuration"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Erreur sauvegarde config: {e}")
    
    def check_for_updates(self, silent: bool = False) -> Optional[UpdateInfo]:
        """Vérifie s'il y a des mises à jour disponibles"""
        try:
            url = f"{self.server_url}/api/v1/check-updates"
            params = {"current_version": self.current_version}
            
            with httpx.Client(timeout=30.0) as client:
                response = client.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                update_info = UpdateInfo(data)
                
                # Mettre à jour la configuration
                self.config["last_check"] = datetime.now().isoformat()
                self._save_config()
                
                if update_info.available:
                    # Vérifier si cette version n'est pas dans la liste à ignorer
                    if update_info.latest_version not in self.config.get("skip_versions", []):
                        if not silent:
                            self.update_available.emit(update_info)
                        return update_info
                
                if not silent:
                    self.update_checked.emit(update_info.available)
                
                return update_info if update_info.available else None
                
        except Exception as e:
            print(f"Erreur vérification mise à jour: {e}")
            if not silent:
                self.update_checked.emit(False)
            return None
    
    def start_periodic_check(self):
        """Démarre les vérifications périodiques"""
        interval = self.config.get("check_interval", self.check_interval)
        self.timer.start(interval * 1000)  # Convertir en millisecondes
        print(f"🔄 Vérifications automatiques démarrées (interval: {interval}s)")
    
    def stop_periodic_check(self):
        """Arrête les vérifications périodiques"""
        self.timer.stop()
        print("⏸️ Vérifications automatiques arrêtées")
    
    def show_update_dialog(self, update_info: UpdateInfo, parent=None) -> bool:
        """Affiche le dialog de mise à jour"""
        # Si on est dans un EXE et que le gestionnaire d'EXE est disponible
        if getattr(sys, 'frozen', False) and EXE_UPDATER_AVAILABLE:
            # Utiliser le dialog spécialisé pour les EXE
            dialog = create_executable_update_dialog(update_info, parent)
            result = dialog.exec()
        else:
            # Utiliser le dialog standard pour les mises à jour de fichiers
            dialog = UpdateDialog(update_info, parent)
            result = dialog.exec()
            
            # Sauvegarder les préférences
            if hasattr(dialog, 'auto_update_cb') and dialog.auto_update_cb.isChecked():
                self.config["auto_install"] = True
                self._save_config()
        
        return result == QDialog.DialogCode.Accepted
    
    def skip_version(self, version: str):
        """Ajoute une version à la liste des versions à ignorer"""
        skip_list = self.config.get("skip_versions", [])
        if version not in skip_list:
            skip_list.append(version)
            self.config["skip_versions"] = skip_list
            self._save_config()
    
    def set_auto_check(self, enabled: bool):
        """Active/désactive les vérifications automatiques"""
        self.config["auto_check"] = enabled
        self._save_config()
        
        if enabled:
            self.start_periodic_check()
        else:
            self.stop_periodic_check()
    
    def set_check_interval(self, interval: int):
        """Définit l'intervalle de vérification en secondes"""
        self.config["check_interval"] = interval
        self._save_config()
        
        if self.timer.isActive():
            self.timer.setInterval(interval * 1000)

# Fonction utilitaire pour vérifier les mises à jour manuellement
def check_updates_manual(server_url: str, current_version: str) -> Optional[UpdateInfo]:
    """Vérifie manuellement les mises à jour (sans PyQt)"""
    try:
        url = f"{server_url.rstrip('/')}/api/v1/check-updates"
        params = {"current_version": current_version}
        
        with httpx.Client(timeout=30.0) as client:
            response = client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return UpdateInfo(data)
            
    except Exception as e:
        print(f"Erreur vérification: {e}")
        return None

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    # Test du système de mise à jour
    app = QApplication(sys.argv)
    
    updater = AutoUpdater("http://72.60.47.183", "1.0.0")
    
    def on_update_available(update_info: UpdateInfo):
        print(f"Mise à jour disponible: {update_info.latest_version}")
        updater.show_update_dialog(update_info)
    
    updater.update_available.connect(on_update_available)
    updater.check_for_updates()
    
    sys.exit(app.exec())