#!/usr/bin/env python3
"""
Test pour vérifier la séquence d'écriture dans les fichiers Excel
"""

import sys
import os
sys.path.append('backend')

from excel_import_utils import ExcelMatelasImporter

def test_excel_sequence():
    """Test la séquence d'écriture dans les fichiers Excel"""
    
    # Configuration de test
    semaine = "S06"
    id_fichier = "2025"
    
    # Crée l'importateur
    importer = ExcelMatelasImporter()
    
    # Simule plusieurs commandes successives
    commandes = [
        # Commande 1: Dumortier (2 configurations)
        [
            {
                "Client_D1": "Mr et Mme DUMORTIER BRUNO & CHRISTELLE",
                "Adresse_D3": "HAZEBROUCK",
                "numero_D2": "75",
                "semaine_D5": "6_2025",
                "lundi_D6": "2025-02-10",
                "vendredi_D7": "2025-02-14",
                "Hauteur_D22": 10,
                "1piece_C11": "X",
                "1piece_D11": "160x200",
                "MV_Medium_C35": "X",
                "fourgon_C58": "X"
            },
            {
                "Client_D1": "Mr et Mme DUMORTIER BRUNO & CHRISTELLE",
                "Adresse_D3": "HAZEBROUCK",
                "numero_D2": "75",
                "semaine_D5": "6_2025",
                "lundi_D6": "2025-02-10",
                "vendredi_D7": "2025-02-14",
                "Hauteur_D22": 10,
                "jumeaux_C10": "X",
                "jumeaux_D10": "160x210",
                "MV_Medium_C35": "X",
                "fourgon_C58": "X"
            }
        ],
        # Commande 2: Solutions Canapés (1 configuration)
        [
            {
                "Client_D1": "SARL SOLUTIONS CANAPES",
                "Adresse_D3": "SECLIN",
                "numero_D2": "75",
                "semaine_D5": "6_2025",
                "lundi_D6": "2025-02-10",
                "vendredi_D7": "2025-02-14",
                "Hauteur_D22": 10,
                "1piece_C11": "X",
                "1piece_D11": "180x200",
                "LN_Ferme_C28": "X",
                "emporte_client_C57": "X"
            }
        ],
        # Commande 3: Deversenne (1 configuration) - devrait aller en I-J
        [
            {
                "Client_D1": "Mr DEVERSENNE CLAUDE",
                "Adresse_D3": "SAINT JANS CAPPEL",
                "numero_D2": "75",
                "semaine_D5": "6_2025",
                "lundi_D6": "2025-02-10",
                "vendredi_D7": "2025-02-14",
                "Hauteur_D22": 9,
                "jumeaux_C10": "X",
                "jumeaux_D10": "160x200",
                "MR_Ferme_C37": "X",
                "emporte_client_C57": "X"
            }
        ]
    ]
    
    print("=== Test de séquence d'écriture Excel ===")
    
    for i, commande in enumerate(commandes):
        print(f"\n--- Commande {i+1} ---")
        try:
            fichiers_crees = importer.import_configurations(commande, semaine, id_fichier)
            print(f"Fichiers créés: {fichiers_crees}")
        except Exception as e:
            print(f"Erreur: {e}")
    
    print("\n=== Test terminé ===")

if __name__ == "__main__":
    test_excel_sequence() 