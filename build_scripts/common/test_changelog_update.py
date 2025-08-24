#!/usr/bin/env python3
"""
Test du système de mise à jour du changelog
"""

import sys
import os
import tempfile
import shutil
from datetime import datetime

# Ajouter le répertoire courant au path
sys.path.append('.')

def test_changelog_update():
    """Test de la mise à jour du changelog"""
    print("=== Test de la mise à jour du changelog ===")
    
    try:
        from update_version import update_version_file, get_current_version
        
        # Créer un fichier version temporaire pour le test
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('''#!/usr/bin/env python3
"""
Fichier de version de test
"""

VERSION = "1.0.0"
BUILD_DATE = "2025-01-01"
BUILD_NUMBER = "20250101"

def get_changelog():
    """Retourne le changelog de l'application"""
    return """
# Changelog - Matelas Processor

## Version 1.0.0 (2025-01-01)

### 🎉 Nouveautés
- Version initiale
"""
''')
        temp_file = f.name
        
        # Sauvegarder le fichier original
        original_version_file = "version.py"
        backup_file = "version.py.backup"
        if os.path.exists(original_version_file):
            shutil.copy2(original_version_file, backup_file)
        
        try:
            # Copier le fichier temporaire vers version.py
            shutil.copy2(temp_file, original_version_file)
            
            # Test de mise à jour
            new_version = "1.1.0"
            new_date = "2025-01-02"
            new_build = "20250102"
            changelog_entry = "## Version 1.1.0 (2025-01-02)\n\n### 🔧 Améliorations\n- Test de mise à jour du changelog\n"
            
            print(f"Version avant mise à jour: {get_current_version()}")
            
            success = update_version_file(new_version, new_date, new_build, changelog_entry)
            
            if success:
                print(f"Version après mise à jour: {get_current_version()}")
                
                # Vérifier que le changelog a été mis à jour
                from version import get_changelog
                changelog = get_changelog()
                
                if "Version 1.1.0" in changelog:
                    print("✅ Changelog mis à jour avec succès!")
                    return True
                else:
                    print("❌ Changelog non mis à jour")
                    return False
            else:
                print("❌ Échec de la mise à jour")
                return False
                
        finally:
            # Restaurer le fichier original
            if os.path.exists(backup_file):
                shutil.copy2(backup_file, original_version_file)
                os.remove(backup_file)
            
            # Nettoyer
            os.unlink(temp_file)
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def test_current_changelog():
    """Test du changelog actuel"""
    print("\n=== Test du changelog actuel ===")
    
    try:
        from version import get_changelog, get_version
        
        changelog = get_changelog()
        current_version = get_version()
        
        print(f"Version actuelle: {current_version}")
        print(f"Changelog disponible (longueur: {len(changelog)} caractères)")
        
        # Vérifier que la version actuelle est dans le changelog
        if f"Version {current_version}" in changelog:
            print(f"✅ Version {current_version} trouvée dans le changelog")
            return True
        else:
            print(f"❌ Version {current_version} non trouvée dans le changelog")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test du changelog actuel: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Test du système de mise à jour du changelog")
    print("=" * 50)
    
    # Test du changelog actuel
    test1 = test_current_changelog()
    
    # Test de la mise à jour
    test2 = test_changelog_update()
    
    print("\n" + "=" * 50)
    if test1 and test2:
        print("✅ Tous les tests sont passés avec succès!")
    else:
        print("❌ Certains tests ont échoué")
    
    print("\n📋 Résumé:")
    print(f"  - Test changelog actuel: {'✅' if test1 else '❌'}")
    print(f"  - Test mise à jour: {'✅' if test2 else '❌'}") 