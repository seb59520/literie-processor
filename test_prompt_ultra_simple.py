#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test avec prompt ultra-simple pour forcer l'extraction
"""

import sys
import os

def get_ultra_simple_prompt():
    """Récupérer le prompt ultra-simple"""
    try:
        with open("prompt_ultra_simple.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None

def get_depyper_text():
    """Récupérer le texte DEPYPER"""
    return """--- PAGE 1 ---
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
680,00 €"""

def get_expected_simple_data():
    """Récupérer les données attendues simplifiées"""
    return {
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
        "paiement": {
            "total_ttc": 1023.00,
            "acompte": 343.00
        }
    }

def main():
    """Fonction principale"""
    print("🔍 Test avec prompt ultra-simple")
    print("=" * 50)
    
    try:
        # Récupérer le prompt ultra-simple
        ultra_prompt = get_ultra_simple_prompt()
        if not ultra_prompt:
            print("❌ Prompt ultra-simple non trouvé")
            return False
        
        print("✅ Prompt ultra-simple chargé")
        
        # Récupérer le texte DEPYPER
        depyper_text = get_depyper_text()
        print(f"✅ Texte DEPYPER chargé ({len(depyper_text)} caractères)")
        
        # Récupérer les données attendues
        expected_data = get_expected_simple_data()
        print("✅ Données attendues définies")
        
        # Préparer le prompt avec le texte
        final_prompt = ultra_prompt.replace("{text}", depyper_text)
        
        print(f"\n📝 Instructions pour le test:")
        print("-" * 40)
        print("1. Copiez le prompt ultra-simple ci-dessous")
        print("2. Testez avec votre LLM préféré")
        print("3. Vérifiez que les données sont extraites correctement")
        
        print(f"\n🎯 Données attendues (simplifiées):")
        print("-" * 40)
        print(f"👤 Client: {expected_data['client']['nom']}")
        print(f"📍 Adresse: {expected_data['client']['adresse']}")
        print(f"🔢 Code: {expected_data['client']['code_client']}")
        print(f"📋 Commande: {expected_data['commande']['numero']}")
        print(f"📅 Date: {expected_data['commande']['date']}")
        print(f"👨‍💼 Commercial: {expected_data['commande']['commercial']}")
        print(f"💰 Total TTC: {expected_data['paiement']['total_ttc']}€")
        print(f"💳 Acompte: {expected_data['paiement']['acompte']}€")
        
        print(f"\n📋 Prompt ultra-simple à tester:")
        print("=" * 60)
        print(final_prompt)
        print("=" * 60)
        
        print(f"\n💡 Ce prompt est:")
        print("- ✅ Ultra-simple et direct")
        print("- ✅ Sans structure JSON complexe")
        print("- ✅ Avec instructions claires")
        print("- ✅ Sans exemples trompeurs")
        print("- ✅ Force l'extraction littérale")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 