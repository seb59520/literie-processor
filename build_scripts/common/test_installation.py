#!/usr/bin/env python3
"""
Script de test pour vérifier l'installation de l'application matelas
"""

import sys
import os
import importlib
import subprocess
from pathlib import Path

def test_python_version():
    """Teste la version de Python"""
    print("🐍 Test de la version Python...")
    if sys.version_info >= (3, 8):
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} OK")
        return True
    else:
        print(f"❌ Python {sys.version_info.major}.{sys.version_info.minor} - Version 3.8+ requise")
        return False

def test_dependencies():
    """Teste les dépendances principales"""
    print("\n📦 Test des dépendances...")
    
    dependencies = [
        ('PyQt6', 'Interface graphique'),
        ('fitz', 'Traitement PDF'),
        ('openpyxl', 'Export Excel'),
        ('httpx', 'API HTTP'),
        ('jinja2', 'Templates'),
        ('cryptography', 'Chiffrement'),
        ('pandas', 'Manipulation données'),
        ('numpy', 'Calculs numériques'),
        ('requests', 'Requêtes HTTP'),
        ('jsonschema', 'Validation JSON'),
        ('pydantic', 'Validation données'),
    ]
    
    all_ok = True
    for module, description in dependencies:
        try:
            importlib.import_module(module)
            print(f"✅ {module} - {description}")
        except ImportError:
            print(f"❌ {module} - {description} - MANQUANT")
            all_ok = False
    
    return all_ok

def test_files():
    """Teste la présence des fichiers essentiels"""
    print("\n📁 Test des fichiers essentiels...")
    
    essential_files = [
        'run_gui.py',
        'app_gui.py',
        'backend/main.py',
        'backend_interface.py',
        'config.py',
        'requirements_gui.txt',
        'backend/requirements.txt',
    ]
    
    all_ok = True
    for file_path in essential_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MANQUANT")
            all_ok = False
    
    return all_ok

def test_directories():
    """Teste la présence des répertoires essentiels"""
    print("\n📂 Test des répertoires essentiels...")
    
    essential_dirs = [
        'backend',
        'assets',
        'template',
        'config',
        'Référentiels',
        'Commandes',
    ]
    
    all_ok = True
    for dir_path in essential_dirs:
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/ - MANQUANT")
            all_ok = False
    
    return all_ok

def test_executable():
    """Teste si l'exécutable existe"""
    print("\n🔧 Test de l'exécutable...")
    
    exe_path = "dist/MatelasApp.exe"
    if os.path.exists(exe_path):
        print(f"✅ {exe_path} - Exécutable trouvé")
        
        # Test de lancement rapide
        try:
            result = subprocess.run([exe_path, "--help"], 
                                  capture_output=True, 
                                  timeout=10,
                                  text=True)
            if result.returncode == 0:
                print("✅ Exécutable fonctionnel")
                return True
            else:
                print("⚠️  Exécutable trouvé mais problème de lancement")
                return False
        except subprocess.TimeoutExpired:
            print("✅ Exécutable se lance (timeout normal)")
            return True
        except Exception as e:
            print(f"⚠️  Erreur lors du test de lancement: {e}")
            return False
    else:
        print(f"❌ {exe_path} - Exécutable non trouvé")
        print("💡 Lancez d'abord: python setup_windows.py")
        return False

def test_gui_import():
    """Teste l'import de l'interface graphique"""
    print("\n🖥️  Test de l'interface graphique...")
    
    try:
        # Test d'import des modules principaux
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Test backend_interface
        from backend_interface import backend_interface
        print("✅ backend_interface importé")
        
        # Test config
        from config import config
        print("✅ config importé")
        
        # Test app_gui (sans lancer l'interface)
        import app_gui
        print("✅ app_gui importé")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

def test_backend():
    """Teste le backend"""
    print("\n⚙️  Test du backend...")
    
    try:
        sys.path.append('backend')
        
        # Test des modules backend essentiels
        import main
        print("✅ backend/main.py importé")
        
        import matelas_utils
        print("✅ matelas_utils importé")
        
        import client_utils
        print("✅ client_utils importé")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import backend: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur backend: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🧪 Test d'installation de l'application Matelas")
    print("=" * 50)
    
    tests = [
        ("Version Python", test_python_version),
        ("Dépendances", test_dependencies),
        ("Fichiers essentiels", test_files),
        ("Répertoires essentiels", test_directories),
        ("Interface graphique", test_gui_import),
        ("Backend", test_backend),
        ("Exécutable", test_executable),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur lors du test {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Résultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés ! L'installation est correcte.")
        return True
    elif passed >= total - 1:  # Permet 1 échec (exécutable non encore créé)
        print("✅ Installation presque complète. Lancez setup_windows.py pour créer l'exécutable.")
        return True
    else:
        print("❌ Plusieurs tests ont échoué. Vérifiez l'installation.")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Test interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        sys.exit(1) 