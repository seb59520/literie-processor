#!/usr/bin/env python3
"""
Test pour valider que les sommiers utilisent le même système de blocs que les matelas
"""

import sys
import os

# Ajouter le répertoire backend au path
backend_dir = os.path.join(os.path.dirname(__file__), "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

def test_sommiers_blocs():
    """Test du système de blocs pour les sommiers"""
    print("=== Test du système de blocs pour les sommiers ===")
    
    try:
        from excel_sommier_import_utils import ExcelSommierImporter
        
        # Créer l'importateur
        importer = ExcelSommierImporter()
        
        print(f"Blocs de colonnes définis: {importer.column_blocks}")
        print(f"Nombre maximum de cas par fichier: {importer.max_cases_per_file}")
        
        # Vérifier que les blocs sont identiques aux matelas
        expected_blocks = [
            ('C', 'D'),  # Cas 1
            ('E', 'F'),  # Cas 2
            ('G', 'H'),  # Cas 3
            ('I', 'J'),  # Cas 4
            ('K', 'L'),  # Cas 5
            ('O', 'P'),  # Cas 6
            ('Q', 'R'),  # Cas 7
            ('S', 'T'),  # Cas 8
            ('U', 'V'),  # Cas 9
            ('W', 'X'),  # Cas 10
        ]
        
        if importer.column_blocks == expected_blocks:
            print("✅ Blocs de colonnes corrects (identiques aux matelas)")
        else:
            print("❌ Blocs de colonnes incorrects")
            print(f"Attendu: {expected_blocks}")
            print(f"Obtenu: {importer.column_blocks}")
        
        # Test avec des données de pré-import
        pre_import_data = [
            {
                # Données client (mêmes clés que les matelas)
                "Client_D1": "Client Test 1",
                "Adresse_D3": "Adresse Test 1",
                "numero_D2": "01 23 45 67 89",
                
                # Champs commande et dates
                "semaine_D5": "S01_2025",
                "lundi_D6": "2025-01-06",
                "vendredi_D7": "2025-01-10",
                
                # Données sommier
                "Type_Sommier_D20": "SOMMIER À LATTES",
                "Materiau_D25": "BOIS",
                "Hauteur_D30": "8",
                "Dimensions_D35": "160x200",
                "Quantite_D40": "2",
                
                # Type d'article
                "type_article": "sommier",
                "sommier_index": 1
            },
            {
                # Données client (mêmes clés que les matelas)
                "Client_D1": "Client Test 2",
                "Adresse_D3": "Adresse Test 2",
                "numero_D2": "01 23 45 67 90",
                
                # Champs commande et dates
                "semaine_D5": "S01_2025",
                "lundi_D6": "2025-01-06",
                "vendredi_D7": "2025-01-10",
                
                # Données sommier
                "Type_Sommier_D20": "SOMMIER TAPISSIER",
                "Materiau_D25": "TAPISSIER",
                "Hauteur_D30": "12",
                "Dimensions_D35": "140x190",
                "Quantite_D40": "1",
                
                # Type d'article
                "type_article": "sommier",
                "sommier_index": 2
            }
        ]
        
        print(f"\nDonnées de pré-import créées: {len(pre_import_data)} éléments")
        for i, item in enumerate(pre_import_data):
            print(f"  {i+1}. Client: {item['Client_D1']}, Type: {item['Type_Sommier_D20']}, Dimensions: {item['Dimensions_D35']}")
        
        # Test de l'export Excel
        print("\n=== Test de l'export Excel ===")
        fichiers_crees = importer.import_configurations(pre_import_data, "S01", "1234")
        print(f"Fichiers Excel créés: {fichiers_crees}")
        
        # Vérifier que les fichiers ont été créés
        for fichier in fichiers_crees:
            if os.path.exists(fichier):
                print(f"✅ Fichier créé: {fichier}")
            else:
                print(f"❌ Fichier manquant: {fichier}")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()

def test_integration_backend():
    """Test d'intégration avec le backend"""
    print("\n=== Test d'intégration avec le backend ===")
    
    try:
        from backend_interface import BackendInterface
        
        # Créer une instance de l'interface
        interface = BackendInterface()
        
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
        from backend.matelas_utils import detecter_noyau_matelas
        from backend.sommier_utils import detecter_type_sommier
        
        noyaux_matelas = detecter_noyau_matelas(matelas_articles)
        types_sommiers = detecter_type_sommier(sommier_articles)
        
        print(f"Noyaux matelas détectés: {noyaux_matelas}")
        print(f"Types sommiers détectés: {types_sommiers}")
        
        # Création des configurations
        configurations_matelas = interface._create_configurations_matelas(
            noyaux_matelas, matelas_articles, 1, 2025, "Test Client"
        )
        
        configurations_sommiers = interface._create_configurations_sommiers(
            types_sommiers, sommier_articles, 1, 2025, "Test Client"
        )
        
        print(f"Configurations matelas créées: {len(configurations_matelas)}")
        print(f"Configurations sommiers créées: {len(configurations_sommiers)}")
        
        # Création du pré-import
        from backend.pre_import_utils import creer_pre_import
        from backend.article_utils import contient_dosseret_ou_tete
        from backend.operation_utils import mots_operation_trouves
        
        donnees_client = llm_data.get('client', {})
        contient_dosseret_tete = contient_dosseret_ou_tete(articles_llm)
        mots_operation_list = mots_operation_trouves(articles_llm)
        
        pre_import_matelas = creer_pre_import(
            configurations_matelas, donnees_client, 
            contient_dosseret_tete, mots_operation_list
        ) if configurations_matelas else []
        
        pre_import_sommiers = interface._creer_pre_import_sommiers(
            configurations_sommiers, donnees_client, 
            contient_dosseret_tete, mots_operation_list
        ) if configurations_sommiers else []
        
        pre_import_total = pre_import_matelas + pre_import_sommiers
        
        print(f"Pré-import total: {len(pre_import_total)} éléments")
        print(f"  - Matelas: {len(pre_import_matelas)}")
        print(f"  - Sommiers: {len(pre_import_sommiers)}")
        
        # Vérifier que les clés client sont identiques
        if pre_import_matelas and pre_import_sommiers:
            matelas_client_keys = set(pre_import_matelas[0].keys()) & {"Client_D1", "Adresse_D3", "numero_D2"}
            sommiers_client_keys = set(pre_import_sommiers[0].keys()) & {"Client_D1", "Adresse_D3", "numero_D2"}
            
            if matelas_client_keys == sommiers_client_keys:
                print("✅ Clés client identiques entre matelas et sommiers")
            else:
                print("❌ Clés client différentes entre matelas et sommiers")
                print(f"Matelas: {matelas_client_keys}")
                print(f"Sommiers: {sommiers_client_keys}")
        
        # Test de l'export Excel global
        if pre_import_total:
            print("\n=== Test de l'export Excel global ===")
            fichiers_crees = interface._export_excel_global(pre_import_total, 1, 2025)
            print(f"Fichiers créés: {fichiers_crees}")
            
            # Vérifier les fichiers
            for fichier in fichiers_crees:
                if os.path.exists(fichier):
                    print(f"✅ Fichier créé: {fichier}")
                else:
                    print(f"❌ Fichier manquant: {fichier}")
        
    except Exception as e:
        print(f"❌ Erreur lors du test d'intégration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Test du système de blocs pour les sommiers")
    print("=" * 60)
    
    test_sommiers_blocs()
    test_integration_backend()
    
    print("\nTous les tests terminés !") 