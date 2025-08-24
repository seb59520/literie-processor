#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour la génération d'exemples de devis variés
"""

import sys
import os
import json
import random
from datetime import datetime, timedelta

# Ajouter le répertoire au path pour importer les modules
sys.path.append(os.path.dirname(__file__))

def generate_random_devis_example():
    """Générer un exemple de devis aléatoire pour les tests"""
    # Données aléatoires pour varier les exemples
    clients = [
        ("Mr et Me LAGADEC HELENE", "25 RUE DE L'ÉGLISE, 59670 BAVINCHOVE", "LAGAHEBAV"),
        ("Mr DUPONT JEAN", "15 AVENUE DE LA PAIX, 59000 LILLE", "DUPOJEALIL"),
        ("Me MARTIN SOPHIE", "8 RUE DU COMMERCE, 59100 ROUBAIX", "MARTSOPROU"),
        ("Mr et Me DURAND PIERRE", "42 BOULEVARD VICTOR HUGO, 59200 TOURCOING", "DURAPIEVIC"),
        ("Mr LEROY ANTOINE", "3 PLACE DE LA RÉPUBLIQUE, 59300 VALENCIENNES", "LEROANTPLA")
    ]
    
    produits = [
        ("LITERIE 160/200/59 CM JUMEAUX SUR PIEDS", [
            "SOMMIERS JUMEAUX RELAXATION MOTORISÉE 5 PLIS PETITE TÊTIÈRE",
            "MÉTRAGE PVC SARANO CAMEL",
            "DOSSERET GALBÉ COINS VIFS 160/90 BASE SOMMIERS",
            "JEU DE 4 PIEDS CYLINDRE VERNI NATUREL 20 CM + 2 PIEDS CENTRAUX + PATINS FEUTRES",
            "MATELAS JUMEAUX - MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES MÉDIUM (50KG/M3)"
        ]),
        ("LITERIE 140/190/59 CM DOUBLE SUR PIEDS", [
            "SOMMIER DOUBLE RELAXATION MOTORISÉE 5 PLIS GRANDE TÊTIÈRE",
            "MÉTRAGE PVC SARANO GRIS",
            "DOSSERET GALBÉ COINS VIFS 140/90 BASE SOMMIERS",
            "JEU DE 4 PIEDS CYLINDRE VERNI NATUREL 20 CM + PATINS FEUTRES",
            "MATELAS DOUBLE - MOUSSE VISCOÉLASTIQUE 7 ZONES DIFFÉRENCIÉES FERME (60KG/M3)"
        ]),
        ("LITERIE 90/200/59 CM SIMPLE SUR PIEDS", [
            "SOMMIER SIMPLE RELAXATION MOTORISÉE 5 PLIS PETITE TÊTIÈRE",
            "MÉTRAGE PVC SARANO BLANC",
            "DOSSERET DROIT COINS VIFS 90/90 BASE SOMMIERS",
            "JEU DE 4 PIEDS CYLINDRE VERNI NATUREL 20 CM + PATINS FEUTRES",
            "MATELAS SIMPLE - LATEX NATUREL 7 ZONES DIFFÉRENCIÉES DOUX (70KG/M3)"
        ])
    ]
    
    remises = [
        ("REMISE 50% SOLDES MODÈLE D'EXPOSITION", -1295.00),
        ("REMISE 30% FIN DE SÉRIE", -850.00),
        ("REMISE 20% PREMIÈRE COMMANDE", -450.00),
        ("REMISE 15% CLIENT FIDÈLE", -320.00),
        ("REMISE 10% PAIEMENT COMPTANT", -180.00)
    ]
    
    # Sélection aléatoire
    client = random.choice(clients)
    produit = random.choice(produits)
    remise = random.choice(remises)
    
    # Date aléatoire dans les 30 derniers jours
    date_commande = datetime.now() - timedelta(days=random.randint(0, 30))
    
    # Numéro de commande aléatoire
    num_commande = f"CM{random.randint(100000, 999999)}"
    
    # Montants aléatoires
    base_ht = random.randint(1500, 3000)
    tva = base_ht * 0.20
    total_ttc = base_ht + tva
    acompte = random.randint(500, 1000)
    net_a_payer = total_ttc - acompte
    
    # Générer le devis
    example_text = f"""DEVIS LITERIE WESTELYNCK

SAS Literie Westelynck
Capital : 23 100 Euros
525 RD 642 - 59190 BORRE
Tél : 03.28.48.04.19
Email : contact@lwest.fr
SIRET : 429 352 891 00015
APE : 3103Z
CEE : FR50 429 352 891
Banque : Crédit Agricole d'Hazebrouck
IBAN : FR76 1670 6050 1650 4613 2602 341

