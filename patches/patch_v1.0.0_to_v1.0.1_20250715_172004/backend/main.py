import os
import shutil
import logging
import json
from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF
import uvicorn
import tempfile
import httpx
from typing import List
from datetime import datetime
# Ajouter le répertoire backend au path pour les imports
import sys
import os
backend_dir = os.path.dirname(__file__)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from date_utils import get_week_dates
from article_utils import contient_dosseret_ou_tete, contient_fermeture_liaison, contient_surmatelas
from operation_utils import mots_operation_trouves
from matelas_utils import detecter_noyau_matelas
from hauteur_utils import calculer_hauteur_matelas
from fermete_utils import detecter_fermete_matelas
from housse_utils import detecter_type_housse
from matiere_housse_utils import detecter_matiere_housse
from poignees_utils import detecter_poignees
from dimensions_utils import detecter_dimensions
from latex_naturel_referentiel import get_valeur_latex_naturel
from latex_mixte7zones_referentiel import get_valeur_latex_mixte7zones
from mousse_rainuree7zones_referentiel import get_valeur_mousse_rainuree7zones
from select43_utils import get_select43_display_value
from select43_longueur_housse_utils import get_select43_longueur_housse_value
from latex_renforce_utils import get_latex_renforce_display_value
from latex_renforce_longueur_utils import get_latex_renforce_longueur_housse
from mousse_visco_utils import get_mousse_visco_display_value
from mousse_visco_longueur_utils import get_mousse_visco_longueur_value
from latex_naturel_longueur_housse_utils import get_latex_naturel_longueur_housse_value
from latex_mixte7zones_longueur_housse_utils import get_latex_mixte7zones_longueur_housse_value
from mousse_rainuree7zones_longueur_housse_utils import get_mousse_rainuree7zones_longueur_housse_value
from decoupe_noyau_utils import calcul_decoupe_noyau
from client_utils import extraire_donnees_client, valider_donnees_client
from pre_import_utils import creer_pre_import, valider_pre_import, formater_pre_import_pour_affichage
import math
import asyncio
import sys
import os

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import config
from llm_provider import llm_manager

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS pour usage interne local uniquement
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
UPLOAD_DIR = tempfile.gettempdir()

