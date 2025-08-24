#!/usr/bin/env python3
"""
Test d'intégration pour la gestion des sommiers avec l'interface backend
"""

import sys
import os
import json
import asyncio

# Ajouter le répertoire courant au path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

async def test_backend_interface_sommiers():
    """Test de l'interface backend avec des sommiers"""
    print("=== Test de l'interface backend avec sommiers ===")
    
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
        
        # Simuler un fichier PDF
        file_info = {
            'filename': 'test_sommiers.pdf',
            'content': 'Contenu test'
        }
        
        # Paramètres de test
        enrich_llm = False
        llm_provider = "ollama"
        openrouter_api_key = None
        semaine_prod = 1
        annee_prod = 2025
        commande_client = "Test Client"
        
        # Simuler le traitement d'un fichier
        result = await interface._process_single_file(
            file_info, enrich_llm, llm_provider, openrouter_api_key,
            semaine_prod, annee_prod, commande_client
        )
        
        # Injecter les données LLM simulées
        result['llm_result'] = json.dumps(llm_data)
        
        # Traiter les résultats
        if result['status'] == 'success':
            print("✅ Traitement réussi")
            
            # Vérifier les configurations
            configurations_matelas = result.get('configurations_matelas', [])
            configurations_sommiers = result.get('configurations_sommiers', [])
            
            print(f"Matelas détectés: {len(configurations_matelas)}")
            for config in configurations_matelas:
                print(f"  - {config.get('noyau', '')} {config.get('dimensions', {})}")
            
            print(f"Sommiers détectés: {len(configurations_sommiers)}")
            for config in configurations_sommiers:
                print(f"  - {config.get('type_sommier', '')} {config.get('dimensions', {})}")
            
            # Vérifier le pré-import
            pre_import = result.get('pre_import', [])
            print(f"Pré-import créé: {len(pre_import)} éléments")
            
            # Compter les types d'articles
            matelas_count = sum(1 for item in pre_import if item.get('type_article') != 'sommier')
            sommiers_count = sum(1 for item in pre_import if item.get('type_article') == 'sommier')
            
            print(f"  - Matelas dans pré-import: {matelas_count}")
            print(f"  - Sommiers dans pré-import: {sommiers_count}")
            
            # Test de l'export Excel global
            if pre_import:
                print("\n=== Test de l'export Excel global ===")
                fichiers_crees = interface._export_excel_global(pre_import, semaine_prod, annee_prod)
                print(f"Fichiers Excel créés: {fichiers_crees}")
                
                # Vérifier que les fichiers ont été créés
                for fichier in fichiers_crees:
                    if os.path.exists(fichier):
                        print(f"✅ Fichier créé: {fichier}")
                    else:
                        print(f"❌ Fichier manquant: {fichier}")
            
        else:
            print(f"❌ Erreur de traitement: {result.get('error', '')}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()

def test_manual_integration():
    """Test manuel d'intégration sans l'interface backend"""
    print("\n=== Test manuel d'intégration ===")
    
    # Simuler le processus complet
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
    from backend_interface import BackendInterface
    interface = BackendInterface()
    
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
    
    # Test de l'export Excel
    if pre_import_total:
        print("\n=== Test de l'export Excel ===")
        fichiers_crees = interface._export_excel_global(pre_import_total, 1, 2025)
        print(f"Fichiers créés: {fichiers_crees}")
        
        # Vérifier les fichiers
        for fichier in fichiers_crees:
            if os.path.exists(fichier):
                print(f"✅ Fichier créé: {fichier}")
            else:
                print(f"❌ Fichier manquant: {fichier}")

async def main():
    """Fonction principale"""
    print("Test d'intégration des sommiers")
    print("=" * 50)
    
    # Test manuel d'abord
    test_manual_integration()
    
    # Test avec l'interface backend
    await test_backend_interface_sommiers()
    
    print("\nTous les tests d'intégration terminés !")

if __name__ == "__main__":
    asyncio.run(main()) 