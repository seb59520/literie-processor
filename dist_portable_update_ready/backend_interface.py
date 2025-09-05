
#!/usr/bin/env python3
"""
Interface entre l'application GUI et le backend existant
"""

import os
import sys
import json
import tempfile
import shutil
import logging
from typing import List, Dict, Optional
from pathlib import Path
import time

# Ajout du dossier backend au path (commenté pour PyInstaller)
# sys.path.append('backend')

# Import des modules backend
from backend.date_utils import get_week_dates
from backend.pre_import_utils import creer_pre_import, valider_pre_import
from backend.main import call_llm
from backend.excel_import_utils import ExcelMatelasImporter
from backend.file_validation import FileValidator, validate_pdf_file
import sys
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # Commenté pour PyInstaller
from config import config
from backend.sommier_utils import segmenter_pieds_sommier


class BackendInterface:
    """Interface pour intégrer le backend existant avec l'interface graphique"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.file_validator = FileValidator({
            'max_file_size_mb': 100,  # Augmenté pour les gros devis
            'min_file_size_kb': 1,    # Minimum 1 KB
            'max_pages': 200,
            'min_text_length': 50,
            'max_text_length': 1000000,
            'allowed_extensions': ['.pdf'],
            'allowed_mime_types': [
                'application/pdf',
                'application/x-pdf', 
                'text/pdf'
            ]
        })
    
    def _split_large_command(self, text: str, max_chars_per_part: int = 15000) -> List[str]:
        """
        Divise une commande volumineuse en plusieurs parties
        
        Args:
            text: Texte complet de la commande
            max_chars_per_part: Nombre maximum de caractères par partie
            
        Returns:
            Liste des parties de la commande
        """
        if len(text) <= max_chars_per_part:
            return [text]
        
        self.logger.info(f"Commande trop volumineuse ({len(text)} caractères), division en parties...")
        
        parts = []
        current_part = ""
        lines = text.split('\n')
        
        for line in lines:
            # Si ajouter cette ligne dépasserait la limite
            if len(current_part) + len(line) + 1 > max_chars_per_part and current_part:
                parts.append(current_part.strip())
                current_part = line
            else:
                if current_part:
                    current_part += '\n' + line
                else:
                    current_part = line
        
        # Ajouter la dernière partie
        if current_part.strip():
            parts.append(current_part.strip())
        
        self.logger.info(f"Commande divisée en {len(parts)} parties")
        return parts
    
    def _merge_llm_results(self, results: List[str]) -> str:
        """
        Fusionne les résultats LLM de plusieurs parties en un seul JSON
        
        Args:
            results: Liste des résultats JSON de chaque partie
            
        Returns:
            JSON fusionné
        """
        if not results:
            return ""
        
        if len(results) == 1:
            return results[0]
        
        self.logger.info(f"Fusion de {len(results)} résultats LLM...")
        
        # Essayer de parser chaque résultat
        parsed_results = []
        for i, result in enumerate(results):
            try:
                parsed = json.loads(result)
                parsed_results.append(parsed)
                self.logger.info(f"Partie {i+1} parsée avec succès")
            except json.JSONDecodeError as e:
                self.logger.warning(f"Erreur parsing partie {i+1}: {e}")
                # Essayer de nettoyer et reparser
                try:
                    cleaned = self._clean_and_parse_json(result)
                    parsed = json.loads(cleaned)
                    parsed_results.append(parsed)
                    self.logger.info(f"Partie {i+1} parsée après nettoyage")
                except:
                    self.logger.error(f"Impossible de parser la partie {i+1}")
        
        if not parsed_results:
            return ""
        
        # Fusionner les résultats
        merged = parsed_results[0].copy()
        
        # Fusionner les articles
        for result in parsed_results[1:]:
            if 'articles' in result and result['articles']:
                if 'articles' not in merged:
                    merged['articles'] = []
                merged['articles'].extend(result['articles'])
        
        # Fusionner les autres champs si nécessaire
        for result in parsed_results[1:]:
            for key, value in result.items():
                if key != 'articles' and key not in merged:
                    merged[key] = value
        
        return json.dumps(merged, ensure_ascii=False, indent=2)
        
    async def process_pdf_files(self, files: List[str], enrich_llm: bool, llm_provider: str, 
                         openrouter_api_key: Optional[str], semaine_prod: int, 
                         annee_prod: int, commande_client: List[str],
                         semaine_matelas: Optional[int] = None, annee_matelas: Optional[int] = None,
                         semaine_sommiers: Optional[int] = None, annee_sommiers: Optional[int] = None,
                         exclusions: Optional[Dict] = None,
                         progress_callback=None) -> Dict:
        """
        Traite les fichiers PDF en utilisant la logique backend existante avec validation préalable
        
        Args:
            files: Liste des chemins vers les fichiers PDF
            enrich_llm: Si True, utilise l'enrichissement LLM
            llm_provider: Provider LLM ('ollama' ou 'openrouter')
            openrouter_api_key: Clé API pour OpenRouter
            semaine_prod: Numéro de semaine de production
            annee_prod: Année de production
            commande_client: Liste des noms de clients
            
        Returns:
            Dict contenant les résultats du traitement
        """
        start_time = time.time()
        results = []
        
        # Étape 1: Validation préalable de tous les fichiers
        self.logger.info(f"Validation de {len(files)} fichiers...")
        validation_results = self.file_validator.validate_multiple_files(files)
        validation_summary = self.file_validator.get_validation_summary(validation_results)
        
        self.logger.info(
            f"Validation terminée: {validation_summary['valid_files']}/{validation_summary['total_files']} "
            f"fichiers valides ({validation_summary['total_size_mb']:.1f} MB total)"
        )
        
        # Filtrer les fichiers invalides
        valid_files = []
        validation_errors = []
        
        for file_path, validation_result in zip(files, validation_results):
            if validation_result.is_valid:
                valid_files.append(file_path)
                self.logger.debug(f"✓ Fichier valide: {file_path} ({validation_result.file_size_mb:.1f} MB)")
            else:
                error_msg = f"Fichier invalide {file_path}: {'; '.join(validation_result.errors)}"
                validation_errors.append(error_msg)
                self.logger.warning(f"✗ {error_msg}")
                
                # Ajouter le résultat d'erreur
                results.append({
                    'file': file_path,
                    'success': False,
                    'error': f"Validation échouée: {'; '.join(validation_result.errors)}",
                    'validation_result': validation_result
                })
        
        if not valid_files:
            return {
                'results': results,
                'validation_summary': validation_summary,
                'total_processing_time': time.time() - start_time,
                'success': False,
                'error': 'Aucun fichier valide à traiter'
            }
        
        self.logger.info(f"Traitement de {len(valid_files)} fichiers valides...")
        errors = []
        
        # Collecte globale de toutes les configurations et pré-imports
        all_configurations = []
        all_pre_imports = []
        
        total_files = len(files)
        
        for idx, file_path in enumerate(files):
            try:
                # Callback de progression avec détails du fichier
                if progress_callback:
                    filename = os.path.basename(file_path)
                    progress_info = {
                        'current_file': idx + 1,
                        'total_files': total_files,
                        'filename': filename,
                        'message': f"Traitement du fichier {filename} ({idx + 1}/{total_files})"
                    }
                    progress_callback(progress_info)
                # Utiliser un répertoire temporaire local
                if hasattr(sys, '_MEIPASS'):  # PyInstaller
                    base_dir = os.path.dirname(sys.executable)
                else:
                    base_dir = os.path.dirname(__file__)
                temp_dir = os.path.join(base_dir, "temp_processing")
                os.makedirs(temp_dir, exist_ok=True)
                temp_file_path = os.path.join(temp_dir, os.path.basename(file_path))
                
                # Copie du fichier vers le répertoire temporaire
                shutil.copy2(file_path, temp_file_path)
                
                # Simulation des paramètres de l'interface web
                file_info = {
                    'filename': os.path.basename(file_path),
                    'file_path': temp_file_path
                }
                
                # Récupérer les informations d'exclusion pour ce fichier
                file_exclusions = {}
                if exclusions:
                    # Debug : vérifier les clés d'exclusion vs le file_path
                    self.logger.info(f"DEBUG - File path: '{file_path}'")
                    self.logger.info(f"DEBUG - Exclusion keys: {list(exclusions.keys())}")
                    
                    if file_path in exclusions:
                        file_exclusions = exclusions[file_path]
                    else:
                        # Essayer de matcher par nom de fichier seulement
                        basename = os.path.basename(file_path)
                        for key, exc_data in exclusions.items():
                            if os.path.basename(key) == basename:
                                file_exclusions = exc_data
                                self.logger.info(f"DEBUG - Matched exclusion by basename: {basename}")
                                break
                
                # Log des exclusions appliquées
                if file_exclusions:
                    self.logger.info(f"DEBUG - Exclusions appliquées à {os.path.basename(file_path)}: {file_exclusions}")
                
                # Appel de la logique backend existante
                result = await self._process_single_file(
                    file_info, enrich_llm, llm_provider, openrouter_api_key,
                    semaine_prod, annee_prod, commande_client[idx] if idx < len(commande_client) else "",
                    semaine_matelas=semaine_matelas, annee_matelas=annee_matelas,
                    semaine_sommiers=semaine_sommiers, annee_sommiers=annee_sommiers,
                    exclusions=file_exclusions
                )
                
                # Collecte des configurations et pré-imports pour l'export global
                if result['status'] == 'success':
                    if 'configurations_matelas' in result and result['configurations_matelas']:
                        all_configurations.extend(result['configurations_matelas'])
                    if 'pre_import' in result and result['pre_import']:
                        all_pre_imports.extend(result['pre_import'])
                
                results.append(result)
                
                # Nettoyage
                os.remove(temp_file_path)
                os.rmdir(temp_dir)
                
            except Exception as e:
                error_msg = f"Erreur lors du traitement de {os.path.basename(file_path)}: {str(e)}"
                self.logger.error(error_msg)
                errors.append(error_msg)
        
        # Export Excel global avec tri des configurations
        fichiers_excel = []
        if all_pre_imports:
            try:
                fichiers_excel = self._export_excel_global(
                    all_pre_imports, semaine_prod, annee_prod,
                    semaine_matelas=semaine_matelas, annee_matelas=annee_matelas,
                    semaine_sommiers=semaine_sommiers, annee_sommiers=annee_sommiers
                )
                self.logger.info(f"Export Excel global terminé: {fichiers_excel}")
            except Exception as e:
                self.logger.error(f"Erreur lors de l'export Excel global: {e}")
                fichiers_excel = []
        
        # Ajouter les fichiers Excel à chaque résultat individuel pour compatibilité avec l'interface GUI
        for result in results:
            if result['status'] == 'success':
                result['fichiers_excel'] = fichiers_excel
        
        # Retour du résultat consolidé
        return {
            'results': results,
            'errors': errors,
            'total_files': len(files),
            'successful_files': len(results),
            'failed_files': len(errors),
            'fichiers_excel': fichiers_excel,
            'total_configurations': len(all_configurations),
            'total_pre_imports': len(all_pre_imports)
        }
    
    async def _process_single_file(self, file_info: Dict, enrich_llm: bool, llm_provider: str,
                           openrouter_api_key: Optional[str], semaine_prod: int,
                           annee_prod: int, commande_client: str,
                           semaine_matelas: Optional[int] = None, annee_matelas: Optional[int] = None,
                           semaine_sommiers: Optional[int] = None, annee_sommiers: Optional[int] = None,
                           exclusions: Optional[Dict] = None) -> Dict:
        """
        Traite un seul fichier PDF
        """
        try:
            # Extraction du texte du PDF
            import fitz  # PyMuPDF
            doc = fitz.open(file_info['file_path'])
            text = "\n".join(page.get_text() for page in doc)
            doc.close()
            
            # Appel LLM si activé
            llm_result = None
            if enrich_llm:
                # Démarrer une session de tracking pour ce fichier
                from backend.cost_tracker import cost_tracker
                file_path = file_info['file_path']
                file_size = os.path.getsize(file_path) if os.path.exists(file_path) else len(text)
                session_id = cost_tracker.start_session(
                    file_name=os.path.basename(file_path),
                    file_path=file_path,
                    file_size=file_size
                )
                
                if llm_provider == "ollama":
                    try:
                        # Déporter l'appel (bloquant) sur un thread dédié
                        import asyncio
                        llm_result = await asyncio.to_thread(lambda: asyncio.run(
                            call_llm(text, file_name=os.path.basename(file_path), file_size=file_size, session_id=session_id)
                        ))
                    except Exception as e:
                        self.logger.warning(f"Erreur LLM Ollama: {e}")
                        llm_result = None
                elif llm_provider == "openrouter":
                    if openrouter_api_key:
                        try:
                            import asyncio
                            llm_result = await asyncio.to_thread(lambda: asyncio.run(
                                call_llm(text, file_name=os.path.basename(file_path), file_size=file_size, session_id=session_id)
                            ))
                        except Exception as e:
                            self.logger.warning(f"Erreur LLM OpenRouter: {e}")
                            llm_result = None
                elif llm_provider == "openai":
                    try:
                        # Récupérer la clé API OpenAI depuis la configuration
                        from config import config
                        openai_api_key = config.get_llm_api_key("openai")
                        if not openai_api_key:
                            # Fallback sur la clé OpenRouter si pas de clé OpenAI spécifique
                            openai_api_key = openrouter_api_key
                        
                        if not openai_api_key:
                            raise ValueError("Aucune clé API OpenAI configurée")
                        
                        # Utiliser le LLM manager pour OpenAI
                        from backend.llm_provider import LLMProviderManager
                        _llm_manager = LLMProviderManager()
                        _llm_manager.set_provider("openai", openai_api_key)
                        
                        # Traitement simple en une fois avec limite raisonnable, déporté en thread
                        import asyncio
                        prompt = self._create_analysis_prompt(text)
                        result = await asyncio.to_thread(lambda: _llm_manager.call_llm(prompt, temperature=0.1, max_tokens=8000))
                        
                        if result["success"]:
                            llm_result = result["content"]
                        else:
                            self.logger.warning(f"Erreur LLM OpenAI: {result.get('error', 'Erreur inconnue')}")
                            llm_result = None
                            
                    except Exception as e:
                        self.logger.warning(f"Erreur LLM OpenAI: {e}")
                        llm_result = None
            
            # Initialisation des variables en dehors du bloc conditionnel
            articles_llm = []
            matelas_articles = []
            sommier_articles = []
            pieds_articles = []
            configurations_matelas = []
            configurations_sommiers = []
            donnees_client = {}
            pre_import_data = []
            
            if llm_result:
                # Parsing du JSON LLM
                cleaned_llm_result = self._clean_and_parse_json(llm_result)
                if cleaned_llm_result:
                    try:
                        llm_data = json.loads(cleaned_llm_result)
                        
                        # Extraction des données client
                        from backend.client_utils import extraire_donnees_client
                        donnees_client = extraire_donnees_client(llm_data)
                        
                        # Extraction des articles
                        for key in llm_data:
                            if isinstance(llm_data[key], list):
                                articles_llm.extend(llm_data[key])
                                if key.lower() == "articles":
                                    for article in llm_data[key]:
                                        description = article.get('description', '').upper()
                                        if 'MATELAS' in description:
                                            matelas_articles.append(article)
                                        elif 'SOMMIER' in description:
                                            sommier_articles.append(article)
                                        elif 'PIEDS' in description:
                                            pieds_articles.append(article)
                        
                        # Détection des noyaux matelas
                        from backend.matelas_utils import detecter_noyau_matelas
                        noyaux_matelas = detecter_noyau_matelas(matelas_articles)
                        
                        # Détection des types sommiers
                        from backend.sommier_utils import detecter_type_sommier
                        types_sommiers = detecter_type_sommier(sommier_articles)
                        
                        # Utiliser les semaines de production séparées si disponibles
                        semaine_matelas_prod = semaine_matelas or semaine_prod
                        annee_matelas_prod = annee_matelas or annee_prod
                        semaine_sommiers_prod = semaine_sommiers or semaine_prod
                        annee_sommiers_prod = annee_sommiers or annee_prod
                        
                        # Auto-exclusion des matelas si matelas + sommiers détectés
                        if matelas_articles and sommier_articles:
                            if not exclusions:
                                exclusions = {}
                            # Exclure automatiquement les matelas par défaut
                            if 'matelas_excluded' not in exclusions:
                                exclusions['matelas_excluded'] = True
                                self.logger.info(f"Auto-exclusion matelas activée pour {file_info['filename']} (matelas + sommiers détectés)")
                        
                        # Vérifier les exclusions avant de créer les configurations
                        create_matelas = True
                        create_sommiers = True
                        exclusion_messages = []
                        
                        if exclusions:
                            if exclusions.get('matelas_excluded', False):
                                create_matelas = False
                                exclusion_messages.append(f"Matelas exclus du traitement pour {file_info['filename']}")
                                self.logger.info(f"Exclusion matelas activée pour {file_info['filename']}")
                            
                            if exclusions.get('sommier_excluded', False):
                                create_sommiers = False  
                                exclusion_messages.append(f"Sommiers exclus du traitement pour {file_info['filename']}")
                                self.logger.info(f"Exclusion sommier activée pour {file_info['filename']}")
                        
                        # Création des configurations matelas (seulement si non exclus)
                        configurations_matelas = self._create_configurations_matelas(
                            noyaux_matelas, matelas_articles, semaine_matelas_prod, annee_matelas_prod, commande_client
                        ) if create_matelas else []
                        
                        # Création des configurations sommiers (seulement si non exclus)
                        configurations_sommiers = self._create_configurations_sommiers(
                            types_sommiers, sommier_articles, semaine_sommiers_prod, annee_sommiers_prod, commande_client
                        ) if create_sommiers else []
                        
                        # Log de débogage pour les exclusions
                        self.logger.info(f"DEBUG Exclusion pour {file_info['filename']}: matelas={len(configurations_matelas)}, sommiers={len(configurations_sommiers)}")
                        if exclusions:
                            self.logger.info(f"DEBUG Exclusions demandées: {exclusions}")
                        
                        # Création du pré-import
                        if (configurations_matelas or configurations_sommiers) and donnees_client:
                            import sys
                            
                            # Ajouter le répertoire backend au path
                            script_dir = os.path.dirname(os.path.abspath(__file__))
                            backend_dir = os.path.join(script_dir, "backend")
                            if backend_dir not in sys.path:
                                sys.path.insert(0, backend_dir)
                            
                            from backend.article_utils import contient_dosseret_ou_tete, contient_fermeture_liaison
                            from backend.operation_utils import mots_operation_trouves
                            
                            contient_dosseret_tete = contient_dosseret_ou_tete(articles_llm)
                            mots_operation_list = mots_operation_trouves(articles_llm, text)
                            fermeture_liaison = contient_fermeture_liaison(articles_llm)
                            
                            # Créer le pré-import pour les matelas
                            pre_import_data_matelas = creer_pre_import(
                                configurations_matelas, donnees_client, 
                                contient_dosseret_tete, mots_operation_list, fermeture_liaison
                            ) if configurations_matelas else []
                            
                            # Créer le pré-import pour les sommiers
                            pre_import_data_sommiers = self._creer_pre_import_sommiers(
                                configurations_sommiers, donnees_client, 
                                contient_dosseret_tete, mots_operation_list
                            ) if configurations_sommiers else []
                            
                            # Combiner les deux pré-imports
                            pre_import_data = pre_import_data_matelas + pre_import_data_sommiers
                            
                            # Log de débogage pour les pré-imports
                            self.logger.info(f"DEBUG Pré-import pour {file_info['filename']}: matelas={len(pre_import_data_matelas)}, sommiers={len(pre_import_data_sommiers)}, total={len(pre_import_data)}")
                            
                            # Note: L'export Excel sera fait globalement après traitement de tous les fichiers
                            fichiers_excel = []
                        
                    except json.JSONDecodeError as e:
                        self.logger.warning(f"Erreur parsing JSON LLM: {e}")
            
            # Détection des pieds indépendants
            from backend.sommier_utils import segmenter_pieds_sommier
            configurations_pieds = []
            for article in pieds_articles:
                pied = segmenter_pieds_sommier(article.get('description', ''), quantite_article=article.get('quantite', 1))
                pied['article_index'] = articles_llm.index(article) + 1 if article in articles_llm else None
                configurations_pieds.append(pied)
            
            # Terminer la session de tracking si elle était démarrée
            if enrich_llm and 'session_id' in locals():
                try:
                    cost_tracker.end_session(session_id, success=True)
                    self.logger.info(f"Session de coût terminée: {session_id}")
                except Exception as e:
                    self.logger.warning(f"Erreur fin de session coût: {e}")
            
            # Calcul des dates
            semaine_annee = f"{semaine_prod}_{annee_prod}"
            lundi, vendredi = get_week_dates(semaine_prod, annee_prod)
            
            return {
                'filename': file_info['filename'],
                'status': 'success',
                'extraction_stats': {
                    'nb_caracteres': len(text),
                    'nb_mots': len(text.split()),
                    'preview': text[:500] + "..." if len(text) > 500 else text
                },
                'texte_extrait': text,
                'llm_result': llm_result,
                'configurations_matelas': configurations_matelas,
                'configurations_sommiers': configurations_sommiers,
                'configurations_pieds': configurations_pieds,
                'donnees_client': donnees_client,
                'pre_import': pre_import_data,
                'exclusion_messages': exclusion_messages if 'exclusion_messages' in locals() else [],
                'calcul_date': {
                    'semaine_annee': semaine_annee,
                    'lundi': lundi,
                    'vendredi': vendredi,
                    'commande_client': commande_client
                }
            }
            
        except Exception as e:
            self.logger.error(f"Erreur lors du traitement: {e}")
            return {
                'filename': file_info['filename'],
                'status': 'error',
                'error': str(e)
            }
    
    def _create_analysis_prompt(self, text: str, is_part: bool = False, part_number: int = 1, total_parts: int = 1) -> str:
        """
        Crée le prompt d'analyse pour l'IA
        
        Args:
            text: Texte à analyser
            is_part: Si True, c'est une partie d'une commande divisée
            part_number: Numéro de la partie (1, 2, 3...)
            total_parts: Nombre total de parties
        """
        part_info = ""
        if is_part:
            part_info = f"""

