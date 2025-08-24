#!/usr/bin/env python3
"""
Test complet pour démontrer toutes les informations traitées pour un matelas RAINUREE
"""

import sys
import os
sys.path.append('backend')

from backend_interface import BackendInterface
from backend.matelas_utils import detecter_noyau_matelas
from backend.matiere_housse_utils import detecter_matiere_housse
from backend.dimensions_utils import detecter_dimensions
from backend.hauteur_utils import calculer_hauteur_matelas
from backend.fermete_utils import detecter_fermete_matelas
from backend.housse_utils import detecter_type_housse
from backend.poignees_utils import detecter_poignees
from backend.mousse_rainuree7zones_referentiel import get_valeur_mousse_rainuree7zones
from backend.mousse_rainuree7zones_longueur_housse_utils import get_mousse_rainuree7zones_longueur_housse_value
from backend.decoupe_noyau_utils import calcul_decoupe_noyau

def test_complet_rainuree():
    """Test complet de toutes les informations traitées pour un matelas RAINUREE"""
    
    print("🧪 TEST COMPLET - MATELAS RAINUREE")
    print("=" * 60)
    
    # Description de test réaliste
    description = "MATELAS 1 PIÈCE - MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES FERME (50KG/ M3) - HOUSSE MATELASSÉE TENCEL LUXE 3D AVEC POIGNÉES INTÉGRÉES LAVABLE A 40°"
    dimensions_str = "89/198/20"
    
    print(f"📝 Description: {description}")
    print(f"📏 Dimensions: {dimensions_str}")
    print()
    
    # 1. DÉTECTION DU NOYAU
    print("🔍 1. DÉTECTION DU NOYAU")
    print("-" * 30)
    articles = [{"description": description}]
    noyaux = detecter_noyau_matelas(articles)
    noyau = noyaux[0]["noyau"] if noyaux else "INCONNU"
    print(f"✅ Noyau détecté: {noyau}")
    print()
    
    # 2. DÉTECTION DE LA MATIÈRE HOUSSE
    print("🛏️ 2. DÉTECTION DE LA MATIÈRE HOUSSE")
    print("-" * 40)
    matiere_housse = detecter_matiere_housse(description)
    print(f"✅ Matière housse: {matiere_housse}")
    print()
    
    # 3. DÉTECTION DES DIMENSIONS
    print("📏 3. DÉTECTION DES DIMENSIONS")
    print("-" * 30)
    dimensions = detecter_dimensions(dimensions_str)
    print(f"✅ Dimensions: {dimensions}")
    print()
    
    # 4. CALCUL DE LA HAUTEUR
    print("📐 4. CALCUL DE LA HAUTEUR")
    print("-" * 25)
    hauteur = calculer_hauteur_matelas(noyau)
    print(f"✅ Hauteur calculée: {hauteur} cm")
    print()
    
    # 5. DÉTECTION DE LA FERMETÉ
    print("💪 5. DÉTECTION DE LA FERMETÉ")
    print("-" * 30)
    fermete = detecter_fermete_matelas(description)
    print(f"✅ Fermeté détectée: {fermete}")
    print()
    
    # 6. DÉTECTION DU TYPE DE HOUSSE
    print("🛏️ 6. DÉTECTION DU TYPE DE HOUSSE")
    print("-" * 35)
    type_housse = detecter_type_housse(description)
    print(f"✅ Type housse: {type_housse}")
    print()
    
    # 7. DÉTECTION DES POIGNÉES (AVEC RÈGLE SPÉCIALE)
    print("🔧 7. DÉTECTION DES POIGNÉES (AVEC RÈGLE SPÉCIALE)")
    print("-" * 50)
    poignees_normales = detecter_poignees(description)
    print(f"   Poignées détectées normalement: {poignees_normales}")
    
    # Règle spéciale TENCEL LUXE 3D
    if matiere_housse == "TENCEL LUXE 3D":
        poignees_finales = "NON"
        print(f"   ⚠️  Règle spéciale TENCEL LUXE 3D appliquée")
    else:
        poignees_finales = poignees_normales
    print(f"✅ Poignées finales: {poignees_finales}")
    print()
    
    # 8. CALCUL DES DIMENSIONS HOUSSE
    print("📐 8. CALCUL DES DIMENSIONS HOUSSE")
    print("-" * 35)
    try:
        dimension_housse = get_valeur_mousse_rainuree7zones(dimensions["largeur"], matiere_housse)
        print(f"✅ Dimension housse (largeur): {dimension_housse}")
        
        # Formatage selon la matière
        if matiere_housse == "POLYESTER":
            dimension_housse_formatee = f"{dimension_housse}"
        else:
            quantite = 1  # Pour le test
            prefixe = "2 x " if quantite == 1 else f"{quantite * 2} x "
            dimension_housse_formatee = f"{prefixe}{dimension_housse}"
        print(f"✅ Dimension housse formatée: {dimension_housse_formatee}")
    except Exception as e:
        print(f"❌ Erreur calcul dimension housse: {e}")
    print()
    
    # 9. CALCUL DE LA LONGUEUR HOUSSE
    print("📏 9. CALCUL DE LA LONGUEUR HOUSSE")
    print("-" * 35)
    try:
        longueur_housse = get_mousse_rainuree7zones_longueur_housse_value(dimensions["longueur"], matiere_housse)
        print(f"✅ Longueur housse: {longueur_housse}")
    except Exception as e:
        print(f"❌ Erreur calcul longueur housse: {e}")
    print()
    
    # 10. CALCUL DE LA DÉCOUPE NOYAU
    print("✂️ 10. CALCUL DE LA DÉCOUPE NOYAU")
    print("-" * 30)
    try:
        decoupe_largeur, decoupe_longueur = calcul_decoupe_noyau(noyau, fermete, dimensions["largeur"], dimensions["longueur"])
        decoupe = f"{decoupe_largeur} x {decoupe_longueur}"
        print(f"✅ Découpe noyau: {decoupe}")
    except Exception as e:
        print(f"❌ Erreur calcul découpe: {e}")
    print()
    
    # 11. SIMULATION CONFIGURATION COMPLÈTE
    print("⚙️ 11. CONFIGURATION COMPLÈTE")
    print("-" * 30)
    config = {
        "matelas_index": 1,
        "noyau": noyau,
        "quantite": 1,
        "hauteur": hauteur,
        "fermete": fermete,
        "housse": type_housse,
        "matiere_housse": matiere_housse,
        "poignees": poignees_finales,
        "dimensions": dimensions,
        "semaine_annee": "12_2025",
        "lundi": "2025-03-24",
        "vendredi": "2025-03-28",
        "commande_client": "TEST001",
        "dimension_housse": dimension_housse_formatee if 'dimension_housse_formatee' in locals() else "N/A",
        "dimension_housse_longueur": longueur_housse if 'longueur_housse' in locals() else "N/A",
        "decoupe_noyau": decoupe if 'decoupe' in locals() else "N/A"
    }
    
    print("📊 Configuration JSON générée:")
    for key, value in config.items():
        print(f"   {key}: {value}")
    print()
    
    # 12. SIMULATION PRÉ-IMPORT EXCEL
    print("📋 12. CHAMPS PRÉ-IMPORT EXCEL")
    print("-" * 35)
    pre_import_fields = {
        "Client_D1": "Mr TEST CLIENT",
        "Adresse_D3": "Adresse Test",
        "numero_D2": "TEST001",
        "semaine_D5": "12_2025",
        "lundi_D6": "2025-03-24",
        "vendredi_D7": "2025-03-28",
        "Hauteur_D22": hauteur,
        "dimension_housse_D23": config.get("dimension_housse", "N/A"),
        "longueur_D24": config.get("dimension_housse_longueur", "N/A"),
        "decoupe_noyau_D25": config.get("decoupe_noyau", "N/A"),
        "poignees_C20": poignees_finales,
        "MR_Ferme_C37": "X" if fermete == "FERME" else "",
        "MR_Medium_C38": "X" if fermete == "MEDIUM" else "",
        "MR_Confort_C39": "X" if fermete == "CONFORT" else "",
        "Hmat_luxe3D_C19": "X" if matiere_housse == "TENCEL LUXE 3D" else "",
        "Hmat_luxe3D_D19": config.get("dimension_housse", "") if matiere_housse == "TENCEL LUXE 3D" else ""
    }
    
    print("📊 Champs Excel générés:")
    for field, value in pre_import_fields.items():
        if value:  # Afficher seulement les champs avec valeur
            print(f"   {field}: {value}")
    print()
    
    # 13. RÈGLES SPÉCIALES APPLIQUÉES
    print("⚠️ 13. RÈGLES SPÉCIALES APPLIQUÉES")
    print("-" * 35)
    regles_appliquees = []
    
    if matiere_housse == "TENCEL LUXE 3D":
        regles_appliquees.append("✅ Poignées forcées à 'NON' (règle TENCEL LUXE 3D)")
        regles_appliquees.append("✅ Case D19 garde sa couleur (TENCEL LUXE 3D détecté)")
    else:
        regles_appliquees.append("✅ Case D19 décolorée (TENCEL LUXE 3D non détecté)")
    
    if fermete == "FERME":
        regles_appliquees.append("✅ Découpe noyau: -1cm largeur, -0.5cm longueur")
    elif fermete == "MEDIUM":
        regles_appliquees.append("✅ Découpe noyau: 0cm largeur, -1cm longueur")
    elif fermete == "CONFORT":
        regles_appliquees.append("✅ Découpe noyau: 0cm largeur, -2cm longueur")
    
    for regle in regles_appliquees:
        print(f"   {regle}")
    print()
    
    # 14. RÉFÉRENTIELS CONSULTÉS
    print("📚 14. RÉFÉRENTIELS CONSULTÉS")
    print("-" * 30)
    referentiels = [
        "mousse_rainuree7zones_tencel_luxe3d_tencel_polyester.json",
        "mousse_rainuree7zones_longueur_housse.json",
        "dimensions_matelas.json",
        "regles_matelas.csv"
    ]
    
    for ref in referentiels:
        print(f"   📄 {ref}")
    print()
    
    # 15. RÉSUMÉ FINAL
    print("📈 15. RÉSUMÉ FINAL")
    print("-" * 20)
    total_champs = len([v for v in pre_import_fields.values() if v])
    print(f"✅ Total champs traités: {total_champs}")
    print(f"✅ Noyau: {noyau}")
    print(f"✅ Matière housse: {matiere_housse}")
    print(f"✅ Dimensions: {dimensions['largeur']}x{dimensions['longueur']}x{dimensions['hauteur']}")
    print(f"✅ Hauteur: {hauteur} cm")
    print(f"✅ Fermeté: {fermete}")
    print(f"✅ Poignées: {poignees_finales}")
    print(f"✅ Type housse: {type_housse}")
    
    print("\n🎉 Test complet terminé avec succès !")
    print("=" * 60)

if __name__ == "__main__":
    test_complet_rainuree() 