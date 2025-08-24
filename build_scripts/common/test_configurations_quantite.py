#!/usr/bin/env python3

import sys
sys.path.append('backend')
import json

# JSON LLM fourni par l'utilisateur (avec quantité=2 pour les matelas)
llm_result = """{
  "societe": {
    "nom": "SAS Literie Westelynck",
    "capital": "23 100 Euros",
    "adresse": "525 RD 642 - 59190 BORRE",
    "telephone": "03.28.48.04.19",
    "fax": "03.28.41.02.74",
    "email": "contact@lwest.fr",
    "siret": "429 352 891 00015",
    "APE": "3103Z",
    "CEE": "FR50 429 352 891",
    "banque": "Crédit Agricole d'Hazebrouck",
    "IBAN": "FR76 1670 6050 1650 4613 2602 341"
  },
  "client": {
    "nom": "SCI LA BORDERIE",
    "adresse": "1009 CHEMIN VERT 59670 WINNEZEELE",
    "code_client": "LABORDWIN"
  },
  "commande": {
    "numero": "CM00009544",
    "date": "04/07/2025",
    "mode_reglement": "VIREMENT",
    "commercial": "P. ALINE"
  },
  "articles": [
    {
      "description": "2 ENSEMBLES DE 180/ 200/ 61 CM JUMEAUX SUR PIEDS",
      "quantite": 1,
      "prix_unitaire": 0,
      "montant_ttc": 0
    },
    {
      "description": "SOMMIERS JUMEAUX RELAXATION MOTORISÉE 5 PLIS TÉLESCOPIQUE - 2X2 MOTEURS RENFORCES (2X6000N) - DOUBLES LATTES ( HÊTRE MULTIPLIS ) - HÊTRE TEINTÉ WENGÉ NOIR 179/ 199/ 19",
      "quantite": 1,
      "prix_unitaire": 2138.15,
      "montant_ttc": 2138.15
    },
    {
      "description": "TÉLÉCOMMANDE NOIRE RADIO FRÉQUENCE (x2) + ÉCLAIRAGE TORCHE",
      "quantite": 1,
      "prix_unitaire": 120,
      "montant_ttc": 120
    },
    {
      "description": "LOT DE 2 RAMPES 3 PLOTS",
      "quantite": 1,
      "prix_unitaire": 12,
      "montant_ttc": 12
    },
    {
      "description": "MATELAS JUMEAUX - LATEX 100% NATUREL PERFORÉ 7 ZONES DIFFÉRENCIÉES FERME - HOUSSE MATELASSÉE TENCEL LUXE 3D LAVABLE A 40° 89/ 198/ 22",
      "quantite": 2,
      "prix_unitaire": 866.5,
      "montant_ttc": 1733
    },
    {
      "description": "JEU DE 8 PIEDS CUBIQUE TEINTÉ WENGÉ 20 CM + PLATINES DE RÉUNION + PATINS FEUTRES (en retrait)",
      "quantite": 1,
      "prix_unitaire": 185.44,
      "montant_ttc": 185.44
    },
    {
      "description": "SOMMIERS JUMEAUX FIXE - DOUBLES LATTES ( HÊTRE MULTIPLIS ) - STRUCTURE PAREMENTÉE - LATTES A FLEUR 3 COTES 179/ 199/ 19",
      "quantite": 1,
      "prix_unitaire": 694.66,
      "montant_ttc": 694.66
    },
    {
      "description": "MÉTRAGE TISSU CASAL 84015 CANOAS col. 13 COTON",
      "quantite": 2.5,
      "prix_unitaire": 78,
      "montant_ttc": 195
    },
    {
      "description": "BUTÉES LATÉRALES & PIEDS FIXE",
      "quantite": 1,
      "prix_unitaire": 69,
      "montant_ttc": 69
    },
    {
      "description": "MATELAS JUMEAUX - LATEX 100% NATUREL PERFORÉ 7 ZONES DIFFÉRENCIÉES FERME - HOUSSE MATELASSÉE TENCEL LUXE 3D LAVABLE A 40° 89/ 198/ 22",
      "quantite": 2,
      "prix_unitaire": 866.5,
      "montant_ttc": 1733
    },
    {
      "description": "JEU DE 8 PIEDS CUBIQUE TEINTÉ WENGÉ 20 CM + 2 PLATINES DE RÉUNION + PATINS FEUTRES (en retrait)",
      "quantite": 1,
      "prix_unitaire": 185.44,
      "montant_ttc": 185.44
    },
    {
      "description": "REMISE : 5% ENLÈVEMENT PAR VOS SOINS (emballage renforcé pour déménagement)",
      "quantite": 1,
      "prix_unitaire": -350.9,
      "montant_ttc": -350.9
    }
  ]
}"""

