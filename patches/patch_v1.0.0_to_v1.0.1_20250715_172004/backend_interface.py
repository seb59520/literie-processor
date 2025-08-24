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

# Ajout du dossier backend au path
sys.path.append('backend')

# Import des modules backend
from date_utils import get_week_dates
from pre_import_utils import creer_pre_import, valider_pre_import
from main import call_llm, call_openrouter
from excel_import_utils import ExcelMatelasImporter
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import config
from sommier_utils import segmenter_pieds_sommier


class BackendInterface:
    """Interface pour intégrer le backend existant avec l'interface graphique"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    async def process_pdf_files(self, files: List[str], enrich_llm: bool, llm_provider: str, 
                         openrouter_api_key: Optional[str], semaine_prod: int, 
                         annee_prod: int, commande_client: List[str]) -> Dict:
        """
        Traite les fichiers PDF en utilisant la logique backend existante
        
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
        results = []
        errors = []
        
        # Collecte globale de toutes les configurations et pré-imports
        all_configurations = []
        all_pre_imports = []
        
        for idx, file_path in enumerate(files):
            try:
                # Création d'un fichier temporaire pour simuler l'upload
                temp_dir = tempfile.mkdtemp()
                temp_file_path = os.path.join(temp_dir, os.path.basename(file_path))
                
                # Copie du fichier vers le répertoire temporaire
                shutil.copy2(file_path, temp_file_path)
                
                # Simulation des paramètres de l'interface web
                file_info = {
                    'filename': os.path.basename(file_path),
                    'file_path': temp_file_path
                }
                
                # Appel de la logique backend existante
                result = await self._process_single_file(
                    file_info, enrich_llm, llm_provider, openrouter_api_key,
                    semaine_prod, annee_prod, commande_client[idx] if idx < len(commande_client) else ""
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
                fichiers_excel = self._export_excel_global(all_pre_imports, semaine_prod, annee_prod)
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
                           annee_prod: int, commande_client: str) -> Dict:
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
                if llm_provider == "ollama":
                    try:
                        llm_result = await call_llm(text)
                    except Exception as e:
                        self.logger.warning(f"Erreur LLM Ollama: {e}")
                        llm_result = None
                elif llm_provider == "openrouter":
                    if openrouter_api_key:
                        try:
                            llm_result = await call_openrouter(text, openrouter_api_key)
                        except Exception as e:
                            self.logger.warning(f"Erreur LLM OpenRouter: {e}")
                            llm_result = None
            
            # Traitement des données LLM
            donnees_client = {}
            configurations_matelas = []
            pre_import_data = []
            
            if llm_result:
                # Parsing du JSON LLM
                cleaned_llm_result = self._clean_and_parse_json(llm_result)
                if cleaned_llm_result:
                    try:
                        llm_data = json.loads(cleaned_llm_result)
                        
                        # Extraction des données client
                        from client_utils import extraire_donnees_client
                        donnees_client = extraire_donnees_client(llm_data)
                        
                        # Extraction des articles
                        articles_llm = []
                        matelas_articles = []
                        sommier_articles = []
                        pieds_articles = []
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
                        from matelas_utils import detecter_noyau_matelas
                        noyaux_matelas = detecter_noyau_matelas(matelas_articles)
                        
                        # Détection des types sommiers
                        from sommier_utils import detecter_type_sommier
                        types_sommiers = detecter_type_sommier(sommier_articles)
                        
                        # Création des configurations matelas
                        configurations_matelas = self._create_configurations_matelas(
                            noyaux_matelas, matelas_articles, semaine_prod, annee_prod, commande_client
                        )
                        
                        # Création des configurations sommiers
                        configurations_sommiers = self._create_configurations_sommiers(
                            types_sommiers, sommier_articles, semaine_prod, annee_prod, commande_client
                        )
                        
                        # Création du pré-import
                        if (configurations_matelas or configurations_sommiers) and donnees_client:
                            import sys
                            import os
                            
                            # Ajouter le répertoire backend au path
                            script_dir = os.path.dirname(os.path.abspath(__file__))
                            backend_dir = os.path.join(script_dir, "backend")
                            if backend_dir not in sys.path:
                                sys.path.insert(0, backend_dir)
                            
                            from article_utils import contient_dosseret_ou_tete
                            from operation_utils import mots_operation_trouves
                            
                            contient_dosseret_tete = contient_dosseret_ou_tete(articles_llm)
                            mots_operation_list = mots_operation_trouves(articles_llm)
                            
                            # Créer le pré-import pour les matelas
                            pre_import_data_matelas = creer_pre_import(
                                configurations_matelas, donnees_client, 
                                contient_dosseret_tete, mots_operation_list
                            ) if configurations_matelas else []
                            
                            # Créer le pré-import pour les sommiers
                            pre_import_data_sommiers = self._creer_pre_import_sommiers(
                                configurations_sommiers, donnees_client, 
                                contient_dosseret_tete, mots_operation_list
                            ) if configurations_sommiers else []
                            
                            # Combiner les deux pré-imports
                            pre_import_data = pre_import_data_matelas + pre_import_data_sommiers
                            
                            # Note: L'export Excel sera fait globalement après traitement de tous les fichiers
                            fichiers_excel = []
                        
                    except json.JSONDecodeError as e:
                        self.logger.warning(f"Erreur parsing JSON LLM: {e}")
            
            # Détection des pieds indépendants
            from sommier_utils import segmenter_pieds_sommier
            configurations_pieds = []
            for article in pieds_articles:
                pied = segmenter_pieds_sommier(article.get('description', ''), quantite_article=article.get('quantite', 1))
                pied['article_index'] = articles_llm.index(article) + 1 if article in articles_llm else None
                configurations_pieds.append(pied)
            
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
    
    def _create_configurations_matelas(self, noyaux_matelas: List[Dict], matelas_articles: List[Dict],
                             semaine_prod: int, annee_prod: int, commande_client: str) -> List[Dict]:
        """
        Crée les configurations matelas à partir des noyaux détectés
        """
        configurations = []
        
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
                import os
                
                # Ajouter le répertoire backend au path
                script_dir = os.path.dirname(os.path.abspath(__file__))
                backend_dir = os.path.join(script_dir, "backend")
                if backend_dir not in sys.path:
                    sys.path.insert(0, backend_dir)
                
                from dimensions_utils import detecter_dimensions
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
                
                # Ajout des dimensions housse et autres calculs
                self._ajouter_dimensions_housse(config)
                # Le calcul de dimension literie est maintenant fait dans _ajouter_dimensions_housse
                
                configurations.append(config)
        
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
                import os
                
                # Ajouter le répertoire backend au path
                script_dir = os.path.dirname(os.path.abspath(__file__))
                backend_dir = os.path.join(script_dir, "backend")
                if backend_dir not in sys.path:
                    sys.path.insert(0, backend_dir)
                
                from dimensions_utils import detecter_dimensions
                from dimensions_sommiers import detecter_dimensions_sommier
                from sommier_utils import calculer_hauteur_sommier, detecter_materiau_sommier, detecter_type_relaxation_sommier, detecter_type_telecommande_sommier, detecter_soufflet_mousse_sommier, detecter_facon_moderne_sommier, detecter_tapissier_a_lattes_sommier, detecter_lattes_francaises_sommier
                from sommier_analytics_utils import analyser_caracteristiques_sommier
                from sommier_utils import detecter_options_sommier
                
                # Extraction des dimensions du sommier
                dimensions_str = article_sommier.get('dimensions') if article_sommier else None
                if dimensions_str:
                    dimensions = detecter_dimensions_sommier(dimensions_str)
                else:
                    dimensions = detecter_dimensions_sommier(description)
                
                # Calcul de la dimension sommier formatée
                dimension_sommier = None
                if dimensions:
                    from dimensions_sommiers import calculer_dimensions_sommiers
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
        import os
        
        # Ajouter le répertoire backend au path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.join(script_dir, "backend")
        if backend_dir not in sys.path:
            sys.path.insert(0, backend_dir)
        
        from hauteur_utils import calculer_hauteur_matelas
        return calculer_hauteur_matelas(noyau)
    
    def _detecter_fermete_matelas(self, description: str) -> str:
        """Détecte la fermeté du matelas"""
        import sys
        import os
        
        # Ajouter le répertoire backend au path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.join(script_dir, "backend")
        if backend_dir not in sys.path:
            sys.path.insert(0, backend_dir)
        
        from fermete_utils import detecter_fermete_matelas
        return detecter_fermete_matelas(description)
    
    def _detecter_type_housse(self, description: str) -> str:
        """Détecte le type de housse"""
        import sys
        import os
        
        # Ajouter le répertoire backend au path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.join(script_dir, "backend")
        if backend_dir not in sys.path:
            sys.path.insert(0, backend_dir)
        
        from housse_utils import detecter_type_housse
        return detecter_type_housse(description)
    
    def _detecter_matiere_housse(self, description: str) -> str:
        """Détecte la matière de la housse"""
        import sys
        import os
        
        # Ajouter le répertoire backend au path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.join(script_dir, "backend")
        if backend_dir not in sys.path:
            sys.path.insert(0, backend_dir)
        
        from matiere_housse_utils import detecter_matiere_housse
        return detecter_matiere_housse(description)
    
    def _detecter_poignees(self, description: str) -> str:
        """Détecte la présence de poignées"""
        import sys
        import os
        
        # Ajouter le répertoire backend au path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.join(script_dir, "backend")
        if backend_dir not in sys.path:
            sys.path.insert(0, backend_dir)
        
        from poignees_utils import detecter_poignees
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
            import os
            
            # Ajouter le répertoire backend au path
            script_dir = os.path.dirname(os.path.abspath(__file__))
            backend_dir = os.path.join(script_dir, "backend")
            if backend_dir not in sys.path:
                sys.path.insert(0, backend_dir)
            
            from latex_naturel_longueur_housse_utils import get_latex_naturel_longueur_housse_value
            from latex_mixte7zones_longueur_housse_utils import get_latex_mixte7zones_longueur_housse_value
            from mousse_rainuree7zones_longueur_housse_utils import get_mousse_rainuree7zones_longueur_housse_value
            from select43_longueur_housse_utils import get_select43_longueur_housse_value
            from latex_renforce_longueur_utils import get_latex_renforce_longueur_housse
            from mousse_visco_longueur_utils import get_mousse_visco_longueur_value
            from latex_naturel_referentiel import get_valeur_latex_naturel, MATIERE_MAP as LN_MATIERE_MAP
            from latex_mixte7zones_referentiel import get_valeur_latex_mixte7zones, MATIERE_MAP as LM7Z_MATIERE_MAP
            from mousse_rainuree7zones_referentiel import get_valeur_mousse_rainuree7zones, MATIERE_MAP as MR7Z_MATIERE_MAP
            from select43_utils import get_select43_display_value
            from latex_renforce_utils import get_latex_renforce_display_value
            from decoupe_noyau_utils import calcul_decoupe_noyau
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
                dimension_housse = get_mousse_visco_longueur_value(dimensions["longueur"])
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
                largeur_decoupe, longueur_decoupe = calcul_decoupe_noyau(noyau, fermete, largeur, longueur)
                config["decoupe_noyau"] = f"{largeur_decoupe} x {longueur_decoupe}"
                
        except Exception as e:
            self.logger.error(f"Erreur lors du calcul des dimensions housse: {e}")
            config["dimension_housse"] = f"Erreur: {e}"
    
    def _calculer_dimensions_sommiers(self, dimensions: Dict) -> str:
        """Calcule les dimensions des sommiers selon les spécifications"""
        try:
            import sys
            import os
            
            # Ajouter le répertoire backend au path
            script_dir = os.path.dirname(os.path.abspath(__file__))
            backend_dir = os.path.join(script_dir, "backend")
            if backend_dir not in sys.path:
                sys.path.insert(0, backend_dir)
            
            from dimensions_sommiers import calculer_dimensions_sommiers
            
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
        try:
            # Supprime les caractères Unicode problématiques
            cleaned_text = raw_text.encode('utf-8', errors='ignore').decode('utf-8')
            
            # Essaie de parser directement
            json.loads(cleaned_text)
            return cleaned_text
        except json.JSONDecodeError:
            # Si ça ne marche pas, on essaie de nettoyer plus agressivement
            try:
                # Supprime les caractères non-ASCII
                cleaned_text = ''.join(char for char in raw_text if ord(char) < 128)
                json.loads(cleaned_text)
                return cleaned_text
            except json.JSONDecodeError:
                # En dernier recours, on retourne le texte original
                return raw_text

    def _export_excel_global(self, pre_import_data: List[Dict], semaine_prod: int, annee_prod: int) -> List[str]:
        """
        Exporte tous les pré-imports dans un seul fichier Excel, triés selon l'ordre des noyaux défini.
        Gère les matelas et les sommiers séparément.
        """
        try:
            semaine = str(semaine_prod).zfill(2)
            annee = str(annee_prod)
            semaine_excel = f"S{semaine}"
            id_fichier = annee
            
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
                        try:
                            return noyau_order.index(noyau)
                        except ValueError:
                            self.logger.info(f"Noyau '{noyau}' non trouvé dans l'ordre, placé à la fin")
                            return len(noyau_order) + 1  # Les noyaux non listés vont à la fin
                    
                    pre_import_matelas = sorted(pre_import_matelas, key=get_noyau_key)
                self.logger.info(f"Pré-imports matelas triés selon l'ordre global défini")
                
                # Export des matelas
                try:
                    from excel_import_utils import ExcelMatelasImporter
                    importer_matelas = ExcelMatelasImporter(template_path_matelas)
                    fichiers_matelas = importer_matelas.import_configurations(pre_import_matelas, semaine_excel, id_fichier)
                    fichiers_crees.extend(fichiers_matelas)
                    self.logger.info(f"Export matelas terminé: {len(fichiers_matelas)} fichier(s)")
                except Exception as e:
                    self.logger.error(f"Erreur lors de l'export matelas: {e}")
            
            # Export des sommiers
            if pre_import_sommiers:
                try:
                    from excel_sommier_import_utils import ExcelSommierImporter
                    importer_sommiers = ExcelSommierImporter(template_path_sommiers)
                    fichiers_sommiers = importer_sommiers.import_configurations(pre_import_sommiers, semaine_excel, id_fichier)
                    fichiers_crees.extend(fichiers_sommiers)
                    self.logger.info(f"Export sommiers terminé: {len(fichiers_sommiers)} fichier(s)")
                except Exception as e:
                    self.logger.error(f"Erreur lors de l'export sommiers: {e}")
            
            return fichiers_crees
        except Exception as e:
            self.logger.error(f"Erreur lors de l'export Excel global: {e}")
            return []


# Instance globale pour l'interface
backend_interface = BackendInterface() 