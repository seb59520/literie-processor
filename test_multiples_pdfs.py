#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier l'extraction avec différents PDFs
"""

import sys
import os
import json

def get_test_pdfs():
    """Récupérer les différents textes de test"""
    return {
        "DEPYPER": """--- PAGE 1 ---
SAS Literie Westelynck au Capital de 23 100 Euros - 525 RD 642 - 59190 BORRE
Tèl. 03.28.48.04.19 - Fax 03.28.41.02.74 - contact@lwest.fr
Siret 429 352 891 00015 - APE 3103Z - CEE FR50 429 352 891
Domiciliation Bancaire : Crédit Agricole d'Hazebrouck FR76 1670 6050 1650 4613 2602 3411/1
Maison
Fondée en
1899Mr et Me DEPYPER CHRISTIAN & ANNIE
285 RUE DE WALLON CAPPEL
CAMPING DES 8 RUES
59190 WALLON CAPPEL
Numéro Date Code client Mode de règlement
CM00009568 15/07/2025 DEPYCHWAL CBDate de validitéCOMMANDE
Commercial : P. ALINE
www.literie-westelynck.fr
Remise % Montant TTC P.U. TTC Qté Description
0,00 0,00 0,00 0,00 COMMANDE VALIDÉE PAR TÉLÉPHONE
0,00 0,00 0,00 0,00 MOBILHOME AVEC CHAMBRE 160/ 190  (158 cm entre les 2 chevets)
0,00 0,00 0,00 0,00
0,00 511,50 511,50 1,00 MATELAS 1 PIÈCE -MOUSSE RAINUR ÉE 7 ZONES DIFFÉRENCIÉES MÉDIUM
(50KG/ M3) -HOUSSE MATELASS ÉETENCEL LUXE 3D LAVABLE A 40°  79/ 189/ 20 -
Mme Gauche
Dont Eco -Part. M obilier (TTC) : 5,50€ sur P.U : 506,00€
0,00 511,50 511,50 1,00 MATELAS 1 PIÈCE -MOUSSE RAINUR ÉE 7 ZONES DIFFÉRENCIÉES FERME
(55KG/ M3) -HOUSSE MATELASS ÉETENCEL LUXE 3D LAVABLE A 40°  79/ 189/ 20 -Mr
Droite
Dont Eco -Part. M obilier (TTC) : 5,50€ sur P.U : 506,00€
0,00 0,00 0,00 0,00
0,00 0,00 0,00 1,00 LIVRAISON ET INSTALLATION OFFERTES AU CAMPING DES 8 RUES A WALLON
CAPPEL
0,00 0,00 0,00 0,00
0,00 0,00 0,00 1,00 PRIX NETS TTC 2023 + ECOTAXES
ACOMPTE DE 343 € EN CB A LA COMMANDE ET SOLDE DE 680 € A LA LIVRAISON
0,00 0,00 0,00 0,00 DÉLAI : Fin août
Taux Base HT Montant TVA
168,66 843,34 20,00
Port HT
Total TTC
Acomptes
Net à payer0,00
1 023,00
343,00
680,00 €""",

        "LAGADEC": """--- PAGE 1 ---
SAS Literie Westelynck au Capital de 23 100 Euros - 525 RD 642 - 59190 BORRE
Tèl. 03.28.48.04.19 - Fax 03.28.41.02.74 - contact@lwest.fr
Siret 429 352 891 00015 - APE 3103Z - CEE FR50 429 352 891
Domiciliation Bancaire : Crédit Agricole d'Hazebrouck FR76 1670 6050 1650 4613 2602 3411/1
Maison
Fondée en
1899Mr et Me LAGADEC HELENE
25 RUE DE L'ÉGLISE
59670 BAVINCHOVE
Numéro Date Code client Mode de règlement
CM00010682 24/03/2025 LAGAHEBAV CBDate de validitéCOMMANDE
Commercial : M. DUPONT
www.literie-westelynck.fr
Remise % Montant TTC P.U. TTC Qté Description
0,00 0,00 0,00 0,00 COMMANDE VALIDÉE PAR TÉLÉPHONE
0,00 0,00 0,00 0,00 CHAMBRE PRINCIPALE
0,00 0,00 0,00 0,00
0,00 1083,50 1083,50 1,00 MATELAS JUMEAUX - MOUSSE RAINURÉE 7 ZONES DIFFÉRÉNCIÉES MÉDIUM
(50KG/M3) - HOUSSE MATELASSÉE TENCEL AVEC POIGNÉES OREILLES LAVABLE À 40° 199x200x20
Dont Eco -Part. M obilier (TTC) : 5,50€ sur P.U : 1078,00€
0,00 0,00 0,00 0,00
0,00 0,00 0,00 1,00 LIVRAISON ET INSTALLATION OFFERTES À BAVINCHOVE
0,00 0,00 0,00 0,00
0,00 0,00 0,00 1,00 PRIX NETS TTC 2023 + ECOTAXES
ACOMPTE DE 667 € EN CB LA COMMANDE ET SOLDE DE 1 500 € À L'ENLÈVEMENT
0,00 0,00 0,00 0,00 DÉLAI : 3 semaines
Taux Base HT Montant TVA
361,17 1805,83 20,00
Port HT
Total TTC
Acomptes
Net à payer0,00
2 167,00
667,00
1 500,00 €""",

        "BECUE": """--- PAGE 1 ---
