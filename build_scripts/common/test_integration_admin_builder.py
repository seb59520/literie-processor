#!/usr/bin/env python3
"""
Script de test pour l'intégration de l'Admin Builder dans le menu d'administration
"""

import os
import sys
import subprocess
import platform
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

def test_admin_dialog_integration():
    """Teste l'intégration de l'Admin Builder dans le dialogue d'administration"""
    print("🧪 Test d'intégration Admin Builder dans le dialogue d'administration")
    print("=" * 70)
    
    try:
        # Créer une application Qt
        app = QApplication(sys.argv)
        
        # Importer le dialogue d'administration
        from admin_dialog import AdminDialog
        
        # Créer le dialogue (sans authentification pour le test)
        dialog = AdminDialog()
        
        # Vérifier que l'onglet Admin Builder est présent
        tab_widget = dialog.tab_widget
        admin_builder_tab_index = -1
        
        for i in range(tab_widget.count()):
            if "Admin Builder" in tab_widget.tabText(i):
                admin_builder_tab_index = i
                break
        
        if admin_builder_tab_index >= 0:
            print("✅ Onglet Admin Builder trouvé dans le dialogue d'administration")
            
            # Activer l'onglet Admin Builder
            tab_widget.setCurrentIndex(admin_builder_tab_index)
            print("✅ Onglet Admin Builder activé")
            
            # Vérifier que les méthodes sont présentes
            if hasattr(dialog, 'launch_admin_builder'):
                print("✅ Méthode launch_admin_builder présente")
            else:
                print("❌ Méthode launch_admin_builder manquante")
            
            if hasattr(dialog, 'test_admin_builder'):
                print("✅ Méthode test_admin_builder présente")
            else:
                print("❌ Méthode test_admin_builder manquante")
            
            if hasattr(dialog, 'show_admin_builder_docs'):
                print("✅ Méthode show_admin_builder_docs présente")
            else:
                print("❌ Méthode show_admin_builder_docs manquante")
            
            if hasattr(dialog, 'check_admin_builder_files'):
                print("✅ Méthode check_admin_builder_files présente")
            else:
                print("❌ Méthode check_admin_builder_files manquante")
            
        else:
            print("❌ Onglet Admin Builder non trouvé dans le dialogue d'administration")
            return False
        
        # Fermer automatiquement après 3 secondes
        timer = QTimer()
        timer.singleShot(3000, dialog.close)
        timer.singleShot(3500, app.quit)
        
        print("⏰ Fermeture automatique dans 3 secondes...")
        
        # Lancer le dialogue
        dialog.show()
        app.exec()
        
        print("✅ Test d'intégration réussi")
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def test_admin_builder_files():
    """Teste la présence des fichiers requis pour l'Admin Builder"""
    print("\n🧪 Test des fichiers Admin Builder")
    print("=" * 50)
    
    required_files = [
        "admin_builder_gui.py",
        "build_complet_avec_referentiels.py",
        "build_mac_complet.py",
        "test_referentiels_inclus.py",
        "test_admin_builder.py",
        "RESUME_ADMIN_BUILDER.md",
        "EULA.txt"  # Fichier critique pour le lancement de l'application
    ]
    
    all_present = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} - Présent")
        else:
            print(f"❌ {file} - Manquant")
            all_present = False
    
    return all_present

def test_admin_dialog_file():
    """Teste que le fichier admin_dialog.py contient les nouvelles méthodes"""
    print("\n🧪 Test du fichier admin_dialog.py")
    print("=" * 50)
    
    try:
        with open("admin_dialog.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_methods = [
            "create_admin_builder_tab",
            "launch_admin_builder",
            "test_admin_builder",
            "show_admin_builder_docs",
            "check_admin_builder_files"
        ]
        
        all_methods_present = True
        
        for method in required_methods:
            if method in content:
                print(f"✅ Méthode {method} présente")
            else:
                print(f"❌ Méthode {method} manquante")
                all_methods_present = False
        
        # Vérifier l'ajout de l'onglet
        if "create_admin_builder_tab()" in content:
            print("✅ Appel à create_admin_builder_tab présent")
        else:
            print("❌ Appel à create_admin_builder_tab manquant")
            all_methods_present = False
        
        return all_methods_present
        
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du fichier: {e}")
        return False

def test_app_gui_integration():
    """Teste que l'application principale peut accéder à l'Admin Builder"""
    print("\n🧪 Test d'intégration avec l'application principale")
    print("=" * 60)
    
    try:
        # Vérifier que la méthode show_admin_dialog existe dans app_gui.py
        with open("app_gui.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "show_admin_dialog" in content:
            print("✅ Méthode show_admin_dialog présente dans app_gui.py")
        else:
            print("❌ Méthode show_admin_dialog manquante dans app_gui.py")
            return False
        
        if "from admin_dialog import show_admin_dialog" in content:
            print("✅ Import de admin_dialog présent dans app_gui.py")
        else:
            print("❌ Import de admin_dialog manquant dans app_gui.py")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

def main():
    """Point d'entrée principal"""
    print("🔨 TEST D'INTÉGRATION ADMIN BUILDER")
    print("=" * 60)
    print(f"Plateforme: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version.split()[0]}")
    print()
    
    tests = [
        ("Fichiers Admin Builder", test_admin_builder_files),
        ("Fichier admin_dialog.py", test_admin_dialog_file),
        ("Intégration app_gui.py", test_app_gui_integration),
        ("Dialogue d'administration", test_admin_dialog_integration)
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
        print("   L'Admin Builder est correctement intégré dans le menu d'administration.")
        return True
    else:
        print("⚠️ Certains tests ont échoué.")
        print("   Vérifiez les erreurs ci-dessus avant d'utiliser l'Admin Builder.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 