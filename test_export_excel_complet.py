#!/usr/bin/env python3
"""
Test complet de l'export Excel avec la correction du pré-import
"""

import sys
import os
import json

# Ajouter le répertoire backend au path
sys.path.append('backend')

from pre_import_utils import creer_pre_import, valider_pre_import
from excel_import_utils import ExcelMatelasImporter

def test_export_excel_complet():
    """Test complet de l'export Excel"""
    
    print("=== TEST EXPORT EXCEL COMPLET ===")
    
    # 1. Créer des données de test
    print("\n📋 Étape 1: Création des données de test")
    
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
            "commande_client": "GALOO",
            "dimension_housse": "79x198",
            "dimension_housse_longueur": "198",
            "decoupe_noyau": "Standard"
        }
    ]
    
    donnees_client = {
        "nom": "Mr et Mme GALOO PASCAL & SANDRINE",
        "adresse": "OXELAERE",
        "code_client": "GALOPOX",
        "titre": "Mr et Mme"
    }
    
    print(f"✅ Configurations matelas: {len(configurations_matelas)}")
    print(f"✅ Données client: {donnees_client['nom']}")
    
    # 2. Créer le pré-import
    print("\n📋 Étape 2: Création du pré-import")
    
    try:
        pre_import_data = creer_pre_import(configurations_matelas, donnees_client, False, [], False)
        print(f"✅ Pré-import créé: {len(pre_import_data)} éléments")
        
        if pre_import_data:
            # Validation
            validation = valider_pre_import(pre_import_data)
            print(f"✅ Validation: {validation}")
            
            # Afficher la structure
            print(f"📋 Structure du pré-import:")
            for key, value in pre_import_data[0].items():
                if key.startswith(('Client_', 'numero_', 'semaine_', 'Hauteur_', 'jumeaux_', 'Hmat_')):
                    print(f"  {key}: {value}")
        else:
            print("❌ Pré-import vide - impossible de continuer")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la création du pré-import: {e}")
        return False
    
    # 3. Test de l'export Excel
    print("\n📋 Étape 3: Test de l'export Excel")
    
    try:
        # Créer l'importateur Excel
        importer = ExcelMatelasImporter()
        print("✅ Importateur Excel créé")
        
        # Paramètres d'export
        semaine_excel = "S25"
        id_fichier = "2025"
        
        print(f"📋 Paramètres d'export: Semaine {semaine_excel}, ID {id_fichier}")
        
        # Exporter
        fichiers_crees = importer.import_configurations(pre_import_data, semaine_excel, id_fichier)
        print(f"✅ Export Excel terminé: {len(fichiers_crees)} fichier(s) créé(s)")
        
        # Vérifier les fichiers
        for fichier in fichiers_crees:
            if os.path.exists(fichier):
                print(f"✅ Fichier créé: {fichier}")
                # Afficher la taille
                taille = os.path.getsize(fichier)
                print(f"  📏 Taille: {taille} octets")
            else:
                print(f"❌ Fichier manquant: {fichier}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'export Excel: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_export_excel_avec_erreurs():
    """Test de l'export Excel avec des données problématiques"""
    
    print("\n=== TEST EXPORT EXCEL AVEC ERREURS ===")
    
    # Test avec données None
    print("\n📋 Test avec données None")
    try:
        pre_import_data = creer_pre_import(None, {}, False, [], False)
        print(f"✅ Pré-import avec None retourne: {len(pre_import_data)} éléments")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
    
    # Test avec données vides
    print("\n📋 Test avec données vides")
    try:
        pre_import_data = creer_pre_import([], {}, False, [], False)
        print(f"✅ Pré-import avec listes vides retourne: {len(pre_import_data)} éléments")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
    
    # Test avec données invalides
    print("\n📋 Test avec données invalides")
    try:
        pre_import_data = creer_pre_import([None], {"nom": "Test"}, False, [], False)
        print(f"✅ Pré-import avec config None retourne: {len(pre_import_data)} éléments")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")

if __name__ == "__main__":
    print("🚀 Démarrage des tests d'export Excel")
    
    # Test principal
    success = test_export_excel_complet()
    
    # Test avec erreurs
    test_export_excel_avec_erreurs()
    
    if success:
        print("\n🎉 Tous les tests sont passés avec succès !")
        print("✅ L'export Excel fonctionne maintenant correctement")
    else:
        print("\n❌ Certains tests ont échoué")
        print("🔧 Vérifiez les erreurs ci-dessus")
    
    print("\n=== FIN DES TESTS ===")

