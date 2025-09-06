#!/usr/bin/env python3
"""
Interface d'administration web pour le système de mise à jour
Permet de gérer les versions, uploader des mises à jour, voir les statistiques
"""

import os
import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from update_server import UpdateServer, create_update_package
from version_manager import VersionManager

class UpdateAdminInterface:
    """Interface d'administration pour les mises à jour"""
    
    def __init__(self, storage_path: str = "update_storage"):
        self.update_server = UpdateServer(storage_path)
        self.version_manager = VersionManager("../")  # Répertoire parent
        
        # Initialiser FastAPI
        self.app = FastAPI(
            title="MATELAS Update Admin",
            description="Interface d'administration pour les mises à jour automatiques",
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
        
        # Créer le dossier templates s'il n'existe pas
        self.templates_dir = Path(__file__).parent / "templates"
        self.templates_dir.mkdir(exist_ok=True)
        
        # Créer les templates HTML
        self._create_templates()
        
        # Initialiser Jinja2
        self.templates = Jinja2Templates(directory=str(self.templates_dir))
        
        # Routes
        self._setup_routes()
    
    def _create_templates(self):
        """Crée les templates HTML nécessaires"""
        
        # Template principal
        main_template = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MATELAS - Administration des Mises à Jour</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .version-card { border-left: 4px solid #007bff; }
        .version-latest { border-left-color: #28a745; }
        .stats-card { background: linear-gradient(45deg, #007bff, #0056b3); color: white; }
        .upload-zone { border: 2px dashed #ccc; border-radius: 10px; padding: 50px; text-align: center; }
        .upload-zone:hover { border-color: #007bff; }
        .log-entry { margin-bottom: 5px; padding: 5px 10px; border-radius: 3px; }
        .log-info { background-color: #d1ecf1; }
        .log-warning { background-color: #fff3cd; }
        .log-error { background-color: #f8d7da; }
        .btn-action { margin: 2px; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-cogs"></i> MATELAS Admin
            </a>
            <div class="navbar-nav ms-auto">
                <span class="navbar-text">Interface de Gestion des Mises à Jour</span>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Actualisation automatique des statistiques
        setInterval(function() {
            fetch('/api/admin/stats')
                .then(response => response.json())
                .then(data => updateStats(data))
                .catch(console.error);
        }, 30000); // 30 secondes

        function updateStats(stats) {
            document.getElementById('total-versions').textContent = stats.total_versions;
            document.getElementById('total-downloads').textContent = stats.total_downloads;
            document.getElementById('storage-used').textContent = formatBytes(stats.storage_used);
        }

        function formatBytes(bytes) {
            if (bytes === 0) return '0 B';
            const k = 1024;
            const sizes = ['B', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }

        function deleteVersion(version) {
            if (confirm('Êtes-vous sûr de vouloir supprimer la version ' + version + ' ?')) {
                fetch('/api/admin/versions/' + version, { method: 'DELETE' })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            location.reload();
                        } else {
                            alert('Erreur: ' + data.message);
                        }
                    });
            }
        }

        function downloadVersion(version) {
            window.open('/api/v1/download/' + version);
        }
    </script>
</body>
</html>'''

        # Page principale (dashboard)
        dashboard_template = '''{% extends "base.html" %}

{% block content %}
<div class="row">
    <!-- Statistiques -->
    <div class="col-md-3 mb-4">
        <div class="card stats-card">
            <div class="card-body text-center">
                <h5 class="card-title">
                    <i class="fas fa-box"></i> Versions
                </h5>
                <h2 id="total-versions">{{ stats.total_versions }}</h2>
            </div>
        </div>
    </div>
    <div class="col-md-3 mb-4">
        <div class="card stats-card">
            <div class="card-body text-center">
                <h5 class="card-title">
                    <i class="fas fa-download"></i> Téléchargements
                </h5>
                <h2 id="total-downloads">{{ stats.total_downloads }}</h2>
            </div>
        </div>
    </div>
    <div class="col-md-3 mb-4">
        <div class="card stats-card">
            <div class="card-body text-center">
                <h5 class="card-title">
                    <i class="fas fa-hdd"></i> Stockage
                </h5>
                <h2 id="storage-used">{{ "%.1f"|format(stats.storage_used / 1024 / 1024) }} MB</h2>
            </div>
        </div>
    </div>
    <div class="col-md-3 mb-4">
        <div class="card stats-card">
            <div class="card-body text-center">
                <h5 class="card-title">
                    <i class="fas fa-clock"></i> Dernière MAJ
                </h5>
                <p class="mb-0">{{ last_update_date }}</p>
            </div>
        </div>
    </div>
</div>

<!-- Actions rapides -->
<div class="row mb-4">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-plus-circle"></i> Nouvelle Version</h5>
            </div>
            <div class="card-body">
                <form action="/admin/create-version" method="POST" class="row g-3">
                    <div class="col-md-6">
                        <label class="form-label">Type de version</label>
                        <select name="version_type" class="form-select" required>
                            <option value="patch">Patch ({{ current_version }} → {{ next_patch }})</option>
                            <option value="minor">Minor ({{ current_version }} → {{ next_minor }})</option>
                            <option value="major">Major ({{ current_version }} → {{ next_major }})</option>
                        </select>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label">Description</label>
                        <input type="text" name="description" class="form-control" required>
                    </div>
                    <div class="col-12">
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-rocket"></i> Créer et Publier
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
    
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-upload"></i> Upload Manuel</h5>
            </div>
            <div class="card-body">
                <form action="/admin/upload" method="POST" enctype="multipart/form-data">
                    <div class="upload-zone" onclick="document.getElementById('fileInput').click()">
                        <i class="fas fa-cloud-upload-alt fa-3x text-muted"></i>
                        <p class="mt-3 text-muted">Cliquez pour sélectionner un fichier ZIP</p>
                        <input type="file" id="fileInput" name="file" accept=".zip" style="display: none;" required>
                    </div>
                    <div class="row g-3 mt-3">
                        <div class="col-md-4">
                            <input type="text" name="version" class="form-control" placeholder="Version (ex: 3.11.0)" required>
                        </div>
                        <div class="col-md-8">
                            <input type="text" name="description" class="form-control" placeholder="Description de la version" required>
                        </div>
                        <div class="col-12">
                            <textarea name="changelog" class="form-control" rows="3" placeholder="Changelog (optionnel)"></textarea>
                        </div>
                        <div class="col-12">
                            <button type="submit" class="btn btn-success">
                                <i class="fas fa-upload"></i> Uploader la Version
                            </button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>

<!-- Liste des versions -->
<div class="card">
    <div class="card-header d-flex justify-content-between align-items-center">
        <h5><i class="fas fa-list"></i> Versions Disponibles</h5>
        <span class="badge bg-secondary">{{ versions|length }} versions</span>
    </div>
    <div class="card-body">
        {% if versions %}
            <div class="row">
                {% for version in versions %}
                <div class="col-md-6 mb-3">
                    <div class="card version-card {{ 'version-latest' if loop.index == 1 else '' }}">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <h6 class="card-title mb-0">
                                    {{ version.version }}
                                    {% if loop.index == 1 %}
                                        <span class="badge bg-success">Latest</span>
                                    {% endif %}
                                </h6>
                                <small class="text-muted">{{ version.date[:10] }}</small>
                            </div>
                            <p class="card-text text-muted">{{ version.description }}</p>
                            
                            <div class="d-flex justify-content-between align-items-center">
                                <small class="text-muted">
                                    <i class="fas fa-download"></i> {{ version.downloads }} téléchargements
                                    <br>
                                    <i class="fas fa-weight"></i> {{ "%.1f"|format(version.size / 1024 / 1024) }} MB
                                </small>
                                <div>
                                    <button onclick="downloadVersion('{{ version.version }}')" 
                                            class="btn btn-sm btn-outline-primary btn-action">
                                        <i class="fas fa-download"></i>
                                    </button>
                                    <button onclick="deleteVersion('{{ version.version }}')" 
                                            class="btn btn-sm btn-outline-danger btn-action">
                                        <i class="fas fa-trash"></i>
                                    </button>
                                </div>
                            </div>
                            
                            {% if version.changelog %}
                            <div class="mt-2">
                                <small class="text-muted">
                                    <strong>Changelog:</strong><br>
                                    {{ version.changelog.replace('\n', '<br>')|safe }}
                                </small>
                            </div>
                            {% endif %}
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        {% else %}
            <div class="text-center text-muted py-5">
                <i class="fas fa-box-open fa-3x"></i>
                <p class="mt-3">Aucune version disponible</p>
                <p>Créez votre première version ci-dessus</p>
            </div>
        {% endif %}
    </div>
</div>
{% endblock %}'''

        # Sauvegarder les templates
        with open(self.templates_dir / "base.html", 'w', encoding='utf-8') as f:
            f.write(main_template)
        
        with open(self.templates_dir / "dashboard.html", 'w', encoding='utf-8') as f:
            f.write(dashboard_template)
    
    def _setup_routes(self):
        """Configure les routes de l'interface d'administration"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def admin_dashboard(request: Request):
            """Page principale d'administration"""
            try:
                # Statistiques
                stats = self.update_server.manifest["statistics"]
                stats["storage_used"] = self.update_server._get_storage_size()
                
                # Versions
                versions = sorted(
                    self.update_server.manifest["versions"], 
                    key=lambda v: v["version"], 
                    reverse=True
                )
                
                # Version actuelle et prochaines versions
                current_version = self.version_manager.current_version["version"]
                version_parts = list(map(int, current_version.split('.')))
                next_patch = f"{version_parts[0]}.{version_parts[1]}.{version_parts[2] + 1}"
                next_minor = f"{version_parts[0]}.{version_parts[1] + 1}.0"
                next_major = f"{version_parts[0] + 1}.0.0"
                
                # Date de dernière mise à jour
                last_update = self.update_server.manifest.get("last_update", "")
                if last_update:
                    last_update_date = datetime.fromisoformat(last_update.replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M')
                else:
                    last_update_date = "Jamais"
                
                return self.templates.TemplateResponse("dashboard.html", {
                    "request": request,
                    "stats": stats,
                    "versions": versions,
                    "current_version": current_version,
                    "next_patch": next_patch,
                    "next_minor": next_minor,
                    "next_major": next_major,
                    "last_update_date": last_update_date
                })
                
            except Exception as e:
                return HTMLResponse(f"<h1>Erreur</h1><p>{str(e)}</p>", status_code=500)
        
        @self.app.post("/admin/create-version")
        async def create_version(
            version_type: str = Form(...),
            description: str = Form(...)
        ):
            """Crée une nouvelle version automatiquement"""
            try:
                # Créer la nouvelle version
                new_version = self.version_manager.update_version(version_type, description)
                
                # Créer le package
                package_path = create_update_package("../", new_version, str(self.update_server.storage_path / "temp"))
                
                # Ajouter au serveur de mise à jour
                package_file = Path(package_path)
                if package_file.exists():
                    # Déplacer vers le dossier versions
                    dest_file = self.update_server.versions_dir / f"matelas_v{new_version}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
                    package_file.rename(dest_file)
                    
                    # Ajouter au manifest
                    version_info = {
                        "version": new_version,
                        "filename": dest_file.name,
                        "date": datetime.now().isoformat(),
                        "description": description,
                        "changelog": f"Version {new_version}\n- {description}",
                        "size": dest_file.stat().st_size,
                        "hash": self.update_server._calculate_file_hash(dest_file),
                        "downloads": 0
                    }
                    
                    # Supprimer l'ancienne version si elle existe
                    self.update_server.manifest["versions"] = [
                        v for v in self.update_server.manifest["versions"] 
                        if v["version"] != new_version
                    ]
                    
                    self.update_server.manifest["versions"].append(version_info)
                    self.update_server.manifest["last_update"] = datetime.now().isoformat()
                    self.update_server.manifest["statistics"]["active_versions"] = len(self.update_server.manifest["versions"])
                    
                    self.update_server._save_manifest()
                
                return HTMLResponse(f"""
                    <script>
                        alert('Version {new_version} créée avec succès !');
                        window.location.href = '/';
                    </script>
                """)
                
            except Exception as e:
                return HTMLResponse(f"""
                    <script>
                        alert('Erreur: {str(e)}');
                        window.location.href = '/';
                    </script>
                """)
        
        @self.app.post("/admin/upload")
        async def upload_manual(
            file: UploadFile = File(...),
            version: str = Form(...),
            description: str = Form(...),
            changelog: str = Form("")
        ):
            """Upload manuel d'une version"""
            try:
                # Vérifier le type de fichier
                if not file.filename.endswith('.zip'):
                    raise HTTPException(status_code=400, detail="Le fichier doit être un ZIP")
                
                # Générer le nom de fichier
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"matelas_v{version}_{timestamp}.zip"
                file_path = self.update_server.versions_dir / filename
                
                # Sauvegarder le fichier
                with open(file_path, 'wb') as f:
                    content = await file.read()
                    f.write(content)
                
                # Calculer les métadonnées
                file_hash = self.update_server._calculate_file_hash(file_path)
                file_size = file_path.stat().st_size
                
                # Ajouter au manifest
                version_info = {
                    "version": version,
                    "filename": filename,
                    "date": datetime.now().isoformat(),
                    "description": description,
                    "changelog": changelog or f"Version {version}",
                    "size": file_size,
                    "hash": file_hash,
                    "downloads": 0
                }
                
                # Supprimer l'ancienne version si elle existe
                self.update_server.manifest["versions"] = [
                    v for v in self.update_server.manifest["versions"] 
                    if v["version"] != version
                ]
                
                self.update_server.manifest["versions"].append(version_info)
                self.update_server.manifest["last_update"] = datetime.now().isoformat()
                self.update_server.manifest["statistics"]["active_versions"] = len(self.update_server.manifest["versions"])
                
                self.update_server._save_manifest()
                
                return HTMLResponse(f"""
                    <script>
                        alert('Version {version} uploadée avec succès !');
                        window.location.href = '/';
                    </script>
                """)
                
            except Exception as e:
                return HTMLResponse(f"""
                    <script>
                        alert('Erreur: {str(e)}');
                        window.location.href = '/';
                    </script>
                """)
        
        @self.app.get("/api/admin/stats")
        async def get_stats():
            """API pour récupérer les statistiques"""
            stats = self.update_server.manifest["statistics"].copy()
            stats["storage_used"] = self.update_server._get_storage_size()
            stats["total_versions"] = len(self.update_server.manifest["versions"])
            return stats
        
        @self.app.delete("/api/admin/versions/{version}")
        async def delete_version(version: str):
            """Supprime une version"""
            try:
                # Trouver et supprimer la version
                version_info = None
                for i, v in enumerate(self.update_server.manifest["versions"]):
                    if v["version"] == version:
                        version_info = self.update_server.manifest["versions"].pop(i)
                        break
                
                if not version_info:
                    return {"success": False, "message": "Version non trouvée"}
                
                # Supprimer le fichier
                file_path = self.update_server.versions_dir / version_info["filename"]
                if file_path.exists():
                    file_path.unlink()
                
                # Mettre à jour le manifest
                self.update_server.manifest["statistics"]["active_versions"] = len(self.update_server.manifest["versions"])
                self.update_server._save_manifest()
                
                return {"success": True, "message": f"Version {version} supprimée avec succès"}
                
            except Exception as e:
                return {"success": False, "message": str(e)}
        
        # Intégrer les routes du serveur de mise à jour
        @self.app.get("/api/v1/check-updates")
        async def check_updates(current_version: str = "1.0.0"):
            # Utiliser la méthode du serveur de mise à jour
            return await self._proxy_to_update_server(f"/api/v1/check-updates?current_version={current_version}")
        
        @self.app.get("/api/v1/versions")
        async def list_versions():
            return await self._proxy_to_update_server("/api/v1/versions")
        
        @self.app.get("/api/v1/download/{version}")
        async def download_version(version: str):
            # Chercher la version dans le manifest
            version_info = None
            for v in self.update_server.manifest["versions"]:
                if v["version"] == version:
                    version_info = v
                    break
            
            if not version_info:
                raise HTTPException(status_code=404, detail="Version non trouvée")
            
            file_path = self.update_server.versions_dir / version_info["filename"]
            
            if not file_path.exists():
                raise HTTPException(status_code=404, detail="Fichier de version non trouvé")
            
            # Incrémenter le compteur de téléchargements
            self.update_server.manifest["statistics"]["total_downloads"] += 1
            version_info["downloads"] = version_info.get("downloads", 0) + 1
            self.update_server._save_manifest()
            
            return FileResponse(
                path=file_path,
                filename=version_info["filename"],
                media_type='application/zip'
            )
    
    async def _proxy_to_update_server(self, path: str):
        """Proxy vers le serveur de mise à jour"""
        # Ici on utilise directement les méthodes du serveur
        # au lieu de faire un appel HTTP
        if "check-updates" in path:
            current_version = path.split("=")[1] if "=" in path else "1.0.0"
            available_versions = self.update_server.manifest["versions"]
            
            if not available_versions:
                return {
                    "update_available": False,
                    "current_version": current_version,
                    "message": "Aucune mise à jour disponible"
                }
            
            # Trouver la version la plus récente
            latest_version = max(available_versions, key=lambda v: v["version"])
            
            update_available = self.update_server._is_newer_version(
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
        
        elif "versions" in path:
            return {
                "versions": sorted(self.update_server.manifest["versions"], 
                                 key=lambda v: v["version"], 
                                 reverse=True),
                "total": len(self.update_server.manifest["versions"])
            }
    
    def run(self, host: str = "0.0.0.0", port: int = 8081):
        """Lance l'interface d'administration"""
        print(f"🚀 Interface d'administration démarrée sur http://{host}:{port}")
        print(f"📁 Stockage: {self.update_server.storage_path}")
        print(f"📦 Versions disponibles: {len(self.update_server.manifest['versions'])}")
        print(f"🌐 Accédez à l'interface: http://{host}:{port}")
        
        uvicorn.run(self.app, host=host, port=port)

def main():
    """Lance l'interface d'administration"""
    import sys
    
    storage_path = sys.argv[1] if len(sys.argv) > 1 else "update_storage"
    admin = UpdateAdminInterface(storage_path)
    admin.run()

if __name__ == "__main__":
    main()