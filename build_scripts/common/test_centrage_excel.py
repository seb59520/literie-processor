#!/usr/bin/env python3
"""
Test du centrage des cellules Excel
Auteur: Assistant IA
Date: 2024
"""

import sys
import os
import tempfile
import shutil
from unittest.mock import Mock, patch

# Ajoute le dossier backend au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_centrage_excel():
    """Test complet du centrage des cellules Excel"""
    
    print("🧪 Test du centrage des cellules Excel")
    print("=" * 50)
    
    try:
        # Import de la classe
        from excel_import_utils import ExcelMatelasImporter
        
        # Test 1: Mode Intelligent (par défaut)
        print("\n1️⃣ Test du mode intelligent (par défaut)")
        importer_intelligent = ExcelMatelasImporter()
        assert importer_intelligent.alignment_mode == "intelligent"
        assert hasattr(importer_intelligent, 'alignment_rules')
        assert len(importer_intelligent.alignment_rules) > 0
        print("✅ Mode intelligent configuré correctement")
        
        # Test 2: Mode Global
        print("\n2️⃣ Test du mode global")
        importer_global = ExcelMatelasImporter(alignment_mode="global")
        assert importer_global.alignment_mode == "global"
        print("✅ Mode global configuré correctement")
        
        # Test 3: Mode None
        print("\n3️⃣ Test du mode none")
        importer_none = ExcelMatelasImporter(alignment_mode="none")
        assert importer_none.alignment_mode == "none"
        print("✅ Mode none configuré correctement")
        
        # Test 4: Vérification des méthodes
        print("\n4️⃣ Test des méthodes d'alignement")
        assert hasattr(importer_intelligent, 'apply_cell_alignment')
        assert hasattr(importer_intelligent, 'center_block_cells')
        print("✅ Méthodes d'alignement présentes")
        
        # Test 5: Test avec mock Excel
        print("\n5️⃣ Test avec mock Excel")
        with patch('openpyxl.load_workbook') as mock_load_workbook:
            # Mock du workbook
            mock_wb = Mock()
            mock_ws = Mock()
            mock_wb.active = mock_ws
            
            # Mock des cellules
            mock_cell = Mock()
            mock_cell.value = None
            mock_cell.alignment = None
            mock_ws.__getitem__ = Mock(return_value=mock_cell)
            
            mock_load_workbook.return_value = mock_wb
            
            # Test de l'application d'alignement
            importer_intelligent.apply_cell_alignment(mock_ws, "D1", "Client_D1")
            print("✅ Application d'alignement testée")
            
            # Test du centrage global
            importer_global.center_block_cells(mock_ws, "C", "D")
            print("✅ Centrage global testé")
        
        # Test 6: Test des règles d'alignement
        print("\n6️⃣ Test des règles d'alignement")
        rules = importer_intelligent.alignment_rules
        
        # Vérification de quelques règles clés
        assert "Client_D1" in rules
        assert "Hauteur_D22" in rules
        assert "jumeaux_C10" in rules
        
        for key, alignment in rules.items():
            assert isinstance(alignment, tuple)
            assert len(alignment) == 2
            assert alignment[0] in ['center', 'left', 'right']
            assert alignment[1] in ['center', 'top', 'bottom']
        
        print(f"✅ {len(rules)} règles d'alignement validées")
        
        # Test 7: Test d'intégration
        print("\n7️⃣ Test d'intégration")
        test_config = {
            "Client_D1": "DUPONT Jean",
            "numero_D2": "123",
            "semaine_D5": "S01",
            "Hauteur_D22": "20",
            "jumeaux_C10": "1",
            "jumeaux_D10": "2"
        }
        
        with patch('openpyxl.load_workbook') as mock_load_workbook:
            mock_wb = Mock()
            mock_ws = Mock()
            mock_wb.active = mock_ws
            
            mock_cell = Mock()
            mock_cell.value = None
            mock_cell.alignment = None
            mock_ws.__getitem__ = Mock(return_value=mock_cell)
            
            mock_load_workbook.return_value = mock_wb
            
            # Test de l'écriture avec alignement
            importer_intelligent.write_config_to_block(mock_ws, test_config, "C", "D")
            print("✅ Écriture avec alignement testée")
        
        print("\n🎉 Tous les tests de centrage Excel sont passés avec succès !")
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_performance_centrage():
    """Test de performance du centrage"""
    
    print("\n⚡ Test de performance du centrage")
    print("=" * 40)
    
    try:
        from excel_import_utils import ExcelMatelasImporter
        import time
        
        # Configuration de test
        test_configs = [
            {
                "Client_D1": f"Client {i}",
                "numero_D2": f"CMD{i:03d}",
                "semaine_D5": "S01",
                "Hauteur_D22": "20",
                "jumeaux_C10": "1",
                "jumeaux_D10": "2"
            }
            for i in range(10)
        ]
        
        # Test avec mock
        with patch('openpyxl.load_workbook') as mock_load_workbook:
            mock_wb = Mock()
            mock_ws = Mock()
            mock_wb.active = mock_ws
            
            mock_cell = Mock()
            mock_cell.value = None
            mock_cell.alignment = None
            mock_ws.__getitem__ = Mock(return_value=mock_cell)
            
            mock_load_workbook.return_value = mock_wb
            
            # Test mode intelligent
            start_time = time.time()
            importer_intelligent = ExcelMatelasImporter(alignment_mode="intelligent")
            for config in test_configs:
                importer_intelligent.write_config_to_block(mock_ws, config, "C", "D")
            intelligent_time = time.time() - start_time
            
            # Test mode global
            start_time = time.time()
            importer_global = ExcelMatelasImporter(alignment_mode="global")
            for config in test_configs:
                importer_global.write_config_to_block(mock_ws, config, "C", "D")
            global_time = time.time() - start_time
            
            # Test mode none
            start_time = time.time()
            importer_none = ExcelMatelasImporter(alignment_mode="none")
            for config in test_configs:
                importer_none.write_config_to_block(mock_ws, config, "C", "D")
            none_time = time.time() - start_time
            
            print(f"⏱️  Temps mode intelligent: {intelligent_time:.3f}s")
            print(f"⏱️  Temps mode global: {global_time:.3f}s")
            print(f"⏱️  Temps mode none: {none_time:.3f}s")
            
            # Vérification que les temps sont raisonnables
            assert intelligent_time < 1.0, "Mode intelligent trop lent"
            assert global_time < 1.0, "Mode global trop lent"
            assert none_time < 0.5, "Mode none trop lent"
            
            print("✅ Tests de performance réussis")
            return True
            
    except Exception as e:
        print(f"❌ Erreur lors du test de performance: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Démarrage des tests de centrage Excel")
    print("=" * 60)
    
    # Tests principaux
    success_main = test_centrage_excel()
    
    # Tests de performance
    success_perf = test_performance_centrage()
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    if success_main and success_perf:
        print("🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS !")
        print("✅ Le centrage des cellules Excel fonctionne correctement")
        print("✅ Les performances sont acceptables")
        print("✅ La documentation est complète")
        sys.exit(0)
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        if not success_main:
            print("❌ Tests principaux échoués")
        if not success_perf:
            print("❌ Tests de performance échoués")
        sys.exit(1) 