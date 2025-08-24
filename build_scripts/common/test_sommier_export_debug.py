#!/usr/bin/env python3
"""
Test de diagnostic pour l'export Excel des sommiers
"""

import sys
import os
sys.path.append('backend')

from backend_interface import BackendInterface
from excel_sommier_import_utils import ExcelSommierImporter

def test_export_sommier_simple():
    """Test d'export simple d'un sommier"""
    print("=== Test export sommier simple ===")
    
    # Données de test
    pre_import_sommier = {
        # Données client
        "Client_D1": "Test Client",
        "Adresse_D3": "123 Rue Test",
        "numero_D2": "0123456789",
        
        # Champs commande et dates
        "semaine_D5": "S01_2025",
        "lundi_D6": "2025-01-06",
        "vendredi_D7": "2025-01-10",
        
        # Données sommier
        "Type_Sommier_D20": "SOMMIER À LATTES",
        "Materiau_D25": "BOIS",
        "Hauteur_D30": "8",
        "Dimensions_D35": "160x200",
        "Quantite_D40": "1",
        "Sommier_DansUnLit_D45": "OUI",
        "Sommier_Pieds_D50": "NON",
        
        # Données de production
        "semaine_annee": "S01_2025",
        "lundi": "2025-01-06",
        "vendredi": "2025-01-10",
        "commande_client": "Test Client",
        
        # Type d'article
        "type_article": "sommier",
        "sommier_index": 1
    }
    
    print("Données de pré-import:")
    for key, value in pre_import_sommier.items():
        print(f"  {key}: {value}")
    
    # Test de l'export
    try:
        importer = ExcelSommierImporter()
        fichiers = importer.import_configurations([pre_import_sommier], "S01", "2025")
        print(f"\n✅ Export réussi: {fichiers}")
        
        # Vérifier si le fichier existe et n'est pas vide
        if fichiers:
            fichier_path = fichiers[0]
            if os.path.exists(fichier_path):
                taille = os.path.getsize(fichier_path)
                print(f"📁 Fichier créé: {fichier_path} (taille: {taille} octets)")
                
                if taille > 1000:  # Plus de 1KB
                    print("✅ Fichier semble correct (taille > 1KB)")
                else:
                    print("⚠️  Fichier semble vide ou trop petit")
            else:
                print("❌ Fichier non trouvé")
        else:
            print("❌ Aucun fichier créé")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'export: {e}")
        import traceback
        traceback.print_exc()

def test_backend_interface_sommier():
    """Test de l'interface backend avec des sommiers"""
    print("\n=== Test interface backend sommier ===")
    
    # Simulation d'une configuration sommier
    config_sommier = {
        "sommier_index": 1,
        "type_sommier": "SOMMIER À LATTES",
        "quantite": 1,
        "hauteur": 8,
        "materiau": "BOIS",
        "dimensions": {"largeur": 160, "longueur": 200},
        "semaine_annee": "S01_2025",
        "lundi": "2025-01-06",
        "vendredi": "2025-01-10",
        "commande_client": "Test Client",
        "sommier_dansunlit": "OUI",
        "sommier_pieds": "NON"
    }
    
    donnees_client = {
        "nom": "Test Client",
        "adresse": "123 Rue Test",
        "telephone": "0123456789"
    }
    
    # Test de création du pré-import
    try:
        backend = BackendInterface()
        pre_import = backend._creer_pre_import_sommiers([config_sommier], donnees_client, False, [])
        
        print("Pré-import créé:")
        for item in pre_import:
            for key, value in item.items():
                print(f"  {key}: {value}")
        
        # Test de l'export global
        fichiers = backend._export_excel_global(pre_import, 1, 2025)
        print(f"\nExport global: {fichiers}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

def test_template_sommier():
    """Test du template sommier"""
    print("\n=== Test template sommier ===")
    
    template_path = "template/template_sommier.xlsx"
    
    if os.path.exists(template_path):
        print(f"✅ Template trouvé: {template_path}")
        
        try:
            import openpyxl
            wb = openpyxl.load_workbook(template_path)
            ws = wb.active
            
            print(f"📊 Feuille active: {ws.title}")
            print(f"📏 Dimensions: {ws.dimensions}")
            
            # Vérifier quelques cellules clés
            cellules_test = ["A1", "C1", "D1", "E1", "F1"]
            for cellule in cellules_test:
                valeur = ws[cellule].value
                print(f"  {cellule}: {valeur}")
            
            wb.close()
            
        except Exception as e:
            print(f"❌ Erreur lecture template: {e}")
    else:
        print(f"❌ Template non trouvé: {template_path}")

if __name__ == "__main__":
    print("Diagnostic export Excel des sommiers")
    print("=" * 50)
    
    test_template_sommier()
    test_export_sommier_simple()
    test_backend_interface_sommier()
    
    print("\n✅ Diagnostic terminé!") 