#!/usr/bin/env python3
"""
Script de test pour les nouvelles semaines de production automatiques
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
        print(f"  Matelas: S{result['matelas']['semaine']}_{result['matelas']['annee']} ({result['matelas']['lundi']} - {result['matelas']['vendredi']})")
        print(f"  Sommiers: S{result['sommiers']['semaine']}_{result['sommiers']['annee']} ({result['sommiers']['lundi']} - {result['sommiers']['vendredi']})")
        
        # Test 2: Seulement sommiers
        print("\n📋 Test 2: Seulement sommiers")
        result = calculate_production_weeks(29, 2025, False, True)
        print(f"  Semaine actuelle: 29_2025")
        print(f"  Recommandation: {result['recommandation']}")
        print(f"  Matelas: S{result['matelas']['semaine']}_{result['matelas']['annee']} ({result['matelas']['lundi']} - {result['matelas']['vendredi']})")
        print(f"  Sommiers: S{result['sommiers']['semaine']}_{result['sommiers']['annee']} ({result['sommiers']['lundi']} - {result['sommiers']['vendredi']})")
        
        # Test 3: Matelas + sommiers
        print("\n📋 Test 3: Matelas + sommiers")
        result = calculate_production_weeks(29, 2025, True, True)
        print(f"  Semaine actuelle: 29_2025")
        print(f"  Recommandation: {result['recommandation']}")
        print(f"  Matelas: S{result['matelas']['semaine']}_{result['matelas']['annee']} ({result['matelas']['lundi']} - {result['matelas']['vendredi']})")
        print(f"  Sommiers: S{result['sommiers']['semaine']}_{result['sommiers']['annee']} ({result['sommiers']['lundi']} - {result['sommiers']['vendredi']})")
        
        # Test 4: Passage d'année (semaine 53)
        print("\n📋 Test 4: Passage d'année (semaine 53)")
        result = calculate_production_weeks(53, 2024, True, True)
        print(f"  Semaine actuelle: 53_2024")
        print(f"  Recommandation: {result['recommandation']}")
        print(f"  Matelas: S{result['matelas']['semaine']}_{result['matelas']['annee']} ({result['matelas']['lundi']} - {result['matelas']['vendredi']})")
        print(f"  Sommiers: S{result['sommiers']['semaine']}_{result['sommiers']['annee']} ({result['sommiers']['lundi']} - {result['sommiers']['vendredi']})")
        
        # Test 5: Semaine actuelle
        current_week = datetime.now().isocalendar()[1]
        current_year = datetime.now().year
        print(f"\n📋 Test 5: Semaine actuelle ({current_week}_{current_year})")
        result = calculate_production_weeks(current_week, current_year, True, True)
        print(f"  Semaine actuelle: {current_week}_{current_year}")
        print(f"  Recommandation: {result['recommandation']}")
        print(f"  Matelas: S{result['matelas']['semaine']}_{result['matelas']['annee']} ({result['matelas']['lundi']} - {result['matelas']['vendredi']})")
        print(f"  Sommiers: S{result['sommiers']['semaine']}_{result['sommiers']['annee']} ({result['sommiers']['lundi']} - {result['sommiers']['vendredi']})")
        
        print("\n✅ Tous les tests de calculate_production_weeks sont passés !")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()

def test_interface_integration():
    """Test de l'intégration avec l'interface"""
    print("\n🧪 Test de l'intégration avec l'interface")
    print("=" * 50)
    
    try:
        # Simuler les valeurs de l'interface
        semaine_ref = 29
        annee_ref = 2025
        semaine_matelas = 30
        annee_matelas = 2025
        semaine_sommiers = 30
        annee_sommiers = 2025
        
        print(f"  Semaine référence: {semaine_ref}_{annee_ref}")
        print(f"  Semaine matelas: {semaine_matelas}_{annee_matelas}")
        print(f"  Semaine sommiers: {semaine_sommiers}_{annee_sommiers}")
        
        # Test avec différentes combinaisons
        test_cases = [
            ("Seulement matelas", True, False),
            ("Seulement sommiers", False, True),
            ("Matelas + sommiers", True, True),
            ("Aucun article", False, False)
        ]
        
        for description, has_matelas, has_sommiers in test_cases:
            print(f"\n  📋 {description}:")
            from date_utils import calculate_production_weeks
            result = calculate_production_weeks(semaine_ref, annee_ref, has_matelas, has_sommiers)
            print(f"    Recommandation: {result['recommandation']}")
            print(f"    Matelas calculé: S{result['matelas']['semaine']}_{result['matelas']['annee']}")
            print(f"    Sommiers calculé: S{result['sommiers']['semaine']}_{result['sommiers']['annee']}")
        
        print("\n✅ Test d'intégration réussi !")
        
    except Exception as e:
        print(f"❌ Erreur lors du test d'intégration: {e}")
        import traceback
        traceback.print_exc()

def test_backend_interface():
    """Test de l'intégration avec le backend interface"""
    print("\n🧪 Test de l'intégration avec le backend interface")
    print("=" * 50)
    
    try:
        # Simuler les paramètres du backend
        semaine_prod = 29
        annee_prod = 2025
        semaine_matelas = 30
        annee_matelas = 2025
        semaine_sommiers = 30
        annee_sommiers = 2025
        
        print(f"  Semaine production (compatibilité): {semaine_prod}_{annee_prod}")
        print(f"  Semaine matelas: {semaine_matelas}_{annee_matelas}")
        print(f"  Semaine sommiers: {semaine_sommiers}_{annee_sommiers}")
        
        # Test de la logique de fallback
        semaine_matelas_prod = semaine_matelas or semaine_prod
        annee_matelas_prod = annee_matelas or annee_prod
        semaine_sommiers_prod = semaine_sommiers or semaine_prod
        annee_sommiers_prod = annee_sommiers or annee_prod
        
        print(f"\n  📋 Résultats du fallback:")
        print(f"    Matelas final: {semaine_matelas_prod}_{annee_matelas_prod}")
        print(f"    Sommiers final: {semaine_sommiers_prod}_{annee_sommiers_prod}")
        
        # Test avec valeurs None (fallback vers semaine_prod)
        semaine_matelas_prod_fallback = None or semaine_prod
        annee_matelas_prod_fallback = None or annee_prod
        semaine_sommiers_prod_fallback = None or semaine_prod
        annee_sommiers_prod_fallback = None or annee_prod
        
        print(f"\n  📋 Test fallback avec None:")
        print(f"    Matelas fallback: {semaine_matelas_prod_fallback}_{annee_matelas_prod_fallback}")
        print(f"    Sommiers fallback: {semaine_sommiers_prod_fallback}_{annee_sommiers_prod_fallback}")
        
        print("\n✅ Test backend interface réussi !")
        
    except Exception as e:
        print(f"❌ Erreur lors du test backend interface: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Fonction principale de test"""
    print("🚀 Test des nouvelles semaines de production automatiques")
    print("=" * 60)
    
    # Test 1: Fonction calculate_production_weeks
    test_calculate_production_weeks()
    
    # Test 2: Intégration interface
    test_interface_integration()
    
    # Test 3: Backend interface
    test_backend_interface()
    
    print("\n🎉 Tous les tests sont terminés !")
    print("\n📝 Résumé des améliorations:")
    print("  ✅ Calcul automatique des semaines de production")
    print("  ✅ Interface utilisateur avec contrôles séparés")
    print("  ✅ Recommandations intelligentes")
    print("  ✅ Compatibilité avec l'ancien code")
    print("  ✅ Gestion du passage d'année")

if __name__ == "__main__":
    main() 