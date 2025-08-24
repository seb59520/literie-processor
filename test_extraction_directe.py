#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour l'extraction directe avec le prompt amélioré
"""

import sys
import os
import json

def get_improved_prompt():
    """Récupérer le prompt amélioré"""
    try:
        with open("prompt_ameliore_extraction.txt", "r", encoding="utf-8") as f:
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

def get_expected_depyper_data():
    """Récupérer les données attendues pour DEPYPER"""
    return {
        "societe": {
            "nom": "SAS Literie Westelynck",
            "capital": "23 100 Euros",
            "adresse": "525 RD 642 - 59190 BORRE",
            "telephone": "03.28.48.04.19",
            "email": "contact@lwest.fr",
            "siret": "429 352 891 00015",
            "APE": "3103Z",
            "CEE": "FR50 429 352 891",
            "banque": "Crédit Agricole d'Hazebrouck",
            "IBAN": "FR76 1670 6050 1650 4613 2602 3411/1"
        },
        "client": {
            "nom": "Mr et Me DEPYPER CHRISTIAN & ANNIE",
            "adresse": "285 RUE DE WALLON CAPPEL, CAMPING DES 8 RUES, 59190 WALLON CAPPEL",
            "code_client": "DEPYCHWAL"
        },
        "commande": {
            "numero": "CM00009568",
            "date": "15/07/2025",
            "date_validite": "",
            "commercial": "P. ALINE",
            "origine": "COMMANDE"
        },
        "mode_mise_a_disposition": {
            "emporte_client_C57": "",
            "fourgon_C58": "",
            "transporteur_C59": ""
        },
        "articles": [
            {
                "type": "matelas",
                "description": "MATELAS 1 PIÈCE -MOUSSE RAINUR ÉE 7 ZONES DIFFÉRENCIÉES MÉDIUM (50KG/ M3) -HOUSSE MATELASS ÉETENCEL LUXE 3D LAVABLE A 40°  79/ 189/ 20",
                "titre_cote": "Mme Gauche",
                "information": "",
                "quantite": 1,
                "dimensions": "79x189x20",
                "noyau": "MOUSSE RAINUR ÉE 7 ZONES",
                "fermete": "MÉDIUM",
                "housse": "MATELASS ÉE",
                "matiere_housse": "TENCEL LUXE 3D",
                "autres_caracteristiques": {
                    "lavable": "40°",
                    "ecotaxe": "5,50€"
                }
            },
            {
                "type": "matelas",
                "description": "MATELAS 1 PIÈCE -MOUSSE RAINUR ÉE 7 ZONES DIFFÉRENCIÉES FERME (55KG/ M3) -HOUSSE MATELASS ÉETENCEL LUXE 3D LAVABLE A 40°  79/ 189/ 20",
                "titre_cote": "Mr Droite",
                "information": "",
                "quantite": 1,
                "dimensions": "79x189x20",
                "noyau": "MOUSSE RAINUR ÉE 7 ZONES",
                "fermete": "FERME",
                "housse": "MATELASS ÉE",
                "matiere_housse": "TENCEL LUXE 3D",
                "autres_caracteristiques": {
                    "lavable": "40°",
                    "ecotaxe": "5,50€"
                }
            }
        ],
        "paiement": {
            "conditions": "ACOMPTE DE 343 € EN CB A LA COMMANDE ET SOLDE DE 680 € A LA LIVRAISON",
            "port_ht": 0.00,
            "base_ht": 843.34,
            "taux_tva": 20.00,
            "total_ttc": 1023.00,
            "acompte": 343.00,
            "net_a_payer": 680.00
        }
    }

def analyze_extraction_result(extracted_json, expected_data):
    """Analyser le résultat de l'extraction"""
    print("🔍 Analyse du résultat d'extraction")
    print("=" * 50)
    
    errors = []
    successes = []
    
    # Vérifier les données client
    if "client" in extracted_json:
        client = extracted_json["client"]
        expected_client = expected_data["client"]
        
        # Vérifier le nom
        if client.get("nom") == expected_client["nom"]:
            successes.append(f"✅ Nom client correct: {client.get('nom')}")
        else:
            errors.append(f"❌ Nom client incorrect: '{client.get('nom')}' au lieu de '{expected_client['nom']}'")
        
        # Vérifier l'adresse
        if client.get("adresse") == expected_client["adresse"]:
            successes.append(f"✅ Adresse client correcte: {client.get('adresse')}")
        else:
            errors.append(f"❌ Adresse client incorrecte: '{client.get('adresse')}' au lieu de '{expected_client['adresse']}'")
        
        # Vérifier le code client
        if client.get("code_client") == expected_client["code_client"]:
            successes.append(f"✅ Code client correct: {client.get('code_client')}")
        else:
            errors.append(f"❌ Code client incorrect: '{client.get('code_client')}' au lieu de '{expected_client['code_client']}'")
    
    # Vérifier les données de commande
    if "commande" in extracted_json:
        commande = extracted_json["commande"]
        expected_commande = expected_data["commande"]
        
        # Vérifier le numéro de commande
        if commande.get("numero") == expected_commande["numero"]:
            successes.append(f"✅ Numéro commande correct: {commande.get('numero')}")
        else:
            errors.append(f"❌ Numéro commande incorrect: '{commande.get('numero')}' au lieu de '{expected_commande['numero']}'")
        
        # Vérifier la date
        if commande.get("date") == expected_commande["date"]:
            successes.append(f"✅ Date commande correcte: {commande.get('date')}")
        else:
            errors.append(f"❌ Date commande incorrecte: '{commande.get('date')}' au lieu de '{expected_commande['date']}'")
        
        # Vérifier le commercial
        if commande.get("commercial") == expected_commande["commercial"]:
            successes.append(f"✅ Commercial correct: {commande.get('commercial')}")
        else:
            errors.append(f"❌ Commercial incorrect: '{commande.get('commercial')}' au lieu de '{expected_commande['commercial']}'")
    
    # Vérifier les paiements
    if "paiement" in extracted_json:
        paiement = extracted_json["paiement"]
        expected_paiement = expected_data["paiement"]
        
        # Vérifier le total TTC
        if paiement.get("total_ttc") == expected_paiement["total_ttc"]:
            successes.append(f"✅ Total TTC correct: {paiement.get('total_ttc')}")
        else:
            errors.append(f"❌ Total TTC incorrect: {paiement.get('total_ttc')} au lieu de {expected_paiement['total_ttc']}")
        
        # Vérifier l'acompte
        if paiement.get("acompte") == expected_paiement["acompte"]:
            successes.append(f"✅ Acompte correct: {paiement.get('acompte')}")
        else:
            errors.append(f"❌ Acompte incorrect: {paiement.get('acompte')} au lieu de {expected_paiement['acompte']}")
    
    # Afficher les résultats
    print(f"\n📊 Résultats de l'analyse:")
    print(f"✅ Succès: {len(successes)}")
    print(f"❌ Erreurs: {len(errors)}")
    
    if successes:
        print(f"\n✅ Succès:")
        for success in successes:
            print(f"  {success}")
    
    if errors:
        print(f"\n❌ Erreurs:")
        for error in errors:
            print(f"  {error}")
    
    return len(errors) == 0

