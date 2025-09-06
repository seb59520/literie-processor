#!/usr/bin/env python3
"""
Consolidateur de packages MATELAS
Regroupe les packages avec le même numéro de version et les upload vers le VPS
"""

import os
import json
import zipfile
import shutil
import requests
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from package_builder import PackageBuilder


@dataclass
class ConsolidatedPackage:
    """Information sur un package consolidé"""
    version: str
    original_packages: List[str]
    consolidated_path: str
    size: int
    files_count: int
    created_at: str


class PackageConsolidator:
    """Gestionnaire de consolidation et d'upload des packages"""
    
    def __init__(self):
        self.builder = PackageBuilder()
        self.base_path = Path.cwd()
        self.updates_path = self.base_path / "online_admin_interface" / "update_storage" / "updates"
        self.consolidated_path = self.updates_path / "consolidated"
        self.consolidated_path.mkdir(parents=True, exist_ok=True)
        
        # Configuration VPS (à personnaliser)
        self.vps_config = {
            "host": "72.60.47.183",
            "username": "root",
            "password": None,  # À définir
            "key_file": None,  # Ou chemin vers clé SSH
            "remote_path": "/var/www/html/update_storage/updates/"
        }
    
    def analyze_packages(self) -> Dict[str, List[str]]:
        """Analyser les packages par numéro de version"""
        version_groups = {}
        
        for zip_file in self.updates_path.glob("*.zip"):
            if zip_file.parent.name == "consolidated":
                continue  # Ignorer les packages déjà consolidés
                
            filename = zip_file.name
            
            # Extraire la version du nom de fichier
            if filename.startswith("matelas_v"):
                # Format: matelas_v3.11.12_... ou matelas_v3.11.12-type_...
                version_part = filename[9:]  # Après "matelas_v"
                
                if "_" in version_part:
                    version = version_part.split("_")[0]
                    # Enlever le suffixe de type s'il existe
                    if "-" in version:
                        version = version.split("-")[0]
                    
                    if version not in version_groups:
                        version_groups[version] = []
                    version_groups[version].append(str(zip_file))
        
        return version_groups
    
    def consolidate_version_packages(self, version: str, package_paths: List[str]) -> Optional[ConsolidatedPackage]:
        """Consolider tous les packages d'une version en un seul ZIP"""
        if len(package_paths) <= 1:
            print(f"ℹ️ Version {version}: Un seul package, pas de consolidation nécessaire")
            return None
        
        print(f"📦 Consolidation de la version {version} ({len(package_paths)} packages)")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        consolidated_name = f"matelas_v{version}_consolidated_{timestamp}.zip"
        consolidated_path = self.consolidated_path / consolidated_name
        
        all_files = {}  # path -> (content, metadata)
        all_metadata = []
        total_files = 0
        
        try:
            # Stocker les packages pour le changelog
            self._current_packages = package_paths
            
            # Extraire tous les fichiers de tous les packages
            for package_path in package_paths:
                print(f"   📂 Traitement de {Path(package_path).name}")
                
                with zipfile.ZipFile(package_path, 'r') as zip_ref:
                    # Lire les métadonnées
                    try:
                        metadata_json = zip_ref.read('metadata.json').decode('utf-8')
                        metadata = json.loads(metadata_json)
                        all_metadata.append(metadata)
                    except Exception as e:
                        print(f"      ⚠️ Métadonnées manquantes: {e}")
                    
                    # Extraire tous les fichiers (sauf metadata.json)
                    for file_info in zip_ref.filelist:
                        if file_info.filename == 'metadata.json':
                            continue
                            
                        file_content = zip_ref.read(file_info.filename)
                        
                        # En cas de conflit, prendre le plus récent
                        if file_info.filename in all_files:
                            print(f"      🔄 Écrasement de {file_info.filename}")
                        
                        all_files[file_info.filename] = file_content
                        total_files += 1
            
            # Créer les métadonnées consolidées
            consolidated_metadata = {
                "version": version,
                "consolidated": True,
                "original_packages": [Path(p).name for p in package_paths],
                "timestamp": timestamp,
                "build_date": datetime.now().strftime("%Y-%m-%d"),
                "description": f"Package consolidé version {version}",
                "changelog": self._generate_consolidated_changelog(all_metadata),
                "type": "consolidé",
                "files_count": len(all_files),
                "created_by": "Package Consolidator",
                "requires_restart": True,
                "backup_before_install": True
            }
            
            # Créer le package consolidé
            with zipfile.ZipFile(consolidated_path, 'w', zipfile.ZIP_DEFLATED) as consolidated_zip:
                # Ajouter les métadonnées
                consolidated_zip.writestr('metadata.json', 
                                        json.dumps(consolidated_metadata, indent=2, ensure_ascii=False))
                
                # Ajouter tous les fichiers
                for file_path, file_content in all_files.items():
                    consolidated_zip.writestr(file_path, file_content)
            
            size = consolidated_path.stat().st_size
            
            print(f"   ✅ Package consolidé créé: {consolidated_name}")
            print(f"   📊 {len(all_files)} fichiers, {size/1024:.1f} KB")
            
            return ConsolidatedPackage(
                version=version,
                original_packages=[Path(p).name for p in package_paths],
                consolidated_path=str(consolidated_path),
                size=size,
                files_count=len(all_files),
                created_at=timestamp
            )
            
        except Exception as e:
            print(f"❌ Erreur lors de la consolidation: {e}")
            return None
    
    def _generate_consolidated_changelog(self, metadata_list: List[Dict]) -> str:
        """Générer un changelog consolidé intelligent"""
        changes = []
        package_types = set()
        
        # Analyser les types de packages à partir des noms de fichiers
        for package_name in [Path(p).name for p in getattr(self, '_current_packages', [])]:
            if '-config_' in package_name:
                package_types.add('Configuration')
            elif '-backend_' in package_name:
                package_types.add('Backend/Traitement')
            elif '-interface_' in package_name:
                package_types.add('Interface Utilisateur')
            elif '-scripts_' in package_name:
                package_types.add('Scripts/Utilitaires')
            elif '-referentiel_' in package_name:
                package_types.add('Référentiels Métier')
            elif '-template_' in package_name:
                package_types.add('Templates Excel')
            else:
                package_types.add('Corrections Générales')
        
        # Générer un changelog détaillé
        if package_types:
            changes.append("MISE À JOUR CONSOLIDÉE v3.11.12:")
            changes.append("")
            
            for pkg_type in sorted(package_types):
                if pkg_type == 'Configuration':
                    changes.append("📋 CONFIGURATION:")
                    changes.append("   • Mise à jour des paramètres système")
                    changes.append("   • Correction des URLs de serveur")
                    changes.append("   • Optimisation des configurations LLM")
                elif pkg_type == 'Backend/Traitement':
                    changes.append("⚙️ BACKEND/TRAITEMENT:")
                    changes.append("   • Améliorations des utilitaires de traitement")
                    changes.append("   • Optimisations des performances")
                    changes.append("   • Corrections de bugs système")
                elif pkg_type == 'Interface Utilisateur':
                    changes.append("🖥️ INTERFACE UTILISATEUR:")
                    changes.append("   • Nouvelles fonctionnalités GUI")
                    changes.append("   • Générateur de packages correctifs")
                    changes.append("   • Améliorations ergonomiques")
                elif pkg_type == 'Scripts/Utilitaires':
                    changes.append("🛠️ SCRIPTS/UTILITAIRES:")
                    changes.append("   • Nouveaux outils de maintenance")
                    changes.append("   • Scripts d'automatisation")
                    changes.append("   • Utilitaires de diagnostic")
                elif pkg_type == 'Référentiels Métier':
                    changes.append("📊 RÉFÉRENTIELS MÉTIER:")
                    changes.append("   • Mise à jour des données produits")
                    changes.append("   • Corrections des tarifs")
                    changes.append("   • Nouveaux référentiels")
                elif pkg_type == 'Templates Excel':
                    changes.append("📄 TEMPLATES EXCEL:")
                    changes.append("   • Mise à jour des modèles")
                    changes.append("   • Corrections de formatage")
                    changes.append("   • Nouveaux templates")
                else:
                    changes.append(f"🔧 {pkg_type.upper()}:")
                    changes.append("   • Corrections et améliorations diverses")
                
                changes.append("")
            
            changes.append("⚠️ IMPORTANT:")
            changes.append("   • Redémarrage de l'application requis")
            changes.append("   • Sauvegarde automatique avant installation")
            changes.append(f"   • {len(getattr(self, '_current_packages', []))} packages consolidés")
        
        return "\n".join(changes) if changes else "Consolidation de plusieurs packages correctifs"
    
    def upload_to_vps(self, package_path: str) -> bool:
        """Upload un package vers le VPS via l'API du serveur de mises à jour"""
        try:
            # NOUVELLE APPROCHE: Utiliser directement l'API du serveur au lieu de SFTP
            local_file = Path(package_path)
            return self._register_package_in_api(local_file)
            
        except Exception as e:
            print(f"❌ Erreur upload: {e}")
            return False
    
    def _register_package_in_api(self, package_path: Path) -> bool:
        """Enregistrer le package dans l'API du serveur de mises à jour"""
        try:
            
            # Extraire la version du nom de fichier
            version_match = re.search(r'v(\d+\.\d+\.\d+)', package_path.name)
            if not version_match:
                print(f"⚠️ Impossible d'extraire la version de {package_path.name}")
                return False
            
            version = version_match.group(1)
            
            # Générer un changelog intelligent basé sur les packages consolidés
            changelog = self._generate_intelligent_changelog(package_path)
            description = self._generate_package_description(package_path)
            
            # Préparer les métadonnées du package
            package_metadata = {
                "version": version,
                "filename": package_path.name,
                "description": description,
                "changelog": changelog,
                "release_date": datetime.now().isoformat(),
                "file_size": package_path.stat().st_size
            }
            
            # URL de l'API d'upload du serveur
            api_url = f"http://{self.vps_config['host']}/api/v1/upload"
            print(f"📤 Upload via API vers {api_url}")
            
            # Préparer les données multipart pour l'upload
            with open(package_path, 'rb') as f:
                files = {'file': (package_path.name, f, 'application/zip')}
                data = {
                    'version': version,
                    'description': package_metadata['description'],
                    'changelog': package_metadata['changelog']
                }
                
                # Faire l'appel API pour uploader la version
                response = requests.post(
                    api_url,
                    files=files,
                    data=data,
                    timeout=60  # Plus de temps pour l'upload
                )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success", False):
                    print(f"✅ API: Version {version} enregistrée avec succès")
                    return True
                else:
                    print(f"❌ API: Échec enregistrement - {result.get('message', 'Erreur inconnue')}")
                    return False
            else:
                print(f"❌ API: Erreur HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur enregistrement API: {e}")
            return False
    
    def _generate_intelligent_changelog(self, package_path: Path) -> str:
        """Générer un changelog intelligent basé sur le contenu du package"""
        try:
            # Si c'est un package consolidé, on peut lire son metadata
            metadata_files = []
            
            # Essayer de lire les métadonnées du package ZIP
            with zipfile.ZipFile(package_path, 'r') as zip_file:
                for file_name in zip_file.namelist():
                    if file_name.endswith('_metadata.json'):
                        metadata_files.append(file_name)
            
            if metadata_files:
                # Utiliser la fonction existante pour générer un changelog détaillé
                # On simule une liste de packages pour la fonction existante
                package_names = []
                for metadata_file in metadata_files:
                    # Extraire le nom du package du fichier de métadonnées
                    pkg_name = metadata_file.replace('_metadata.json', '')
                    package_names.append(pkg_name)
                
                # Réutiliser la logique existante
                changelog = self._generate_changelog_from_packages(package_names)
                return changelog
            else:
                # Fallback si pas de métadonnées spécifiques
                return f"Mise à jour consolidée avec corrections et améliorations multiples"
                
        except Exception as e:
            print(f"⚠️ Erreur génération changelog: {e}")
            return "Mise à jour consolidée avec corrections et améliorations"
    
    def _generate_package_description(self, package_path: Path) -> str:
        """Générer une description intelligente du package"""
        try:
            version_match = re.search(r'v(\d+\.\d+\.\d+)', package_path.name)
            version = version_match.group(1) if version_match else "inconnue"
            
            # Analyser le nom du fichier pour plus de contexte
            if "consolidated" in package_path.name.lower():
                return f"Package consolidé MATELAS v{version} - Mise à jour complète avec corrections multiples"
            elif "patch" in package_path.name.lower():
                return f"Package correctif MATELAS v{version} - Corrections ciblées"
            else:
                return f"Mise à jour MATELAS v{version} - Améliorations et corrections"
                
        except Exception:
            return "Package de mise à jour MATELAS avec améliorations"
    
    def _generate_changelog_from_packages(self, package_names: list) -> str:
        """Générer un changelog basé sur une liste de noms de packages"""
        package_types = set()
        changes = []
        
        # Analyser les types de packages
        for package_name in package_names:
            if 'config' in package_name or 'settings' in package_name:
                package_types.add('Configuration')
            elif 'backend' in package_name or 'utils' in package_name:
                package_types.add('Backend/Traitement')
            elif 'gui' in package_name or 'interface' in package_name or 'app_gui' in package_name:
                package_types.add('Interface Utilisateur')
            elif 'script' in package_name or 'tool' in package_name:
                package_types.add('Scripts/Utilitaires')
            elif 'referentiel' in package_name or 'data' in package_name:
                package_types.add('Référentiels Métier')
            elif 'template' in package_name or 'excel' in package_name:
                package_types.add('Templates Excel')
            else:
                package_types.add('Corrections Générales')
        
        # Générer le changelog
        if package_types:
            changes.append("🎯 MISE À JOUR CONSOLIDÉE:")
            changes.append("")
            
            for pkg_type in sorted(package_types):
                if pkg_type == 'Configuration':
                    changes.append("📋 CONFIGURATION:")
                    changes.append("   • Mise à jour des paramètres système")
                    changes.append("   • Optimisation des configurations")
                elif pkg_type == 'Backend/Traitement':
                    changes.append("⚙️ BACKEND/TRAITEMENT:")
                    changes.append("   • Améliorations des utilitaires")
                    changes.append("   • Optimisations des performances")
                elif pkg_type == 'Interface Utilisateur':
                    changes.append("🖥️ INTERFACE UTILISATEUR:")
                    changes.append("   • Améliorations ergonomiques")
                    changes.append("   • Nouvelles fonctionnalités GUI")
                elif pkg_type == 'Scripts/Utilitaires':
                    changes.append("🛠️ SCRIPTS/UTILITAIRES:")
                    changes.append("   • Outils de maintenance")
                    changes.append("   • Scripts d'automatisation")
                elif pkg_type == 'Référentiels Métier':
                    changes.append("📊 RÉFÉRENTIELS:")
                    changes.append("   • Mise à jour des données")
                elif pkg_type == 'Templates Excel':
                    changes.append("📄 TEMPLATES:")
                    changes.append("   • Mise à jour des modèles")
                else:
                    changes.append(f"🔧 {pkg_type.upper()}:")
                    changes.append("   • Corrections diverses")
                changes.append("")
            
            changes.append("⚠️ INSTALLATION:")
            changes.append("   • Redémarrage de l'application recommandé")
            changes.append("   • Sauvegarde automatique des données")
        
        return "\n".join(changes) if changes else "Mise à jour avec corrections et améliorations"
    
    def consolidate_and_upload_all(self, upload_to_vps: bool = True) -> Dict[str, ConsolidatedPackage]:
        """Consolider toutes les versions et optionnellement upload vers VPS"""
        print("🚀 Consolidation et Upload des packages")
        print("=" * 50)
        
        # Analyser les packages par version
        version_groups = self.analyze_packages()
        
        if not version_groups:
            print("ℹ️ Aucun package à consolider")
            return {}
        
        print(f"📊 {len(version_groups)} version(s) détectée(s):")
        for version, packages in version_groups.items():
            print(f"   • v{version}: {len(packages)} package(s)")
        
        consolidated_packages = {}
        
        # Consolider chaque version
        for version, packages in version_groups.items():
            consolidated = self.consolidate_version_packages(version, packages)
            
            if consolidated:
                consolidated_packages[version] = consolidated
                
                # Upload vers VPS si demandé
                if upload_to_vps:
                    print(f"📤 Upload de la version {version}...")
                    success = self.upload_to_vps(consolidated.consolidated_path)
                    
                    if success:
                        print(f"✅ Version {version} uploadée avec succès")
                    else:
                        print(f"❌ Échec upload version {version}")
        
        print(f"\n🎉 Consolidation terminée: {len(consolidated_packages)} package(s) consolidé(s)")
        return consolidated_packages
    
    def configure_vps_access(self, host: str = None, username: str = None, 
                           password: str = None, key_file: str = None):
        """Configurer l'accès VPS"""
        if host:
            self.vps_config["host"] = host
        if username:
            self.vps_config["username"] = username
        if password:
            self.vps_config["password"] = password
        if key_file:
            self.vps_config["key_file"] = key_file
        
        print(f"🔧 Configuration VPS mise à jour: {self.vps_config['host']}")


