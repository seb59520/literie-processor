import logging
import math
import re
import unicodedata
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


DIMENSION_PATTERN = re.compile(r"(\d{2,3})\s*/\s*(\d{2,3})\s*/\s*(\d{2,3})")
TETE_PATTERN = re.compile(r"T[ÊE]TE", re.IGNORECASE)
DOS_PATTERN = re.compile(r"DOS+ERET", re.IGNORECASE)
CHEVET_PATTERN = re.compile(r"CHEVET", re.IGNORECASE)
PIEDS_CUBIQUE_PATTERN = re.compile(r"PIEDS?\s+CUBIQUE", re.IGNORECASE)
PIEDS_CYLINDRE_PATTERN = re.compile(r"PIEDS?\s+CYLINDRE", re.IGNORECASE)
PLATINE_PATTERN = re.compile(r"PLATINE\s+DE\s+RE", re.IGNORECASE)
PATIN_FEUTRE_PATTERN = re.compile(r"PATINS?\s+FEUTRE", re.IGNORECASE)
PATIN_CARRELAGE_PATTERN = re.compile(r"PATINS?\s+CARRELAGE", re.IGNORECASE)
PATIN_TEFLON_PATTERN = re.compile(r"PATINS?\s+T[ÉE]FLON", re.IGNORECASE)
MATERIAU_PATTERNS = {
    "FRÊNE": re.compile(r"FR[ÊE]NE", re.IGNORECASE),
    "HÊTRE": re.compile(r"H[ÊE]TRE", re.IGNORECASE),
    "TAPISSIER": re.compile(r"TAPISSIER", re.IGNORECASE),
    "MÉTAL": re.compile(r"M[ÉE]TAL|ACIER", re.IGNORECASE),
}


def _normalize_article_text(text: str) -> str:
    if not text:
        return ""
    return unicodedata.normalize("NFKD", text).replace("\n", " ")


def _extract_dimension_tuple(text: str) -> Optional[Tuple[int, int, int]]:
    if not text:
        return None
    match = DIMENSION_PATTERN.search(text)
    if not match:
        return None
    try:
        return tuple(int(match.group(i)) for i in range(1, 4))
    except ValueError:
        return None


def _dimension_tuple_to_mm(values: Tuple[int, int, int]) -> Dict[str, int]:
    largeur, longueur, hauteur = values
    return {"largeur": largeur, "longueur": longueur, "hauteur": hauteur}


def _format_dimensions_mm(values: Dict[str, int]) -> str:
    if not values:
        return ""
    return f"{values['largeur'] * 10} X {values['longueur'] * 10} X {values['hauteur'] * 10}"


def _detect_relaxation(text: str) -> str:
    if "RELAXATION" in text:
        return "RELAXATION"
    if "MANUEL" in text:
        return "MANUEL"
    if "MOTORIS" in text or "MOTORISE" in text:
        return "MOTORISE"
    if "FIXE" in text:
        return "FIXE"
    return ""


def _detect_telecommande(text: str) -> str:
    if "RADIO" in text:
        return "TELECOMMANDE SANS FIL"
    if "TELECOMMAND" in text:
        return "TELECOMMANDE FILAIRE"
    return "NON"


def _detect_materiau(text: str) -> str:
    for name, pattern in MATERIAU_PATTERNS.items():
        if pattern.search(text):
            return name
    return ""


def _extract_options_from_texts(texts: List[str]) -> Dict[str, str]:
    options = defaultdict(str)
    accessoires = []
    for raw in texts:
        normalized = _normalize_article_text(raw)
        upper = normalized.upper()
        if TETE_PATTERN.search(upper):
            accessoires.append({"type": "tete", "description": raw.strip()})
        if DOS_PATTERN.search(upper):
            accessoires.append({"type": "dosseret", "description": raw.strip()})
        if CHEVET_PATTERN.search(upper):
            accessoires.append({"type": "chevet", "description": raw.strip()})
        if PIEDS_CUBIQUE_PATTERN.search(upper):
            options["pieds_cubique"] = "OUI"
            accessoires.append({"type": "pieds_cubique", "description": raw.strip()})
        if PIEDS_CYLINDRE_PATTERN.search(upper):
            options["pieds_cylindre"] = "OUI"
            accessoires.append({"type": "pieds_cylindre", "description": raw.strip()})
        if "PIEDS CENTRAUX" in upper or "PIED CENTRAL" in upper:
            options["pieds_centraux"] = "OUI"
        if PLATINE_PATTERN.search(upper):
            options["platine_reunion"] = "OUI"
        if PATIN_FEUTRE_PATTERN.search(upper):
            options["patins_feutre"] = "OUI"
        if PATIN_CARRELAGE_PATTERN.search(upper):
            options["patins_carrelage"] = "OUI"
        if PATIN_TEFLON_PATTERN.search(upper):
            options["patins_teflon"] = "OUI"
        if "STRUCTURE PAREMENT" in upper or "MÉTRAGE" in upper:
            options["finition_paremente"] = "OUI"
    return {"options": dict(options), "accessoires": accessoires}


