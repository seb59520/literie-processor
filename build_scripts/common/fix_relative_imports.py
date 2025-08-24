#!/usr/bin/env python3
"""
Script pour corriger automatiquement les imports relatifs dans backend_interface.py
"""

import re

def fix_relative_imports():
    """Corrige tous les imports relatifs dans backend_interface.py"""
    
    # Lire le fichier
    with open('backend_interface.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Liste des modules backend à corriger
    backend_modules = [
        'dimensions_utils',
        'dimensions_sommiers', 
        'sommier_utils',
        'sommier_analytics_utils',
        'hauteur_utils',
        'fermete_utils',
        'housse_utils',
        'matiere_housse_utils',
        'poignees_utils',
        'latex_naturel_longueur_housse_utils',
        'latex_renforce_longueur_utils',
        'mousse_visco_longueur_utils',
        'latex_naturel_referentiel',
        'latex_renforce_utils',
        'decoupe_noyau_utils',
        'excel_import_utils',
        'excel_sommier_import_utils'
    ]
    
    # Corriger chaque import relatif
    for module in backend_modules:
        # Pattern pour trouver les imports relatifs
        pattern = rf'from {module} import'
        replacement = f'from backend.{module} import'
        
        # Appliquer la correction
        content = re.sub(pattern, replacement, content)
        print(f"✓ Corrigé: {module}")
    
    # Écrire le fichier corrigé
    with open('backend_interface.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Tous les imports relatifs ont été corrigés !")

if __name__ == "__main__":
    fix_relative_imports() 