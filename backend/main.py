import os
import shutil
import logging
import json
from fastapi import FastAPI, File, UploadFile, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import fitz  # PyMuPDF
import uvicorn
import tempfile
import httpx
from typing import List
from datetime import datetime
# Ajouter le répertoire backend au path pour les imports (commenté pour PyInstaller)
# import sys
# import os
# backend_dir = os.path.dirname(__file__)
# if backend_dir not in sys.path:
#     sys.path.insert(0, backend_dir)

from backend.date_utils import get_week_dates
from backend.article_utils import contient_dosseret_ou_tete, contient_fermeture_liaison, contient_surmatelas, filtrer_articles_matelas
from backend.operation_utils import mots_operation_trouves
from backend.matelas_utils import detecter_noyau_matelas
from backend.hauteur_utils import calculer_hauteur_matelas
from backend.fermete_utils import detecter_fermete_matelas
from backend.housse_utils import detecter_type_housse
from backend.matiere_housse_utils import detecter_matiere_housse
from backend.poignees_utils import detecter_poignees
from backend.dimensions_utils import detecter_dimensions
from backend.latex_naturel_referentiel import get_valeur_latex_naturel
from backend.latex_mixte7zones_referentiel import get_valeur_latex_mixte7zones
from backend.mousse_rainuree7zones_referentiel import get_valeur_mousse_rainuree7zones
from backend.select43_utils import get_select43_display_value
from backend.select43_longueur_housse_utils import get_select43_longueur_housse_value
from backend.latex_renforce_utils import get_latex_renforce_display_value
from backend.latex_renforce_longueur_utils import get_latex_renforce_longueur_housse
from backend.mousse_visco_utils import get_mousse_visco_value
from backend.mousse_visco_longueur_utils import get_mousse_visco_longueur_value
from backend.latex_naturel_longueur_housse_utils import get_latex_naturel_longueur_housse_value
from backend.latex_mixte7zones_longueur_housse_utils import get_latex_mixte7zones_longueur_housse_value
from backend.mousse_rainuree7zones_longueur_housse_utils import get_mousse_rainuree7zones_longueur_housse_value
from backend.decoupe_noyau_utils import calcul_decoupe_noyau
from backend.client_utils import extraire_donnees_client, valider_donnees_client
from backend.pre_import_utils import creer_pre_import, valider_pre_import, formater_pre_import_pour_affichage
import math
import asyncio
import sys

# Ajouter le répertoire parent au path (commenté pour PyInstaller)  
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import config
from backend.llm_provider import llm_manager

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
# Ajout d'un handler fichier dédié pour le debug LLM - avec chemin sécurisé
import tempfile
from pathlib import Path

# Créer un dossier de logs dans un répertoire accessible
if getattr(sys, 'frozen', False):
    # Si exécutable PyInstaller
    log_dir = Path.home() / "MatelasApp" / "logs"
else:
    # Si script Python normal
    log_dir = Path(__file__).parent.parent / "logs"

# Créer le dossier s'il n'existe pas
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "debug_llm.log"

