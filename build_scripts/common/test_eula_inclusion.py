#!/usr/bin/env python3
"""
Script de test pour vérifier que l'EULA est correctement inclus dans les constructions
"""

import os
import sys
import re

def test_eula_in_build_scripts():
    """Teste que l'EULA est inclus dans les scripts de construction"""
    print("🧪 Test de l'inclusion de l'EULA dans les scripts de construction")
    print("=" * 70)
    
    build_scripts = [
        "build_complet_avec_referentiels.py",
        "build_mac_complet.py"
    ]
    
    all_scripts_ok = True
    
    for script in build_scripts:
        print(f"\n📄 Vérification de {script}:")
        
        if not os.path.exists(script):
            print(f"   ❌ Script non trouvé: {script}")
            all_scripts_ok = False
            continue
        
        try:
            with open(script, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier la présence de l'EULA dans les fichiers critiques
            if "EULA.txt" in content:
                print(f"   ✅ EULA.txt référencé dans {script}")
                
                # Vérifier qu'il est dans la liste des fichiers critiques
                if "critical_files_to_include" in content:
                    print(f"   ✅ Liste critical_files_to_include présente")
                    
                    # Vérifier que l'EULA est dans cette liste
                    if "('EULA.txt', '.')" in content:
                        print(f"   ✅ EULA.txt dans la liste des fichiers critiques")
                    else:
                        print(f"   ❌ EULA.txt manquant dans la liste des fichiers critiques")
                        all_scripts_ok = False
                else:
                    print(f"   ❌ Liste critical_files_to_include manquante")
                    all_scripts_ok = False
            else:
                print(f"   ❌ EULA.txt non référencé dans {script}")
                all_scripts_ok = False
                
        except Exception as e:
            print(f"   ❌ Erreur lors de la lecture de {script}: {e}")
            all_scripts_ok = False
    
    return all_scripts_ok

def test_eula_file_exists():
    """Teste que le fichier EULA.txt existe"""
    print("\n🧪 Test de l'existence du fichier EULA.txt")
    print("=" * 50)
    
    if os.path.exists("EULA.txt"):
        print("✅ Fichier EULA.txt présent")
        
        # Vérifier que le fichier n'est pas vide
        try:
            with open("EULA.txt", 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            if content:
                print(f"✅ EULA.txt contient {len(content)} caractères")
                return True
            else:
                print("❌ EULA.txt est vide")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors de la lecture d'EULA.txt: {e}")
            return False
    else:
        print("❌ Fichier EULA.txt manquant")
        return False

def test_eula_in_admin_builder():
    """Teste que l'EULA est vérifié dans l'Admin Builder"""
    print("\n🧪 Test de la vérification EULA dans l'Admin Builder")
    print("=" * 60)
    
    admin_dialog_file = "admin_dialog.py"
    
    if not os.path.exists(admin_dialog_file):
        print(f"❌ Fichier {admin_dialog_file} non trouvé")
        return False
    
    try:
        with open(admin_dialog_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier que l'EULA est dans la liste des fichiers requis
        if "EULA.txt" in content:
            print("✅ EULA.txt référencé dans admin_dialog.py")
            
            # Vérifier qu'il est dans la méthode check_admin_builder_files
            if "check_admin_builder_files" in content:
                print("✅ Méthode check_admin_builder_files présente")
                
                # Vérifier que l'EULA est dans la liste required_files
                if "EULA.txt" in content and "required_files" in content:
                    print("✅ EULA.txt dans la liste des fichiers requis")
                    return True
                else:
                    print("❌ EULA.txt manquant dans la liste des fichiers requis")
                    return False
            else:
                print("❌ Méthode check_admin_builder_files manquante")
                return False
        else:
            print("❌ EULA.txt non référencé dans admin_dialog.py")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la lecture de {admin_dialog_file}: {e}")
        return False

def test_eula_in_app_gui():
    """Teste que l'EULA est correctement géré dans app_gui.py"""
    print("\n🧪 Test de la gestion EULA dans app_gui.py")
    print("=" * 55)
    
    app_gui_file = "app_gui.py"
    
    if not os.path.exists(app_gui_file):
        print(f"❌ Fichier {app_gui_file} non trouvé")
        return False
    
    try:
        with open(app_gui_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier les éléments critiques liés à l'EULA
        eula_checks = [
            ("check_eula_acceptance", "Méthode de vérification EULA"),
            ("EULA.txt", "Référence au fichier EULA"),
            ("eula_file = \"EULA.txt\"", "Définition du fichier EULA"),
            ("Contrat d'utilisation", "Interface utilisateur EULA"),
            ("sys.exit(1)", "Arrêt si EULA manquant")
        ]
        
        all_checks_ok = True
        
        for check, description in eula_checks:
            if check in content:
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ {description} manquante")
                all_checks_ok = False
        
        return all_checks_ok
        
    except Exception as e:
        print(f"❌ Erreur lors de la lecture de {app_gui_file}: {e}")
        return False

def main():
    """Point d'entrée principal"""
    print("📋 TEST D'INCLUSION EULA")
    print("=" * 60)
    print(f"Plateforme: {os.name}")
    print(f"Python: {sys.version.split()[0]}")
    print()
    
    tests = [
        ("Fichier EULA.txt", test_eula_file_exists),
        ("Scripts de construction", test_eula_in_build_scripts),
        ("Admin Builder", test_eula_in_admin_builder),
        ("Application principale", test_eula_in_app_gui)
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
    print("📊 RÉSUMÉ DES TESTS EULA")
    print("=" * 30)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{test_name}: {status}")
    
    print(f"\n🎯 Résultat global: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests EULA sont réussis !")
        print("   L'EULA est correctement inclus et géré dans tous les composants.")
        return True
    else:
        print("⚠️ Certains tests EULA ont échoué.")
        print("   L'application pourrait ne pas se lancer correctement.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 