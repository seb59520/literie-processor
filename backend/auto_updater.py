#!/usr/bin/env python3
"""
Auto-updater MATELAS avec télémétrie
Version améliorée qui envoie les informations du poste au serveur
"""

import os
import sys
import json
import shutil
import zipfile
import tempfile
import subprocess
import platform
import socket
import getpass
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import requests
from PyQt6.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QProgressBar, QTextEdit, 
                            QMessageBox, QFrame)
from PyQt6.QtCore import QThread, pyqtSignal, QTimer, Qt
from PyQt6.QtGui import QFont, QPixmap, QIcon

class SystemInfoCollector:
    """Collecteur d'informations système pour la télémétrie"""
    
    @staticmethod
    def get_client_id():
        """Génère ou récupère l'ID unique du client"""
        client_id_file = Path.home() / ".matelas_client_id"
        
        if client_id_file.exists():
            try:
                return client_id_file.read_text(encoding='utf-8').strip()
            except:
                pass
        
        # Générer un nouvel ID
        client_id = str(uuid.uuid4())
        try:
            client_id_file.write_text(client_id, encoding='utf-8')
        except:
            pass
        
        return client_id
    
    @staticmethod
    def collect_system_info():
        """Collecte les informations système du poste"""
        try:
            return {
                "platform": platform.platform(),
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "hostname": socket.gethostname(),
                "username": getpass.getuser(),
                "python_version": platform.python_version()
            }
        except Exception as e:
            return {"error": str(e), "platform": "Inconnu"}
    
    @staticmethod
    def get_application_info():
        """Récupère les informations sur l'application MATELAS"""
        try:
            # Essayer de lire la version depuis version.py
            version_file = Path("version.py")
            if version_file.exists():
                version_content = version_file.read_text(encoding='utf-8')
                # Extraire la version
                for line in version_content.split('\n'):
                    if 'VERSION' in line and '=' in line:
                        version = line.split('=')[1].strip().strip('"').strip("'")
                        return {"version": version}
            
            # Fallback
            return {"version": "3.10.3"}
        except:
            return {"version": "Inconnue"}

class TelemetryUpdateInfo:
    """Classe pour gérer les informations de mise à jour avec télémétrie"""
    
    def __init__(self):
        self.available = False
        self.latest_version = ""
        self.download_url = ""
        self.description = ""
        self.changelog = ""
        self.file_size = 0
        self.current_version = ""
        self.release_date = ""
        
        # Informations télémétrie
        self.client_id = SystemInfoCollector.get_client_id()
        self.system_info = SystemInfoCollector.collect_system_info()
        self.app_info = SystemInfoCollector.get_application_info()

