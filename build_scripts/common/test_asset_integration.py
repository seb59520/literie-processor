#!/usr/bin/env python3
import sys
import os

# Simuler le mode PyInstaller
if len(sys.argv) > 1 and sys.argv[1] == "--pyinstaller":
    # Simuler sys._MEIPASS
    sys._MEIPASS = os.path.dirname(os.path.abspath(__file__))

# Ajouter le backend au path
sys.path.append('backend')

try:
    from backend.asset_utils import get_asset_path, is_pyinstaller_mode
    
    print(f"Mode PyInstaller: {is_pyinstaller_mode()}")
    
    # Test des assets
    test_assets = ["lit-double.png", "logo_westelynck.png"]
    
    for asset in test_assets:
        path = get_asset_path(asset)
        if path:
            print(f"✅ {asset}: {path}")
            print(f"   Existe: {os.path.exists(path)}")
        else:
            print(f"❌ {asset}: Non trouvé")
        print()
        
except Exception as e:
    print(f"❌ Erreur: {e}")
