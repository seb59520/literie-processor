#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de lancement pour l'application de test LLM
"""

import sys
import os
import subprocess

def check_dependencies():
    """Vérification des dépendances"""
    missing_deps = []
    
    # Vérifier PyQt
    try:
        import PyQt6
    except ImportError:
        try:
            import PyQt5
        except ImportError:
            missing_deps.append("PyQt5 ou PyQt6")
    
    # Vérifier les modules backend
    try:
        from config import config
        from backend.llm_provider import llm_manager
    except ImportError as e:
        missing_deps.append(f"Modules backend: {e}")
    
    if missing_deps:
        print("❌ Dépendances manquantes:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\n💡 Solutions:")
        print("   - Installer PyQt: pip install PyQt6 ou pip install PyQt5")
        print("   - Vérifier que vous êtes dans le répertoire racine du projet")
        return False
    
    return True

def main():
    """Fonction principale"""
    print("🚀 Lancement de l'application de test LLM...")
    
    # Vérifier les dépendances
    if not check_dependencies():
        sys.exit(1)
    
    # Vérifier que le fichier existe
    if not os.path.exists("test_llm_prompt.py"):
        print("❌ Fichier test_llm_prompt.py non trouvé")
        print("💡 Assurez-vous d'être dans le répertoire racine du projet")
        sys.exit(1)
    
    try:
        # Lancer l'application
        print("✅ Dépendances OK, lancement de l'application...")
        subprocess.run([sys.executable, "test_llm_prompt.py"])
        
    except KeyboardInterrupt:
        print("\n👋 Application fermée par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 