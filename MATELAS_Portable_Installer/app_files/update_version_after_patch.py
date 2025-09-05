#!/usr/bin/env python3
"""
Script pour mettre à jour le fichier version.py après installation d'un patch
"""

import re
from pathlib import Path
from datetime import datetime

def update_version_file(new_version: str, app_dir: Path = None):
    """
    Met à jour le fichier version.py avec la nouvelle version
    
    Args:
        new_version: La nouvelle version (ex: "3.10.1")
        app_dir: Répertoire de l'application (par défaut: répertoire courant)
    """
    if app_dir is None:
        app_dir = Path.cwd()
    
    version_file = app_dir / "version.py"
    
    if not version_file.exists():
        print(f"❌ Fichier version.py non trouvé: {version_file}")
        return False
    
    print(f"📝 Mise à jour de version.py: {new_version}")
    
    try:
        # Lire le fichier actuel
        with open(version_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Obtenir la date actuelle
        build_date = datetime.now().strftime("%Y-%m-%d")
        build_number = datetime.now().strftime("%Y%m%d")
        
        # Remplacer la version
        content = re.sub(
            r'VERSION = "[^"]*"',
            f'VERSION = "{new_version}"',
            content
        )
        
        # Remplacer la date de build
        content = re.sub(
            r'BUILD_DATE = "[^"]*"',
            f'BUILD_DATE = "{build_date}"',
            content
        )
        
        # Remplacer le numéro de build
        content = re.sub(
            r'BUILD_NUMBER = "[^"]*"',
            f'BUILD_NUMBER = "{build_number}"',
            content
        )
        
        # Sauvegarder le fichier mis à jour
        with open(version_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Version mise à jour: {new_version}")
        print(f"✅ Date de build: {build_date}")
        print(f"✅ Numéro de build: {build_number}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {e}")
        return False

def test_version_update():
    """Test de la mise à jour de version"""
    print("🧪 Test de mise à jour de version")
    print("=" * 40)
    
    # Sauvegarder la version actuelle
    version_file = Path("version.py")
    backup_file = Path("version.py.backup")
    
    if version_file.exists():
        with open(version_file, 'r') as f:
            original_content = f.read()
        
        with open(backup_file, 'w') as f:
            f.write(original_content)
        print("💾 Version actuelle sauvegardée")
    
    # Tester la mise à jour
    test_version = "3.10.1"
    success = update_version_file(test_version)
    
    if success:
        # Vérifier la mise à jour
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("version", version_file)
            version_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(version_module)
            
            print(f"🔍 Version lue: {version_module.VERSION}")
            print(f"🔍 Build date: {version_module.BUILD_DATE}")
            print(f"🔍 Build number: {version_module.BUILD_NUMBER}")
            
            if version_module.VERSION == test_version:
                print("✅ Test réussi!")
            else:
                print("❌ Test échoué - version non mise à jour")
                
        except Exception as e:
            print(f"❌ Erreur lors de la vérification: {e}")
    
    # Restaurer la version originale
    if backup_file.exists():
        with open(backup_file, 'r') as f:
            original_content = f.read()
        
        with open(version_file, 'w') as f:
            f.write(original_content)
        
        backup_file.unlink()
        print("🔄 Version originale restaurée")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Mode utilisation normale
        new_version = sys.argv[1]
        app_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else None
        
        print(f"📝 Mise à jour vers version {new_version}")
        success = update_version_file(new_version, app_dir)
        
        if success:
            print("✅ Mise à jour réussie")
            sys.exit(0)
        else:
            print("❌ Mise à jour échouée")
            sys.exit(1)
    else:
        # Mode test
        test_version_update()