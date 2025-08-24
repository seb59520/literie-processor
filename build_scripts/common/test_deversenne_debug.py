#!/usr/bin/env python3
"""
Test de debug complet pour la commande Deversenne
"""

import sys
import os
sys.path.append('backend')

from matelas_utils import detecter_noyau_matelas
from fermete_utils import detecter_fermete_matelas
from housse_utils import detecter_type_housse
from matiere_housse_utils import detecter_matiere_housse
from poignees_utils import detecter_poignees
from pre_import_utils import creer_pre_import

def test_deversenne_debug():
    """Test de debug complet pour Deversenne"""
    
    # Description exacte de Deversenne
    description = "MATELAS 1 PIÈCE - MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES FERME (50KG/ M3) - HOUSSE MATELASSÉE TENCEL LUXE 3D AVEC POIGNÉES INTÉGRÉES LAVABLE A 40°"
    
    print("=== Test de debug Deversenne ===")
    print(f"Description: {description}")
    
    # Test de détection du noyau
    print(f"\n--- Détection noyau ---")
    articles = [{"description": description}]
    noyaux = detecter_noyau_matelas(articles)
    print(f"Noyaux détectés: {noyaux}")
    
    # Test de détection de fermeté
    print(f"\n--- Détection fermeté ---")
    fermete = detecter_fermete_matelas(description)
    print(f"Fermeté détectée: {fermete}")
    
    # Test de détection housse
    print(f"\n--- Détection housse ---")
    housse = detecter_type_housse(description)
    print(f"Type housse: {housse}")
    
    # Test de détection matière housse
    print(f"\n--- Détection matière housse ---")
    matiere_housse = detecter_matiere_housse(description)
    print(f"Matière housse: {matiere_housse}")
    
    # Test de détection poignées
    print(f"\n--- Détection poignées ---")
    poignees = detecter_poignees(description)
    print(f"Poignées: {poignees}")
    
    # Test de création de configuration
    print(f"\n--- Création configuration ---")
    if noyaux:
        noyau_info = noyaux[0]
        config = {
            "matelas_index": 1,
            "noyau": noyau_info["noyau"],
            "quantite": 2,
            "hauteur": 9,
            "fermete": fermete,
            "housse": housse,
            "matiere_housse": matiere_housse,
            "poignees": poignees,
            "dimensions": {
                "largeur": 79.0,
                "longueur": 198.0,
                "hauteur": 20.0
            },
            "semaine_annee": "6_2025",
            "lundi": "2025-02-10",
            "vendredi": "2025-02-14",
            "commande_client": "75",
            "dimension_housse_longueur": 5.5,
            "dimension_housse": "4 x 91",
            "dimension_literie": "160x200",
            "decoupe_noyau": "79.0 x 198.0"
        }
        
        print(f"Configuration créée:")
        print(f"  - Noyau: {config['noyau']}")
        print(f"  - Fermeté: {config['fermete']}")
        print(f"  - Housse: {config['housse']}")
        print(f"  - Matière housse: {config['matiere_housse']}")
        print(f"  - Poignées: {config['poignees']}")
        
        # Test de création du pré-import
        print(f"\n--- Création pré-import ---")
        donnees_client = {
            "nom": "Mr DEVERSENNE CLAUDE",
            "adresse": "SAINT JANS CAPPEL",
            "code_client": "DEVECSA"
        }
        
        pre_import = creer_pre_import([config], donnees_client, False, ["ENLEVEMENT"])
        
        if pre_import:
            item = pre_import[0]
            print(f"Pré-import créé:")
            print(f"  - MR_Ferme_C37: '{item.get('MR_Ferme_C37', 'VIDE')}'")
            print(f"  - MR_Medium_C38: '{item.get('MR_Medium_C38', 'VIDE')}'")
            print(f"  - MR_Confort_C39: '{item.get('MR_Confort_C39', 'VIDE')}'")
            print(f"  - Hmat_luxe3D_C19: '{item.get('Hmat_luxe3D_C19', 'VIDE')}'")
            print(f"  - poignees_C20: '{item.get('poignees_C20', 'VIDE')}'")
            print(f"  - jumeaux_C10: '{item.get('jumeaux_C10', 'VIDE')}'")
            print(f"  - emporte_client_C57: '{item.get('emporte_client_C57', 'VIDE')}'")
            
            if item.get('MR_Ferme_C37') == 'X':
                print("\n✅ SUCCÈS: MR_Ferme_C37 est coché")
            else:
                print("\n❌ ÉCHEC: MR_Ferme_C37 n'est pas coché")
        else:
            print("❌ ÉCHEC: Aucun pré-import créé")
    
    print("\n=== Test terminé ===")

if __name__ == "__main__":
    test_deversenne_debug() 