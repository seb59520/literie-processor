#!/usr/bin/env python3

import json
import sys
sys.path.append('backend')

# Texte extrait du PDF
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
000 € A L'ENLÈVEMENT

SAS Literie Westelynck au Capital de 23 100 Euros - 525 RD 642 - 59190 BORRE
Tèl. 03.28.48.04.19 - Fax 03.28.41.02.74 - contact@lwest.fr
Siret 429 352 891 00015 - APE 3103Z - CEE FR50 429 352 891
Domiciliation Bancaire : Crédit Agricole d'Hazebrouck FR76 1670 6050 1650 4613 2602 341
2/2
Maison
Fondée en 
1899
Remise % Montant TTC
P.U. TTC
Qté
Description
0,00
0,00
0,00
0,00
DÉLAI : DÉBUT SEPTEMBRE AVEC RETRAIT SEMAINE 38
Taux
Base HT
Montant TVA
1 111,20
5 555,90
20,00
Port HT
Total TTC
Acomptes
Net à payer
0,00
6 714,79
0,00
6 714,79 €"""

# Résultat LLM
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
    "date_validite": null,
    "commercial": "P. ALINE",
    "origine": "www.literie-westelynck.fr"
  },
  "articles": [
    {
      "quantite": 1,
      "description": "SOMMIERS JUMEAUX RELAXATION MOTORISÉE 5 PLIS TÉLESCOPIQUE",
      "dimensions": "179/ 199/ 19",
      "pu_ttc": 2138.15,
      "eco_part": 13.15,
      "pu_ht": 2125.00
    },
    {
      "quantite": 1,
      "description": "TÉLÉCOMMANDE NOIRE RADIO FRÉQUENCE (x2) + ÉCLAIRAGE TORCHE",
      "montant": 120.00
    },
    {
      "quantite": 1,
      "description": "LOT DE 2 RAMPES 3 PLOTS",
      "montant": 12.00
    },
    {
      "quantite": 2,
      "description": "MATELAS JUMEAUX - LATEX 100% NATUREL PERFORÉ 7 ZONES DIFFÉRENCIÉES FERME - HOUSSE MATELASSÉE TENCEL LUXE 3D LAVABLE A 40°",
      "dimensions": "89/ 198/ 22",
      "pu_ttc": 1733.00,
      "eco_part": 5.50,
      "pu_ht": 861.00
    },
    {
      "quantite": 1,
      "description": "JEU DE 8 PIEDS CUBIQUE TEINTÉ WENGÉ 20 CM + PLATINES DE RÉUNION + PATINS FEUTRES (en retrait)",
      "dimensions": null,
      "pu_ttc": 185.44,
      "eco_part": 1.44,
      "pu_ht": 184.00
    },
    {
      "quantite": 1,
      "description": "SOMMIERS JUMEAUX FIXE - DOUBLES LATTES ( HÊTRE MULTIPLIS ) - STRUCTURE PAREMENTÉE - LATTES A FLEUR 3 COTES",
      "dimensions": "179/ 199/ 19",
      "pu_ttc": 694.66,
      "eco_part": 9.66,
      "pu_ht": 685.00
    },
    {
      "quantite": 2.5,
      "description": "MÉTRAGE TISSU CASAL 84015 CANOAS col. 13 COTON",
      "montant": 195.00
    },
    {
      "quantite": 1,
      "description": "BUTÉES LATÉRALES & PIEDS FIXE",
      "montant": 69.00
    }
  ],
  "paiement": {
    "conditions": "VIREMENT",
    "port_ht": 0.00,
    "base_ht": 5555.90,
    "taux_tva": 20.00,
    "total_ttc": 6714.79,
    "acompte": 1714.79,
    "net_a_payer": 6714.79
  }
}"""

