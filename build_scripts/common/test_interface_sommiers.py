#!/usr/bin/env python3
"""
Test de l'interface avec affichage des sommiers
"""

import sys
import os
sys.path.append('backend')

from backend_interface import BackendInterface

def test_interface_sommiers():
    """Test de l'interface avec des données sommiers"""
    print("=== Test interface avec sommiers ===")
    
    # Simulation de résultats avec matelas et sommiers
    result = {
        'filename': 'test_devis.pdf',
        'status': 'success',
        'configurations_matelas': [
            {
                'matelas_index': 1,
                'noyau': 'LATEX NATUREL',
                'quantite': 1,
                'hauteur': 18,
                'housse': 'SIMPLE',
                'matiere_housse': 'TENCEL',
                'fermete': 'MOYENNE',
                'poignees': 'AVEC',
                'dimensions': {'largeur': 160, 'longueur': 200},
                'type_article': 'matelas'
            }
        ],
        'configurations_sommiers': [
            {
                'sommier_index': 1,
                'type_sommier': 'SOMMIER À LATTES',
                'quantite': 1,
                'hauteur': 8,
                'materiau': 'BOIS',
                'sommier_dansunlit': 'OUI',
                'sommier_pieds': 'NON',
                'dimensions': {'largeur': 160, 'longueur': 200},
                'type_article': 'sommier'
            },
            {
                'sommier_index': 2,
                'type_sommier': 'SOMMIER TAPISSIER',
                'quantite': 1,
                'hauteur': 12,
                'materiau': 'TAPISSIER',
                'sommier_dansunlit': 'NON',
                'sommier_pieds': 'OUI',
                'dimensions': {'largeur': 180, 'longueur': 200},
                'type_article': 'sommier'
            }
        ],
        'pre_import': [
            # Pré-import matelas
            {
                'Client_D1': 'Test Client',
                'numero_D2': '0123456789',
                'semaine_D5': 'S01_2025',
                'noyau': 'LATEX NATUREL',
                'quantite': 1,
                'jumeaux_D10': '160x200',
                'Hauteur_D22': 18,
                'HSimple_tencel_C14': 'X',
                'type_article': 'matelas'
            },
            # Pré-import sommiers
            {
                'Client_D1': 'Test Client',
                'numero_D2': '0123456789',
                'semaine_D5': 'S01_2025',
                'Type_Sommier_D20': 'SOMMIER À LATTES',
                'Quantite_D40': 1,
                'Dimensions_D35': '160x200',
                'Hauteur_D30': 8,
                'Materiau_D25': 'BOIS',
                'Sommier_DansUnLit_D45': 'OUI',
                'Sommier_Pieds_D50': 'NON',
                'type_article': 'sommier'
            },
            {
                'Client_D1': 'Test Client',
                'numero_D2': '0123456789',
                'semaine_D5': 'S01_2025',
                'Type_Sommier_D20': 'SOMMIER TAPISSIER',
                'Quantite_D40': 1,
                'Dimensions_D35': '180x200',
                'Hauteur_D30': 12,
                'Materiau_D25': 'TAPISSIER',
                'Sommier_DansUnLit_D45': 'NON',
                'Sommier_Pieds_D50': 'OUI',
                'type_article': 'sommier'
            }
        ],
        'fichiers_excel': ['Matelas_S01_2025_1.xlsx', 'Sommier_S01_2025_1.xlsx']
    }
    
    print("Résultat simulé créé avec:")
    print(f"  - {len(result['configurations_matelas'])} configuration(s) matelas")
    print(f"  - {len(result['configurations_sommiers'])} configuration(s) sommier")
    print(f"  - {len(result['pre_import'])} élément(s) pré-import")
    print(f"  - {len(result['fichiers_excel'])} fichier(s) Excel")
    
    # Test de l'interface backend
    backend = BackendInterface()
    
    # Simulation de l'affichage
    print("\n=== Simulation affichage ===")
    
    # Test des configurations matelas
    print("\nConfigurations matelas:")
    for i, config in enumerate(result['configurations_matelas']):
        print(f"  {i+1}. {config['noyau']} - {config['dimensions']['largeur']}x{config['dimensions']['longueur']} - {config['housse']} {config['matiere_housse']}")
    
    # Test des configurations sommiers
    print("\nConfigurations sommiers:")
    for i, config in enumerate(result['configurations_sommiers']):
        print(f"  {i+1}. {config['type_sommier']} - {config['dimensions']['largeur']}x{config['dimensions']['longueur']} - {config['materiau']}")
        print(f"      Dans un lit: {config['sommier_dansunlit']}, Pieds: {config['sommier_pieds']}")
    
    # Test du pré-import
    print("\nPré-import:")
    for i, item in enumerate(result['pre_import']):
        type_article = item.get('type_article', 'matelas')
        if type_article == 'matelas':
            print(f"  {i+1}. MATELAS - {item.get('noyau', '')} - {item.get('jumeaux_D10', '')}")
        else:
            print(f"  {i+1}. SOMMIER - {item.get('Type_Sommier_D20', '')} - {item.get('Dimensions_D35', '')}")
    
    print("\n✅ Test interface terminé!")

def test_detection_caracteristiques():
    """Test de la détection des caractéristiques sommiers"""
    print("\n=== Test détection caractéristiques ===")
    
    from sommier_analytics_utils import analyser_caracteristiques_sommier
    
    test_descriptions = [
        "Sommier à lattes dans un lit avec pieds 160x200",
        "SOMMIER DANS UN LIT standard sans pieds",
        "Sommier tapissier avec PIEDS 180x200",
        "Sommier métallique standard 140x190"
    ]
    
    for desc in test_descriptions:
        result = analyser_caracteristiques_sommier(desc)
        print(f"'{desc}' -> {result}")

if __name__ == "__main__":
    print("Test de l'interface avec affichage des sommiers")
    print("=" * 60)
    
    test_detection_caracteristiques()
    test_interface_sommiers()
    
    print("\n✅ Tous les tests terminés!") 