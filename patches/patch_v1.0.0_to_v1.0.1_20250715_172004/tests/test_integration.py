"""
Tests d'intégration pour l'application Matelas
Utilisation: pytest tests/test_integration.py -v
"""

import pytest
import sys
import os
import json
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Imports des modules à tester
from backend_interface import backend_interface
from backend import pre_import_utils, excel_import_utils
from config import config


class TestIntegrationComplete:
    """Tests d'intégration complets pour le flux de traitement"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        # Créer un dossier temporaire pour les tests
        self.test_dir = tempfile.mkdtemp()
        self.output_dir = os.path.join(self.test_dir, "output")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Données de test
        self.test_llm_data = {
            "client": {
                "nom": "DUPONT Jean",
                "adresse": "123 Rue de la Paix, 75001 Paris",
                "code_client": "DUP001"
            },
            "commande": {
                "numero": "CMD001",
                "date": "2024-01-15",
                "commercial": "MARTIN"
            },
            "articles": [
                {
                    "quantite": 1,
                    "description": "Matelas latex naturel 140x190 ferme housse simple polyester",
                    "dimensions": "140x190",
                    "pu_ttc": 1200.0
                }
            ],
            "paiement": {
                "conditions": "30 jours",
                "total_ttc": 1200.0
            }
        }
    
    def teardown_method(self):
        """Nettoyage après chaque test"""
        # Supprimer le dossier temporaire
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    @patch('backend_interface.backend_interface.call_llm')
    @patch('backend_interface.backend_interface.call_openrouter')
    async def test_flux_complet_avec_llm(self, mock_openrouter, mock_llm):
        """Test du flux complet avec enrichissement LLM"""
        # Mock des réponses LLM
        mock_llm.return_value = json.dumps(self.test_llm_data)
        mock_openrouter.return_value = json.dumps(self.test_llm_data)
        
        # Créer un fichier PDF de test
        test_pdf = os.path.join(self.test_dir, "test.pdf")
        with open(test_pdf, 'w') as f:
            f.write("Test PDF content")
        
        # Paramètres de test
        files = [test_pdf]
        enrich_llm = True
        llm_provider = "ollama"
        openrouter_api_key = None
        semaine_prod = 1
        annee_prod = 2024
        commande_client = ["Test Client"]
        
        # Exécuter le traitement
        result = await backend_interface.process_pdf_files(
            files, enrich_llm, llm_provider, openrouter_api_key,
            semaine_prod, annee_prod, commande_client
        )
        
        # Vérifications
        assert result is not None
        assert "results" in result
        assert len(result["results"]) > 0
        
        # Vérifier que les résultats contiennent les données attendues
        first_result = result["results"][0]
        assert "configurations_matelas" in first_result
        assert "pre_import" in first_result
        assert "fichiers_excel" in first_result
    
    @patch('backend_interface.backend_interface.call_llm')
    @patch('backend_interface.backend_interface.call_openrouter')
    async def test_flux_complet_sans_llm(self, mock_openrouter, mock_llm):
        """Test du flux complet sans enrichissement LLM"""
        # Créer un fichier PDF de test
        test_pdf = os.path.join(self.test_dir, "test.pdf")
        with open(test_pdf, 'w') as f:
            f.write("Test PDF content")
        
        # Paramètres de test
        files = [test_pdf]
        enrich_llm = False
        llm_provider = "ollama"
        openrouter_api_key = None
        semaine_prod = 1
        annee_prod = 2024
        commande_client = ["Test Client"]
        
        # Exécuter le traitement
        result = await backend_interface.process_pdf_files(
            files, enrich_llm, llm_provider, openrouter_api_key,
            semaine_prod, annee_prod, commande_client
        )
        
        # Vérifications
        assert result is not None
        assert "results" in result
        assert len(result["results"]) > 0
    
    def test_integration_pre_import_excel(self):
        """Test d'intégration entre pré-import et Excel"""
        # Créer des configurations de test
        configurations = [{
            "matelas_index": 1,
            "noyau": "LATEX NATUREL",
            "quantite": 1,
            "dimensions": {"largeur": 140, "longueur": 190},
            "hauteur": 20,
            "fermete": "Ferme",
            "housse": "Simple",
            "matiere_housse": "Polyester"
        }]
        
        donnees_client = {
            "nom": "DUPONT Jean",
            "adresse": "Paris",
            "code_client": "DUP001"
        }
        
        # Créer le pré-import
        pre_import = pre_import_utils.creer_pre_import(
            configurations, donnees_client, False, []
        )
        
        # Vérifier que le pré-import est valide
        assert pre_import_utils.valider_pre_import(pre_import)
        
        # Tester l'export Excel
        with patch('openpyxl.load_workbook') as mock_load_workbook:
            mock_wb = Mock()
            mock_ws = Mock()
            mock_wb.active = mock_ws
            mock_ws.cell.return_value.value = None
            mock_load_workbook.return_value = mock_wb
            
            importer = excel_import_utils.ExcelMatelasImporter()
            resultat = importer.import_configurations(pre_import, "S01", "TEST")
            
            assert isinstance(resultat, list)
            assert len(resultat) > 0
    
    def test_integration_multiples_fichiers(self):
        """Test d'intégration avec plusieurs fichiers"""
        # Créer plusieurs fichiers de test
        test_files = []
        for i in range(3):
            test_pdf = os.path.join(self.test_dir, f"test_{i}.pdf")
            with open(test_pdf, 'w') as f:
                f.write(f"Test PDF content {i}")
            test_files.append(test_pdf)
        
        # Simuler le traitement de plusieurs fichiers
        results = []
        for i, file_path in enumerate(test_files):
            # Simuler les données LLM pour chaque fichier
            llm_data = {
                "client": {
                    "nom": f"CLIENT_{i}",
                    "adresse": f"VILLE_{i}",
                    "code_client": f"CODE_{i}"
                },
                "articles": [
                    {
                        "quantite": 1,
                        "description": f"Matelas test {i}",
                        "dimensions": "140x190"
                    }
                ]
            }
            
            # Créer les configurations
            configurations = [{
                "matelas_index": 1,
                "noyau": "LATEX NATUREL",
                "quantite": 1,
                "dimensions": {"largeur": 140, "longueur": 190},
                "hauteur": 20,
                "fermete": "Ferme",
                "housse": "Simple",
                "matiere_housse": "Polyester"
            }]
            
            # Créer le pré-import
            donnees_client = {
                "nom": llm_data["client"]["nom"],
                "adresse": llm_data["client"]["adresse"],
                "code_client": llm_data["client"]["code_client"]
            }
            
            pre_import = pre_import_utils.creer_pre_import(
                configurations, donnees_client, False, []
            )
            
            results.append({
                "filename": os.path.basename(file_path),
                "configurations_matelas": configurations,
                "pre_import": pre_import,
                "fichiers_excel": []
            })
        
        # Vérifications
        assert len(results) == 3
        for result in results:
            assert "configurations_matelas" in result
            assert "pre_import" in result
            assert len(result["configurations_matelas"]) > 0
            assert len(result["pre_import"]) > 0