def _merge_options(options_a: Dict[str, str], options_b: Dict[str, str]) -> Dict[str, str]:
    merged = dict(options_a)
    for key, value in options_b.items():
        if value:
            merged[key] = value
    return merged

def extract_mr_mme_from_description(description):
    """
    Extrait MR ou MME depuis la description du matelas
    Cherche après le dernier tiret "-" s'il contient Mr/Mme
    Args:
        description (str): Description complète du matelas
    Returns:
        str: "MR", "MME" ou chaîne vide si aucun titre trouvé
    """
    if not description:
        return ""
    
    # Chercher le dernier segment après un tiret "-"
    segments = description.split('-')
    if len(segments) > 1:
        # Prendre le dernier segment et le nettoyer
        last_segment = segments[-1].strip()
        
        # Chercher Mr/Mme dans ce segment (avec ou sans Gauche/Droite)
        match = re.search(r'\b(Mr|MR|Mme|MME)\b', last_segment, re.IGNORECASE)
        if match:
            raw_result = match.group(1)
            # Normaliser: Mr -> MR, Mme -> MME
            if raw_result.lower() == 'mr':
                return 'MR'
            elif raw_result.lower() == 'mme':
                return 'MME'
            else:
                return raw_result.upper()
    
    # Si pas de tiret, chercher Mr/Mme directement dans la description (fallback)
    match = re.search(r'\b(Mr|MR|Mme|MME)\b', description.strip(), re.IGNORECASE)
    if match:
        raw_result = match.group(1)
        if raw_result.lower() == 'mr':
            return 'MR'
        elif raw_result.lower() == 'mme':
            return 'MME'
        else:
            return raw_result.upper()
    
    return ""

def extract_cote_from_description(description):
    """
    Extrait la mention Gauche/Droite depuis la description du matelas
    Cherche après le dernier tiret "-" s'il contient Gauche/Droite
    Args:
        description (str): Description complète du matelas
    Returns:
        str: "GAUCHE", "DROITE" ou chaîne vide si aucune mention trouvée
    """
    if not description:
        return ""
    
    # Chercher le dernier segment après un tiret "-"
    segments = description.split('-')
    if len(segments) > 1:
        # Prendre le dernier segment et le nettoyer
        last_segment = segments[-1].strip()
        
        # Chercher Gauche/Droite dans ce segment
        match = re.search(r'\b(Gauche|Droite|GAUCHE|DROITE)\b', last_segment, re.IGNORECASE)
        if match:
            return match.group(1).upper()
    
    # Si pas de tiret, chercher dans toute la description (fallback)
    match = re.search(r'\b(Gauche|Droite|GAUCHE|DROITE)\b', description.strip(), re.IGNORECASE)
    if match:
        return match.group(1).upper()
    
    return ""

def extract_mr_mme_from_all_fields(config):
    """
    Teste tous les champs possibles d'une configuration pour trouver MR/MME
    Args:
        config (dict): Configuration matelas complète
    Returns:
        str: "MR", "MME" ou chaîne vide si aucun titre trouvé
    """
    # PRIORITÉ 1: Vérifier d'abord le champ titre_cote directement (extraction LLM)
    titre_cote = config.get("titre_cote", "").strip()
    if titre_cote:
        # Normaliser directement si c'est juste MR/MME/Mr/Mme
        normalized = titre_cote.upper()
        if normalized in ['MR', 'MME']:
            return normalized
        elif normalized in ['MONSIEUR', 'M.', 'MRS']:
            return 'MR'  
        elif normalized in ['MADAME', 'MME.', 'MMES']:
            return 'MME'
        # Sinon utiliser le pattern matching
        result = extract_mr_mme_from_description(titre_cote)
        if result:
            return result
    
    # Liste des autres champs qui peuvent contenir MR/MME  
    fields_to_check = [
        "titre_cote_simple",
        # PRIORITÉ 2: Descriptions et textes d'articles
        "description", "nom", "type", "information", 
        "autres_caracteristiques", "matelas_description", "article_description",
        "description_article", "article_complet", "article_line", 
        "description_complete", "texte_article", "denomination"
    ]
    
    for field in fields_to_check:
        value = config.get(field, "")
        if value:
            result = extract_mr_mme_from_description(str(value))
            if result:
                return result
    
    return ""

def extract_cote_from_all_fields(config):
    """
    Teste tous les champs possibles d'une configuration pour trouver GAUCHE/DROITE
    Args:
        config (dict): Configuration matelas complète
    Returns:
        str: "GAUCHE", "DROITE" ou chaîne vide si aucun côté trouvé
    """
    # PRIORITÉ 1: Vérifier d'abord le champ titre_cote directement
    titre_cote = config.get("titre_cote", "").strip()
    if titre_cote:
        result = extract_cote_from_description(titre_cote)
        if result:
            return result
    
    # Liste des autres champs qui peuvent contenir Gauche/Droite
    fields_to_check = [
        "titre_cote_simple",
        "description", "nom", "type", "information", 
        "autres_caracteristiques", "matelas_description", "article_description",
        "description_article", "article_complet", "article_line", 
        "description_complete", "texte_article", "denomination"
    ]
    
    for field in fields_to_check:
        value = config.get(field, "")
        if value:
            result = extract_cote_from_description(str(value))
            if result:
                return result
    
    return ""

