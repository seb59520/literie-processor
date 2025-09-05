#!/usr/bin/env python3
"""
Démonstration du système d'alerte de mise à jour
Modifie temporairement la version pour déclencher l'alerte
"""

from pathlib import Path
import shutil
from datetime import datetime

def create_demo_version():
    """Créer une version de démonstration avec version antérieure"""
    print("🎭 DÉMONSTRATION DU SYSTÈME D'ALERTE")
    print("=" * 40)
    
    # Sauvegarder le fichier version.py original
    original_version = Path("version.py")
    backup_version = Path("version_backup.py")
    
    print("💾 Sauvegarde de version.py...")
    shutil.copy2(original_version, backup_version)
    
    # Créer une version de démonstration avec version antérieure
    demo_version_content = '''#!/usr/bin/env python3
"""
Fichier de version centralisé pour l'application Matelas Processor - VERSION DEMO
"""

# Version principale de l'application (VERSION ANTÉRIEURE POUR DEMO)
VERSION = "3.8.0"

# Informations de build
BUILD_DATE = "2025-09-01"
BUILD_NUMBER = "20250901_demo"

# Informations complètes
VERSION_INFO = {
    "version": VERSION,
    "build_date": BUILD_DATE,
    "build_number": BUILD_NUMBER,
    "full_version": f"{VERSION} (Build {BUILD_NUMBER})"
}

def get_version():
    """Retourne la version de l'application"""
    return VERSION

def get_full_version():
    """Retourne la version complète avec build"""
    return VERSION_INFO["full_version"]

def get_version_info():
    """Retourne toutes les informations de version"""
    return VERSION_INFO.copy()

def get_changelog():
    """Retourne le changelog de l'application"""
    return """
# Changelog - Matelas Processor (VERSION DEMO)

## Version 3.8.0 (2025-09-01) - VERSION DE DÉMONSTRATION

### ⚠️ ATTENTION
Cette version est antérieure à la version 3.11.0 disponible sur le serveur.
L'indicateur de mise à jour dans la barre de statut devrait afficher une alerte rouge.

### 🎯 Test du système d'alerte
- Version locale: 3.8.0
- Version serveur: 3.11.0  
- Résultat attendu: Alerte rouge "Mise à jour: 3.8.0 → 3.11.0"
"""

if __name__ == "__main__":
    print(f"Matelas Processor - Version DEMO {get_full_version()}")
    print(f"Build date: {BUILD_DATE}")
    print(f"Build number: {BUILD_NUMBER}")
'''
    
    print("✏️ Création de la version de démonstration...")
    with open(original_version, 'w', encoding='utf-8') as f:
        f.write(demo_version_content)
    
    print(f"🎯 Version modifiée: 3.8.0 (antérieure à 3.11.0)")
    print(f"📋 Fichier sauvegardé: {backup_version}")
    
    return backup_version

def restore_original_version(backup_file):
    """Restaurer la version originale"""
    print("\\n🔄 Restauration de la version originale...")
    
    original_version = Path("version.py")
    
    if backup_file.exists():
        shutil.copy2(backup_file, original_version)
        backup_file.unlink()  # Supprimer le backup
        print("✅ Version originale restaurée")
        return True
    else:
        print("❌ Fichier de sauvegarde non trouvé")
        return False

def show_demo_instructions():
    """Afficher les instructions de démonstration"""
    print("\\n📋 INSTRUCTIONS DE DÉMONSTRATION")
    print("=" * 40)
    
    print("\\n🎯 Que va-t-il se passer:")
    print("1. L'application démarrera avec la version 3.8.0")
    print("2. Après 2 secondes, elle vérifiera les mises à jour")
    print("3. Elle détectera que la version 3.11.0 est disponible")
    print("4. L'indicateur passera au ROUGE avec le texte:")
    print("   'Mise à jour: 3.8.0 → 3.11.0'")
    
    print("\\n🖱️ Interactions possibles:")
    print("• Cliquez sur l'indicateur rouge pour ouvrir le dialog d'installation")
    print("• Le tooltip affichera: 'Nouvelle version 3.11.0 disponible ! Cliquez pour installer'")
    
    print("\\n⚠️ IMPORTANT:")
    print("• Cette démonstration utilise une version temporaire")
    print("• Après la démonstration, restaurez la version originale")
    print("• Ou utilisez le script de restauration fourni")

if __name__ == "__main__":
    try:
        # Créer la version de démonstration
        backup_file = create_demo_version()
        
        show_demo_instructions()
        
        print("\\n🚀 LANCEMENT DE LA DÉMONSTRATION")
        print("=" * 40)
        print("Démarrez maintenant l'application avec:")
        print("python3 app_gui.py")
        print()
        print("Observez la barre de statut en bas à droite!")
        print("L'indicateur devrait passer au rouge après quelques secondes.")
        print()
        
        input("Appuyez sur Entrée après avoir testé l'application...")
        
        # Restaurer automatiquement
        restore_original_version(backup_file)
        
        print("\\n🎉 DÉMONSTRATION TERMINÉE!")
        print("Version originale restaurée automatiquement.")
        
    except KeyboardInterrupt:
        print("\\n\\n⚠️ Démonstration interrompue")
        print("N'oubliez pas de restaurer la version originale!")
        
        if 'backup_file' in locals() and backup_file.exists():
            restore_original_version(backup_file)
            print("✅ Version originale restaurée")
    
    except Exception as e:
        print(f"\\n❌ Erreur: {e}")
        
        # Tentative de restauration en cas d'erreur
        backup_file = Path("version_backup.py")
        if backup_file.exists():
            restore_original_version(backup_file)
            print("✅ Version originale restaurée après erreur")