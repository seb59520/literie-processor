#!/usr/bin/env python3
"""
Test de compatibilité des référentiels après mise à jour
"""

import sys
import os

# Ajouter le backend au path
sys.path.append('backend')

def test_referentiels_modules():
    """Test des modules de référentiels mis à jour"""
    print("=== TEST COMPATIBILITE REFERENTIELS ===")
    print()
    
    try:
        # Test du module latex_naturel_referentiel
        print("🧪 Test latex_naturel_referentiel...")
        from backend.latex_naturel_referentiel import get_valeur_latex_naturel, REFERENTIEL_PATH
        
        print(f"   REFERENTIEL_PATH: {REFERENTIEL_PATH}")
        print(f"   Existe: {os.path.exists(REFERENTIEL_PATH) if REFERENTIEL_PATH else False}")
        
        # Test d'une valeur
        try:
            valeur = get_valeur_latex_naturel(79, "LUXE 3D")
            print(f"   ✅ Test fonctionnel: 79 LUXE 3D = {valeur}")
        except Exception as e:
            print(f"   ❌ Erreur test: {e}")
        
        print()
        
        # Test du module select43_utils
        print("🧪 Test select43_utils...")
        from backend.select43_utils import get_select43_value
        
        try:
            valeur = get_select43_value(79, "LUXE 3D")
            print(f"   ✅ Test fonctionnel: 79 LUXE 3D = {valeur}")
        except Exception as e:
            print(f"   ❌ Erreur test: {e}")
        
        print()
        
        # Test du module mousse_visco_utils
        print("🧪 Test mousse_visco_utils...")
        from backend.mousse_visco_utils import get_mousse_visco_value
        
        try:
            valeur = get_mousse_visco_value(79, "LUXE 3D")
            print(f"   ✅ Test fonctionnel: 79 LUXE 3D = {valeur}")
        except Exception as e:
            print(f"   ❌ Erreur test: {e}")
        
        print()
        
        print("✅ Tous les tests de référentiels sont passés!")
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
    except Exception as e:
        print(f"❌ Erreur: {e}")


def test_pyinstaller_simulation():
    """Simule le comportement en mode PyInstaller"""
    print("=== TEST SIMULATION PYINSTALLER ===")
    print()
    
    # Simuler sys._MEIPASS
    import sys
    original_meipass = getattr(sys, '_MEIPASS', None)
    sys._MEIPASS = os.path.dirname(os.path.abspath(__file__))
    
    try:
        from backend.asset_utils import get_referentiel_path, is_pyinstaller_mode
        
        print(f"Mode PyInstaller: {is_pyinstaller_mode()}")
        print(f"Base path: {sys._MEIPASS}")
        print()
        
        # Test des référentiels en mode PyInstaller simulé
        test_files = [
            "dimensions_matelas.json",
            "latex_naturel_tencel_luxe3d_tencel_polyester.json",
            "select43_tencel_luxe3d_tencel_polyester.json"
        ]
        
        for file in test_files:
            path = get_referentiel_path(file)
            if path:
                print(f"✅ {file}: {path}")
                print(f"   Existe: {os.path.exists(path)}")
            else:
                print(f"❌ {file}: Non trouvé")
            print()
        
        print("✅ Simulation PyInstaller réussie!")
        
    except Exception as e:
        print(f"❌ Erreur simulation: {e}")
    finally:
        # Restaurer l'état original
        if original_meipass is None:
            delattr(sys, '_MEIPASS')
        else:
            sys._MEIPASS = original_meipass


if __name__ == "__main__":
    test_referentiels_modules()
    print()
    test_pyinstaller_simulation() 