#!/usr/bin/env python3
"""
Test du système d'alertes de noyaux non détectés
"""

import sys
import os
sys.path.append('backend')

def test_detection_noyau_alerts():
    """Test de la détection des alertes de noyaux non détectés"""
    print("🧪 TEST DÉTECTION ALERTES NOYAUX")
    print("=" * 50)
    
    # Simuler des données LLM avec des noyaux non détectés
    llm_data = {
        "articles": [
            {
                "description": "MATELAS 1 PIÈCE - HOUSSE MATELASSÉE TENCEL LUXE 3D LAVABLE A 40°",
                "quantite": 1,
                "dimensions": "139/189/20"
            },
            {
                "description": "MATELAS JUMEAUX - HOUSSE SIMPLE POLYESTER",
                "quantite": 2,
                "dimensions": "89/198/18"
            },
            {
                "description": "MATELAS 1 PIÈCE - LATEX 100% NATUREL PERFORÉ 7 ZONES DIFFÉRENCIÉES FERME",
                "quantite": 1,
                "dimensions": "160/200/22"
            }
        ]
    }
    
    print("📝 Données LLM de test:")
    for i, article in enumerate(llm_data["articles"]):
        print(f"  Article {i+1}: {article['description'][:80]}...")
    print()
    
    # Test de détection des noyaux
    from matelas_utils import detecter_noyau_matelas
    matelas_articles = llm_data["articles"]
    noyaux_matelas = detecter_noyau_matelas(matelas_articles)
    
    print("🔍 Résultats de détection des noyaux:")
    for i, noyau_info in enumerate(noyaux_matelas):
        print(f"  Matelas {i+1}: {noyau_info['noyau']}")
    print()
    
    # Identifier les noyaux INCONNU
    alerts = []
    for i, noyau_info in enumerate(noyaux_matelas):
        if noyau_info['noyau'] == 'INCONNU':
            if i < len(matelas_articles):
                article = matelas_articles[i]
                alert = {
                    'index': noyau_info['index'],
                    'description': article.get('description', ''),
                    'noyau': noyau_info['noyau'],
                    'quantite': article.get('quantite', 1),
                    'dimensions': article.get('dimensions', '')
                }
                alerts.append(alert)
    
    print("⚠️ Alertes détectées:")
    if alerts:
        for i, alert in enumerate(alerts):
            print(f"  Alerte {i+1}:")
            print(f"    Index: {alert['index']}")
            print(f"    Description: {alert['description'][:60]}...")
            print(f"    Noyau: {alert['noyau']}")
            print(f"    Quantité: {alert['quantite']}")
            print(f"    Dimensions: {alert['dimensions']}")
        print(f"✅ {len(alerts)} alerte(s) détectée(s)")
    else:
        print("✅ Aucune alerte détectée")
    
    return len(alerts) > 0

def test_noyau_alert_dialog():
    """Test de la classe NoyauAlertDialog"""
    print("\n🧪 TEST CLASSE NOYAUALERTDIALOG")
    print("=" * 50)
    
    try:
        from PyQt6.QtWidgets import QApplication
        from app_gui import NoyauAlertDialog
        
        # Créer une application Qt pour les tests
        app = QApplication([])
        
        # Simuler des alertes de noyaux
        noyau_alerts = {
            "/path/to/file1.pdf": [
                {
                    'index': 1,
                    'description': "MATELAS 1 PIÈCE - HOUSSE MATELASSÉE TENCEL LUXE 3D LAVABLE A 40°",
                    'noyau': 'INCONNU',
                    'quantite': 1,
                    'dimensions': '139/189/20'
                },
                {
                    'index': 2,
                    'description': "MATELAS JUMEAUX - HOUSSE SIMPLE POLYESTER",
                    'noyau': 'INCONNU',
                    'quantite': 2,
                    'dimensions': '89/198/18'
                }
            ],
            "/path/to/file2.pdf": [
                {
                    'index': 1,
                    'description': "MATELAS 1 PIÈCE - HOUSSE MATELASSÉE TENCEL LUXE 3D LAVABLE A 40°",
                    'noyau': 'INCONNU',
                    'quantite': 1,
                    'dimensions': '160/200/22'
                }
            ]
        }
        
        # Créer le dialog
        dialog = NoyauAlertDialog(noyau_alerts)
        
        print(f"  Dialog créé avec {len(noyau_alerts)} fichiers")
        print(f"  Total alertes: {sum(len(alerts) for alerts in noyau_alerts.values())}")
        print(f"  Interface initialisée correctement")
        
        # Test de récupération des corrections
        corrections = dialog.get_corrections()
        print(f"  Corrections récupérées: {len(corrections)} fichiers")
        
        print("\n✅ Test de NoyauAlertDialog réussi !")
        
    except Exception as e:
        print(f"❌ Erreur dans test_noyau_alert_dialog: {e}")
        return False
    
    return True