def create_mr_mme_with_cote(config):
    """
    Crée le champ MrMME_D4 fusionné avec le côté (Gauche/Droite)
    Args:
        config (dict): Configuration matelas complète
    Returns:
        str: "MR", "MME", "MR GAUCHE", "MME DROITE", etc. ou chaîne vide
    """
    mr_mme = extract_mr_mme_from_all_fields(config)
    cote = extract_cote_from_all_fields(config)
    
    if mr_mme and cote:
        return f"{mr_mme} {cote}"
    elif mr_mme:
        return mr_mme
    else:
        return ""

class PreImportBuilder:
    """Construit les structures de pré-import pour matelas et sommiers."""

    def __init__(self, logger_instance: Optional[logging.Logger] = None):
        self.logger = logger_instance or logging.getLogger(__name__)

    def build_matelas_pre_import(
        self,
        configurations_matelas: List[Dict],
        donnees_client: Dict,
        contient_dosseret_tete: bool = False,
        mots_operation_trouves: Optional[List[str]] = None,
        fermeture_liaison: bool = False,
    ) -> List[Dict]:
        pre_import_data = []

        if not configurations_matelas:
            self.logger.warning("configurations_matelas est vide ou None")
            return []

        if not donnees_client:
            self.logger.warning("donnees_client est vide ou None")
            return []

        if not isinstance(configurations_matelas, list):
            self.logger.warning(f"configurations_matelas n'est pas une liste: {type(configurations_matelas)}")
            return []

        if not isinstance(donnees_client, dict):
            self.logger.warning(f"donnees_client n'est pas un dictionnaire: {type(donnees_client)}")
            return []

        try:
            for i, config in enumerate(configurations_matelas):
                if not config or not isinstance(config, dict):
                    self.logger.warning(f"Configuration {i} invalide: {config}")
                    continue

                quantite = config.get("quantite", 1)
                housse = config.get("housse", "")
                matiere_housse = config.get("matiere_housse", "")
                poignees = config.get("poignees", "")
                noyau = config.get("noyau", "")
                fermete = config.get("fermete", "")
                surmatelas = config.get("surmatelas", False)
                mots_operations = mots_operation_trouves or []

                dimensions = config.get("dimensions", {})
                if not isinstance(dimensions, dict):
                    dimensions = {}
                largeur = dimensions.get("largeur", "")
                longueur = dimensions.get("longueur", "")

                dimension_housse = config.get("dimension_housse", "")
                dimension_housse_longueur = config.get("dimension_housse_longueur", "")
                decoupe_noyau = config.get("decoupe_noyau", "")
                dimension_literie = config.get("dimension_literie", "")

                pre_import_item = {
                    "Client_D1": donnees_client.get("nom", ""),
                    "Adresse_D3": donnees_client.get("adresse", ""),
                    "MrMME_D4": create_mr_mme_with_cote(config),
                    "numero_D2": config.get("commande_client", ""),
                    "semaine_D5": config.get("semaine_annee", ""),
                    "lundi_D6": config.get("lundi", ""),
                    "vendredi_D7": config.get("vendredi", ""),
                    "Hauteur_D22": config.get("hauteur", ""),
                    "dosseret_tete_C8": "X" if contient_dosseret_tete else "",
                    "jumeaux_C10": "X" if quantite == 2 else "",
                    "jumeaux_D10": dimension_literie if quantite == 2 else "",
                    "1piece_C11": "X" if quantite == 1 else "",
                    "1piece_D11": dimension_literie if quantite == 1 else "",
                    "HSimple_polyester_C13": "X" if housse == "SIMPLE" and matiere_housse == "POLYESTER" else "",
                    "HSimple_tencel_C14": "X" if housse == "SIMPLE" and matiere_housse == "TENCEL" else "",
                    "HSimple_autre_C15": "X" if housse == "SIMPLE" and matiere_housse == "AUTRE" else "",
                    "Hmat_polyester_C17": "X" if housse in ["MATELASSÉE", "MATELASSEE"] and matiere_housse == "POLYESTER" else "",
                    "Hmat_tencel_C18": "X" if housse in ["MATELASSÉE", "MATELASSEE"] and matiere_housse == "TENCEL" else "",
                    "Hmat_luxe3D_C19": "X" if housse in ["MATELASSÉE", "MATELASSEE"] and matiere_housse == "TENCEL LUXE 3D" else "",
                    "poignees_C20": "X" if poignees == "OUI" else "",
                    "dimension_housse_D23": dimension_housse,
                    "longueur_D24": dimension_housse_longueur,
                    "decoupe_noyau_D25": decoupe_noyau,
                    "LN_Ferme_C28": "X" if noyau == "LATEX NATUREL" and fermete == "FERME" else "",
                    "LN_Medium_C29": "X" if noyau == "LATEX NATUREL" and fermete == "MEDIUM" else "",
                    "LM7z_Ferme_C30": "X" if noyau == "LATEX MIXTE 7 ZONES" and fermete == "FERME" else "",
                    "LM7z_Medium_C31": "X" if noyau == "LATEX MIXTE 7 ZONES" and fermete == "MEDIUM" else "",
                    "LM3z_Ferme_C32": "X" if noyau == "LATEX MIXTE 3 ZONES" and fermete == "FERME" else "",
                    "LM3z_Medium_C33": "X" if noyau == "LATEX MIXTE 3 ZONES" and fermete == "MEDIUM" else "",
                    "MV_Ferme_C34": "X" if noyau == "MOUSSE VISCO" and fermete == "FERME" else "",
                    "MV_Medium_C35": "X" if noyau == "MOUSSE VISCO" and fermete == "MEDIUM" else "",
                    "MV_Confort_C36": "X" if noyau == "MOUSSE VISCO" and fermete == "CONFORT" else "",
                    "MR_Ferme_C37": "X" if "MOUSSE RAINUREE" in noyau and fermete == "FERME" else "",
                    "MR_Medium_C38": "X" if "MOUSSE RAINUREE" in noyau and fermete == "MEDIUM" else "",
                    "MR_Confort_C39": "X" if "MOUSSE RAINUREE" in noyau and fermete == "CONFORT" else "",
                    "SL43_Ferme_C40": "X" if noyau == "SELECT 43" and fermete == "FERME" else "",
                    "SL43_Medium_C41": "X" if noyau == "SELECT 43" and fermete == "MEDIUM" else "",
                    "LR_Ferme_C32": "X" if noyau == "LATEX RENFORCE" and fermete == "FERME" else "",
                    "LR_Medium_C33": "X" if noyau == "LATEX RENFORCE" and fermete == "MEDIUM" else "",
                    "LR_Confort_C44": "X" if noyau == "LATEX RENFORCE" and fermete == "CONFORT" else "",
                    "Surmatelas_C45": "X" if surmatelas else "",
                    "FDL_C51": "X" if fermeture_liaison else "",
                    "emporte_client_C57": "X" if "ENLEVEMENT" in mots_operations else "",
                    "fourgon_C58": "X" if "LIVRAISON" in mots_operations else "",
                    "transporteur_C59": "X" if "EXPEDITION" in mots_operations else "",
                    "matelas_index": config.get("matelas_index", i + 1),
                    "noyau": config.get("noyau", ""),
                    "quantite": config.get("quantite", 1)
                }

                dimension_brute = f"{largeur} x {longueur}" if largeur and longueur else ""

                if pre_import_item["HSimple_polyester_C13"] == "X":
                    pre_import_item["HSimple_polyester_D13"] = self._format_dimension_with_quantity(dimension_brute, quantite)
                if pre_import_item["HSimple_tencel_C14"] == "X":
                    pre_import_item["HSimple_tencel_D14"] = self._format_dimension_with_quantity(dimension_brute, quantite)
                if pre_import_item["HSimple_autre_C15"] == "X":
                    pre_import_item["HSimple_autre_D15"] = self._format_dimension_with_quantity(dimension_brute, quantite)
                if pre_import_item["Hmat_polyester_C17"] == "X":
                    pre_import_item["Hmat_polyester_D17"] = self._format_dimension_with_quantity(dimension_brute, quantite)
                if pre_import_item["Hmat_tencel_C18"] == "X":
                    pre_import_item["Hmat_tencel_D18"] = self._format_dimension_with_quantity(dimension_brute, quantite)
                if pre_import_item["Hmat_luxe3D_C19"] == "X":
                    pre_import_item["Hmat_luxe3D_D19"] = self._format_dimension_with_quantity(dimension_brute, quantite)

                pre_import_data.append(pre_import_item)
                self.logger.info(f"Pré-import créé pour matelas {i + 1}: {pre_import_item}")

            self.logger.info(f"Pré-import créé avec succès: {len(pre_import_data)} éléments")
            return pre_import_data

        except Exception as e:
            self.logger.error(f"Erreur lors de la création du pré-import: {e}")
            return []

    def build_sommier_pre_import(
        self,
        configurations_sommiers: List[Dict],
        donnees_client: Dict,
        mots_operation_list: Optional[List[str]] = None,
        articles_llm: Optional[List[Dict]] = None,
        contient_dosseret_tete: bool = False,  # Conservé pour compatibilité future
    ) -> List[Dict]:
        pre_import_data = []

        if not configurations_sommiers:
            self.logger.warning("configurations_sommiers est vide ou None")
            return []

        if not donnees_client:
            self.logger.warning("donnees_client est vide ou None")
            return []

        if not isinstance(configurations_sommiers, list):
            self.logger.warning(f"configurations_sommiers n'est pas une liste: {type(configurations_sommiers)}")
            return []

        if not isinstance(donnees_client, dict):
            self.logger.warning(f"donnees_client n'est pas un dictionnaire: {type(donnees_client)}")
            return []

        default_articles = articles_llm or []

        try:
            for i, config in enumerate(configurations_sommiers):
                if not config or not isinstance(config, dict):
                    self.logger.warning(f"Configuration sommier {i} invalide: {config}")
                    continue
                config_mots_operations = config.get('mots_operation_trouves') or []
                mots_operation = config_mots_operations or mots_operation_list or []
                article_payload = config.get('articles') or default_articles

                dimension_calculee = config.get('dimension_sommier') or self._calculer_dimensions_sommiers(config.get('dimensions', {}))
                pre_import_item = {
                    "Client_D1": donnees_client.get('nom', ''),
                    "Adresse_D3": donnees_client.get('adresse', ''),
                    "numero_D2": config.get('commande_client', ''),
                    "semaine_D5": config.get('semaine_annee', ''),
                    "lundi_D6": config.get('lundi', ''),
                    "vendredi_D7": config.get('vendredi', ''),
                    "Type_Sommier_D20": config.get('type_sommier', ''),
                    "Materiau_D25": config.get('materiau', ''),
                    "Hauteur_D30": str(config.get('hauteur', '')),
                    "Dimensions_D35": dimension_calculee or '',
                    "Dimension_Sommier_D36": dimension_calculee or '',
                    "Type_Relaxation_Sommier_D37": config.get('type_relaxation_sommier', ''),
                    "Type_Telecommande_Sommier_D38": config.get('type_telecommande_sommier', ''),
                    "Soufflet_Mousse_D39": config.get('soufflet_mousse', ''),
                    "Facon_Moderne_D40": config.get('facon_moderne', ''),
                    "Tapissier_A_Lattes_D41": config.get('tapissier_a_lattes', ''),
                    "Lattes_Francaises_D42": config.get('lattes_francaises', ''),
                    "Quantite_D43": str(config.get('quantite', 1)),
                    "Sommier_DansUnLit_D45": config.get('sommier_dansunlit', 'NON'),
                    "Sommier_Pieds_D50": config.get('sommier_pieds', 'NON'),
                    "emporte_client_C57": "X" if "ENLEVEMENT" in mots_operation else "",
                    "fourgon_C58": "X" if "LIVRAISON" in mots_operation else "",
                    "transporteur_C59": "X" if "EXPEDITION" in mots_operation else "",
                    "semaine_annee": config.get('semaine_annee', ''),
                    "lundi": config.get('lundi', ''),
                    "vendredi": config.get('vendredi', ''),
                    "commande_client": config.get('commande_client', ''),
                    "type_article": "sommier",
                    "sommier_index": config.get('sommier_index', i + 1),
                    "articles": article_payload
                }

                description_sommier = config.get('description', '')
                pre_import_item["description"] = description_sommier
                pre_import_item["MrMME_D4"] = create_mr_mme_with_cote(config)

                options = config.get('options_sommier', {})
                self._apply_sommier_options(pre_import_item, options, description_sommier)

                pre_import_data.append(pre_import_item)
                self.logger.info(f"Pré-import sommier créé pour sommier {i + 1}: {pre_import_item}")

            self.logger.info(f"Pré-import sommier créé avec succès: {len(pre_import_data)} éléments")
            return pre_import_data

        except Exception as e:
            self.logger.error(f"Erreur lors de la création du pré-import sommier: {e}")
            return []

    def _format_dimension_with_quantity(self, dimension: str, quantite) -> str:
        if quantite and quantite > 1 and dimension:
            return f"{quantite} x ({dimension})"
        return dimension

    def _calculer_dimensions_sommiers(self, dimensions: Dict) -> str:
        if not dimensions:
            return ""
        try:
            from backend.dimensions_sommiers import calculer_dimensions_sommiers
            resultat = calculer_dimensions_sommiers(dimensions)
            return resultat if resultat else ""
        except Exception as e:
            self.logger.error(f"Erreur lors du calcul des dimensions sommiers: {e}")
            return ""

    def _apply_sommier_options(self, pre_import_item: Dict, options: Dict, description_sommier: str) -> None:
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

        has_paremente = False
        if description_sommier:
            desc_upper = description_sommier.upper()
            desc_normalized = desc_upper.replace('É', 'E').replace('Ê', 'E')
            if ("STRUCTURE PAREMENTEE" in desc_normalized or
                "STRUCTURE PAREMENTÉE" in desc_upper or
                "PAREMENTE" in desc_normalized or
                "PAREMENTÉE" in desc_upper):
                has_paremente = True
                self.logger.info(f"PAREMENTEE détecté dans la description: {description_sommier[:100]}")

        for opt, champ in options_mapping.items():
            if has_paremente and opt in ['finition_multiplis', 'finition_multiplis_tv', 'finition_multiplis_l']:
                pre_import_item[champ] = ''
            elif opt == 'finition_paremente':
                if has_paremente:
                    pre_import_item[champ] = 'X'
                else:
                    pre_import_item[champ] = 'X' if options.get(opt) == 'OUI' else ''
            else:
                pre_import_item[champ] = 'X' if options.get(opt) == 'OUI' else ''


