#!/usr/bin/env python3
"""
Test pour vérifier que les champs manquants sont bien générés pour TENCEL LUXE 3D
"""

import sys
import os
sys.path.append('backend')

from pre_import_utils import creer_pre_import

def test_champs_manquants_tencel_luxe3d():
    """Test des champs manquants pour TENCEL LUXE 3D"""
    
    print("🧪 Test des champs manquants pour TENCEL LUXE 3D")
    print("=" * 60)
    
    # Configuration de test avec votre description exacte
    config_test = {
        "matelas_index": 1,
        "noyau": "MOUSSE RAINUREE 7 ZONES",
        "quantite": 1,
        "hauteur": 9,
        "fermete": "FERME",
        "housse": "MATELASSEE",
        "matiere_housse": "TENCEL LUXE 3D",
        "poignees": "NON",  # Règle spéciale TENCEL LUXE 3D
        "dimensions": {
            "largeur": 89,
            "longueur": 198,
            "hauteur": 20
        },
        "semaine_annee": "12_2025",
        "lundi": "2025-03-24",
        "vendredi": "2025-03-28",
        "commande_client": "TEST001",
        "dimension_housse": "2 x 101",  # Calculé via référentiel
        "dimension_housse_longueur": 5.5,  # Calculé via référentiel
        "decoupe_noyau": "89.0 x 198.0"  # Selon fermeté FERME
    }
    
    donnees_client = {
        "nom": "Mr TEST CLIENT",
        "adresse": "Adresse Test",
        "code_client": "TEST"
    }
    
    print("📋 Configuration de test:")
    print(f"  - Noyau: {config_test['noyau']}")
    print(f"  - Fermeté: {config_test['fermete']}")
    print(f"  - Housse: {config_test['housse']}")
    print(f"  - Matière housse: {config_test['matiere_housse']}")
    print(f"  - Poignées: {config_test['poignees']}")
    print(f"  - Dimensions housse: {config_test['dimension_housse']}")
    print(f"  - Longueur housse: {config_test['dimension_housse_longueur']}")
    print()
    
    try:
        # Créer le pré-import
        pre_import = creer_pre_import([config_test], donnees_client)
        
        if pre_import:
            item = pre_import[0]
            
            print("✅ Pré-import créé avec succès")
            print()
            
            # Vérifier les champs manquants
            print("🔍 Vérification des champs manquants:")
            print("-" * 40)
            
            # Champs C19 et D19 (TENCEL LUXE 3D)
            c19_value = item.get('Hmat_luxe3D_C19', 'VIDE')
            d19_value = item.get('Hmat_luxe3D_D19', 'VIDE')
            print(f"  - Hmat_luxe3D_C19: '{c19_value}' (attendu: 'X')")
            print(f"  - Hmat_luxe3D_D19: '{d19_value}' (attendu: '89 x 198')")
            
            # Champs dimensions housse
            dim_housse = item.get('dimension_housse_D23', 'VIDE')
            print(f"  - dimension_housse_D23: '{dim_housse}' (attendu: '2 x 101')")
            
            # Champs longueur housse
            longueur_housse = item.get('longueur_D24', 'VIDE')
            print(f"  - longueur_D24: '{longueur_housse}' (attendu: '5.5')")
            
            # Champs poignées
            poignees = item.get('poignees_C20', 'VIDE')
            print(f"  - poignees_C20: '{poignees}' (attendu: '')")
            
            # Champs noyau
            mr_ferme = item.get('MR_Ferme_C37', 'VIDE')
            print(f"  - MR_Ferme_C37: '{mr_ferme}' (attendu: 'X')")
            
            print()
            
            # Validation des résultats
            print("📊 Validation des résultats:")
            print("-" * 30)
            
            success_count = 0
            total_tests = 6
            
            if c19_value == 'X':
                print("✅ Hmat_luxe3D_C19: CORRECT")
                success_count += 1
            else:
                print("❌ Hmat_luxe3D_C19: INCORRECT")
            
            if d19_value == '89 x 198':
                print("✅ Hmat_luxe3D_D19: CORRECT")
                success_count += 1
            else:
                print("❌ Hmat_luxe3D_D19: INCORRECT")
            
            if dim_housse == '2 x 101':
                print("✅ dimension_housse_D23: CORRECT")
                success_count += 1
            else:
                print("❌ dimension_housse_D23: INCORRECT")
            
            if longueur_housse == 5.5:
                print("✅ longueur_D24: CORRECT")
                success_count += 1
            else:
                print("❌ longueur_D24: INCORRECT")
            
            if poignees == '':
                print("✅ poignees_C20: CORRECT (vide car règle TENCEL LUXE 3D)")
                success_count += 1
            else:
                print("❌ poignees_C20: INCORRECT")
            
            if mr_ferme == 'X':
                print("✅ MR_Ferme_C37: CORRECT")
                success_count += 1
            else:
                print("❌ MR_Ferme_C37: INCORRECT")
            
            print()
            print(f"🎯 Résultat: {success_count}/{total_tests} tests réussis")
            
            if success_count == total_tests:
                print("🎉 TOUS LES TESTS RÉUSSIS ! Les champs manquants sont bien générés.")
                return True
            else:
                print("⚠️  Certains tests ont échoué. Vérifiez la génération des champs.")
                return False
                
        else:
            print("❌ ÉCHEC: Aucun pré-import créé")
            return False
            
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        return False

if __name__ == "__main__":
    test_champs_manquants_tencel_luxe3d() 