class TelemetryUpdateChecker(QThread):
    """Thread pour vérifier les mises à jour avec envoi de télémétrie"""
    
    update_available = pyqtSignal(object)
    no_update = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, server_url="https://edceecf7fdaf.ngrok-free.app"):
        super().__init__()
        self.server_url = server_url
    
    def run(self):
        """Vérifier les mises à jour avec télémétrie"""
        try:
            info = TelemetryUpdateInfo()
            
            # Préparer les headers avec informations télémétrie
            headers = {
                "Content-Type": "application/json",
                "X-Client-ID": info.client_id,
                "X-Current-Version": info.app_info.get("version", "Inconnue"),
                "X-Platform": info.system_info.get("platform", "Inconnu"),
                "X-Hostname": info.system_info.get("hostname", "Inconnu"),
                "X-Username": info.system_info.get("username", "Inconnu"),
                "User-Agent": f"MATELAS-Client/{info.app_info.get('version', '1.0')}"
            }
            
            # Envoyer la requête avec télémétrie
            response = requests.get(
                f"{self.server_url}/api/v1/check-updates",
                params={"current_version": info.app_info.get("version", "0.0.0")},
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("available", False):
                    info.available = True
                    info.latest_version = data.get("latest_version", "")
                    info.download_url = data.get("download_url", "")
                    info.description = data.get("description", "")
                    info.changelog = data.get("changelog", "")
                    info.file_size = data.get("file_size", 0)
                    info.current_version = data.get("current_version", "")
                    info.release_date = data.get("release_date", "")
                    
                    self.update_available.emit(info)
                else:
                    self.no_update.emit("Vous avez la dernière version")
            else:
                self.error_occurred.emit(f"Erreur serveur: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            self.error_occurred.emit("Impossible de se connecter au serveur de mise à jour")
        except requests.exceptions.Timeout:
            self.error_occurred.emit("Timeout de connexion au serveur")
        except Exception as e:
            self.error_occurred.emit(f"Erreur lors de la vérification: {str(e)}")

class TelemetryUpdateDialog(QDialog):
    """Dialog de mise à jour avec télémétrie améliorée"""
    
    def __init__(self, update_info: TelemetryUpdateInfo):
        super().__init__()
        self.update_info = update_info
        self.download_thread = None
        self.install_thread = None
        
        self.setWindowTitle("MATELAS - Mise à Jour Disponible")
        self.setFixedSize(600, 700)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint)
        
        # Améliorer la visibilité de la fenêtre
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                border: 2px solid #0078d4;
                border-radius: 8px;
            }
            QLabel {
                color: #333333;
                background-color: transparent;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 8px;
            }
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 4px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
                border-radius: 2px;
            }
            QFrame {
                background-color: transparent;
                border: none;
            }
        """)
        
        self.init_ui()
        self.show_update_info()
    
    def init_ui(self):
        """Initialiser l'interface utilisateur"""
        layout = QVBoxLayout()
        
        # En-tête avec icône
        header_frame = QFrame()
        header_layout = QHBoxLayout()
        
        # Logo/Icône (si disponible)
        icon_label = QLabel()
        try:
            if Path("assets/logo_westelynck.png").exists():
                pixmap = QPixmap("assets/logo_westelynck.png").scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio)
                icon_label.setPixmap(pixmap)
        except:
            icon_label.setText("🚀")
            icon_label.setFont(QFont("Arial", 24))
        
        header_info = QLabel("Mise à jour MATELAS disponible")
        header_info.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(header_info)
        header_layout.addStretch()
        header_frame.setLayout(header_layout)
        layout.addWidget(header_frame)
        
        # Informations sur la mise à jour
        self.info_text = QTextEdit()
        self.info_text.setMaximumHeight(200)
        self.info_text.setReadOnly(True)
        layout.addWidget(self.info_text)
        
        # Informations télémétrie (masquées par défaut)
        telemetry_frame = QFrame()
        telemetry_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        telemetry_layout = QVBoxLayout()
        
        telemetry_title = QLabel("📊 Informations du poste (envoyées de manière anonyme)")
        telemetry_title.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        telemetry_layout.addWidget(telemetry_title)
        
        self.telemetry_info = QLabel()
        self.telemetry_info.setStyleSheet("color: #666; font-size: 9px;")
        self.telemetry_info.setWordWrap(True)
        telemetry_layout.addWidget(self.telemetry_info)
        
        telemetry_frame.setLayout(telemetry_layout)
        layout.addWidget(telemetry_frame)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status
        self.status_label = QLabel("Prêt à télécharger")
        layout.addWidget(self.status_label)
        
        # Boutons
        buttons_layout = QHBoxLayout()
        
        self.download_btn = QPushButton("📥 Télécharger et Installer")
        self.download_btn.clicked.connect(self.start_download)
        self.download_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        
        self.cancel_btn = QPushButton("❌ Annuler")
        self.cancel_btn.clicked.connect(self.reject)
        
        self.later_btn = QPushButton("⏰ Plus tard")
        self.later_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(self.later_btn)
        buttons_layout.addWidget(self.cancel_btn)
        buttons_layout.addWidget(self.download_btn)
        
        layout.addLayout(buttons_layout)
        self.setLayout(layout)
    
    def show_update_info(self):
        """Afficher les informations de mise à jour"""
        info_text = f"""
🎯 NOUVELLE VERSION DISPONIBLE

📦 Version actuelle: {self.update_info.current_version}
🆕 Nouvelle version: {self.update_info.latest_version}
📅 Date de sortie: {self.update_info.release_date[:10] if self.update_info.release_date else 'Inconnue'}
📊 Taille: {self.update_info.file_size / (1024*1024):.1f} MB

📝 Description:
{self.update_info.description}

🔄 Changelog:
{self.update_info.changelog}
        """
        
        self.info_text.setPlainText(info_text.strip())
        
        # Informations télémétrie
        telemetry_text = f"""
🖥️ Poste: {self.update_info.system_info.get('hostname', 'Inconnu')} | 
👤 Utilisateur: {self.update_info.system_info.get('username', 'Inconnu')} | 
💻 OS: {self.update_info.system_info.get('system', 'Inconnu')} | 
🆔 ID Client: {self.update_info.client_id[:8]}...
        """
        
        self.telemetry_info.setText(telemetry_text.strip())
    
    def start_download(self):
        """Démarrer le téléchargement"""
        self.download_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.status_label.setText("Téléchargement en cours...")
        
        self.download_thread = DownloadThread(self.update_info.download_url)
        self.download_thread.progress.connect(self.update_progress)
        self.download_thread.finished_signal.connect(self.download_finished)
        self.download_thread.error.connect(self.download_error)
        self.download_thread.start()
    
    def update_progress(self, value):
        """Mettre à jour la barre de progression"""
        self.progress_bar.setValue(value)
    
    def download_finished(self, file_path):
        """Téléchargement terminé, démarrer l'installation"""
        self.status_label.setText("Installation en cours...")
        self.progress_bar.setValue(100)
        
        self.install_thread = InstallThread(file_path, self.update_info)
        self.install_thread.finished_signal.connect(self.install_finished)
        self.install_thread.error.connect(self.install_error)
        self.install_thread.start()
    
    def download_error(self, error_msg):
        """Erreur de téléchargement"""
        self.status_label.setText(f"Erreur de téléchargement: {error_msg}")
        self.download_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        QMessageBox.critical(self, "Erreur", f"Erreur de téléchargement:\n{error_msg}")
    
    def install_finished(self, success):
        """Installation terminée"""
        if success:
            self.status_label.setText("✅ Mise à jour installée avec succès!")
            
            # Proposer de redémarrer
            result = QMessageBox.question(
                self, 
                "Mise à jour terminée",
                "La mise à jour a été installée avec succès.\n\nVoulez-vous redémarrer l'application maintenant?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if result == QMessageBox.StandardButton.Yes:
                self.restart_application()
            
            self.accept()
        else:
            self.status_label.setText("❌ Erreur d'installation")
            self.download_btn.setEnabled(True)
    
    def install_error(self, error_msg):
        """Erreur d'installation"""
        self.status_label.setText(f"Erreur d'installation: {error_msg}")
        self.download_btn.setEnabled(True)
        
        QMessageBox.critical(self, "Erreur", f"La mise à jour n'a pas pu être installée:\n{error_msg}")
    
    def restart_application(self):
        """Redémarrer l'application"""
        try:
            # Déterminer comment redémarrer
            is_exe = getattr(sys, 'frozen', False)
            
            if is_exe:
                # Mode EXE
                exe_path = sys.executable
                subprocess.Popen([exe_path], cwd=Path(exe_path).parent)
            else:
                # Mode développement
                subprocess.Popen([sys.executable, "app_gui.py"], cwd=Path.cwd())
            
            # Fermer l'application actuelle
            QApplication.instance().quit()
            
        except Exception as e:
            QMessageBox.warning(self, "Redémarrage", f"Impossible de redémarrer automatiquement: {e}")

class DownloadThread(QThread):
    """Thread pour télécharger la mise à jour"""
    
    progress = pyqtSignal(int)
    finished_signal = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, download_url):
        super().__init__()
        self.download_url = download_url
    
    def run(self):
        """Télécharger le fichier"""
        try:
            response = requests.get(self.download_url, stream=True, timeout=300)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            # Créer un fichier temporaire
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_file:
                temp_path = temp_file.name
                
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        temp_file.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            progress = int((downloaded / total_size) * 100)
                            self.progress.emit(progress)
            
            self.finished_signal.emit(temp_path)
            
        except Exception as e:
            self.error.emit(str(e))

