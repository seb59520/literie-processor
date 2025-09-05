import re
import logging

logger = logging.getLogger(__name__)

def extraire_titre_depuis_produits(articles_llm: list) -> str:
    """
    Extrait le titre (Mr ou Mme) depuis les descriptions des produits (matelas/sommiers)
    
    Args:
        articles_llm (list): Liste des articles extraits par le LLM
        
    Returns:
        str: Titre extrait ("Mr", "Mme") ou chaîne vide si aucun titre trouvé
    """
    if not articles_llm:
        return ""
    
    # Rechercher dans toutes les descriptions d'articles
    for article in articles_llm:
        if isinstance(article, dict):
            description = article.get('description', '')
            if description:
                # Rechercher "Mr" ou "Mme" dans la description
                match = re.search(r'\b(Mr|Mme)\b', description, re.IGNORECASE)
                if match:
                    titre = match.group(1).upper()
                    # Normaliser "MR" en "Mr" et "MME" en "Mme"
                    if titre == "MR":
                        return "Mr"
                    elif titre == "MME":
                        return "Mme"
                    return titre
    
    return ""

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
        "code_client": None,
        "titre": None  # Nouveau champ pour Mr/Mme
    }
    
    try:
        # Récupération des données client depuis llm_data
        if isinstance(llm_data, dict) and "client" in llm_data:
            client_raw = llm_data["client"]
            if isinstance(client_raw, dict):
                # Extraction du nom
                if "nom" in client_raw and client_raw["nom"]:
                    nom_complet = client_raw["nom"].strip()
                    client_data["nom"] = nom_complet
                
                # Extraction de l'adresse
                if "adresse" in client_raw and client_raw["adresse"]:
                    adresse_complete = client_raw["adresse"].strip()
                    # Traitement de l'adresse : on ne garde que ce qui suit le code postal
                    client_data["adresse"] = extraire_ville_adresse(adresse_complete)
                
                # Extraction du code client
                if "code_client" in client_raw and client_raw["code_client"]:
                    client_data["code_client"] = client_raw["code_client"].strip()
        
        # Extraction du titre depuis les descriptions des produits
        articles_llm = []
        if isinstance(llm_data, dict):
            for key in llm_data:
                if isinstance(llm_data[key], list):
                    articles_llm.extend(llm_data[key])
        
        client_data["titre"] = extraire_titre_depuis_produits(articles_llm)
        
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