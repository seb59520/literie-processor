#!/usr/bin/env python3
"""
Serveur de mises à jour pour l'application MATELAS_FINAL
Héberge les versions et permet le téléchargement des mises à jour
"""

import os
import json
import hashlib
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

class UpdateServer:
    """Serveur de mises à jour"""
    
    def __init__(self, storage_path: str = "update_storage"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        
        # Dossiers pour les différentes ressources
        self.versions_dir = self.storage_path / "versions"
        self.patches_dir = self.storage_path / "patches"
        self.metadata_dir = self.storage_path / "metadata"
        
        for directory in [self.versions_dir, self.patches_dir, self.metadata_dir]:
            directory.mkdir(exist_ok=True)
        
        # Fichier de métadonnées principal
        self.manifest_file = self.metadata_dir / "manifest.json"
        self.manifest = self._load_manifest()
        
        # Initialiser FastAPI
        self.app = FastAPI(
            title="MATELAS Update Server",
            description="Serveur de mises à jour automatiques",
            version="1.0.0"
        )
        
        # Configuration CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        self._setup_routes()
    
    def _load_manifest(self) -> Dict:
        """Charge le manifest des versions disponibles"""
        if self.manifest_file.exists():
            try:
                with open(self.manifest_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erreur chargement manifest: {e}")
        
        return {
            "server_version": "1.0.0",
            "last_update": datetime.now().isoformat(),
            "versions": [],
            "patches": [],
            "statistics": {
                "total_downloads": 0,
                "active_versions": 0
            }
        }
    
    def _save_manifest(self):
        """Sauvegarde le manifest"""
        try:
            with open(self.manifest_file, 'w', encoding='utf-8') as f:
                json.dump(self.manifest, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur sauvegarde manifest: {e}")
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calcule le hash SHA256 d'un fichier"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception:
            return ""
    
    def _setup_routes(self):
        """Configure les routes de l'API"""
        
        @self.app.get("/")
        async def root():
            """Page d'accueil du serveur de mises à jour"""
            return {
                "service": "MATELAS Update Server",
                "version": "1.0.0",
                "status": "running",
                "available_versions": len(self.manifest["versions"]),
                "available_patches": len(self.manifest["patches"])
            }
        
        @self.app.get("/api/v1/check-updates")
        async def check_updates(current_version: str = "1.0.0"):
            """Vérifie s'il y a des mises à jour disponibles"""
            try:
                available_versions = self.manifest["versions"]
                
                if not available_versions:
                    return {
                        "update_available": False,
                        "current_version": current_version,
                        "message": "Aucune mise à jour disponible"
                    }
                
                # Trouver la version la plus récente
                latest_version = max(available_versions, key=lambda v: v["version"])
                
                update_available = self._is_newer_version(
                    latest_version["version"], 
                    current_version
                )
                
                response = {
                    "update_available": update_available,
                    "current_version": current_version,
                    "latest_version": latest_version["version"] if update_available else current_version,
                    "release_date": latest_version.get("date", ""),
                    "description": latest_version.get("description", ""),
                    "download_url": f"/api/v1/download/{latest_version['version']}" if update_available else None,
                    "file_size": latest_version.get("size", 0) if update_available else 0,
                    "changelog": latest_version.get("changelog", "") if update_available else ""
                }
                
                return response
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Erreur lors de la vérification: {str(e)}")
        
        @self.app.get("/api/v1/versions")
        async def list_versions():
            """Liste toutes les versions disponibles"""
            return {
                "versions": sorted(self.manifest["versions"], 
                                 key=lambda v: v["version"], 
                                 reverse=True),
                "total": len(self.manifest["versions"])
            }
        
        @self.app.get("/api/v1/download/{version}")
        async def download_version(version: str):
            """Télécharge une version spécifique"""
            try:
                # Chercher la version dans le manifest
                version_info = None
                for v in self.manifest["versions"]:
                    if v["version"] == version:
                        version_info = v
                        break
                
                if not version_info:
                    raise HTTPException(status_code=404, detail="Version non trouvée")
                
                file_path = self.versions_dir / version_info["filename"]
                
                if not file_path.exists():
                    raise HTTPException(status_code=404, detail="Fichier de version non trouvé")
                
                # Incrémenter le compteur de téléchargements
                self.manifest["statistics"]["total_downloads"] += 1
                version_info["downloads"] = version_info.get("downloads", 0) + 1
                self._save_manifest()
                
                return FileResponse(
                    path=file_path,
                    filename=version_info["filename"],
                    media_type='application/zip'
                )
                
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Erreur téléchargement: {str(e)}")
        
        @self.app.post("/api/v1/upload")
        async def upload_version(
            version: str,
            description: str = "",
            changelog: str = "",
            file: UploadFile = File(...)
        ):
            """Upload une nouvelle version"""
            try:
                # Vérifier que c'est un fichier ZIP
                if not file.filename.endswith('.zip'):
                    raise HTTPException(status_code=400, detail="Le fichier doit être un ZIP")
                
                # Générer le nom de fichier
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"matelas_v{version}_{timestamp}.zip"
                file_path = self.versions_dir / filename
                
                # Sauvegarder le fichier
                with open(file_path, 'wb') as f:
                    content = await file.read()
                    f.write(content)
                
                # Calculer les métadonnées
                file_hash = self._calculate_file_hash(file_path)
                file_size = file_path.stat().st_size
                
                # Ajouter au manifest
                version_info = {
                    "version": version,
                    "filename": filename,
                    "date": datetime.now().isoformat(),
                    "description": description,
                    "changelog": changelog,
                    "size": file_size,
                    "hash": file_hash,
                    "downloads": 0
                }
                
                # Supprimer l'ancienne version si elle existe
                self.manifest["versions"] = [
                    v for v in self.manifest["versions"] 
                    if v["version"] != version
                ]
                
                self.manifest["versions"].append(version_info)
                self.manifest["last_update"] = datetime.now().isoformat()
                self.manifest["statistics"]["active_versions"] = len(self.manifest["versions"])
                
                self._save_manifest()
                
                return {
                    "success": True,
                    "message": f"Version {version} uploadée avec succès",
                    "version_info": version_info
                }
                
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Erreur upload: {str(e)}")
        
        @self.app.delete("/api/v1/versions/{version}")
        async def delete_version(version: str):
            """Supprime une version"""
            try:
                # Trouver et supprimer la version
                version_info = None
                for i, v in enumerate(self.manifest["versions"]):
                    if v["version"] == version:
                        version_info = self.manifest["versions"].pop(i)
                        break
                
                if not version_info:
                    raise HTTPException(status_code=404, detail="Version non trouvée")
                
                # Supprimer le fichier
                file_path = self.versions_dir / version_info["filename"]
                if file_path.exists():
                    file_path.unlink()
                
                # Mettre à jour le manifest
                self.manifest["statistics"]["active_versions"] = len(self.manifest["versions"])
                self._save_manifest()
                
                return {
                    "success": True,
                    "message": f"Version {version} supprimée avec succès"
                }
                
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Erreur suppression: {str(e)}")
        
        @self.app.get("/api/v1/statistics")
        async def get_statistics():
            """Retourne les statistiques du serveur"""
            return {
                "statistics": self.manifest["statistics"],
                "server_info": {
                    "uptime": "N/A",  # À implémenter
                    "storage_used": self._get_storage_size(),
                    "last_update": self.manifest["last_update"]
                }
            }
    
    def _is_newer_version(self, version1: str, version2: str) -> bool:
        """Compare deux versions et retourne True si version1 > version2"""
        try:
            v1_parts = list(map(int, version1.split('.')))
            v2_parts = list(map(int, version2.split('.')))
            
            # Égaliser la longueur des versions
            max_len = max(len(v1_parts), len(v2_parts))
            v1_parts.extend([0] * (max_len - len(v1_parts)))
            v2_parts.extend([0] * (max_len - len(v2_parts)))
            
            return v1_parts > v2_parts
        except Exception:
            return version1 != version2
    
    def _get_storage_size(self) -> int:
        """Calcule la taille totale du stockage utilisé"""
        total_size = 0
        try:
            for file_path in self.storage_path.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
        except Exception:
            pass
        return total_size
    
    def run(self, host: str = "0.0.0.0", port: int = 8080):
        """Lance le serveur"""
        print(f"🚀 Démarrage du serveur de mises à jour sur {host}:{port}")
        print(f"📁 Stockage: {self.storage_path}")
        print(f"📦 Versions disponibles: {len(self.manifest['versions'])}")
        
        uvicorn.run(self.app, host=host, port=port)

# Utilitaire pour créer un package de mise à jour
def create_update_package(source_dir: str, version: str, output_dir: str = "updates") -> str:
    """Crée un package de mise à jour à partir du code source"""
    source_path = Path(source_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Nom du fichier de sortie
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"matelas_v{version}_{timestamp}.zip"
    zip_path = output_path / zip_filename
    
    print(f"🎁 Création du package de mise à jour: {zip_filename}")
    
    # Fichiers à inclure
    include_patterns = [
        "*.py",
        "*.json", 
        "*.md",
        "*.txt",
        "*.ico",
        "*.png",
        "backend/**/*",
        "config/**/*",
        "assets/**/*",
        "template/**/*"
    ]
    
    # Fichiers à exclure
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
        ".DS_Store",
        "update_storage"
    ]
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for pattern in include_patterns:
            for file_path in source_path.rglob(pattern.replace('**/*', '**')):
                if file_path.is_file():
                    # Vérifier si le fichier doit être exclu
                    should_exclude = False
                    for exclude in exclude_patterns:
                        if exclude.replace('**/*', '') in str(file_path):
                            should_exclude = True
                            break
                    
                    if not should_exclude:
                        relative_path = file_path.relative_to(source_path)
                        zipf.write(file_path, relative_path)
                        print(f"  + {relative_path}")
        
        # Ajouter les métadonnées de version
        version_metadata = {
            "version": version,
            "created_date": datetime.now().isoformat(),
            "package_type": "full_update",
            "requires_restart": True,
            "install_instructions": [
                "Fermer l'application",
                "Extraire le contenu dans le dossier d'installation", 
                "Redémarrer l'application"
            ]
        }
        
        zipf.writestr("update_metadata.json", json.dumps(version_metadata, indent=2))
    
    print(f"✅ Package créé: {zip_path} ({zip_path.stat().st_size} bytes)")
    return str(zip_path)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "create-package":
        # Mode création de package
        version = sys.argv[2] if len(sys.argv) > 2 else "1.0.0"
        source_dir = sys.argv[3] if len(sys.argv) > 3 else "."
        package_path = create_update_package(source_dir, version)
        print(f"Package créé: {package_path}")
    else:
        # Mode serveur
        server = UpdateServer()
        server.run()