@app.get("/", response_class=HTMLResponse)
def index(request: Request, result: dict = None, error: str = None):
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
        # Extraction du texte
        try:
            logger.info("Ouverture PDF avec PyMuPDF")
            doc = fitz.open(temp_path)
            text = "\n".join(page.get_text() for page in doc)
            doc.close()
            logger.info(f"Extraction texte réussie - {len(text)} caractères")
            processing_steps["extraction"] = {
                "nb_caracteres": len(text),
                "nb_mots": len(text.split()),
                "preview": text[:500] + "..." if len(text) > 500 else text
            }
            processing_steps["progress"] = 50
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
                    llm_result = await call_llm(text)
                    logger.info(f"LLM appelé avec succès - réponse: {llm_result[:100]}...")
                    try:
                        llm_data = json.loads(llm_result)
                        processing_steps["llm"] = {
                            "model": "mistral:latest",
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
                            "model": "mistral:latest",
                            "raw_result": llm_result
                        }
                    processing_steps["progress"] = 100
                except Exception as e:
                    logger.error(f"Erreur LLM: {e}")
                    llm_result = f"Erreur LLM: {e}"
                    processing_steps["llm"] = {
                        "model": "mistral:latest",
                        "error": str(e)
                    }
            elif llm_provider == "openrouter":
                try:
                    if not openrouter_api_key:
                        raise Exception("Clé API OpenRouter manquante")
                    logger.info("Appel à OpenRouter avec GPT-4-Turbo")
                    llm_result = await call_openrouter(text, openrouter_api_key)
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
                            # Extraction des données client
                            donnees_client = extraire_donnees_client(llm_data)
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
                        for article in llm_data[key]:
                            description = article.get('description', '').upper()
                            logger.info(f"Article description pour {f.filename}: {description[:50]}...")
                            if 'MATELAS' in description:
                                matelas_articles.append(article)
                                logger.info(f"Matelas trouvé pour {f.filename}: {description[:50]}...")
                elif key == "paiement" and isinstance(llm_data[key], dict):
                    # Ajouter les conditions de paiement pour la recherche des mots opérationnels
                    conditions_paiement.append(llm_data[key])
                    logger.info(f"Conditions paiement ajoutées pour {f.filename}")
            logger.info(f"DEBUG articles_llm pour {f.filename}: {articles_llm}")
            logger.info(f"DEBUG matelas_articles pour {f.filename}: {matelas_articles}")
            logger.info(f"DEBUG conditions_paiement pour {f.filename}: {conditions_paiement}")
            contient_dosseret_tete = contient_dosseret_ou_tete(articles_llm)
            # Rechercher les mots opérationnels dans les articles ET les conditions de paiement
            mots_operation_list = mots_operation_trouves(articles_llm + conditions_paiement)
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
        for i, noyau_info in enumerate(noyaux_matelas):
            if noyau_info['noyau'] != 'INCONNU':
                # Trouver l'article correspondant pour récupérer la quantité et la description
                quantite = 1  # Valeur par défaut
                description = ""
                if noyau_info['index'] <= len(matelas_articles):
                    article_matelas = matelas_articles[noyau_info['index'] - 1]
                    quantite = article_matelas.get('quantite', 1)
                    description = article_matelas.get('description', '')
                
                dimensions_str = article_matelas.get('dimensions') if article_matelas else None
                if dimensions_str:
                    dimensions = detecter_dimensions(dimensions_str)
                else:
                    dimensions = detecter_dimensions(description)
                
                # Création de la configuration (une seule par noyau)
                config = {
                    "matelas_index": noyau_info['index'],
                    "noyau": noyau_info['noyau'],
                    "quantite": quantite,  # Garder la quantité originale
                    "hauteur": calculer_hauteur_matelas(noyau_info['noyau']),
                    "fermete": detecter_fermete_matelas(description),
                    "housse": detecter_type_housse(description),
                    "matiere_housse": detecter_matiere_housse(description),
                    "poignees": detecter_poignees(description),
                    "dimensions": dimensions,
                    "semaine_annee": semaine_annee,
                    "lundi": lundi,
                    "vendredi": vendredi,
                    "commande_client": cc_val
                }
                # Ajout de la dimension housse selon le noyau
                dimension_housse = None
                try:
                    if noyau_info['noyau'] == 'LATEX NATUREL' and config["dimensions"] and config["matiere_housse"] in get_valeur_latex_naturel.__globals__["MATIERE_MAP"]:
                        valeur = get_valeur_latex_naturel(config["dimensions"]["largeur"], config["matiere_housse"])
                        if config["matiere_housse"] == "POLYESTER":
                            dimension_housse = f"{valeur}"
                        else:
                            prefixe = "4 x " if quantite == 2 else ("2 x " if quantite == 1 else f"{quantite * 2} x ")
                            dimension_housse = f"{prefixe}{valeur}"
                        # Ajout de la dimension housse longueur (affichage simple, sans préfixe)
                        dimension_housse_longueur = get_latex_naturel_longueur_housse_value(config["dimensions"]["longueur"], config["matiere_housse"])
                        if dimension_housse_longueur is not None:
                            config["dimension_housse_longueur"] = dimension_housse_longueur
                    elif noyau_info['noyau'] == 'LATEX MIXTE 7 ZONES' and config["dimensions"] and config["matiere_housse"] in get_valeur_latex_mixte7zones.__globals__["MATIERE_MAP"]:
                        valeur = get_valeur_latex_mixte7zones(config["dimensions"]["largeur"], config["matiere_housse"])
                        if config["matiere_housse"] == "POLYESTER":
                            dimension_housse = f"{valeur}"
                        else:
                            prefixe = "4 x " if quantite == 2 else ("2 x " if quantite == 1 else f"{quantite * 2} x ")
                            dimension_housse = f"{prefixe}{valeur}"
                        # Ajout de la dimension housse longueur (affichage simple, sans préfixe)
                        dimension_housse_longueur = get_latex_mixte7zones_longueur_housse_value(config["dimensions"]["longueur"], config["matiere_housse"])
                        if dimension_housse_longueur is not None:
                            config["dimension_housse_longueur"] = dimension_housse_longueur
                    elif noyau_info['noyau'] == 'MOUSSE RAINUREE 7 ZONES' and config["dimensions"] and config["matiere_housse"] in get_valeur_mousse_rainuree7zones.__globals__["MATIERE_MAP"]:
                        valeur = get_valeur_mousse_rainuree7zones(config["dimensions"]["largeur"], config["matiere_housse"])
                        if config["matiere_housse"] == "POLYESTER":
                            dimension_housse = f"{valeur}"
                        else:
                            prefixe = "4 x " if quantite == 2 else ("2 x " if quantite == 1 else f"{quantite * 2} x ")
                            dimension_housse = f"{prefixe}{valeur}"
                        # Ajout de la dimension housse longueur (affichage simple, sans préfixe)
                        dimension_housse_longueur = get_mousse_rainuree7zones_longueur_housse_value(config["dimensions"]["longueur"], config["matiere_housse"])
                        if dimension_housse_longueur is not None:
                            config["dimension_housse_longueur"] = dimension_housse_longueur
                    elif noyau_info['noyau'] == 'SELECT 43' and config["dimensions"] and config["matiere_housse"]:
                        dimension_housse = get_select43_display_value(config["dimensions"]["largeur"], config["matiere_housse"], quantite)
                        # Ajout de la dimension housse longueur (affichage simple, sans préfixe)
                        dimension_housse_longueur = get_select43_longueur_housse_value(config["dimensions"]["longueur"], config["matiere_housse"])
                        if dimension_housse_longueur is not None:
                            config["dimension_housse_longueur"] = dimension_housse_longueur
                    elif noyau_info['noyau'] == 'LATEX RENFORCE' and config["dimensions"] and config["matiere_housse"]:
                        dimension_housse = get_latex_renforce_display_value(config["dimensions"]["largeur"], config["matiere_housse"], quantite)
                        # Ajout de la dimension housse longueur (affichage simple, sans préfixe)
                        dimension_housse_longueur = get_latex_renforce_longueur_housse(config["dimensions"]["longueur"], config["matiere_housse"])
                        if dimension_housse_longueur is not None:
                            config["dimension_housse_longueur"] = dimension_housse_longueur
                    elif noyau_info['noyau'] == 'MOUSSE VISCO' and config["dimensions"]:
                        dimension_housse = get_mousse_visco_longueur_value(config["dimensions"]["longueur"])
                        # Ajout de la dimension housse longueur
                        dimension_housse_longueur = get_mousse_visco_longueur_value(config["dimensions"]["longueur"])
                        if dimension_housse_longueur is not None:
                            config["dimension_housse_longueur"] = dimension_housse_longueur
                except Exception as e:
                    dimension_housse = f"Erreur: {e}"
                if dimension_housse:
                    config["dimension_housse"] = dimension_housse
                # Calcul de la dimension literie
                dimension_literie = None
                if dimensions:
                    largeur = dimensions["largeur"]
                    longueur = dimensions["longueur"]
                    largeur_arrondie = int(math.ceil(largeur / 10.0) * 10)
                    longueur_arrondie = int(math.ceil(longueur / 10.0) * 10)
                    if quantite == 2:
                        largeur_literie = largeur_arrondie * 2
                    else:
                        largeur_literie = largeur_arrondie
                    dimension_literie = f"{largeur_literie}x{longueur_arrondie}"
                    config["dimension_literie"] = dimension_literie
                    # Calcul découpe noyau
                    fermete = config.get("fermete", "")
                    largeur_decoupe, longueur_decoupe = calcul_decoupe_noyau(noyau_info['noyau'], fermete, largeur, longueur)
                    config["decoupe_noyau"] = f"{largeur_decoupe} x {longueur_decoupe}"
                configurations_matelas.append(config)
        
        # Étape de pré-import : création du JSON structuré pour l'import Excel
        pre_import_data = []
        if configurations_matelas and donnees_client:
            try:
                logger.info(f"Création du pré-import pour {f.filename}")
                # Récupération des mots d'opération depuis le résultat LLM
                # mots_operation_list est déjà défini plus haut
                if llm_result and "mots_operation_trouves" in llm_result:
                    mots_operation_list = llm_result["mots_operation_trouves"]
                
                pre_import_data = creer_pre_import(configurations_matelas, donnees_client, contient_dosseret_tete, mots_operation_list)
                logger.info(f"Pré-import créé avec succès: {len(pre_import_data)} éléments")
                
                # Validation du pré-import
                if valider_pre_import(pre_import_data):
                    logger.info("Pré-import validé avec succès")
                else:
                    logger.warning("Pré-import non valide")
                
                # === AJOUT EXPORT EXCEL ===
                try:
                    from excel_import_utils import ExcelMatelasImporter
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
                
            except Exception as e:
                logger.error(f"Erreur lors de la création du pré-import: {e}")
                pre_import_data = []
        
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