def _logistics_to_operations(logistics: Dict[str, bool]) -> List[str]:
    ops = []
    if logistics.get("pickup"):
        ops.append("ENLEVEMENT")
    if logistics.get("delivery"):
        ops.append("LIVRAISON")
    if logistics.get("transporteur"):
        ops.append("EXPEDITION")
    return ops


def _strip_price_prefix(text: str) -> str:
    """Strip leading price/quantity prefix from article raw text.
    E.g. '2 001,50 2 001,50 1,00 SOMMIER...' -> 'SOMMIER...'
    Handles multiline: '0,00 0,00 0,00\\n1 977,69 1 977,69 1,00 SOMMIER...' -> 'SOMMIER...'
    """
    if not text:
        return text
    result = text
    # Strip multiple price prefix lines
    for _ in range(3):
        match = re.match(r"^[\d\s]+[,\.]\d{2}\s+[\d\s]+[,\.]\d{2}\s+[\d\s]+[,\.]\d{2}\s*\n?", result)
        if match:
            remaining = result[match.end():]
            if remaining.strip():
                result = remaining
            else:
                break
        else:
            break
    # Final strip of the last price prefix before the description text
    match = re.match(r"^[\d\s]+[,\.]\d{2}\s+[\d\s]+[,\.]\d{2}\s+[\d\s]+[,\.]\d{2}\s+", result)
    if match:
        result = result[match.end():]
    return result


