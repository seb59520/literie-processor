#!/usr/bin/env python3
"""
Script pour tester l'exécutable et diagnostiquer les erreurs
"""

import subprocess
import sys
import os
from pathlib import Path

def test_executable():
    """Teste l'exécutable et capture les erreurs"""
    print("🧪 Test de l'exécutable MatelasApp")
    print("=" * 40)
    
    executable_path = Path("dist/MatelasApp")
    if not executable_path.exists():
        print("❌ Exécutable non trouvé dans dist/MatelasApp")
        return False
    
    print(f"📁 Exécutable trouvé: {executable_path}")
    print("🚀 Lancement de l'application...")
    print("💡 L'application devrait s'ouvrir dans une nouvelle fenêtre")
    print("   Si elle ne s'ouvre pas, vérifiez les erreurs ci-dessous")
    print("-" * 40)
    
    try:
        # Lancer l'exécutable avec capture des erreurs
        result = subprocess.run(
            [str(executable_path)],
            capture_output=True,
            text=True,
            timeout=30  # Timeout de 30 secondes
        )
        
        if result.returncode == 0:
            print("✅ Application lancée avec succès!")
            if result.stdout:
                print("📤 Sortie standard:")
                print(result.stdout)
        else:
            print(f"❌ Erreur lors du lancement (code: {result.returncode})")
            if result.stderr:
                print("📤 Erreurs:")
                print(result.stderr)
            if result.stdout:
                print("📤 Sortie standard:")
                print(result.stdout)
                
    except subprocess.TimeoutExpired:
        print("✅ Application lancée (timeout atteint - normal pour une GUI)")
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False
    
    return True

def check_dependencies():
    """Vérifie les dépendances nécessaires"""
    print("\n🔍 Vérification des dépendances")
    print("=" * 40)
    
    dependencies = [
        'PyQt6',
        'openpyxl',
        'requests',
        'aiofiles',
        'asyncio'
    ]
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - MANQUANT")
    
    return True

def main():
    print("🚀 Diagnostic de l'exécutable MatelasApp")
    print("=" * 50)
    
    # Vérifier les dépendances
    check_dependencies()
    
    # Tester l'exécutable
    if test_executable():
        print("\n🎉 Test terminé!")
        print("💡 Si l'application ne s'ouvre pas, essayez:")
        print("   - Vérifier que vous avez les permissions d'exécution")
        print("   - Lancer depuis le terminal: ./dist/MatelasApp")
        print("   - Vérifier les logs dans le dossier logs/")
    else:
        print("\n❌ Problème détecté")
        print("💡 Essayez de recompiler avec:")
        print("   python3 build_debug_console_fixed.py")

if __name__ == "__main__":
    main() 