async def call_llm(text: str):
    """
    Appelle le LLM configuré par l'utilisateur
    """
    try:
        # Récupérer le provider actuel
        current_provider = config.get_current_llm_provider()
        
        # Si OpenRouter est sélectionné, utiliser l'ancienne méthode
        if current_provider == "openrouter":
            return await call_openrouter(text, config.get_llm_api_key(current_provider))
        
        # Sinon, utiliser le nouveau système de providers
        # Pour Ollama, pas besoin de clé API
        if current_provider == "ollama":
            api_key = None  # Ollama ne nécessite pas de clé API
        else:
            api_key = config.get_llm_api_key(current_provider)
            if not api_key:
                logger.error(f"Aucune clé API configurée pour {current_provider}")
                return f"Erreur: Clé API manquante pour {current_provider}"
        
        # Prompt pour tous les providers (même que OpenRouter)
        prompt = f"""Tu es un assistant expert en extraction de données structurées à partir de documents PDF commerciaux.

Analyse le texte suivant : 

{text}

Extrais uniquement les informations sous forme de **JSON**.  
Respecte exactement cette structure :

{{
  "societe": {{
    "nom": "...",
    "capital": "...",
    "adresse": "...",
    "telephone": "...",
    "fax": "...",
    "email": "...",
    "siret": "...",
    "APE": "...",
    "CEE": "...",
    "banque": "...",
    "IBAN": "..."
  }},
  "client": {{
    "nom": "...",
    "adresse": "...",
    "code_client": "..."
  }},
  "commande": {{
    "numero": "...",
    "date": "...",
    "date_validite": "...",
    "commercial": "...",
    "origine": "..."
  }},
  "articles": [
    {{
      "quantite": ...,
      "description": "...",
      "dimensions": "...",
      "pu_ttc": ...,
      "eco_part": ...,
      "pu_ht": ...
    }},
    {{
      "quantite": ...,
      "description": "...",
      "montant": ...
    }}
  ],
  "paiement": {{
    "conditions": "...",
    "port_ht": ...,
    "base_ht": ...,
    "taux_tva": ...,
    "total_ttc": ...,
    "acompte": ...,
    "net_a_payer": ...
  }}
}}

N'invente aucune donnée manquante, laisse la valeur `null` si tu ne la trouves pas.  
Réponds uniquement avec le JSON valide, sans explication ni phrase autour."""
        
        # Configurer le provider
        llm_manager.set_provider(current_provider, api_key)
        
        # Appeler le LLM
        logger.info(f"Appel LLM avec provider: {current_provider}")
        result = llm_manager.call_llm(prompt, temperature=0.1, max_tokens=2000)
        
        if result["success"]:
            return result["content"]
        else:
            logger.error(f"Erreur LLM {current_provider}: {result.get('error', 'Erreur inconnue')}")
            return f"Erreur LLM {current_provider}: {result.get('error', 'Erreur inconnue')}"
            
    except Exception as e:
        logger.error(f"Erreur lors de l'appel LLM: {e}")
        return f"Erreur lors de l'appel LLM: {str(e)}"

