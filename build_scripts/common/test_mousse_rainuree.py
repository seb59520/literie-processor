#!/usr/bin/env python3
"""
Test pour vérifier la détection correcte de MOUSSE RAINUREE 7 ZONES
"""

import sys
import os
sys.path.append('backend')

from pre_import_utils import creer_pre_import

def test_mousse_rainuree():
    """Test la détection de MOUSSE RAINUREE 7 ZONES"""
    
    # Configuration de test
    configurations_matelas = [
        {
            "matelas_index": 1,
            "noyau": "MOUSSE RAINUREE 7 ZONES",
            "quantite": 2,
            "hauteur": 9,
            "fermete": "FERME",
            "housse": "MATELASSEE",
            "matiere_housse": "TENCEL LUXE 3D",
            "poignees": "OUI",
            "dimensions": {
                "largeur": 79.0,
                "longueur": 198.0,
                "hauteur": 20.0
            },
            "semaine_annee": "6_2025",
            "lundi": "2025-02-10",
            "vendredi": "2025-02-14",
            "commande_client": "75",
            "dimension_housse_longueur": 5.5,
            "dimension_housse": "4 x 91",
            "dimension_literie": "160x200",
            "decoupe_noyau": "79.0 x 198.0"
        }
    ]
    
    donnees_client = {
        "nom": "Mr DEVERSENNE CLAUDE",
        "adresse": "SAINT JANS CAPPEL",
        "code_client": "DEVECSA"
    }
    
    print("=== Test MOUSSE RAINUREE 7 ZONES ===")
    
    try:
        pre_import = creer_pre_import(configurations_matelas, donnees_client)
        
        if pre_import:
            config = pre_import[0]
            
            print(f"Noyau détecté: {config.get('noyau', 'N/A')}")
            print(f"Fermeté détectée: {configurations_matelas[0].get('fermete', 'N/A')}")
            print(f"MR_Ferme_C37: '{config.get('MR_Ferme_C37', 'VIDE')}'")
            print(f"MR_Medium_C38: '{config.get('MR_Medium_C38', 'VIDE')}'")
            print(f"MR_Confort_C39: '{config.get('MR_Confort_C39', 'VIDE')}'")
            
            if config.get('MR_Ferme_C37') == 'X':
                print("✅ SUCCÈS: MR_Ferme_C37 est correctement coché")
            else:
                print("❌ ÉCHEC: MR_Ferme_C37 n'est pas coché")
                
        else:
            print("❌ ÉCHEC: Aucun pré-import créé")
            
    except Exception as e:
        print(f"❌ ERREUR: {e}")
    
    print("\n=== Test terminé ===")

if __name__ == "__main__":
    test_mousse_rainuree() 