def _build_config_from_order(order_doc: Dict) -> Dict:
    articles = [a.get("raw_text", "") for a in order_doc.get("articles", [])]
    combined_text = "\n".join(articles)
    normalized_combined = _normalize_article_text(combined_text).upper()

    dim_tuple = None
    for article in articles:
        dim_tuple = _extract_dimension_tuple(article)
        if dim_tuple:
            break
    dimensions_dict = _dimension_tuple_to_mm(dim_tuple) if dim_tuple else {}
    dimension_text = _format_dimensions_mm(dimensions_dict) if dimensions_dict else ""

    options_info = _extract_options_from_texts(articles)
    options = options_info["options"]
    accessoires = options_info["accessoires"]

    config = {
        "commande_client": order_doc.get("order_number", ""),
        "semaine_annee": order_doc.get("semaine", ""),
        "type_sommier": order_doc.get("order_type", "").upper(),
        "materiau": _detect_materiau(normalized_combined),
        "hauteur": str(dimensions_dict.get("hauteur", "")) if dimensions_dict else "",
        "dimensions": dimensions_dict,
        "dimension_sommier": dimension_text,
        "type_relaxation_sommier": _detect_relaxation(normalized_combined),
        "type_telecommande_sommier": _detect_telecommande(normalized_combined),
        "soufflet_mousse": "OUI" if "SOUFFLET" in normalized_combined else "",
        "facon_moderne": "OUI" if "MODERNE" in normalized_combined else "",
        "tapissier_a_lattes": "OUI" if "TAPISSIER" in normalized_combined and "LATTES" in normalized_combined else "",
        "lattes_francaises": "OUI" if "LATTES FRAN" in normalized_combined else "",
        "quantite": 1,
        "sommier_dansunlit": "OUI" if "DANS UN LIT" in normalized_combined or "LITERIE" in normalized_combined else "NON",
        "sommier_pieds": "OUI" if "SUR PIED" in normalized_combined or "PIEDS" in normalized_combined else "NON",
        "options_sommier": options,
        "articles": [{"description": _strip_price_prefix(txt)} for txt in articles],
        "accessoires_detectes": accessoires,
        "logistique_detectee": order_doc.get("logistics", {}),
        "mots_operation_trouves": _logistics_to_operations(order_doc.get("logistics", {})),
        "description": combined_text,
    }
    return config


