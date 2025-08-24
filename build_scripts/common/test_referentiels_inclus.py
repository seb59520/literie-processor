#!/usr/bin/env python3
"""
Script de test pour vérifier que tous les référentiels sont bien inclus
"""

import os
import sys
import json
from pathlib import Path

def test_referentiels_inclus():
    """Teste que tous les référentiels sont bien inclus"""
    
    print("🔍 TEST DES RÉFÉRENTIELS INCLUS")
    print("=" * 50)
    
    # Vérifier les référentiels critiques
    referentiels_critiques = [
        "backend/Référentiels/dimensions_matelas.json",
        "backend/Référentiels/longueurs_matelas.json",
        "backend/Référentiels/7z_dimensions_matelas.json",
        "backend/Référentiels/7z_longueurs_matelas.json",
        "backend/Référentiels/s43_dimensions_matelas.json",
        "backend/Référentiels/s43_longueurs_matelas.json",
        "backend/Référentiels/latex_naturel_longueur_housse.json",
        "backend/Référentiels/latex_mixte7zones_longueur_housse.json",
        "backend/Référentiels/latex_renforce_longueur_housse.json",
        "backend/Référentiels/mousse_rainuree7zones_longueur_housse.json",
        "backend/Référentiels/mousse_visco_longueur_tencel.json",
        "backend/Référentiels/select43_longueur_housse.json",
    ]
    
    print("📋 Vérification des référentiels critiques:")
    missing_critical = []
    
    for ref in referentiels_critiques:
        if os.path.exists(ref):
            # Vérifier que le fichier JSON est valide
            try:
                with open(ref, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"   ✅ {ref} (valide, {len(data)} entrées)")
            except json.JSONDecodeError as e:
                print(f"   ⚠️ {ref} (JSON invalide: {e})")
            except Exception as e:
                print(f"   ❌ {ref} (erreur: {e})")
                missing_critical.append(ref)
        else:
            print(f"   ❌ {ref} (manquant)")
            missing_critical.append(ref)
    
    print()
    
    # Lister tous les fichiers de référentiels
    referentiels_dir = "backend/Référentiels"
    if os.path.exists(referentiels_dir):
        print("📁 Tous les fichiers de référentiels:")
        all_refs = []
        for root, dirs, files in os.walk(referentiels_dir):
            for file in files:
                if file.endswith(('.json', '.csv')):
                    file_path = os.path.join(root, file)
                    all_refs.append(file_path)
                    print(f"   📄 {file_path}")
        
        print(f"\n📊 Statistiques:")
        print(f"   Total référentiels: {len(all_refs)}")
        print(f"   Référentiels critiques manquants: {len(missing_critical)}")
        
        if missing_critical:
            print(f"\n⚠️ Référentiels critiques manquants:")
            for ref in missing_critical:
                print(f"   - {ref}")
        else:
            print(f"\n✅ Tous les référentiels critiques sont présents")
            
    else:
        print(f"❌ Dossier référentiels non trouvé: {referentiels_dir}")
    
    print()
    
    # Vérifier les templates
    print("📋 Vérification des templates:")
    templates_critiques = [
        "template/template_matelas.xlsx",
        "template/template_sommier.xlsx",
        "backend/template/template_matelas.xlsx",
        "backend/template/template_sommier.xlsx",
    ]
    
    for template in templates_critiques:
        if os.path.exists(template):
            size_kb = os.path.getsize(template) / 1024
            print(f"   ✅ {template} ({size_kb:.1f} KB)")
        else:
            print(f"   ❌ {template} (manquant)")
    
    print()
    
    # Vérifier les configurations
    print("📋 Vérification des configurations:")
    configs_critiques = [
        "config/mappings_matelas.json",
        "config/mappings_sommiers.json",
    ]
    
    for config in configs_critiques:
        if os.path.exists(config):
            try:
                with open(config, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"   ✅ {config} (valide, {len(data)} entrées)")
            except Exception as e:
                print(f"   ❌ {config} (erreur: {e})")
        else:
            print(f"   ❌ {config} (manquant)")
    
    print()
    
    # Vérifier les assets
    print("📋 Vérification des assets:")
    assets_critiques = [
        "assets/lit-double.png",
        "assets/logo_westelynck.png",
        "assets/lit-double.ico",
    ]
    
    for asset in assets_critiques:
        if os.path.exists(asset):
            size_kb = os.path.getsize(asset) / 1024
            print(f"   ✅ {asset} ({size_kb:.1f} KB)")
        else:
            print(f"   ❌ {asset} (manquant)")
    
    print()
    
    # Résumé
    print("📊 RÉSUMÉ:")
    print(f"   Référentiels critiques: {len(referentiels_critiques) - len(missing_critical)}/{len(referentiels_critiques)} présents")
    print(f"   Templates: {len([t for t in templates_critiques if os.path.exists(t)])}/{len(templates_critiques)} présents")
    print(f"   Configurations: {len([c for c in configs_critiques if os.path.exists(c)])}/{len(configs_critiques)} présentes")
    print(f"   Assets: {len([a for a in assets_critiques if os.path.exists(a)])}/{len(assets_critiques)} présents")
    
    if missing_critical:
        print(f"\n⚠️ ATTENTION: {len(missing_critical)} référentiels critiques manquent!")
        print("   L'application peut ne pas fonctionner correctement.")
        return False
    else:
        print(f"\n✅ Tous les fichiers critiques sont présents!")
        print("   L'application devrait fonctionner correctement.")
        return True


if __name__ == "__main__":
    success = test_referentiels_inclus()
    sys.exit(0 if success else 1) 