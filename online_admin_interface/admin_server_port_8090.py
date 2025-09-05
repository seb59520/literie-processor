#!/usr/bin/env python3
"""
Serveur d'administration MATELAS - Port 8090 (pour éviter le conflit)
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

# Sécurité basique
security = HTTPBasic()

# Configuration
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "matelas2025"
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

@app.get("/")
def root():
    """Page d'accueil publique"""
    return {"message": "MATELAS Update Server", "status": "online", "port": 8090}

@app.get("/api/v1/check-updates")
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
            "download_url": f"http://localhost:8090/api/v1/download/{latest['version']}",
            "description": latest.get("description", ""),
            "changelog": latest.get("changelog", ""),
            "file_size": latest.get("file_size", 0),
            "release_date": latest.get("release_date", ""),
            "current_version": "0.0.0"
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/api/v1/download/{version}")
def download_version(version: str):
    """Télécharger une version"""
    try:
        manifest = load_manifest()
        versions = manifest.get("versions", [])
        
        for v in versions:
            if v["version"] == version:
                file_path = VERSIONS_PATH / v["filename"]
                if file_path.exists():
                    # Incrémenter le compteur
                    v["downloads"] = v.get("downloads", 0) + 1
                    manifest["statistics"]["total_downloads"] = manifest["statistics"].get("total_downloads", 0) + 1
                    save_manifest(manifest)
                    
                    return FileResponse(
                        file_path, 
                        filename=v["filename"],
                        media_type="application/zip"
                    )
        
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
        # Validation
        if not file.filename.endswith('.zip'):
            raise HTTPException(400, "Le fichier doit être un ZIP")
        
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
            file_path.unlink()
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
        raise HTTPException(500, f"Erreur d'upload: {str(e)}")

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
    print("=" * 55)
    print(f"🌐 Interface admin: http://localhost:8090/admin")
    print(f"👤 Identifiants: {ADMIN_USERNAME} / {ADMIN_PASSWORD}")
    print(f"📦 API clients: http://localhost:8090/api/v1/check-updates")
    print()
    print("💡 Ce serveur utilise le port 8090 pour éviter les conflits")
    print("⚠️  Pour la production, utilisez le port 80/443 avec un reverse proxy")
    
    uvicorn.run(app, host="0.0.0.0", port=8090)