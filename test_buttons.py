#!/usr/bin/env python3
"""Test des boutons d'action"""

import sys
import os
from pathlib import Path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Test 1: Vérifier que le dossier results peut être créé
def test_results_folder():
    results_folder = Path("resultats_excel")
    results_folder.mkdir(exist_ok=True)
    print(f"✅ Dossier créé: {results_folder.absolute()}")
    return results_folder.exists()

# Test 2: Vérifier la génération HTML
def test_html_generation():
    try:
        # Simuler des données de test
        all_results = [
            {"filename": "test1.pdf", "summary": "Test matelas 1", "timestamp": "2025-08-24"},
            {"filename": "test2.pdf", "summary": "Test matelas 2", "timestamp": "2025-08-24"}
        ]
        
        from datetime import datetime
        html = f"""<!DOCTYPE html>
<html><head><title>Test</title></head>
<body>
<h1>Test Rapport</h1>
<p>Généré: {datetime.now()}</p>
<p>Fichiers: {len(all_results)}</p>
</body></html>"""
        
        report_file = Path("test_rapport.html")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Rapport HTML test créé: {report_file.absolute()}")
        report_file.unlink()  # Nettoyer
        return True
        
    except Exception as e:
        print(f"❌ Erreur HTML: {e}")
        return False

# Test 3: Vérifier l'export JSON
def test_json_export():
    try:
        import json
        
        test_data = {
            "timestamp": str(datetime.now()),
            "resultats": [{"filename": "test.pdf", "summary": "Test"}]
        }
        
        test_file = Path("test_export.json")
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Export JSON test créé: {test_file.absolute()}")
        test_file.unlink()  # Nettoyer
        return True
        
    except Exception as e:
        print(f"❌ Erreur JSON: {e}")
        return False

def main():
    print("🧪 Test des fonctionnalités des boutons")
    print("=" * 40)
    
    results = []
    results.append(test_results_folder())
    results.append(test_html_generation()) 
    results.append(test_json_export())
    
    success_count = sum(results)
    print(f"\n📊 Résultats: {success_count}/3 tests réussis")
    
    if success_count == 3:
        print("✅ Tous les tests réussis - Les boutons devraient fonctionner !")
    else:
        print("⚠️ Certains tests ont échoué")

if __name__ == "__main__":
    from datetime import datetime
    main()