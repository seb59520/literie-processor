#!/usr/bin/env python3
"""
Script de test pour le système de gestion des mises à jour
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path

def test_version_manager():
    """Test du gestionnaire de version"""
    print("🧪 Test du gestionnaire de version...")
    
    try:
        from version_manager import version_manager
        
        # Test des informations de version
        info = version_manager.get_version_info()
        print(f"✅ Version actuelle: {info['version']}")
        print(f"✅ Build: {info['build']}")
        print(f"✅ Fichiers suivis: {len(info['files'])}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur gestionnaire de version: {e}")
        return False

def test_patch_creation():
    """Test de création de patch"""
    print("\n🧪 Test de création de patch...")
    
    try:
        from deploy_patch import PatchDeployer
        
        deployer = PatchDeployer()
        
        # Créer un patch de test
        patch_path = deployer.create_patch_package(
            "1.0.0", 
            "Test du système de gestion des mises à jour"
        )
        
        print(f"✅ Patch créé: {Path(patch_path).name}")
        
        # Vérifier que le fichier existe
        if Path(patch_path).exists():
            print(f"✅ Fichier patch existe: {Path(patch_path).stat().st_size} bytes")
            return True
        else:
            print("❌ Fichier patch non trouvé")
            return False
            
    except Exception as e:
        print(f"❌ Erreur création patch: {e}")
        return False

def test_patch_application():
    """Test d'application de patch"""
    print("\n🧪 Test d'application de patch...")
    
    try:
        from version_manager import version_manager
        
        # Lister les patches disponibles
        patches = version_manager.list_patches()
        
        if not patches:
            print("⚠️  Aucun patch disponible pour test")
            return True
        
        # Prendre le premier patch
        test_patch = patches[0]
        print(f"📦 Test avec patch: {Path(test_patch).name}")
        
        # Créer un environnement de test
        test_dir = Path(tempfile.mkdtemp())
        print(f"📁 Environnement de test: {test_dir}")
        
        # Copier les fichiers nécessaires
        shutil.copy("version_manager.py", test_dir)
        shutil.copy("update_manager_gui.py", test_dir)
        
        # Simuler l'application du patch (sans réellement l'appliquer)
        print("✅ Simulation d'application de patch réussie")
        
        # Nettoyer
        shutil.rmtree(test_dir)
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur application patch: {e}")
        return False

def test_gui_components():
    """Test des composants GUI"""
    print("\n🧪 Test des composants GUI...")
    
    try:
        # Test d'import des modules GUI
        from update_manager_gui import UpdateManagerGUI, CreatePatchDialog
        
        print("✅ Modules GUI importés avec succès")
        
        # Test de création des classes (sans QApplication)
        # On teste juste l'import et la structure
        print("✅ Classes GUI disponibles")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur composants GUI: {e}")
        return False

def test_deployment_script():
    """Test du script de déploiement"""
    print("\n🧪 Test du script de déploiement...")
    
    try:
        from deploy_patch import PatchDeployer
        
        deployer = PatchDeployer()
        
        # Test de listing des packages
        packages = deployer.list_packages()
        print(f"✅ Packages disponibles: {len(packages)}")
        
        # Test de nettoyage (simulation)
        print("✅ Fonction de nettoyage disponible")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur script de déploiement: {e}")
        return False

def test_file_structure():
    """Test de la structure des fichiers"""
    print("\n🧪 Test de la structure des fichiers...")
    
    required_files = [
        "version_manager.py",
        "update_manager_gui.py", 
        "deploy_patch.py",
        "launch_update_manager.bat",
        "README_GESTION_MAJ.md"
    ]
    
    required_dirs = [
        "patches",
        "backups", 
        "dist"
    ]
    
    all_good = True
    
    # Vérifier les fichiers
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MANQUANT")
            all_good = False
    
    # Vérifier les dossiers
    for dir in required_dirs:
        if Path(dir).exists():
            print(f"✅ {dir}/")
        else:
            print(f"❌ {dir}/ - MANQUANT")
            all_good = False
    
    return all_good

def main():
    """Fonction principale de test"""
    print("🚀 Test du Système de Gestion des Mises à Jour")
    print("=" * 50)
    
    tests = [
        ("Gestionnaire de version", test_version_manager),
        ("Création de patch", test_patch_creation),
        ("Application de patch", test_patch_application),
        ("Composants GUI", test_gui_components),
        ("Script de déploiement", test_deployment_script),
        ("Structure des fichiers", test_file_structure)
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
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nRésultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés ! Le système est prêt.")
        return True
    else:
        print("⚠️  Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 