def test_logique_actuelle():
    """Test de la logique actuelle (une configuration par article)"""
    print("🔍 TEST 1: Logique actuelle (une configuration par article)")
    print("=" * 60)
    
    # Simuler la logique actuelle
    configurations = []
    articles_matelas = []
    
    # Filtrer les articles matelas
    for article in json.loads(llm_result)["articles"]:
        desc = article["description"].upper()
        if "MATELAS" in desc:
            articles_matelas.append(article)
    
    print(f"📋 Articles matelas trouvés: {len(articles_matelas)}")
    
    # Logique actuelle : une configuration par article
    for i, article in enumerate(articles_matelas):
        config = {
            "matelas_index": i + 1,
            "noyau": "LATEX NATUREL",
            "quantite": article["quantite"],
            "description": article["description"],
            "dimensions": {"largeur": 89, "longueur": 198, "hauteur": 22}
        }
        configurations.append(config)
        print(f"  Configuration {len(configurations)}: {config['quantite']}x matelas")
    
    print(f"\n✅ Résultat actuel: {len(configurations)} configurations")
    return configurations

def test_logique_modifiee():
    """Test de la logique modifiée (une configuration par unité)"""
    print("\n🔧 TEST 2: Logique modifiée (une configuration par unité)")
    print("=" * 60)
    
    # Simuler la logique modifiée
    configurations = []
    articles_matelas = []
    
    # Filtrer les articles matelas
    for article in json.loads(llm_result)["articles"]:
        desc = article["description"].upper()
        if "MATELAS" in desc:
            articles_matelas.append(article)
    
    print(f"📋 Articles matelas trouvés: {len(articles_matelas)}")
    
    # Logique modifiée : une configuration par unité
    config_index = 1
    for i, article in enumerate(articles_matelas):
        quantite = article["quantite"]
        
        # Créer une configuration pour chaque unité
        for j in range(int(quantite)):
            config = {
                "matelas_index": config_index,
                "noyau": "LATEX NATUREL",
                "quantite": 1,  # Toujours 1 par configuration
                "description": article["description"],
                "dimensions": {"largeur": 89, "longueur": 198, "hauteur": 22}
            }
            configurations.append(config)
            print(f"  Configuration {config_index}: 1x matelas (unité {j+1}/{int(quantite)})")
            config_index += 1
    
    print(f"\n✅ Résultat modifié: {len(configurations)} configurations")
    return configurations

def test_logique_hybride():
    """Test de la logique hybride (garder la quantité mais créer plusieurs configurations)"""
    print("\n🔄 TEST 3: Logique hybride (quantité originale + configurations multiples)")
    print("=" * 60)
    
    # Simuler la logique hybride
    configurations = []
    articles_matelas = []
    
    # Filtrer les articles matelas
    for article in json.loads(llm_result)["articles"]:
        desc = article["description"].upper()
        if "MATELAS" in desc:
            articles_matelas.append(article)
    
    print(f"📋 Articles matelas trouvés: {len(articles_matelas)}")
    
    # Logique hybride : garder la quantité originale mais créer plusieurs configurations
    config_index = 1
    for i, article in enumerate(articles_matelas):
        quantite = article["quantite"]
        
        # Créer une configuration pour chaque unité, mais garder la quantité originale
        for j in range(int(quantite)):
            config = {
                "matelas_index": config_index,
                "noyau": "LATEX NATUREL",
                "quantite": quantite,  # Garder la quantité originale
                "description": article["description"],
                "dimensions": {"largeur": 89, "longueur": 198, "hauteur": 22}
            }
            configurations.append(config)
            print(f"  Configuration {config_index}: {quantite}x matelas (unité {j+1}/{int(quantite)})")
            config_index += 1
    
    print(f"\n✅ Résultat hybride: {len(configurations)} configurations")
    return configurations

def comparer_resultats():
    """Compare les trois approches"""
    print("\n📊 COMPARAISON DES APPROCHES")
    print("=" * 60)
    
    actuel = test_logique_actuelle()
    modifie = test_logique_modifiee()
    hybride = test_logique_hybride()
    
    print(f"\n📈 RÉSUMÉ:")
    print(f"  • Logique actuelle: {len(actuel)} configurations")
    print(f"  • Logique modifiée: {len(modifie)} configurations")
    print(f"  • Logique hybride: {len(hybride)} configurations")
    
    print(f"\n💡 RECOMMANDATION:")
    if len(hybride) > len(actuel):
        print(f"  La logique hybride créerait {len(hybride)} configurations au lieu de {len(actuel)}")
        print(f"  Cela donnerait {len(hybride)} lignes Excel au lieu de {len(actuel)}")
        print(f"  Chaque configuration garde sa quantité originale: {[c['quantite'] for c in hybride]}")
    else:
        print(f"  Aucun changement nécessaire")

if __name__ == "__main__":
    comparer_resultats() 