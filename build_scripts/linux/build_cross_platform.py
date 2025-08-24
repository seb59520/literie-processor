#!/usr/bin/env python3
"""
Script de compilation cross-platform pour Mac et Windows
"""

import os
import sys
import platform
import subprocess

def detect_platform():
    """Détecte la plateforme actuelle"""
    system = platform.system().lower()
    if system == "darwin":
        return "mac"
    elif system == "windows":
        return "windows"
    elif system == "linux":
        return "linux"
    else:
        return "unknown"

def build_for_platform(target_platform):
    """Compile pour la plateforme spécifiée"""
    print(f"🔨 Compilation pour {target_platform.upper()}...")
    
    if target_platform == "mac":
        script = "build_standalone_exe_final.py"
    elif target_platform == "windows":
        script = "build_windows_final.py"
    else:
        print(f"❌ Plateforme non supportée: {target_platform}")
        return False
    
    try:
        result = subprocess.run([sys.executable, script], check=True)
        print(f"✅ Compilation {target_platform} réussie!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur compilation {target_platform}: {e}")
        return False

def main():
    """Fonction principale"""
    current_platform = detect_platform()
    print(f"🚀 Compilation cross-platform MatelasApp")
    print(f"📱 Plateforme actuelle: {current_platform.upper()}")
    print("=" * 50)
    
    # Compiler pour la plateforme actuelle
    print(f"\n🎯 Compilation pour {current_platform.upper()}:")
    if build_for_platform(current_platform):
        print(f"✅ Version {current_platform} créée avec succès!")
    else:
        print(f"❌ Échec compilation {current_platform}")
    
    # Demander si compiler pour d'autres plateformes
    if current_platform == "mac":
        print(f"\n🌐 Voulez-vous aussi compiler pour Windows?")
        print("   Note: Cross-compilation Windows depuis Mac nécessite Wine")
        print("   Recommandation: Compilez directement sur Windows")
    
    print(f"\n📁 Résultats:")
    if current_platform == "mac":
        print(f"   - Mac: dist/MatelasApp")
    elif current_platform == "windows":
        print(f"   - Windows: dist/MatelasApp.exe")
        print(f"   - Installateur: MatelasApp_Windows/")

if __name__ == "__main__":
    main() 