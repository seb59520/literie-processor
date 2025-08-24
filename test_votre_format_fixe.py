#!/usr/bin/env python3
"""
Test du format 139x189x20 maintenant supporté
"""

import sys
sys.path.append('backend')

from dimensions_utils import detecter_dimensions

def test_format_fixe():
    """Test du format exact de votre description"""
    
    print("=== TEST DU FORMAT 139x189x20 ===")
    
    # Votre description exacte du test LLM
    description_llm = "MATELAS 1 PIÈCE - MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES FERME (50KG/ M3) - HOUSSE MATELASSÉE TENCEL LUXE 3D AVEC POIGNÉES INTÉGRÉES DÉHOUSSABLE SUR 3 CÔTÉS ET LAVABLE A 40°  139/ 189/ 20"
    
    # Le format extrait par le LLM
    format_llm = "139x189x20"
    
    print(f"📝 Description complète: {description_llm}")
    print(f"📏 Format extrait par LLM: {format_llm}")
    
    # Test 1: Format avec x (nouveau support)
    print(f"\n🔍 Test 1: Format avec 'x' ({format_llm})")
    dimensions_x = detecter_dimensions(format_llm)
    
    if dimensions_x:
        print(f"   ✅ SUCCÈS: Dimensions détectées: {dimensions_x}")
        print(f"   📏 Largeur: {dimensions_x['largeur']} cm")
        print(f"   📏 Longueur: {dimensions_x['longueur']} cm")
        print(f"   📏 Hauteur: {dimensions_x['hauteur']} cm")
        
        # Calcul des dimensions arrondies
        largeur_arrondie = int(round(dimensions_x['largeur'] / 10.0) * 10)
        longueur_arrondie = int(round(dimensions_x['longueur'] / 10.0) * 10)
        
        print(f"   📐 Dimensions arrondies: {largeur_arrondie} x {longueur_arrondie}")
        print(f"   📊 Format Excel: {largeur_arrondie} x {longueur_arrondie}")
        
    else:
        print(f"   ❌ ÉCHEC: Aucune dimension détectée dans '{format_llm}'")
        return False
    
    # Test 2: Format avec / (ancien support)
    print(f"\n🔍 Test 2: Format avec '/' (139/ 189/ 20)")
    format_slash = "139/ 189/ 20"
    dimensions_slash = detecter_dimensions(format_slash)
    
    if dimensions_slash:
        print(f"   ✅ SUCCÈS: Dimensions détectées: {dimensions_slash}")
        print(f"   📏 Largeur: {dimensions_slash['largeur']} cm")
        print(f"   📏 Longueur: {dimensions_slash['longueur']} cm")
        print(f"   📏 Hauteur: {dimensions_slash['hauteur']} cm")
    else:
        print(f"   ❌ ÉCHEC: Aucune dimension détectée dans '{format_slash}'")
    
    # Test 3: Recherche dans la description complète
    print(f"\n🔍 Test 3: Recherche dans la description complète")
    dimensions_desc = detecter_dimensions(description_llm)
    
    if dimensions_desc:
        print(f"   ✅ SUCCÈS: Dimensions trouvées dans la description: {dimensions_desc}")
    else:
        print(f"   ❌ ÉCHEC: Aucune dimension trouvée dans la description complète")
    
    # Résumé
    print(f"\n🎯 RÉSUMÉ DU TEST:")
    print(f"   ✅ Format 'x' (139x189x20): {'SUPPORTÉ' if dimensions_x else 'NON SUPPORTÉ'}")
    print(f"   ✅ Format '/' (139/ 189/ 20): {'SUPPORTÉ' if dimensions_slash else 'NON SUPPORTÉ'}")
    print(f"   ✅ Description complète: {'SUPPORTÉ' if dimensions_desc else 'NON SUPPORTÉ'}")
    
    if dimensions_x:
        print(f"\n🚀 PROBLÈME RÉSOLU !")
        print(f"   - Le format '139x189x20' est maintenant reconnu")
        print(f"   - Les dimensions seront extraites: 139 x 189 x 20")
        print(f"   - L'Excel sera généré avec: 140 x 190")
        print(f"\n🔧 PROCHAINE ÉTAPE:")
        print(f"   - Relancer l'application")
        print(f"   - Traiter votre PDF avec l'option LLM activée")
        print(f"   - Les dimensions devraient maintenant apparaître dans l'Excel")
        return True
    else:
        print(f"\n❌ PROBLÈME PERSISTANT")
        print(f"   - Le format '139x189x20' n'est toujours pas reconnu")
        print(f"   - Vérifier la modification de dimensions_utils.py")
        return False

if __name__ == "__main__":
    success = test_format_fixe()
    
    if success:
        print("\n🎉 SUCCÈS: Le format 139x189x20 est maintenant supporté !")
    else:
        print("\n❌ ÉCHEC: Le problème persiste")
    
    print("\n=== FIN DU TEST ===")