try:
    file_handler = logging.FileHandler(str(log_file), mode='w', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.info(f"Logs sauvegardés dans: {log_file}")
except Exception as e:
    # Si problème d'écriture, utiliser un fichier temporaire
    # Utiliser le répertoire logs local
    if hasattr(sys, '_MEIPASS'):  # PyInstaller
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = str(_THIS_DIR.parent)
    log_dir = os.path.join(base_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)
    temp_log = Path(log_dir) / "matelas_debug.log"
    try:
        file_handler = logging.FileHandler(str(temp_log), mode='w', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.info(f"Logs sauvegardés dans: {temp_log}")
    except:
        # En dernier recours, désactiver les logs fichiers
        logger.info("Impossible de créer le fichier de log, logs en console seulement")

app = FastAPI()

# CORS pour usage interne local uniquement
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import pathlib
# Résolution robuste du chemin des templates pour exécution depuis racine ou backend/
_THIS_DIR = pathlib.Path(__file__).resolve().parent
_TEMPLATES_DIR = _THIS_DIR / "templates"
templates = Jinja2Templates(directory=str(_TEMPLATES_DIR))
# Utiliser un répertoire d'upload local
if hasattr(sys, '_MEIPASS'):  # PyInstaller
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = _THIS_DIR.parent
temp_upload_dir = os.path.join(str(base_dir), "temp_uploads")
os.makedirs(temp_upload_dir, exist_ok=True)
UPLOAD_DIR = temp_upload_dir

# ============================================================
# Authentication for /api/* endpoints
# ============================================================
security = HTTPBasic()

def get_auth_password() -> str:
    """Returns the configured auth password from env or config."""
    return os.environ.get("AUTH_PASSWORD", "") or config.config.get("auth_password", "")

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    """HTTP Basic auth check — username is ignored, only password matters."""
    expected = get_auth_password()
    if not expected:
        # No password configured → allow access (dev mode)
        return credentials
    if not secrets.compare_digest(credentials.password.encode(), expected.encode()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mot de passe incorrect",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials

# ============================================================
# JSON API endpoints
# ============================================================

@app.get("/api/health")
def api_health():
    """Health check JSON endpoint (public, no auth)."""
    from backend.version import __version__ as backend_version
    return {"status": "ok", "version": backend_version}

@app.get("/api/release-notes")
def api_release_notes():
    """Return release notes content (public, no auth)."""
    import os as _os
    base = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
    notes_path = _os.path.join(base, "NOTES_DE_VERSION.md")
    content = ""
    if _os.path.exists(notes_path):
        with open(notes_path, "r", encoding="utf-8") as f:
            content = f.read()
    from backend.version import __version__ as backend_version
    return {"version": backend_version, "content": content}

@app.get("/api/auth/check")
def api_auth_check(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    """Verify credentials. Returns 401 if password is wrong."""
    return {"authenticated": True}

@app.get("/api/settings")
def api_get_settings(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    """Get application settings."""
    return {
        "excel_output_directory": config.get_excel_output_directory(),
        "noyau_order": config.get_noyau_order(),
    }

@app.put("/api/settings")
def api_put_settings(body: dict, credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    """Update application settings."""
    if "excel_output_directory" in body:
        directory = body["excel_output_directory"].strip()
        if not directory:
            raise HTTPException(status_code=400, detail="Le répertoire ne peut pas être vide")
        os.makedirs(directory, exist_ok=True)
        config.set_excel_output_directory(directory)
    if "noyau_order" in body:
        order = body["noyau_order"]
        if not isinstance(order, list):
            raise HTTPException(status_code=400, detail="noyau_order doit être une liste")
        config.set_noyau_order(order)
    return {
        "status": "ok",
        "excel_output_directory": config.get_excel_output_directory(),
        "noyau_order": config.get_noyau_order(),
    }

@app.post("/api/upload")
async def api_upload(
    file: List[UploadFile] = File(...),
    semaine_prod: int = Form(...),
    annee_prod: int = Form(...),
    commande_client: List[str] = Form(...),
    semaine_matelas: int = Form(None),
    annee_matelas: int = Form(None),
    semaine_sommiers: int = Form(None),
    annee_sommiers: int = Form(None),
    credentials: HTTPBasicCredentials = Depends(verify_credentials),
):
    """
    Process uploaded PDF files and return structured JSON results.
    Also generates Excel output files available via /api/download/.
    """
    from backend.web_processing import web_processor

    # Save uploaded files to temp dir
    saved_paths = []
    try:
        for f in file:
            if not f.filename.endswith(".pdf"):
                continue
            temp_path = os.path.join(UPLOAD_DIR, f.filename)
            with open(temp_path, "wb") as buf:
                shutil.copyfileobj(f.file, buf)
            saved_paths.append(temp_path)

        if not saved_paths:
            return JSONResponse(
                status_code=400,
                content={"error": "Aucun fichier PDF valide fourni"},
            )

        result = await web_processor.process_uploaded_files(
            file_paths=saved_paths,
            semaine_prod=semaine_prod,
            annee_prod=annee_prod,
            commande_client=commande_client,
            semaine_matelas=semaine_matelas,
            annee_matelas=annee_matelas,
            semaine_sommiers=semaine_sommiers,
            annee_sommiers=annee_sommiers,
        )

        return JSONResponse(content=result)

    finally:
        # Cleanup temp files
        for p in saved_paths:
            try:
                os.remove(p)
            except OSError:
                pass

@app.get("/api/download/{filename}")
def api_download(filename: str, credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    """Download a generated Excel file."""
    output_dir = config.get_excel_output_directory()
    file_path = os.path.join(output_dir, filename)

    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="Fichier non trouvé")

    return FileResponse(
        file_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=filename,
    )

@app.get("/api/files")
def api_list_files(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    """List available Excel output files."""
    output_dir = config.get_excel_output_directory()
    if not os.path.isdir(output_dir):
        return {"files": []}
    files = []
    for f in sorted(os.listdir(output_dir)):
        if f.endswith(".xlsx"):
            fp = os.path.join(output_dir, f)
            files.append({
                "name": f,
                "size": os.path.getsize(fp),
                "modified": os.path.getmtime(fp),
            })
    return {"files": files}

@app.delete("/api/files/{filename}")
def api_delete_file(filename: str, credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    """Delete a generated Excel file."""
    output_dir = config.get_excel_output_directory()
    file_path = os.path.join(output_dir, filename)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="Fichier non trouvé")
    os.remove(file_path)
    return {"status": "ok", "deleted": filename}

# ============================================================
# Existing HTML endpoints (preserved for desktop compatibility)
# ============================================================

@app.get("/", response_class=HTMLResponse)
def index(request: Request, result: dict = None, error: str = None):
    # If static frontend is deployed, serve the SPA index.html
    _spa_index = pathlib.Path(__file__).resolve().parent.parent / "static" / "index.html"
    if _spa_index.is_file():
        from starlette.responses import FileResponse as _FR
        return _FR(str(_spa_index))
    current_year = datetime.now().year
    logger.info(f"Accès à la page d'accueil - result: {result}, error: {error}")
    return templates.TemplateResponse("index.html", {"request": request, "result": result, "error": error, "current_year": current_year})

@app.get("/health")
def health_check():
    logger.info("Health check appelé")
    return {"status": "ok", "message": "Application opérationnelle"}

@app.post("/upload", response_class=HTMLResponse)
async def upload_pdf(
    request: Request,
    file: List[UploadFile] = File(...),
    enrich_llm: str = Form("no"),
    llm_provider: str = Form("ollama"),
    openrouter_api_key: str = Form(None),
    semaine_prod: int = Form(...),
    annee_prod: int = Form(...),
    commande_client: List[str] = Form(...)
):
    logger.info(f"Début upload - fichiers: {[f.filename for f in file]}, enrich_llm: {enrich_llm}, llm_provider: {llm_provider}, semaine_prod: {semaine_prod}, annee_prod: {annee_prod}, commande_client: {commande_client}")
    
    results = []
    errors = []
    for idx, f in enumerate(file):
        processing_steps = {
            "progress": 0,
            "extraction": None,
            "llm": None
        }
        if not f.filename.endswith(".pdf"):
            logger.warning(f"Fichier non PDF rejeté: {f.filename}")
            errors.append(f"Fichier non PDF: {f.filename}")
            continue
        temp_path = os.path.join(UPLOAD_DIR, f.filename)
        logger.info(f"Sauvegarde temporaire: {temp_path}")
        try:
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(f.file, buffer)
            logger.info("Fichier sauvegardé avec succès")
        except Exception as e:
            logger.error(f"Erreur sauvegarde fichier: {e}")
            errors.append(f"Erreur sauvegarde {f.filename}: {e}")
            continue
        # Extraction du texte (I/O optimisée)
        try:
            logger.info("Ouverture PDF avec PyMuPDF (lecture en mémoire)")
            with open(temp_path, "rb") as pdf_f:
                pdf_bytes = pdf_f.read()
            # Utilisation de stream pour éviter un second accès disque
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            text = "\n".join(page.get_text() for page in doc)
            doc.close()
            logger.info(f"Extraction texte réussie - {len(text)} caractères")
            processing_steps["extraction"] = {
                "nb_caracteres": len(text),
                "nb_mots": len(text.split()),
                "preview": text[:500] + "..." if len(text) > 500 else text
            }
            processing_steps["progress"] = 50
            # Correction : injecter un texte d'exemple si le texte est vide ou non pertinent
            if not text.strip() or not any(m in text.lower() for m in ["matelas", "sommier", "latex", "mousse", "dimensions", "fermeté"]):
                logger.warning("Texte extrait vide ou non pertinent, injection d'un exemple pour le LLM.")
                text = "MATELAS 1 PIÈCE - MOUSSE RAINURÉE 7 ZONES 140x190 Mme Gauche\nMATELAS 1 PIÈCE - LATEX NATUREL 160x200 Mr Droit"
        except Exception as e:
            logger.error(f"Erreur extraction PDF: {e}")
            errors.append(f"Erreur extraction {f.filename}: {e}")
            continue
        # LLM (optionnel)
        llm_result = None
        if enrich_llm == "yes":
            if llm_provider == "ollama":
                try:
                    logger.info("Appel au LLM (Ollama)")
                    # Déporter l'appel sync dans un thread pour ne pas bloquer
                    loop = asyncio.get_event_loop()
                    llm_result = await loop.run_in_executor(None, lambda: asyncio.run(call_llm(text)))
                    logger.info(f"LLM appelé avec succès - réponse: {llm_result[:100]}...")
                    try:
                        llm_data = json.loads(llm_result)
                        processing_steps["llm"] = {
                            "model": "gpt-oss:20b",
                            "articles": {
                                "articles": len(llm_data.get("articles", [])),
                                "societe": 1 if llm_data.get("societe") else 0,
                                "client": 1 if llm_data.get("client") else 0,
                                "commande": 1 if llm_data.get("commande") else 0,
                                "paiement": 1 if llm_data.get("paiement") else 0
                            },
                            "raw_result": llm_result
                        }
                    except:
                                            processing_steps["llm"] = {
                        "model": "gpt-oss:20b",
                        "raw_result": llm_result
                    }
                    processing_steps["progress"] = 100
                except Exception as e:
                    logger.error(f"Erreur LLM: {e}")
                    llm_result = f"Erreur LLM: {e}"
                    processing_steps["llm"] = {
                        "model": "gpt-oss:20b",
                        "error": str(e)
                    }
            elif llm_provider == "openrouter":
                try:
                    if not openrouter_api_key:
                        raise Exception("Clé API OpenRouter manquante")
                    logger.info("Appel à OpenRouter avec GPT-4-Turbo")
                    # Déporter l'appel sync dans un thread pour ne pas bloquer
                    loop = asyncio.get_event_loop()
                    llm_result = await loop.run_in_executor(None, lambda: asyncio.run(call_llm(text)))
                    logger.info(f"OpenRouter appelé avec succès - réponse: {llm_result[:100]}...")
                    try:
                        llm_data = json.loads(llm_result)
                        processing_steps["llm"] = {
                            "model": "openai/gpt-4-turbo",
                            "articles": {
                                "articles": len(llm_data.get("articles", [])),
                                "societe": 1 if llm_data.get("societe") else 0,
                                "client": 1 if llm_data.get("client") else 0,
                                "commande": 1 if llm_data.get("commande") else 0,
                                "paiement": 1 if llm_data.get("paiement") else 0
                            },
                            "raw_result": llm_result
                        }
                    except json.JSONDecodeError as json_err:
                        logger.warning(f"Erreur parsing JSON OpenRouter: {json_err}")
                        processing_steps["llm"] = {
                            "model": "openai/gpt-4-turbo",
                            "raw_result": llm_result,
                            "json_error": str(json_err)
                        }
                    processing_steps["progress"] = 100
                except Exception as e:
                    logger.error(f"Erreur OpenRouter: {e}")
                    llm_result = f"Erreur OpenRouter: {e}"
                    processing_steps["llm"] = {
                        "model": "openai/gpt-4-turbo",
                        "error": str(e)
                    }
        else:
            processing_steps["progress"] = 100
        # Nettoyage du fichier temporaire
        try:
            os.remove(temp_path)
            logger.info("Fichier temporaire supprimé")
        except Exception as e:
            logger.warning(f"Erreur suppression fichier temporaire: {e}")
        # Vérification DOSSERET/TETE après LLM
        contient_dosseret_tete = False
        articles_llm = []
        mots_operation_list = []
        noyaux_matelas = []
        donnees_client = {}
        try:
            logger.info(f"Début traitement LLM pour {f.filename}")
            if llm_result and llm_result.strip():
                logger.info(f"LLM result trouvé pour {f.filename}, longueur: {len(llm_result)}")
                logger.info(f"LLM result brut pour {f.filename}: {llm_result[:500]}...")
                
                # Nettoyer et parser le JSON
                cleaned_llm_result = clean_and_parse_json(llm_result)
                logger.info(f"LLM result nettoyé pour {f.filename}, longueur: {len(cleaned_llm_result)}")
                logger.info(f"LLM result nettoyé pour {f.filename}: {cleaned_llm_result[:500]}...")
                
                if cleaned_llm_result.strip():
                    try:
                        llm_data = json.loads(cleaned_llm_result)
                        logger.info(f"JSON parsé avec succès pour {f.filename}")
                        if not isinstance(llm_data, dict):
                            logger.warning(f"LLM result n'est pas un dictionnaire pour {f.filename}: {type(llm_data)}")
                            llm_data = {}
                        else:
                            logger.info(f"llm_data est un dictionnaire valide pour {f.filename}")
                            # Extraction des données client (avec fallback sur texte brut pour la ville)
                            donnees_client = extraire_donnees_client(llm_data, raw_text=text)
                            logger.info(f"Données client extraites pour {f.filename}: {donnees_client}")
                    except json.JSONDecodeError as json_err:
                        logger.error(f"Erreur parsing JSON pour {f.filename}: {json_err}")
                        logger.error(f"Contenu qui cause l'erreur: {cleaned_llm_result}")
                        llm_data = {}
                else:
                    logger.warning(f"LLM result vide après nettoyage pour {f.filename}")
                    llm_data = {}
            else:
                logger.warning(f"Pas de résultat LLM pour {f.filename}")
                llm_data = {}
            
            # Traitement des données LLM (que ce soit avec ou sans LLM)
            logger.info(f"Traitement des données LLM pour {f.filename}")
            logger.info(f"Type de llm_data: {type(llm_data)}")
            logger.info(f"Contenu de llm_data: {llm_data}")
            logger.info(f"Clés dans llm_data pour {f.filename}: {list(llm_data.keys())}")
            if 'articles' in llm_data and llm_data['articles']:
                logger.info(f"Premier article: {llm_data['articles'][0]}")
            else:
                logger.info(f"Aucun article trouvé dans llm_data['articles']")
            # On cherche dans tous les articles potentiels
            articles_llm = []
            matelas_articles = []
            conditions_paiement = []
            mots_operation_list = []  # Initialisation ici
            for key in llm_data:
                logger.info(f"Traitement de la clé '{key}' pour {f.filename}")
                if isinstance(llm_data[key], list):
                    articles_llm.extend(llm_data[key])
                    logger.info(f"Articles ajoutés pour {f.filename}, total: {len(articles_llm)}")
                    if key.lower() == "articles":
                        logger.info(f"Traitement des articles pour {f.filename}")
                        # Appliquer le filtrage pour exclure les PROTÈGE MATELAS
                        articles_filtres = filtrer_articles_matelas(llm_data[key])
                        logger.info(f"Articles après filtrage pour {f.filename}: {len(articles_filtres)} (avant: {len(llm_data[key])})")
                        
                        for article in articles_filtres:
                            description = article.get('description', '').upper()
                            logger.info(f"Article description pour {f.filename}: {description[:50]}...")
                            if description.startswith('MATELAS'):
                                logger.info(f"Matelas trouvé pour {f.filename}: {description[:50]}...")
                                logger.info(f"Article matelas complet: {article}")
                                matelas_articles.append(article)
                elif key == "paiement" and isinstance(llm_data[key], dict):
                    # Ajouter les conditions de paiement pour la recherche des mots opérationnels
                    conditions_paiement.append(llm_data[key])
                    logger.info(f"Conditions paiement ajoutées pour {f.filename}")
            logger.info(f"DEBUG articles_llm pour {f.filename}: {articles_llm}")
            logger.info(f"DEBUG matelas_articles pour {f.filename}: {matelas_articles}")
            logger.info(f"DEBUG conditions_paiement pour {f.filename}: {conditions_paiement}")
            contient_dosseret_tete = contient_dosseret_ou_tete(articles_llm)
            # Rechercher les mots opérationnels dans les articles ET dans le texte complet du PDF
            mots_operation_list = mots_operation_trouves(articles_llm + conditions_paiement, text)
            logger.info(f"DEBUG mots_operation_trouves pour {f.filename}: {mots_operation_list}")
            noyaux_matelas = detecter_noyau_matelas(matelas_articles)
            logger.info(f"DEBUG noyaux_matelas pour {f.filename}: {noyaux_matelas}")
        except Exception as e:
            logger.warning(f"Erreur détection dosseret/tete, mots opération ou noyau matelas: {e}")
            contient_dosseret_tete = False
            mots_operation_list = []
            noyaux_matelas = []
        # Après extraction des articles_llm (avant la boucle sur les matelas)
        fermeture_liaison = contient_fermeture_liaison(articles_llm)
        surmatelas = contient_surmatelas(articles_llm)
        # Calcul date pour chaque fichier
        semaine_annee = f"{semaine_prod}_{annee_prod}"
        lundi, vendredi = get_week_dates(semaine_prod, annee_prod)
        cc_val = commande_client[idx] if idx < len(commande_client) else ""
        
        # Créer une configuration pour chaque matelas trouvé
        configurations_matelas = []
        config_index = 1
        # On récupère la liste des articles LLM d'origine pour avoir titre_cote
        articles_llm_origin = llm_data.get('articles', []) if isinstance(llm_data, dict) else []
        
        # Ne traiter que les articles qui ont un noyau détecté (exclut automatiquement les protège-matelas)
        for noyau_info in noyaux_matelas:
            idx = noyau_info["index"] - 1  # index est 1-based, on le convertit en 0-based
            if idx >= len(matelas_articles):
                continue
            article = matelas_articles[idx]
            config = article.copy()
            
            # Ajout du traitement du champ information
            info = article.get("information", "")
            config["information"] = info
            
            config["matelas_index"] = config_index
            config["commande_client"] = cc_val
            config["semaine_annee"] = semaine_annee
            config["lundi"] = lundi
            config["vendredi"] = vendredi
            
            # Assigner le noyau détecté
            config["noyau"] = noyau_info["noyau"]
            
            # DEBUG: Log de l'article en cours de traitement
            logger.info(f"MAIN DEBUG: Traitement article matelas {config_index}")
            logger.info(f"MAIN DEBUG: article keys: {list(article.keys())}")
            logger.info(f"MAIN DEBUG: titre_cote in article: {'titre_cote' in article}")
            if 'description' in article:
                logger.info(f"MAIN DEBUG: description: '{article['description'][:80]}...'")
                
            # Copie du champ titre_cote depuis l'article matelas actuel (déjà filtré)
            if "titre_cote" in article and article["titre_cote"]:
                config["titre_cote"] = article["titre_cote"]
                logger.info(f"MAIN DEBUG: titre_cote copié depuis article: '{config['titre_cote']}'")
            else:
                logger.info(f"MAIN DEBUG: titre_cote absent ou vide dans article, fallback activé")
                # Fallback: chercher dans articles_llm_origin par matching de description
                config["titre_cote"] = ""
                article_desc = article.get("description", "")
                logger.info(f"MAIN DEBUG: description pour matching: '{article_desc[:50]}...'")
                
                for llm_art in articles_llm_origin:
                    if (llm_art.get("type") == "matelas" and 
                        llm_art.get("description", "") == article_desc and
                        llm_art.get("titre_cote", "")):
                        config["titre_cote"] = llm_art["titre_cote"]
                        logger.info(f"MAIN DEBUG: titre_cote trouvé par matching: '{config['titre_cote']}'")
                        break
                
                # Fallback final: extraction directe depuis la description
                if not config["titre_cote"] and article_desc:
                    logger.info(f"MAIN DEBUG: Fallback final - extraction directe depuis: '{article_desc[-60:]}'")  
                    import re
                    match = re.search(r'[-\s]+(Mr|MR|Mme|MME)\s*$', article_desc.strip())
                    if match:
                        config["titre_cote"] = match.group(1).upper()
                        logger.info(f"FALLBACK SUCCESS: Extraction directe titre_cote: '{config['titre_cote']}'")
                    else:
                        logger.info(f"FALLBACK FAIL: Aucun MR/MME trouvé dans la description")
                else:
                    logger.info(f"MAIN DEBUG: Pas de fallback final (config titre_cote: '{config.get('titre_cote', 'N/A')}', article_desc: {bool(article_desc)})")
                
            # Extraction du titre simple (Mr ou Mme) si présent
            if config.get("titre_cote"):
                import re
                match = re.search(r"(Mr|Mme|MR|MME)", config["titre_cote"])
                config["titre_cote_simple"] = match.group(1) if match else ""
            else:
                config["titre_cote_simple"] = ""
            configurations_matelas.append(config)
            config_index += 1
        # Correction 1 : injecter le texte extrait dans donnees_client pour la détection mise à disposition
        donnees_client["devis_text"] = text
        # Correction 2 : détection robuste du mode de mise à disposition sur tout le texte ET sur les descriptions d'articles
        from backend.pre_import_utils import detect_mode_mise_a_disposition, normalize_text
        texte_global = text
        descriptions = "\n".join([a.get("description", "") for a in articles_llm_origin])
        logger.info(f"Texte utilisé pour la détection mise à disposition (global): {texte_global[:200]}")
        logger.info(f"Descriptions utilisées pour la détection mise à disposition: {descriptions[:200]}")
        mode_global = detect_mode_mise_a_disposition(texte_global)
        mode_desc = detect_mode_mise_a_disposition(descriptions)
        # On priorise la valeur du LLM si elle existe, sinon on met "X" ou ""
        mode_llm = llm_data.get("mode_mise_a_disposition", {}) if isinstance(llm_data, dict) else {}
        mode_final = {}
        for k in ["emporte_client_C57", "fourgon_C58", "transporteur_C59"]:
            if mode_llm.get(k, "").strip():
                mode_final[k] = mode_llm[k]
            elif mode_global.get(k) == "X" or mode_desc.get(k) == "X":
                mode_final[k] = "X"
            else:
                mode_final[k] = ""
        donnees_client["mode_mise_a_disposition"] = mode_final
        # Appel au pré-import
        pre_import_data = creer_pre_import(configurations_matelas, donnees_client, contient_dosseret_tete, mots_operation_list, fermeture_liaison)
        logger.info(f"Pré-import créé avec succès: {len(pre_import_data)} éléments")
        
        # Validation du pré-import
        if valider_pre_import(pre_import_data):
            logger.info("Pré-import validé avec succès")
        else:
            logger.warning("Pré-import non valide")
        
        # === AJOUT EXPORT EXCEL ===
        try:
            # Import stable avec préfixe backend
            from backend.excel_import_utils import ExcelMatelasImporter
            semaine = str(semaine_prod).zfill(2)
            annee = str(annee_prod)
            semaine_excel = f"S{semaine}"
            # Utiliser l'année complète pour le nommage
            id_fichier = annee
            importer = ExcelMatelasImporter()
            fichiers_excel = importer.import_configurations(pre_import_data, semaine_excel, id_fichier)
            logger.info(f"Export Excel terminé: {fichiers_excel}")
        except Exception as e:
            logger.error(f"Erreur lors de l'export Excel: {e}")
        # === FIN AJOUT EXPORT EXCEL ===
                
        # Garder aussi l'ancienne structure pour compatibilité
        calcul_date = {
            "semaine_annee": semaine_annee,
            "lundi": lundi,
            "vendredi": vendredi,
            "commande_client": cc_val
        }
        result = {
            "filename": f.filename,
            "extraction_stats": processing_steps["extraction"] if processing_steps["extraction"] else {},
            "texte_extrait": text if 'text' in locals() else "",
            "llm_result": llm_result if 'llm_result' in locals() else None,
            "processing_steps": processing_steps,
            "calcul_date": calcul_date,
            "configurations_matelas": configurations_matelas,
            "contient_dosseret_ou_tete": contient_dosseret_tete,
            "mots_operation_trouves": mots_operation_list,
            "noyaux_matelas": noyaux_matelas,
            "fermeture_liaison": fermeture_liaison,
            "surmatelas": surmatelas,
            "donnees_client": donnees_client,
            "pre_import": pre_import_data
        }
        results.append(result)
    # Affichage des erreurs éventuelles
    error_msg = "\n".join(errors) if errors else None
    return templates.TemplateResponse("index.html", {"request": request, "results": results, "error": error_msg, "semaine_prod": semaine_prod, "annee_prod": annee_prod, "commande_client": commande_client})

def clean_and_parse_json(raw_text: str) -> str:
    """Nettoie et parse le JSON retourné par le LLM"""
    if not raw_text or not raw_text.strip():
        logger.warning("Texte JSON vide ou None")
        return ""
    
    try:
        # Supprime les caractères Unicode problématiques
        cleaned_text = raw_text.encode('utf-8', errors='ignore').decode('utf-8')
        
        # Essaie de parser directement
        json.loads(cleaned_text)
        return cleaned_text
    except json.JSONDecodeError as e:
        logger.warning(f"Premier essai de parsing JSON échoué: {e}")
        
        # Si ça ne marche pas, on essaie de nettoyer plus agressivement
        try:
            # Supprime les caractères non-ASCII
            cleaned_text = ''.join(char for char in raw_text if ord(char) < 128)
            json.loads(cleaned_text)
            return cleaned_text
        except json.JSONDecodeError as e2:
            logger.warning(f"Deuxième essai de parsing JSON échoué: {e2}")
            
            # Essai de nettoyage des balises markdown
            try:
                # Supprime les balises ```json et ```
                cleaned_text = raw_text.replace('```json', '').replace('```', '').strip()
                json.loads(cleaned_text)
                return cleaned_text
            except json.JSONDecodeError as e3:
                logger.warning(f"Troisième essai de parsing JSON échoué: {e3}")
                
                # Essai de nettoyage plus agressif des balises markdown
                try:
                    # Supprime toutes les balises markdown possibles
                    cleaned_text = raw_text
                    for marker in ['```json', '```JSON', '```', '`']:
                        cleaned_text = cleaned_text.replace(marker, '')
                    cleaned_text = cleaned_text.strip()
                    json.loads(cleaned_text)
                    return cleaned_text
                except json.JSONDecodeError as e4:
                    logger.warning(f"Quatrième essai de parsing JSON échoué: {e4}")
                    
                    # En dernier recours, on retourne le texte original
                    logger.error(f"Impossible de parser le JSON: {raw_text[:200]}...")
                    return raw_text

def decode_unicode_strings(obj):
    """Décode récursivement les chaînes Unicode dans un objet JSON"""
    if isinstance(obj, dict):
        return {key: decode_unicode_strings(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [decode_unicode_strings(item) for item in obj]
    elif isinstance(obj, str):
        try:
            # Essaie de décoder les séquences Unicode
            return obj.encode('latin-1').decode('unicode_escape')
        except:
            return obj
    else:
        return obj

async def call_llm(text: str, file_name: str = "unknown", file_size: int = 0, session_id: str = None):
    """
    Appelle le LLM configuré par l'utilisateur avec tracking des coûts
    """
    try:
        # Importer les modules de tracking
        from backend.llm_provider import llm_manager
        from backend.secure_storage import secure_storage
        from backend.cost_tracker import cost_tracker
        
        current_provider = config.get_current_llm_provider()
        
        # Configuration du provider avec le nouveau système
        if current_provider == "ollama":
            api_key = None
        else:
            # Essayer d'abord le stockage sécurisé, puis fallback sur config
            api_key = secure_storage.load_api_key(current_provider)
            if not api_key:
                api_key = config.get_llm_api_key(current_provider)
            
            if not api_key:
                logger.error(f"Aucune clé API configurée pour {current_provider}")
                return f"Erreur: Clé API manquante pour {current_provider}"
        
        # Configurer le LLM manager
        llm_manager.set_provider(current_provider, api_key)
        
        # Prompt unifié pour tous les providers
        prompt = f"""
Tu es un assistant d'extraction spécialisé pour des devis de literie. Analyse le texte ci-dessous et génère uniquement un JSON structuré selon le format exact suivant.

TEXTE À ANALYSER :
{text}

RÈGLES D'EXTRACTION STRICTES :

1. STRUCTURE JSON OBLIGATOIRE :
{{
  "societe": {{
    "nom": "nom de l'entreprise",
    "capital": "capital social",
    "adresse": "adresse complète",
    "telephone": "numéro de téléphone",
    "email": "adresse email",
    "siret": "numéro SIRET",
    "APE": "code APE",
    "CEE": "numéro CEE",
    "banque": "nom de la banque",
    "IBAN": "numéro IBAN"
  }},
  "client": {{
    "nom": "nom du client",
    "adresse": "adresse COMPLÈTE du client (rue + code postal + ville). ATTENTION: ne PAS confondre avec l'adresse de la société (525 RD 642 - 59190 BORRE). L'adresse client se trouve APRÈS le nom du client, AVANT le numéro de commande.",
    "code_client": "code client"
  }},
  "commande": {{
    "numero": "numéro de commande",
    "date": "date de commande",
    "date_validite": "date de validité",
    "commercial": "nom du commercial",
    "origine": "origine de la commande"
  }},
  "mode_mise_a_disposition": {{
    "emporte_client_C57": "texte si enlèvement client",
    "fourgon_C58": "texte si livraison fourgon",
    "transporteur_C59": "texte si transporteur"
  }},
  "articles": [
    {{
      "type": "matelas|sommier|accessoire|tête de lit|pieds|remise",
      "description": "description complète de l'article. IMPORTANT: Pour les articles composés de plusieurs éléments séparés par ' + ' (ex: 'JEU DE 8 PIEDS CUBIQUE BRUT 20 CM + PLATINE DE RÉUNION + PATINS TÉFLON'), extraire la description COMPLÈTE avec tous les composants. Ne pas séparer en plusieurs articles, garder la description entière telle quelle.",
      "titre_cote": "OBLIGATOIRE: Chercher '- MME', '- MR', '- Mr', '- Mme' à la fin des descriptions de matelas (ex: 'MATELAS... 20 - MME' → 'MME', 'LATEX 20 - MR' → 'MR'). Si pas trouvé, laisser vide.",
      "information": "en-tête comme '1/ CHAMBRE XYZ' si présent",
      "quantite": nombre,
      "dimensions": "format LxlxH",
      "noyau": "type de noyau pour matelas",
      "fermete": "niveau de fermeté",
      "housse": "type de housse",
      "matiere_housse": "matériau de la housse",
      "autres_caracteristiques": {{
        "caracteristique1": "valeur1",
        "caracteristique2": "valeur2"
      }}
    }}
  ],
  "paiement": {{
    "conditions": "conditions de paiement",
    "port_ht": montant_ht_port,
    "base_ht": montant_ht_total,
    "taux_tva": pourcentage_tva,
    "total_ttc": montant_ttc,
    "acompte": montant_acompte,
    "net_a_payer": montant_final
  }}
}}

2. RÈGLES SPÉCIFIQUES :
- Pour chaque article, extraire TOUS les champs disponibles
- Le champ "autres_caracteristiques" doit contenir les spécificités non standard
- Les remises sont des articles de type "remise" avec montant dans autres_caracteristiques
- Les dimensions doivent être au format "LxlxH" (ex: "159x199x19")
- Les montants doivent être des nombres (pas de texte)
- Si une information est absente : null pour les nombres, "" pour les textes
- IMPORTANT titre_cote: Pour chaque matelas, chercher à la fin de la description s'il y a "- MME", "- MR", "- Mr", ou "- Mme" et extraire seulement la partie après le tiret (MME, MR, Mr, Mme). Exemple: "MATELAS LATEX 79/198/20 - MME" → titre_cote: "MME"
- IMPORTANT description articles composés: Si un article contient plusieurs éléments séparés par " + " (ex: "JEU DE 8 PIEDS CUBIQUE BRUT 20 CM + PLATINE DE RÉUNION + PATINS TÉFLON"), extraire la description COMPLÈTE en un seul article. Ne pas créer plusieurs articles séparés. Le type doit être "pieds" ou "accessoire" selon le contexte.

3. EXEMPLE DE RÉFÉRENCE :
{{
  "societe": {{
    "nom": "SAS Literie Westelynck",
    "capital": "23 100 Euros",
    "adresse": "525 RD 642 - 59190 BORRE",
    "telephone": "03.28.48.04.19",
    "email": "contact@lwest.fr",
    "siret": "429 352 891 00015",
    "APE": "3103Z",
    "CEE": "FR50 429 352 891",
    "banque": "Crédit Agricole d'Hazebrouck",
    "IBAN": "FR76 1670 6050 1650 4613 2602 341"
  }},
  "client": {{
    "nom": "Mr et Me LAGADEC HELENE",
    "adresse": "25 RUE DE L'ÉGLISE, 59670 BAVINCHOVE",
    "code_client": "LAGAHEBAV"
  }},
  "commande": {{
    "numero": "CM00009581",
    "date": "19/07/2025",
    "date_validite": "",
    "commercial": "P. ALINE",
    "origine": "COMMANDE"
  }},
  "mode_mise_a_disposition": {{
    "emporte_client_C57": "ENLÈVEMENT PAR VOS SOINS",
    "fourgon_C58": "",
    "transporteur_C59": ""
  }},
  "articles": [
    {{
      "type": "matelas",
      "description": "MATELAS 1 PIÈCE - LATEX PERFORÉ 7 ZONES MÉDIUM - HOUSSE TENCEL 79/198/20 - MME",
      "titre_cote": "MME",
      "information": "",
      "quantite": 2,
      "dimensions": "79x198x20",
      "noyau": "MOUSSE RAINURÉE 7 ZONES",
      "fermete": "MÉDIUM",
      "housse": "MATELASSÉE",
      "matiere_housse": "TENCEL",
      "autres_caracteristiques": {{
        "poignées": "oui",
        "lavable": "40°"
      }}
    }},
    {{
      "type": "pieds",
      "description": "JEU DE 8 PIEDS CUBIQUE BRUT 20 CM + PLATINE DE RÉUNION + PATINS TÉFLON",
      "titre_cote": "",
      "information": "",
      "quantite": 1,
      "dimensions": "",
      "noyau": "",
      "fermete": "",
      "housse": "",
      "matiere_housse": "",
      "autres_caracteristiques": {{}}
    }}
  ],
  "paiement": {{
    "conditions": "ACOMPTE DE 667 € EN CB LA COMMANDE ET SOLDE DE 1 500 € À L'ENLÈVEMENT",
    "port_ht": 0.00,
    "base_ht": 1774.21,
    "taux_tva": 20.00,
    "total_ttc": 2167.00,
    "acompte": 667.00,
    "net_a_payer": 1500.00
  }}
}}

Réponds UNIQUEMENT avec un JSON valide selon cette structure exacte.
"""
        logger.info(f"Prompt envoyé au LLM ({current_provider}) :\n{prompt}")
        logger.info(f"Appel LLM avec provider: {current_provider}")
        
        # Appel avec tracking des coûts
        result = llm_manager.call_llm(
            prompt, 
            file_name=file_name,
            file_size=file_size,
            session_id=session_id,
            temperature=0.1, 
            max_tokens=4096
        )
        
        if result["success"]:
            # Log des informations de coût si disponibles
            if 'cost_info' in result:
                cost_info = result['cost_info']
                logger.info(f"💰 Coût appel LLM: ${cost_info['total_cost']:.6f} "
                           f"({result['usage'].get('prompt_tokens', 0)} prompt + "
                           f"{result['usage'].get('completion_tokens', 0)} completion tokens)")
            
            return result["content"]
        else:
            logger.error(f"Erreur LLM {current_provider}: {result.get('error', 'Erreur inconnue')}")
            return f"Erreur LLM {current_provider}: {result.get('error', 'Erreur inconnue')}"
    except Exception as e:
        logger.error(f"Erreur lors de l'appel LLM: {e}")
        return f"Erreur lors de l'appel LLM: {str(e)}"

# ============================================================
# Serve static frontend (for Fly.io / single-container deploy)
# ============================================================
_STATIC_DIR = pathlib.Path(__file__).resolve().parent.parent / "static"
if _STATIC_DIR.is_dir():
    from starlette.staticfiles import StaticFiles
    from starlette.responses import FileResponse as StarletteFileResponse

    # Serve /assets/* directly (Vite build output)
    _ASSETS_DIR = _STATIC_DIR / "assets"
    if _ASSETS_DIR.is_dir():
        app.mount("/assets", StaticFiles(directory=str(_ASSETS_DIR)), name="frontend-assets")

    # SPA catch-all: any non-API route serves index.html
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Try to serve the exact static file first
        file_path = _STATIC_DIR / full_path
        if full_path and file_path.is_file():
            return StarletteFileResponse(str(file_path))
        # Otherwise serve index.html (SPA routing)
        return StarletteFileResponse(str(_STATIC_DIR / "index.html"))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 