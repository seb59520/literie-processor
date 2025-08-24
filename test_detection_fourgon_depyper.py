#!/usr/bin/env python3
"""
Test spécifique de la détection du mode de livraison dans la commande DEPYPER
"""

import json
import re

def get_depyper_text():
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

def analyser_texte_livraison(texte):
    """Analyse le texte pour détecter les informations de livraison"""
    print("🔍 ANALYSE DE LA DÉTECTION DE LIVRAISON")
    print("=" * 60)
    
    # Normaliser le texte
    texte_upper = texte.upper()
    
    print(f"📄 Texte analysé ({len(texte)} caractères)")
    print()
    
    # 1. Recherche des mots-clés de livraison
    mots_cles_livraison = [
        "FOURGON", "LIVRAISON", "ENLÈVEMENT", "RETRAIT", "TRANSPORTEUR",
        "TRANSPORT", "INSTALLATION", "CAMPING"
    ]
    
    print("🎯 RECHERCHE DES MOTS-CLÉS DE LIVRAISON:")
    for mot in mots_cles_livraison:
        if mot in texte_upper:
            # Trouver le contexte autour du mot
            index = texte_upper.find(mot)
            debut = max(0, index - 50)
            fin = min(len(texte), index + len(mot) + 50)
            contexte = texte[debut:fin]
            print(f"   ✅ '{mot}' trouvé dans: '{contexte.strip()}'")
        else:
            print(f"   ❌ '{mot}' non trouvé")
    
    print()
    
    # 2. Recherche spécifique des phrases de livraison
    phrases_livraison = [
        r"LIVRAISON.*CAMPING",
        r"CAMPING.*LIVRAISON", 
        r"LIVRAISON.*OFFERTES",
        r"INSTALLATION.*OFFERTES",
        r"AU CAMPING",
        r"LIVRAISON.*INSTALLATION"
    ]
    
    print("🔍 RECHERCHE DES PHRASES DE LIVRAISON:")
    for pattern in phrases_livraison:
        matches = re.findall(pattern, texte_upper, re.IGNORECASE)
        if matches:
            for match in matches:
                print(f"   ✅ Pattern '{pattern}': '{match}'")
        else:
            print(f"   ❌ Pattern '{pattern}': Aucun match")
    
    print()
    
    # 3. Analyse du contexte de livraison
    print("📋 ANALYSE DU CONTEXTE DE LIVRAISON:")
    
    # Chercher la ligne complète contenant "LIVRAISON"
    lignes = texte.split('\n')
    for i, ligne in enumerate(lignes):
        if 'LIVRAISON' in ligne.upper():
            print(f"   📍 Ligne {i+1}: '{ligne.strip()}'")
            
            # Analyser cette ligne
            if 'CAMPING' in ligne.upper():
                print(f"      🏕️ Contient 'CAMPING' → Livraison sur site")
            if 'OFFERTES' in ligne.upper():
                print(f"      🎁 Contient 'OFFERTES' → Service gratuit")
            if 'INSTALLATION' in ligne.upper():
                print(f"      🔧 Contient 'INSTALLATION' → Service complet")
    
    print()
    
    # 4. Classification du mode de livraison
    print("🏷️ CLASSIFICATION DU MODE DE LIVRAISON:")
    
    if 'CAMPING' in texte_upper and 'LIVRAISON' in texte_upper:
        print("   🚚 Mode détecté: LIVRAISON SUR SITE (CAMPING)")
        print("   📍 Localisation: CAMPING DES 8 RUES A WALLON CAPPEL")
        print("   💰 Service: OFFERT (gratuit)")
        print("   🔧 Inclus: INSTALLATION")
        print()
        print("   🎯 RECOMMANDATION: fourgon_C58 = 'LIVRAISON ET INSTALLATION OFFERTES AU CAMPING DES 8 RUES A WALLON CAPPEL'")
    else:
        print("   ❓ Mode de livraison non clairement identifié")
    
    print()
    
    # 5. Vérification des champs JSON attendus
    print("📊 CHAMPS JSON ATTENDUS:")
    print("   emporte_client_C57: null (pas d'enlèvement client)")
    print("   fourgon_C58: 'LIVRAISON ET INSTALLATION OFFERTES AU CAMPING DES 8 RUES A WALLON CAPPEL'")
    print("   transporteur_C59: null (pas de transporteur externe)")
    
    return True

def simuler_extraction_llm():
    """Simule ce que devrait extraire le LLM"""
    print("\n🤖 SIMULATION D'EXTRACTION LLM")
    print("=" * 60)
    
    print("📋 JSON attendu pour la commande DEPYPER:")
    
    json_attendu = {
        "mode_mise_a_disposition": {
            "emporte_client_C57": None,
            "fourgon_C58": "LIVRAISON ET INSTALLATION OFFERTES AU CAMPING DES 8 RUES A WALLON CAPPEL",
            "transporteur_C59": None
        }
    }
    
    print(json.dumps(json_attendu, indent=2, ensure_ascii=False))
    
    print("\n✅ Ce JSON devrait être extrait par le LLM")
    print("❌ Si ce n'est pas le cas, le prompt LLM doit être amélioré")

def main():
    """Fonction principale"""
    print("🔍 TEST DE DÉTECTION FOURGON - COMMANDE DEPYPER")
    print("=" * 70)
    
    # Récupérer le texte DEPYPER
    texte = get_depyper_text()
    
    # Analyser le texte
    analyser_texte_livraison(texte)
    
    # Simuler l'extraction LLM
    simuler_extraction_llm()
    
    print("\n🎯 CONCLUSION:")
    print("La commande DEPYPER contient clairement des informations de livraison")
    print("Le LLM devrait détecter: 'LIVRAISON ET INSTALLATION OFFERTES AU CAMPING'")
    print("Si ce n'est pas le cas, le prompt LLM doit être amélioré pour mieux détecter")
    print("les livraisons sur site et les services d'installation")

if __name__ == "__main__":
    main()

