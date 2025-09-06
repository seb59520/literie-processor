#!/usr/bin/env python3
"""
Gestionnaire de mise à jour spécialisé pour les exécutables
Gère le téléchargement et l'installation de nouveaux EXE
"""

import os
import sys
import shutil
import tempfile
import subprocess
from pathlib import Path
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QProgressDialog

class ExecutableUpdater(QThread):
    """Thread pour mettre à jour un exécutable"""
    
    progress_updated = pyqtSignal(int)
    status_updated = pyqtSignal(str)
    update_completed = pyqtSignal()
    error_occurred = pyqtSignal(str)
    
    def __init__(self, download_url: str, current_exe_path: str):
        super().__init__()
        self.download_url = download_url
        self.current_exe_path = Path(current_exe_path)
        self.cancelled = False
    
    def run(self):
        """Processus de mise à jour de l'exécutable"""
        try:
            # 1. Télécharger le package de mise à jour
            self.status_updated.emit("Téléchargement de la mise à jour...")
            temp_zip = self._download_update()
            if not temp_zip:
                return
            
            # 2. Extraire et valider
            self.status_updated.emit("Extraction du package...")
            new_exe_path = self._extract_update(temp_zip)
            if not new_exe_path:
                return
            
            # 3. Sauvegarder l'ancien exe
            self.status_updated.emit("Sauvegarde de l'ancienne version...")
            if not self._backup_current_exe():
                return
            
            # 4. Installer la nouvelle version
            self.status_updated.emit("Installation de la nouvelle version...")
            if not self._install_new_exe(new_exe_path):
                return
            
            # 5. Nettoyer et redémarrer
            self.status_updated.emit("Finalisation...")
            self._cleanup_temp_files()
            
            self.update_completed.emit()
            
        except Exception as e:
            self.error_occurred.emit(f"Erreur lors de la mise à jour: {str(e)}")
    
    def _download_update(self) -> Path:
        """Télécharge le package de mise à jour"""
        try:
            import httpx
            
            temp_dir = Path(tempfile.mkdtemp(prefix="matelas_update_"))
            temp_zip = temp_dir / "update.zip"
            
            with httpx.stream("GET", self.download_url, timeout=300.0) as response:
                response.raise_for_status()
                
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                with open(temp_zip, 'wb') as f:
                    for chunk in response.iter_bytes(chunk_size=8192):
                        if self.cancelled:
                            self.error_occurred.emit("Téléchargement annulé")
                            return None
                        
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            progress = int((downloaded / total_size) * 50)  # 50% pour le téléchargement
                            self.progress_updated.emit(progress)
            
            return temp_zip
            
        except Exception as e:
            self.error_occurred.emit(f"Erreur de téléchargement: {str(e)}")
            return None
    
    def _extract_update(self, zip_path: Path) -> Path:
        """Extrait le package et retourne le chemin du nouvel exe"""
        try:
            import zipfile
            import json
            
            extract_dir = zip_path.parent / "extracted"
            extract_dir.mkdir(exist_ok=True)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            self.progress_updated.emit(60)
            
            # Chercher les métadonnées
            metadata_file = extract_dir / "update_metadata.json"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                    exe_name = metadata.get("executable_name", "MatelasProcessor.exe")
            else:
                exe_name = "MatelasProcessor.exe"  # Nom par défaut
            
            new_exe = extract_dir / exe_name
            if not new_exe.exists():
                # Chercher le premier .exe dans le dossier
                exe_files = list(extract_dir.glob("*.exe"))
                if exe_files:
                    new_exe = exe_files[0]
                else:
                    self.error_occurred.emit("Aucun exécutable trouvé dans le package")
                    return None
            
            self.progress_updated.emit(70)
            return new_exe
            
        except Exception as e:
            self.error_occurred.emit(f"Erreur d'extraction: {str(e)}")
            return None
    
    def _backup_current_exe(self) -> bool:
        """Sauvegarde l'exécutable actuel"""
        try:
            if self.current_exe_path.exists():
                backup_path = self.current_exe_path.with_suffix('.exe.backup')
                shutil.copy2(self.current_exe_path, backup_path)
                self.progress_updated.emit(80)
            return True
        except Exception as e:
            self.error_occurred.emit(f"Erreur de sauvegarde: {str(e)}")
            return False
    
    def _install_new_exe(self, new_exe_path: Path) -> bool:
        """Installe le nouvel exécutable"""
        try:
            # Sur Windows, on ne peut pas remplacer un exe en cours d'exécution
            # On va créer un script batch qui fera le remplacement après fermeture
            if sys.platform == "win32":
                return self._install_on_windows(new_exe_path)
            else:
                # Sur autres plateformes
                shutil.copy2(new_exe_path, self.current_exe_path)
                self.progress_updated.emit(90)
                return True
                
        except Exception as e:
            self.error_occurred.emit(f"Erreur d'installation: {str(e)}")
            return False
    
    def _install_on_windows(self, new_exe_path: Path) -> bool:
        """Installation spéciale pour Windows"""
        try:
            # Créer un script batch pour le remplacement
            update_script = self.current_exe_path.parent / "update_install.bat"
            
            script_content = f'''@echo off
echo Mise a jour en cours...
timeout /t 2 /nobreak >nul

REM Attendre que l'application se ferme
:wait_loop
tasklist /FI "IMAGENAME eq {self.current_exe_path.name}" 2>NUL | find /I /N "{self.current_exe_path.name}">NUL
if "%ERRORLEVEL%"=="0" (
    timeout /t 1 /nobreak >nul
    goto wait_loop
)

REM Remplacer l'exe
echo Remplacement de l'executable...
copy "{new_exe_path}" "{self.current_exe_path}" >nul 2>&1

if %ERRORLEVEL%==0 (
    echo Mise a jour reussie !
    echo Redemarrage de l'application...
    start "" "{self.current_exe_path}"
) else (
    echo Erreur lors de la mise a jour !
    pause
)

REM Nettoyer
del "{new_exe_path}" >nul 2>&1
del "%~f0" >nul 2>&1
'''
            
            with open(update_script, 'w', encoding='cp1252') as f:
                f.write(script_content)
            
            # Lancer le script en arrière-plan
            subprocess.Popen([str(update_script)], creationflags=subprocess.CREATE_NO_WINDOW)
            
            self.progress_updated.emit(95)
            return True
            
        except Exception as e:
            self.error_occurred.emit(f"Erreur installation Windows: {str(e)}")
            return False
    
    def _cleanup_temp_files(self):
        """Nettoie les fichiers temporaires"""
        try:
            # Les fichiers temporaires seront nettoyés par le système
            self.progress_updated.emit(100)
        except Exception:
            pass  # Pas critique
    
    def cancel(self):
        """Annule la mise à jour"""
        self.cancelled = True