def convert_pdf_orders_to_sommier_configs(order_documents: List[Dict]) -> List[Dict]:
    aggregated: Dict[str, Dict] = {}
    for order_doc in order_documents:
        config = _build_config_from_order(order_doc)
        key = config.get("commande_client") or order_doc.get("file_path")
        if key in aggregated:
            existing = aggregated[key]
            existing['articles'].extend(config['articles'])
            existing['accessoires_detectes'].extend(config['accessoires_detectes'])
            existing['options_sommier'] = _merge_options(existing['options_sommier'], config['options_sommier'])
            if not existing.get('dimension_sommier') and config.get('dimension_sommier'):
                existing['dimension_sommier'] = config['dimension_sommier']
                existing['dimensions'] = config['dimensions']
            existing['logistique_detectee'].update(config['logistique_detectee'])
            existing['mots_operation_trouves'] = list({*existing.get('mots_operation_trouves', []), *config.get('mots_operation_trouves', [])})
        else:
            aggregated[key] = config

    configs = []
    for idx, (_, cfg) in enumerate(sorted(aggregated.items()), start=1):
        cfg['sommier_index'] = idx
        configs.append(cfg)
    return configs

def creer_pre_import(configurations_matelas, donnees_client, contient_dosseret_tete=False, mots_operation_trouves=None, fermeture_liaison=False):
    builder = PreImportBuilder()
    return builder.build_matelas_pre_import(
        configurations_matelas,
        donnees_client,
        contient_dosseret_tete=contient_dosseret_tete,
        mots_operation_trouves=mots_operation_trouves,
        fermeture_liaison=fermeture_liaison
    )

