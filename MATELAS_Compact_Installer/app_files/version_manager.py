#!/usr/bin/env python3
"""
Gestionnaire de version pour l'application Matelas
Gère automatiquement les versions et les mises à jour
"""

import os
import json
import hashlib
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class VersionManager:
    """Gestionnaire de version pour l'application"""
    
    def __init__(self, app_root: str = "."):
        self.app_root = Path(app_root)
        self.version_file = self.app_root / "VERSION.json"
        self.changelog_file = self.app_root / "CHANGELOG.md"
        self.patches_dir = self.app_root / "patches"
        self.backup_dir = self.app_root / "backups"
        
        # Créer les répertoires nécessaires
        self.patches_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)
        
        # Charger ou créer la version actuelle
        self.current_version = self._load_version()
    
    def _load_version(self) -> Dict:
        """Charge la version actuelle depuis le fichier VERSION.json"""
        if self.version_file.exists():
            try:
                with open(self.version_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erreur chargement version: {e}")
        
        # Version par défaut si le fichier n'existe pas
        return {
            "version": "1.0.0",
            "build": "1",
            "date": datetime.now().isoformat(),
            "hash": "",
            "files": {},
            "dependencies": self._get_dependencies()
        }
    
    def _save_version(self):
        """Sauvegarde la version actuelle"""
        try:
            with open(self.version_file, 'w', encoding='utf-8') as f:
                json.dump(self.current_version, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur sauvegarde version: {e}")
    
    def _get_dependencies(self) -> Dict:
        """Récupère les dépendances actuelles"""
        deps = {}
        
        # Lire requirements.txt
        req_file = self.app_root / "requirements_gui.txt"
        if req_file.exists():
            with open(req_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '==' in line:
                            package, version = line.split('==', 1)
                            deps[package] = version
                        else:
                            deps[line] = "latest"
        
        return deps
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calcule le hash SHA256 d'un fichier"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception:
            return ""
    
    def _scan_files(self) -> Dict[str, str]:
        """Scanne tous les fichiers de l'application et calcule leurs hashes"""
        files = {}
        
        # Fichiers et dossiers à inclure
        include_patterns = [
            "*.py",
            "*.json", 
            "*.md",
            "*.txt",
            "*.bat",
            "*.ico",
            "*.png",
            "backend/*",
            "config/*",
            "assets/*",
            "template/*"
        ]
        
        # Fichiers et dossiers à exclure
        exclude_patterns = [
            "__pycache__",
            "*.pyc",
            ".git",
            "logs",
            "output",
            "backups",
            "patches",
            "dist",
            "build",
            ".DS_Store"
        ]
        
        for pattern in include_patterns:
            for file_path in self.app_root.rglob(pattern):
                if file_path.is_file():
                    # Vérifier si le fichier doit être exclu
                    should_exclude = False
                    for exclude in exclude_patterns:
                        if exclude in str(file_path):
                            should_exclude = True
                            break
                    
                    if not should_exclude:
                        relative_path = str(file_path.relative_to(self.app_root))
                        files[relative_path] = self._calculate_file_hash(file_path)
        
        return files
    
    def update_version(self, version_type: str = "patch", description: str = ""):
        """Met à jour la version de l'application"""
        current = self.current_version["version"].split(".")
        major, minor, patch = map(int, current)
        
        if version_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif version_type == "minor":
            minor += 1
            patch = 0
        else:  # patch
            patch += 1
        
        new_version = f"{major}.{minor}.{patch}"
        new_build = str(int(self.current_version["build"]) + 1)
        
        # Scanner les fichiers actuels
        current_files = self._scan_files()
        current_hash = hashlib.sha256(json.dumps(current_files, sort_keys=True).encode()).hexdigest()
        
        # Mettre à jour la version
        self.current_version.update({
            "version": new_version,
            "build": new_build,
            "date": datetime.now().isoformat(),
            "hash": current_hash,
            "files": current_files,
            "dependencies": self._get_dependencies()
        })
        
        # Sauvegarder
        self._save_version()
        
        # Ajouter au changelog
        self._add_to_changelog(new_version, description)
        
        print(f"✅ Version mise à jour: {new_version} (build {new_build})")
        return new_version
    
    def _add_to_changelog(self, version: str, description: str):
        """Ajoute une entrée au changelog"""
        if not self.changelog_file.exists():
            with open(self.changelog_file, 'w', encoding='utf-8') as f:
                f.write("# Changelog\n\n")
        
        with open(self.changelog_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ajouter la nouvelle version en haut
        new_entry = f"## Version {version} - {datetime.now().strftime('%Y-%m-%d')}\n\n"
        if description:
            new_entry += f"{description}\n\n"
        new_entry += "---\n\n"
        
        with open(self.changelog_file, 'w', encoding='utf-8') as f:
            f.write(new_entry + content)
    
    def create_patch(self, target_version: str, description: str = "") -> str:
        """Crée un patch pour une version spécifique"""
        # Créer un backup de la version actuelle
        backup_name = f"backup_v{self.current_version['version']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_path = self.backup_dir / backup_name
        
        # Créer le patch
        patch_name = f"patch_v{target_version}_to_v{self.current_version['version']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        patch_path = self.patches_dir / f"{patch_name}.zip"
        
        with zipfile.ZipFile(patch_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Ajouter les fichiers modifiés
            for file_path, file_hash in self.current_version["files"].items():
                full_path = self.app_root / file_path
                if full_path.exists():
                    zipf.write(full_path, file_path)
            
            # Ajouter les métadonnées du patch
            patch_metadata = {
                "from_version": target_version,
                "to_version": self.current_version["version"],
                "date": datetime.now().isoformat(),
                "description": description,
                "files": self.current_version["files"],
                "dependencies": self.current_version["dependencies"]
            }
            
            zipf.writestr("patch_metadata.json", json.dumps(patch_metadata, indent=2))
        
        print(f"✅ Patch créé: {patch_path}")
        return str(patch_path)
    
    def apply_patch(self, patch_path: str) -> bool:
        """Applique un patch"""
        try:
            with zipfile.ZipFile(patch_path, 'r') as zipf:
                # Vérifier les métadonnées
                if "patch_metadata.json" in zipf.namelist():
                    metadata = json.loads(zipf.read("patch_metadata.json"))
                    print(f"📦 Application du patch: {metadata['from_version']} → {metadata['to_version']}")
                    
                    if metadata.get("description"):
                        print(f"📝 Description: {metadata['description']}")
                
                # Extraire les fichiers
                zipf.extractall(self.app_root)
                
                # Mettre à jour la version
                if "patch_metadata.json" in zipf.namelist():
                    self.current_version.update({
                        "version": metadata["to_version"],
                        "build": str(int(self.current_version["build"]) + 1),
                        "date": datetime.now().isoformat(),
                        "hash": metadata.get("hash", ""),
                        "files": metadata.get("files", {}),
                        "dependencies": metadata.get("dependencies", {})
                    })
                    self._save_version()
                
                print("✅ Patch appliqué avec succès")
                return True
                
        except Exception as e:
            print(f"❌ Erreur lors de l'application du patch: {e}")
            return False
    
    def check_for_updates(self, remote_version_url: str = None) -> Dict:
        """Vérifie s'il y a des mises à jour disponibles"""
        # Pour l'instant, retourne les informations de la version actuelle
        # À étendre avec une vérification en ligne
        return {
            "current_version": self.current_version["version"],
            "current_build": self.current_version["build"],
            "last_update": self.current_version["date"],
            "files_count": len(self.current_version["files"]),
            "dependencies_count": len(self.current_version["dependencies"])
        }
    
    def get_version_info(self) -> Dict:
        """Retourne les informations de version actuelles"""
        return self.current_version.copy()
    
    def list_patches(self) -> List[str]:
        """Liste tous les patches disponibles"""
        patches = []
        for patch_file in self.patches_dir.glob("*.zip"):
            patches.append(str(patch_file))
        return sorted(patches, reverse=True)

# Instance globale
version_manager = VersionManager() 