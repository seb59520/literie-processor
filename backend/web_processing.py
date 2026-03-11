#!/usr/bin/env python3
"""
Module de traitement web pour l'application MATELAS.
Encapsule la logique de backend_interface.py sans dépendance PyQt6.
Utilisé par les endpoints API JSON de main.py.
"""

import os
import sys
import json
import shutil
import logging
import math
import re
import time
import asyncio
import tempfile
from typing import List, Dict, Optional
from pathlib import Path

import fitz  # PyMuPDF

from backend.date_utils import get_week_dates
from backend.pre_import_utils import (
    creer_pre_import, creer_pre_import_sommier, valider_pre_import,
    detect_mode_mise_a_disposition
)
from backend.main import call_llm
from backend.excel_import_utils import ExcelMatelasImporter
from backend.file_validation import FileValidator
from backend.client_utils import extraire_donnees_client
from backend.article_utils import (
    contient_dosseret_ou_tete, contient_fermeture_liaison,
    contient_surmatelas, filtrer_articles_matelas
)
from backend.operation_utils import mots_operation_trouves
from backend.matelas_utils import detecter_noyau_matelas
from backend.hauteur_utils import calculer_hauteur_matelas
from backend.fermete_utils import detecter_fermete_matelas
from backend.housse_utils import detecter_type_housse
from backend.matiere_housse_utils import detecter_matiere_housse
from backend.poignees_utils import detecter_poignees
from backend.dimensions_utils import detecter_dimensions
from backend.dimensions_sommiers import detecter_dimensions_sommier, calculer_dimensions_sommiers
from backend.sommier_utils import (
    detecter_type_sommier, calculer_hauteur_sommier,
    detecter_materiau_sommier, detecter_type_relaxation_sommier,
    detecter_type_telecommande_sommier, detecter_soufflet_mousse_sommier,
    detecter_facon_moderne_sommier, detecter_tapissier_a_lattes_sommier,
    detecter_lattes_francaises_sommier, segmenter_pieds_sommier,
    detecter_options_sommier
)
from backend.sommier_analytics_utils import analyser_caracteristiques_sommier
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
from config import config

logger = logging.getLogger(__name__)


