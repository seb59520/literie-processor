#!/usr/bin/env python3
"""
Script de test pour la gestion des sommiers
"""

import sys
import os
import json

# Ajouter le répertoire backend au path
backend_dir = os.path.join(os.path.dirname(__file__), "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

def test_detection_sommiers():
    """Test de la détection des types de sommiers"""
    print("=== Test de détection des types de sommiers ===")
    
    from sommier_utils import detecter_type_sommier, calculer_hauteur_sommier, detecter_materiau_sommier
    
    # Articles de test
    articles_test = [
        {"description": "Sommier à lattes bois massif 160x200"},
        {"description": "Sommier tapissier 140x190"},
        {"description": "Sommier métallique à ressorts 180x200"},
        {"description": "Sommier plat standard 160x200"},
        {"description": "Sommier bois massif 200x200"},
        {"description": "Sommier à lattes 140x190"}
    ]
    
    # Test de détection des types
    types_detectes = detecter_type_sommier(articles_test)
    print(f"Types détectés: {types_detectes}")
    
    # Test de calcul des hauteurs
    for type_info in types_detectes:
        hauteur = calculer_hauteur_sommier(type_info['type_sommier'])
        print(f"Type: {type_info['type_sommier']} -> Hauteur: {hauteur}cm")
    
    # Test de détection des matériaux
    for article in articles_test:
        materiau = detecter_materiau_sommier(article['description'])
        print(f"Description: {article['description']} -> Matériau: {materiau}")
    
    print()

def test_configurations_sommiers():
    """Test de création des configurations sommiers"""
    print("=== Test de création des configurations sommiers ===")
    
    from sommier_utils import detecter_type_sommier
    from dimensions_utils import detecter_dimensions
    
    # Articles de test
    articles_test = [
        {"description": "Sommier à lattes bois massif 160x200", "quantite": 2},
        {"description": "Sommier tapissier 140x190", "quantite": 1}
    ]
    
    # Détection des types
    types_sommiers = detecter_type_sommier(articles_test)
    print(f"Types détectés: {types_sommiers}")
    
    # Création des configurations
    configurations = []
    for i, type_info in enumerate(types_sommiers):
        if type_info['type_sommier'] != 'INCONNU':
            article = articles_test[type_info['index'] - 1]
            quantite = article.get('quantite', 1)
            description = article.get('description', '')
            
            # Détection des dimensions
            dimensions = detecter_dimensions(description)
            
            # Configuration
            config = {
                "sommier_index": type_info['index'],
                "type_sommier": type_info['type_sommier'],
                "quantite": quantite,
                "hauteur": 10,  # Valeur par défaut
                "materiau": "BOIS",  # Valeur par défaut
                "dimensions": dimensions,
                "semaine_annee": "01_2025",
                "lundi": "2025-01-06",
                "vendredi": "2025-01-10",
                "commande_client": "Test Client"
            }
            
            configurations.append(config)
    
    print(f"Configurations créées: {len(configurations)}")
    for config in configurations:
        print(f"  - {config['type_sommier']} {config['dimensions']} (qte: {config['quantite']})")
    
    print()

def test_pre_import_sommiers():
    """Test de création du pré-import pour les sommiers"""
    print("=== Test de création du pré-import sommiers ===")
    
    # Configurations de test
    configurations_sommiers = [
        {
            "sommier_index": 1,
            "type_sommier": "SOMMIER À LATTES",
            "quantite": 2,
            "hauteur": 8,
            "materiau": "BOIS",
            "dimensions": {"largeur": 160, "longueur": 200},
            "semaine_annee": "01_2025",
            "lundi": "2025-01-06",
            "vendredi": "2025-01-10",
            "commande_client": "Test Client"
        },
        {
            "sommier_index": 2,
            "type_sommier": "SOMMIER TAPISSIER",
            "quantite": 1,
            "hauteur": 12,
            "materiau": "TAPISSIER",
            "dimensions": {"largeur": 140, "longueur": 190},
            "semaine_annee": "01_2025",
            "lundi": "2025-01-06",
            "vendredi": "2025-01-10",
            "commande_client": "Test Client"
        }
    ]
    
    # Données client de test
    donnees_client = {
        "nom": "Client Test",
        "adresse": "123 Rue Test, 75000 Paris",
        "telephone": "01 23 45 67 89"
    }
    
    # Création du pré-import
    pre_import_data = []
    for config in configurations_sommiers:
        pre_import_item = {
            # Données client
            "Client_D1": donnees_client.get('nom', ''),
            "Client_D2": donnees_client.get('adresse', ''),
            "Client_D3": donnees_client.get('telephone', ''),
            
            # Données sommier
            "Article_D6": f"Sommier {config.get('type_sommier', '')}",
            "Quantite_D11": str(config.get('quantite', 1)),
            "Dimensions_D15": f"{config.get('dimensions', {}).get('largeur', '')}x{config.get('dimensions', {}).get('longueur', '')}",
            "Type_Sommier_D20": config.get('type_sommier', ''),
            "Materiau_D25": config.get('materiau', ''),
            "Hauteur_D30": str(config.get('hauteur', '')),
            "Prix_D35": config.get('prix', ''),
            
            # Données de production
            "semaine_annee": config.get('semaine_annee', ''),
            "lundi": config.get('lundi', ''),
            "vendredi": config.get('vendredi', ''),
            "commande_client": config.get('commande_client', ''),
            
            # Type d'article
            "type_article": "sommier",
            "sommier_index": config.get('sommier_index', 0)
        }
        
        pre_import_data.append(pre_import_item)
    
    print(f"Pré-import créé: {len(pre_import_data)} éléments")
    for item in pre_import_data:
        print(f"  - {item['Article_D6']} {item['Dimensions_D15']} (qte: {item['Quantite_D11']})")
    
    print()

def test_excel_sommier_import():
    """Test de l'export Excel pour les sommiers"""
    print("=== Test de l'export Excel sommiers ===")
    
    try:
        from excel_sommier_import_utils import ExcelSommierImporter
        
        # Pré-import de test
        pre_import_data = [
            {
                "Client_D1": "Client Test 1",
                "Client_D2": "Adresse Test 1",
                "Article_D6": "Sommier à lattes",
                "Quantite_D11": "2",
                "Dimensions_D15": "160x200",
                "Type_Sommier_D20": "SOMMIER À LATTES",
                "Materiau_D25": "BOIS",
                "Hauteur_D30": "8",
                "Prix_D35": "400.00"
            },
            {
                "Client_D1": "Client Test 2",
                "Client_D2": "Adresse Test 2",
                "Article_D6": "Sommier tapissier",
                "Quantite_D11": "1",
                "Dimensions_D15": "140x190",
                "Type_Sommier_D20": "SOMMIER TAPISSIER",
                "Materiau_D25": "TAPISSIER",
                "Hauteur_D30": "12",
                "Prix_D35": "300.00"
            }
        ]
        
        # Test de l'importateur
        importer = ExcelSommierImporter()
        fichiers_crees = importer.import_configurations(pre_import_data, "S01", "1234")
        
        print(f"Fichiers Excel créés: {fichiers_crees}")
        
    except Exception as e:
        print(f"Erreur lors du test Excel: {e}")
    
    print()

def test_integration_complete():
    """Test d'intégration complète avec matelas et sommiers"""
    print("=== Test d'intégration complète ===")
    
    # Simuler des données LLM avec matelas et sommiers
    llm_data = {
        "articles": [
            {"description": "Matelas latex naturel 160x200", "quantite": 1},
            {"description": "Sommier à lattes bois massif 160x200", "quantite": 1},
            {"description": "Matelas mousse visco 140x190", "quantite": 2},
            {"description": "Sommier tapissier 140x190", "quantite": 1}
        ],
        "client": {
            "nom": "Client Test",
            "adresse": "123 Rue Test, 75000 Paris",
            "telephone": "01 23 45 67 89"
        }
    }
    
    # Extraction des articles
    articles_llm = []
    matelas_articles = []
    sommier_articles = []
    
    for key in llm_data:
        if isinstance(llm_data[key], list):
            articles_llm.extend(llm_data[key])
            if key.lower() == "articles":
                for article in llm_data[key]:
                    description = article.get('description', '').upper()
                    if 'MATELAS' in description:
                        matelas_articles.append(article)
                    elif 'SOMMIER' in description:
                        sommier_articles.append(article)
    
    print(f"Articles extraits: {len(articles_llm)}")
    print(f"Matelas: {len(matelas_articles)}")
    print(f"Sommiers: {len(sommier_articles)}")
    
    # Détection des types
    from matelas_utils import detecter_noyau_matelas
    from sommier_utils import detecter_type_sommier
    
    noyaux_matelas = detecter_noyau_matelas(matelas_articles)
    types_sommiers = detecter_type_sommier(sommier_articles)
    
    print(f"Noyaux matelas détectés: {noyaux_matelas}")
    print(f"Types sommiers détectés: {types_sommiers}")
    
    print()

if __name__ == "__main__":
    print("Tests de gestion des sommiers")
    print("=" * 50)
    
    test_detection_sommiers()
    test_configurations_sommiers()
    test_pre_import_sommiers()
    test_excel_sommier_import()
    test_integration_complete()
    
    print("Tous les tests terminés !") 