#!/usr/bin/env python3
"""
Générateur de packages correctifs MATELAS
Permet de créer des packages de mise à jour directement depuis l'application
"""

import os
import zipfile
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import hashlib

from version import VERSION, BUILD_DATE


class PackageBuilder:
    """Constructeur de packages correctifs MATELAS"""
    
    def __init__(self):
        self.base_path = Path.cwd()
        self.update_path = self.base_path / "online_admin_interface" / "update_storage" / "updates"
        self.current_version = VERSION
        
        # S'assurer que le répertoire existe
        self.update_path.mkdir(parents=True, exist_ok=True)
    
    def get_next_version(self) -> str:
        """Calculer la prochaine version corrective"""
        parts = self.current_version.split('.')
        if len(parts) >= 3:
            # Incrémenter le patch number
            parts[2] = str(int(parts[2]) + 1)
            return '.'.join(parts)
        return f"{self.current_version}.1"
    
    def create_package_metadata(self, version: str, description: str, 
                              files: List[str], changelog: str = "") -> Dict:
        """Créer les métadonnées du package"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Calculer les hashes des fichiers
        file_hashes = {}
        for file_path in files:
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    file_hashes[file_path] = hashlib.sha256(f.read()).hexdigest()
        
        metadata = {
            "version": version,
            "previous_version": self.current_version,
            "timestamp": timestamp,
            "build_date": datetime.now().strftime("%Y-%m-%d"),
            "description": description,
            "changelog": changelog,
            "type": "correctif",
            "files": files,
            "file_hashes": file_hashes,
            "created_by": "Package Builder GUI",
            "requires_restart": True,
            "backup_before_install": True
        }
        
        return metadata
    
    def get_critical_files(self) -> List[str]:
        """Retourner la liste des fichiers critiques à inclure par défaut"""
        critical_files = [
            "app_gui.py",
            "version.py",
            "backend_interface.py",
            "config.py"
        ]
        
        # Ajouter les fichiers backend critiques
        backend_files = [
            "backend/main.py",
            "backend/llm_provider.py",
            "backend/excel_import_utils.py",
            "backend/requirements.txt"
        ]
        
        # Vérifier quels fichiers existent
        existing_files = []
        for file_path in critical_files + backend_files:
            if os.path.exists(file_path):
                existing_files.append(file_path)
        
        return existing_files
    
    def create_correction_package(self, description: str, files_to_include: List[str], 
                                 changelog: str = "", custom_version: str = None) -> Dict:
        """Créer un package correctif complet"""
        
        # Déterminer la version
        if custom_version:
            new_version = custom_version
        else:
            new_version = self.get_next_version()
        
        # Créer les métadonnées
        metadata = self.create_package_metadata(new_version, description, files_to_include, changelog)
        
        # Nom du fichier ZIP
        timestamp = metadata["timestamp"]
        zip_filename = f"matelas_v{new_version}_{timestamp}.zip"
        zip_path = self.update_path / zip_filename
        
        try:
            # Créer le package ZIP
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                
                # Ajouter le fichier de métadonnées
                metadata_json = json.dumps(metadata, indent=2, ensure_ascii=False)
                zipf.writestr("update_metadata.json", metadata_json)
                
                # Ajouter les fichiers sélectionnés
                for file_path in files_to_include:
                    if os.path.exists(file_path):
                        # Préserver la structure des dossiers
                        arcname = file_path
                        zipf.write(file_path, arcname)
                        print(f"✓ Ajouté: {file_path}")
                    else:
                        print(f"⚠️ Fichier non trouvé: {file_path}")
                
                # Ajouter un script d'installation si nécessaire
                install_script = self._create_install_script(metadata)
                zipf.writestr("install.py", install_script)
            
            # Calculer la taille du fichier
            file_size = zip_path.stat().st_size
            
            result = {
                "success": True,
                "package_path": str(zip_path),
                "package_name": zip_filename,
                "version": new_version,
                "size": file_size,
                "files_count": len(files_to_include),
                "metadata": metadata
            }
            
            print(f"✅ Package créé avec succès: {zip_filename}")
            print(f"📦 Taille: {file_size / 1024:.1f} KB")
            print(f"📁 Emplacement: {zip_path}")
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "package_path": None
            }
    
    def _create_install_script(self, metadata: Dict) -> str:
        """Créer un script d'installation automatique pour le package"""
        script = f'''#!/usr/bin/env python3
"""
Script d'installation automatique pour le package {metadata["version"]}
Généré automatiquement par Package Builder
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path

def backup_files(files_to_backup):
    """Sauvegarder les fichiers existants"""
    backup_dir = Path("backup") / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    for file_path in files_to_backup:
        if os.path.exists(file_path):
            dest_path = backup_dir / file_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file_path, dest_path)
            print(f"📋 Sauvegardé: {{file_path}}")
    
    return str(backup_dir)

def install_update():
    """Installer la mise à jour"""
    print("🚀 Installation de la mise à jour v{metadata['version']}")
    print("=" * 50)
    
    # Charger les métadonnées
    with open("update_metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)
    
    # Sauvegarder les fichiers existants
    if metadata.get("backup_before_install", True):
        backup_dir = backup_files(metadata["files"])
        print(f"💾 Backup créé dans: {{backup_dir}}")
    
    # Copier les nouveaux fichiers
    for file_path in metadata["files"]:
        if os.path.exists(file_path):
            # Le fichier est dans le ZIP, il sera extrait automatiquement
            print(f"📝 Mis à jour: {{file_path}}")
    
    print("✅ Installation terminée avec succès!")
    print("⚠️  Redémarrage de l'application recommandé")

if __name__ == "__main__":
    install_update()
'''
        return script
    
    def list_available_packages(self) -> List[Dict]:
        """Lister les packages disponibles dans le répertoire"""
        packages = []
        
        for zip_file in self.update_path.glob("*.zip"):
            try:
                with zipfile.ZipFile(zip_file, 'r') as zipf:
                    if "update_metadata.json" in zipf.namelist():
                        metadata_content = zipf.read("update_metadata.json").decode('utf-8')
                        metadata = json.loads(metadata_content)
                        
                        packages.append({
                            "filename": zip_file.name,
                            "path": str(zip_file),
                            "size": zip_file.stat().st_size,
                            "created": zip_file.stat().st_mtime,
                            "metadata": metadata
                        })
            except Exception as e:
                print(f"Erreur lecture package {zip_file.name}: {e}")
        
        # Trier par date de création (plus récent en premier)
        packages.sort(key=lambda x: x["created"], reverse=True)
        
        return packages


def create_quick_correction_package(description: str, files: List[str] = None, 
                                   changelog: str = "") -> Dict:
    """Fonction utilitaire pour créer rapidement un package correctif"""
    builder = PackageBuilder()
    
    if files is None:
        files = builder.get_critical_files()
    
    return builder.create_correction_package(description, files, changelog)


if __name__ == "__main__":
    # Test de création d'un package
    builder = PackageBuilder()
    critical_files = builder.get_critical_files()
    
    result = builder.create_correction_package(
        description="Test package correctif",
        files_to_include=critical_files,
        changelog="Test de génération de package depuis le module"
    )
    
    if result["success"]:
        print(f"Package de test créé: {result['package_name']}")
    else:
        print(f"Erreur: {result['error']}")