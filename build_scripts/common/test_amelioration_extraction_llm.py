#!/usr/bin/env python3
"""
Test d'amélioration de l'extraction LLM pour corriger le problème de description tronquée
"""

import sys
sys.path.append('backend')

# Texte extrait réel avec description complète
texte_extrait = """SAS Literie Westelynck au Capital de 23 100 Euros - 525 RD 642 - 59190 BORRE
Tèl. 03.28.48.04.19 - Fax 03.28.41.02.74 - contact@lwest.fr
Siret 429 352 891 00015 - APE 3103Z - CEE FR50 429 352 891
Domiciliation Bancaire : Crédit Agricole d'Hazebrouck FR76 1670 6050 1650 4613 2602 341
1/1
Maison
Fondée en 
1899
Me BERKEIN EDWIGE
575 ROUTE D'HERZEELE
59670 WINNEZEELE
Numéro
Date
Code client
Mode de règlement
CM00009547
07/07/2025
BERKEDWIN
CB
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
LITERIE 160/ 200
0,00
0,00
0,00
0,00
0,00
894,00
894,00
1,00
MATELAS 1 PIÈCE - MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES FERME
(50KG/ M3) - HOUSSE MATELASSÉE TENCEL LUXE 3D AVEC POIGNÉES INTÉGRÉES 
DÉHOUSSABLE SUR 3 CÔTÉS ET LAVABLE A 40°  159/ 198/ 20
Dont Eco-Part. M obilier (TTC) : 15,00€ sur P.U : 879,00€
0,00
-43,95
-43,95
1,00
REMISE : 5% ENLÈVEMENT PAR VOS SOINS
0,00
0,00
0,00
0,00
0,00
0,00
0,00
1,00
PRIX NETS TTC 2023 + ECOTAXES
ACOMPTE DE 250.05 € A LA COMMANDE ET SOLDE DE 600 € A L'ENLÈVEMENT
0,00
0,00
0,00
0,00
DÉLAI :  AVANT CONGÉS SI POSSIBLE SINON APRÈS 15 AOÛT
Taux
Base HT
Montant TVA
139,18
695,87
20,00
Port HT
Total TTC
Acomptes
Net à payer
0,00
850,05
250,05
600,00 €"""

# Résultat LLM actuel (problématique)
llm_result_actuel = """{
  "articles": [
    {
      "quantite": 1,
      "description": "MATELAS 1 PIÈCE - MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES FERME",
      "dimensions": "159/ 198/ 20",
      "pu_ttc": 894.00,
      "eco_part": 15.00,
      "pu_ht": 879.00
    }
  ]
}"""

# Résultat LLM amélioré (solution)
llm_result_ameliore = """{
  "articles": [
    {
      "quantite": 1,
      "description": "MATELAS 1 PIÈCE - MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES FERME (50KG/ M3) - HOUSSE MATELASSÉE TENCEL LUXE 3D AVEC POIGNÉES INTÉGRÉES DÉHOUSSABLE SUR 3 CÔTÉS ET LAVABLE A 40°",
      "dimensions": "159/ 198/ 20",
      "pu_ttc": 894.00,
      "eco_part": 15.00,
      "pu_ht": 879.00
    }
  ]
}"""

def test_extraction_actuelle():
    """Test avec l'extraction LLM actuelle (problématique)"""
    print("🔍 TEST EXTRACTION ACTUELLE (PROBLÉMATIQUE)")
    print("=" * 60)
    
    import json
    llm_data = json.loads(llm_result_actuel)
    
    for article in llm_data["articles"]:
        description = article["description"]
        print(f"Description extraite: {description}")
        print(f"Longueur: {len(description)} caractères")
        
        # Test des détections
        from matiere_housse_utils import detecter_matiere_housse
        from housse_utils import detecter_type_housse
        from fermete_utils import detecter_fermete_matelas
        
        matiere = detecter_matiere_housse(description)
        type_housse = detecter_type_housse(description)
        fermete = detecter_fermete_matelas(description)
        
        print(f"Matière housse: {matiere}")
        print(f"Type housse: {type_housse}")
        print(f"Fermeté: {fermete}")
        print()

def test_extraction_amelioree():
    """Test avec l'extraction LLM améliorée (solution)"""
    print("✅ TEST EXTRACTION AMÉLIORÉE (SOLUTION)")
    print("=" * 60)
    
    import json
    llm_data = json.loads(llm_result_ameliore)
    
    for article in llm_data["articles"]:
        description = article["description"]
        print(f"Description extraite: {description}")
        print(f"Longueur: {len(description)} caractères")
        
        # Test des détections
        from matiere_housse_utils import detecter_matiere_housse
        from housse_utils import detecter_type_housse
        from fermete_utils import detecter_fermete_matelas
        
        matiere = detecter_matiere_housse(description)
        type_housse = detecter_type_housse(description)
        fermete = detecter_fermete_matelas(description)
        
        print(f"Matière housse: {matiere}")
        print(f"Type housse: {type_housse}")
        print(f"Fermeté: {fermete}")
        print()