def creer_pre_import_sommier(configurations_sommier, donnees_client, mots_operation_trouves=None, articles_llm=None, contient_dosseret_tete=False):
    builder = PreImportBuilder()
    return builder.build_sommier_pre_import(
        configurations_sommier,
        donnees_client,
        mots_operation_list=mots_operation_trouves,
        articles_llm=articles_llm,
        contient_dosseret_tete=contient_dosseret_tete
    )

def normalize_text(text: str) -> str:
    """Normalise le texte pour la recherche robuste (minuscules, suppression accents/espaces multiples)."""
    if not isinstance(text, str):
        return ""
    text_nfkd = unicodedata.normalize('NFKD', text)
    text_ascii = ''.join(c for c in text_nfkd if not unicodedata.combining(c))
    text_ascii = text_ascii.lower()
    text_ascii = re.sub(r"\s+", " ", text_ascii).strip()
    return text_ascii

def detect_mode_mise_a_disposition(text: str) -> dict:
    """Détecte le mode de mise à disposition à partir d'un texte global.

    Retourne un dict avec clés 'emporte_client_C57', 'fourgon_C58', 'transporteur_C59' valant "X" ou "".
    """
    norm = normalize_text(text)
    emporte = False
    fourgon = False
    transporteur = False

    # Enlèvement client
    patterns_enlev = [
        r"enlev\w*", r"enlevement", r"enlèvement", r"par vos soins", r"emporte(?:r|) client", r"retrait boutique",
    ]
    # Livraison fourgon interne
    patterns_fourgon = [
        r"fourgon", r"livraison", r"livre\w*", r"livre par nous", r"livraison magasin",
    ]
    # Transporteur/expédition
    patterns_transp = [
        r"transporteur", r"exped\w*", r"expédition", r"colis", r"palette", r"messagerie",
    ]

    def any_match(patterns):
        return any(re.search(p, norm) for p in patterns)

    if any_match(patterns_enlev):
        emporte = True
    if any_match(patterns_fourgon):
        fourgon = True
    if any_match(patterns_transp):
        transporteur = True

    return {
        "emporte_client_C57": "X" if emporte else "",
        "fourgon_C58": "X" if fourgon else "",
        "transporteur_C59": "X" if transporteur else "",
    }

def valider_pre_import(pre_import_data):
    """
    Valide la structure du pré-import
    
    Args:
        pre_import_data: Liste des données de pré-import
        
    Returns:
        bool: True si valide, False sinon
    """
    try:
        if not pre_import_data:
            logger.warning("Pré-import vide")
            return False
        
        for i, item in enumerate(pre_import_data):
            # Vérification des champs obligatoires de base
            required_fields = [
                "Client_D1", "Adresse_D3", "MrMME_D4", "Hauteur_D22", "numero_D2", "semaine_D5", 
                "lundi_D6", "vendredi_D7", "dosseret_tete_C8", "jumeaux_C10", "jumeaux_D10",
                "1piece_C11", "1piece_D11", "HSimple_polyester_C13", "HSimple_tencel_C14",
                "HSimple_autre_C15", "Hmat_polyester_C17", "Hmat_tencel_C18", "Hmat_luxe3D_C19",
                "poignees_C20", "dimension_housse_D23", "longueur_D24", "decoupe_noyau_D25",
                "LN_Ferme_C28", "LN_Medium_C29", "LM7z_Ferme_C30", "LM7z_Medium_C31",
                "LM3z_Ferme_C32", "LM3z_Medium_C33", "MV_Ferme_C34", "MV_Medium_C35",
                "MV_Confort_C36", "MR_Ferme_C37", "MR_Medium_C38", "MR_Confort_C39",
                "SL43_Ferme_C40", "SL43_Medium_C41", "LR_Ferme_C32", "LR_Medium_C33", "LR_Confort_C44", "Surmatelas_C45", "FDL_C51", "emporte_client_C57",
                "fourgon_C58", "transporteur_C59"
            ]
            
            for field in required_fields:
                if field not in item:
                    logger.warning(f"Champ manquant dans le pré-import {i}: {field}")
                    return False
            
            # Vérification que les valeurs ne sont pas vides
            if not item.get("Client_D1") or not item.get("Adresse_D3"):
                logger.warning(f"Données client manquantes dans le pré-import {i}")
                return False
        
        logger.info("Pré-import validé avec succès")
        return True
        
    except Exception as e:
        logger.error(f"Erreur lors de la validation du pré-import: {e}")
        return False

