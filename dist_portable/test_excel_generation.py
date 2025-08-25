#!/usr/bin/env python3
"""
Script pour diagnostiquer les problèmes de génération Excel
"""

import os
import json
import sys
from pathlib import Path
import tempfile

def check_excel_dependencies():
    """Vérifier les dépendances Excel"""
    print("🔧 Vérification des dépendances Excel...")
    
    try:
        import pandas
        print("✅ pandas disponible")
    except ImportError:
        print("❌ pandas manquant - pip install pandas")
        return False
    
    try:
        import openpyxl
        print("✅ openpyxl disponible") 
    except ImportError:
        print("❌ openpyxl manquant - pip install openpyxl")
        return False
    
    return True

def check_config():
    """Vérifier la configuration"""
    print("\n🔧 Vérification de la configuration...")
    
    config_file = Path("matelas_config.json")
    if not config_file.exists():
        print("❌ matelas_config.json manquant")
        return None
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        print("✅ Configuration chargée")
        
        provider = config.get('current_llm_provider', '')
        api_key = config.get(f'llm_api_key_{provider}', '')
        
        if not api_key or api_key == "VOTRE_CLE_API_ICI":
            print(f"⚠️ Clé API {provider} non configurée")
            return config
        else:
            print(f"✅ Clé API {provider} configurée")
            return config
            
    except Exception as e:
        print(f"❌ Erreur lecture config: {e}")
        return None

def check_output_directories():
    """Vérifier les dossiers de sortie"""
    print("\n🔧 Vérification des dossiers de sortie...")
    
    # Dossiers standards
    output_dirs = [
        "resultats_excel",
        "exports", 
        "output",
        os.path.expanduser("~/Desktop/resultats_excel"),
        os.path.expanduser("~/Documents/matelas_results")
    ]
    
    existing_dirs = []
    for dir_path in output_dirs:
        if os.path.exists(dir_path):
            try:
                # Tester les permissions d'écriture
                test_file = os.path.join(dir_path, "test_write.tmp")
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                print(f"✅ {dir_path} - accessible en écriture")
                existing_dirs.append(dir_path)
            except Exception as e:
                print(f"⚠️ {dir_path} - erreur permissions: {e}")
        else:
            print(f"ℹ️ {dir_path} - n'existe pas")
    
    if not existing_dirs:
        print("\n📁 Création d'un dossier de test...")
        test_dir = "resultats_excel_test"
        try:
            os.makedirs(test_dir, exist_ok=True)
            test_file = os.path.join(test_dir, "test.txt")
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            print(f"✅ Dossier de test créé: {test_dir}")
            return [test_dir]
        except Exception as e:
            print(f"❌ Impossible de créer dossier test: {e}")
            return []
    
    return existing_dirs

def test_excel_creation():
    """Tester la création d'un fichier Excel simple"""
    print("\n🔧 Test de création Excel...")
    
    try:
        import pandas as pd
        from datetime import datetime
        
        # Données de test
        data = {
            'Client': ['Test Client'],
            'Date': [datetime.now().strftime('%Y-%m-%d')],
            'Produit': ['Matelas Test'],
            'Prix': [1000.00],
            'Status': ['Test']
        }
        
        df = pd.DataFrame(data)
        
        # Tentative de sauvegarde dans différents endroits
        output_dirs = check_output_directories()
        
        if not output_dirs:
            print("❌ Aucun dossier de sortie accessible")
            return False
        
        for output_dir in output_dirs:
            try:
                test_file = os.path.join(output_dir, f"test_excel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
                df.to_excel(test_file, index=False)
                
                if os.path.exists(test_file):
                    file_size = os.path.getsize(test_file)
                    print(f"✅ Fichier Excel créé: {test_file} ({file_size} bytes)")
                    
                    # Nettoyer le fichier de test
                    try:
                        os.remove(test_file)
                        print("✅ Fichier de test nettoyé")
                    except:
                        pass
                    
                    return True
                else:
                    print(f"⚠️ Fichier non créé dans {output_dir}")
                    
            except Exception as e:
                print(f"❌ Erreur création dans {output_dir}: {e}")
                continue
        
        print("❌ Échec création Excel dans tous les dossiers")
        return False
        
    except Exception as e:
        print(f"❌ Erreur test Excel: {e}")
        return False

def check_backend_modules():
    """Vérifier les modules backend nécessaires"""
    print("\n🔧 Vérification des modules backend...")
    
    required_modules = [
        'backend_interface',
        'backend.excel_import_utils',
        'backend.pre_import_utils'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} manquant")
            missing_modules.append(module)
    
    return len(missing_modules) == 0

def analyze_workflow():
    """Analyser le workflow de génération Excel"""
    print("\n🔧 Analyse du workflow de génération...")
    
    print("📋 Le processus de génération Excel nécessite:")
    print("   1. ✅ API fonctionnelle (pour traiter les PDFs)")
    print("   2. ✅ Dépendances Excel (pandas, openpyxl)")
    print("   3. ✅ Modules backend (processing)")
    print("   4. ✅ Permissions d'écriture (dossier output)")
    print("   5. ⚠️  Données traitées (résultats du processing)")
    
    print("\n❓ Questions de diagnostic:")
    print("   • Avez-vous sélectionné et traité des fichiers PDF?")
    print("   • L'API fonctionne-t-elle? (Test_API.bat)")
    print("   • Y a-t-il des erreurs dans les logs de l'application?")
    print("   • L'onglet 'Résumé' montre-t-il des résultats?")

def main():
    """Fonction principale de diagnostic"""
    print("=" * 60)
    print("DIAGNOSTIC GÉNÉRATION FICHIERS EXCEL")
    print("=" * 60)
    
    # Tests des composants
    deps_ok = check_excel_dependencies()
    config = check_config()  
    modules_ok = check_backend_modules()
    excel_test_ok = test_excel_creation()
    
    # Analyse du workflow
    analyze_workflow()
    
    # Résumé
    print("\n" + "=" * 60)
    print("RÉSUMÉ DU DIAGNOSTIC")
    print("=" * 60)
    
    if deps_ok and config and modules_ok and excel_test_ok:
        print("\n✅ TOUS LES COMPOSANTS EXCEL SONT FONCTIONNELS")
        print("\n🔍 Si aucun fichier Excel n'est généré:")
        print("   1. Vérifiez que l'API fonctionne (Test_API.bat)")
        print("   2. Assurez-vous d'avoir traité des PDFs avec succès")
        print("   3. Vérifiez l'onglet 'Résumé' pour voir les résultats")
        print("   4. Consultez les logs d'erreur de l'application")
    else:
        print("\n❌ PROBLÈMES DÉTECTÉS:")
        if not deps_ok:
            print("   • Dépendances Excel manquantes")
        if not config:
            print("   • Configuration invalide")  
        if not modules_ok:
            print("   • Modules backend manquants")
        if not excel_test_ok:
            print("   • Test de création Excel échoué")
    
    print(f"\n📝 SOLUTIONS:")
    print("   1. Test API: Test_API.bat")
    print("   2. Réinstaller dépendances: pip install pandas openpyxl")
    print("   3. Vérifier que des PDFs ont été traités avec succès")
    print("   4. Consulter les logs détaillés dans l'application")

if __name__ == "__main__":
    main()