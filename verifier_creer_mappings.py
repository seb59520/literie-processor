#!/usr/bin/env python3

"""
Script pour vérifier et créer les mappings manquants entre les champs du pré-import et les cellules Excel
"""

import sys
import json
import os
sys.path.append('backend')

from mapping_manager import MappingManager
from pre_import_utils import creer_pre_import, valider_pre_import

def verifier_mappings_existants():
    """Vérifie les mappings existants dans le mapping manager"""
    
    print("🔍 VÉRIFICATION DES MAPPINGS EXISTANTS")
    print("=" * 50)
    
    try:
        # Charger le mapping manager
        mapping_manager = MappingManager()
        
        # Récupérer les mappings actuels
        mappings_matelas = mapping_manager.matelas_mappings
        mappings_sommiers = mapping_manager.sommiers_mappings
        
        print(f"📋 Mappings matelas actuels: {len(mappings_matelas)} champs")
        print(f"📋 Mappings sommiers actuels: {len(mappings_sommiers)} champs")
        
        return mapping_manager, mappings_matelas, mappings_sommiers
        
    except Exception as e:
        print(f"❌ Erreur lors du chargement du mapping manager: {e}")
        return None, {}, {}

def lister_champs_pre_import():
    """Liste tous les champs disponibles dans le pré-import"""
    
    # Données de test pour générer un pré-import complet
    donnees_client = {
        "nom": "Mr TEST MAPPING",
        "adresse": "VILLE TEST"
    }
    
    configurations_matelas = [
        {
            "matelas_index": 1,
            "noyau": "SELECT 43",
            "quantite": 1,
            "hauteur": 20,
            "fermete": "FERME",
            "housse": "MATELASSÉE",
            "matiere_housse": "TENCEL LUXE 3D",
            "poignees": "OUI",
            "dimensions": {"largeur": 89, "longueur": 198},
            "semaine_annee": "25_2025",
            "lundi": "2025-06-16",
            "vendredi": "2025-06-20",
            "commande_client": "TEST",
            "dimension_housse": "89x198",
            "dimension_housse_longueur": "198",
            "decoupe_noyau": "STANDARD",
            "surmatelas": True,
            "mots_operations_trouves": ["ENLEVEMENT", "LIVRAISON"]
        }
    ]
    
    # Créer le pré-import pour obtenir tous les champs
    pre_import_data = creer_pre_import(configurations_matelas, donnees_client, contient_dosseret_tete=True)
    
    if pre_import_data:
        # Récupérer tous les champs du premier élément
        champs_pre_import = list(pre_import_data[0].keys())
        
        # Filtrer les champs de référence
        champs_mapping = [champ for champ in champs_pre_import if champ not in ['matelas_index', 'noyau', 'quantite']]
        
        print(f"📋 Champs pré-import disponibles: {len(champs_mapping)}")
        return champs_mapping
    else:
        print("❌ Impossible de générer le pré-import de test")
        return []

def identifier_mappings_manquants(champs_pre_import, mappings_existants):
    """Identifie les mappings manquants"""
    
    print("\n🔍 IDENTIFICATION DES MAPPINGS MANQUANTS")
    print("-" * 40)
    
    mappings_manquants = []
    
    for champ in champs_pre_import:
        if champ not in mappings_existants:
            mappings_manquants.append(champ)
            print(f"  ❌ Manquant: {champ}")
        else:
            print(f"  ✅ Existant: {champ} -> {mappings_existants[champ]}")
    
    return mappings_manquants

def proposer_mappings_manquants(champs_manquants):
    """Propose des mappings pour les champs manquants"""
    
    print(f"\n💡 PROPOSITION DE MAPPINGS POUR {len(champs_manquants)} CHAMPS MANQUANTS")
    print("-" * 60)
    
    # Mapping intelligent basé sur le nom du champ
    propositions = {}
    
    for champ in champs_manquants:
        # Extraire les informations du nom du champ
        if '_C' in champ:
            # Champ C (colonne C)
            partie_nom = champ.split('_C')[0]
            ligne = champ.split('_C')[1]
            propositions[champ] = f"C{ligne}"
        elif '_D' in champ:
            # Champ D (colonne D)
            partie_nom = champ.split('_D')[0]
            ligne = champ.split('_D')[1]
            propositions[champ] = f"D{ligne}"
        else:
            # Champ par défaut
            propositions[champ] = "C1"  # Par défaut
        
        print(f"  📝 {champ} -> {propositions[champ]}")
    
    return propositions

def creer_mappings_manquants(mapping_manager, propositions):
    """Crée les mappings manquants dans le mapping manager"""
    
    print(f"\n🔧 CRÉATION DES MAPPINGS MANQUANTS")
    print("-" * 40)
    
    if not propositions:
        print("  ✅ Aucun mapping manquant à créer")
        return True
    
    try:
        # Ajouter les nouveaux mappings aux mappings existants
        mappings_actuels = mapping_manager.matelas_mappings.copy()
        mappings_actuels.update(propositions)
        
        # Sauvegarder les mappings mis à jour
        mapping_manager.matelas_mappings = mappings_actuels
        mapping_manager.save_mappings("matelas", mappings_actuels)
        
        print(f"  ✅ {len(propositions)} mappings créés avec succès")
        
        # Afficher les nouveaux mappings
        for champ, cellule in propositions.items():
            print(f"    📝 {champ} -> {cellule}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lors de la création des mappings: {e}")
        return False