def main():
    """Fonction principale"""
    print("🔍 Test d'extraction directe avec le prompt amélioré")
    print("=" * 60)
    
    try:
        # Récupérer le prompt amélioré
        improved_prompt = get_improved_prompt()
        if not improved_prompt:
            print("❌ Prompt amélioré non trouvé")
            return False
        
        print("✅ Prompt amélioré chargé")
        
        # Récupérer le texte DEPYPER
        depyper_text = get_depyper_text()
        print(f"✅ Texte DEPYPER chargé ({len(depyper_text)} caractères)")
        
        # Récupérer les données attendues
        expected_data = get_expected_depyper_data()
        print("✅ Données attendues définies")
        
        # Préparer le prompt avec le texte
        final_prompt = improved_prompt.replace("{text}", depyper_text)
        
        print(f"\n📝 Instructions pour le test:")
        print("-" * 40)
        print("1. Copiez le prompt final ci-dessous")
        print("2. Testez avec votre LLM préféré")
        print("3. Comparez le résultat avec les données attendues")
        print("4. Vérifiez que les données extraites sont correctes")
        
        print(f"\n🎯 Données attendues pour DEPYPER:")
        print("-" * 40)
        print(f"👤 Client: {expected_data['client']['nom']}")
        print(f"📍 Adresse: {expected_data['client']['adresse']}")
        print(f"🔢 Code: {expected_data['client']['code_client']}")
        print(f"📋 Commande: {expected_data['commande']['numero']}")
        print(f"📅 Date: {expected_data['commande']['date']}")
        print(f"👨‍💼 Commercial: {expected_data['commande']['commercial']}")
        print(f"💰 Total TTC: {expected_data['paiement']['total_ttc']}€")
        print(f"💳 Acompte: {expected_data['paiement']['acompte']}€")
        
        print(f"\n📋 Prompt final à tester:")
        print("=" * 60)
        print(final_prompt)
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 