class InstallThread(QThread):
    """Thread pour installer la mise à jour"""
    
    finished_signal = pyqtSignal(bool)
    error = pyqtSignal(str)
    
    def __init__(self, zip_path, update_info):
        super().__init__()
        self.zip_path = zip_path
        self.update_info = update_info
    
    def run(self):
        """Installer la mise à jour"""
        try:
            success = self._install_update()
            self.finished_signal.emit(success)
        except Exception as e:
            self.error.emit(str(e))
    
    def _install_update(self) -> bool:
        """Installer la mise à jour"""
        try:
            # Déterminer le répertoire d'installation
            is_exe = getattr(sys, 'frozen', False)
            app_dir = Path(sys.executable).parent if is_exe else Path.cwd()
            
            # Créer une sauvegarde
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = app_dir / f"backup_{timestamp}"
            
            # Sauvegarder les fichiers critiques
            critical_files = ["matelas_config.json", "notion_config.json", "config/secure_keys.dat"]
            backup_created = False
            
            for file_name in critical_files:
                source_file = app_dir / file_name
                if source_file.exists():
                    if not backup_created:
                        backup_dir.mkdir(exist_ok=True)
                        backup_created = True
                    
                    backup_file_path = backup_dir / file_name
                    backup_file_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_file, backup_file_path)
            
            # Installer la mise à jour
            if is_exe:
                success = self._extract_for_exe(self.zip_path, app_dir)
            else:
                success = self._extract_for_dev(self.zip_path, app_dir)
            
            if success and backup_created:
                # Restaurer les fichiers de configuration
                for file_name in critical_files:
                    backup_file = backup_dir / file_name
                    target_file = app_dir / file_name
                    
                    if backup_file.exists():
                        target_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(backup_file, target_file)
            
            # Mettre à jour le fichier de version
            self._update_version_file(app_dir)
            
            # Nettoyer le fichier temporaire
            Path(self.zip_path).unlink()
            
            return success
            
        except Exception as e:
            return False
    
    def _extract_for_exe(self, zip_path: str, app_dir: Path) -> bool:
        """Extraction spéciale pour mode EXE"""
        try:
            exe_name = Path(sys.executable).name
            
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                for file_info in zipf.filelist:
                    file_path = Path(file_info.filename)
                    
                    # Ignorer l'EXE principal et autres EXE
                    if file_path.name == exe_name or file_path.suffix.lower() == '.exe':
                        continue
                    
                    target_path = app_dir / file_path
                    
                    if file_info.is_dir():
                        target_path.mkdir(parents=True, exist_ok=True)
                    else:
                        target_path.parent.mkdir(parents=True, exist_ok=True)
                        with zipf.open(file_info) as source, open(target_path, 'wb') as target:
                            shutil.copyfileobj(source, target)
            
            return True
        except Exception as e:
            return False
    
    def _extract_for_dev(self, zip_path: str, app_dir: Path) -> bool:
        """Extraction normale pour mode développement"""
        try:
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                zipf.extractall(app_dir)
            return True
        except Exception as e:
            return False
    
    def _update_version_file(self, app_dir: Path):
        """Mettre à jour le fichier version.py"""
        try:
            version_file = app_dir / "version.py"
            if version_file.exists():
                content = version_file.read_text(encoding='utf-8')
                
                # Remplacer la version
                new_content = content
                for line in content.split('\n'):
                    if 'VERSION' in line and '=' in line:
                        old_line = line
                        new_line = f'VERSION = "{self.update_info.latest_version}"'
                        new_content = new_content.replace(old_line, new_line)
                        break
                
                version_file.write_text(new_content, encoding='utf-8')
        except Exception:
            pass

