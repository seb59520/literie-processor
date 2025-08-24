#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier l'extraction correcte des données DEPYPER
"""

import sys
import os
import json

# Ajouter le répertoire au path pour importer les modules
sys.path.append(os.path.dirname(__file__))

def get_improved_prompt():
    """Récupérer le prompt amélioré"""
    try:
        with open("prompt_ameliore_extraction.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None

def get_test_text():
    """Récupérer le texte de test DEPYPER"""
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

def analyze_extraction_errors(extracted_json, expected_data):
    """Analyser les erreurs d'extraction"""
    print("🔍 Analyse des erreurs d'extraction")
    print("=" * 50)
    
    errors = []
    
    # Vérifier les données client
    if "client" in extracted_json:
        client = extracted_json["client"]
        
        # Vérifier le nom
        expected_name = "Mr et Me DEPYPER CHRISTIAN & ANNIE"
        if client.get("nom") != expected_name:
            errors.append(f"❌ Nom client incorrect: '{client.get('nom')}' au lieu de '{expected_name}'")
        else:
            print(f"✅ Nom client correct: {client.get('nom')}")
        
        # Vérifier l'adresse
        expected_address = "285 RUE DE WALLON CAPPEL, CAMPING DES 8 RUES, 59190 WALLON CAPPEL"
        if client.get("adresse") != expected_address:
            errors.append(f"❌ Adresse client incorrecte: '{client.get('adresse')}' au lieu de '{expected_address}'")
        else:
            print(f"✅ Adresse client correcte: {client.get('adresse')}")
        
        # Vérifier le code client
        expected_code = "DEPYCHWAL"
        if client.get("code_client") != expected_code:
            errors.append(f"❌ Code client incorrect: '{client.get('code_client')}' au lieu de '{expected_code}'")
        else:
            print(f"✅ Code client correct: {client.get('code_client')}")
    
    # Vérifier les données de commande
    if "commande" in extracted_json:
        commande = extracted_json["commande"]
        
        # Vérifier le numéro de commande
        expected_num = "CM00009568"
        if commande.get("numero") != expected_num:
            errors.append(f"❌ Numéro commande incorrect: '{commande.get('numero')}' au lieu de '{expected_num}'")
        else:
            print(f"✅ Numéro commande correct: {commande.get('numero')}")
        
        # Vérifier la date
        expected_date = "15/07/2025"
        if commande.get("date") != expected_date:
            errors.append(f"❌ Date commande incorrecte: '{commande.get('date')}' au lieu de '{expected_date}'")
        else:
            print(f"✅ Date commande correcte: {commande.get('date')}")
        
        # Vérifier le commercial
        expected_commercial = "P. ALINE"
        if commande.get("commercial") != expected_commercial:
            errors.append(f"❌ Commercial incorrect: '{commande.get('commercial')}' au lieu de '{expected_commercial}'")
        else:
            print(f"✅ Commercial correct: {commande.get('commercial')}")
    
    # Vérifier les articles
    if "articles" in extracted_json:
        articles = extracted_json["articles"]
        print(f"📦 Nombre d'articles détectés: {len(articles)}")
        
        # Chercher les matelas
        matelas_count = 0
        for article in articles:
            if article.get("type") == "matelas":
                matelas_count += 1
                print(f"🛏️ Matelas {matelas_count}: {article.get('description', '')[:50]}...")
        
        if matelas_count != 2:
            errors.append(f"❌ Nombre de matelas incorrect: {matelas_count} au lieu de 2")
        else:
            print(f"✅ Nombre de matelas correct: {matelas_count}")
    
    # Vérifier les paiements
    if "paiement" in extracted_json:
        paiement = extracted_json["paiement"]
        
        # Vérifier le total TTC
        expected_total = 1023.00
        if paiement.get("total_ttc") != expected_total:
            errors.append(f"❌ Total TTC incorrect: {paiement.get('total_ttc')} au lieu de {expected_total}")
        else:
            print(f"✅ Total TTC correct: {paiement.get('total_ttc')}")
        
        # Vérifier l'acompte
        expected_acompte = 343.00
        if paiement.get("acompte") != expected_acompte:
            errors.append(f"❌ Acompte incorrect: {paiement.get('acompte')} au lieu de {expected_acompte}")
        else:
            print(f"✅ Acompte correct: {paiement.get('acompte')}")
    
    return errors

def test_prompt_improvement():
    """Tester l'amélioration du prompt"""
    print("🔧 Test d'amélioration du prompt")
    print("=" * 50)
    
    # Récupérer le prompt amélioré
    improved_prompt = get_improved_prompt()
    if not improved_prompt:
        print("❌ Prompt amélioré non trouvé")
        return False
    
    print("✅ Prompt amélioré chargé")
    
    # Récupérer le texte de test
    test_text = get_test_text()
    print(f"✅ Texte de test chargé ({len(test_text)} caractères)")
    
    # Afficher les données attendues
    print("\n📋 Données attendues pour DEPYPER:")
    print("-" * 40)
    print("👤 Client: Mr et Me DEPYPER CHRISTIAN & ANNIE")
    print("📍 Adresse: 285 RUE DE WALLON CAPPEL, CAMPING DES 8 RUES, 59190 WALLON CAPPEL")
    print("🔢 Code client: DEPYCHWAL")
    print("📋 Commande: CM00009568")
    print("📅 Date: 15/07/2025")
    print("👨‍💼 Commercial: P. ALINE")
    print("🛏️ Matelas: 2 (Médium et Ferme)")
    print("💰 Total TTC: 1023,00€")
    print("💳 Acompte: 343,00€")
    
    # Instructions pour le test manuel
    print("\n🧪 Instructions pour le test:")
    print("-" * 40)
    print("1. Copiez le prompt amélioré depuis 'prompt_ameliore_extraction.txt'")
    print("2. Remplacez {text} par le texte de test DEPYPER")
    print("3. Testez avec votre LLM préféré")
    print("4. Vérifiez que les données extraites correspondent aux données attendues")
    
    return True

def main():
    """Fonction principale"""
    print("🔍 Test d'amélioration du prompt pour extraction DEPYPER")
    print("=" * 60)
    
    try:
        success = test_prompt_improvement()
        
        if success:
            print("\n🎉 Test de préparation terminé !")
            print("=" * 60)
            print("✅ Prompt amélioré créé")
            print("✅ Texte de test préparé")
            print("✅ Données de référence définies")
            print("\n💡 Utilisez le prompt amélioré pour éviter les erreurs d'extraction")
        else:
            print("\n❌ Échec de la préparation du test")
        
        return success
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 