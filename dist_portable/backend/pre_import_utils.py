import logging
import re
import unicodedata

logger = logging.getLogger(__name__)

def creer_pre_import(configurations_matelas, donnees_client, contient_dosseret_tete=False, mots_operation_trouves=None, fermeture_liaison=False):
    """
    Crée un JSON de pré-import à partir des configurations matelas et des données client
    
    Args:
        configurations_matelas: Liste des configurations matelas
        donnees_client: Dictionnaire contenant les données client
        contient_dosseret_tete: Booléen indiquant si DOSSERET ou TETE a été détecté
        mots_operation_trouves: Liste des mots d'opération trouvés dans le document
        fermeture_liaison: Booléen indiquant si "Fermeture de liaison" a été détecté
        
    Returns:
        list: Liste de dictionnaires de pré-import, un par configuration matelas
    """
    pre_import_data = []
    
    # Vérifications de sécurité
    if not configurations_matelas:
        logger.warning("configurations_matelas est vide ou None")
        return []
    
    if not donnees_client:
        logger.warning("donnees_client est vide ou None")
        return []
    
    if not isinstance(configurations_matelas, list):
        logger.warning(f"configurations_matelas n'est pas une liste: {type(configurations_matelas)}")
        return []
    
    if not isinstance(donnees_client, dict):
        logger.warning(f"donnees_client n'est pas un dictionnaire: {type(donnees_client)}")
        return []
    
    try:
        for i, config in enumerate(configurations_matelas):
            # Vérification de sécurité pour chaque configuration
            if not config or not isinstance(config, dict):
                logger.warning(f"Configuration {i} invalide: {config}")
                continue
                
            # Récupération des valeurs de base
            quantite = config.get("quantite", 1)
            housse = config.get("housse", "")
            matiere_housse = config.get("matiere_housse", "")
            poignees = config.get("poignees", "")
            noyau = config.get("noyau", "")
            fermete = config.get("fermete", "")
            surmatelas = config.get("surmatelas", False)
            mots_operations = mots_operation_trouves or []
            
            # Récupération des dimensions (pour référence)
            dimensions = config.get("dimensions", {})
            if not isinstance(dimensions, dict):
                dimensions = {}
            largeur = dimensions.get("largeur", "")
            longueur = dimensions.get("longueur", "")
            
            # Récupération des autres valeurs
            dimension_housse = config.get("dimension_housse", "")
            dimension_housse_longueur = config.get("dimension_housse_longueur", "")
            decoupe_noyau = config.get("decoupe_noyau", "")
            dimension_literie = config.get("dimension_literie", "")  # Utiliser la valeur calculée
            
            pre_import_item = {
                # Champs client
                "Client_D1": donnees_client.get("nom", ""),
                "Adresse_D3": donnees_client.get("adresse", ""),
                "MrMME_D4": donnees_client.get("titre", ""),  # Nouveau champ pour Mr/Mme
                
                # Champs commande et dates
                "numero_D2": config.get("commande_client", ""),
                "semaine_D5": config.get("semaine_annee", ""),
                "lundi_D6": config.get("lundi", ""),
                "vendredi_D7": config.get("vendredi", ""),
                
                # Champs matelas
                "Hauteur_D22": config.get("hauteur", ""),
                
                # Champs détection
                "dosseret_tete_C8": "X" if contient_dosseret_tete else "",
                
                # Champs quantité
                "jumeaux_C10": "X" if quantite == 2 else "",
                "jumeaux_D10": dimension_literie if quantite == 2 else "",
                "1piece_C11": "X" if quantite == 1 else "",
                "1piece_D11": dimension_literie if quantite == 1 else "",
                
                # Champs housse et matière
                "HSimple_polyester_C13": "X" if housse == "SIMPLE" and matiere_housse == "POLYESTER" else "",
                "HSimple_tencel_C14": "X" if housse == "SIMPLE" and matiere_housse == "TENCEL" else "",
                "HSimple_autre_C15": "X" if housse == "SIMPLE" and matiere_housse == "AUTRE" else "",
                "Hmat_polyester_C17": "X" if housse in ["MATELASSÉE", "MATELASSEE"] and matiere_housse == "POLYESTER" else "",
                "Hmat_tencel_C18": "X" if housse in ["MATELASSÉE", "MATELASSEE"] and matiere_housse == "TENCEL" else "",
                "Hmat_luxe3D_C19": "X" if housse in ["MATELASSÉE", "MATELASSEE"] and matiere_housse == "TENCEL LUXE 3D" else "",
                
                # Champs poignées
                "poignees_C20": "X" if poignees == "OUI" else "",
                
                # Champs dimensions
                "dimension_housse_D23": dimension_housse,
                "longueur_D24": dimension_housse_longueur,
                "decoupe_noyau_D25": decoupe_noyau,
                
                # Champs noyau et fermeté
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
                
                # Champs surmatelas
                "Surmatelas_C45": "X" if surmatelas else "",
                
                # Champs fermeture de liaison
                "FDL_C51": "X" if fermeture_liaison else "",
                
                # Champs opérations
                "emporte_client_C57": "X" if "ENLEVEMENT" in mots_operations else "",
                "fourgon_C58": "X" if "LIVRAISON" in mots_operations else "",
                "transporteur_C59": "X" if "EXPEDITION" in mots_operations else "",
                
                # Informations de référence
                "matelas_index": config.get("matelas_index", i + 1),
                "noyau": config.get("noyau", ""),
                "quantite": config.get("quantite", 1)
            }
            
            # Ajout des champs D conditionnels pour les housses
            # Utiliser les dimensions brutes (largeur x longueur) au lieu de dimension_literie
            dimension_brute = f"{largeur} x {longueur}" if largeur and longueur else ""
            
            # Fonction pour ajouter le préfixe quantité si nécessaire
            def format_dimension_with_quantity(dim, qty):
                if qty > 1 and dim:
                    return f"{qty} x ({dim})"
                return dim
            
            if pre_import_item["HSimple_polyester_C13"] == "X":
                pre_import_item["HSimple_polyester_D13"] = format_dimension_with_quantity(dimension_brute, quantite)
            if pre_import_item["HSimple_tencel_C14"] == "X":
                pre_import_item["HSimple_tencel_D14"] = format_dimension_with_quantity(dimension_brute, quantite)
            if pre_import_item["HSimple_autre_C15"] == "X":
                pre_import_item["HSimple_autre_D15"] = format_dimension_with_quantity(dimension_brute, quantite)
            if pre_import_item["Hmat_polyester_C17"] == "X":
                pre_import_item["Hmat_polyester_D17"] = format_dimension_with_quantity(dimension_brute, quantite)
            if pre_import_item["Hmat_tencel_C18"] == "X":
                pre_import_item["Hmat_tencel_D18"] = format_dimension_with_quantity(dimension_brute, quantite)
            if pre_import_item["Hmat_luxe3D_C19"] == "X":
                pre_import_item["Hmat_luxe3D_D19"] = format_dimension_with_quantity(dimension_brute, quantite)
            
            pre_import_data.append(pre_import_item)
            logger.info(f"Pré-import créé pour matelas {i + 1}: {pre_import_item}")
        
        logger.info(f"Pré-import créé avec succès: {len(pre_import_data)} éléments")
        return pre_import_data
        
    except Exception as e:
        logger.error(f"Erreur lors de la création du pré-import: {e}")
        return []

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
                "SL43_Ferme_C40", "SL43_Medium_C41", "Surmatelas_C45", "FDL_C51", "emporte_client_C57",
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