def check_for_updates_with_telemetry(server_url="https://edceecf7fdaf.ngrok-free.app") -> Optional[TelemetryUpdateInfo]:
    """Vérifier les mises à jour avec télémétrie (version synchrone)"""
    try:
        info = TelemetryUpdateInfo()
        
        headers = {
            "X-Client-ID": info.client_id,
            "X-Current-Version": info.app_info.get("version", "Inconnue"),
            "X-Platform": info.system_info.get("platform", "Inconnu"),
            "X-Hostname": info.system_info.get("hostname", "Inconnu"),
            "X-Username": info.system_info.get("username", "Inconnu"),
            "User-Agent": f"MATELAS-Client/{info.app_info.get('version', '1.0')}"
        }
        
        response = requests.get(
            f"{server_url}/api/v1/check-updates",
            params={"current_version": info.app_info.get("version", "0.0.0")},
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("available", False):
                info.available = True
                info.latest_version = data.get("latest_version", "")
                info.download_url = data.get("download_url", "")
                info.description = data.get("description", "")
                info.changelog = data.get("changelog", "")
                info.file_size = data.get("file_size", 0)
                info.current_version = data.get("current_version", "")
                info.release_date = data.get("release_date", "")
                
                return info
        
        return None
        
    except Exception as e:
        print(f"Erreur vérification mise à jour: {e}")
        return None

def show_update_dialog_with_telemetry(server_url="https://edceecf7fdaf.ngrok-free.app"):
    """Afficher le dialog de mise à jour avec télémétrie"""
    try:
        # Vérifier les mises à jour
        update_info = check_for_updates_with_telemetry(server_url)
        
        if update_info and update_info.available:
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)
            
            dialog = TelemetryUpdateDialog(update_info)
            result = dialog.exec()
            
            return result == QDialog.DialogCode.Accepted
        else:
            return False
            
    except Exception as e:
        print(f"Erreur dialog mise à jour: {e}")
        return False

