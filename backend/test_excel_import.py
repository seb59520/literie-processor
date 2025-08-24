"""
Script de test pour l'importateur Excel
Démonstration de l'utilisation de ExcelMatelasImporter
"""

import json
from excel_import_utils import ExcelMatelasImporter
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_excel_import():
    """
    Test complet de l'importateur Excel avec données réelles du pré-import
    """
    
    # Création de l'importateur
    importer = ExcelMatelasImporter()
    
    # Exemple de configurations JSON (simulant les données réelles du pré-import)
    configurations = [
        {
            # Champs client
            "Client_D1": "DUPONT Jean",
            "Adresse_D3": "123 Rue de la Paix, 75001 Paris",
            
            # Champs commande et dates
            "numero_D2": "CMD001",
            "semaine_D5": "28_2024",
            "lundi_D6": "08/07/2024",
            "vendredi_D7": "12/07/2024",
            
            # Champs matelas
            "Hauteur_D22": "20",
            
            # Champs détection
            "dosseret_tete_C8": "X",
            
            # Champs quantité
            "jumeaux_C10": "X",
            "jumeaux_D10": "320x200",
            "1piece_C11": "",
            "1piece_D11": "",
            
            # Champs housse et matière
            "HSimple_polyester_C13": "",
            "HSimple_polyester_D13": "",
            "HSimple_tencel_C14": "",
            "HSimple_tencel_D14": "",
            "HSimple_autre_C15": "",
            "HSimple_autre_D15": "",
            "Hmat_polyester_C17": "",
            "Hmat_polyester_D17": "",
            "Hmat_tencel_C18": "",
            "Hmat_tencel_D18": "",
            "Hmat_luxe3D_C19": "X",
            "Hmat_luxe3D_D19": "2 x (160 x 200)",
            
            # Champs poignées
            "poignees_C20": "X",
            
            # Champs dimensions
            "dimension_housse_D23": "160 x 200",
            "longueur_D24": "200",
            "decoupe_noyau_D25": "160 x 200",
            
            # Champs noyau et fermeté
            "LN_Ferme_C28": "",
            "LN_Medium_C29": "X",
            "LM7z_Ferme_C30": "",
            "LM7z_Medium_C31": "",
            "LM3z_Ferme_C32": "",
            "LM3z_Medium_C33": "",
            "MV_Ferme_C34": "",
            "MV_Medium_C35": "",
            "MV_Confort_C36": "",
            "MR_Ferme_C37": "",
            "MR_Medium_C38": "",
            "MR_Confort_C39": "",
            "SL43_Ferme_C40": "",
            "SL43_Medium_C41": "",
            
            # Champs surmatelas
            "Surmatelas_C45": "",
            
            # Champs opérations
            "emporte_client_C57": "X",
            "fourgon_C58": "",
            "transporteur_C59": "",
        },
        {
            # Champs client
            "Client_D1": "MARTIN Marie",
            "Adresse_D3": "456 Avenue des Champs, 69000 Lyon",
            
            # Champs commande et dates
            "numero_D2": "CMD002",
            "semaine_D5": "28_2024",
            "lundi_D6": "08/07/2024",
            "vendredi_D7": "12/07/2024",
            
            # Champs matelas
            "Hauteur_D22": "18",
            
            # Champs détection
            "dosseret_tete_C8": "",
            
            # Champs quantité
            "jumeaux_C10": "",
            "jumeaux_D10": "",
            "1piece_C11": "X",
            "1piece_D11": "140x190",
            
            # Champs housse et matière
            "HSimple_polyester_C13": "X",
            "HSimple_polyester_D13": "140 x 190",
            "HSimple_tencel_C14": "",
            "HSimple_tencel_D14": "",
            "HSimple_autre_C15": "",
            "HSimple_autre_D15": "",
            "Hmat_polyester_C17": "",
            "Hmat_polyester_D17": "",
            "Hmat_tencel_C18": "",
            "Hmat_tencel_D18": "",
            "Hmat_luxe3D_C19": "",
            "Hmat_luxe3D_D19": "",
            
            # Champs poignées
            "poignees_C20": "",
            
            # Champs dimensions
            "dimension_housse_D23": "140 x 190",
            "longueur_D24": "190",
            "decoupe_noyau_D25": "140 x 190",
            
            # Champs noyau et fermeté
            "LN_Ferme_C28": "",
            "LN_Medium_C29": "",
            "LM7z_Ferme_C30": "",
            "LM7z_Medium_C31": "",
            "LM3z_Ferme_C32": "",
            "LM3z_Medium_C33": "",
            "MV_Ferme_C34": "",
            "MV_Medium_C35": "",
            "MV_Confort_C36": "X",
            "MR_Ferme_C37": "",
            "MR_Medium_C38": "",
            "MR_Confort_C39": "",
            "SL43_Ferme_C40": "",
            "SL43_Medium_C41": "",
            
            # Champs surmatelas
            "Surmatelas_C45": "",
            
            # Champs opérations
            "emporte_client_C57": "",
            "fourgon_C58": "X",
            "transporteur_C59": "",
        }
    ]
    
    try:
        # Import des configurations
        logger.info("Début de l'import Excel...")
        created_files = importer.import_configurations(configurations, "S28", "2024")
        
        logger.info("Import terminé avec succès!")
        logger.info(f"Fichiers créés: {len(created_files)}")
        
        for i, filepath in enumerate(created_files, 1):
            logger.info(f"Fichier {i}: {filepath}")
            
        return created_files
        
    except Exception as e:
        logger.error(f"Erreur lors de l'import: {e}")
        raise

def test_with_json_file(json_file_path: str, semaine: str, id_client: str):
    """
    Test avec un fichier JSON existant
    
    Args:
        json_file_path: Chemin vers le fichier JSON
        semaine: Code semaine
        id_client: ID du client
    """
    try:
        # Lecture du fichier JSON
        with open(json_file_path, 'r', encoding='utf-8') as f:
            configurations = json.load(f)
        
        logger.info(f"Chargement de {len(configurations)} configurations depuis {json_file_path}")
        
        # Import
        importer = ExcelMatelasImporter()
        created_files = importer.import_configurations(configurations, semaine, id_client)
        
        logger.info(f"Import terminé. {len(created_files)} fichier(s) créé(s)")
        return created_files
        
    except FileNotFoundError:
        logger.error(f"Fichier JSON non trouvé: {json_file_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Erreur de décodage JSON: {e}")
        raise
    except Exception as e:
        logger.error(f"Erreur lors de l'import: {e}")
        raise

if __name__ == "__main__":
    # Test avec les données d'exemple
    print("=== Test avec données réelles du pré-import ===")
    test_excel_import()
    
    # Test avec un fichier JSON (décommentez si vous avez un fichier JSON)
    # print("\n=== Test avec fichier JSON ===")
    # test_with_json_file("test_housse.json", "S02", "5678") 