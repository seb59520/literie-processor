#!/usr/bin/env python3
"""
Script simplifié pour créer et publier une nouvelle version
Usage simple pour l'usage quotidien
"""

import sys
from pathlib import Path

# Ajouter le répertoire courant au path
sys.path.insert(0, str(Path.cwd()))
sys.path.insert(0, str(Path.cwd() / "backend"))

def main():
    print("🎯 MATELAS - Nouvelle Version")
    print("=" * 40)
    
    # Demander le type de version
    print("📋 Types de version disponibles :")
    print("  1. 🐛 PATCH (3.9.0 → 3.9.1) - Corrections de bugs")
    print("  2. ✨ MINOR (3.9.0 → 3.10.0) - Nouvelles fonctionnalités")  
    print("  3. 🚀 MAJOR (3.9.0 → 4.0.0) - Changements majeurs")
    print("")
    
    while True:
        choice = input("Choisissez le type (1/2/3): ").strip()
        if choice == "1":
            version_type = "patch"
            break
        elif choice == "2":
            version_type = "minor"
            break
        elif choice == "3":
            version_type = "major"
            break
        else:
            print("❌ Choix invalide, veuillez saisir 1, 2 ou 3")
    
    # Demander la description
    print("")
    description = input("📝 Description de la version: ").strip()
    if not description:
        description = f"Version {version_type} automatique"
    
    # Confirmation
    print("")
    print("📋 Résumé :")
    print(f"   🔖 Type: {version_type.upper()}")
    print(f"   📝 Description: {description}")
    print("")
    
    confirm = input("Continuer ? (o/n): ").strip().lower()
    if confirm not in ['o', 'oui', 'y', 'yes']:
        print("❌ Annulé par l'utilisateur")
        return
    
    # Lancer le processus
    print("")
    print("🚀 Lancement du processus de build et publication...")
    print("=" * 50)
    
    try:
        from build_and_publish import BuildAndPublishSystem
        
        builder = BuildAndPublishSystem()
        success = builder.full_build_and_publish(version_type, description)
        
        if success:
            print("")
            print("🎊 SUCCÈS COMPLET !")
            print("✅ Nouvelle version créée et publiée")
            print("🔄 Vos clients recevront automatiquement la mise à jour")
            print("🌐 Interface admin: http://localhost:8081")
        else:
            print("")
            print("❌ Échec du processus")
            print("💡 Vérifiez les logs ci-dessus pour plus de détails")
            
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("💡 Assurez-vous que tous les fichiers sont présents")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Processus interrompu par l'utilisateur")