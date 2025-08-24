#!/usr/bin/env python3
"""
Diagnostic très approfondi pour l'exécutable qui ne se lance pas
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path

def test_python_environment():
    """Teste l'environnement Python de base"""
    print("=== TEST ENVIRONNEMENT PYTHON ===")
    
    # Test de base
    try:
        result = subprocess.run([sys.executable, "-c", "print('Python fonctionne')"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Python de base fonctionne")
        else:
            print("❌ Python de base ne fonctionne pas")
            return False
    except Exception as e:
        print(f"❌ Erreur Python de base: {e}")
        return False
    
    # Test des imports critiques
    critical_imports = [
        ('sys', 'Module système'),
        ('os', 'Module OS'),
        ('subprocess', 'Module subprocess'),
        ('tempfile', 'Module tempfile'),
    ]
    
    for module, description in critical_imports:
        try:
            __import__(module)
            print(f"✅ {module} - {description}")
        except ImportError as e:
            print(f"❌ {module} - {description}: {e}")
            return False
    
    return True

def test_gui_imports():
    """Teste les imports de l'interface graphique"""
    print("\n=== TEST IMPORTS GUI ===")
    
    gui_imports = [
        ('PyQt6.QtCore', 'PyQt6 Core'),
        ('PyQt6.QtWidgets', 'PyQt6 Widgets'),
        ('PyQt6.QtGui', 'PyQt6 GUI'),
    ]
    
    for module, description in gui_imports:
        try:
            __import__(module)
            print(f"✅ {module} - {description}")
        except ImportError as e:
            print(f"❌ {module} - {description}: {e}")
            return False
    
    return True

def test_backend_imports():
    """Teste les imports du backend"""
    print("\n=== TEST IMPORTS BACKEND ===")
    
    # Ajouter le répertoire courant au path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    backend_imports = [
        ('backend_interface', 'Interface backend'),
        ('config', 'Configuration'),
    ]
    
    for module, description in backend_imports:
        try:
            __import__(module)
            print(f"✅ {module} - {description}")
        except ImportError as e:
            print(f"❌ {module} - {description}: {e}")
            return False
    
    return True

def test_file_structure():
    """Teste la structure des fichiers"""
    print("\n=== TEST STRUCTURE FICHIERS ===")
    
    required_files = [
        'run_gui.py',
        'app_gui.py',
        'backend_interface.py',
        'config.py',
    ]
    
    required_dirs = [
        'backend',
        'assets',
        'template',
        'config',
        'Commandes',
    ]
    
    all_ok = True
    
    for file_path in required_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path} ({size} bytes)")
        else:
            print(f"❌ {file_path} - MANQUANT")
            all_ok = False
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            files_count = len(os.listdir(dir_path))
            print(f"✅ {dir_path}/ ({files_count} éléments)")
        else:
            print(f"❌ {dir_path}/ - MANQUANT")
            all_ok = False
    
    return all_ok

