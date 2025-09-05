#!/usr/bin/env python3
"""
Script pour mettre à jour les chemins des référentiels dans tous les modules
pour utiliser la fonction get_referentiel_path du module asset_utils
"""

import os
import re
import glob

def update_referentiel_paths():
    """Met à jour les chemins des référentiels dans tous les modules"""
    
    print("=== MISE A JOUR DES CHEMINS REFERENTIELS ===")
    print()
    
    # Modules qui utilisent les référentiels
    modules_to_update = [
        "backend/latex_naturel_referentiel.py",
        "backend/latex_mixte7zones_referentiel.py", 
        "backend/mousse_rainuree7zones_referentiel.py",
        "backend/select43_utils.py",
        "backend/select43_longueur_housse_utils.py",
        "backend/latex_renforce_utils.py",
        "backend/latex_renforce_longueur_utils.py",
        "backend/mousse_visco_utils.py",
        "backend/mousse_visco_longueur_utils.py",
        "backend/latex_naturel_longueur_housse_utils.py",
        "backend/latex_mixte7zones_longueur_housse_utils.py",
        "backend/mousse_rainuree7zones_longueur_housse_utils.py"
    ]
    
    updated_count = 0
    
    for module_path in modules_to_update:
        if not os.path.exists(module_path):
            print(f"⚠️ Module non trouvé: {module_path}")
            continue
            
        print(f"📝 Traitement de: {module_path}")
        
        # Lire le contenu du fichier
        with open(module_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern pour détecter les référentiels
        patterns = [
            # Pattern pour REFERENTIEL_PATH = os.path.join(os.path.dirname(__file__), "Référentiels", "fichier.json")
            (r'REFERENTIEL_PATH\s*=\s*os\.path\.join\(os\.path\.dirname\(__file__\),\s*["\']Référentiels["\'],\s*["\']([^"\']+)["\']\)', 
             r'from .asset_utils import get_referentiel_path\nREFERENTIEL_PATH = get_referentiel_path(r"\1")'),
            
            # Pattern pour json_path = os.path.join(script_dir, "Référentiels", "fichier.json")
            (r'json_path\s*=\s*os\.path\.join\(script_dir,\s*["\']Référentiels["\'],\s*["\']([^"\']+)["\']\)',
             r'from .asset_utils import get_referentiel_path\njson_path = get_referentiel_path(r"\1")'),
        ]
        
        # Appliquer les patterns
        for pattern, replacement in patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                print(f"   ✅ Mis à jour: {pattern[:50]}...")
        
        # Si le contenu a changé, écrire le fichier
        if content != original_content:
            with open(module_path, 'w', encoding='utf-8') as f:
                f.write(content)
            updated_count += 1
            print(f"   💾 Fichier mis à jour")
        else:
            print(f"   ⏭️ Aucun changement nécessaire")
        
        print()
    
    print(f"=== RESUME ===")
    print(f"Modules traités: {len(modules_to_update)}")
    print(f"Modules mis à jour: {updated_count}")
    print()
    
    if updated_count > 0:
        print("✅ Les chemins des référentiels ont été mis à jour pour utiliser asset_utils")
        print("Les modules sont maintenant compatibles avec PyInstaller")
    else:
        print("ℹ️ Aucun module n'a nécessité de mise à jour")


def test_referentiels():
    """Test des référentiels après mise à jour"""
    print("=== TEST DES REFERENTIELS ===")
    print()
    
    try:
        from backend.asset_utils import get_referentiel_path
        
        test_files = [
            "dimensions_matelas.json",
            "longueurs_matelas.json",
            "latex_naturel_tencel_luxe3d_tencel_polyester.json",
            "mousse_rainuree7zones_tencel_luxe3d_tencel_polyester.json"
        ]
        
        for file in test_files:
            path = get_referentiel_path(file)
            if path:
                print(f"✅ {file}: {path}")
                print(f"   Existe: {os.path.exists(path)}")
            else:
                print(f"❌ {file}: Non trouvé")
            print()
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")


if __name__ == "__main__":
    update_referentiel_paths()
    print()
    test_referentiels() 