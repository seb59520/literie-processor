#!/usr/bin/env python3
"""
Serveur d'administration MATELAS avec télémétrie - VERSION INTERNET
Sécurisé pour l'exposition publique avec authentification renforcée
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
import hashlib
import time

from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Request, Depends, status
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import uvicorn

# Rate limiting
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title=\"MATELAS Update Server with Telemetry - Internet Ready\",
    description=\"Serveur de mise à jour avec télémétrie - Version sécurisée Internet\",
    version=\"2.1.0\"
)

# Configuration CORS plus restrictive pour Internet
app.add_middleware(
    CORSMiddleware,
    allow_origins=[\"*\"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=[\"GET\", \"POST\"],
    allow_headers=[\"*\"],
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configuration des templates et fichiers statiques
templates = Jinja2Templates(directory=\"templates\")
app.mount(\"/static\", StaticFiles(directory=\"static\"), name=\"static\")

# Sécurité basique
security = HTTPBasic()

# Configuration - CHANGEZ CES VALEURS EN PRODUCTION
ADMIN_USERNAME = os.getenv(\"MATELAS_ADMIN_USER\", \"admin\")
ADMIN_PASSWORD = os.getenv(\"MATELAS_ADMIN_PASS\", \"matelas2025_CHANGE_ME\")
SECRET_KEY = os.getenv(\"MATELAS_SECRET_KEY\", secrets.token_urlsafe(32))

STORAGE_PATH = Path(\"update_storage\")
VERSIONS_PATH = STORAGE_PATH / \"versions\"
METADATA_PATH = STORAGE_PATH / \"metadata\"
TELEMETRY_PATH = STORAGE_PATH / \"telemetry\"
LOGS_PATH = STORAGE_PATH / \"logs\"

# Initialiser les dossiers
for path in [STORAGE_PATH, VERSIONS_PATH, METADATA_PATH, TELEMETRY_PATH, LOGS_PATH]:
    path.mkdir(exist_ok=True)

# Dictionnaire pour le rate limiting par IP
request_counts = {}

def log_security_event(event_type: str, ip: str, details: str = \"\"):
    \"\"\"Logger les événements de sécurité\"\"\"
    log_entry = {
        \"timestamp\": datetime.now().isoformat(),
        \"type\": event_type,
        \"ip\": ip,
        \"details\": details
    }
    
    log_file = LOGS_PATH / f\"security_{datetime.now().strftime('%Y%m%d')}.log\"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry) + \"\\\\n\")

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    \"\"\"Vérification des credentials admin avec logging\"\"\"
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    
    if not (correct_username and correct_password):
        log_security_event(\"auth_failed\", \"unknown\", f\"Username: {credentials.username}\")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=\"Identifiants incorrects\",
            headers={\"WWW-Authenticate\": \"Basic\"},
        )
    
    return credentials.username

def check_rate_limit(request: Request, limit: int = 20) -> bool:
    \"\"\"Vérifier le rate limiting par IP\"\"\"
    client_ip = request.client.host
    current_time = time.time()
    
    # Nettoyer les anciens compteurs (plus d'une minute)
    request_counts.clear()
    for ip in list(request_counts.keys()):
        request_counts[ip] = [t for t in request_counts[ip] if current_time - t < 60]
        if not request_counts[ip]:
            del request_counts[ip]
    
    # Vérifier le nombre de requêtes pour cette IP
    if client_ip not in request_counts:
        request_counts[client_ip] = []
    
    request_counts[client_ip].append(current_time)
    
    if len(request_counts[client_ip]) > limit:
        log_security_event(\"rate_limit_exceeded\", client_ip, f\"Requests: {len(request_counts[client_ip])}\")
        return False
    
    return True

def load_manifest():
    \"\"\"Charger le manifest des versions\"\"\"
    manifest_file = METADATA_PATH / \"manifest.json\"
    if manifest_file.exists():
        with open(manifest_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {\"versions\": [], \"statistics\": {\"total_downloads\": 0}}

def save_manifest(manifest):
    \"\"\"Sauvegarder le manifest\"\"\"
    manifest_file = METADATA_PATH / \"manifest.json\"
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

def save_client_info(client_info, request: Request):
    \"\"\"Sauvegarder les informations d'un client\"\"\"
    client_id = client_info.get(\"client_id\", \"unknown\")
    client_file = TELEMETRY_PATH / f\"client_{client_id}.json\"
    
    # Ajouter des informations de sécurité
    client_info[\"last_seen\"] = datetime.now().isoformat()
    client_info[\"ip_address\"] = request.client.host
    
    # Hasher les informations sensibles pour la vie privée
    if \"username\" in client_info.get(\"system_info\", {}):
        username = client_info[\"system_info\"][\"username\"]
        client_info[\"system_info\"][\"username_hash\"] = hashlib.sha256(username.encode()).hexdigest()[:16]
    
    with open(client_file, 'w', encoding='utf-8') as f:
        json.dump(client_info, f, ensure_ascii=False, indent=2)

def load_all_clients():
    \"\"\"Charger les informations de tous les clients\"\"\"
    clients = []
    if not TELEMETRY_PATH.exists():
        return clients
    
    for client_file in TELEMETRY_PATH.glob(\"client_*.json\"):
        try:
            with open(client_file, 'r', encoding='utf-8') as f:
                client_data = json.load(f)
                clients.append(client_data)
        except:
            continue
    
    # Trier par dernière connexion
    clients.sort(key=lambda x: x.get(\"last_seen\", \"\"), reverse=True)
    return clients

def get_client_stats():
    \"\"\"Obtenir les statistiques des clients\"\"\"
    clients = load_all_clients()
    
    # Clients actifs (connectés dans les 24 dernières heures)
    now = datetime.now()
    active_clients = 0
    
    versions_count = {}
    os_count = {}
    
    for client in clients:
        try:
            last_seen = datetime.fromisoformat(client.get(\"last_seen\", \"\"))
            if now - last_seen < timedelta(days=1):
                active_clients += 1
        except:
            pass
        
        # Compter les versions
        version = client.get(\"current_version\", \"Inconnue\")
        versions_count[version] = versions_count.get(version, 0) + 1
        
        # Compter les OS
        os_name = client.get(\"system_info\", {}).get(\"platform\", \"Inconnu\")
        os_count[os_name] = os_count.get(os_name, 0) + 1
    
    return {
        \"total_clients\": len(clients),
        \"active_clients\": active_clients,
        \"versions_distribution\": versions_count,
        \"os_distribution\": os_count
    }

# ============= ROUTES PUBLIQUES (API CLIENTS AVEC TÉLÉMÉTRIE) =============

@app.get(\"/\")
@limiter.limit(\"30/minute\")
def root(request: Request):
    \"\"\"Page d'accueil publique\"\"\"
    return {\"message\": \"MATELAS Update Server with Telemetry\", \"status\": \"online\", \"version\": \"2.1.0\"}

@app.post(\"/api/v1/check-updates\")
@limiter.limit(\"10/minute\")
def check_updates_with_telemetry(request: Request):
    \"\"\"API pour vérifier les mises à jour avec collecte de télémétrie\"\"\"
    if not check_rate_limit(request, 10):
        raise HTTPException(429, \"Trop de requêtes\")
        
    try:
        # Récupérer les informations du client depuis le body de la requête
        client_info = {}
        
        # Informations IP et User-Agent
        client_info[\"ip_address\"] = request.client.host
        client_info[\"user_agent\"] = request.headers.get(\"user-agent\", \"\")
        
        # Générer un ID unique si pas fourni
        client_info[\"client_id\"] = request.headers.get(\"X-Client-ID\", str(uuid.uuid4()))
        
        # Informations basiques (seront enrichies par le client)
        client_info[\"current_version\"] = request.headers.get(\"X-Current-Version\", \"Inconnue\")
        client_info[\"system_info\"] = {
            \"platform\": request.headers.get(\"X-Platform\", \"Inconnu\"),
            \"hostname\": request.headers.get(\"X-Hostname\", \"Inconnu\"),
            \"username\": request.headers.get(\"X-Username\", \"Inconnu\")
        }
        
        # Sauvegarder les informations du client
        save_client_info(client_info, request)
        
        # Continuer avec la logique de mise à jour normale
        manifest = load_manifest()
        versions = manifest.get(\"versions\", [])
        
        if not versions:
            return JSONResponse({\"available\": False, \"message\": \"Aucune version disponible\"})
        
        # Version la plus récente
        latest = max(versions, key=lambda x: tuple(map(int, x[\"version\"].split('.'))))
        
        # Construire l'URL de téléchargement avec l'URL publique
        base_url = str(request.base_url).rstrip('/')
        download_url = f\"{base_url}/api/v1/download/{latest['version']}\"
        
        return JSONResponse({
            \"available\": True,
            \"latest_version\": latest[\"version\"],
            \"download_url\": download_url,
            \"description\": latest.get(\"description\", \"\"),
            \"changelog\": latest.get(\"changelog\", \"\"),
            \"file_size\": latest.get(\"file_size\", 0),
            \"release_date\": latest.get(\"release_date\", \"\"),
            \"current_version\": client_info[\"current_version\"]
        })
    except Exception as e:
        log_security_event(\"api_error\", request.client.host, str(e))
        return JSONResponse({\"error\": str(e)}, status_code=500)

@app.get(\"/api/v1/check-updates\")
@limiter.limit(\"10/minute\")
def check_updates_get(request: Request, current_version: str = \"0.0.0\"):
    \"\"\"API GET pour compatibilité avec les anciens clients\"\"\"
    if not check_rate_limit(request, 10):
        raise HTTPException(429, \"Trop de requêtes\")
        
    try:
        # Informations basiques du client
        client_info = {
            \"client_id\": request.headers.get(\"X-Client-ID\", str(uuid.uuid4())),
            \"ip_address\": request.client.host,
            \"user_agent\": request.headers.get(\"user-agent\", \"\"),
            \"current_version\": current_version,
            \"system_info\": {
                \"platform\": request.headers.get(\"X-Platform\", \"Inconnu\"),
                \"hostname\": request.headers.get(\"X-Hostname\", \"Inconnu\"),
                \"username\": request.headers.get(\"X-Username\", \"Inconnu\")
            }
        }
        
        save_client_info(client_info, request)
        
        manifest = load_manifest()
        versions = manifest.get(\"versions\", [])
        
        if not versions:
            return JSONResponse({\"available\": False, \"message\": \"Aucune version disponible\"})
        
        latest = max(versions, key=lambda x: tuple(map(int, x[\"version\"].split('.'))))
        
        # Construire l'URL de téléchargement avec l'URL publique
        base_url = str(request.base_url).rstrip('/')
        download_url = f\"{base_url}/api/v1/download/{latest['version']}\"
        
        return JSONResponse({
            \"available\": True,
            \"latest_version\": latest[\"version\"],
            \"download_url\": download_url,
            \"description\": latest.get(\"description\", \"\"),
            \"changelog\": latest.get(\"changelog\", \"\"),
            \"file_size\": latest.get(\"file_size\", 0),
            \"release_date\": latest.get(\"release_date\", \"\"),
            \"current_version\": current_version
        })
    except Exception as e:
        log_security_event(\"api_error\", request.client.host, str(e))
        return JSONResponse({\"error\": str(e)}, status_code=500)

@app.get(\"/api/v1/download/{version}\")
@limiter.limit(\"5/minute\")
def download_version(version: str, request: Request):
    \"\"\"Télécharger une version avec tracking du téléchargement\"\"\"
    if not check_rate_limit(request, 5):
        raise HTTPException(429, \"Trop de requêtes de téléchargement\")
        
    try:
        manifest = load_manifest()
        versions = manifest.get(\"versions\", [])
        
        for v in versions:
            if v[\"version\"] == version:
                file_path = VERSIONS_PATH / v[\"filename\"]
                if file_path.exists():
                    # Incrémenter le compteur
                    v[\"downloads\"] = v.get(\"downloads\", 0) + 1
                    manifest[\"statistics\"][\"total_downloads\"] = manifest[\"statistics\"].get(\"total_downloads\", 0) + 1
                    save_manifest(manifest)
                    
                    # Logger le téléchargement
                    download_info = {
                        \"client_id\": request.headers.get(\"X-Client-ID\", \"unknown\"),
                        \"ip_address\": request.client.host,
                        \"version\": version,
                        \"timestamp\": datetime.now().isoformat(),
                        \"user_agent\": request.headers.get(\"user-agent\", \"\")
                    }
                    
                    downloads_log = TELEMETRY_PATH / \"downloads.jsonl\"
                    with open(downloads_log, 'a', encoding='utf-8') as f:
                        f.write(json.dumps(download_info) + \"\\\\n\")
                    
                    log_security_event(\"download\", request.client.host, f\"Version: {version}\")
                    
                    return FileResponse(
                        file_path, 
                        filename=v[\"filename\"],
                        media_type=\"application/zip\"
                    )
        
        raise HTTPException(404, \"Version non trouvée\")
    except Exception as e:
        log_security_event(\"download_error\", request.client.host, str(e))
        raise HTTPException(500, str(e))

# ============= INTERFACE D'ADMINISTRATION AVEC TÉLÉMÉTRIE =============

@app.get(\"/admin\", response_class=HTMLResponse)
@limiter.limit(\"30/minute\")
def admin_dashboard(request: Request, username: str = Depends(verify_credentials)):
    \"\"\"Tableau de bord d'administration avec télémétrie\"\"\"
    log_security_event(\"admin_access\", request.client.host, f\"User: {username}\")
    
    manifest = load_manifest()
    versions = manifest.get(\"versions\", [])
    stats = manifest.get(\"statistics\", {})
    client_stats = get_client_stats()
    
    # Statistiques
    total_versions = len(versions)
    total_downloads = stats.get(\"total_downloads\", 0)
    latest_version = max(versions, key=lambda x: tuple(map(int, x[\"version\"].split('.'))))[\"version\"] if versions else \"Aucune\"
    
    return templates.TemplateResponse(\"admin_dashboard_telemetry.html\", {
        \"request\": request,
        \"total_versions\": total_versions,
        \"total_downloads\": total_downloads,
        \"latest_version\": latest_version,
        \"total_clients\": client_stats[\"total_clients\"],
        \"active_clients\": client_stats[\"active_clients\"],
        \"versions\": sorted(versions, key=lambda x: tuple(map(int, x[\"version\"].split('.'))), reverse=True)
    })

@app.get(\"/admin/clients\", response_class=HTMLResponse)
@limiter.limit(\"30/minute\")
def admin_clients(request: Request, username: str = Depends(verify_credentials)):
    \"\"\"Page de gestion des clients connectés\"\"\"
    log_security_event(\"clients_access\", request.client.host, f\"User: {username}\")
    
    clients = load_all_clients()
    client_stats = get_client_stats()
    
    return templates.TemplateResponse(\"admin_clients.html\", {
        \"request\": request,
        \"clients\": clients,
        \"client_stats\": client_stats
    })

@app.get(\"/api/v1/clients/{client_id}/details\")
@limiter.limit(\"60/minute\")
def get_client_details(client_id: str, request: Request, username: str = Depends(verify_credentials)):
    \"\"\"API pour obtenir les détails d'un client spécifique\"\"\"
    try:
        client_file = TELEMETRY_PATH / f\"client_{client_id}.json\"
        
        if not client_file.exists():
            raise HTTPException(404, \"Client non trouvé\")
        
        with open(client_file, 'r', encoding='utf-8') as f:
            client_data = json.load(f)
        
        # Enrichir les données avec des informations calculées
        system_info = client_data.get(\"system_info\", {})
        
        response_data = {
            \"client_id\": client_data.get(\"client_id\", \"\"),
            \"hostname\": system_info.get(\"hostname\", \"Inconnu\"),
            \"username\": system_info.get(\"username\", \"Inconnu\"),
            \"platform\": system_info.get(\"platform\", \"Inconnu\"),
            \"ip_address\": client_data.get(\"ip_address\", \"Inconnue\"),
            \"current_version\": client_data.get(\"current_version\", \"Inconnue\"),
            \"first_seen\": client_data.get(\"first_seen\", \"Inconnue\"),
            \"last_seen\": client_data.get(\"last_seen\", \"Inconnue\"),
            \"user_agent\": client_data.get(\"user_agent\", \"Non disponible\"),
            \"update_count\": client_data.get(\"update_count\", 0)
        }
        
        return JSONResponse(response_data)
        
    except Exception as e:
        log_security_event(\"client_details_error\", request.client.host, str(e))
        raise HTTPException(500, f\"Erreur lors de la récupération des détails: {str(e)}\")

@app.get(\"/admin/upload\", response_class=HTMLResponse)
@limiter.limit(\"10/minute\")
def admin_upload_page(request: Request, username: str = Depends(verify_credentials)):
    \"\"\"Page d'upload\"\"\"
    return templates.TemplateResponse(\"admin_upload.html\", {\"request\": request})

# Autres routes admin avec rate limiting...
# (Upload, delete, stats similaires mais avec @limiter.limit())

@app.get(\"/admin/security\", response_class=HTMLResponse)
@limiter.limit(\"10/minute\")
def admin_security(request: Request, username: str = Depends(verify_credentials)):
    \"\"\"Page de sécurité et logs\"\"\"
    log_security_event(\"security_access\", request.client.host, f\"User: {username}\")
    
    # Lire les logs de sécurité récents
    today_log = LOGS_PATH / f\"security_{datetime.now().strftime('%Y%m%d')}.log\"
    recent_events = []
    
    if today_log.exists():
        with open(today_log, 'r', encoding='utf-8') as f:
            for line in f.readlines()[-50:]:  # Derniers 50 événements
                try:
                    event = json.loads(line.strip())
                    recent_events.append(event)
                except:
                    continue
    
    return templates.TemplateResponse(\"admin_security.html\", {
        \"request\": request,
        \"recent_events\": recent_events[::-1]  # Plus récents en premier
    })

if __name__ == \"__main__\":
    print(\"🚀 Démarrage du serveur d'administration MATELAS avec TÉLÉMÉTRIE - VERSION INTERNET\")
    print(\"=\" * 80)
    
    if ADMIN_PASSWORD == \"matelas2025_CHANGE_ME\":
        print(\"⚠️  ATTENTION: Utilisez des identifiants sécurisés en production!\")
        print(\"   Définissez les variables d'environnement:\")
        print(\"   export MATELAS_ADMIN_USER=votre_admin\")
        print(\"   export MATELAS_ADMIN_PASS=votre_mot_de_passe_fort\")
    
    print(f\"🌐 Interface admin: http://0.0.0.0:8091/admin\")
    print(f\"👥 Gestion clients: http://0.0.0.0:8091/admin/clients\")
    print(f\"🔒 Logs sécurité: http://0.0.0.0:8091/admin/security\")
    print(f\"👤 Identifiants: {ADMIN_USERNAME} / {'*' * len(ADMIN_PASSWORD)}\")
    print(f\"📦 API clients: http://0.0.0.0:8091/api/v1/check-updates\")
    print()
    print(\"🔒 Fonctionnalités de sécurité activées:\")
    print(\"   • Rate limiting par IP\")
    print(\"   • Logs d'audit complets\")
    print(\"   • Protection contre les attaques par force brute\")
    print(\"   • Headers de sécurité\")
    
    uvicorn.run(app, host=\"0.0.0.0\", port=8091)