⚠️ ATTENTION : Ceci est la PARTIE {part_number}/{total_parts} d'une commande volumineuse.
- Analyse uniquement cette partie du document
- Extrais tous les articles présents dans cette partie
- Les informations de société, client et commande peuvent être répétées dans chaque partie
- Concentre-toi sur l'extraction des articles de cette section spécifique

"""
        
        return f"""Tu es un assistant expert en extraction de données structurées à partir de documents PDF commerciaux.{part_info}

Analyse le texte suivant : 

{text}

⚠️ INSTRUCTIONS CRITIQUES POUR LES MATELAS :
- Pour chaque matelas, tu dois extraire la description COMPLÈTE incluant TOUTES les informations (noyau, fermeté, housse, matière, poignées, caractéristiques spéciales...)
- NE TRONQUE JAMAIS la description d'un matelas !
- Si la description s'étend sur plusieurs lignes, combine-les en une seule description complète.
- Exemple de description complète : "MATELAS 1 PIÈCE - MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES FERME (50KG/ M3) - HOUSSE MATELASSÉE TENCEL LUXE 3D AVEC POIGNÉES INTÉGRÉES DÉHOUSSABLE SUR 3 CÔTÉS ET LAVABLE A 40°"

⚠️ INSTRUCTIONS CRITIQUES POUR LA DÉTECTION DES JUMEAUX :
- Tu dois DÉTECTER et EXTRACTER TOUS les types de matelas (jumeaux vs 1 pièce)
- Recherche spécifiquement les mots-clés suivants :
  * "jumeaux", "MATELAS JUMEAUX", "2 PIÈCES", "DEUX PIÈCES"
  * "1 PIÈCE", "UNE PIÈCE", "SIMPLE"
