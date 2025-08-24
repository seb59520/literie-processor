import re
import logging

logger = logging.getLogger(__name__)

def extraire_donnees_client(llm_data: dict) -> dict:
    """
    Extrait les données client depuis l'extraction LLM et les traite
    
    Args:
        llm_data: Dictionnaire contenant les données extraites par le LLM
        
    Returns:
        dict: Dictionnaire contenant les données client traitées
    """
    client_data = {
        "nom": None,
        "adresse": None,
        "code_client": None
    }
    
    try:
        # Récupération des données client depuis llm_data
        if isinstance(llm_data, dict) and "client" in llm_data:
            client_raw = llm_data["client"]
            if isinstance(client_raw, dict):
                # Extraction du nom
                if "nom" in client_raw and client_raw["nom"]:
                    client_data["nom"] = client_raw["nom"].strip()
                
                # Extraction de l'adresse
                if "adresse" in client_raw and client_raw["adresse"]:
                    adresse_complete = client_raw["adresse"].strip()
                    # Traitement de l'adresse : on ne garde que ce qui suit le code postal
                    client_data["adresse"] = extraire_ville_adresse(adresse_complete)
                
                # Extraction du code client
                if "code_client" in client_raw and client_raw["code_client"]:
                    client_data["code_client"] = client_raw["code_client"].strip()
        
        logger.info(f"Données client extraites: {client_data}")
        return client_data
        
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction des données client: {e}")
        return client_data

def extraire_ville_adresse(adresse_complete: str) -> str:
    """
    Extrait la ville de l'adresse complète en ne gardant que ce qui suit le code postal
    
    Args:
        adresse_complete: Adresse complète (ex: "7 RUE DU MILIEU 59190 HAZEBROUCK")
        
    Returns:
        str: Ville extraite (ex: "HAZEBROUCK")
    """
    try:
        if not adresse_complete:
            return None
        
        # Pattern pour détecter un code postal français (5 chiffres)
        # Suivi d'un espace et de la ville
        pattern = r'\b\d{5}\s+(.+)$'
        match = re.search(pattern, adresse_complete)
        
        if match:
            ville = match.group(1).strip()
            logger.info(f"Ville extraite: '{ville}' depuis l'adresse: '{adresse_complete}'")
            return ville
        else:
            # Si pas de code postal détecté, on retourne l'adresse complète
            logger.warning(f"Aucun code postal détecté dans l'adresse: '{adresse_complete}'")
            return adresse_complete.strip()
            
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction de la ville: {e}")
        return adresse_complete.strip() if adresse_complete else None

def valider_donnees_client(client_data: dict) -> bool:
    """
    Valide que les données client sont cohérentes
    
    Args:
        client_data: Dictionnaire contenant les données client
        
    Returns:
        bool: True si les données sont valides, False sinon
    """
    try:
        # Vérification de base
        if not client_data:
            return False
        
        # Le nom est obligatoire
        if not client_data.get("nom"):
            logger.warning("Nom du client manquant")
            return False
        
        # L'adresse est obligatoire
        if not client_data.get("adresse"):
            logger.warning("Adresse du client manquante")
            return False
        
        logger.info("Données client validées avec succès")
        return True
        
    except Exception as e:
        logger.error(f"Erreur lors de la validation des données client: {e}")
        return False 