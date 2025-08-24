#!/usr/bin/env python3

# Test des longueurs housse pour SELECT 43 et LATEX RENFORCÉ

# Configuration de test
config_test = {
    "matelas_index": 1,
    "noyau": "SELECT 43",
    "quantite": 1,
    "hauteur": 20,
    "fermete": "MOYENNE",
    "housse": "ZIPPÉE",
    "matiere_housse": "LUXE_3D",
    "poignees": "2 POIGNÉES",
    "dimensions": {"largeur": 160, "longueur": 200},
    "semaine_annee": "1_2024",
    "lundi": "2024-01-01",
    "vendredi": "2024-01-05",
    "commande_client": "TEST"
}

# Test SELECT 43
print("=== TEST SELECT 43 ===")
print(f"Configuration: {config_test}")
print(f"Dimensions: {config_test['dimensions']}")
print(f"Matière housse: {config_test['matiere_housse']}")

try:
    from backend.select43_longueur_housse_utils import get_select43_longueur_housse_value
    dimension_housse_longueur = get_select43_longueur_housse_value(
        config_test["dimensions"]["longueur"], 
        config_test["matiere_housse"]
    )
    print(f"Longueur housse SELECT 43: {dimension_housse_longueur}")
    
    if dimension_housse_longueur is not None:
        config_test["dimension_housse_longueur"] = dimension_housse_longueur
        print(f"✅ Longueur housse ajoutée au config: {config_test['dimension_housse_longueur']}")
    else:
        print("❌ Longueur housse non trouvée")
except Exception as e:
    print(f"❌ Erreur SELECT 43: {e}")

print("\n" + "="*50 + "\n")

# Test LATEX RENFORCÉ
config_test2 = {
    "matelas_index": 2,
    "noyau": "LATEX RENFORCE",
    "quantite": 1,
    "hauteur": 20,
    "fermete": "MOYENNE",
    "housse": "ZIPPÉE",
    "matiere_housse": "TENCEL",
    "poignees": "2 POIGNÉES",
    "dimensions": {"largeur": 160, "longueur": 200},
    "semaine_annee": "1_2024",
    "lundi": "2024-01-01",
    "vendredi": "2024-01-05",
    "commande_client": "TEST"
}

print("=== TEST LATEX RENFORCÉ ===")
print(f"Configuration: {config_test2}")
print(f"Dimensions: {config_test2['dimensions']}")
print(f"Matière housse: {config_test2['matiere_housse']}")

try:
    from backend.latex_renforce_longueur_utils import get_latex_renforce_longueur_housse
    dimension_housse_longueur = get_latex_renforce_longueur_housse(
        config_test2["dimensions"]["longueur"], 
        config_test2["matiere_housse"]
    )
    print(f"Longueur housse LATEX RENFORCÉ: {dimension_housse_longueur}")
    
    if dimension_housse_longueur is not None:
        config_test2["dimension_housse_longueur"] = dimension_housse_longueur
        print(f"✅ Longueur housse ajoutée au config: {config_test2['dimension_housse_longueur']}")
    else:
        print("❌ Longueur housse non trouvée")
except Exception as e:
    print(f"❌ Erreur LATEX RENFORCÉ: {e}")

print("\n" + "="*50 + "\n")

# Test avec différentes matières
print("=== TEST DIFFÉRENTES MATIÈRES ===")
matieres = ["LUXE_3D", "TENCEL", "POLYESTER"]
longueur_test = 200

for matiere in matieres:
    try:
        # Test SELECT 43
        valeur_select43 = get_select43_longueur_housse_value(longueur_test, matiere)
        print(f"SELECT 43 - {matiere}: {valeur_select43}")
        
        # Test LATEX RENFORCÉ
        valeur_latex = get_latex_renforce_longueur_housse(longueur_test, matiere)
        print(f"LATEX RENFORCÉ - {matiere}: {valeur_latex}")
        print("-" * 30)
    except Exception as e:
        print(f"❌ Erreur pour {matiere}: {e}")

print("\n✅ Tests terminés !") 