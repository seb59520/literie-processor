#!/usr/bin/env python3
"""
Serveur d'administration MATELAS avec télémétrie des postes clients
Collecte automatiquement les informations des postes qui se connectent
"""

import os
import json
import shutil
import zipfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import secrets
import platform
import uuid

from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Request, Depends, status
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uvicorn

app = FastAPI(
    title="MATELAS Update Server with Telemetry",
    description="Serveur de mise à jour avec télémétrie des postes clients",
    version="2.0.0"
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

# Configuration de l'URL du serveur (pour les téléchargements)
# Auto-détection de l'URL ngrok ou utilisation de localhost par défaut
SERVER_BASE_URL = "https://edceecf7fdaf.ngrok-free.app"  # URL ngrok pour accès Internet
STORAGE_PATH = Path("update_storage")
VERSIONS_PATH = STORAGE_PATH / "updates"
METADATA_PATH = STORAGE_PATH / "metadata"
TELEMETRY_PATH = STORAGE_PATH / "telemetry"

# Initialiser les dossiers
STORAGE_PATH.mkdir(exist_ok=True)
VERSIONS_PATH.mkdir(exist_ok=True)
METADATA_PATH.mkdir(exist_ok=True)
TELEMETRY_PATH.mkdir(exist_ok=True)

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

def save_client_info(client_info):
    """Sauvegarder les informations d'un client"""
    client_id = client_info.get("client_id", "unknown")
    client_file = TELEMETRY_PATH / f"client_{client_id}.json"
    
    # Ajouter timestamp
    client_info["last_seen"] = datetime.now().isoformat()
    
    with open(client_file, 'w', encoding='utf-8') as f:
        json.dump(client_info, f, ensure_ascii=False, indent=2)

def load_all_clients(hide_unknown=False):
    """Charger les informations de tous les clients"""
    clients = []
    if not TELEMETRY_PATH.exists():
        return clients
    
    for client_file in TELEMETRY_PATH.glob("client_*.json"):
        try:
            with open(client_file, 'r', encoding='utf-8') as f:
                client_data = json.load(f)
                
                # Filtrer les postes "inconnus" si demandé
                if hide_unknown:
                    system_info = client_data.get("system_info", {})
                    hostname = system_info.get("hostname", "")
                    username = system_info.get("username", "")
                    platform = system_info.get("platform", "")
                    
                    # Ignorer les postes avec des informations "Inconnu"
                    if (hostname == "Inconnu" or hostname == "" or
                        username == "Inconnu" or username == "" or
                        platform == "Inconnu" or platform == ""):
                        continue
                
                clients.append(client_data)
        except:
            continue
    
    # Trier par dernière connexion
    clients.sort(key=lambda x: x.get("last_seen", ""), reverse=True)
    return clients

def get_client_stats():
    """Obtenir les statistiques des clients"""
    clients = load_all_clients()
    
    # Clients actifs (connectés dans les 24 dernières heures)
    now = datetime.now()
    active_clients = 0
    
    versions_count = {}
    os_count = {}
    
    for client in clients:
        try:
            last_seen = datetime.fromisoformat(client.get("last_seen", ""))
            if now - last_seen < timedelta(days=1):
                active_clients += 1
        except:
            pass
        
        # Compter les versions
        version = client.get("current_version", "Inconnue")
        versions_count[version] = versions_count.get(version, 0) + 1
        
        # Compter les OS
        os_name = client.get("system_info", {}).get("platform", "Inconnu")
        os_count[os_name] = os_count.get(os_name, 0) + 1
    
    return {
        "total_clients": len(clients),
        "active_clients": active_clients,
        "versions_distribution": versions_count,
        "os_distribution": os_count
    }

# ============= ROUTES PUBLIQUES (API CLIENTS AVEC TÉLÉMÉTRIE) =============

@app.get("/")
def root():
    """Page d'accueil publique"""
    return {"message": "MATELAS Update Server with Telemetry", "status": "online", "port": 8090}

@app.post("/api/v1/check-updates")
def check_updates_with_telemetry(request: Request):
    """API pour vérifier les mises à jour avec collecte de télémétrie"""
    try:
        # Récupérer les informations du client depuis le body de la requête
        client_info = {}
        
        # Informations IP et User-Agent
        client_info["ip_address"] = request.client.host
        client_info["user_agent"] = request.headers.get("user-agent", "")
        
        # Générer un ID unique si pas fourni
        client_info["client_id"] = request.headers.get("X-Client-ID", str(uuid.uuid4()))
        
        # Informations basiques (seront enrichies par le client)
        client_info["current_version"] = request.headers.get("X-Current-Version", "Inconnue")
        client_info["system_info"] = {
            "platform": request.headers.get("X-Platform", "Inconnu"),
            "hostname": request.headers.get("X-Hostname", "Inconnu"),
            "username": request.headers.get("X-Username", "Inconnu")
        }
        
        # Sauvegarder les informations du client
        save_client_info(client_info)
        
        # Continuer avec la logique de mise à jour normale
        manifest = load_manifest()
        versions = manifest.get("versions", [])
        
        if not versions:
            return JSONResponse({"available": False, "message": "Aucune version disponible"})
        
        # Version la plus récente
        latest = max(versions, key=lambda x: tuple(map(int, x["version"].split('.'))))
        
        # Comparer les versions
        try:
            current_tuple = tuple(map(int, client_info["current_version"].split('.')))
            latest_tuple = tuple(map(int, latest["version"].split('.')))
            is_update_available = latest_tuple > current_tuple
        except ValueError:
            # Si la version actuelle n'est pas dans le bon format, considérer qu'une mise à jour est disponible
            is_update_available = True
        
        return JSONResponse({
            "available": is_update_available,
            "latest_version": latest["version"],
            "download_url": f"{SERVER_BASE_URL}/api/v1/download/{latest['version']}",
            "description": latest.get("description", ""),
            "changelog": latest.get("changelog", ""),
            "file_size": latest.get("file_size", 0),
            "release_date": latest.get("release_date", ""),
            "current_version": client_info["current_version"]
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/api/v1/check-updates")
def check_updates_get(request: Request, current_version: str = "0.0.0"):
    """API GET pour compatibilité avec les anciens clients"""
    try:
        # Informations basiques du client
        client_info = {
            "client_id": request.headers.get("X-Client-ID", str(uuid.uuid4())),
            "ip_address": request.client.host,
            "user_agent": request.headers.get("user-agent", ""),
            "current_version": current_version,
            "system_info": {
                "platform": request.headers.get("X-Platform", "Inconnu"),
                "hostname": request.headers.get("X-Hostname", "Inconnu"),
                "username": request.headers.get("X-Username", "Inconnu")
            }
        }
        
        save_client_info(client_info)
        
        manifest = load_manifest()
        versions = manifest.get("versions", [])
        
        if not versions:
            return JSONResponse({"available": False, "message": "Aucune version disponible"})
        
        latest = max(versions, key=lambda x: tuple(map(int, x["version"].split('.'))))
        
        # Comparer les versions
        try:
            current_tuple = tuple(map(int, current_version.split('.')))
            latest_tuple = tuple(map(int, latest["version"].split('.')))
            is_update_available = latest_tuple > current_tuple
        except ValueError:
            # Si la version actuelle n'est pas dans le bon format, considérer qu'une mise à jour est disponible
            is_update_available = True
        
        return JSONResponse({
            "available": is_update_available,
            "latest_version": latest["version"],
            "download_url": f"{SERVER_BASE_URL}/api/v1/download/{latest['version']}",
            "description": latest.get("description", ""),
            "changelog": latest.get("changelog", ""),
            "file_size": latest.get("file_size", 0),
            "release_date": latest.get("release_date", ""),
            "current_version": current_version
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/api/v1/download/{version}")
def download_version(version: str, request: Request):
    """Télécharger une version avec tracking du téléchargement"""
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
                    
                    # Logger le téléchargement
                    download_info = {
                        "client_id": request.headers.get("X-Client-ID", "unknown"),
                        "ip_address": request.client.host,
                        "version": version,
                        "timestamp": datetime.now().isoformat(),
                        "user_agent": request.headers.get("user-agent", "")
                    }
                    
                    downloads_log = TELEMETRY_PATH / "downloads.jsonl"
                    with open(downloads_log, 'a', encoding='utf-8') as f:
                        f.write(json.dumps(download_info) + "\n")
                    
                    return FileResponse(
                        file_path, 
                        filename=v["filename"],
                        media_type="application/zip"
                    )
        
        raise HTTPException(404, "Version non trouvée")
    except Exception as e:
        raise HTTPException(500, str(e))

# ============= INTERFACE D'ADMINISTRATION AVEC TÉLÉMÉTRIE =============

@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request, username: str = Depends(verify_credentials)):
    """Tableau de bord d'administration avec télémétrie"""
    manifest = load_manifest()
    versions = manifest.get("versions", [])
    stats = manifest.get("statistics", {})
    client_stats = get_client_stats()
    
    # Statistiques
    total_versions = len(versions)
    total_downloads = stats.get("total_downloads", 0)
    latest_version = max(versions, key=lambda x: tuple(map(int, x["version"].split('.'))))["version"] if versions else "Aucune"
    
    return templates.TemplateResponse("admin_dashboard_telemetry.html", {
        "request": request,
        "total_versions": total_versions,
        "total_downloads": total_downloads,
        "latest_version": latest_version,
        "total_clients": client_stats["total_clients"],
        "active_clients": client_stats["active_clients"],
        "versions": sorted(versions, key=lambda x: tuple(map(int, x["version"].split('.'))), reverse=True)
    })

@app.get("/admin/clients", response_class=HTMLResponse)
def admin_clients(request: Request, hide_unknown: bool = False, username: str = Depends(verify_credentials)):
    """Page de gestion des clients connectés"""
    clients = load_all_clients(hide_unknown=hide_unknown)
    all_clients = load_all_clients(hide_unknown=False)  # Pour les stats totales
    client_stats = get_client_stats()
    
    return templates.TemplateResponse("admin_clients.html", {
        "request": request,
        "clients": clients,
        "client_stats": client_stats,
        "hide_unknown": hide_unknown,
        "total_clients": len(all_clients),
        "visible_clients": len(clients)
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
    """Page des statistiques avec télémétrie"""
    manifest = load_manifest()
    client_stats = get_client_stats()
    
    return templates.TemplateResponse("admin_stats_telemetry.html", {
        "request": request,
        "manifest": manifest,
        "client_stats": client_stats
    })

@app.get("/api/v1/telemetry/stats")
def get_telemetry_stats():
    """API pour obtenir les statistiques de télémétrie en temps réel"""
    try:
        clients = load_all_clients()
        
        # Calculer les statistiques
        now = datetime.now()
        active_clients = 0
        total_clients = len(clients)
        
        for client in clients:
            # Client actif si vu dans les 30 dernières minutes
            if client.get("last_seen"):
                try:
                    last_seen = datetime.fromisoformat(client["last_seen"])
                    if (now - last_seen).seconds < 1800:  # 30 minutes
                        active_clients += 1
                except:
                    pass
        
        return {
            "active_clients": active_clients,
            "total_clients": total_clients,
            "last_update": now.isoformat(),
            "timestamp": now.strftime("%H:%M:%S")
        }
    except Exception as e:
        return {"error": str(e), "active_clients": 0, "total_clients": 0}

@app.get("/api/v1/clients/{client_id}/details")
def get_client_details(client_id: str):
    """API pour obtenir les détails d'un client spécifique"""
    try:
        client_file = TELEMETRY_PATH / f"client_{client_id}.json"
        
        if not client_file.exists():
            raise HTTPException(404, "Client non trouvé")
        
        with open(client_file, 'r', encoding='utf-8') as f:
            client_data = json.load(f)
        
        # Enrichir les données avec des informations calculées
        system_info = client_data.get("system_info", {})
        
        response_data = {
            "client_id": client_data.get("client_id", ""),
            "hostname": system_info.get("hostname", "Inconnu"),
            "username": system_info.get("username", "Inconnu"),
            "platform": system_info.get("platform", "Inconnu"),
            "ip_address": client_data.get("ip_address", "Inconnue"),
            "current_version": client_data.get("current_version", "Inconnue"),
            "first_seen": client_data.get("first_seen", "Inconnue"),
            "last_seen": client_data.get("last_seen", "Inconnue"),
            "user_agent": client_data.get("user_agent", "Non disponible"),
            "update_count": client_data.get("update_count", 0)
        }
        
        return JSONResponse(response_data)
        
    except Exception as e:
        raise HTTPException(500, f"Erreur lors de la récupération des détails: {str(e)}")

@app.delete("/api/v1/clients/{client_id}")
def delete_client(client_id: str, username: str = Depends(verify_credentials)):
    """API pour supprimer un client de la télémétrie"""
    try:
        client_file = TELEMETRY_PATH / f"client_{client_id}.json"
        
        if not client_file.exists():
            raise HTTPException(404, "Client non trouvé")
        
        # Lire les informations du client avant suppression pour les logs
        with open(client_file, 'r', encoding='utf-8') as f:
            client_data = json.load(f)
        
        # Supprimer le fichier
        client_file.unlink()
        
        # Log de la suppression
        print(f"🗑️ Client supprimé: {client_id} ({client_data.get('system_info', {}).get('hostname', 'Inconnu')})")
        
        return {
            "success": True, 
            "message": f"Client {client_id} supprimé avec succès",
            "deleted_client": {
                "client_id": client_id,
                "hostname": client_data.get('system_info', {}).get('hostname', 'Inconnu'),
                "last_seen": client_data.get('last_seen', 'N/A')
            }
        }
    except FileNotFoundError:
        raise HTTPException(404, "Client non trouvé")
    except Exception as e:
        raise HTTPException(500, f"Erreur lors de la suppression: {str(e)}")

@app.delete("/api/v1/clients/cleanup/old")
def cleanup_old_clients(days: int = 30, username: str = Depends(verify_credentials)):
    """API pour supprimer les clients inactifs depuis X jours"""
    try:
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days)
        deleted_clients = []
        
        for client_file in TELEMETRY_PATH.glob("client_*.json"):
            try:
                with open(client_file, 'r', encoding='utf-8') as f:
                    client_data = json.load(f)
                
                last_seen_str = client_data.get("last_seen", "")
                if last_seen_str:
                    last_seen = datetime.fromisoformat(last_seen_str)
                    if last_seen < cutoff_date:
                        client_id = client_data.get("client_id", "unknown")
                        hostname = client_data.get('system_info', {}).get('hostname', 'Inconnu')
                        
                        client_file.unlink()
                        deleted_clients.append({
                            "client_id": client_id,
                            "hostname": hostname,
                            "last_seen": last_seen_str
                        })
            except:
                continue
        
        print(f"🧹 Nettoyage automatique: {len(deleted_clients)} clients supprimés (plus de {days} jours)")
        
        return {
            "success": True,
            "message": f"{len(deleted_clients)} clients inactifs supprimés",
            "deleted_count": len(deleted_clients),
            "deleted_clients": deleted_clients,
            "cutoff_days": days
        }
    except Exception as e:
        raise HTTPException(500, f"Erreur lors du nettoyage: {str(e)}")

if __name__ == "__main__":
    print("🚀 Démarrage du serveur d'administration MATELAS avec TÉLÉMÉTRIE")
    print("=" * 70)
    print(f"🌐 Interface admin: http://localhost:8091/admin")
    print(f"👥 Gestion clients: http://localhost:8091/admin/clients")
    print(f"👤 Identifiants: {ADMIN_USERNAME} / {ADMIN_PASSWORD}")
    print(f"📦 API clients: http://localhost:8091/api/v1/check-updates")
    print()
    print("📊 Nouvelles fonctionnalités télémétrie:")
    print("   • Suivi des postes clients en temps réel")
    print("   • Informations système (OS, nom de poste, utilisateur)")
    print("   • Statistiques de versions utilisées")
    print("   • Historique des téléchargements")
    
    uvicorn.run(app, host="0.0.0.0", port=8092)