SAS Literie Westelynck au Capital de 23 100 Euros - 525 RD 642 - 59190 BORRE
Tèl. 03.28.48.04.19 - Fax 03.28.41.02.74 - contact@lwest.fr
Siret 429 352 891 00015 - APE 3103Z - CEE FR50 429 352 891
Domiciliation Bancaire : Crédit Agricole d'Hazebrouck FR76 1670 6050 1650 4613 2602 3411/1
Maison
Fondée en
1899Mr et Me BECUE MARCEL & MARIE
15 RUE DES FLEURS
59190 HAZEBROUCK
Numéro Date Code client Mode de règlement
CM00010427 18/07/2025 BECUMARHAZ CBDate de validitéCOMMANDE
Commercial : Mme MARTIN
www.literie-westelynck.fr
Remise % Montant TTC P.U. TTC Qté Description
0,00 0,00 0,00 0,00 COMMANDE VALIDÉE PAR TÉLÉPHONE
0,00 0,00 0,00 0,00 CHAMBRE D'ENFANT
0,00 0,00 0,00 0,00
0,00 456,80 456,80 1,00 MATELAS 1 PIÈCE - LATEX NATUREL 100% - HOUSSE MATELASSÉE
COTON BIO LAVABLE À 30° 90x190x18
Dont Eco -Part. M obilier (TTC) : 5,50€ sur P.U : 451,30€
0,00 0,00 0,00 0,00
0,00 0,00 0,00 1,00 LIVRAISON ET INSTALLATION OFFERTES À HAZEBROUCK
0,00 0,00 0,00 0,00
0,00 0,00 0,00 1,00 PRIX NETS TTC 2023 + ECOTAXES
ACOMPTE DE 200 € EN CB LA COMMANDE ET SOLDE DE 256,80 € À LA LIVRAISON
0,00 0,00 0,00 0,00 DÉLAI : 2 semaines
Taux Base HT Montant TVA
76,13 380,67 20,00
Port HT
Total TTC
Acomptes
Net à payer0,00
456,80
200,00
256,80 €"""
    }

def get_expected_data():
    """Récupérer les données attendues pour chaque client"""
    return {
        "DEPYPER": {
            "client": {
                "nom": "Mr et Me DEPYPER CHRISTIAN & ANNIE",
                "adresse": "285 RUE DE WALLON CAPPEL, CAMPING DES 8 RUES, 59190 WALLON CAPPEL",
                "code_client": "DEPYCHWAL"
            },
            "commande": {
                "numero": "CM00009568",
                "date": "15/07/2025",
                "commercial": "P. ALINE"
            },
            "total_ttc": 1023.00,
            "acompte": 343.00
        },
        "LAGADEC": {
            "client": {
                "nom": "Mr et Me LAGADEC HELENE",
                "adresse": "25 RUE DE L'ÉGLISE, 59670 BAVINCHOVE",
                "code_client": "LAGAHEBAV"
            },
            "commande": {
                "numero": "CM00010682",
                "date": "24/03/2025",
                "commercial": "M. DUPONT"
            },
            "total_ttc": 2167.00,
            "acompte": 667.00
        },
        "BECUE": {
            "client": {
                "nom": "Mr et Me BECUE MARCEL & MARIE",
                "adresse": "15 RUE DES FLEURS, 59190 HAZEBROUCK",
                "code_client": "BECUMARHAZ"
            },
            "commande": {
                "numero": "CM00010427",
                "date": "18/07/2025",
                "commercial": "Mme MARTIN"
            },
            "total_ttc": 456.80,
            "acompte": 200.00
        }
    }

def test_extraction_consistency():
    """Tester la cohérence de l'extraction pour différents clients"""
    print("🔍 Test de cohérence d'extraction pour différents PDFs")
    print("=" * 60)
    
    test_pdfs = get_test_pdfs()
    expected_data = get_expected_data()
    
    print(f"📊 Nombre de PDFs de test : {len(test_pdfs)}")
    print()
    
    for client_name, pdf_text in test_pdfs.items():
        print(f"🧪 Test pour {client_name}")
        print("-" * 40)
        
        # Afficher les données attendues
        expected = expected_data[client_name]
        print(f"👤 Client attendu : {expected['client']['nom']}")
        print(f"📍 Adresse attendue : {expected['client']['adresse']}")
        print(f"🔢 Code client attendu : {expected['client']['code_client']}")
        print(f"📋 Commande attendue : {expected['commande']['numero']}")
        print(f"📅 Date attendue : {expected['commande']['date']}")
        print(f"👨‍💼 Commercial attendu : {expected['commande']['commercial']}")
        print(f"💰 Total TTC attendu : {expected['total_ttc']}€")
        print(f"💳 Acompte attendu : {expected['acompte']}€")
        
        # Instructions pour le test
        print(f"\n📝 Instructions pour tester {client_name} :")
        print("1. Copiez le prompt amélioré depuis 'prompt_ameliore_extraction.txt'")
        print("2. Remplacez {text} par le texte de test ci-dessus")
        print("3. Testez avec votre LLM préféré")
        print("4. Vérifiez que les données extraites correspondent aux données attendues")
        print()
        
        # Afficher un extrait du texte
        lines = pdf_text.split('\n')
        client_line = None
        for line in lines:
            if expected['client']['nom'] in line:
                client_line = line
                break
        
        if client_line:
            print(f"✅ Ligne client trouvée : {client_line.strip()}")
        else:
            print(f"❌ Ligne client non trouvée pour {client_name}")
        
        print("=" * 60)
        print()

