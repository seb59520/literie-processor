#!/usr/bin/env python3
"""
Script de lancement pour l'Admin Builder
Interface d'administration pour la génération d'exécutables
"""

import os
import sys
import subprocess
import platform

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    print("🔍 Vérification des dépendances...")
    
    # Vérifier PyQt6
    try:
        import PyQt6
        print("✅ PyQt6 installé")
    except ImportError:
        print("❌ PyQt6 non installé")
        print("   Installation: pip install PyQt6")
        return False
    
    # Vérifier PyInstaller
    try:
        import PyInstaller
        print("✅ PyInstaller installé")
    except ImportError:
        print("❌ PyInstaller non installé")
        print("   Installation: pip install pyinstaller")
        return False
    
    return True

def check_scripts():
    """Vérifie que tous les scripts nécessaires sont présents"""
    print("📁 Vérification des scripts...")
    
    required_scripts = [
        "build_complet_avec_referentiels.py",
        "build_mac_complet.py", 
        "test_referentiels_inclus.py"
    ]
    
    missing_scripts = []
    for script in required_scripts:
        if os.path.exists(script):
            print(f"✅ {script}")
        else:
            print(f"❌ {script}")
            missing_scripts.append(script)
    
    if missing_scripts:
        print(f"\n⚠️ Scripts manquants: {len(missing_scripts)}")
        for script in missing_scripts:
            print(f"   - {script}")
        print("   L'Admin Builder peut ne pas fonctionner correctement.")
        return False
    
    return True

def launch_admin_builder():
    """Lance l'Admin Builder"""
    print("🚀 Lancement de l'Admin Builder...")
    
    try:
        # Lancer l'application
        result = subprocess.run([
            sys.executable, "admin_builder_gui.py"
        ], check=True)
        
        print("✅ Admin Builder fermé normalement")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors du lancement: {e}")
        return False
    except KeyboardInterrupt:
        print("\n⏹️ Arrêt demandé par l'utilisateur")
        return True
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

def main():
    """Point d'entrée principal"""
    print("=" * 60)
    print("🔨 ADMIN BUILDER - LANCEUR")
    print("=" * 60)
    print(f"Plateforme: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version.split()[0]}")
    print()
    
    # Vérifications préalables
    if not check_dependencies():
        print("\n❌ Dépendances manquantes")
        print("   Installez les dépendances manquantes avant de relancer.")
        return False
    
    print()
    
    if not check_scripts():
        print("\n⚠️ Certains scripts sont manquants")
        print("   L'Admin Builder peut ne pas fonctionner correctement.")
        
        response = input("\nContinuer quand même ? (o/N): ").strip().lower()
        if response not in ['o', 'oui', 'y', 'yes']:
            print("❌ Arrêt demandé par l'utilisateur")
            return False
    
    print()
    
    # Lancer l'Admin Builder
    success = launch_admin_builder()
    
    if success:
        print("\n✅ Admin Builder terminé avec succès")
    else:
        print("\n❌ Erreur lors de l'exécution de l'Admin Builder")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 