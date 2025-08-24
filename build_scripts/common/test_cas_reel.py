#!/usr/bin/env python3

# Test avec le cas réel du JSON fourni

# Configuration du matelas de l'exemple
config_reel = {
    "matelas_index": 1,
    "noyau": "LATEX NATUREL",
    "quantite": 2,
    "hauteur": 10,
    "fermete": "FERME",
    "housse": "MATELASSEE",
    "matiere_housse": "TENCEL LUXE 3D",  # C'est cette matière qui pose problème
    "poignees": "OUI",
    "dimensions": {
        "largeur": 79,
        "longueur": 198
    },
    "semaine_annee": "12_2025",
    "lundi": "2025-03-24",
    "vendredi": "2025-03-28",
    "commande_client": "12"
}

print("=== TEST CAS RÉEL ===")
print(f"Noyau: {config_reel['noyau']}")
print(f"Matière housse: {config_reel['matiere_housse']}")
print(f"Dimensions: {config_reel['dimensions']}")

# Test LATEX NATUREL avec TENCEL LUXE 3D
try:
    from backend.latex_naturel_longueur_housse_utils import get_latex_naturel_longueur_housse_value
    
    dimension_housse_longueur = get_latex_naturel_longueur_housse_value(
        config_reel["dimensions"]["longueur"], 
        config_reel["matiere_housse"]
    )
    
    print(f"Longueur housse calculée: {dimension_housse_longueur}")
    
    if dimension_housse_longueur is not None:
        config_reel["dimension_housse_longueur"] = dimension_housse_longueur
        print(f"✅ Longueur housse ajoutée au config: {config_reel['dimension_housse_longueur']}")
        print(f"✅ Configuration finale: {config_reel}")
    else:
        print("❌ Longueur housse non trouvée")
        
except Exception as e:
    print(f"❌ Erreur: {e}")

print("\n" + "="*50 + "\n")

# Test avec différentes matières pour vérifier le mapping
print("=== TEST MAPPING MATIÈRES ===")
matieres_test = ["TENCEL LUXE 3D", "LUXE 3D", "TENCEL", "POLYESTER"]
longueur_test = 198

for matiere in matieres_test:
    try:
        valeur = get_latex_naturel_longueur_housse_value(longueur_test, matiere)
        print(f"LATEX NATUREL - {matiere}: {valeur}")
    except Exception as e:
        print(f"❌ Erreur pour {matiere}: {e}")

print("\n✅ Test terminé !") 