class WebProcessor:
    """Traitement des PDFs pour l'API web, sans dépendance GUI."""

    def __init__(self):
        self.file_validator = FileValidator({
            'max_file_size_mb': 100,
            'min_file_size_kb': 1,
            'max_pages': 200,
            'min_text_length': 50,
            'max_text_length': 1000000,
            'allowed_extensions': ['.pdf'],
            'allowed_mime_types': ['application/pdf', 'application/x-pdf', 'text/pdf']
        })

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def process_uploaded_files(
        self,
        file_paths: List[str],
        semaine_prod: int,
        annee_prod: int,
        commande_client: List[str],
        semaine_matelas: Optional[int] = None,
        annee_matelas: Optional[int] = None,
        semaine_sommiers: Optional[int] = None,
        annee_sommiers: Optional[int] = None,
        exclusions: Optional[Dict] = None,
        progress_callback=None,
    ) -> Dict:
        """
        Traite une liste de fichiers PDF et retourne les résultats structurés + fichiers Excel.
        """
        start_time = time.time()
        results = []
        errors = []

        # Validation
        validation_results = self.file_validator.validate_multiple_files(file_paths)
        validation_summary = self.file_validator.get_validation_summary(validation_results)

        valid_files = []
        for fp, vr in zip(file_paths, validation_results):
            if vr.is_valid:
                valid_files.append(fp)
            else:
                msg = f"Fichier invalide {fp}: {'; '.join(vr.errors)}"
                errors.append(msg)
                results.append({'file': fp, 'success': False, 'error': msg})

        if not valid_files:
            return {
                'results': results,
                'validation_summary': validation_summary,
                'total_processing_time': time.time() - start_time,
                'success': False,
                'error': 'Aucun fichier valide à traiter',
            }

        all_pre_imports: List[Dict] = []
        total_files = len(valid_files)

        for idx, file_path in enumerate(valid_files):
            try:
                if progress_callback:
                    progress_callback({
                        'current_file': idx + 1,
                        'total_files': total_files,
                        'filename': os.path.basename(file_path),
                    })

                file_exclusions = self._get_file_exclusions(file_path, exclusions)
                cc = commande_client[idx] if idx < len(commande_client) else ""

                result = await self._process_single_file(
                    file_path, semaine_prod, annee_prod, cc,
                    semaine_matelas=semaine_matelas, annee_matelas=annee_matelas,
                    semaine_sommiers=semaine_sommiers, annee_sommiers=annee_sommiers,
                    exclusions=file_exclusions,
                )

                if result.get('status') == 'success' and result.get('pre_import'):
                    all_pre_imports.extend(result['pre_import'])

                results.append(result)
            except Exception as e:
                logger.error(f"Erreur traitement {os.path.basename(file_path)}: {e}")
                errors.append(str(e))
                results.append({
                    'filename': os.path.basename(file_path),
                    'status': 'error',
                    'error': str(e),
                })

        # Export Excel global
        fichiers_excel = []
        if all_pre_imports:
            try:
                fichiers_excel = self._export_excel_global(
                    all_pre_imports, semaine_prod, annee_prod,
                    semaine_matelas=semaine_matelas, annee_matelas=annee_matelas,
                    semaine_sommiers=semaine_sommiers, annee_sommiers=annee_sommiers,
                )
            except Exception as e:
                logger.error(f"Erreur export Excel global: {e}")

        for r in results:
            if r.get('status') == 'success':
                r['fichiers_excel'] = fichiers_excel

        return {
            'results': results,
            'errors': errors,
            'total_files': len(file_paths),
            'successful_files': sum(1 for r in results if r.get('status') == 'success'),
            'failed_files': len(errors),
            'fichiers_excel': fichiers_excel,
            'total_pre_imports': len(all_pre_imports),
            'total_processing_time': time.time() - start_time,
        }

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _get_file_exclusions(self, file_path: str, exclusions: Optional[Dict]) -> Dict:
        if not exclusions:
            return {}
        if file_path in exclusions:
            return exclusions[file_path]
        basename = os.path.basename(file_path)
        for key, exc_data in exclusions.items():
            if os.path.basename(key) == basename:
                return exc_data
        return {}

    async def _process_single_file(
        self, file_path: str, semaine_prod: int, annee_prod: int,
        commande_client: str,
        semaine_matelas: Optional[int] = None, annee_matelas: Optional[int] = None,
        semaine_sommiers: Optional[int] = None, annee_sommiers: Optional[int] = None,
        exclusions: Optional[Dict] = None,
    ) -> Dict:
        filename = os.path.basename(file_path)
        try:
            # Extract text
            with open(file_path, "rb") as f:
                pdf_bytes = f.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            text = "\n".join(page.get_text() for page in doc)
            doc.close()

            file_size = len(pdf_bytes)

            # Split large texts
            parts = self._split_large_text(text)

            # LLM calls
            from backend.cost_tracker import cost_tracker
            session_id = cost_tracker.start_session(
                file_name=filename, file_path=file_path, file_size=file_size
            )

            llm_results = []
            for part in parts:
                try:
                    llm_result = await call_llm(
                        part, file_name=filename, file_size=file_size, session_id=session_id
                    )
                    if llm_result:
                        llm_results.append(llm_result)
                except Exception as e:
                    logger.warning(f"Erreur LLM pour une partie: {e}")

            try:
                cost_tracker.end_session(session_id, success=True)
            except Exception:
                pass

            logger.info(f"[WEB] llm_results count: {len(llm_results)}")
            for i, r in enumerate(llm_results):
                logger.info(f"[WEB] llm_result[{i}] type={type(r).__name__} len={len(str(r))} first200={str(r)[:200]}")
                logger.info(f"[WEB] llm_result[{i}] last200={str(r)[-200:]}")

            merged_llm = self._merge_llm_results(llm_results)

            # Parse LLM JSON
            articles_llm = []
            matelas_articles = []
            sommier_articles = []
            pieds_articles = []
            donnees_client = {}
            llm_data = {}

            if merged_llm:
                cleaned = self._clean_and_parse_json(merged_llm)
                if cleaned:
                    try:
                        llm_data = json.loads(cleaned)
                        if not isinstance(llm_data, dict):
                            llm_data = {}
                    except json.JSONDecodeError:
                        llm_data = {}

            logger.info(f"[WEB] merged_llm length: {len(merged_llm) if merged_llm else 0}")
            if merged_llm:
                logger.info(f"[WEB] merged_llm first 500 chars: {merged_llm[:500]}")

            if llm_data:
                logger.info(f"[WEB] llm_data keys: {list(llm_data.keys())}")
                donnees_client = extraire_donnees_client(llm_data, raw_text=text)
                for key in llm_data:
                    if isinstance(llm_data[key], list):
                        articles_llm.extend(llm_data[key])
                        if key.lower() == "articles":
                            for article in llm_data[key]:
                                art_type = article.get('type', '').lower()
                                desc = article.get('description', '').upper()
                                if art_type == 'matelas' or ('MATELAS' in desc and art_type not in ('sommier', 'pieds', 'accessoire', 'remise')):
                                    matelas_articles.append(article)
                                elif art_type == 'sommier' or ('SOMMIER' in desc and art_type not in ('matelas', 'pieds', 'accessoire', 'remise')):
                                    sommier_articles.append(article)
                                elif art_type == 'pieds' or ('PIEDS' in desc and art_type not in ('matelas', 'sommier', 'accessoire', 'remise')):
                                    pieds_articles.append(article)
            else:
                logger.warning(f"[WEB] llm_data is empty! JSON parsing failed")

            logger.info(f"[WEB] matelas_articles: {len(matelas_articles)}, sommier_articles: {len(sommier_articles)}, pieds_articles: {len(pieds_articles)}")

            # Detect mattress cores
            noyaux_matelas = detecter_noyau_matelas(matelas_articles)
            types_sommiers = detecter_type_sommier(sommier_articles) if sommier_articles else []
            logger.info(f"[WEB] noyaux_matelas: {noyaux_matelas}, types_sommiers: {types_sommiers}")

            # Production weeks
            sem_mat = semaine_matelas or semaine_prod
            an_mat = annee_matelas or annee_prod
            sem_som = semaine_sommiers or semaine_prod
            an_som = annee_sommiers or annee_prod

            if not exclusions:
                exclusions = {}
            create_matelas = not exclusions.get('matelas_excluded', False)
            create_sommiers = not exclusions.get('sommier_excluded', False)

            # Build configurations
            configurations_matelas = self._create_configurations_matelas(
                noyaux_matelas, matelas_articles, sem_mat, an_mat, commande_client
            ) if create_matelas else []

            configurations_sommiers = self._create_configurations_sommiers(
                types_sommiers, sommier_articles, sem_som, an_som, commande_client
            ) if create_sommiers else []

            # Pieds
            configurations_pieds = []
            for article in pieds_articles:
                pied = segmenter_pieds_sommier(article.get('description', ''), quantite_article=article.get('quantite', 1))
                configurations_pieds.append(pied)

            # Pre-import
            pre_import_data = []
            if (configurations_matelas or configurations_sommiers) and donnees_client:
                contient_dosseret_tete = contient_dosseret_ou_tete(articles_llm)
                mots_op = mots_operation_trouves(articles_llm, text)
                fermeture = contient_fermeture_liaison(articles_llm)

                # Mise à disposition detection
                donnees_client["devis_text"] = text
                descriptions = "\n".join([a.get("description", "") for a in llm_data.get('articles', [])])
                mode_global = detect_mode_mise_a_disposition(text)
                mode_desc = detect_mode_mise_a_disposition(descriptions)
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

                if configurations_matelas:
                    pre_import_data.extend(creer_pre_import(
                        configurations_matelas, donnees_client,
                        contient_dosseret_tete, mots_op, fermeture
                    ))

                if configurations_sommiers:
                    pre_import_data.extend(creer_pre_import_sommier(
                        configurations_sommiers, donnees_client,
                        mots_operation_trouves=mots_op,
                        articles_llm=articles_llm,
                        contient_dosseret_tete=contient_dosseret_tete,
                    ))

            semaine_annee = f"{semaine_prod}_{annee_prod}"
            lundi, vendredi = get_week_dates(semaine_prod, annee_prod)

            return {
                'filename': filename,
                'status': 'success',
                'extraction_stats': {
                    'nb_caracteres': len(text),
                    'nb_mots': len(text.split()),
                },
                'configurations_matelas': configurations_matelas,
                'configurations_sommiers': configurations_sommiers,
                'configurations_pieds': configurations_pieds,
                'donnees_client': donnees_client,
                'pre_import': pre_import_data,
                'calcul_date': {
                    'semaine_annee': semaine_annee,
                    'lundi': lundi,
                    'vendredi': vendredi,
                    'commande_client': commande_client,
                },
            }

        except Exception as e:
            logger.error(f"Erreur traitement {filename}: {e}")
            return {'filename': filename, 'status': 'error', 'error': str(e)}

    # ------------------------------------------------------------------
    # Text splitting & LLM result merging
    # ------------------------------------------------------------------

    def _split_large_text(self, text: str, max_chars: int = 15000) -> List[str]:
        if len(text) <= max_chars:
            return [text]
        parts = []
        current = ""
        for line in text.split('\n'):
            if len(current) + len(line) + 1 > max_chars and current:
                parts.append(current.strip())
                current = line
            else:
                current = current + '\n' + line if current else line
        if current.strip():
            parts.append(current.strip())
        logger.info(f"Texte divisé en {len(parts)} parties")
        return parts

    def _merge_llm_results(self, results: List[str]) -> str:
        if not results:
            return ""
        if len(results) == 1:
            return results[0]

        parsed = []
        for r in results:
            try:
                parsed.append(json.loads(r))
            except json.JSONDecodeError:
                cleaned = self._clean_and_parse_json(r)
                try:
                    parsed.append(json.loads(cleaned))
                except Exception:
                    pass

        if not parsed:
            return ""

        merged = parsed[0].copy()
        for p in parsed[1:]:
            if 'articles' in p:
                merged.setdefault('articles', []).extend(p['articles'])
            for k, v in p.items():
                if k != 'articles' and k not in merged:
                    merged[k] = v

        return json.dumps(merged, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------
    # JSON cleaning
    # ------------------------------------------------------------------

    def _clean_and_parse_json(self, raw_text: str) -> str:
        if not raw_text or not raw_text.strip():
            return ""

        # Direct parse
        try:
            json.loads(raw_text)
            return raw_text
        except json.JSONDecodeError:
            pass

        # Strip markdown fences
        cleaned = re.sub(r'```(?:json|JSON)?\s*', '', raw_text)
        cleaned = re.sub(r'\s*```', '', cleaned).strip()
        try:
            json.loads(cleaned)
            return cleaned
        except json.JSONDecodeError as e:
            logger.warning(f"[WEB] clean_json after fence strip failed: {e}")
            logger.info(f"[WEB] cleaned last 100: {cleaned[-100:]}")

        # Extract JSON block
        m = re.search(r'\{.*\}', cleaned, re.DOTALL)
        if m:
            try:
                json.loads(m.group(0))
                return m.group(0)
            except json.JSONDecodeError as e:
                logger.warning(f"[WEB] clean_json extract block failed: {e}")

        # Fix common syntax errors
        fixed = re.sub(r'\}\s*"', '}, "', cleaned)
        fixed = re.sub(r'\}\s*\{', '}, {', fixed)
        fixed = re.sub(r'\]\s*"', '], "', fixed)
        fixed = re.sub(r',\s*([}\]])', r'\1', fixed)
        try:
            json.loads(fixed)
            return fixed
        except json.JSONDecodeError:
            pass

        return raw_text

    # ------------------------------------------------------------------
    # Mattress configuration builder
    # ------------------------------------------------------------------

    def _create_configurations_matelas(
        self, noyaux: List[Dict], articles: List[Dict],
        semaine: int, annee: int, commande_client: str
    ) -> List[Dict]:
        configs = []
        idx = 1
        for noyau_info in noyaux:
            if noyau_info['noyau'] == 'INCONNU':
                continue
            article_idx = noyau_info['index'] - 1
            if article_idx >= len(articles):
                continue
            article = articles[article_idx]
            quantite = article.get('quantite', 1)
            description = article.get('description', '')

            dims_str = article.get('dimensions')
            dims = detecter_dimensions(dims_str) if dims_str else detecter_dimensions(description)

            is_jumeaux = (
                article.get('est_jumeaux') is True
                or article.get('type_matelas') == 'jumeaux'
                or 'jumeaux' in description.lower()
            )

            q_float = float(quantite) if isinstance(quantite, (int, float, str)) else 1.0
            q_int = max(1, int(q_float))

            iterations = 1 if (is_jumeaux and q_float > 1) else q_int
            q_per_config = q_float if (is_jumeaux and q_float > 1) else 1

            for _ in range(iterations):
                mat_housse = self._detect_matiere_housse(description)
                cfg = {
                    "matelas_index": idx,
                    "noyau": noyau_info['noyau'],
                    "quantite": q_per_config,
                    "hauteur": calculer_hauteur_matelas(noyau_info['noyau']),
                    "fermete": detecter_fermete_matelas(description),
                    "housse": detecter_type_housse(description),
                    "matiere_housse": mat_housse,
                    "poignees": self._detect_poignees(description, mat_housse),
                    "dimensions": dims,
                    "semaine_annee": f"{semaine}_{annee}",
                    "lundi": get_week_dates(semaine, annee)[0],
                    "vendredi": get_week_dates(semaine, annee)[1],
                    "commande_client": commande_client,
                    "description": description,
                }
                if article.get('titre_cote'):
                    cfg["titre_cote"] = article['titre_cote']
                if article.get('information'):
                    cfg["information"] = article['information']

                self._add_housse_dimensions(cfg)
                configs.append(cfg)
                idx += 1

        return configs

    def _detect_matiere_housse(self, description: str) -> str:
        return detecter_matiere_housse(description)

    def _detect_poignees(self, description: str, matiere_housse: str) -> str:
        type_housse = detecter_type_housse(description)
        if matiere_housse == "TENCEL LUXE 3D":
            return "NON"
        if type_housse == "MATELASSEE" and "TENCEL" in matiere_housse:
            return "OUI"
        return detecter_poignees(description)

    # ------------------------------------------------------------------
    # Sommier configuration builder
    # ------------------------------------------------------------------

    def _create_configurations_sommiers(
        self, types_sommiers: List[Dict], articles: List[Dict],
        semaine: int, annee: int, commande_client: str
    ) -> List[Dict]:
        configs = []
        for type_info in types_sommiers:
            if type_info['type_sommier'] == 'INCONNU':
                continue
            art_idx = type_info['index'] - 1
            if art_idx >= len(articles):
                continue
            article = articles[art_idx]
            quantite = article.get('quantite', 1)
            description = article.get('description', '')

            dims_str = article.get('dimensions')
            dims = detecter_dimensions_sommier(dims_str) if dims_str else detecter_dimensions_sommier(description)
            dim_sommier = calculer_dimensions_sommiers(dims) if dims else None
            caracteristiques = analyser_caracteristiques_sommier(description)

            cfg = {
                "sommier_index": type_info['index'],
                "type_sommier": type_info['type_sommier'],
                "quantite": quantite,
                "hauteur": calculer_hauteur_sommier(type_info['type_sommier']),
                "materiau": detecter_materiau_sommier(description),
                "dimensions": dims,
                "dimension_sommier": dim_sommier,
                "type_relaxation_sommier": detecter_type_relaxation_sommier(description),
                "type_telecommande_sommier": detecter_type_telecommande_sommier(description),
                "soufflet_mousse": detecter_soufflet_mousse_sommier(description),
                "facon_moderne": detecter_facon_moderne_sommier(description),
                "tapissier_a_lattes": detecter_tapissier_a_lattes_sommier(description),
                "lattes_francaises": detecter_lattes_francaises_sommier(description),
                "semaine_annee": f"{semaine}_{annee}",
                "lundi": get_week_dates(semaine, annee)[0],
                "vendredi": get_week_dates(semaine, annee)[1],
                "commande_client": commande_client,
                "description": description,
                "sommier_dansunlit": caracteristiques["sommier_dansunlit"],
                "sommier_pieds": caracteristiques["sommier_pieds"],
                "pieds_segmentes": segmenter_pieds_sommier(description, quantite_article=quantite),
                "options_sommier": detecter_options_sommier(description),
            }
            configs.append(cfg)

        return configs

    # ------------------------------------------------------------------
    # Housse dimensions
    # ------------------------------------------------------------------

    def _add_housse_dimensions(self, cfg: Dict):
        try:
            noyau = cfg.get("noyau", "")
            quantite = cfg.get("quantite", 1)
            dims = cfg.get("dimensions")
            matiere = cfg.get("matiere_housse", "")
            dimension_housse = None

            if not dims:
                return

            largeur = dims.get("largeur", 0)
            longueur = dims.get("longueur", 0)

            if noyau == 'LATEX NATUREL' and matiere in LN_MATIERE_MAP:
                val = get_valeur_latex_naturel(largeur, matiere)
                if matiere == "POLYESTER":
                    dimension_housse = f"{val}"
                else:
                    prefixe = "4 x " if quantite == 2 else ("2 x " if quantite == 1 else f"{int(quantite) * 2} x ")
                    dimension_housse = f"{prefixe}{val}"
                hl = get_latex_naturel_longueur_housse_value(longueur, matiere)
                if hl is not None:
                    cfg["dimension_housse_longueur"] = hl

            elif noyau == 'LATEX MIXTE 7 ZONES' and matiere in LM7Z_MATIERE_MAP:
                val = get_valeur_latex_mixte7zones(largeur, matiere)
                if matiere == "POLYESTER":
                    dimension_housse = f"{val}"
                else:
                    prefixe = "4 x " if quantite == 2 else ("2 x " if quantite == 1 else f"{int(quantite) * 2} x ")
                    dimension_housse = f"{prefixe}{val}"
                hl = get_latex_mixte7zones_longueur_housse_value(longueur, matiere)
                if hl is not None:
                    cfg["dimension_housse_longueur"] = hl

            elif noyau == 'MOUSSE RAINUREE 7 ZONES' and matiere in MR7Z_MATIERE_MAP:
                val = get_valeur_mousse_rainuree7zones(largeur, matiere)
                if matiere == "POLYESTER":
                    dimension_housse = f"{val}"
                else:
                    prefixe = "4 x " if quantite == 2 else ("2 x " if quantite == 1 else f"{int(quantite) * 2} x ")
                    dimension_housse = f"{prefixe}{val}"
                hl = get_mousse_rainuree7zones_longueur_housse_value(longueur, matiere)
                if hl is not None:
                    cfg["dimension_housse_longueur"] = hl

            elif noyau == 'SELECT 43' and matiere:
                dimension_housse = get_select43_display_value(largeur, matiere, quantite)
                hl = get_select43_longueur_housse_value(longueur, matiere)
                if hl is not None:
                    cfg["dimension_housse_longueur"] = hl

            elif noyau == 'LATEX RENFORCE' and matiere:
                dimension_housse = get_latex_renforce_display_value(largeur, matiere, quantite)
                hl = get_latex_renforce_longueur_housse(longueur, matiere)
                if hl is not None:
                    cfg["dimension_housse_longueur"] = hl

            elif noyau == 'MOUSSE VISCO':
                dimension_housse = get_mousse_visco_value(largeur, matiere)
                hl = get_mousse_visco_longueur_value(longueur)
                if hl is not None:
                    cfg["dimension_housse_longueur"] = hl

            if dimension_housse:
                cfg["dimension_housse"] = dimension_housse

            # Dimension literie
            largeur_arr = int(math.ceil(largeur / 10.0) * 10)
            longueur_arr = int(math.ceil(longueur / 10.0) * 10)

            if (largeur_arr - largeur) > 3.0 or (longueur_arr - longueur) > 3.0:
                lf, lof = largeur, longueur
            else:
                lf, lof = largeur_arr, longueur_arr

            if quantite == 2:
                lf *= 2
            cfg["dimension_literie"] = f"{int(lf)}x{int(lof)}"

            # Decoupe noyau
            fermete = cfg.get("fermete", "")
            ld, lod = calcul_decoupe_noyau(noyau, fermete, largeur, longueur)
            cfg["decoupe_noyau"] = f"{str(ld).replace(',', '.')} x {str(lod).replace(',', '.')}"

        except Exception as e:
            logger.error(f"Erreur calcul dimensions housse: {e}")

    # ------------------------------------------------------------------
    # Excel export
    # ------------------------------------------------------------------

    def _export_excel_global(
        self, pre_import_data: List[Dict], semaine_prod: int, annee_prod: int,
        semaine_matelas: Optional[int] = None, annee_matelas: Optional[int] = None,
        semaine_sommiers: Optional[int] = None, annee_sommiers: Optional[int] = None,
    ) -> List[str]:
        sem_mat = semaine_matelas or semaine_prod
        an_mat = annee_matelas or annee_prod
        sem_som = semaine_sommiers or semaine_prod
        an_som = annee_sommiers or annee_prod

        sem_mat_s = str(sem_mat).zfill(2)
        sem_som_s = str(sem_som).zfill(2)

        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        tpl_matelas = os.path.join(script_dir, "template", "template_matelas.xlsx")
        tpl_sommiers = os.path.join(script_dir, "template", "template_sommier.xlsx")

        logger.info(f"[EXPORT] pre_import_data count: {len(pre_import_data)}")
        for pi in pre_import_data:
            logger.info(f"[EXPORT] item type_article={pi.get('type_article', 'NONE')}, noyau={pi.get('noyau', 'NONE')}, Client={pi.get('Client_D1', '?')}")

        pre_mat = [x for x in pre_import_data if x.get('type_article') != 'sommier']
        pre_som = [x for x in pre_import_data if x.get('type_article') == 'sommier']

        logger.info(f"[EXPORT] pre_mat count: {len(pre_mat)}, pre_som count: {len(pre_som)}")

        fichiers = []

        if pre_mat:
            noyau_order = config.get_noyau_order()
            logger.info(f"[SORT] noyau_order from config: {noyau_order}")
            logger.info(f"[SORT] pre_mat noyaux BEFORE sort: {[pi.get('noyau', '???') for pi in pre_mat]}")
            if noyau_order:
                def sort_key(pi):
                    n = pi.get('noyau', '').replace(' 7 ZONES', '')
                    norm = [x.replace(' 7 ZONES', '') for x in noyau_order]
                    try:
                        idx = norm.index(n)
                    except ValueError:
                        try:
                            idx = noyau_order.index(pi.get('noyau', ''))
                        except ValueError:
                            idx = len(noyau_order) + 1
                    logger.info(f"[SORT] noyau='{pi.get('noyau', '')}' -> sort_key={idx}")
                    return idx
                pre_mat = sorted(pre_mat, key=sort_key)
            logger.info(f"[SORT] pre_mat noyaux AFTER sort: {[pi.get('noyau', '???') for pi in pre_mat]}")

            imp = ExcelMatelasImporter(tpl_matelas)
            fichiers.extend(imp.import_configurations(pre_mat, f"S{sem_mat_s}", str(an_mat)))

        if pre_som:
            from backend.excel_sommier_import_utils import ExcelSommierImporter
            imp = ExcelSommierImporter(tpl_sommiers)
            fichiers.extend(imp.import_configurations(pre_som, f"S{sem_som_s}", str(an_som)))

        return fichiers


# Singleton
web_processor = WebProcessor()