class ExecutableUpdateManager:
    """Gestionnaire de mise à jour pour les exécutables"""
    
    def __init__(self, parent_widget=None):
        self.parent = parent_widget
        self.updater_thread = None
    
    def install_executable_update(self, download_url: str, version: str):
        """Lance l'installation d'une mise à jour d'exécutable"""
        try:
            # Déterminer le chemin de l'exécutable actuel
            if getattr(sys, 'frozen', False):
                current_exe = Path(sys.executable)
            else:
                # Mode développement - simuler
                current_exe = Path("MatelasProcessor.exe")
            
            # Dialog de progression
            progress_dialog = QProgressDialog(
                f"Installation de la version {version}...",
                "Annuler",
                0, 100,
                self.parent
            )
            progress_dialog.setWindowTitle("Mise à jour")
            progress_dialog.setModal(True)
            progress_dialog.show()
            
            # Créer et configurer le thread de mise à jour
            self.updater_thread = ExecutableUpdater(download_url, str(current_exe))
            
            # Connecter les signaux
            self.updater_thread.progress_updated.connect(progress_dialog.setValue)
            self.updater_thread.status_updated.connect(progress_dialog.setLabelText)
            self.updater_thread.update_completed.connect(
                lambda: self._on_update_completed(progress_dialog)
            )
            self.updater_thread.error_occurred.connect(
                lambda error: self._on_update_error(progress_dialog, error)
            )
            
            # Gérer l'annulation
            progress_dialog.canceled.connect(self.updater_thread.cancel)
            
            # Lancer la mise à jour
            self.updater_thread.start()
            
        except Exception as e:
            QMessageBox.critical(
                self.parent,
                "Erreur de mise à jour",
                f"Impossible de démarrer la mise à jour:\n{str(e)}"
            )
    
    def _on_update_completed(self, progress_dialog):
        """Appelé quand la mise à jour est terminée"""
        progress_dialog.close()
        
        # Message de succès avec redémarrage automatique
        msg = QMessageBox(self.parent)
        msg.setWindowTitle("Mise à jour terminée")
        msg.setText("La mise à jour a été installée avec succès.")
        msg.setInformativeText("L'application va se fermer et redémarrer automatiquement.")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        msg.exec()
        
        # Fermer l'application (le script batch la redémarrera)
        if self.parent:
            self.parent.close()
        else:
            sys.exit(0)
    
    def _on_update_error(self, progress_dialog, error_msg):
        """Appelé en cas d'erreur de mise à jour"""
        progress_dialog.close()
        
        QMessageBox.critical(
            self.parent,
            "Erreur de mise à jour",
            f"La mise à jour a échoué:\n\n{error_msg}\n\nVeuillez réessayer plus tard."
        )

