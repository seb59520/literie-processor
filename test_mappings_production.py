#!/usr/bin/env python3
"""
Test du chargement des mappings en mode production
"""

import sys
import os

# Ajouter le backend au path
sys.path.append('backend')

def test_mappings_production():
    """Test du chargement des mappings en mode production"""
    print("=== TEST MAPPINGS PRODUCTION ===")
    print()
    
    try:
        from backend.mapping_manager import MappingManager
        from backend.asset_utils import get_config_path
        
        print("✅ MappingManager importé avec succès")
        print()
        
        # Test des chemins de configuration
        print("🔍 Test des chemins de configuration:")
        matelas_config = get_config_path("mappings_matelas.json")
        sommiers_config = get_config_path("mappings_sommiers.json")
        
        print(f"   mappings_matelas.json: {matelas_config}")
        print(f"   Existe: {os.path.exists(matelas_config) if matelas_config else False}")
        print(f"   mappings_sommiers.json: {sommiers_config}")
        print(f"   Existe: {os.path.exists(sommiers_config) if sommiers_config else False}")
        print()
        
        # Test du MappingManager
        print("🔍 Test du MappingManager:")
        mapping_manager = MappingManager()
        
        print(f"   matelas_mappings_file: {mapping_manager.matelas_mappings_file}")
        print(f"   sommiers_mappings_file: {mapping_manager.sommiers_mappings_file}")
        print()
        
        # Test du chargement des mappings
        print("🔍 Test du chargement des mappings:")
        matelas_mappings = mapping_manager.load_mappings("matelas")
        sommiers_mappings = mapping_manager.load_mappings("sommiers")
        
        print(f"   Mappings matelas chargés: {len(matelas_mappings)} entrées")
        print(f"   Mappings sommiers chargés: {len(sommiers_mappings)} entrées")
        print()
        
        # Afficher quelques mappings
        print("📋 Exemples de mappings matelas:")
        for i, (field, cell) in enumerate(list(matelas_mappings.items())[:5]):
            print(f"   {field} -> {cell}")
        print()
        
        print("📋 Exemples de mappings sommiers:")
        for i, (field, cell) in enumerate(list(sommiers_mappings.items())[:5]):
            print(f"   {field} -> {cell}")
        print()
        
        # Test de la fonction get_cell_for_field
        print("🔍 Test get_cell_for_field:")
        test_fields = ["Client_D1", "Adresse_D3", "numero_D2"]
        
        for field in test_fields:
            matelas_cell = mapping_manager.get_cell_for_field(field, "matelas")
            sommiers_cell = mapping_manager.get_cell_for_field(field, "sommiers")
            print(f"   {field}: matelas={matelas_cell}, sommiers={sommiers_cell}")
        print()
        
        # Test de validation
        print("🔍 Test de validation:")
        valid_cells = ["D1", "C10", "E25"]
        invalid_cells = ["", "ABC", "1D", "D"]
        
        for cell in valid_cells:
            is_valid = mapping_manager.validate_cell_format(cell)
            print(f"   {cell}: {'✅ Valide' if is_valid else '❌ Invalide'}")
        
        for cell in invalid_cells:
            is_valid = mapping_manager.validate_cell_format(cell)
            print(f"   '{cell}': {'✅ Valide' if is_valid else '❌ Invalide'}")
        print()
        
        print("✅ Test des mappings terminé avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_mappings_production()
    if success:
        print("\n🎉 Tous les tests sont passés !")
    else:
        print("\n💥 Des erreurs ont été détectées")
    
    input("\nAppuyez sur Entrée pour continuer...") 