def test_calculs_dimensions():
    """Test des calculs de dimensions avec les deux extractions"""
    print("📏 TEST CALCULS DIMENSIONS")
    print("=" * 60)
    
    import json
    
    # Test avec extraction actuelle
    print("🔍 AVEC EXTRACTION ACTUELLE:")
    llm_data_actuel = json.loads(llm_result_actuel)
    article_actuel = llm_data_actuel["articles"][0]
    
    from mousse_rainuree7zones_referentiel import get_valeur_mousse_rainuree7zones
    from mousse_rainuree7zones_longueur_housse_utils import get_mousse_rainuree7zones_longueur_housse_value
    from matiere_housse_utils import detecter_matiere_housse
    
    matiere_actuel = detecter_matiere_housse(article_actuel["description"])
    print(f"  Matière détectée: {matiere_actuel}")
    
    try:
        dim_housse_actuel = get_valeur_mousse_rainuree7zones(159, matiere_actuel)
        print(f"  Dimension housse: {dim_housse_actuel}")
    except Exception as e:
        print(f"  ❌ Erreur dimension housse: {e}")
    
    try:
        longueur_actuel = get_mousse_rainuree7zones_longueur_housse_value(198, matiere_actuel)
        print(f"  Longueur housse: {longueur_actuel}")
    except Exception as e:
        print(f"  ❌ Erreur longueur housse: {e}")
    
    print()
    
    # Test avec extraction améliorée
    print("✅ AVEC EXTRACTION AMÉLIORÉE:")
    llm_data_ameliore = json.loads(llm_result_ameliore)
    article_ameliore = llm_data_ameliore["articles"][0]
    
    matiere_ameliore = detecter_matiere_housse(article_ameliore["description"])
    print(f"  Matière détectée: {matiere_ameliore}")
    
    try:
        dim_housse_ameliore = get_valeur_mousse_rainuree7zones(159, matiere_ameliore)
        print(f"  Dimension housse: {dim_housse_ameliore}")
    except Exception as e:
        print(f"  ❌ Erreur dimension housse: {e}")
    
    try:
        longueur_ameliore = get_mousse_rainuree7zones_longueur_housse_value(198, matiere_ameliore)
        print(f"  Longueur housse: {longueur_ameliore}")
    except Exception as e:
        print(f"  ❌ Erreur longueur housse: {e}")

def proposer_ameliorations():
    """Propose des améliorations pour le prompt LLM"""
    print("💡 PROPOSITIONS D'AMÉLIORATIONS")
    print("=" * 60)
    
    print("1. 🔧 MODIFICATION DU PROMPT LLM")
    print("   - Ajouter une instruction explicite pour extraire TOUTE la description")
    print("   - Spécifier de ne pas tronquer les descriptions de matelas")
    print("   - Demander d'inclure les informations sur la housse")
    print()
    
    print("2. 🔄 FALLBACK VERS TEXTE EXTRUIT")
    print("   - Si le LLM ne fournit pas assez d'informations sur la housse")
    print("   - Utiliser le texte extrait pour compléter la description")
    print("   - Rechercher les informations manquantes dans le texte original")
    print()
    
    print("3. 🎯 DÉTECTION INTELLIGENTE")
    print("   - Détecter automatiquement si la description est complète")
    print("   - Compléter avec des informations par défaut si nécessaire")
    print("   - Afficher des alertes quand des informations sont manquantes")
    print()
    
    print("4. 📝 PROMPT AMÉLIORÉ SUGGÉRÉ:")
    print("""
    IMPORTANT : Pour chaque matelas, tu dois extraire la description COMPLÈTE 
    incluant TOUTES les informations sur :
    - Le type de noyau (MOUSSE RAINURÉE, LATEX, etc.)
    - La fermeté (FERME, MEDIUM, CONFORT)
    - Le type de housse (MATELASSÉE, SIMPLE, etc.)
    - La matière de la housse (TENCEL LUXE 3D, TENCEL, POLYESTER, etc.)
    - Les poignées (AVEC POIGNÉES, SANS POIGNÉES, etc.)
    - Les caractéristiques spéciales (DÉHOUSSABLE, LAVABLE, etc.)
    
    NE TRONQUE JAMAIS la description d'un matelas !
    """)

if __name__ == "__main__":
    test_extraction_actuelle()
    print()
    test_extraction_amelioree()
    print()
    test_calculs_dimensions()
    print()
    proposer_ameliorations() 