# Intégration avec le système de mise à jour existant
def create_executable_update_dialog(update_info, parent=None):
    """Crée un dialog spécialisé pour les mises à jour d'exécutable"""
    from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
    
    dialog = QDialog(parent)
    dialog.setWindowTitle("Mise à jour disponible")
    dialog.setFixedSize(500, 300)
    dialog.setModal(True)
    
    layout = QVBoxLayout(dialog)
    
    # Message principal
    title = QLabel(f"🎉 Nouvelle version disponible: {update_info.latest_version}")
    title.setStyleSheet("font-weight: bold; font-size: 14px; color: #2196F3; margin: 10px;")
    layout.addWidget(title)
    
    # Informations
    info_text = f"""
<b>Version actuelle:</b> {update_info.current_version}<br>
<b>Nouvelle version:</b> {update_info.latest_version}<br>
<b>Taille:</b> {update_info.file_size / 1024 / 1024:.1f} MB<br>
<br>
<b>Nouveautés:</b><br>
{update_info.changelog.replace(chr(10), '<br>')}
"""
    
    info_label = QLabel(info_text)
    info_label.setWordWrap(True)
    info_label.setStyleSheet("margin: 10px;")
    layout.addWidget(info_label)
    
    # Avertissement
    warning = QLabel("⚠️ L'application sera redémarrée après l'installation.")
    warning.setStyleSheet("color: #ff6b35; font-weight: bold; margin: 10px;")
    layout.addWidget(warning)
    
    # Boutons
    button_layout = QHBoxLayout()
    
    install_btn = QPushButton("📥 Installer maintenant")
    install_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 8px 16px; }")
    
    later_btn = QPushButton("⏰ Plus tard")
    later_btn.setStyleSheet("QPushButton { padding: 8px 16px; }")
    
    cancel_btn = QPushButton("❌ Ignorer cette version")
    cancel_btn.setStyleSheet("QPushButton { padding: 8px 16px; }")
    
    button_layout.addWidget(install_btn)
    button_layout.addWidget(later_btn)
    button_layout.addWidget(cancel_btn)
    
    layout.addLayout(button_layout)
    
    # Gestionnaire de mise à jour
    update_manager = ExecutableUpdateManager(dialog)
    
    def install_update():
        dialog.accept()
        full_download_url = f"http://72.60.47.183{update_info.download_url}"  # URL complète
        update_manager.install_executable_update(full_download_url, update_info.latest_version)
    
    install_btn.clicked.connect(install_update)
    later_btn.clicked.connect(dialog.reject)
    cancel_btn.clicked.connect(dialog.reject)
    
    return dialog