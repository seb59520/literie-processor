#!/usr/bin/env python3
"""
Test complet pour la commande Deversenne
"""

import sys
import os
sys.path.append('backend')

from backend_interface import traiter_fichier_pdf

def test_deversenne_complet():
    """Test complet du traitement de la commande Deversenne"""
    
    fichier_pdf = "Commandes/Commandes deversenne.pdf"
    
    print("=== Test complet Deversenne ===")
    
    try:
        resultat = traiter_fichier_pdf(fichier_pdf)
        
        if resultat and resultat.get("status") == "success":
            print("✅ Traitement réussi")
            
            pre_import = resultat.get("pre_import", [])
            if pre_import:
                config = pre_import[0]
                
                print(f"\n--- Configuration détectée ---")
                print(f"Noyau: {resultat.get('configurations_matelas', [{}])[0].get('noyau', 'N/A')}")
                print(f"Fermeté: {resultat.get('configurations_matelas', [{}])[0].get('fermete', 'N/A')}")
                print(f"Quantité: {resultat.get('configurations_matelas', [{}])[0].get('quantite', 'N/A')}")
                
                print(f"\n--- Cases cochées ---")
                print(f"MR_Ferme_C37: '{config.get('MR_Ferme_C37', 'VIDE')}'")
                print(f"MR_Medium_C38: '{config.get('MR_Medium_C38', 'VIDE')}'")
                print(f"MR_Confort_C39: '{config.get('MR_Confort_C39', 'VIDE')}'")
                print(f"Hmat_luxe3D_C19: '{config.get('Hmat_luxe3D_C19', 'VIDE')}'")
                print(f"poignees_C20: '{config.get('poignees_C20', 'VIDE')}'")
                print(f"jumeaux_C10: '{config.get('jumeaux_C10', 'VIDE')}'")
                print(f"emporte_client_C57: '{config.get('emporte_client_C57', 'VIDE')}'")
                
                if config.get('MR_Ferme_C37') == 'X':
                    print("\n✅ SUCCÈS: MR_Ferme_C37 est correctement coché")
                else:
                    print("\n❌ ÉCHEC: MR_Ferme_C37 n'est pas coché")
                    
            else:
                print("❌ ÉCHEC: Aucun pré-import généré")
        else:
            print(f"❌ ÉCHEC: Traitement échoué - {resultat}")
            
    except Exception as e:
        print(f"❌ ERREUR: {e}")
    
    print("\n=== Test terminé ===")

if __name__ == "__main__":
    test_deversenne_complet() 