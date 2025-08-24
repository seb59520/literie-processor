#!/usr/bin/env python3
"""
Script de test pour vérifier la numérotation des cas dans les fichiers Excel
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from backend.excel_import_utils import ExcelMatelasImporter
from backend.excel_sommier_import_utils import ExcelSommierImporter

def test_matelas_numerotation():
    """Test de la numérotation des cas pour les matelas"""
    print("=== Test de numérotation des cas - Matelas ===")
    
    importer = ExcelMatelasImporter()
    
    # Configuration de test
    config_test = {
        "Client_D1": "Client Test",
        "Adresse_D3": "Adresse Test",
        "numero_D2": "12345",
        "semaine_D5": "S01",
        "lundi_D6": "2025-01-06",
        "vendredi_D7": "2025-01-10",
        "Hauteur_D22": "20",
        "dimension_housse_D23": "160x200",
        "longueur_D24": "200",
        "decoupe_noyau_D25": "Standard",
        "jumeaux_C10": True,
        "jumeaux_D10": True,
        "1piece_C11": False,
        "1piece_D11": False,
        "HSimple_polyester_C13": True,
        "HSimple_polyester_D13": True,
        "HSimple_tencel_C14": False,
        "HSimple_tencel_D14": False,
        "HSimple_autre_C15": False,
        "HSimple_autre_D15": False,
        "Hmat_polyester_C17": False,
        "Hmat_polyester_D17": False,
        "Hmat_tencel_C18": False,
        "Hmat_tencel_D18": False,
        "Hmat_luxe3D_C19": False,
        "Hmat_luxe3D_D19": False,
        "poignees_C20": True,
        "LN_Ferme_C28": True,
        "LN_Medium_C29": False,
        "LM7z_Ferme_C30": False,
        "LM7z_Medium_C31": False,
        "LM3z_Ferme_C32": False,
        "LM3z_Medium_C33": False,
        "MV_Ferme_C34": False,
        "MV_Medium_C35": False,
        "MV_Confort_C36": False,
        "MR_Ferme_C37": False,
        "MR_Medium_C38": False,
        "MR_Confort_C39": False,
        "SL43_Ferme_C40": False,
        "SL43_Medium_C41": False,
        "Surmatelas_C45": False,
        "emporte_client_C57": False,
        "fourgon_C58": False,
        "transporteur_C59": False,
    }
    
    # Créer plusieurs configurations pour tester la création de plusieurs fichiers
    configurations = [config_test.copy() for _ in range(15)]  # 15 configurations = 2 fichiers
    
    try:
        print(f"Génération de {len(configurations)} configurations matelas...")
        created_files = importer.import_configurations(configurations, "S01", "TEST")
        
        print(f"Fichiers créés: {created_files}")
        print("✅ Test matelas terminé avec succès")
        
        return created_files
        
    except Exception as e:
        print(f"❌ Erreur lors du test matelas: {e}")
        return []

def test_sommiers_numerotation():
    """Test de la numérotation des cas pour les sommiers"""
    print("\n=== Test de numérotation des cas - Sommiers ===")
    
    importer = ExcelSommierImporter()
    
    # Configuration de test pour sommier
    config_test = {
        "Client_D1": "Client Test",
        "Adresse_D3": "Adresse Test",
        "numero_D2": "12345",
        "semaine_D5": "S01",
        "lundi_D6": "2025-01-06",
        "vendredi_D7": "2025-01-10",
        "Type_Sommier_D20": "SOMMIER À LATTES",
        "Materiau_D25": "BOIS",
        "Hauteur_D30": "8",
        "Dimensions_D35": "160x200",
        "Quantite_D40": "2",
        "Sommier_DansUnLit_D45": False,
        "Sommier_Pieds_D50": True,
    }
    
    # Créer plusieurs configurations pour tester la création de plusieurs fichiers
    configurations = [config_test.copy() for _ in range(15)]  # 15 configurations = 2 fichiers
    
    try:
        print(f"Génération de {len(configurations)} configurations sommiers...")
        created_files = importer.import_configurations(configurations, "S01", "TEST")
        
        print(f"Fichiers créés: {created_files}")
        print("✅ Test sommiers terminé avec succès")
        
        return created_files
        
    except Exception as e:
        print(f"❌ Erreur lors du test sommiers: {e}")
        return []

def main():
    """Fonction principale de test"""
    print("🧪 Test de la numérotation des cas dans les fichiers Excel")
    print("=" * 60)
    
    # Test des matelas
    matelas_files = test_matelas_numerotation()
    
    # Test des sommiers
    sommier_files = test_sommiers_numerotation()
    
    print("\n" + "=" * 60)
    print("📊 Résumé des tests:")
    print(f"   - Fichiers matelas créés: {len(matelas_files)}")
    print(f"   - Fichiers sommiers créés: {len(sommier_files)}")
    
    if matelas_files or sommier_files:
        print("\n📝 Vérifiez manuellement les fichiers créés pour confirmer:")
        print("   - Fichier 1: cas 1 à 10")
        print("   - Fichier 2: cas 11 à 20")
        print("   - etc.")
    
    print("\n✅ Tests terminés!")

if __name__ == "__main__":
    main() 