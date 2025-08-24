#!/usr/bin/env python3

import sys
sys.path.append('backend')
import json

# Texte extrait du PDF (données originales)
texte_extrait = """SAS Literie Westelynck au Capital de 23 100 Euros - 525 RD 642 - 59190 BORRE
Tèl. 03.28.48.04.19 - Fax 03.28.41.02.74 - contact@lwest.fr
Siret 429 352 891 00015 - APE 3103Z - CEE FR50 429 352 891
Domiciliation Bancaire : Crédit Agricole d'Hazebrouck FR76 1670 6050 1650 4613 2602 341
1/2
Maison
Fondée en 
1899
SCI LA BORDERIE
1009 CHEMIN VERT
59670 WINNEZEELE
Numéro
Date
Code client
Mode de règlement
CM00009544
04/07/2025
LABORDWIN
VIREMENT
Date de validité
COMMANDE
Commercial : P. ALINE
www.literie-westelynck.fr
Remise % Montant TTC
P.U. TTC
Qté
Description
0,00
0,00
0,00
0,00
2 ENSEMBLES DE 180/ 200/ 61 CM JUMEAUX SUR PIEDS
0,00
0,00
0,00
0,00
0,00
2 138,15
2 138,15
1,00
SOMMIERS JUMEAUX RELAXATION MOTORISÉE 5 PLIS TÉLESCOPIQUE - 2X2 
MOTEURS RENFORCES (2X6000N) - DOUBLES LATTES ( HÊTRE MULTIPLIS ) -
HÊTRE TEINTÉ WENGÉ NOIR 179/ 199/ 19
Dont Eco-Part. M obilier (TTC) : 13,15€ sur P.U : 2 125,00€
0,00
120,00
120,00
1,00
TÉLÉCOMMANDE NOIRE RADIO FRÉQUENCE (x2) + ÉCLAIRAGE TORCHE
0,00
12,00
12,00
1,00
LOT DE 2 RAMPES 3 PLOTS
0,00
1 733,00
866,50
2,00
MATELAS JUMEAUX - LATEX 100% NATUREL PERFORÉ 7 ZONES DIFFÉRENCIÉES 
FERME - HOUSSE MATELASSÉE TENCEL LUXE 3D LAVABLE A 40°  89/ 198/ 22
Dont Eco-Part. M obilier (TTC) : 5,50€ sur P.U : 861,00€
0,00
185,44
185,44
1,00
JEU DE 8 PIEDS CUBIQUE TEINTÉ WENGÉ 20 CM + PLATINES DE RÉUNION + 
PATINS FEUTRES  (en retrait)
Dont Eco-Part. M obilier (TTC) : 1,44€ sur P.U : 184,00€
0,00
0,00
0,00
0,00
0,00
694,66
694,66
1,00
SOMMIERS JUMEAUX FIXE - DOUBLES LATTES ( HÊTRE MULTIPLIS ) - STRUCTURE 
PAREMENTÉE - LATTES A FLEUR 3 COTES 179/ 199/ 19
Dont Eco-Part. M obilier (TTC) : 9,66€ sur P.U : 685,00€
0,00
195,00
78,00
2,50
MÉTRAGE TISSU CASAL 84015 CANOAS col. 13 COTON
0,00
69,00
69,00
1,00
BUTÉES LATÉRALES & PIEDS FIXE
0,00
1 733,00
866,50
2,00
MATELAS JUMEAUX - LATEX 100% NATUREL PERFORÉ 7 ZONES DIFFÉRENCIÉES 
FERME - HOUSSE MATELASSÉE TENCEL LUXE 3D LAVABLE A 40°  89/ 198/ 22
Dont Eco-Part. M obilier (TTC) : 5,50€ sur P.U : 861,00€
0,00
185,44
185,44
1,00
JEU DE 8 PIEDS CUBIQUE TEINTÉ WENGÉ 20 CM + 2 PLATINES DE RÉUNION + 
PATINS FEUTRES  (en retrait)
Dont Eco-Part. M obilier (TTC) : 1,44€ sur P.U : 184,00€
0,00
0,00
0,00
0,00
0,00
-350,90
-350,90
1,00
REMISE : 5% ENLÈVEMENT PAR VOS SOINS  (emballage renforcé pour déménagement)
0,00
0,00
0,00
0,00
0,00
0,00
0,00
1,00
PRIX NETS TTC 2023 + ECOTAXES
ACOMPTE DE 1 714.79 € A RECEVOIR PAR VIREMENT A LA COMMANDE ET SOLDE 5 
000 € A L'ENLÈVEMENT"""

# JSON LLM (résultat du traitement)
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

