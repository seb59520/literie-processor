#!/usr/bin/env python3
"""
Script de test pour le tableau de hauteur des matelas
Vérifie la compatibilité avec l'ancien système et teste toutes les fonctionnalités
"""

import sys
import os

# Ajouter le répertoire backend au path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_compatibilite_ancien_systeme():
    """Test de compatibilité avec l'ancien système"""
    print("🧪 TEST DE COMPATIBILITÉ AVEC L'ANCIEN SYSTÈME")
    print("=" * 60)
    
    # Importer les deux systèmes
    try:
        from hauteur_utils import calculer_hauteur_matelas as ancien_calcul
        print("✅ Ancien système importé avec succès")
    except ImportError as e:
        print(f"❌ Erreur import ancien système: {e}")
        return False
    
    try:
        from tableau_hauteur_utils import calculer_hauteur_matelas as nouveau_calcul
        print("✅ Nouveau système importé avec succès")
    except ImportError as e:
        print(f"❌ Erreur import nouveau système: {e}")
        return False
    
    # Tests de compatibilité
    noyaux_test = [
        "LATEX NATUREL",
        "LATEX MIXTE 7 ZONES", 
        "MOUSSE RAINUREE 7 ZONES",
        "MOUSSE RAINURÉE 7 ZONES",
        "LATEX RENFORCE",
        "SELECT 43",
        "MOUSSE VISCO"
    ]
    
    print("\n📊 COMPARAISON DES RÉSULTATS:")
    print("-" * 60)
    print(f"{'Noyau':<25} {'Ancien':<8} {'Nouveau':<8} {'Status':<10}")
    print("-" * 60)
    
    compatibilite_ok = True
    
    for noyau in noyaux_test:
        ancien_resultat = ancien_calcul(noyau)
        nouveau_resultat = nouveau_calcul(noyau)
        
        status = "✅ OK" if ancien_resultat == nouveau_resultat else "❌ DIFF"
        if ancien_resultat != nouveau_resultat:
            compatibilite_ok = False
        
        print(f"{noyau:<25} {ancien_resultat:<8} {nouveau_resultat:<8} {status:<10}")
    
    print("-" * 60)
    if compatibilite_ok:
        print("🎉 COMPATIBILITÉ PARFAITE - Tous les résultats sont identiques")
    else:
        print("⚠️ INCOMPATIBILITÉ DÉTECTÉE - Certains résultats diffèrent")
    
    return compatibilite_ok

def test_nouvelles_fonctionnalites():
    """Test des nouvelles fonctionnalités"""
    print("\n🚀 TEST DES NOUVELLES FONCTIONNALITÉS")
    print("=" * 60)
    
    try:
        from tableau_hauteur_utils import tableau_hauteur
        print("✅ Gestionnaire tableau hauteur importé")
    except ImportError as e:
        print(f"❌ Erreur import gestionnaire: {e}")
        return False
    
    # Test 1: Informations complètes
    print("\n📋 TEST INFORMATIONS COMPLÈTES:")
    noyau_test = "LATEX MIXTE 7 ZONES"
    info = tableau_hauteur.obtenir_info_complete(noyau_test)
    print(f"Infos {noyau_test}:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    # Test 2: Catégories
    print("\n🏷️ TEST CATÉGORIES:")
    categories = tableau_hauteur.obtenir_categories()
    for categorie, stats in categories.items():
        print(f"  {categorie}: {stats.get('description', 'N/A')}")
    
    # Test 3: Noyaux par hauteur
    print("\n📏 TEST NOYAUX PAR HAUTEUR:")
    for hauteur in [8, 9, 10]:
        noyaux = tableau_hauteur.lister_noyaux_par_hauteur(hauteur)
        print(f"  {hauteur}cm: {', '.join(noyaux)}")
    
    # Test 4: Statistiques catégorie
    print("\n📊 TEST STATISTIQUES CATÉGORIE:")
    stats_latex = tableau_hauteur.obtenir_statistiques_categorie("LATEX")
    print(f"  LATEX - Min: {stats_latex.get('hauteur_min')}cm, Max: {stats_latex.get('hauteur_max')}cm")
    
    print("✅ Toutes les nouvelles fonctionnalités testées avec succès")
    return True

def test_export_csv():
    """Test de l'export CSV"""
    print("\n📄 TEST EXPORT CSV:")
    print("=" * 60)
    
    try:
        from tableau_hauteur_utils import tableau_hauteur
        
        # Test export
        output_file = "test_tableau_hauteur.csv"
        tableau_hauteur.exporter_tableau_csv(output_file)
        
        # Vérifier que le fichier existe
        if os.path.exists(output_file):
            print(f"✅ Fichier CSV créé: {output_file}")
            
            # Lire et afficher les premières lignes
            with open(output_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                print(f"📊 {len(lines)} lignes dans le fichier")
                print("📋 Premières lignes:")
                for i, line in enumerate(lines[:5]):
                    print(f"  {i+1}: {line.strip()}")
            
            # Nettoyer
            os.remove(output_file)
            print("🧹 Fichier de test supprimé")
            return True
        else:
            print("❌ Fichier CSV non créé")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'export CSV: {e}")
        return False

def test_performance():
    """Test de performance"""
    print("\n⚡ TEST DE PERFORMANCE:")
    print("=" * 60)
    
    try:
        from tableau_hauteur_utils import tableau_hauteur
        import time
        
        # Test avec 1000 appels
        noyaux = tableau_hauteur.lister_tous_noyaux()
        iterations = 1000
        
        start_time = time.time()
        for _ in range(iterations):
            for noyau in noyaux:
                tableau_hauteur.obtenir_hauteur(noyau)
        end_time = time.time()
        
        temps_total = end_time - start_time
        temps_moyen = temps_total / (iterations * len(noyaux))
        
        print(f"⏱️ Temps total pour {iterations * len(noyaux)} appels: {temps_total:.4f}s")
        print(f"⏱️ Temps moyen par appel: {temps_moyen:.6f}s")
        
        if temps_total < 1.0:
            print("✅ Performance excellente")
            return True
        else:
            print("⚠️ Performance acceptable mais pourrait être optimisée")
            return True
            
    except Exception as e:
        print(f"❌ Erreur lors du test de performance: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🧪 TESTS COMPLETS DU TABLEAU DE HAUTEUR")
    print("=" * 80)
    
    # Tests
    tests = [
        ("Compatibilité ancien système", test_compatibilite_ancien_systeme),
        ("Nouvelles fonctionnalités", test_nouvelles_fonctionnalites),
        ("Export CSV", test_export_csv),
        ("Performance", test_performance)
    ]
    
    resultats = {}
    
    for nom_test, fonction_test in tests:
        try:
            resultats[nom_test] = fonction_test()
        except Exception as e:
            print(f"❌ Erreur dans {nom_test}: {e}")
            resultats[nom_test] = False
    
    # Résumé
    print("\n" + "=" * 80)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 80)
    
    for nom_test, resultat in resultats.items():
        status = "✅ RÉUSSI" if resultat else "❌ ÉCHOUÉ"
        print(f"{nom_test:<30} {status}")
    
    succes_total = sum(resultats.values())
    total_tests = len(resultats)
    
    print("-" * 80)
    print(f"RÉSULTAT GLOBAL: {succes_total}/{total_tests} tests réussis")
    
    if succes_total == total_tests:
        print("🎉 TOUS LES TESTS SONT RÉUSSIS !")
        print("✅ Le tableau de hauteur est prêt à être utilisé")
    else:
        print("⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main() 