def formater_pre_import_pour_affichage(pre_import_data):
    """
    Formate les données de pré-import pour l'affichage dans l'interface
    
    Args:
        pre_import_data: Liste des données de pré-import
        
    Returns:
        dict: Données formatées pour l'affichage
    """
    try:
        formatted_data = {
            "nombre_elements": len(pre_import_data),
            "elements": []
        }
        
        for i, item in enumerate(pre_import_data):
            formatted_item = {
                "index": i + 1,
                "matelas_index": item.get("matelas_index", i + 1),
                "noyau": item.get("noyau", ""),
                "quantite": item.get("quantite", 1),
                "champs": {
                    "Client_D1": item.get("Client_D1", ""),
                    "Adresse_D3": item.get("Adresse_D3", ""),
                    "MrMME_D4": item.get("MrMME_D4", ""),
                    "numero_D2": item.get("numero_D2", ""),
                    "semaine_D5": item.get("semaine_D5", ""),
                    "lundi_D6": item.get("lundi_D6", ""),
                    "vendredi_D7": item.get("vendredi_D7", ""),
                    "Hauteur_D22": item.get("Hauteur_D22", ""),
                    "dosseret_tete_C8": item.get("dosseret_tete_C8", ""),
                    "jumeaux_C10": item.get("jumeaux_C10", ""),
                    "jumeaux_D10": item.get("jumeaux_D10", ""),
                    "1piece_C11": item.get("1piece_C11", ""),
                    "1piece_D11": item.get("1piece_D11", ""),
                    "HSimple_polyester_C13": item.get("HSimple_polyester_C13", ""),
                    "HSimple_tencel_C14": item.get("HSimple_tencel_C14", ""),
                    "HSimple_autre_C15": item.get("HSimple_autre_C15", ""),
                    "Hmat_polyester_C17": item.get("Hmat_polyester_C17", ""),
                    "Hmat_tencel_C18": item.get("Hmat_tencel_C18", ""),
                    "Hmat_luxe3D_C19": item.get("Hmat_luxe3D_C19", ""),
                    "poignees_C20": item.get("poignees_C20", ""),
                    "dimension_housse_D23": item.get("dimension_housse_D23", ""),
                    "longueur_D24": item.get("longueur_D24", ""),
                    "decoupe_noyau_D25": item.get("decoupe_noyau_D25", ""),
                    "LN_Ferme_C28": item.get("LN_Ferme_C28", ""),
                    "LN_Medium_C29": item.get("LN_Medium_C29", ""),
                    "LM7z_Ferme_C30": item.get("LM7z_Ferme_C30", ""),
                    "LM7z_Medium_C31": item.get("LM7z_Medium_C31", ""),
                    "LM3z_Ferme_C32": item.get("LM3z_Ferme_C32", ""),
                    "LM3z_Medium_C33": item.get("LM3z_Medium_C33", ""),
                    "MV_Ferme_C34": item.get("MV_Ferme_C34", ""),
                    "MV_Medium_C35": item.get("MV_Medium_C35", ""),
                    "MV_Confort_C36": item.get("MV_Confort_C36", ""),
                    "MR_Ferme_C37": item.get("MR_Ferme_C37", ""),
                    "MR_Medium_C38": item.get("MR_Medium_C38", ""),
                    "MR_Confort_C39": item.get("MR_Confort_C39", ""),
                    "SL43_Ferme_C40": item.get("SL43_Ferme_C40", ""),
                    "SL43_Medium_C41": item.get("SL43_Medium_C41", ""),
                    "LR_Ferme_C32": item.get("LR_Ferme_C32", ""),
                    "LR_Medium_C33": item.get("LR_Medium_C33", ""),
                    "LR_Confort_C44": item.get("LR_Confort_C44", ""),
                    "Surmatelas_C45": item.get("Surmatelas_C45", ""),
                    "FDL_C51": item.get("FDL_C51", ""),
                    "emporte_client_C57": item.get("emporte_client_C57", ""),
                    "fourgon_C58": item.get("fourgon_C58", ""),
                    "transporteur_C59": item.get("transporteur_C59", "")
                }
            }
            formatted_data["elements"].append(formatted_item)
        
        return formatted_data
        
    except Exception as e:
        logger.error(f"Erreur lors du formatage du pré-import: {e}")
        return {"nombre_elements": 0, "elements": []} 