def analyser_incoherences():
    """Analyse les incohérences entre le texte extrait et le résultat LLM"""
    
    print("=== ANALYSE DES INCOHÉRENCES ===")
    print()
    
    # Parser le JSON LLM
    try:
        llm_data = json.loads(llm_result)
        articles_llm = llm_data.get('articles', [])
    except Exception as e:
        print(f"❌ Erreur parsing JSON LLM: {e}")
        return
    
    print(f"📊 STATISTIQUES:")
    print(f"   - Articles dans le LLM: {len(articles_llm)}")
    print()
    
    # Analyser les articles manquants
    print("🔍 ARTICLES MANQUANTS DANS LE LLM:")
    
    # Articles présents dans le texte mais pas dans le LLM
    articles_manquants = []
    
    # Chercher les articles dans le texte extrait
    lignes = texte_extrait.split('\n')
    for i, ligne in enumerate(lignes):
        if 'MATELAS' in ligne.upper() or 'SOMMIER' in ligne.upper() or 'PIEDS' in ligne.upper() or 'TÉLÉCOMMANDE' in ligne.upper() or 'RAMPES' in ligne.upper() or 'MÉTRAGE' in ligne.upper() or 'BUTÉES' in ligne.upper() or 'REMISE' in ligne.upper():
            # Chercher la quantité et le prix dans les lignes suivantes
            quantite = None
            prix = None
            description = ligne.strip()
            
            # Chercher la quantité dans les lignes précédentes
            for j in range(max(0, i-5), i):
                if lignes[j].strip().replace(',', '').replace(' ', '').isdigit():
                    try:
                        quantite = float(lignes[j].strip().replace(',', '.'))
                        break
                    except:
                        pass
            
            # Chercher le prix dans les lignes suivantes
            for j in range(i+1, min(len(lignes), i+10)):
                if '€' in lignes[j] or (lignes[j].strip().replace(',', '').replace(' ', '').replace('.', '').isdigit() and len(lignes[j].strip()) > 3):
                    try:
                        prix_str = lignes[j].strip().replace('€', '').replace(' ', '').replace(',', '.')
                        prix = float(prix_str)
                        break
                    except:
                        pass
            
            # Vérifier si cet article est dans le LLM
            trouve = False
            for article_llm in articles_llm:
                desc_llm = article_llm.get('description', '').upper()
                if any(mot in desc_llm for mot in description.upper().split()[:3]):
                    trouve = True
                    break
            
            if not trouve and description and len(description) > 10:
                articles_manquants.append({
                    'description': description,
                    'quantite': quantite,
                    'prix': prix,
                    'ligne': i+1
                })
    
    if articles_manquants:
        for article in articles_manquants:
            print(f"   ❌ Ligne {article['ligne']}: {article['description']}")
            if article['quantite']:
                print(f"      Quantité: {article['quantite']}")
            if article['prix']:
                print(f"      Prix: {article['prix']}€")
            print()
    else:
        print("   ✅ Aucun article manquant détecté")
    
    print("🔍 ARTICLES DUPLIQUÉS DANS LE TEXTE:")
    
    # Chercher les articles dupliqués dans le texte
    articles_texte = {}
    for i, ligne in enumerate(lignes):
        if 'MATELAS' in ligne.upper() or 'SOMMIER' in ligne.upper() or 'PIEDS' in ligne.upper():
            description = ligne.strip()
            if description in articles_texte:
                articles_texte[description].append(i+1)
            else:
                articles_texte[description] = [i+1]
    
    dupliques = {desc: lignes for desc, lignes in articles_texte.items() if len(lignes) > 1}
    
    if dupliques:
        for desc, lignes in dupliques.items():
            print(f"   ⚠️  Article dupliqué: {desc}")
            print(f"      Lignes: {lignes}")
            print()
    else:
        print("   ✅ Aucun article dupliqué détecté")
    
    print("🔍 INCOHÉRENCES DE QUANTITÉS:")
    
    # Comparer les quantités
    for article_llm in articles_llm:
        desc_llm = article_llm.get('description', '')
        if not isinstance(desc_llm, str):
            continue
        desc_llm = desc_llm.upper()
        quantite_llm = article_llm.get('quantite', 0)
        
        # Chercher dans le texte
        mots_desc = [str(mot).upper() for mot in desc_llm.split()[:3]]
        for i, ligne in enumerate(lignes):
            ligne_str = str(ligne)
            if any(mot in ligne_str.upper() for mot in mots_desc):
                # Chercher la quantité dans les lignes précédentes
                for j in range(max(0, i-5), i):
                    if str(lignes[j]).strip().replace(',', '').replace(' ', '').isdigit():
                        try:
                            quantite_texte = float(str(lignes[j]).strip().replace(',', '.'))
                            if quantite_texte != quantite_llm:
                                print(f"   ⚠️  Quantité différente pour '{desc_llm[:50]}...'")
                                print(f"      LLM: {quantite_llm}, Texte: {quantite_texte}")
                                print()
                            break
                        except:
                            pass

if __name__ == "__main__":
    analyser_incoherences() 