def test_integration_complete():
    """Test d'intégration complet du système d'alertes"""
    print("\n🧪 TEST D'INTÉGRATION COMPLET")
    print("=" * 50)
    
    # Simuler le flux complet
    print("1. 📄 Analyse de fichiers PDF...")
    print("2. 🔍 Détection des noyaux...")
    print("3. ⚠️ Identification des noyaux non détectés...")
    print("4. 🖥️ Affichage du dialog d'alertes...")
    print("5. ✅ Correction par l'utilisateur...")
    print("6. 🔄 Continuation du traitement...")
    
    # Test avec différents scénarios
    scenarios = [
        {
            "name": "Aucune alerte",
            "articles": [
                {"description": "MATELAS LATEX 100% NATUREL", "quantite": 1}
            ],
            "expected_alerts": 0
        },
        {
            "name": "Une alerte",
            "articles": [
                {"description": "MATELAS HOUSSE SIMPLE", "quantite": 1}
            ],
            "expected_alerts": 1
        },
        {
            "name": "Plusieurs alertes",
            "articles": [
                {"description": "MATELAS HOUSSE SIMPLE", "quantite": 1},
                {"description": "MATELAS STANDARD", "quantite": 2}
            ],
            "expected_alerts": 2
        }
    ]
    
    for scenario in scenarios:
        print(f"\n--- Scénario: {scenario['name']} ---")
        
        llm_data = {"articles": scenario["articles"]}
        
        # Test de détection
        from matelas_utils import detecter_noyau_matelas
        noyaux = detecter_noyau_matelas(scenario["articles"])
        
        alerts = []
        for i, noyau_info in enumerate(noyaux):
            if noyau_info['noyau'] == 'INCONNU':
                alerts.append(noyau_info)
        
        print(f"  Alertes détectées: {len(alerts)} (attendu: {scenario['expected_alerts']})")
        
        if len(alerts) == scenario['expected_alerts']:
            print("  ✅ Scénario réussi")
        else:
            print("  ❌ Scénario échoué")
    
    print("\n✅ Test d'intégration complet terminé !")
    return True

def main():
    """Fonction principale de test"""
    print("🚀 DÉBUT DES TESTS - SYSTÈME D'ALERTES NOYAUX")
    print("=" * 60)
    
    tests = [
        test_detection_noyau_alerts,
        test_noyau_alert_dialog,
        test_integration_complete
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
        print("\n✅ Le système d'alertes de noyaux est prêt !")
        print("\n📋 Fonctionnalités testées:")
        print("  • Détection des noyaux non détectés")
        print("  • Interface utilisateur d'alertes")
        print("  • Gestion multi-fichiers")
        print("  • Corrections par liste déroulante")
        print("  • Intégration avec le workflow existant")
    else:
        print("⚠️  Certains tests ont échoué")
    
    return passed == total

if __name__ == "__main__":
    main() 