def verifier_mapping_specifique(champ_specifique="SL43_Ferme_C40"):
    """Vérifie un mapping spécifique"""
    
    print(f"\n🎯 VÉRIFICATION DU MAPPING SPÉCIFIQUE: {champ_specifique}")
    print("-" * 50)
    
    try:
        mapping_manager = MappingManager()
        mappings_matelas = mapping_manager.matelas_mappings
        
        if champ_specifique in mappings_matelas:
            cellule = mappings_matelas[champ_specifique]
            print(f"  ✅ Mapping existant: {champ_specifique} -> {cellule}")
            
            # Vérifier si la cellule correspond au nom du champ
            if champ_specifique.endswith("_C40"):
                cellule_attendue = "C40"
                if cellule == cellule_attendue:
                    print(f"  ✅ Cellule correcte: {cellule} (attendue: {cellule_attendue})")
                else:
                    print(f"  ⚠️  Cellule incorrecte: {cellule} (attendue: {cellule_attendue})")
                    return False
        else:
            print(f"  ❌ Mapping manquant: {champ_specifique}")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lors de la vérification: {e}")
        return False

def test_mapping_complet():
    """Test complet du mapping avec des données réelles"""
    
    print(f"\n🧪 TEST COMPLET DU MAPPING")
    print("-" * 30)
    
    try:
        # Données de test
        donnees_client = {
            "nom": "Mr TEST SL43",
            "adresse": "VILLE TEST"
        }
        
        configurations_matelas = [
            {
                "matelas_index": 1,
                "noyau": "SELECT 43",
                "quantite": 1,
                "hauteur": 20,
                "fermete": "FERME",
                "housse": "MATELASSÉE",
                "matiere_housse": "TENCEL LUXE 3D",
                "poignees": "OUI",
                "dimensions": {"largeur": 89, "longueur": 198},
                "semaine_annee": "25_2025",
                "lundi": "2025-06-16",
                "vendredi": "2025-06-20",
                "commande_client": "TEST",
                "dimension_housse": "89x198",
                "dimension_housse_longueur": "198",
                "decoupe_noyau": "STANDARD",
                "surmatelas": True,
                "mots_operations_trouves": ["ENLEVEMENT", "LIVRAISON"]
            }
        ]
        
        # Créer le pré-import
        pre_import_data = creer_pre_import(configurations_matelas, donnees_client, contient_dosseret_tete=True)
        
        if pre_import_data:
            item = pre_import_data[0]
            
            # Vérifier le champ spécifique
            if "SL43_Ferme_C40" in item:
                valeur = item["SL43_Ferme_C40"]
                print(f"  ✅ Champ SL43_Ferme_C40 trouvé: '{valeur}'")
                
                if valeur == "X":
                    print(f"  ✅ Valeur correcte pour SELECT 43 FERME")
                else:
                    print(f"  ⚠️  Valeur inattendue: '{valeur}'")
            else:
                print(f"  ❌ Champ SL43_Ferme_C40 manquant dans le pré-import")
            
            # Afficher tous les champs SL43
            champs_sl43 = [k for k in item.keys() if k.startswith("SL43")]
            print(f"  📋 Champs SL43 trouvés: {champs_sl43}")
            
            for champ in champs_sl43:
                print(f"    - {champ}: '{item[champ]}'")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lors du test: {e}")
        return False

def main():
    """Fonction principale"""
    
    print("🔧 VÉRIFICATION ET CRÉATION DES MAPPINGS")
    print("=" * 60)
    
    # 1. Vérifier les mappings existants
    mapping_manager, mappings_matelas, mappings_sommiers = verifier_mappings_existants()
    
    if not mapping_manager:
        print("❌ Impossible de continuer sans mapping manager")
        return
    
    # 2. Lister tous les champs du pré-import
    champs_pre_import = lister_champs_pre_import()
    
    if not champs_pre_import:
        print("❌ Impossible de lister les champs du pré-import")
        return
    
    # 3. Identifier les mappings manquants
    mappings_manquants = identifier_mappings_manquants(champs_pre_import, mappings_matelas)
    
    # 4. Proposer des mappings pour les champs manquants
    if mappings_manquants:
        propositions = proposer_mappings_manquants(mappings_manquants)
        
        # 5. Créer les mappings manquants
        succes = creer_mappings_manquants(mapping_manager, propositions)
        
        if succes:
            print(f"\n✅ {len(mappings_manquants)} mappings créés avec succès")
        else:
            print(f"\n❌ Erreur lors de la création des mappings")
    else:
        print(f"\n✅ Tous les mappings sont déjà présents")
    
    # 6. Vérifier le mapping spécifique SL43_Ferme_C40
    verifier_mapping_specifique("SL43_Ferme_C40")
    
    # 7. Test complet
    test_mapping_complet()
    
    print(f"\n🎉 Vérification terminée!")

if __name__ == "__main__":
    main() 