def create_consolidation_gui():
    """Interface graphique pour la consolidation (optionnelle)"""
    try:
        from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                                   QLabel, QTextEdit, QCheckBox, QLineEdit, 
                                   QFormLayout, QGroupBox, QProgressBar)
        from PyQt6.QtCore import QThread, pyqtSignal
        
        class ConsolidationDialog(QDialog):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.setWindowTitle("📦 Consolidation et Upload des Packages")
                self.setMinimumSize(600, 500)
                
                # Fix transparence : définir une couleur de fond solide
                self.setStyleSheet("""
                    QDialog {
                        background-color: #f8f9fa;
                        color: #333;
                    }
                    QGroupBox {
                        font-weight: bold;
                        border: 2px solid #ddd;
                        border-radius: 5px;
                        margin-top: 10px;
                        padding-top: 10px;
                        background-color: white;
                    }
                    QGroupBox::title {
                        subcontrol-origin: margin;
                        left: 10px;
                        padding: 0 5px 0 5px;
                    }
                    QPushButton {
                        padding: 8px 15px;
                        border: 1px solid #007bff;
                        border-radius: 4px;
                        background-color: #007bff;
                        color: white;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #0056b3;
                    }
                    QPushButton:disabled {
                        background-color: #6c757d;
                        border-color: #6c757d;
                    }
                    QLineEdit {
                        padding: 8px;
                        border: 1px solid #ddd;
                        border-radius: 4px;
                        background-color: white;
                    }
                    QTextEdit {
                        border: 1px solid #ddd;
                        border-radius: 4px;
                        background-color: white;
                        font-family: 'Consolas', 'Monaco', monospace;
                    }
                    QCheckBox {
                        spacing: 5px;
                    }
                    QCheckBox::indicator {
                        width: 18px;
                        height: 18px;
                    }
                    QProgressBar {
                        border: 1px solid #ddd;
                        border-radius: 4px;
                        text-align: center;
                        background-color: #f8f9fa;
                    }
                    QProgressBar::chunk {
                        background-color: #007bff;
                        border-radius: 3px;
                    }
                """)
                
                self.consolidator = PackageConsolidator()
                self.setup_ui()
            
            def setup_ui(self):
                layout = QVBoxLayout(self)
                
                # Configuration VPS
                vps_group = QGroupBox("Configuration VPS")
                vps_layout = QFormLayout()
                
                self.host_input = QLineEdit("72.60.47.183")
                self.username_input = QLineEdit("root")
                self.password_input = QLineEdit()
                self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
                
                vps_layout.addRow("Serveur:", self.host_input)
                vps_layout.addRow("Utilisateur:", self.username_input)
                vps_layout.addRow("Mot de passe:", self.password_input)
                
                vps_group.setLayout(vps_layout)
                layout.addWidget(vps_group)
                
                # Options
                options_group = QGroupBox("Options")
                options_layout = QVBoxLayout()
                
                self.upload_checkbox = QCheckBox("Upload automatique vers VPS")
                self.upload_checkbox.setChecked(True)
                
                options_layout.addWidget(self.upload_checkbox)
                options_group.setLayout(options_layout)
                layout.addWidget(options_group)
                
                # Zone de log
                self.log_text = QTextEdit()
                self.log_text.setMaximumHeight(200)
                layout.addWidget(QLabel("Log:"))
                layout.addWidget(self.log_text)
                
                # Barre de progression
                self.progress_bar = QProgressBar()
                self.progress_bar.hide()
                layout.addWidget(self.progress_bar)
                
                # Boutons
                buttons_layout = QHBoxLayout()
                
                self.analyze_btn = QPushButton("📊 Analyser")
                self.consolidate_btn = QPushButton("🚀 Consolider et Upload")
                self.close_btn = QPushButton("❌ Fermer")
                
                self.analyze_btn.clicked.connect(self.analyze_packages)
                self.consolidate_btn.clicked.connect(self.start_consolidation)
                self.close_btn.clicked.connect(self.reject)
                
                buttons_layout.addWidget(self.analyze_btn)
                buttons_layout.addWidget(self.consolidate_btn)
                buttons_layout.addWidget(self.close_btn)
                
                layout.addLayout(buttons_layout)
            
            def analyze_packages(self):
                """Analyser les packages disponibles"""
                self.log_text.clear()
                
                version_groups = self.consolidator.analyze_packages()
                
                if not version_groups:
                    self.log_text.append("ℹ️ Aucun package à consolider")
                    return
                
                self.log_text.append(f"📊 {len(version_groups)} version(s) détectée(s):")
                
                for version, packages in version_groups.items():
                    self.log_text.append(f"   • v{version}: {len(packages)} package(s)")
                    for pkg in packages:
                        pkg_name = Path(pkg).name
                        self.log_text.append(f"      - {pkg_name}")
            
            def start_consolidation(self):
                """Démarrer la consolidation"""
                # Configurer VPS
                self.consolidator.configure_vps_access(
                    host=self.host_input.text(),
                    username=self.username_input.text(),
                    password=self.password_input.text()
                )
                
                self.log_text.clear()
                self.progress_bar.show()
                self.consolidate_btn.setEnabled(False)
                
                # Lancer la consolidation
                upload = self.upload_checkbox.isChecked()
                result = self.consolidator.consolidate_and_upload_all(upload)
                
                if result:
                    self.log_text.append(f"✅ {len(result)} package(s) consolidé(s)")
                else:
                    self.log_text.append("ℹ️ Aucun package à consolider")
                
                self.progress_bar.hide()
                self.consolidate_btn.setEnabled(True)
        
        return ConsolidationDialog
        
    except ImportError:
        return None


if __name__ == "__main__":
    import sys
    
    consolidator = PackageConsolidator()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        # Mode graphique
        gui_class = create_consolidation_gui()
        if gui_class:
            from PyQt6.QtWidgets import QApplication
            app = QApplication.instance() or QApplication(sys.argv)
            
            dialog = gui_class()
            dialog.exec()
        else:
            print("❌ PyQt6 non disponible pour l'interface graphique")
    else:
        # Mode console
        print("🔐 Configuration requise pour l'upload VPS")
        password = input("Mot de passe root VPS (ou Entrée pour ignorer l'upload): ").strip()
        
        if password:
            consolidator.configure_vps_access(password=password)
            upload = True
        else:
            upload = False
        
        consolidator.consolidate_and_upload_all(upload_to_vps=upload)