async def call_openrouter(text: str, api_key: str) -> str:
    """Appelle OpenRouter avec GPT-4-Turbo"""
    # Nettoyer la clé API (supprimer espaces et retours à la ligne)
    api_key = api_key.strip()
    
    prompt = f"""Tu es un assistant expert en extraction de données structurées à partir de documents PDF commerciaux.

Analyse le texte suivant : 

{text}

Extrais uniquement les informations sous forme de **JSON**.  
Respecte exactement cette structure :

{{
  "societe": {{
    "nom": "...",
    "capital": "...",
    "adresse": "...",
    "telephone": "...",
    "fax": "...",
    "email": "...",
    "siret": "...",
    "APE": "...",
    "CEE": "...",
    "banque": "...",
    "IBAN": "..."
  }},
  "client": {{
    "nom": "...",
    "adresse": "...",
    "code_client": "..."
  }},
  "commande": {{
    "numero": "...",
    "date": "...",
    "date_validite": "...",
    "commercial": "...",
    "origine": "..."
  }},
  "articles": [
    {{
      "quantite": ...,
      "description": "...",
      "dimensions": "...",
      "pu_ttc": ...,
      "eco_part": ...,
      "pu_ht": ...
    }},
    {{
      "quantite": ...,
      "description": "...",
      "montant": ...
    }}
  ],
  "paiement": {{
    "conditions": "...",
    "port_ht": ...,
    "base_ht": ...,
    "taux_tva": ...,
    "total_ttc": ...,
    "acompte": ...,
    "net_a_payer": ...
  }}
}}

N'invente aucune donnée manquante, laisse la valeur `null` si tu ne la trouves pas.  
Réponds uniquement avec le JSON valide, sans explication ni phrase autour."""

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-4-turbo",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.1,
                    "max_tokens": 2000
                }
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"Erreur appel OpenRouter: {e}")
        raise e

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 