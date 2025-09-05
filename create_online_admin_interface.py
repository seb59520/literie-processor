#!/usr/bin/env python3
"""
Créateur d'interface d'administration web complète pour serveur en ligne
Interface moderne sans besoin de toucher au code
"""

import os
from pathlib import Path

def create_online_admin_interface():
    """Crée l'interface d'administration web complète"""
    
    print("🌐 CRÉATION INTERFACE ADMIN WEB POUR SERVEUR EN LIGNE")
    print("=" * 65)
    
    # Créer la structure
    admin_dir = Path("online_admin_interface")
    admin_dir.mkdir(exist_ok=True)
    
    templates_dir = admin_dir / "templates"
    static_dir = admin_dir / "static"
    
    templates_dir.mkdir(exist_ok=True)
    static_dir.mkdir(exist_ok=True)
    (static_dir / "css").mkdir(exist_ok=True)
    (static_dir / "js").mkdir(exist_ok=True)
    
    # 1. Serveur FastAPI principal
    main_server = '''#!/usr/bin/env python3
"""
Serveur d'administration MATELAS - Version production en ligne
Interface complète sans besoin de toucher le code
"""

import os
import json
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import secrets
import hashlib

from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Request, Depends, status
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uvicorn

app = FastAPI(
    title="MATELAS Update Server",
    description="Serveur de mise à jour avec interface d'administration",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration des templates et fichiers statiques
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Sécurité basique (à améliorer en production)
security = HTTPBasic()

# Configuration
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "matelas2025"  # À changer en production !
STORAGE_PATH = Path("update_storage")
VERSIONS_PATH = STORAGE_PATH / "versions"
METADATA_PATH = STORAGE_PATH / "metadata"

# Initialiser les dossiers
STORAGE_PATH.mkdir(exist_ok=True)
VERSIONS_PATH.mkdir(exist_ok=True)
METADATA_PATH.mkdir(exist_ok=True)

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    """Vérification des credentials admin"""
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants incorrects",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

def load_manifest():
    """Charger le manifest des versions"""
    manifest_file = METADATA_PATH / "manifest.json"
    if manifest_file.exists():
        with open(manifest_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"versions": [], "statistics": {"total_downloads": 0}}

def save_manifest(manifest):
    """Sauvegarder le manifest"""
    manifest_file = METADATA_PATH / "manifest.json"
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

# ============= ROUTES PUBLIQUES (API CLIENTS) =============

@app.route("/")
def root():
    """Page d'accueil publique"""
    return {"message": "MATELAS Update Server", "status": "online"}

@app.route("/api/v1/check-updates")
def check_updates():
    """API pour vérifier les mises à jour (utilisée par les clients)"""
    try:
        manifest = load_manifest()
        versions = manifest.get("versions", [])
        
        if not versions:
            return JSONResponse({"available": False, "message": "Aucune version disponible"})
        
        # Version la plus récente
        latest = max(versions, key=lambda x: tuple(map(int, x["version"].split('.'))))
        
        return JSONResponse({
            "available": True,
            "latest_version": latest["version"],
            "download_url": f"/api/v1/download/{latest['version']}",
            "description": latest.get("description", ""),
            "changelog": latest.get("changelog", ""),
            "file_size": latest.get("file_size", 0),
            "release_date": latest.get("release_date", ""),
            "current_version": "0.0.0"  # Le client doit fournir sa version
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.route("/api/v1/download/<version>")
def download_version(version: str):
    """Télécharger une version"""
    try:
        manifest = load_manifest()
        versions = manifest.get("versions", [])
        
        for v in versions:
            if v["version"] == version:
                file_path = VERSIONS_PATH / v["filename"]
                if file_path.exists():
                    # Incrémenter le compteur de téléchargements
                    v["downloads"] = v.get("downloads", 0) + 1
                    manifest["statistics"]["total_downloads"] = manifest["statistics"].get("total_downloads", 0) + 1
                    save_manifest(manifest)
                    
                    return FileResponse(
                        file_path, 
                        filename=v["filename"],
                        media_type="application/zip"
                    )
                else:
                    raise HTTPException(404, "Fichier non trouvé")
        
        raise HTTPException(404, "Version non trouvée")
    except Exception as e:
        raise HTTPException(500, str(e))

# ============= INTERFACE D'ADMINISTRATION =============

@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request, username: str = Depends(verify_credentials)):
    """Tableau de bord d'administration"""
    manifest = load_manifest()
    versions = manifest.get("versions", [])
    stats = manifest.get("statistics", {})
    
    # Statistiques
    total_versions = len(versions)
    total_downloads = stats.get("total_downloads", 0)
    latest_version = max(versions, key=lambda x: tuple(map(int, x["version"].split('.'))))["version"] if versions else "Aucune"
    
    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request,
        "total_versions": total_versions,
        "total_downloads": total_downloads,
        "latest_version": latest_version,
        "versions": sorted(versions, key=lambda x: tuple(map(int, x["version"].split('.'))), reverse=True)
    })

@app.get("/admin/upload", response_class=HTMLResponse)  
def admin_upload_page(request: Request, username: str = Depends(verify_credentials)):
    """Page d'upload"""
    return templates.TemplateResponse("admin_upload.html", {"request": request})

@app.post("/admin/upload")
async def admin_upload_version(
    request: Request,
    file: UploadFile = File(...),
    version: str = Form(...),
    description: str = Form(""),
    changelog: str = Form(""),
    username: str = Depends(verify_credentials)
):
    """Upload d'une nouvelle version"""
    try:
        # Validation du fichier
        if not file.filename.endswith('.zip'):
            raise HTTPException(400, "Le fichier doit être un ZIP")
        
        # Validation de la version
        try:
            version_parts = list(map(int, version.split('.')))
            if len(version_parts) != 3:
                raise ValueError()
        except ValueError:
            raise HTTPException(400, "Format de version invalide (ex: 3.10.4)")
        
        # Nom du fichier
        filename = f"matelas_v{version}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        file_path = VERSIONS_PATH / filename
        
        # Sauvegarder le fichier
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Mettre à jour le manifest
        manifest = load_manifest()
        
        # Vérifier que la version n'existe pas déjà
        existing_versions = [v["version"] for v in manifest["versions"]]
        if version in existing_versions:
            file_path.unlink()  # Supprimer le fichier uploadé
            raise HTTPException(400, f"La version {version} existe déjà")
        
        # Ajouter la nouvelle version
        new_version = {
            "version": version,
            "filename": filename,
            "description": description,
            "changelog": changelog,
            "file_size": len(content),
            "release_date": datetime.now().isoformat(),
            "downloads": 0
        }
        
        manifest["versions"].append(new_version)
        save_manifest(manifest)
        
        return RedirectResponse("/admin?success=Version uploadée avec succès", status_code=303)
        
    except HTTPException:
        raise
    except Exception as e:
        return HTTPException(500, f"Erreur d'upload: {str(e)}")

@app.post("/admin/delete/{version}")
def admin_delete_version(version: str, username: str = Depends(verify_credentials)):
    """Supprimer une version"""
    try:
        manifest = load_manifest()
        versions = manifest["versions"]
        
        # Trouver et supprimer la version
        version_to_delete = None
        for i, v in enumerate(versions):
            if v["version"] == version:
                version_to_delete = versions.pop(i)
                break
        
        if not version_to_delete:
            raise HTTPException(404, "Version non trouvée")
        
        # Supprimer le fichier
        file_path = VERSIONS_PATH / version_to_delete["filename"]
        if file_path.exists():
            file_path.unlink()
        
        save_manifest(manifest)
        
        return {"success": True, "message": f"Version {version} supprimée"}
        
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/admin/stats", response_class=HTMLResponse)
def admin_stats(request: Request, username: str = Depends(verify_credentials)):
    """Page des statistiques"""
    manifest = load_manifest()
    return templates.TemplateResponse("admin_stats.html", {
        "request": request,
        "manifest": manifest
    })

if __name__ == "__main__":
    print("🚀 Démarrage du serveur d'administration MATELAS")
    print("=" * 50)
    print(f"🌐 Interface admin: http://localhost:8080/admin")
    print(f"👤 Identifiants: {ADMIN_USERNAME} / {ADMIN_PASSWORD}")
    print(f"📦 API clients: http://localhost:8080/api/v1/check-updates")
    
    uvicorn.run(app, host="0.0.0.0", port=8080)
'''
    
    (admin_dir / "main.py").write_text(main_server, encoding='utf-8')
    
    # 2. Template du dashboard principal
    dashboard_template = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MATELAS Update Center</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .hero-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem 0;
        }
        .stats-card {
            border: none;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }
        .stats-card:hover {
            transform: translateY(-5px);
        }
        .version-badge {
            font-size: 0.8rem;
        }
    </style>