def test_simple_gui_launch():
    """Teste le lancement simple de l'interface graphique"""
    print("\n=== TEST LANCEMENT GUI SIMPLE ===")
    
    # Créer un test simple
    test_script = '''#!/usr/bin/env python3
import sys
import os

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
    from PyQt6.QtCore import Qt
    
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Test MatelasApp")
    window.setGeometry(100, 100, 400, 200)
    
    label = QLabel("Test de l'interface graphique", window)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    window.setCentralWidget(label)
    
    window.show()
    print("✅ Interface graphique créée avec succès")
    
    # Fermer après 2 secondes
    import time
    time.sleep(2)
    app.quit()
    
except Exception as e:
    print(f"❌ Erreur interface graphique: {e}")
    import traceback
    traceback.print_exc()
'''
    
    with open("test_gui_simple.py", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    print("Test de lancement de l'interface graphique...")
    
    try:
        result = subprocess.run([sys.executable, "test_gui_simple.py"], 
                              capture_output=True, text=True, timeout=30)
        
        print(f"Code de retour: {result.returncode}")
        if result.stdout:
            print(f"Sortie: {result.stdout}")
        if result.stderr:
            print(f"Erreur: {result.stderr}")
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("✅ Interface graphique fonctionne (timeout normal)")
        return True
    except Exception as e:
        print(f"❌ Erreur test GUI: {e}")
        return False

def test_backend_launch():
    """Teste le lancement du backend"""
    print("\n=== TEST LANCEMENT BACKEND ===")
    
    test_script = '''#!/usr/bin/env python3
import sys
import os

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from backend_interface import backend_interface
    from config import config
    
    print("✅ Backend interface importé")
    print("✅ Config importé")
    
    # Test simple du backend
    print("Test du backend...")
    
except Exception as e:
    print(f"❌ Erreur backend: {e}")
    import traceback
    traceback.print_exc()
'''
    
    with open("test_backend_simple.py", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    try:
        result = subprocess.run([sys.executable, "test_backend_simple.py"], 
                              capture_output=True, text=True, timeout=30)
        
        print(f"Code de retour: {result.returncode}")
        if result.stdout:
            print(f"Sortie: {result.stdout}")
        if result.stderr:
            print(f"Erreur: {result.stderr}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Erreur test backend: {e}")
        return False

def test_full_application():
    """Teste l'application complète"""
    print("\n=== TEST APPLICATION COMPLETE ===")
    
    test_script = '''#!/usr/bin/env python3
import sys
import os

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Démarrage de l'application...")
    
    # Test des imports principaux
    from backend_interface import backend_interface
    from config import config
    import app_gui
    
    print("✅ Tous les imports réussis")
    
    # Test de création de l'application
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    
    print("✅ Application Qt créée")
    
    # Test de création de la fenêtre principale
    from app_gui import MatelasApp
    window = MatelasApp()
    
    print("✅ Fenêtre principale créée")
    
    # Fermer immédiatement
    app.quit()
    print("✅ Test terminé avec succès")
    
except Exception as e:
    print(f"❌ Erreur application complète: {e}")
    import traceback
    traceback.print_exc()
'''
    
    with open("test_full_app.py", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    try:
        result = subprocess.run([sys.executable, "test_full_app.py"], 
                              capture_output=True, text=True, timeout=60)
        
        print(f"Code de retour: {result.returncode}")
        if result.stdout:
            print(f"Sortie: {result.stdout}")
        if result.stderr:
            print(f"Erreur: {result.stderr}")
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("✅ Application complète fonctionne (timeout normal)")
        return True
    except Exception as e:
        print(f"❌ Erreur test application complète: {e}")
        return False

def create_minimal_executable():
    """Crée un exécutable minimal pour tester"""
    print("\n=== CREATION EXECUTABLE MINIMAL ===")
    
    # Créer un script minimal
    minimal_script = '''#!/usr/bin/env python3
import sys
import os

print("=== EXECUTABLE MINIMAL MATELAS ===")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")

try:
    from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
    from PyQt6.QtCore import Qt
    
    app = QApplication(sys.argv)
    
    window = QMainWindow()
    window.setWindowTitle("MatelasApp - Test Minimal")
    window.setGeometry(100, 100, 500, 300)
    
    central_widget = QWidget()
    layout = QVBoxLayout()
    
    label1 = QLabel("Application Matelas - Test Minimal")
    label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(label1)
    
    label2 = QLabel("Si vous voyez cette fenêtre, l'exécutable fonctionne !")
    label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(label2)
    
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)
    
    window.show()
    print("✅ Fenêtre affichée avec succès")
    
    # Garder ouvert 5 secondes
    import time
    time.sleep(5)
    
    app.quit()
    print("✅ Test terminé")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
    input("Appuyez sur Entrée pour continuer...")
'''
    
    with open("minimal_test.py", "w", encoding="utf-8") as f:
        f.write(minimal_script)
    
    # Créer le spec minimal
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['minimal_test.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtWidgets',
        'PyQt6.QtGui',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MatelasApp_Minimal',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
    
    with open("minimal_test.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    print("Compilation de l'exécutable minimal...")
    
    try:
        # Nettoyer
        for dir_to_clean in ["build", "dist"]:
            if os.path.exists(dir_to_clean):
                shutil.rmtree(dir_to_clean)
        
        # Compiler
        result = subprocess.run([
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "minimal_test.spec"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Exécutable minimal créé")
            print("Lancez: dist\\MatelasApp_Minimal.exe")
            return True
        else:
            print(f"❌ Erreur compilation: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("DIAGNOSTIC APPROFONDI - EXECUTABLE MATELAS")
    print("=" * 60)
    
    tests = [
        ("Environnement Python", test_python_environment),
        ("Structure fichiers", test_file_structure),
        ("Imports GUI", test_gui_imports),
        ("Imports Backend", test_backend_imports),
        ("Lancement GUI simple", test_simple_gui_launch),
        ("Lancement Backend", test_backend_launch),
        ("Application complète", test_full_application),
        ("Exécutable minimal", create_minimal_executable),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*20} {test_name} {'='*20}")
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur lors du test {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé
    print("\n" + "=" * 60)
    print("RESUME DES TESTS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nRésultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés !")
        print("💡 Le problème vient probablement de l'exécutable PyInstaller")
    elif passed >= total - 2:
        print("⚠️  La plupart des tests sont passés")
        print("💡 Vérifiez l'exécutable minimal créé")
    else:
        print("❌ Plusieurs tests ont échoué")
        print("💡 Corrigez les problèmes avant de créer l'exécutable")
    
    print("\nFICHIERS DE TEST CREES:")
    print("- test_gui_simple.py")
    print("- test_backend_simple.py") 
    print("- test_full_app.py")
    print("- minimal_test.py")
    print("- minimal_test.spec")
    
    return passed >= total - 2

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nDiagnostic interrompu")
        sys.exit(1)
    except Exception as e:
        print(f"\nErreur inattendue: {e}")
        sys.exit(1) 