def analyser_texte_original():
    """Analyse le texte original pour identifier les articles matelas"""
    print("🔍 ANALYSE DU TEXTE ORIGINAL")
    print("=" * 60)
    
    lignes = texte_extrait.split('\n')
    articles_matelas_texte = []
    
    for i, ligne in enumerate(lignes):
        if "MATELAS" in ligne.upper():
            # Chercher la quantité dans les lignes précédentes
            quantite = 1
            prix_unitaire = 0
            montant_ttc = 0
            
            # Chercher la quantité (ligne précédente ou même ligne)
            for j in range(max(0, i-3), i+1):
                if j < len(lignes):
                    ligne_quantite = lignes[j].strip()
                    # Chercher un nombre suivi de ",00" (format français)
                    if ",00" in ligne_quantite and ligne_quantite.replace(",00", "").replace(" ", "").isdigit():
                        try:
                            quantite = float(ligne_quantite.replace(",00", "").replace(" ", ""))
                            break
                        except:
                            pass
            
            # Chercher le prix unitaire et montant TTC
            for j in range(max(0, i-5), i+1):
                if j < len(lignes):
                    ligne_prix = lignes[j].strip()
                    if "1 733,00" in ligne_prix:
                        prix_unitaire = 866.5
                        montant_ttc = 1733
                        break
            
            article = {
                "ligne_texte": i + 1,
                "description": ligne.strip(),
                "quantite": quantite,
                "prix_unitaire": prix_unitaire,
                "montant_ttc": montant_ttc
            }
            articles_matelas_texte.append(article)
            print(f"  Article matelas trouvé ligne {i+1}:")
            print(f"    Description: {ligne.strip()[:80]}...")
            print(f"    Quantité: {quantite}")
            print(f"    Prix unitaire: {prix_unitaire}")
            print(f"    Montant TTC: {montant_ttc}")
            print()
    
    return articles_matelas_texte

def analyser_llm_result():
    """Analyse le résultat LLM pour identifier les articles matelas"""
    print("🤖 ANALYSE DU RÉSULTAT LLM")
    print("=" * 60)
    
    llm_data = json.loads(llm_result)
    articles_matelas_llm = []
    
    for i, article in enumerate(llm_data["articles"]):
        if "MATELAS" in article["description"].upper():
            article_llm = {
                "index_llm": i + 1,
                "description": article["description"],
                "quantite": article["quantite"],
                "prix_unitaire": article["prix_unitaire"],
                "montant_ttc": article["montant_ttc"]
            }
            articles_matelas_llm.append(article_llm)
            print(f"  Article matelas LLM {i+1}:")
            print(f"    Description: {article['description'][:80]}...")
            print(f"    Quantité: {article['quantite']}")
            print(f"    Prix unitaire: {article['prix_unitaire']}")
            print(f"    Montant TTC: {article['montant_ttc']}")
            print()
    
    return articles_matelas_llm

def comparer_fusion():
    """Compare les articles pour détecter une fusion"""
    print("🔍 DÉTECTION DE FUSION")
    print("=" * 60)
    
    articles_texte = analyser_texte_original()
    articles_llm = analyser_llm_result()
    
    print(f"📊 RÉSUMÉ:")
    print(f"  • Articles matelas dans le texte original: {len(articles_texte)}")
    print(f"  • Articles matelas dans le LLM: {len(articles_llm)}")
    
    if len(articles_texte) > len(articles_llm):
        print(f"\n⚠️  FUSION DÉTECTÉE!")
        print(f"  Le LLM a fusionné {len(articles_texte)} articles en {len(articles_llm)}")
        
        # Analyser les détails
        for i, article_texte in enumerate(articles_texte):
            print(f"\n  Article texte {i+1}:")
            print(f"    Ligne: {article_texte['ligne_texte']}")
            print(f"    Quantité: {article_texte['quantite']}")
            print(f"    Montant TTC: {article_texte['montant_ttc']}")
        
        for i, article_llm in enumerate(articles_llm):
            print(f"\n  Article LLM {i+1}:")
            print(f"    Index: {article_llm['index_llm']}")
            print(f"    Quantité: {article_llm['quantite']}")
            print(f"    Montant TTC: {article_llm['montant_ttc']}")
        
        # Vérifier si les montants correspondent
        total_texte = sum(a['montant_ttc'] for a in articles_texte)
        total_llm = sum(a['montant_ttc'] for a in articles_llm)
        
        print(f"\n💰 VÉRIFICATION MONTANTS:")
        print(f"  • Total texte original: {total_texte}")
        print(f"  • Total LLM: {total_llm}")
        
        if abs(total_texte - total_llm) < 1:
            print(f"  ✅ Les montants correspondent - fusion correcte")
        else:
            print(f"  ❌ Différence de montants - fusion incorrecte")
            
    elif len(articles_texte) == len(articles_llm):
        print(f"\n✅ AUCUNE FUSION DÉTECTÉE")
        print(f"  Le LLM a gardé le même nombre d'articles")
    else:
        print(f"\n❓ ANOMALIE DÉTECTÉE")
        print(f"  Le LLM a plus d'articles que le texte original")

if __name__ == "__main__":
    comparer_fusion() 