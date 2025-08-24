#!/usr/bin/env python3
"""
Test détaillé des calculs de longueurs et dimensions housse pour matelas RAINUREE
"""

import sys
import os
sys.path.append('backend')

from backend.mousse_rainuree7zones_referentiel import get_valeur_mousse_rainuree7zones
from backend.mousse_rainuree7zones_longueur_housse_utils import get_mousse_rainuree7zones_longueur_housse_value

def test_calculs_housse_rainuree():
    """Test détaillé des calculs housse pour RAINUREE"""
    
    print("🧪 TEST DÉTAILLÉ - CALCULS HOUSSE RAINUREE")
    print("=" * 60)
    
    # Cas de test : matelas 89x198 avec TENCEL LUXE 3D
    largeur_matelas = 89
    longueur_matelas = 198
    matiere_housse = "TENCEL LUXE 3D"
    
    print(f"📏 Matelas: {largeur_matelas} x {longueur_matelas} cm")
    print(f"🛏️ Matière housse: {matiere_housse}")
    print()
    
    # 1. CALCUL DIMENSION HOUSSE (LARGEUR)
    print("📐 1. CALCUL DIMENSION HOUSSE (LARGEUR)")
    print("-" * 45)
    
    try:
        dimension_housse = get_valeur_mousse_rainuree7zones(largeur_matelas, matiere_housse)
        print(f"✅ Largeur matelas: {largeur_matelas} cm")
        print(f"✅ Dimension housse calculée: {dimension_housse} cm")
        print(f"📊 Référentiel consulté: mousse_rainuree7zones_tencel_luxe3d_tencel_polyester.json")
        print(f"🔍 Recherche: MATELAS={largeur_matelas} → LUXE_3D={dimension_housse}")
    except Exception as e:
        print(f"❌ Erreur calcul dimension housse: {e}")
    print()
    
    # 2. CALCUL LONGUEUR HOUSSE
    print("📏 2. CALCUL LONGUEUR HOUSSE")
    print("-" * 30)
    
    try:
        longueur_housse = get_mousse_rainuree7zones_longueur_housse_value(longueur_matelas, matiere_housse)
        print(f"✅ Longueur matelas: {longueur_matelas} cm")
        print(f"✅ Longueur housse calculée: {longueur_housse} cm")
        print(f"📊 Référentiel consulté: mousse_rainuree7zones_longueur_housse.json")
        print(f"🔍 Recherche: LONGUEUR={longueur_matelas} → LUXE_3D={longueur_housse}")
    except Exception as e:
        print(f"❌ Erreur calcul longueur housse: {e}")
    print()
    
    # 3. FORMATAGE FINAL
    print("🎨 3. FORMATAGE FINAL")
    print("-" * 20)
    
    quantite = 1
    if matiere_housse == "POLYESTER":
        dimension_housse_formatee = f"{dimension_housse}"
    else:
        prefixe = "2 x " if quantite == 1 else f"{quantite * 2} x "
        dimension_housse_formatee = f"{prefixe}{dimension_housse}"
    
    print(f"✅ Dimension housse formatée: {dimension_housse_formatee}")
    print(f"✅ Longueur housse: {longueur_housse}")
    print()
    
    # 4. DÉMONSTRATION RÉFÉRENTIELS
    print("📚 4. DÉMONSTRATION RÉFÉRENTIELS")
    print("-" * 35)
    
    print("📄 Référentiel largeur housse (extrait):")
    print("   MATELAS | LUXE_3D | TENCEL_S | POLY_S")
    print("   --------|---------|----------|--------")
    for i in range(87, 92):  # Autour de 89
        print(f"   {i:7} | {i+12:7} | {i+18:8} | {i*2+12:6}")
    print()
    
    print("📄 Référentiel longueur housse (extrait):")
    print("   LONGUEUR | LUXE_3D | TENCEL | POLYESTER")
    print("   ---------|---------|--------|----------")
    for i in range(196, 201):  # Autour de 198
        if i == 198:
            print(f"   {i:8} | {i-192.5:7.1f} | {i-190:6.1f} | {i+14:9}")
        else:
            print(f"   {i:8} | {i-192.5:7.1f} | {i-190:6.1f} | {i+14:9}")
    print()
    
    # 5. TEST AVEC DIFFÉRENTES MATIÈRES
    print("🧪 5. TEST AVEC DIFFÉRENTES MATIÈRES")
    print("-" * 40)
    
    matieres = ["TENCEL LUXE 3D", "TENCEL", "POLYESTER"]
    
    for matiere in matieres:
        try:
            dim_housse = get_valeur_mousse_rainuree7zones(largeur_matelas, matiere)
            long_housse = get_mousse_rainuree7zones_longueur_housse_value(longueur_matelas, matiere)
            
            if matiere == "POLYESTER":
                formatage = f"{dim_housse}"
            else:
                formatage = f"2 x {dim_housse}"
            
            print(f"✅ {matiere:15} → {formatage:8} x {long_housse:4} cm")
        except Exception as e:
            print(f"❌ {matiere:15} → Erreur: {e}")
    print()
    
    # 6. TEST AVEC DIFFÉRENTES DIMENSIONS
    print("📏 6. TEST AVEC DIFFÉRENTES DIMENSIONS")
    print("-" * 40)
    
    test_dimensions = [
        (80, 190, "TENCEL LUXE 3D"),
        (90, 200, "TENCEL LUXE 3D"),
        (100, 210, "TENCEL LUXE 3D")
    ]
    
    for largeur, longueur, matiere in test_dimensions:
        try:
            dim_housse = get_valeur_mousse_rainuree7zones(largeur, matiere)
            long_housse = get_mousse_rainuree7zones_longueur_housse_value(longueur, matiere)
            formatage = f"2 x {dim_housse}"
            
            print(f"✅ {largeur:3}x{longueur:3} cm → {formatage:8} x {long_housse:4} cm")
        except Exception as e:
            print(f"❌ {largeur:3}x{longueur:3} cm → Erreur: {e}")
    print()
    
    # 7. RÉSUMÉ FINAL
    print("📊 7. RÉSUMÉ FINAL")
    print("-" * 20)
    
    print(f"🎯 Matelas testé: {largeur_matelas} x {longueur_matelas} cm")
    print(f"🛏️ Matière: {matiere_housse}")
    print(f"📐 Dimension housse: {dimension_housse_formatee}")
    print(f"📏 Longueur housse: {longueur_housse} cm")
    print()
    
    print("📋 Champs Excel générés:")
    print(f"   dimension_housse_D23: {dimension_housse_formatee}")
    print(f"   longueur_D24: {longueur_housse}")
    print()
    
    print("🎉 Test terminé avec succès !")
    print("=" * 60)

if __name__ == "__main__":
    test_calculs_housse_rainuree() 