# Compatibilité avec l'ancienne API
UpdateInfo = TelemetryUpdateInfo
UpdateDialog = TelemetryUpdateDialog
UpdateChecker = TelemetryUpdateChecker

# Fonctions principales
def check_for_updates(server_url="https://edceecf7fdaf.ngrok-free.app"):
    """Fonction de compatibilité"""
    return check_for_updates_with_telemetry(server_url)

def show_update_dialog(server_url="https://edceecf7fdaf.ngrok-free.app"):
    """Fonction de compatibilité"""
    return show_update_dialog_with_telemetry(server_url)

if __name__ == "__main__":
    print("🔍 Test du client avec télémétrie...")
    
    # Test de collecte d'informations
    print("📊 Informations système:")
    system_info = SystemInfoCollector.collect_system_info()
    for key, value in system_info.items():
        print(f"   {key}: {value}")
    
    print(f"\n🆔 ID Client: {SystemInfoCollector.get_client_id()}")
    
    # Test de vérification de mise à jour
    print("\n🔍 Vérification des mises à jour...")
    update_info = check_for_updates_with_telemetry()
    
    if update_info:
        print(f"✅ Mise à jour disponible: {update_info.latest_version}")
        
        # Lancer l'interface graphique si disponible
        if len(sys.argv) > 1 and sys.argv[1] == "--gui":
            show_update_dialog_with_telemetry()
    else:
        print("ℹ️ Aucune mise à jour disponible")