- Si tu trouves "jumeaux" ou "2 PIÈCES" → marquer comme jumeaux
- Si tu trouves "1 PIÈCE" ou rien de spécifique → marquer comme 1 pièce
- IMPORTANT : La détection des jumeaux est CRUCIALE pour le calcul des dimensions housse !

⚠️ INSTRUCTIONS CRITIQUES POUR LA LIVRAISON :
- Tu dois DÉTECTER et EXTRACTER TOUS les modes de livraison mentionnés dans le document
- Recherche spécifiquement les mots-clés suivants :
  * "fourgon", "livraison par fourgon", "fourgon de l'entreprise"
  * "enlèvement", "retrait", "enlèvement par vos soins"
  * "transporteur", "livraison par transporteur"
  * "livraison", "mode de livraison", "transport"
- Si tu trouves des informations de livraison, remplis les champs appropriés
- Si aucune information n'est trouvée, mets "Non spécifié" ou laisse vide

Pour chaque ligne d'article, même si elle est similaire ou dupliquée, crée une entrée distincte dans le tableau "articles".
Inclue aussi toutes les lignes de remise, réduction ou montant négatif, même si elles ne ressemblent pas à un article classique.
Ne fusionne jamais deux lignes, même si elles semblent identiques.

⚠️ IMPORTANT : Tu dois répondre UNIQUEMENT avec du JSON valide, sans texte avant ou après.
Extrais les informations sous forme de **JSON**.  
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
  "mode_mise_a_disposition": {{
    "emporte_client_C57": "X si enlèvement client, null sinon",
    "fourgon_C58": "X si livraison fourgon/sur site, null sinon",
    "transporteur_C59": "X si transporteur externe, null sinon"
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

EXEMPLES DE DÉTECTION DE JUMEAUX :

Exemple 1 - Matelas Jumeaux :
"MATELAS JUMEAUX - MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES FERME (50KG/ M3) - HOUSSE MATELASSÉE TENCEL LUXE 3D AVEC POIGNÉES INTÉGRÉES DÉHOUSSABLE SUR 3 CÔTÉS ET LAVABLE A 40° 139/ 189/ 20"
→ type_matelas: "jumeaux", est_jumeaux: true

Exemple 2 - Matelas 1 Pièce :
"MATELAS 1 PIÈCE - MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES FERME (50KG/ M3) - HOUSSE MATELASSÉE TENCEL LUXE 3D AVEC POIGNÉES INTÉGRÉES DÉHOUSSABLE SUR 3 CÔTÉS ET LAVABLE A 40° 139/ 189/ 20"
→ type_matelas: "1_piece", est_jumeaux: false

Exemple 3 - Matelas Simple (sans précision) :
"MATELAS - MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES FERME (50KG/ M3) - HOUSSE MATELASSÉE TENCEL LUXE 3D AVEC POIGNÉES INTÉGRÉES DÉHOUSSABLE SUR 3 CÔTÉS ET LAVABLE A 40° 139/ 189/ 20"
→ type_matelas: "1_piece", est_jumeaux: false

EXEMPLES DE DÉTECTION DE LIVRAISON :

Exemple 1 - Fourgon :
"Livraison par fourgon de l'entreprise" → fourgon_C58: "X"

Exemple 2 - Enlèvement :
"5% enlèvement par vos soins" → emporte_client_C57: "X"

Exemple 3 - Transporteur :
"Livraison par transporteur" → transporteur_C59: "X"

Exemple 4 - Livraison sur site :
"LIVRAISON ET INSTALLATION OFFERTES AU CAMPING" → fourgon_C58: "X"

Exemple 5 - Aucune info :
Si rien n'est mentionné → fourgon_C58: null

⚠️ RÈGLES FINALES :
1. Sois TRÈS ATTENTIF à la détection des jumeaux - c'est CRUCIAL pour les calculs !
2. Sois TRÈS ATTENTIF aux informations de livraison et remplis TOUS les champs que tu peux identifier !

N'invente aucune donnée manquante, laisse la valeur `null` si tu ne la trouves pas.  
Réponds uniquement avec le JSON valide, sans explication ni phrase autour."""
    
    def _create_configurations_matelas(self, noyaux_matelas: List[Dict], matelas_articles: List[Dict],
                             semaine_prod: int, annee_prod: int, commande_client: str) -> List[Dict]:
        """
        Crée les configurations matelas à partir des noyaux détectés
        Crée une configuration séparée pour chaque unité de quantité
        """
        configurations = []
        config_index = 1  # Index pour les configurations
        
        for i, noyau_info in enumerate(noyaux_matelas):
            if noyau_info['noyau'] != 'INCONNU':
                # Trouver l'article correspondant
                quantite = 1
                description = ""
                if noyau_info['index'] <= len(matelas_articles):
                    article_matelas = matelas_articles[noyau_info['index'] - 1]
                    quantite = article_matelas.get('quantite', 1)
                    description = article_matelas.get('description', '')
                
                # Détection des dimensions
                import sys
                
                # Ajouter le répertoire backend au path
                script_dir = os.path.dirname(os.path.abspath(__file__))
                backend_dir = os.path.join(script_dir, "backend")
                if backend_dir not in sys.path:
                    sys.path.insert(0, backend_dir)
                
                from backend.dimensions_utils import detecter_dimensions
                dimensions_str = article_matelas.get('dimensions') if article_matelas else None
                if dimensions_str:
                    dimensions = detecter_dimensions(dimensions_str)
                else:
                    dimensions = detecter_dimensions(description)
                
                # CRÉATION D'UNE CONFIGURATION PAR LIGNE MATELAS
                # Si quantité = 2 et mot "jumeaux" présent = 1 configuration avec quantité = 2
                # Sinon, créer une configuration par unité de quantité
                
                # Détecter si c'est des jumeaux (priorité aux champs LLM, fallback sur la description)
                is_jumeaux = False
                if article_matelas:
                    # Vérifier d'abord les champs LLM spécifiques
                    if article_matelas.get('est_jumeaux') is True:
                        is_jumeaux = True
                    elif article_matelas.get('type_matelas') == 'jumeaux':
                        is_jumeaux = True
                    # Fallback sur la détection dans la description
                    elif "jumeaux" in description.lower():
                        is_jumeaux = True
                
                # Convertir quantite en float pour la comparaison
                quantite_float = float(quantite) if isinstance(quantite, (int, float, str)) else 1.0
                
                if is_jumeaux and quantite_float > 1:
                    # Cas des jumeaux : 1 configuration avec la quantité totale
                    config = {
                        "matelas_index": config_index,  # Index unique pour chaque configuration
                        "noyau": noyau_info['noyau'],
                        "quantite": quantite_float,  # Garder la quantité totale pour les jumeaux
                        "hauteur": self._calculer_hauteur_matelas(noyau_info['noyau']),
                        "fermete": self._detecter_fermete_matelas(description),
                        "housse": self._detecter_type_housse(description),
                        "matiere_housse": self._detecter_matiere_housse(description),
                        "poignees": self._detecter_poignees(description),
                        "dimensions": dimensions,
                        "semaine_annee": f"{semaine_prod}_{annee_prod}",
                        "lundi": get_week_dates(semaine_prod, annee_prod)[0],
                        "vendredi": get_week_dates(semaine_prod, annee_prod)[1],
                        "commande_client": commande_client
                    }
                    
                    # Ajouter titre_cote depuis l'article LLM si disponible
                    if article_matelas and 'titre_cote' in article_matelas and article_matelas['titre_cote']:
                        config["titre_cote"] = article_matelas['titre_cote']
                        self.logger.info(f"DEBUG BACKEND_INTERFACE: Config jumeaux {config_index} - titre_cote copié: '{config['titre_cote']}'")
                    else:
                        self.logger.info(f"DEBUG BACKEND_INTERFACE: Config jumeaux {config_index} - titre_cote absent ou vide")
                    
                    # Ajout des dimensions housse et autres calculs
                    self._ajouter_dimensions_housse(config)
                    # Le calcul de dimension literie est maintenant fait dans _ajouter_dimensions_housse
                    
                    configurations.append(config)
                    config_index += 1
                else:
                    # Cas normal : créer une configuration par unité de quantité
                    # Convertir quantite en entier pour éviter l'erreur 'float' object cannot be interpreted as an integer
                    quantite_int = int(quantite) if isinstance(quantite, (int, float)) else 1
                    for q in range(quantite_int):
                        config = {
                            "matelas_index": config_index,  # Index unique pour chaque configuration
                            "noyau": noyau_info['noyau'],
                            "quantite": 1,  # Chaque configuration représente 1 unité
                            "hauteur": self._calculer_hauteur_matelas(noyau_info['noyau']),
                            "fermete": self._detecter_fermete_matelas(description),
                            "housse": self._detecter_type_housse(description),
                            "matiere_housse": self._detecter_matiere_housse(description),
                            "poignees": self._detecter_poignees(description),
                            "dimensions": dimensions,
                            "semaine_annee": f"{semaine_prod}_{annee_prod}",
                            "lundi": get_week_dates(semaine_prod, annee_prod)[0],
                            "vendredi": get_week_dates(semaine_prod, annee_prod)[1],
                            "commande_client": commande_client
                        }
                        
                        # Ajouter titre_cote depuis l'article LLM si disponible
                        if article_matelas and 'titre_cote' in article_matelas and article_matelas['titre_cote']:
                            config["titre_cote"] = article_matelas['titre_cote']
                        
                        # Ajout des dimensions housse et autres calculs
                        self._ajouter_dimensions_housse(config)
                        # Le calcul de dimension literie est maintenant fait dans _ajouter_dimensions_housse
                        
                        configurations.append(config)
                        config_index += 1
        
        return configurations
    
    def _create_configurations_sommiers(self, types_sommiers: List[Dict], sommier_articles: List[Dict],
                                      semaine_prod: int, annee_prod: int, commande_client: str) -> List[Dict]:
        """
        Crée les configurations sommiers à partir des types détectés
        """
        configurations = []
        
        for i, type_info in enumerate(types_sommiers):
            if type_info['type_sommier'] != 'INCONNU':
                # Trouver l'article correspondant
                quantite = 1
                description = ""
                if type_info['index'] <= len(sommier_articles):
                    article_sommier = sommier_articles[type_info['index'] - 1]
                    quantite = article_sommier.get('quantite', 1)
                    description = article_sommier.get('description', '')
                
                # Détection des dimensions
                import sys
                
                # Ajouter le répertoire backend au path
                script_dir = os.path.dirname(os.path.abspath(__file__))
                backend_dir = os.path.join(script_dir, "backend")
                if backend_dir not in sys.path:
                    sys.path.insert(0, backend_dir)
                
                from backend.dimensions_utils import detecter_dimensions
                from backend.dimensions_sommiers import detecter_dimensions_sommier
                from backend.sommier_utils import calculer_hauteur_sommier, detecter_materiau_sommier, detecter_type_relaxation_sommier, detecter_type_telecommande_sommier, detecter_soufflet_mousse_sommier, detecter_facon_moderne_sommier, detecter_tapissier_a_lattes_sommier, detecter_lattes_francaises_sommier
                from backend.sommier_analytics_utils import analyser_caracteristiques_sommier
                from backend.sommier_utils import detecter_options_sommier
                
                # Extraction des dimensions du sommier
                dimensions_str = article_sommier.get('dimensions') if article_sommier else None
                if dimensions_str:
                    dimensions = detecter_dimensions_sommier(dimensions_str)
                else:
                    dimensions = detecter_dimensions_sommier(description)
                
                # Calcul de la dimension sommier formatée
                dimension_sommier = None
                if dimensions:
                    from backend.dimensions_sommiers import calculer_dimensions_sommiers
                    dimension_sommier = calculer_dimensions_sommiers(dimensions)
                
                # Analyse des caractéristiques spécifiques du sommier
                caracteristiques = analyser_caracteristiques_sommier(description)
                
                # Détection du type relaxation
                type_relaxation_sommier = detecter_type_relaxation_sommier(description)
                
                # Détection du type télécommande
                type_telecommande_sommier = detecter_type_telecommande_sommier(description)
                
                # Détection des nouvelles caractéristiques
                soufflet_mousse = detecter_soufflet_mousse_sommier(description)
                facon_moderne = detecter_facon_moderne_sommier(description)
                tapissier_a_lattes = detecter_tapissier_a_lattes_sommier(description)
                lattes_francaises = detecter_lattes_francaises_sommier(description)
                
                # Segmentation des pieds
                pieds_segmentes = segmenter_pieds_sommier(description, quantite_article=quantite)
                
                # Création de la configuration sommier
                config = {
                    "sommier_index": type_info['index'],
                    "type_sommier": type_info['type_sommier'],
                    "quantite": quantite,
                    "hauteur": calculer_hauteur_sommier(type_info['type_sommier']),
                    "materiau": detecter_materiau_sommier(description),
                    "dimensions": dimensions,
                    "dimension_sommier": dimension_sommier,  # Nouveau champ
                    "type_relaxation_sommier": type_relaxation_sommier,  # Nouveau champ
                    "type_telecommande_sommier": type_telecommande_sommier,  # Nouveau champ
                    "soufflet_mousse": soufflet_mousse,  # Nouveau champ
                    "facon_moderne": facon_moderne,  # Nouveau champ
                    "tapissier_a_lattes": tapissier_a_lattes,  # Nouveau champ
                    "lattes_francaises": lattes_francaises,  # Nouveau champ
                    "semaine_annee": f"{semaine_prod}_{annee_prod}",
                    "lundi": get_week_dates(semaine_prod, annee_prod)[0],
                    "vendredi": get_week_dates(semaine_prod, annee_prod)[1],
                    "commande_client": commande_client,
                    # Nouvelles caractéristiques détectées
                    "sommier_dansunlit": caracteristiques["sommier_dansunlit"],
                    "sommier_pieds": caracteristiques["sommier_pieds"],
                    "pieds_segmentes": pieds_segmentes,
                    # Détection des options sommier (butees, rampes, etc.)
                    "options_sommier": detecter_options_sommier(description)
                }
                
                configurations.append(config)
        
        return configurations
    
    def _calculer_hauteur_matelas(self, noyau: str) -> int:
        """Calcule la hauteur du matelas selon le noyau"""
        import sys
        
        # Ajouter le répertoire backend au path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.join(script_dir, "backend")
        if backend_dir not in sys.path:
            sys.path.insert(0, backend_dir)
        
        from backend.hauteur_utils import calculer_hauteur_matelas
        return calculer_hauteur_matelas(noyau)
    
    def _detecter_fermete_matelas(self, description: str) -> str:
        """Détecte la fermeté du matelas"""
        import sys
        
        # Ajouter le répertoire backend au path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.join(script_dir, "backend")
        if backend_dir not in sys.path:
            sys.path.insert(0, backend_dir)
        
        from backend.fermete_utils import detecter_fermete_matelas
        return detecter_fermete_matelas(description)
    
    def _detecter_type_housse(self, description: str) -> str:
        """Détecte le type de housse"""
        import sys
        
        # Ajouter le répertoire backend au path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.join(script_dir, "backend")
        if backend_dir not in sys.path:
            sys.path.insert(0, backend_dir)
        
        from backend.housse_utils import detecter_type_housse
        return detecter_type_housse(description)
    
    def _detecter_matiere_housse(self, description: str) -> str:
        """Détecte la matière de la housse"""
        import sys
        
        # Ajouter le répertoire backend au path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.join(script_dir, "backend")
        if backend_dir not in sys.path:
            sys.path.insert(0, backend_dir)
        
        from backend.matiere_housse_utils import detecter_matiere_housse
        return detecter_matiere_housse(description)
    
    def _detecter_poignees(self, description: str) -> str:
        """Détecte la présence de poignées"""
        import sys
        
        # Ajouter le répertoire backend au path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.join(script_dir, "backend")
        if backend_dir not in sys.path:
            sys.path.insert(0, backend_dir)
        
        from backend.poignees_utils import detecter_poignees
        from backend.matiere_housse_utils import detecter_matiere_housse
        from backend.housse_utils import detecter_type_housse
        
        # Détecter d'abord la matière et le type de housse
        matiere_housse = detecter_matiere_housse(description)
        type_housse = detecter_type_housse(description)
        
        # Règle spéciale : si TENCEL LUXE 3D, forcer les poignées à NON
        if matiere_housse == "TENCEL LUXE 3D":
            return "NON"
        
        # Nouvelle règle : si housse MATELASSEE et matière contient TENCEL, forcer poignées à OUI
        if type_housse == "MATELASSEE" and "TENCEL" in matiere_housse:
            return "OUI"
        
        # Sinon, utiliser la détection normale
        return detecter_poignees(description)
    
    def _creer_pre_import_sommiers(self, configurations_sommiers: List[Dict], donnees_client: Dict,
                                  contient_dosseret_tete: bool, mots_operation_list: List[str]) -> List[Dict]:
        """
        Crée le pré-import pour les sommiers
        """
        pre_import_data = []
        
        for config in configurations_sommiers:
            # Créer les données de pré-import pour un sommier
            pre_import_item = {
                # Données client (mêmes clés que les matelas)
                "Client_D1": donnees_client.get('nom', ''),
                "Adresse_D3": donnees_client.get('adresse', ''),
                "numero_D2": config.get('commande_client', ''),  # Harmonisé avec les matelas
                # Champs commande et dates (mêmes clés que les matelas)
                "semaine_D5": config.get('semaine_annee', ''),
                "lundi_D6": config.get('lundi', ''),
                "vendredi_D7": config.get('vendredi', ''),
                # Données sommier
                "Type_Sommier_D20": config.get('type_sommier', ''),
                "Materiau_D25": config.get('materiau', ''),
                "Hauteur_D30": str(config.get('hauteur', '')),
                "Dimensions_D35": self._calculer_dimensions_sommiers(config.get('dimensions', {})),
                "Dimension_Sommier_D36": config.get('dimension_sommier', ''),  # Nouveau champ
                "Type_Relaxation_Sommier_D37": config.get('type_relaxation_sommier', ''),  # Nouveau champ
                "Type_Telecommande_Sommier_D38": config.get('type_telecommande_sommier', ''),  # Nouveau champ
                "Soufflet_Mousse_D39": config.get('soufflet_mousse', ''),  # Nouveau champ
                "Facon_Moderne_D40": config.get('facon_moderne', ''),  # Nouveau champ
                "Tapissier_A_Lattes_D41": config.get('tapissier_a_lattes', ''),  # Nouveau champ
                "Lattes_Francaises_D42": config.get('lattes_francaises', ''),  # Nouveau champ
                "Quantite_D43": str(config.get('quantite', 1)),
                # Nouvelles caractéristiques
                "Sommier_DansUnLit_D45": config.get('sommier_dansunlit', 'NON'),
                "Sommier_Pieds_D50": config.get('sommier_pieds', 'NON'),
                # Champs opérations (ajoutés pour harmoniser avec les matelas)
                "emporte_client_C57": "X" if "ENLEVEMENT" in mots_operation_list else "",
                "fourgon_C58": "X" if "LIVRAISON" in mots_operation_list else "",
                "transporteur_C59": "X" if "EXPEDITION" in mots_operation_list else "",
                # Données de production
                "semaine_annee": config.get('semaine_annee', ''),
                "lundi": config.get('lundi', ''),
                "vendredi": config.get('vendredi', ''),
                "commande_client": config.get('commande_client', ''),
                # Type d'article
                "type_article": "sommier",
                "sommier_index": config.get('sommier_index', 0)
            }
            # Ajout des options_sommier dans le pré-import (X si OUI, sinon '')
            options = config.get('options_sommier', {})
            options_mapping = {
                'butees_laterales': 'Butees_Laterales_D60',
                'butees_pieds': 'Butees_Pieds_D61',
                'solidarisation': 'Solidarisation_D62',
                'demi_corbeille': 'Demi_Corbeille_D63',
                'profile': 'Profile_D64',
                'renforces': 'Renforces_D65',
                'genou_moins': 'Genou_Moins_D66',
                'tronc_plus': 'Tronc_Plus_D67',
                'calles': 'Calles_D68',
                'rampes': 'Rampes_D69',
                'autre': 'Autre_D70',
                'platine_reunion': 'Platine_Reunion_D71',
                'pieds_centraux': 'Pieds_Centraux_D72',
                'patins_feutre': 'Patins_Feutre_D73',
                'patins_carrelage': 'Patins_Carrelage_D74',
                'patins_teflon': 'Patins_Teflon_D75',
                'finition_multiplis': 'Finition_Multiplis_D76',
                'finition_90mm': 'Finition_90mm_D77',
                'finition_paremente': 'Finition_Paremente_D78',
                'finition_multiplis_tv': 'Finition_Multiplis_TV_D79',
                'finition_multiplis_l': 'Finition_Multiplis_L_D80',
                'finition_chene': 'Finition_Chene_D81',
                'finition_frene_tv': 'Finition_Frene_TV_D82',
                'finition_frene_l': 'Finition_Frene_L_D83'
            }
            for opt, champ in options_mapping.items():
                pre_import_item[champ] = 'X' if options.get(opt) == 'OUI' else ''
            # Supprimer pieds_segmentes du pré-import s'il existe
            if 'pieds_segmentes' in pre_import_item:
                del pre_import_item['pieds_segmentes']
            pre_import_data.append(pre_import_item)
        
        return pre_import_data
    
    def _ajouter_dimensions_housse(self, config: Dict):
        """Ajoute les dimensions housse selon le noyau"""
        try:
            # Import des fonctions nécessaires
            import sys
                
            # Ajouter le répertoire backend au path
            script_dir = os.path.dirname(os.path.abspath(__file__))
            backend_dir = os.path.join(script_dir, "backend")
            if backend_dir not in sys.path:
                sys.path.insert(0, backend_dir)
            
            from backend.latex_naturel_longueur_housse_utils import get_latex_naturel_longueur_housse_value
            from backend.latex_mixte7zones_longueur_housse_utils import get_latex_mixte7zones_longueur_housse_value
            from backend.mousse_rainuree7zones_longueur_housse_utils import get_mousse_rainuree7zones_longueur_housse_value
            from backend.select43_longueur_housse_utils import get_select43_longueur_housse_value
            from backend.latex_renforce_longueur_utils import get_latex_renforce_longueur_housse
            from backend.mousse_visco_utils import get_mousse_visco_value
            from backend.mousse_visco_longueur_utils import get_mousse_visco_longueur_value
            from backend.latex_naturel_referentiel import get_valeur_latex_naturel, MATIERE_MAP as LN_MATIERE_MAP
            from backend.latex_mixte7zones_referentiel import get_valeur_latex_mixte7zones, MATIERE_MAP as LM7Z_MATIERE_MAP
            from backend.mousse_rainuree7zones_referentiel import get_valeur_mousse_rainuree7zones, MATIERE_MAP as MR7Z_MATIERE_MAP
            from backend.select43_utils import get_select43_display_value
            from backend.latex_renforce_utils import get_latex_renforce_display_value
            from backend.decoupe_noyau_utils import calcul_decoupe_noyau
            import math
            
            noyau = config.get("noyau", "")
            quantite = config.get("quantite", 1)
            dimension_housse = None
            dimensions = config.get("dimensions", {})
            matiere_housse = config.get("matiere_housse", "")
            
            if noyau == 'LATEX NATUREL' and dimensions and matiere_housse in LN_MATIERE_MAP:
                valeur = get_valeur_latex_naturel(dimensions["largeur"], matiere_housse)
                if matiere_housse == "POLYESTER":
                    dimension_housse = f"{valeur}"
                else:
                    prefixe = "4 x " if quantite == 2 else ("2 x " if quantite == 1 else f"{quantite * 2} x ")
                    dimension_housse = f"{prefixe}{valeur}"
                # Ajout de la dimension housse longueur
                dimension_housse_longueur = get_latex_naturel_longueur_housse_value(dimensions["longueur"], matiere_housse)
                if dimension_housse_longueur is not None:
                    config["dimension_housse_longueur"] = dimension_housse_longueur
                    
            elif noyau == 'LATEX MIXTE 7 ZONES' and dimensions and matiere_housse in LM7Z_MATIERE_MAP:
                valeur = get_valeur_latex_mixte7zones(dimensions["largeur"], matiere_housse)
                if matiere_housse == "POLYESTER":
                    dimension_housse = f"{valeur}"
                else:
                    prefixe = "4 x " if quantite == 2 else ("2 x " if quantite == 1 else f"{quantite * 2} x ")
                    dimension_housse = f"{prefixe}{valeur}"
                # Ajout de la dimension housse longueur
                dimension_housse_longueur = get_latex_mixte7zones_longueur_housse_value(dimensions["longueur"], matiere_housse)
                if dimension_housse_longueur is not None:
                    config["dimension_housse_longueur"] = dimension_housse_longueur
                    
            elif noyau == 'MOUSSE RAINUREE 7 ZONES' and dimensions and matiere_housse in MR7Z_MATIERE_MAP:
                valeur = get_valeur_mousse_rainuree7zones(dimensions["largeur"], matiere_housse)
                if matiere_housse == "POLYESTER":
                    dimension_housse = f"{valeur}"
                else:
                    prefixe = "4 x " if quantite == 2 else ("2 x " if quantite == 1 else f"{quantite * 2} x ")
                    dimension_housse = f"{prefixe}{valeur}"
                # Ajout de la dimension housse longueur
                dimension_housse_longueur = get_mousse_rainuree7zones_longueur_housse_value(dimensions["longueur"], matiere_housse)
                if dimension_housse_longueur is not None:
                    config["dimension_housse_longueur"] = dimension_housse_longueur
                    
            elif noyau == 'SELECT 43' and dimensions and matiere_housse:
                dimension_housse = get_select43_display_value(dimensions["largeur"], matiere_housse, quantite)
                # Ajout de la dimension housse longueur
                dimension_housse_longueur = get_select43_longueur_housse_value(dimensions["longueur"], matiere_housse)
                if dimension_housse_longueur is not None:
                    config["dimension_housse_longueur"] = dimension_housse_longueur
                    
            elif noyau == 'LATEX RENFORCE' and dimensions and matiere_housse:
                dimension_housse = get_latex_renforce_display_value(dimensions["largeur"], matiere_housse, quantite)
                # Ajout de la dimension housse longueur
                dimension_housse_longueur = get_latex_renforce_longueur_housse(dimensions["longueur"], matiere_housse)
                if dimension_housse_longueur is not None:
                    config["dimension_housse_longueur"] = dimension_housse_longueur
                    
            elif noyau == 'MOUSSE VISCO' and dimensions:
                # Dimension housse (largeur) - utiliser le bon référentiel
                dimension_housse = get_mousse_visco_value(dimensions["largeur"], matiere_housse)
                # Ajout de la dimension housse longueur
                dimension_housse_longueur = get_mousse_visco_longueur_value(dimensions["longueur"])
                if dimension_housse_longueur is not None:
                    config["dimension_housse_longueur"] = dimension_housse_longueur
                
            if dimension_housse:
                config["dimension_housse"] = dimension_housse
                
            # Calcul de la dimension literie
            if dimensions:
                largeur = dimensions["largeur"]
                longueur = dimensions["longueur"]
                
                # Contrôle d'arrondi : ne pas arrondir si la différence est > 3cm
                largeur_arrondie_temp = int(math.ceil(largeur / 10.0) * 10)
                longueur_arrondie_temp = int(math.ceil(longueur / 10.0) * 10)
                
                # Vérifier si l'arrondi dépasse 3cm (30mm)
                if (largeur_arrondie_temp - largeur) > 3.0 or (longueur_arrondie_temp - longueur) > 3.0:
                    # Utiliser les dimensions originales si l'arrondi est trop important
                    largeur_finale = largeur
                    longueur_finale = longueur
                else:
                    # Utiliser les dimensions arrondies
                    largeur_finale = largeur_arrondie_temp
                    longueur_finale = longueur_arrondie_temp
                
                if quantite == 2:
                    largeur_literie = largeur_finale * 2
                else:
                    largeur_literie = largeur_finale
                dimension_literie = f"{largeur_literie}x{longueur_finale}"
                config["dimension_literie"] = dimension_literie
                
                # Calcul découpe noyau
                fermete = config.get("fermete", "")
                largeur_decoupe, longueur_decoupe = calcul_decoupe_noyau(noyau, fermete, largeur, longueur)
                # Forcer l'utilisation du point décimal
                largeur_str = str(largeur_decoupe).replace(',', '.')
                longueur_str = str(longueur_decoupe).replace(',', '.')
                config["decoupe_noyau"] = f"{largeur_str} x {longueur_str}"
                
        except Exception as e:
            self.logger.error(f"Erreur lors du calcul des dimensions housse: {e}")
            config["dimension_housse"] = f"Erreur: {e}"
    
    def _calculer_dimensions_sommiers(self, dimensions: Dict) -> str:
        """Calcule les dimensions des sommiers selon les spécifications"""
        try:
            import sys
                
            # Ajouter le répertoire backend au path
            script_dir = os.path.dirname(os.path.abspath(__file__))
            backend_dir = os.path.join(script_dir, "backend")
            if backend_dir not in sys.path:
                sys.path.insert(0, backend_dir)
            
            from backend.dimensions_sommiers import calculer_dimensions_sommiers
            
            if not dimensions:
                return ""
            
            resultat = calculer_dimensions_sommiers(dimensions)
            return resultat if resultat else ""
            
        except Exception as e:
            self.logger.error(f"Erreur lors du calcul des dimensions sommiers: {e}")
            # Fallback vers l'ancien format si erreur
            if dimensions:
                largeur = dimensions.get('largeur', '')
                longueur = dimensions.get('longueur', '')
                return f"{largeur}x{longueur}" if largeur and longueur else ""
            return ""
    
    def _calculer_dimension_literie(self, config: Dict):
        """Calcule la dimension literie"""
        import math
        dimensions = config.get("dimensions")
        quantite = config.get("quantite", 1)
        
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
    
    def _clean_and_parse_json(self, raw_text: str) -> str:
        """Nettoie et parse le JSON retourné par le LLM"""
        
        # Log de debug pour analyser la réponse
        self.logger.info(f"DEBUG: Tentative de parsing JSON - Longueur: {len(raw_text)}")
        self.logger.info(f"DEBUG: Début du texte: {raw_text[:100]}...")
        
        # Sauvegarder la réponse complète pour debug
        try:
            with open("debug_llm_response_full.txt", "w", encoding="utf-8") as f:
                f.write(raw_text)
            self.logger.info(f"DEBUG: Réponse complète sauvée dans debug_llm_response_full.txt")
        except Exception as e:
            self.logger.error(f"DEBUG: Erreur sauvegarde debug: {e}")
        
        try:
            # Supprime les caractères Unicode problématiques
            cleaned_text = raw_text.encode('utf-8', errors='ignore').decode('utf-8')
            
            # Essaie de parser directement
            json.loads(cleaned_text)
            self.logger.info(f"DEBUG: Parsing direct réussi!")
            return cleaned_text
        except json.JSONDecodeError as e:
            self.logger.info(f"DEBUG: Parsing direct échoué: {e}, tentative nettoyage backticks")
            
            # Tentative de nettoyage des backticks AVANT nettoyage ASCII
            try:
                import re
                # Supprime les backticks et le mot "json" s'il est présent
                cleaned_text = re.sub(r'```(?:json)?\s*', '', raw_text)
                cleaned_text = re.sub(r'\s*```', '', cleaned_text)
                self.logger.info(f"DEBUG: Après suppression backticks: {cleaned_text[:100]}...")
                json.loads(cleaned_text)  # Test si c'est du JSON valide
                self.logger.info(f"DEBUG: Parsing backticks réussi!")
                return cleaned_text
            except (json.JSONDecodeError, AttributeError) as e_backticks:
                self.logger.info(f"DEBUG: Parsing backticks échoué: {e_backticks}, tentative nettoyage ASCII")
            
            # Si ça ne marche pas, on essaie de nettoyer plus agressivement
            try:
                # Supprime les caractères non-ASCII
                cleaned_text = ''.join(char for char in raw_text if ord(char) < 128)
                json.loads(cleaned_text)
                return cleaned_text
            except json.JSONDecodeError as e2:
                self.logger.info(f"DEBUG: Parsing après nettoyage ASCII échoué")
                
                # Essaie de trouver du JSON dans le texte
                try:
                    import re
                    # Cherche un bloc JSON entre accolades
                    json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
                    if json_match:
                        json_text = json_match.group(0)
                        json.loads(json_text)  # Test si c'est du JSON valide
                        return json_text
                except (json.JSONDecodeError, AttributeError):
                    self.logger.info(f"DEBUG: Parsing regex accolades échoué")
                
                # Essaie de trouver du JSON entouré de backticks
                try:
                    import re
                    # Cherche du JSON entouré de ```json ... ``` ou ``` ... ```
                    json_block_match = re.search(r'```(?:json)?\s*(\{.*\})\s*```', raw_text, re.DOTALL)
                    if json_block_match:
                        json_text = json_block_match.group(1)
                        json.loads(json_text)  # Test si c'est du JSON valide
                        return json_text
                except (json.JSONDecodeError, AttributeError):
                    self.logger.info(f"DEBUG: Aucun match trouvé avec regex backticks")
                
                # Essaie une approche alternative : supprimer les backticks et parser
                try:
                    import re
                    # Supprime les backticks et le mot "json" s'il est présent
                    cleaned_text = re.sub(r'```(?:json)?\s*', '', raw_text)
                    cleaned_text = re.sub(r'\s*```', '', cleaned_text)
                    self.logger.info(f"DEBUG: Texte après suppression backticks: {cleaned_text[:100]}...")
                    json.loads(cleaned_text)  # Test si c'est du JSON valide
                    return cleaned_text
                except (json.JSONDecodeError, AttributeError) as e3:
                    self.logger.info(f"DEBUG: Parsing après suppression backticks échoué: {e3}")
                    
                    # Si c'est une erreur de chaîne non terminée, essaie d'extraire le JSON valide
                    if "Unterminated string" in str(e3) or "Expecting value" in str(e3):
                        self.logger.info(f"DEBUG: Tentative de correction des chaînes non terminées")
                        try:
                            import re
                            # Supprime les backticks
                            cleaned_text = re.sub(r'```(?:json)?\s*', '', raw_text)
                            cleaned_text = re.sub(r'\s*```', '', cleaned_text)
                            
                            # Essaie d'extraire le JSON jusqu'à la première erreur
                            # Cherche la position de l'erreur
                            error_match = re.search(r'line (\d+) column (\d+)', str(e3))
                            if error_match:
                                error_line = int(error_match.group(1))
                                error_column = int(error_match.group(2))
                                
                                self.logger.info(f"DEBUG: Erreur à la ligne {error_line}, colonne {error_column}")
                                
                                # Prend les lignes jusqu'à l'erreur (exclus)
                                lines = cleaned_text.split('\n')
                                valid_lines = lines[:error_line-1]  # -1 car les lignes commencent à 1
                                
                                # Essaie de fermer proprement le JSON
                                valid_text = '\n'.join(valid_lines)
                                
                                # Compte les accolades ouvertes et fermées
                                open_braces = valid_text.count('{')
                                close_braces = valid_text.count('}')
                                
                                # Compte les crochets ouverts et fermés
                                open_brackets = valid_text.count('[')
                                close_brackets = valid_text.count(']')
                                
                                # Ajoute les accolades fermantes manquantes
                                for _ in range(open_braces - close_braces):
                                    valid_text += '\n}'
                                
                                # Ajoute les crochets fermants manquants
                                for _ in range(open_brackets - close_brackets):
                                    valid_text += '\n]'
                                # SUPPRESSION DE LA DERNIERE VIRGULE ORPHELINE
                                import re
                                # On supprime la dernière virgule avant un crochet ou une accolade fermante
                                valid_text = re.sub(r',\s*([}\]])', r'\1', valid_text)
                                self.logger.info(f"DEBUG: JSON extrait jusqu'à la ligne {error_line-1}, {open_braces} accolades ouvertes, {close_braces} fermées, {open_brackets} crochets ouverts, {close_brackets} fermés (virgule finale supprimée)")
                                # Test si c'est du JSON valide
                                json.loads(valid_text)
                                return valid_text
                        except (json.JSONDecodeError, AttributeError) as e4:
                            self.logger.info(f"DEBUG: Correction des chaînes échouée: {e4}")
                            
                            # Si ça ne marche toujours pas, essaie une approche plus agressive
                            try:
                                # Cherche le dernier objet JSON complet
                                import re
                                # Cherche le dernier objet qui se termine par }
                                last_object_match = re.search(r'(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})', cleaned_text)
                                if last_object_match:
                                    last_object = last_object_match.group(1)
                                    # Cherche le dernier tableau qui se termine par ]
                                    last_array_match = re.search(r'(\[[^\[\]]*(?:\{[^{}]*\}[^\[\]]*)*\])', cleaned_text)
                                    if last_array_match:
                                        # Combine jusqu'au dernier tableau
                                        end_pos = last_array_match.end()
                                        valid_text = cleaned_text[:end_pos]
                                        
                                        # Ferme les structures ouvertes
                                        open_braces = valid_text.count('{')
                                        close_braces = valid_text.count('}')
                                        open_brackets = valid_text.count('[')
                                        close_brackets = valid_text.count(']')
                                        
                                        for _ in range(open_braces - close_braces):
                                            valid_text += '\n}'
                                        for _ in range(open_brackets - close_brackets):
                                            valid_text += '\n]'
                                        # SUPPRESSION DE LA DERNIERE VIRGULE ORPHELINE
                                        valid_text = re.sub(r',\s*([}\]])', r'\1', valid_text)
                                        self.logger.info(f"DEBUG: Approche agressive - JSON extrait jusqu'à la position {end_pos} (virgule finale supprimée)")
                                        json.loads(valid_text)
                                        return valid_text
                            except (json.JSONDecodeError, AttributeError) as e5:
                                self.logger.info(f"DEBUG: Approche agressive échouée: {e5}")
                
                # En dernier recours, on retourne le texte original
                self.logger.warning(f"Impossible de parser le JSON LLM: {raw_text[:200]}...")
                return raw_text

    def _export_excel_global(self, pre_import_data: List[Dict], semaine_prod: int, annee_prod: int,
                           semaine_matelas: Optional[int] = None, annee_matelas: Optional[int] = None,
                           semaine_sommiers: Optional[int] = None, annee_sommiers: Optional[int] = None) -> List[str]:
        """
        Exporte tous les pré-imports dans un seul fichier Excel, triés selon l'ordre des noyaux défini.
        Gère les matelas et les sommiers séparément avec leurs semaines de production respectives.
        """
        try:
            # Utiliser les semaines de production calculées ou les semaines de référence par défaut
            semaine_matelas_prod = semaine_matelas or semaine_prod
            annee_matelas_prod = annee_matelas or annee_prod
            semaine_sommiers_prod = semaine_sommiers or semaine_prod
            annee_sommiers_prod = annee_sommiers or annee_prod
            
            # Formater les semaines pour le nommage des fichiers
            semaine_matelas_str = str(semaine_matelas_prod).zfill(2)
            annee_matelas_str = str(annee_matelas_prod)
            semaine_sommiers_str = str(semaine_sommiers_prod).zfill(2)
            annee_sommiers_str = str(annee_sommiers_prod)
            
            semaine_excel_matelas = f"S{semaine_matelas_str}"
            semaine_excel_sommiers = f"S{semaine_sommiers_str}"
            id_fichier_matelas = annee_matelas_str
            id_fichier_sommiers = annee_sommiers_str
            
            fichiers_crees = []
            
            # Chemin absolu vers les templates (défini au début pour être accessible partout)
            script_dir = os.path.dirname(os.path.abspath(__file__))
            template_path_matelas = os.path.join(script_dir, "template", "template_matelas.xlsx")
            template_path_sommiers = os.path.join(script_dir, "template", "template_sommier.xlsx")
            
            # Séparer les matelas et les sommiers
            pre_import_matelas = [item for item in pre_import_data if item.get('type_article') != 'sommier']
            pre_import_sommiers = [item for item in pre_import_data if item.get('type_article') == 'sommier']
            
            self.logger.info(f"Export global: {len(pre_import_matelas)} matelas, {len(pre_import_sommiers)} sommiers")
            
            # Export des matelas
            if pre_import_matelas:
                # Récupérer l'ordre des noyaux depuis la config
                noyau_order = config.get_noyau_order()
                self.logger.info(f"Ordre des noyaux pour tri global: {noyau_order}")
                
                # Afficher les noyaux présents dans les pré-imports
                noyaux_presents = []
                for pre_import in pre_import_matelas:
                    noyau = pre_import.get('noyau')
                    if noyau:
                        noyaux_presents.append(noyau)
                self.logger.info(f"Noyaux présents dans les pré-imports: {noyaux_presents}")
                
                # Trier les pré-imports selon l'ordre des noyaux
                if noyau_order:
                    def get_noyau_key(pre_import):
                        noyau = pre_import.get('noyau', '')
                        self.logger.info(f"Tri global de la configuration avec noyau: {noyau}")
                        
                        # Normaliser le noyau pour le matching (ignorer "7 ZONES")
                        noyau_normalized = noyau.replace(' 7 ZONES', '')
                        noyau_order_normalized = [n.replace(' 7 ZONES', '') for n in noyau_order]
                        
                        try:
                            return noyau_order_normalized.index(noyau_normalized)
                        except ValueError:
                            # Si pas trouvé avec normalisation, essayer le noyau exact
                            try:
                                return noyau_order.index(noyau)
                            except ValueError:
                                self.logger.info(f"Noyau '{noyau}' non trouvé dans l'ordre, placé à la fin")
                                return len(noyau_order) + 1  # Les noyaux non listés vont à la fin
                    
                    pre_import_matelas = sorted(pre_import_matelas, key=get_noyau_key)
                self.logger.info(f"Pré-imports matelas triés selon l'ordre global défini")
                
                # Export des matelas
                try:
                    from backend.excel_import_utils import ExcelMatelasImporter
                    importer_matelas = ExcelMatelasImporter(template_path_matelas)
                    fichiers_matelas = importer_matelas.import_configurations(pre_import_matelas, semaine_excel_matelas, id_fichier_matelas)
                    fichiers_crees.extend(fichiers_matelas)
                    self.logger.info(f"Export matelas terminé: {len(fichiers_matelas)} fichier(s) avec semaine {semaine_excel_matelas}_{id_fichier_matelas}")
                except Exception as e:
                    self.logger.error(f"Erreur lors de l'export matelas: {e}")
            
            # Export des sommiers
            if pre_import_sommiers:
                try:
                    from backend.excel_sommier_import_utils import ExcelSommierImporter
                    importer_sommiers = ExcelSommierImporter(template_path_sommiers)
                    fichiers_sommiers = importer_sommiers.import_configurations(pre_import_sommiers, semaine_excel_sommiers, id_fichier_sommiers)
                    fichiers_crees.extend(fichiers_sommiers)
                    self.logger.info(f"Export sommiers terminé: {len(fichiers_sommiers)} fichier(s) avec semaine {semaine_excel_sommiers}_{id_fichier_sommiers}")
                except Exception as e:
                    self.logger.error(f"Erreur lors de l'export sommiers: {e}")
            
            return fichiers_crees
        except Exception as e:
            self.logger.error(f"Erreur lors de l'export Excel global: {e}")
            return []


# Instance globale pour l'interface
backend_interface = BackendInterface() 