class TestIntegrationErreurs:
    """Tests d'intégration pour la gestion d'erreurs"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.test_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Nettoyage après chaque test"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    @patch('backend_interface.backend_interface.call_llm')
    async def test_erreur_llm(self, mock_llm):
        """Test de gestion d'erreur LLM"""
        # Mock d'une erreur LLM
        mock_llm.side_effect = Exception("Erreur LLM")
        
        # Créer un fichier de test
        test_pdf = os.path.join(self.test_dir, "test.pdf")
        with open(test_pdf, 'w') as f:
            f.write("Test PDF content")
        
        # Paramètres de test
        files = [test_pdf]
        enrich_llm = True
        llm_provider = "ollama"
        openrouter_api_key = None
        semaine_prod = 1
        annee_prod = 2024
        commande_client = ["Test Client"]
        
        # Le traitement doit continuer malgré l'erreur LLM
        result = await backend_interface.process_pdf_files(
            files, enrich_llm, llm_provider, openrouter_api_key,
            semaine_prod, annee_prod, commande_client
        )
        
        # Vérifier que le traitement s'est terminé
        assert result is not None
        assert "results" in result
    
    def test_erreur_fichier_inexistant(self):
        """Test de gestion d'erreur fichier inexistant"""
        # Essayer de traiter un fichier qui n'existe pas
        files = ["fichier_inexistant.pdf"]
        
        # Le traitement doit gérer cette erreur gracieusement
        # (Ce test vérifie que l'application ne plante pas)
        assert True  # Placeholder pour le test
    
    def test_erreur_configuration_invalide(self):
        """Test de gestion d'erreur configuration invalide"""
        # Configuration invalide
        configurations = [{
            "matelas_index": 1,
            # Données manquantes
        }]
        
        donnees_client = {
            "nom": "",
            "adresse": "",
            "code_client": ""
        }
        
        # Le pré-import doit être créé même avec des données invalides
        pre_import = pre_import_utils.creer_pre_import(
            configurations, donnees_client, False, []
        )
        
        # Vérifier que le pré-import est créé mais peut être invalide
        assert isinstance(pre_import, list)
        assert len(pre_import) > 0


class TestIntegrationPerformance:
    """Tests d'intégration pour les performances"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.test_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Nettoyage après chaque test"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_performance_grand_volume(self):
        """Test de performance avec un grand volume de données"""
        # Créer un grand nombre de configurations
        configurations = []
        for i in range(100):
            configurations.append({
                "matelas_index": i + 1,
                "noyau": "LATEX NATUREL",
                "quantite": 1,
                "dimensions": {"largeur": 140, "longueur": 190},
                "hauteur": 20,
                "fermete": "Ferme",
                "housse": "Simple",
                "matiere_housse": "Polyester"
            })
        
        donnees_client = {
            "nom": "CLIENT_TEST",
            "adresse": "VILLE_TEST",
            "code_client": "CODE_TEST"
        }
        
        # Mesurer le temps de création du pré-import
        import time
        start_time = time.time()
        
        pre_import = pre_import_utils.creer_pre_import(
            configurations, donnees_client, False, []
        )
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Vérifications
        assert len(pre_import) == 100
        assert processing_time < 5.0  # Doit prendre moins de 5 secondes
    
    def test_performance_excel_import(self):
        """Test de performance de l'import Excel"""
        # Créer beaucoup de données de pré-import
        pre_import_data = []
        for i in range(50):
            pre_import_data.append({
                "Client_D1": f"CLIENT_{i}",
                "numero_D2": f"CMD_{i}",
                "semaine_D5": "1_2024",
                "Hauteur_D22": 20,
                "noyau": "LATEX NATUREL",
                "quantite": 1
            })
        
        # Mesurer le temps d'import Excel
        import time
        start_time = time.time()
        
        with patch('openpyxl.load_workbook') as mock_load_workbook:
            mock_wb = Mock()
            mock_ws = Mock()
            mock_wb.active = mock_ws
            mock_ws.cell.return_value.value = None
            mock_load_workbook.return_value = mock_wb
            
            importer = excel_import_utils.ExcelMatelasImporter()
            resultat = importer.import_configurations(pre_import_data, "S01", "TEST")
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Vérifications
        assert len(resultat) > 0
        assert processing_time < 3.0  # Doit prendre moins de 3 secondes


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 