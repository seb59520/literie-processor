#!/usr/bin/env python3
"""
Script de test pour l'Admin Builder
Teste les fonctionnalités principales de l'interface d'administration
"""

import os
import sys
import subprocess
import platform
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

def test_admin_builder_launch():
    """Teste le lancement de l'Admin Builder"""
    print("🧪 Test de lancement de l'Admin Builder")
    print("=" * 50)
    
    try:
        # Créer une application Qt
        app = QApplication(sys.argv)
        
        # Importer l'Admin Builder
        from admin_builder_gui import AdminBuilderGUI
        
        # Créer l'interface
        window = AdminBuilderGUI()
        window.show()
        
        print("✅ Interface Admin Builder créée avec succès")
        print("✅ Fenêtre affichée")
        
        # Fermer automatiquement après 5 secondes
        timer = QTimer()
        timer.singleShot(5000, window.close)
        timer.singleShot(6000, app.quit)
        
        print("⏰ Fermeture automatique dans 5 secondes...")
        
        # Lancer l'application
        app.exec()
        
        print("✅ Test de lancement réussi")
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def test_build_scripts():
    """Teste la présence et la validité des scripts de construction"""
    print("\n🧪 Test des scripts de construction")
    print("=" * 50)
    
    scripts_to_test = [
        "build_complet_avec_referentiels.py",
        "build_mac_complet.py",
        "test_referentiels_inclus.py"
    ]
    
    all_valid = True
    
    for script in scripts_to_test:
        if os.path.exists(script):
            print(f"✅ {script} - Présent")
            
            # Test de syntaxe Python
            try:
                with open(script, 'r', encoding='utf-8') as f:
                    compile(f.read(), script, 'exec')
                print(f"   ✅ Syntaxe Python valide")
            except SyntaxError as e:
                print(f"   ❌ Erreur de syntaxe: {e}")
                all_valid = False
        else:
            print(f"❌ {script} - Manquant")
            all_valid = False
    
    return all_valid

def test_dependencies():
    """Teste les dépendances nécessaires"""
    print("\n🧪 Test des dépendances")
    print("=" * 50)
    
    dependencies = [
        ("PyQt6", "PyQt6"),
        ("PyInstaller", "PyInstaller"),
        ("subprocess", "subprocess"),
        ("threading", "threading"),
        ("platform", "platform")
    ]
    
    all_available = True
    
    for name, module in dependencies:
        try:
            __import__(module)
            print(f"✅ {name} - Disponible")
        except ImportError:
            print(f"❌ {name} - Manquant")
            all_available = False
    
    return all_available

def test_file_structure():
    """Teste la structure des fichiers nécessaires"""
    print("\n🧪 Test de la structure des fichiers")
    print("=" * 50)
    
    required_files = [
        "app_gui.py",
        "backend/",
        "config/",
        "template/",
        "assets/"
    ]
    
    all_present = True
    
    for file_path in required_files:
        if os.path.exists(file_path):
            if os.path.isdir(file_path):
                print(f"✅ {file_path} - Dossier présent")
            else:
                print(f"✅ {file_path} - Fichier présent")
        else:
            print(f"❌ {file_path} - Manquant")
            all_present = False
    
    return all_present

def main():
    """Point d'entrée principal"""
    print("🔨 TEST ADMIN BUILDER")
    print("=" * 60)
    print(f"Plateforme: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version.split()[0]}")
    print()
    
    tests = [
        ("Dépendances", test_dependencies),
        ("Structure des fichiers", test_file_structure),
        ("Scripts de construction", test_build_scripts),
        ("Lancement Admin Builder", test_admin_builder_launch)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"🧪 {test_name}")
        print("-" * 30)
        
        try:
            result = test_func()
            results.append((test_name, result))
            
            if result:
                print(f"✅ {test_name} - RÉUSSI")
            else:
                print(f"❌ {test_name} - ÉCHOUÉ")
                
        except Exception as e:
            print(f"❌ {test_name} - ERREUR: {e}")
            results.append((test_name, False))
        
        print()
    
    # Résumé
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 30)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{test_name}: {status}")
    
    print(f"\n🎯 Résultat global: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont réussis !")
        print("   L'Admin Builder est prêt à être utilisé.")
        return True
    else:
        print("⚠️ Certains tests ont échoué.")
        print("   Vérifiez les erreurs ci-dessus avant d'utiliser l'Admin Builder.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 