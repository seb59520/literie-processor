#!/usr/bin/env python3
"""
Script de test pour vérifier la gestion des chemins d'assets
"""

import sys
import os

# Ajouter le backend au path
sys.path.append('backend')

def test_asset_paths():
    """Test de la fonction get_asset_path"""
    print("=== TEST GESTION DES ASSETS ===")
    
    try:
        from backend.asset_utils import get_asset_path, is_pyinstaller_mode, get_base_path
        
        print(f"Mode PyInstaller: {is_pyinstaller_mode()}")
        print(f"Chemin de base: {get_base_path()}")
        print()
        
        # Test des assets
        test_assets = [
            "lit-double.png",
            "lit-double.ico", 
            "logo_westelynck.png",
            "logo_westelynck.svg"
        ]
        
        for asset in test_assets:
            path = get_asset_path(asset)
            if path:
                print(f"✅ {asset}: {path}")
                print(f"   Existe: {os.path.exists(path)}")
            else:
                print(f"❌ {asset}: Non trouvé")
            print()
        
        # Test des templates
        from backend.asset_utils import get_template_path
        test_templates = [
            "template_matelas.xlsx",
            "template_sommier.xlsx"
        ]
        
        print("=== TEST TEMPLATES ===")
        for template in test_templates:
            path = get_template_path(template)
            if path:
                print(f"✅ {template}: {path}")
                print(f"   Existe: {os.path.exists(path)}")
            else:
                print(f"❌ {template}: Non trouvé")
            print()
        
        # Test des configs
        from backend.asset_utils import get_config_path
        test_configs = [
            "mappings_matelas.json",
            "mappings_sommiers.json"
        ]
        
        print("=== TEST CONFIGS ===")
        for config in test_configs:
            path = get_config_path(config)
            if path:
                print(f"✅ {config}: {path}")
                print(f"   Existe: {os.path.exists(path)}")
            else:
                print(f"❌ {config}: Non trouvé")
            print()
        
        # Test des référentiels
        from backend.asset_utils import get_referentiel_path
        test_referentiels = [
            "dimensions_matelas.json",
            "7z_dimensions_matelas.json"
        ]
        
        print("=== TEST REFERENTIELS ===")
        for referentiel in test_referentiels:
            path = get_referentiel_path(referentiel)
            if path:
                print(f"✅ {referentiel}: {path}")
                print(f"   Existe: {os.path.exists(path)}")
            else:
                print(f"❌ {referentiel}: Non trouvé")
            print()
            
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
    except Exception as e:
        print(f"❌ Erreur: {e}")


if __name__ == "__main__":
    test_asset_paths() 