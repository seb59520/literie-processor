#!/usr/bin/env python3
"""
Script de diagnostic pour l'installation Windows
"""

import os
import sys
import subprocess
import importlib
from pathlib import Path

def check_python_environment():
    """Vérifie l'environnement Python"""
    print("🐍 DIAGNOSTIC ENVIRONNEMENT PYTHON")
    print("=" * 50)
    
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Python path: {sys.path[:3]}...")
    print(f"Platform: {sys.platform}")
    print(f"Architecture: {sys.maxsize > 2**32 and '64-bit' or '32-bit'}")
    
    # Vérifier pip
    try:
        import pip
        print(f"Pip version: {pip.__version__}")
    except ImportError:
        print("❌ Pip non disponible")
        return False
    
    return True

def check_pyinstaller():
    """Vérifie PyInstaller"""
    print("\n🔧 DIAGNOSTIC PYINSTALLER")
    print("=" * 50)
    
    try:
        import PyInstaller
        print(f"PyInstaller version: {PyInstaller.__version__}")
        
        # Test de commande
        result = subprocess.run([
            sys.executable, "-m", "PyInstaller", "--version"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✅ PyInstaller fonctionne: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ PyInstaller ne fonctionne pas: {result.stderr}")
            return False
            
    except ImportError:
        print("❌ PyInstaller non installé")
        return False
    except Exception as e:
        print(f"❌ Erreur PyInstaller: {e}")
        return False

def check_dependencies():
    """Vérifie les dépendances critiques"""
    print("\n📦 DIAGNOSTIC DÉPENDANCES")
    print("=" * 50)
    
    critical_deps = [
        ('PyQt6', 'Interface graphique'),
        ('fitz', 'Traitement PDF'),
        ('openpyxl', 'Export Excel'),
        ('httpx', 'API HTTP'),
        ('jinja2', 'Templates'),
        ('cryptography', 'Chiffrement'),
    ]
    
    all_ok = True
    for module, description in critical_deps:
        try:
            importlib.import_module(module)
            print(f"✅ {module} - {description}")
        except ImportError as e:
            print(f"❌ {module} - {description} - ERREUR: {e}")
            all_ok = False
    
    return all_ok

def check_project_structure():
    """Vérifie la structure du projet"""
    print("\n📁 DIAGNOSTIC STRUCTURE PROJET")
    print("=" * 50)
    
    required_files = [
        'run_gui.py',
        'app_gui.py',
        'backend_interface.py',
        'config.py',
        'setup_windows.py',
    ]
    
    required_dirs = [
        'backend',
        'assets',
        'template',
        'config',
        'Référentiels',
        'Commandes',
    ]
    
    all_ok = True
    
    print("Fichiers requis:")
    for file_path in required_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path} ({size} bytes)")
        else:
            print(f"❌ {file_path} - MANQUANT")
            all_ok = False
    
    print("\nRépertoires requis:")
    for dir_path in required_dirs:
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            files_count = len(os.listdir(dir_path))
            print(f"✅ {dir_path}/ ({files_count} éléments)")
        else:
            print(f"❌ {dir_path}/ - MANQUANT")
            all_ok = False
    
    return all_ok

def check_imports():
    """Teste les imports critiques"""
    print("\n📥 DIAGNOSTIC IMPORTS")
    print("=" * 50)
    
    try:
        # Test des imports principaux
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        print("Test backend_interface...")
        from backend_interface import backend_interface
        print("✅ backend_interface importé")
        
        print("Test config...")
        from config import config
        print("✅ config importé")
        
        print("Test app_gui...")
        import app_gui
        print("✅ app_gui importé")
        
        print("Test backend...")
        sys.path.append('backend')
        import main
        print("✅ backend/main importé")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

def test_simple_build():
    """Teste une compilation simple"""
    print("\n🔨 TEST COMPILATION SIMPLE")
    print("=" * 50)
    
    try:
        # Créer un fichier test simple
        test_file = "test_simple.py"
        with open(test_file, "w") as f:
            f.write('''#!/usr/bin/env python3
print("Hello World!")
''')
        
        print("Test avec un fichier simple...")
        result = subprocess.run([
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            test_file
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ Compilation simple réussie")
            
            # Nettoyer
            if os.path.exists("dist/test_simple.exe"):
                os.remove("dist/test_simple.exe")
            if os.path.exists("build"):
                import shutil
                shutil.rmtree("build")
            if os.path.exists("dist"):
                import shutil
                shutil.rmtree("dist")
            if os.path.exists("test_simple.spec"):
                os.remove("test_simple.spec")
            if os.path.exists(test_file):
                os.remove(test_file)
            
            return True
        else:
            print(f"❌ Compilation simple échouée:")
            print(f"Erreur: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur test compilation: {e}")
        return False

def main():
    """Fonction principale de diagnostic"""
    print("🔍 DIAGNOSTIC COMPLET - INSTALLATION WINDOWS")
    print("=" * 60)
    
    tests = [
        ("Environnement Python", check_python_environment),
        ("PyInstaller", check_pyinstaller),
        ("Dépendances critiques", check_dependencies),
        ("Structure projet", check_project_structure),
        ("Imports", check_imports),
        ("Test compilation simple", test_simple_build),
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
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DIAGNOSTIC")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Résultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés ! L'installation devrait fonctionner.")
        print("💡 Lancez: python setup_windows.py")
    elif passed >= total - 1:
        print("⚠️  Presque tous les tests sont passés. L'installation peut fonctionner.")
        print("💡 Lancez: python setup_windows.py")
    else:
        print("❌ Plusieurs tests ont échoué. Corrigez les problèmes avant l'installation.")
        print("\n🔧 SOLUTIONS RECOMMANDÉES:")
        print("1. Réinstallez Python 3.8+ avec 'Add to PATH'")
        print("2. Mettez à jour pip: python -m pip install --upgrade pip")
        print("3. Réinstallez PyInstaller: pip install --force-reinstall pyinstaller")
        print("4. Vérifiez que tous les fichiers du projet sont présents")
    
    return passed >= total - 1

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Diagnostic interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        sys.exit(1) 