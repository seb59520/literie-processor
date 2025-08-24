#!/usr/bin/env python3
"""
Test de débogage pour comprendre pourquoi seulement 1 configuration est affichée
"""

import sys
import os
import json

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def test_configuration_display():
    """Test pour vérifier l'affichage des configurations"""
    
    print("🔍 Test de débogage des configurations")
    print("=" * 50)
    
    # Simuler les données comme elles seraient dans l'interface
    all_results = []
    all_configurations = []
    
    # Premier fichier (vanacker)
    result1 = {
        'filename': 'Commandes vanacker.pdf',
        'status': 'success',
        'configurations_matelas': [
            {
                'matelas_index': 1,
                'noyau': 'LATEX NATUREL',
                'quantite': 1,
                'dimensions': {'largeur': 89, 'longueur': 198},
                'housse': 'Simple',
                'matiere_housse': 'TENCEL',
                'hauteur': 18,
                'fermete': 'Moyenne'
            }
        ],
        'pre_import': [{'Client_D1': 'VANACKER', 'numero_D2': '2025', 'noyau': 'LATEX NATUREL'}],
        'fichiers_excel': ['output/Matelas_S35_2025_1.xlsx']
    }
    
    # Deuxième fichier (thullier)
    result2 = {
        'filename': 'Commandes thullier.pdf',
        'status': 'success',
        'configurations_matelas': [
            {
                'matelas_index': 1,
                'noyau': 'LATEX NATUREL',
                'quantite': 1,
                'dimensions': {'largeur': 89, 'longueur': 199},
                'housse': 'Simple',
                'matiere_housse': 'TENCEL',
                'hauteur': 18,
                'fermete': 'Moyenne'
            }
        ],
        'pre_import': [{'Client_D1': 'THULLIER', 'numero_D2': '2025', 'noyau': 'LATEX NATUREL'}],
        'fichiers_excel': ['output/Matelas_S35_2025_2.xlsx']
    }
    
    # Simuler l'accumulation comme dans l'interface
    all_results.append(result1)
    all_results.append(result2)
    
    all_configurations.extend(result1.get('configurations_matelas', []))
    all_configurations.extend(result2.get('configurations_matelas', []))
    
    print(f"📊 Nombre de résultats: {len(all_results)}")
    print(f"📊 Nombre de configurations: {len(all_configurations)}")
    print(f"📊 Nombre de fichiers Excel: {len(result1.get('fichiers_excel', [])) + len(result2.get('fichiers_excel', []))}")
    
    print("\n🔍 Détail des configurations:")
    for i, config in enumerate(all_configurations):
        print(f"  Configuration {i+1}:")
        print(f"    - Index: {config.get('matelas_index')}")
        print(f"    - Noyau: {config.get('noyau')}")
        print(f"    - Dimensions: {config.get('dimensions')}")
        print(f"    - Fichier source: {get_source_file(config, all_results)}")
    
    print("\n🔍 Test de la méthode display_configurations:")
    test_display_configurations(all_configurations, all_results)

def get_source_file(config, all_results):
    """Trouve le fichier source d'une configuration (comme dans l'interface)"""
    for result in all_results:
        if config in result.get('configurations_matelas', []):
            return os.path.basename(result.get('filename', 'N/A'))
    return "N/A"

def test_display_configurations(configurations, all_results):
    """Test de la méthode display_configurations"""
    if not configurations:
        print("  ❌ Aucune configuration à afficher")
        return
    
    print(f"  ✅ Affichage de {len(configurations)} configurations:")
    
    for i, config in enumerate(configurations):
        try:
            # Trouver le fichier source
            filename = "N/A"
            for result in all_results:
                if config in result.get('configurations_matelas', []):
                    filename = os.path.basename(result.get('filename', 'N/A'))
                    break
            
            print(f"    Ligne {i+1}: {filename} | {config.get('noyau')} | {config.get('dimensions')}")
            
        except Exception as e:
            print(f"    ❌ Erreur ligne {i+1}: {e}")

if __name__ == "__main__":
    test_configuration_display() 