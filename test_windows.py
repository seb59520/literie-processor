#!/usr/bin/env python3
"""
Script de test pour vérifier que tout fonctionne correctement sur Windows
avant de compiler l'exécutable
"""

import os
import sys
import platform

def test_system():
    """Teste l'environnement système"""
    print("=== TEST SYSTEME ===")
    print(f"OS: {platform.system()}")
    print(f"Version: {platform.release()}")
    print(f"Architecture: {platform.architecture()[0]}")
    print(f"Python: {platform.python_version()}")
    
    if platform.system() != "Windows":
        print("[!] ATTENTION: Ce script est concu pour Windows")
    else:
        print("[OK] Systeme Windows detecte")
    
    return True

def test_encoding():
    """Teste l'encodage des caractères"""
    print("\n=== TEST ENCODAGE ===")
    
    try:
        # Test d'écriture avec accents
        test_text = "Test d'encodage avec accents: àéêëîïôöùûü"
        with open("test_encoding.txt", "w", encoding="utf-8") as f:
            f.write(test_text)
        
        # Test de lecture
        with open("test_encoding.txt", "r", encoding="utf-8") as f:
            read_text = f.read()
        
        if test_text == read_text:
            print("[OK] Encodage UTF-8 fonctionne")
        else:
            print("[!] Probleme d'encodage detecte")
        
        # Nettoyer
        os.remove("test_encoding.txt")
        
    except Exception as e:
        print(f"[ERREUR] Test encodage: {e}")
        return False
    
    return True

def test_imports():
    """Teste l'import des modules principaux"""
    print("\n=== TEST IMPORTS ===")
    
    modules = [
        ("PyQt6.QtWidgets", "Interface graphique"),
        ("PyQt6.QtCore", "Core PyQt6"),
        ("requests", "Requetes HTTP"),
        ("pathlib", "Gestion chemins"),
        ("json", "JSON"),
        ("datetime", "Date/heure"),
        ("logging", "Logs"),
        ("webbrowser", "Navigateur"),
        ("subprocess", "Processus"),
        ("csv", "CSV"),
    ]
    
    success = 0
    total = len(modules)
    
    for module, desc in modules:
        try:
            __import__(module)
            print(f"[OK] {module:<20} - {desc}")
            success += 1
        except ImportError:
            print(f"[!] {module:<20} - {desc} (MANQUANT)")
    
    # Modules optionnels
    optional = [
        ("openpyxl", "Excel"),
        ("pandas", "Donnees"),
        ("psutil", "Monitoring"),
    ]
    
    print("\nModules optionnels:")
    for module, desc in optional:
        try:
            __import__(module)
            print(f"[OK] {module:<20} - {desc}")
        except ImportError:
            print(f"[!] {module:<20} - {desc} (optionnel)")
    
    if success == total:
        print(f"\n[OK] Tous les modules requis sont disponibles ({success}/{total})")
        return True
    else:
        print(f"\n[!] Modules manquants: {total - success}/{total}")
        return False

def test_application():
    """Teste l'import de l'application principale"""
    print("\n=== TEST APPLICATION ===")
    
    try:
        # Test sans interface graphique
        sys.argv = ['test']  # Éviter les arguments de ligne de commande
        
        import app_gui
        print("[OK] app_gui.py importable")
        
        # Test de la classe principale
        from PyQt6.QtWidgets import QApplication
        app = QApplication([])
        
        matelas_app = app_gui.MatelasApp()
        print("[OK] MatelasApp instanciable")
        
        # Test des méthodes critiques
        if hasattr(matelas_app, 'generate_html_report'):
            html = matelas_app.generate_html_report()
            if html and len(html) > 100:
                print("[OK] Generation HTML fonctionne")
            else:
                print("[!] Generation HTML problematique")
        
        return True
        
    except Exception as e:
        print(f"[ERREUR] Application: {e}")
        return False

def test_compilation_requirements():
    """Teste les prérequis pour PyInstaller"""
    print("\n=== TEST COMPILATION ===")
    
    try:
        import PyInstaller
        print(f"[OK] PyInstaller disponible: {PyInstaller.__version__}")
    except ImportError:
        print("[!] PyInstaller non installe")
        print("    pip install pyinstaller")
        return False
    
    # Vérifier les fichiers nécessaires
    files = [
        "app_gui.py",
        "config.py", 
        "matelas_config.json",
    ]
    
    missing = []
    for file in files:
        if os.path.exists(file):
            print(f"[OK] {file} present")
        else:
            print(f"[!] {file} manquant")
            missing.append(file)
    
    if missing:
        print(f"[!] Fichiers manquants: {missing}")
        return False
    
    return True

def main():
    print("=== TEST WINDOWS POUR COMPILATION ===")
    print("Application: Processeur de Devis Literie")
    print("=" * 50)
    
    tests = [
        ("Systeme", test_system),
        ("Encodage", test_encoding),
        ("Imports", test_imports),
        ("Application", test_application),
        ("Compilation", test_compilation_requirements),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n--- {name} ---")
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"[ERREUR] {name}: {e}")
            results.append(False)
    
    # Résumé
    success = sum(results)
    total = len(results)
    
    print(f"\n{'='*50}")
    print(f"RESULTAT: {success}/{total} tests reussis")
    
    if success == total:
        print("[OK] TOUS LES TESTS REUSSIS!")
        print("Vous pouvez compiler avec: python build_windows.py")
    else:
        print("[!] Certains tests ont echoue")
        print("Resolvez les problemes avant de compiler")
    
    print("=" * 50)
    
    return success == total

if __name__ == "__main__":
    success = main()
    input("\nAppuyez sur Entree pour fermer...")
    sys.exit(0 if success else 1)