CLIENT :
{client[0]}
{client[1]}
Code client : {client[2]}

COMMANDE N° {num_commande}
Date : {date_commande.strftime('%d/%m/%Y')}
Commercial : P. ALINE
Origine : COMMANDE

LIVRAISON : ENLÈVEMENT PAR VOS SOINS

{produit[0]}

"""
    
    # Ajouter les produits
    for i, prod in enumerate(produit[1], 1):
        example_text += f"{i}. {prod}\n   Quantité : {random.randint(1, 3)}\n\n"
    
    # Ajouter la remise
    example_text += f"{len(produit[1]) + 1}. {remise[0]}\n   Montant : {remise[1]:.2f}€\n\n"
    
    # Ajouter la remise enlèvement
    remise_enlevement = random.randint(20, 100)
    example_text += f"{len(produit[1]) + 2}. REMISE : 5% ENLÈVEMENT PAR VOS SOINS\n   Montant : -{remise_enlevement:.2f}€\n\n"
    
    # Conditions de paiement et totaux
    example_text += f"""CONDITIONS DE PAIEMENT :
ACOMPTE DE {acompte} € EN CB LA COMMANDE ET SOLDE DE {net_a_payer:.0f} € À L'ENLÈVEMENT

PORT HT : 0,00€
BASE HT : {base_ht:.2f}€
TVA 20% : {tva:.2f}€
TOTAL TTC : {total_ttc:.2f}€
ACOMPTE : {acompte:.2f}€
NET À PAYER : {net_a_payer:.2f}€"""
    
    return example_text

def test_generation_exemples():
    """Test de génération d'exemples variés"""
    print("🎲 Test de génération d'exemples de devis variés")
    print("=" * 60)
    
    # Générer plusieurs exemples
    examples = []
    for i in range(5):
        print(f"\n📋 Exemple {i+1}:")
        print("-" * 40)
        
        example = generate_random_devis_example()
        examples.append(example)
        
        # Afficher les informations clés
        lines = example.split('\n')
        
        # Extraire les informations importantes
        client_line = None
        commande_line = None
        produit_line = None
        
        for line in lines:
            if "CLIENT :" in line:
                client_line = lines[lines.index(line) + 1].strip()
            elif "COMMANDE N°" in line:
                commande_line = line.strip()
            elif "LITERIE" in line and "CM" in line:
                produit_line = line.strip()
                break
        
        print(f"👤 Client: {client_line}")
        print(f"📋 Commande: {commande_line}")
        print(f"🛏️ Produit: {produit_line}")
        
        # Vérifier la variété
        if i > 0:
            # Comparer avec les exemples précédents
            is_different = False
            for prev_example in examples[:-1]:
                if example != prev_example:
                    is_different = True
                    break
            
            if is_different:
                print("✅ Exemple différent des précédents")
            else:
                print("⚠️ Exemple identique aux précédents")
    
    # Test de variété globale
    print(f"\n📊 Analyse de variété:")
    print(f"   • Nombre d'exemples générés: {len(examples)}")
    
    unique_examples = set(examples)
    print(f"   • Exemples uniques: {len(unique_examples)}")
    
    if len(unique_examples) == len(examples):
        print("✅ Tous les exemples sont différents")
    else:
        print(f"⚠️ {len(examples) - len(unique_examples)} exemples identiques détectés")
    
    # Test de structure
    print(f"\n🔍 Test de structure:")
    for i, example in enumerate(examples):
        required_sections = [
            "DEVIS LITERIE WESTELYNCK",
            "CLIENT :",
            "COMMANDE N°",
            "LITERIE",
            "CONDITIONS DE PAIEMENT :",
            "TOTAL TTC :"
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in example:
                missing_sections.append(section)
        
        if missing_sections:
            print(f"   ❌ Exemple {i+1}: Sections manquantes: {missing_sections}")
        else:
            print(f"   ✅ Exemple {i+1}: Structure complète")
    
    return len(unique_examples) == len(examples)

def main():
    """Fonction principale"""
    print("🎲 Test de génération d'exemples de devis")
    print("=" * 60)
    
    try:
        success = test_generation_exemples()
        
        print(f"\n🎉 Test terminé !")
        print("=" * 60)
        
        if success:
            print("✅ GÉNÉRATION D'EXEMPLES FONCTIONNELLE")
            print("   • Tous les exemples sont différents")
            print("   • Structure complète maintenue")
            print("   • Variété des données assurée")
        else:
            print("⚠️ PROBLÈMES DÉTECTÉS")
            print("   • Certains exemples sont identiques")
            print("   • Vérifiez la génération aléatoire")
        
        return success
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 