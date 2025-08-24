#!/usr/bin/env python3
"""
Test de la fonction creer_pre_import corrigée
"""

import sys
import os

# Ajouter le répertoire backend au path
sys.path.append('backend')

from pre_import_utils import creer_pre_import, valider_pre_import

def test_pre_import_fixed():
    """Test de la fonction creer_pre_import avec les corrections de sécurité"""
    
    print("=== TEST PRÉ-IMPORT CORRIGÉ ===")
    
    # Test 1: Paramètres valides
    print("\n📋 Test 1: Paramètres valides")
    configurations_matelas = [
        {
            "matelas_index": 1,
            "noyau": "MOUSSE RAINUREE 7 ZONES",
            "quantite": 2,
            "hauteur": 20,
            "fermete": "FERME",
            "housse": "MATELASSÉE",
            "matiere_housse": "TENCEL LUXE 3D",
            "poignees": "INTÉGRÉES",
            "dimensions": {"largeur": 79, "longueur": 198},
            "semaine_annee": "25_2025",
            "lundi": "2025-06-16",
            "vendredi": "2025-06-20",
            "commande_client": "GALOO"
        }
    ]
    
    donnees_client = {
        "nom": "Mr et Mme GALOO PASCAL & SANDRINE",
        "adresse": "OXELAERE",
        "code_client": "GALOPOX",
        "titre": "Mr et Mme"
    }
    
    try:
        pre_import_data = creer_pre_import(configurations_matelas, donnees_client, False, [], False)
        print(f"✅ Pré-import créé avec succès: {len(pre_import_data)} éléments")
        
        if pre_import_data:
            validation = valider_pre_import(pre_import_data)
            print(f"✅ Validation: {validation}")
            
            # Afficher le premier élément
            print(f"📋 Premier élément: {pre_import_data[0]}")
        else:
            print("❌ Pré-import vide")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Test 2: Paramètres None (doit retourner liste vide)
    print("\n📋 Test 2: Paramètres None")
    try:
        pre_import_data = creer_pre_import(None, donnees_client, False, [], False)
        print(f"✅ Retourne liste vide pour configurations_matelas None: {len(pre_import_data)} éléments")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
    
    try:
        pre_import_data = creer_pre_import(configurations_matelas, None, False, [], False)
        print(f"✅ Retourne liste vide pour donnees_client None: {len(pre_import_data)} éléments")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
    
    # Test 3: Paramètres vides (doit retourner liste vide)
    print("\n📋 Test 3: Paramètres vides")
    try:
        pre_import_data = creer_pre_import([], donnees_client, False, [], False)
        print(f"✅ Retourne liste vide pour configurations_matelas vide: {len(pre_import_data)} éléments")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
    
    try:
        pre_import_data = creer_pre_import(configurations_matelas, {}, False, [], False)
        print(f"✅ Retourne liste vide pour donnees_client vide: {len(pre_import_data)} éléments")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
    
    print("\n=== FIN DES TESTS ===")

if __name__ == "__main__":
    test_pre_import_fixed()

