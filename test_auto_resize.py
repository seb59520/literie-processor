#!/usr/bin/env python3
"""
Script de test pour le redimensionnement automatique des colonnes Excel
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.excel_import_utils import ExcelMatelasImporter
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_auto_resize():
    """
    Teste le redimensionnement automatique avec des données de test
    """
    print("=== Test du redimensionnement automatique des colonnes ===")
    
    # Créer l'importateur avec auto-resize activé
    importer = ExcelMatelasImporter(auto_resize=True)
    
    # Données de test avec des contenus de longueurs variées
    test_configs = [
        {
            "Client_D1": "Client avec un nom très très long pour tester le redimensionnement",
            "Adresse_D3": "123 Rue de la Longue Adresse qui dépasse largement la largeur standard",
            "MrMME_D4": "MR",
            "numero_D2": "CMD-2024-001234-EXTRA-LONG",
            "semaine_D5": "S01",
            "lundi_D6": "2024-01-15",
            "vendredi_D7": "2024-01-19",
            "Hauteur_D22": "25 cm avec détails supplémentaires",
            "dimension_housse_D23": "160x200 cm dimension extra détaillée",
            "longueur_D24": "200 cm avec spécifications techniques complètes",
            "jumeaux_C10": True,
            "HSimple_polyester_C13": True,
            "Hmat_luxe3D_C19": True,
            "poignees_C20": True,
            "LN_Ferme_C28": True,
        },
        {
            "Client_D1": "Client 2",
            "Adresse_D3": "Adresse courte",
            "MrMME_D4": "MME", 
            "numero_D2": "CMD-002",
            "semaine_D5": "S01",
            "Hauteur_D22": "20",
            "jumeaux_C11": True,
            "HSimple_tencel_C14": True,
            "MV_Medium_C35": True,
        }
    ]
    
    try:
        print(f"Test avec {len(test_configs)} configurations...")
        
        # Importer les configurations
        created_files = importer.import_configurations(
            configurations=test_configs,
            semaine="S01", 
            id_fichier="TEST"
        )
        
        print(f"✅ Test réussi!")
        print(f"Fichiers créés avec redimensionnement automatique:")
        for file in created_files:
            print(f"  - {file}")
        
        # Test avec auto-resize désactivé pour comparaison
        print("\n=== Test sans redimensionnement pour comparaison ===")
        importer_no_resize = ExcelMatelasImporter(auto_resize=False)
        
        created_files_no_resize = importer_no_resize.import_configurations(
            configurations=test_configs,
            semaine="S01",
            id_fichier="NO_RESIZE"
        )
        
        print(f"Fichiers créés sans redimensionnement:")
        for file in created_files_no_resize:
            print(f"  - {file}")
            
        print(f"\n✅ Tous les tests terminés avec succès!")
        print(f"Comparez les fichiers pour voir la différence:")
        print(f"- Avec redimensionnement: {created_files[0] if created_files else 'Aucun'}")
        print(f"- Sans redimensionnement: {created_files_no_resize[0] if created_files_no_resize else 'Aucun'}")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        logger.error(f"Test échoué: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_auto_resize()
    sys.exit(0 if success else 1)