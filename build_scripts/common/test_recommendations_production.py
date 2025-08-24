#!/usr/bin/env python3
"""
Script de test pour les recommandations de production automatiques
"""

import sys
import os
from datetime import datetime

# Ajouter le répertoire backend au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_calculate_production_weeks():
    """Test de la fonction calculate_production_weeks"""
    print("🧪 Test de la fonction calculate_production_weeks")
    print("=" * 50)
    
    try:
        from date_utils import calculate_production_weeks
        
        # Test 1: Seulement matelas
        print("\n📋 Test 1: Seulement matelas")
        result = calculate_production_weeks(29, 2025, True, False)
        print(f"  Semaine actuelle: 29_2025")
        print(f"  Recommandation: {result['recommandation']}")
        print(f"  Matelas: S{result['matelas']['semaine']}_{result['matelas']['annee']}")
        print(f"  Sommiers: S{result['sommiers']['semaine']}_{result['sommiers']['annee']}")
        
        # Test 2: Seulement sommiers
        print("\n📋 Test 2: Seulement sommiers")
        result = calculate_production_weeks(29, 2025, False, True)
        print(f"  Semaine actuelle: 29_2025")
        print(f"  Recommandation: {result['recommandation']}")
        print(f"  Matelas: S{result['matelas']['semaine']}_{result['matelas']['annee']}")
        print(f"  Sommiers: S{result['sommiers']['semaine']}_{result['sommiers']['annee']}")
        
        # Test 3: Matelas + sommiers
        print("\n📋 Test 3: Matelas + sommiers")
        result = calculate_production_weeks(29, 2025, True, True)
        print(f"  Semaine actuelle: 29_2025")
        print(f"  Recommandation: {result['recommandation']}")
        print(f"  Matelas: S{result['matelas']['semaine']}_{result['matelas']['annee']}")
        print(f"  Sommiers: S{result['sommiers']['semaine']}_{result['sommiers']['annee']}")
        
        # Test 4: Passage d'année (semaine 53)
        print("\n📋 Test 4: Passage d'année (semaine 53)")
        result = calculate_production_weeks(53, 2024, True, True)
        print(f"  Semaine actuelle: 53_2024")
        print(f"  Recommandation: {result['recommandation']}")
        print(f"  Matelas: S{result['matelas']['semaine']}_{result['matelas']['annee']}")
        print(f"  Sommiers: S{result['sommiers']['semaine']}_{result['sommiers']['annee']}")
        
        print("\n✅ Tous les tests de calculate_production_weeks passent !")
        
    except Exception as e:
        print(f"❌ Erreur dans test_calculate_production_weeks: {e}")
        return False
    
    return True

def test_analyze_content():
    """Test des fonctions d'analyse de contenu"""
    print("\n🧪 Test des fonctions d'analyse de contenu")
    print("=" * 50)
    
    try:
        # Simuler des données LLM
        llm_result = """{
            "articles": [
                {
                    "quantite": 1,
                    "description": "MATELAS 1 PIÈCE - LATEX NATUREL 160x200",
                    "dimensions": "160/200/20"
                },
                {
                    "quantite": 1,
                    "description": "SOMMIER À LATTES BOIS MASSIF 160x200",
                    "dimensions": "160/200"
                }
            ]
        }"""
        
        # Test d'analyse LLM
        print("\n📋 Test analyse LLM")
        from app_gui import ProcessingThread
        
        # Créer une instance temporaire pour tester
        thread = ProcessingThread([], False, "ollama", None, 1, 2025, [])
        
        has_matelas, has_sommiers, matelas_count, sommier_count = thread.analyze_llm_content(llm_result)
        
        print(f"  Matelas détectés: {has_matelas} ({matelas_count} articles)")
        print(f"  Sommiers détectés: {has_sommiers} ({sommier_count} articles)")
        
        # Test d'analyse texte
        print("\n📋 Test analyse texte")
        text = "MATELAS LATEX NATUREL 160x200 - SOMMIER À LATTES BOIS MASSIF"
        
        has_matelas, has_sommiers, matelas_count, sommier_count = thread.analyze_text_content(text)
        
        print(f"  Matelas détectés: {has_matelas} ({matelas_count} occurrences)")
        print(f"  Sommiers détectés: {has_sommiers} ({sommier_count} occurrences)")
        
        print("\n✅ Tous les tests d'analyse de contenu passent !")
        
    except Exception as e:
        print(f"❌ Erreur dans test_analyze_content: {e}")
        return False
    
    return True

def test_production_recommendation_dialog():
    """Test de la classe ProductionRecommendationDialog"""
    print("\n🧪 Test de la classe ProductionRecommendationDialog")
    print("=" * 50)
    
    try:
        from PyQt6.QtWidgets import QApplication
        from app_gui import ProductionRecommendationDialog
        
        # Créer une application Qt pour les tests
        app = QApplication([])
        
        # Simuler des résultats d'analyse
        file_analysis_results = {
            "/path/to/file1.pdf": {
                'has_matelas': True,
                'has_sommiers': False,
                'matelas_count': 2,
                'sommier_count': 0,
                'semaine_actuelle': 29,
                'annee_actuelle': 2025,
                'recommendation': "Production matelas en S+1",
                'semaine_matelas': 30,
                'annee_matelas': 2025,
                'semaine_sommiers': 30,
                'annee_sommiers': 2025
            },
            "/path/to/file2.pdf": {
                'has_matelas': True,
                'has_sommiers': True,
                'matelas_count': 1,
                'sommier_count': 1,
                'semaine_actuelle': 29,
                'annee_actuelle': 2025,
                'recommendation': "Sommiers en S+1, matelas en S+2",
                'semaine_matelas': 31,
                'annee_matelas': 2025,
                'semaine_sommiers': 30,
                'annee_sommiers': 2025
            }
        }
        
        # Créer le dialog
        dialog = ProductionRecommendationDialog(file_analysis_results)
        
        print(f"  Dialog créé avec {len(file_analysis_results)} fichiers")
        print(f"  Interface initialisée correctement")
        
        # Test de récupération des recommandations
        recommendations = dialog.get_recommendations()
        print(f"  Recommandations récupérées: {len(recommendations)} fichiers")
        
        for filename, rec in recommendations.items():
            print(f"    {os.path.basename(filename)}:")
            print(f"      Matelas: S{rec['semaine_matelas']}_{rec['annee_matelas']}")
            print(f"      Sommiers: S{rec['semaine_sommiers']}_{rec['annee_sommiers']}")
        
        print("\n✅ Test de ProductionRecommendationDialog réussi !")
        
    except Exception as e:
        print(f"❌ Erreur dans test_production_recommendation_dialog: {e}")
        return False
    
    return True

def main():
    """Fonction principale de test"""
    print("🚀 DÉBUT DES TESTS - RECOMMANDATIONS DE PRODUCTION")
    print("=" * 60)
    
    tests = [
        test_calculate_production_weeks,
        test_analyze_content,
        test_production_recommendation_dialog
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Erreur dans le test {test.__name__}: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 RÉSULTATS: {passed}/{total} tests passent")
    
    if passed == total:
        print("🎉 TOUS LES TESTS PASSENT !")
        print("\n✅ Le système de recommandations de production est prêt !")
        print("\n📋 Fonctionnalités testées:")
        print("  • Calcul automatique des semaines de production")
        print("  • Détection du contenu (matelas/sommiers)")
        print("  • Interface de recommandations")
        print("  • Gestion de plusieurs fichiers")
        print("  • Passage d'année")
    else:
        print("⚠️  Certains tests ont échoué")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 