</head>
<body class="bg-light">
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/admin">
                <i class="fas fa-download me-2"></i>
                MATELAS Update Center
            </a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/admin/upload">
                    <i class="fas fa-upload me-1"></i>Upload
                </a>
                <a class="nav-link" href="/admin/stats">
                    <i class="fas fa-chart-bar me-1"></i>Stats
                </a>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero-section">
        <div class="container text-center">
            <h1 class="display-4 mb-3">
                <i class="fas fa-server me-3"></i>
                Centre d'Administration
            </h1>
            <p class="lead">Gérez vos mises à jour MATELAS sans toucher au code</p>
        </div>
    </section>

    <!-- Dashboard -->
    <div class="container my-5">
        <!-- Statistiques -->
        <div class="row mb-5">
            <div class="col-md-4">
                <div class="card stats-card h-100 text-center">
                    <div class="card-body">
                        <i class="fas fa-box fa-3x text-primary mb-3"></i>
                        <h3 class="card-title">{{ total_versions }}</h3>
                        <p class="card-text text-muted">Versions Disponibles</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card stats-card h-100 text-center">
                    <div class="card-body">
                        <i class="fas fa-download fa-3x text-success mb-3"></i>
                        <h3 class="card-title">{{ total_downloads }}</h3>
                        <p class="card-text text-muted">Téléchargements Totaux</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card stats-card h-100 text-center">
                    <div class="card-body">
                        <i class="fas fa-tag fa-3x text-warning mb-3"></i>
                        <h3 class="card-title">{{ latest_version }}</h3>
                        <p class="card-text text-muted">Version Actuelle</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Actions Rapides -->
        <div class="row mb-5">
            <div class="col-12">
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">
                            <i class="fas fa-bolt me-2"></i>
                            Actions Rapides
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <a href="/admin/upload" class="btn btn-success btn-lg w-100">
                                    <i class="fas fa-upload me-2"></i>
                                    Uploader Nouvelle Version
                                </a>
                            </div>
                            <div class="col-md-6 mb-3">
                                <a href="/admin/stats" class="btn btn-info btn-lg w-100">
                                    <i class="fas fa-chart-line me-2"></i>
                                    Voir Statistiques Détaillées
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Liste des Versions -->
        <div class="card">
            <div class="card-header bg-dark text-white">
                <h5 class="mb-0">
                    <i class="fas fa-list me-2"></i>
                    Versions Disponibles
                </h5>
            </div>
            <div class="card-body">
                {% if versions %}
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead class="table-light">
                            <tr>
                                <th>Version</th>
                                <th>Description</th>
                                <th>Date de sortie</th>
                                <th>Téléchargements</th>
                                <th>Taille</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for version in versions %}
                            <tr>
                                <td>
                                    <span class="badge bg-primary version-badge">
                                        v{{ version.version }}
                                    </span>
                                </td>
                                <td>{{ version.description[:50] }}...</td>
                                <td>{{ version.release_date[:10] }}</td>
                                <td>
                                    <span class="badge bg-success">
                                        {{ version.downloads or 0 }}
                                    </span>
                                </td>
                                <td>{{ "%.1f MB"|format(version.file_size / 1024 / 1024) }}</td>
                                <td>
                                    <button class="btn btn-sm btn-outline-danger" 
                                            onclick="deleteVersion('{{ version.version }}')">
                                        <i class="fas fa-trash"></i>
                                    </button>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                {% else %}
                <div class="text-center py-5">
                    <i class="fas fa-inbox fa-5x text-muted mb-3"></i>
                    <h5 class="text-muted">Aucune version disponible</h5>
                    <p class="text-muted">Uploadez votre première version pour commencer</p>
                    <a href="/admin/upload" class="btn btn-primary">
                        <i class="fas fa-upload me-2"></i>
                        Uploader maintenant
                    </a>
                </div>
                {% endif %}
            </div>
        </div>
    </div>

    <!-- Scripts -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function deleteVersion(version) {
            if (confirm(`Êtes-vous sûr de vouloir supprimer la version ${version} ?`)) {
                fetch(`/admin/delete/${version}`, {
                    method: 'POST',
                    credentials: 'same-origin'
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload();
                    } else {
                        alert('Erreur: ' + data.message);
                    }
                })
                .catch(error => {
                    alert('Erreur: ' + error);
                });
            }
        }
        
        // Afficher message de succès depuis URL
        const urlParams = new URLSearchParams(window.location.search);
        const success = urlParams.get('success');
        if (success) {
            const alert = document.createElement('div');
            alert.className = 'alert alert-success alert-dismissible fade show position-fixed';
            alert.style.top = '20px';
            alert.style.right = '20px';
            alert.style.zIndex = '9999';
            alert.innerHTML = `
                ${success}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            document.body.appendChild(alert);
            
            // Nettoyer l'URL
            window.history.replaceState({}, document.title, '/admin');
        }
    </script>
</body>
</html>'''
    
    (templates_dir / "admin_dashboard.html").write_text(dashboard_template, encoding='utf-8')
    
    # 3. Template d'upload
    upload_template = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload Version - MATELAS Update Center</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .upload-area {
            border: 2px dashed #dee2e6;
            border-radius: 10px;
            padding: 3rem;
            text-align: center;
            transition: all 0.3s ease;
            background: #f8f9fa;
        }
        .upload-area:hover, .upload-area.dragover {
            border-color: #0d6efd;
            background: #e7f3ff;
        }
        .upload-icon {
            font-size: 4rem;
            color: #6c757d;
            margin-bottom: 1rem;
        }
    </style>
</head>
<body class="bg-light">
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/admin">
                <i class="fas fa-download me-2"></i>
                MATELAS Update Center
            </a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/admin">
                    <i class="fas fa-home me-1"></i>Dashboard
                </a>
                <a class="nav-link active" href="/admin/upload">
                    <i class="fas fa-upload me-1"></i>Upload
                </a>
            </div>
        </div>
    </nav>

    <!-- Page Header -->
    <div class="container my-5">
        <div class="row">
            <div class="col-12">
                <h2 class="mb-4">
                    <i class="fas fa-upload text-primary me-3"></i>
                    Uploader Nouvelle Version
                </h2>
                <p class="text-muted">
                    Glissez-déposez votre fichier ZIP ou utilisez le formulaire ci-dessous
                </p>
            </div>
        </div>

        <!-- Formulaire d'Upload -->
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <div class="card shadow">
                    <div class="card-body">
                        <form id="uploadForm" action="/admin/upload" method="post" enctype="multipart/form-data">
                            <!-- Zone de Drop -->
                            <div class="upload-area mb-4" id="uploadArea">
                                <i class="fas fa-cloud-upload-alt upload-icon"></i>
                                <h5>Glissez votre fichier ZIP ici</h5>
                                <p class="text-muted mb-3">ou cliquez pour sélectionner</p>
                                <input type="file" class="form-control d-none" name="file" id="fileInput" accept=".zip" required>
                                <button type="button" class="btn btn-outline-primary" onclick="document.getElementById('fileInput').click()">
                                    <i class="fas fa-folder-open me-2"></i>
                                    Choisir un fichier
                                </button>
                            </div>

                            <!-- Informations sur le fichier -->
                            <div id="fileInfo" class="d-none mb-4">
                                <div class="alert alert-success">
                                    <i class="fas fa-file-archive me-2"></i>
                                    <span id="fileName"></span> - <span id="fileSize"></span>
                                </div>
                            </div>

                            <!-- Métadonnées -->
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="version" class="form-label">
                                            <i class="fas fa-tag me-2"></i>Version *
                                        </label>
                                        <input type="text" class="form-control" name="version" id="version" 
                                               placeholder="ex: 3.10.4" pattern="\\d+\\.\\d+\\.\\d+" required>
                                        <div class="form-text">Format: MAJOR.MINOR.PATCH (ex: 3.10.4)</div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="description" class="form-label">
                                            <i class="fas fa-info-circle me-2"></i>Description
                                        </label>
                                        <input type="text" class="form-control" name="description" id="description" 
                                               placeholder="ex: Correction bugs interface">
                                    </div>
                                </div>
                            </div>

                            <div class="mb-4">
                                <label for="changelog" class="form-label">
                                    <i class="fas fa-list me-2"></i>Changelog
                                </label>
                                <textarea class="form-control" name="changelog" id="changelog" rows="4" 
                                          placeholder="Décrivez les changements apportés dans cette version..."></textarea>
                            </div>

                            <!-- Boutons d'action -->
                            <div class="d-flex justify-content-between">
                                <a href="/admin" class="btn btn-secondary">
                                    <i class="fas fa-arrow-left me-2"></i>Retour
                                </a>
                                <button type="submit" class="btn btn-primary" id="submitBtn">
                                    <i class="fas fa-upload me-2"></i>Uploader Version
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>

        <!-- Progress -->
        <div class="row justify-content-center mt-4">
            <div class="col-lg-8">
                <div class="progress d-none" id="progressBar">
                    <div class="progress-bar" role="progressbar" style="width: 0%"></div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const fileInfo = document.getElementById('fileInfo');
        const fileName = document.getElementById('fileName');
        const fileSize = document.getElementById('fileSize');
        const form = document.getElementById('uploadForm');
        const submitBtn = document.getElementById('submitBtn');
        const progressBar = document.getElementById('progressBar');

        // Drag & Drop
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => uploadArea.classList.add('dragover'), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => uploadArea.classList.remove('dragover'), false);
        });

        uploadArea.addEventListener('drop', handleDrop, false);

        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files.length > 0 && files[0].name.endsWith('.zip')) {
                fileInput.files = files;
                showFileInfo(files[0]);
            }
        }

        fileInput.addEventListener('change', function(e) {
            if (e.target.files.length > 0) {
                showFileInfo(e.target.files[0]);
            }
        });

        function showFileInfo(file) {
            fileName.textContent = file.name;
            fileSize.textContent = formatFileSize(file.size);
            fileInfo.classList.remove('d-none');
            
            // Auto-détecter la version depuis le nom du fichier
            const versionMatch = file.name.match(/v?(\\d+\\.\\d+\\.\\d+)/);
            if (versionMatch) {
                document.getElementById('version').value = versionMatch[1];
            }
        }

        function formatFileSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }

        // Gérer la soumission du formulaire
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            if (!fileInput.files.length) {
                alert('Veuillez sélectionner un fichier ZIP');
                return;
            }

            if (!fileInput.files[0].name.endsWith('.zip')) {
                alert('Le fichier doit être un ZIP');
                return;
            }

            const formData = new FormData(form);
            
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Upload en cours...';
            progressBar.classList.remove('d-none');
            
            fetch('/admin/upload', {
                method: 'POST',
                body: formData,
                credentials: 'same-origin'
            })
            .then(response => {
                if (response.redirected) {
                    window.location.href = response.url;
                } else {
                    return response.json();
                }
            })
            .catch(error => {
                alert('Erreur: ' + error);
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="fas fa-upload me-2"></i>Uploader Version';
                progressBar.classList.add('d-none');
            });
        });
    </script>
</body>
</html>'''
    
    (templates_dir / "admin_upload.html").write_text(upload_template, encoding='utf-8')
    
    # 4. Template des statistiques
    stats_template = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Statistiques - MATELAS Update Center</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-light">
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/admin">
                <i class="fas fa-download me-2"></i>
                MATELAS Update Center
            </a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/admin">
                    <i class="fas fa-home me-1"></i>Dashboard
                </a>
                <a class="nav-link active" href="/admin/stats">
                    <i class="fas fa-chart-bar me-1"></i>Stats
                </a>
            </div>
        </div>
    </nav>

    <!-- Page Content -->
    <div class="container my-5">
        <h2 class="mb-4">
            <i class="fas fa-chart-line text-primary me-3"></i>
            Statistiques Détaillées
        </h2>

        <!-- Métriques -->
        <div class="row mb-5">
            <div class="col-md-3">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-download fa-2x text-success mb-2"></i>
                        <h4>{{ manifest.statistics.total_downloads or 0 }}</h4>
                        <small class="text-muted">Total Téléchargements</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-box fa-2x text-primary mb-2"></i>
                        <h4>{{ manifest.versions|length }}</h4>
                        <small class="text-muted">Versions Disponibles</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-hdd fa-2x text-warning mb-2"></i>
                        <h4>{{ "%.1f GB"|format((manifest.versions|sum(attribute='file_size') or 0) / 1024 / 1024 / 1024) }}</h4>
                        <small class="text-muted">Stockage Utilisé</small>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-calendar fa-2x text-info mb-2"></i>
                        <h4>{{ manifest.versions|length and manifest.versions[0].release_date[:10] or 'N/A' }}</h4>
                        <small class="text-muted">Dernière Version</small>
                    </div>
                </div>
            </div>
        </div>

        <!-- Graphiques -->
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-chart-pie me-2"></i>Téléchargements par Version</h5>
                    </div>
                    <div class="card-body">
                        <canvas id="downloadsChart"></canvas>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-chart-bar me-2"></i>Taille des Versions</h5>
                    </div>
                    <div class="card-body">
                        <canvas id="sizeChart"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tableau détaillé -->
        <div class="card mt-4">
            <div class="card-header">
                <h5><i class="fas fa-table me-2"></i>Détails par Version</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Version</th>
                                <th>Description</th>
                                <th>Date</th>
                                <th>Téléchargements</th>
                                <th>Taille</th>
                                <th>Popularité</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for version in manifest.versions %}
                            <tr>
                                <td><span class="badge bg-primary">v{{ version.version }}</span></td>
                                <td>{{ version.description[:40] }}...</td>
                                <td>{{ version.release_date[:10] }}</td>
                                <td>{{ version.downloads or 0 }}</td>
                                <td>{{ "%.1f MB"|format(version.file_size / 1024 / 1024) }}</td>
                                <td>
                                    <div class="progress" style="height: 20px;">
                                        <div class="progress-bar" style="width: {{ (version.downloads or 0) * 100 / ([manifest.statistics.total_downloads, 1]|max) }}%">
                                            {{ "%.1f"|format((version.downloads or 0) * 100 / ([manifest.statistics.total_downloads, 1]|max)) }}%
                                        </div>
                                    </div>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Données pour les graphiques
        const versions = {{ manifest.versions|tojson }};
        const versionLabels = versions.map(v => `v${v.version}`);
        const downloadData = versions.map(v => v.downloads || 0);
        const sizeData = versions.map(v => (v.file_size || 0) / 1024 / 1024); // MB

        // Graphique des téléchargements
        const downloadsCtx = document.getElementById('downloadsChart').getContext('2d');
        new Chart(downloadsCtx, {
            type: 'pie',
            data: {
                labels: versionLabels,
                datasets: [{
                    data: downloadData,
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
                        '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });

        // Graphique des tailles
        const sizeCtx = document.getElementById('sizeChart').getContext('2d');
        new Chart(sizeCtx, {
            type: 'bar',
            data: {
                labels: versionLabels,
                datasets: [{
                    label: 'Taille (MB)',
                    data: sizeData,
                    backgroundColor: '#36A2EB'
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Taille (MB)'
                        }
                    }
                }
            }
        });
    </script>
</body>
</html>'''
    
    (templates_dir / "admin_stats.html").write_text(stats_template, encoding='utf-8')
    
    # 5. Créer les scripts de déploiement
    deployment_guide = '''# 🚀 GUIDE DE DÉPLOIEMENT SERVEUR EN LIGNE

## 📋 ÉTAPES DE DÉPLOIEMENT

### 1. Préparation du serveur
```bash
# Sur votre serveur Linux (Ubuntu/Debian)
sudo apt update
sudo apt install python3 python3-pip nginx certbot

# Installer les dépendances Python
pip3 install fastapi uvicorn jinja2 python-multipart
```

### 2. Configuration du serveur
```bash
# Copier les fichiers sur le serveur
scp -r online_admin_interface/* user@your-server.com:/var/www/matelas-updates/

# Créer le service systemd
sudo nano /etc/systemd/system/matelas-updates.service
```

Contenu du service:
```ini
[Unit]
Description=MATELAS Update Server
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/matelas-updates
Environment=PATH=/usr/local/bin:/usr/bin:/bin
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### 3. Configuration Nginx
```nginx
server {
    listen 80;
    server_name updates.votre-domaine.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Augmenter la taille max pour les uploads
    client_max_body_size 500M;
}
```

### 4. SSL avec Let's Encrypt
```bash
sudo certbot --nginx -d updates.votre-domaine.com
```

### 5. Démarrage des services
```bash
sudo systemctl enable matelas-updates
sudo systemctl start matelas-updates
sudo systemctl enable nginx
sudo systemctl restart nginx
```

## 🌐 URLS D'ACCÈS

- **Interface Admin**: https://updates.votre-domaine.com/admin
- **API Clients**: https://updates.votre-domaine.com/api/v1/check-updates
- **Identifiants par défaut**: admin / matelas2025

## 🔧 CONFIGURATION PRODUCTION

### Sécurité
1. Changez le mot de passe admin dans main.py (ligne 42)
2. Configurez un reverse proxy Nginx
3. Activez HTTPS avec certbot
4. Limitez les IPs d'administration (optionnel)

### Performance
1. Configurez les logs rotatifs
2. Monitorer l'espace disque (dossier versions/)
3. Backup automatique quotidien
4. Configuration firewall (ports 80, 443, 22)

### Backup
```bash
# Script de backup quotidien
#!/bin/bash
tar -czf backup-$(date +%Y%m%d).tar.gz /var/www/matelas-updates/update_storage/
```

## 📱 UTILISATION DEPUIS VOTRE POSTE

1. **Via navigateur**: https://updates.votre-domaine.com/admin
2. **Upload direct**: Glisser-déposer vos fichiers ZIP
3. **Gestion visuelle**: Aucune ligne de code à toucher
4. **Statistiques temps réel**: Voir les téléchargements
'''
    
    (admin_dir / "DEPLOYMENT_GUIDE.md").write_text(deployment_guide, encoding='utf-8')
    
    # 6. Script de déploiement automatique
    deploy_script = '''#!/bin/bash
# Script de déploiement automatique pour serveur

set -e

echo "🚀 DÉPLOIEMENT SERVEUR MATELAS UPDATE"
echo "===================================="

# Variables
SERVER_USER=${1:-"root"}
SERVER_HOST=${2:-"your-server.com"}
SERVER_PATH="/var/www/matelas-updates"

if [ "$SERVER_HOST" = "your-server.com" ]; then
    echo "❌ Usage: ./deploy.sh <user> <server-host>"
    echo "   Exemple: ./deploy.sh ubuntu updates.mondomaine.com"
    exit 1
fi

echo "📤 Envoi des fichiers vers $SERVER_USER@$SERVER_HOST..."

# Créer le répertoire sur le serveur
ssh $SERVER_USER@$SERVER_HOST "mkdir -p $SERVER_PATH"

# Copier les fichiers
rsync -avz --delete \\
    --exclude=".git" \\
    --exclude="*.pyc" \\
    --exclude="__pycache__" \\
    ./ $SERVER_USER@$SERVER_HOST:$SERVER_PATH/

echo "⚙️ Installation des dépendances sur le serveur..."

ssh $SERVER_USER@$SERVER_HOST << 'EOF'
cd /var/www/matelas-updates
pip3 install fastapi uvicorn jinja2 python-multipart
mkdir -p update_storage/{versions,metadata}
chmod 755 main.py
EOF

echo "🔧 Configuration du service systemd..."

ssh $SERVER_USER@$SERVER_HOST << 'EOF'
cat > /etc/systemd/system/matelas-updates.service << 'UNIT'
[Unit]
Description=MATELAS Update Server
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/matelas-updates
Environment=PATH=/usr/local/bin:/usr/bin:/bin
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
UNIT

systemctl daemon-reload
systemctl enable matelas-updates
systemctl restart matelas-updates
EOF

echo "✅ DÉPLOIEMENT TERMINÉ!"
echo ""
echo "🌐 Votre serveur est accessible à:"
echo "   http://$SERVER_HOST:8080/admin"
echo ""
echo "🔐 Identifiants par défaut:"
echo "   Utilisateur: admin"
echo "   Mot de passe: matelas2025"
echo ""
echo "⚠️  N'oubliez pas de:"
echo "   1. Configurer Nginx en reverse proxy"
echo "   2. Installer SSL avec certbot"
echo "   3. Changer le mot de passe admin"
'''
    
    (admin_dir / "deploy.sh").write_text(deploy_script, encoding='utf-8')
    
    # Rendre le script exécutable
    try:
        (admin_dir / "deploy.sh").chmod(0o755)
    except:
        pass
    
    # 7. Fichier requirements.txt
    requirements = '''fastapi==0.104.1
uvicorn==0.24.0
jinja2==3.1.2
python-multipart==0.0.6
'''
    
    (admin_dir / "requirements.txt").write_text(requirements, encoding='utf-8')
    
    # 8. Configuration exemple
    config_example = '''{
    "server": {
        "host": "0.0.0.0",
        "port": 8080,
        "domain": "updates.votre-domaine.com"
    },
    "security": {
        "admin_username": "admin",
        "admin_password": "matelas2025",
        "api_key": "your-secret-api-key"
    },
    "storage": {
        "max_file_size": "500MB",
        "backup_enabled": true,
        "cleanup_old_versions": false
    },
    "notifications": {
        "email_enabled": false,
        "email_smtp": "smtp.gmail.com",
        "email_from": "updates@votre-domaine.com"
    }
}'''
    
    (admin_dir / "config.json.example").write_text(config_example, encoding='utf-8')
    
    print(f"✅ Interface d'administration créée dans: {admin_dir}")
    print(f"📁 Structure complète générée")
    print(f"🌐 Prête pour déploiement en ligne")
    
    return admin_dir

if __name__ == "__main__":
    admin_path = create_online_admin_interface()
    
    print(f"\n🎉 INTERFACE D'ADMINISTRATION CRÉÉE!")
    print(f"📁 Dossier: {admin_path}")
    print(f"\n🚀 DÉMARRAGE LOCAL POUR TEST:")
    print(f"cd {admin_path}")
    print(f"python3 main.py")
    print(f"\n🌐 Puis ouvrez: http://localhost:8080/admin")
    print(f"🔐 Identifiants: admin / matelas2025")