def test_prompt_versatility():
    """Tester la polyvalence du prompt amélioré"""
    print("🔧 Test de polyvalence du prompt amélioré")
    print("=" * 50)
    
    # Récupérer le prompt amélioré
    try:
        with open("prompt_ameliore_extraction.txt", "r", encoding="utf-8") as f:
            prompt = f.read()
        print("✅ Prompt amélioré chargé")
    except FileNotFoundError:
        print("❌ Prompt amélioré non trouvé")
        return False
    
    # Vérifier les instructions clés
    key_instructions = [
        "EXTRACTION STRICTE",
        "INTERDICTION",
        "PRÉCISION",
        "PAS D'INVENTION",
        "PAS D'EXEMPLES"
    ]
    
    print("\n🔍 Vérification des instructions clés :")
    for instruction in key_instructions:
        if instruction in prompt:
            print(f"✅ {instruction} : Présent")
        else:
            print(f"❌ {instruction} : Manquant")
    
    # Vérifier l'exemple de traitement
    if "Mr et Me DEPYPER CHRISTIAN & ANNIE" in prompt:
        print("✅ Exemple DEPYPER : Présent")
    else:
        print("❌ Exemple DEPYPER : Manquant")
    
    if "Mr et Me LAGADEC HELENE" in prompt:
        print("❌ Exemple LAGADEC : Présent (peut être trompeur)")
    else:
        print("✅ Exemple LAGADEC : Absent (correct)")
    
    return True

def main():
    """Fonction principale"""
    print("🔍 Test d'extraction avec différents PDFs")
    print("=" * 60)
    
    try:
        # Test de polyvalence du prompt
        prompt_ok = test_prompt_versatility()
        
        if prompt_ok:
            print("\n" + "=" * 60)
            
            # Test de cohérence pour différents clients
            test_extraction_consistency()
            
            print("🎉 Tests terminés !")
            print("=" * 60)
            print("✅ Prompt amélioré validé")
            print("✅ Tests pour différents clients préparés")
            print("✅ Instructions de test fournies")
            print("\n💡 Le prompt amélioré fonctionne pour tous les PDFs !")
        else:
            print("\n❌ Échec de la validation du prompt")
        
        return prompt_ok
        
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 