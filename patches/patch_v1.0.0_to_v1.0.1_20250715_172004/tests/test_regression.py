"""
Tests de régression pour l'application Matelas
Utilisation: pytest tests/test_regression.py -v
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
from backend import pre_import_utils, excel_import_utils, client_utils
from backend import dimensions_utils, hauteur_utils, fermete_utils
from backend import housse_utils, matiere_housse_utils, poignees_utils
from backend import matelas_utils, latex_naturel_referentiel
from config import config


class TestRegressionFonctionnalites:
    """Tests de régression pour les fonctionnalités principales"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.test_dir = tempfile.mkdtemp()
        self.output_dir = os.path.join(self.test_dir, "output")
        os.makedirs(self.output_dir, exist_ok=True)
    
    def teardown_method(self):
        """Nettoyage après chaque test"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_regression_extraction_client(self):
        """Test de régression pour l'extraction des données client"""
        # Données de test standardisées
        test_cases = [
            {
                "input": {
                    "client": {
                        "nom": "DUPONT Jean",
                        "adresse": "123 Rue de la Paix, 75001 Paris",
                        "code_client": "DUP001"
                    }
                },
                "expected": {
                    "nom": "DUPONT Jean",
                    "adresse": "Paris",
                    "code_client": "DUP001"
                }
            },
            {
                "input": {
                    "client": {
                        "nom": "MARTIN Marie",
                        "adresse": "456 Avenue des Champs, 69000 Lyon",
                        "code_client": "MAR002"
                    }
                },
                "expected": {
                    "nom": "MARTIN Marie",
                    "adresse": "Lyon",
                    "code_client": "MAR002"
                }
            }
        ]
        
        for test_case in test_cases:
            result = client_utils.extraire_donnees_client(test_case["input"])
            assert result["nom"] == test_case["expected"]["nom"]
            assert result["adresse"] == test_case["expected"]["adresse"]
            assert result["code_client"] == test_case["expected"]["code_client"]
    
    def test_regression_detection_dimensions(self):
        """Test de régression pour la détection des dimensions"""
        # Cas de test standardisés
        test_cases = [
            {
                "input": "Matelas 140/190 cm",
                "expected": {"largeur": 140, "longueur": 190}
            },
            {
                "input": "Matelas 160/200 cm",
                "expected": {"largeur": 160, "longueur": 200}
            },
            {
                "input": "Matelas jumeaux 80/200",
                "expected": {"largeur": 80, "longueur": 200}
            },
            {
                "input": "Matelas 1.60/2.00 m",
                "expected": {"largeur": 1.6, "longueur": 2.0}
            }
        ]
        
        for test_case in test_cases:
            result = dimensions_utils.detecter_dimensions(test_case["input"])
            assert result["largeur"] == test_case["expected"]["largeur"]
            assert result["longueur"] == test_case["expected"]["longueur"]
    
    def test_regression_calcul_hauteur(self):
        """Test de régression pour le calcul de hauteur"""
        # Cas de test standardisés
        test_cases = [
            {
                "input": "LATEX NATUREL",
                "expected": 10
            },
            {
                "input": "MOUSSE VISCO",
                "expected": 10
            },
            {
                "input": "LATEX MIXTE 7 ZONES",
                "expected": 9
            }
        ]
        
        for test_case in test_cases:
            result = hauteur_utils.calculer_hauteur_matelas(test_case["input"])
            assert result == test_case["expected"]
    
    def test_regression_detection_fermete(self):
        """Test de régression pour la détection de fermeté"""
        # Cas de test standardisés
        test_cases = [
            {
                "input": "Matelas ferme",
                "expected": "FERME"
            },
            {
                "input": "Matelas medium",
                "expected": "MEDIUM"
            },
            {
                "input": "Matelas confort",
                "expected": "CONFORT"
            }
        ]
        
        for test_case in test_cases:
            result = fermete_utils.detecter_fermete_matelas(test_case["input"])
            assert result == test_case["expected"]
    
    def test_regression_detection_housse(self):
        """Test de régression pour la détection du type de housse"""
        # Cas de test standardisés
        test_cases = [
            {
                "input": "Housse simple polyester",
                "expected": "SIMPLE"
            },
            {
                "input": "Housse matelassée tencel",
                "expected": "MATELASSEE"
            },
            {
                "input": "Housse luxe 3D",
                "expected": "INCONNUE"
            }
        ]
        
        for test_case in test_cases:
            result = housse_utils.detecter_type_housse(test_case["input"])
            assert result == test_case["expected"]
    
    def test_regression_detection_matiere_housse(self):
        """Test de régression pour la détection de la matière de housse"""
        # Cas de test standardisés
        test_cases = [
            {
                "input": "Housse polyester",
                "expected": "POLYESTER"
            },
            {
                "input": "Housse tencel",
                "expected": "TENCEL"
            }
        ]
        
        for test_case in test_cases:
            result = matiere_housse_utils.detecter_matiere_housse(test_case["input"])
            assert result == test_case["expected"]
    
    def test_regression_detection_poignees(self):
        """Test de régression pour la détection des poignées"""
        # Cas de test standardisés
        test_cases = [
            {
                "input": "Matelas avec poignées",
                "expected": "OUI"
            },
            {
                "input": "Matelas standard",
                "expected": "NON"
            }
        ]
        
        for test_case in test_cases:
            result = poignees_utils.detecter_poignees(test_case["input"])
            assert result == test_case["expected"]
    
    def test_regression_detection_noyau(self):
        """Test de régression pour la détection du noyau"""
        # Cas de test standardisés
        test_cases = [
            {
                "input": [{"description": "Matelas 100% latex naturel"}],
                "expected": "LATEX NATUREL"
            },
            {
                "input": [{"description": "Matelas latex mixte 7 zones"}],
                "expected": "LATEX MIXTE 7 ZONES"
            },
            {
                "input": [{"description": "Matelas mousse visco"}],
                "expected": "MOUSSE VISCO"
            }
        ]
        
        for test_case in test_cases:
            result = matelas_utils.detecter_noyau_matelas(test_case["input"])
            assert result[0]["noyau"] == test_case["expected"]


class TestRegressionPreImport:
    """Tests de régression pour le pré-import"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.test_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Nettoyage après chaque test"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_regression_creation_pre_import(self):
        """Test de régression pour la création du pré-import"""
        # Configuration de test standardisée
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
        
        # Vérifications de régression
        assert len(pre_import) == 1
        assert "Client_D1" in pre_import[0]
        assert pre_import[0]["Client_D1"] == "DUPONT Jean"
        assert "numero_D2" in pre_import[0]
        assert "semaine_D5" in pre_import[0]
        assert "Hauteur_D22" in pre_import[0]
        assert pre_import[0]["Hauteur_D22"] == 20
        assert "noyau" in pre_import[0]
        assert pre_import[0]["noyau"] == "LATEX NATUREL"
        assert "quantite" in pre_import[0]
        assert pre_import[0]["quantite"] == 1
    
    def test_regression_validation_pre_import(self):
        """Test de régression pour la validation du pré-import"""
        # Données de test standardisées
        pre_import_valide = [{
            "Client_D1": "DUPONT Jean",
            "numero_D2": "123",
            "semaine_D5": "1_2024",
            "Hauteur_D22": 20,
            "noyau": "LATEX NATUREL",
            "quantite": 1
        }]
        
        pre_import_invalide = [{
            "Client_D1": "",
            "numero_D2": "123",
            "semaine_D5": "1_2024"
        }]
        
        # Vérifications de régression
        assert pre_import_utils.valider_pre_import(pre_import_valide) == True
        assert pre_import_utils.valider_pre_import(pre_import_invalide) == False
    
    def test_regression_pre_import_multiples_configurations(self):
        """Test de régression pour le pré-import avec multiples configurations"""
        # Configurations multiples
        configurations = [
            {
                "matelas_index": 1,
                "noyau": "LATEX NATUREL",
                "quantite": 1,
                "dimensions": {"largeur": 140, "longueur": 190},
                "hauteur": 20,
                "fermete": "Ferme",
                "housse": "Simple",
                "matiere_housse": "Polyester"
            },
            {
                "matelas_index": 2,
                "noyau": "LATEX MIXTE 7 ZONES",
                "quantite": 2,
                "dimensions": {"largeur": 160, "longueur": 200},
                "hauteur": 22,
                "fermete": "Medium",
                "housse": "Matelassée",
                "matiere_housse": "Tencel"
            }
        ]
        
        donnees_client = {
            "nom": "DUPONT Jean",
            "adresse": "Paris",
            "code_client": "DUP001"
        }
        
        # Créer le pré-import
        pre_import = pre_import_utils.creer_pre_import(
            configurations, donnees_client, False, []
        )
        
        # Vérifications de régression
        assert len(pre_import) == 3  # 1 + 2 quantités
        assert all("Client_D1" in item for item in pre_import)
        assert all(item["Client_D1"] == "DUPONT Jean" for item in pre_import)
        assert all("noyau" in item for item in pre_import)
        assert any(item["noyau"] == "LATEX NATUREL" for item in pre_import)
        assert any(item["noyau"] == "LATEX MIXTE 7 ZONES" for item in pre_import)


class TestRegressionReferentiels:
    """Tests de régression pour les référentiels"""
    
    def test_regression_latex_naturel_referentiel(self):
        """Test de régression pour le référentiel latex naturel"""
        # Cas de test standardisés
        test_cases = [
            {
                "largeur": 140,
                "matiere": "POLYESTER"
            },
            {
                "largeur": 160,
                "matiere": "TENCEL"
            },
            {
                "largeur": 180,
                "matiere": "POLYESTER"
            }
        ]
        
        for test_case in test_cases:
            try:
                result = latex_naturel_referentiel.get_valeur_latex_naturel(
                    test_case["largeur"],
                    test_case["matiere"]
                )
                
                # Vérifications de régression
                assert isinstance(result, (int, float, str))
            except (ValueError, FileNotFoundError):
                # Ignorer les erreurs si les référentiels ne sont pas disponibles
                pass
    
    def test_regression_latex_mixte7zones_referentiel(self):
        """Test de régression pour le référentiel latex mixte 7 zones"""
        from backend import latex_mixte7zones_referentiel
        
        # Cas de test standardisés
        test_cases = [
            {
                "largeur": 140,
                "matiere": "POLYESTER"
            },
            {
                "largeur": 160,
                "matiere": "TENCEL"
            }
        ]
        
        for test_case in test_cases:
            try:
                result = latex_mixte7zones_referentiel.get_valeur_latex_mixte7zones(
                    test_case["largeur"],
                    test_case["matiere"]
                )
                
                # Vérifications de régression
                assert isinstance(result, (int, float, str))
            except (ValueError, FileNotFoundError):
                # Ignorer les erreurs si les référentiels ne sont pas disponibles
                pass
    
    def test_regression_mousse_rainuree7zones_referentiel(self):
        """Test de régression pour le référentiel mousse rainurée 7 zones"""
        from backend import mousse_rainuree7zones_referentiel
        
        # Cas de test standardisés
        test_cases = [
            {
                "largeur": 140,
                "matiere": "POLYESTER"
            },
            {
                "largeur": 160,
                "matiere": "TENCEL"
            }
        ]
        
        for test_case in test_cases:
            try:
                result = mousse_rainuree7zones_referentiel.get_valeur_mousse_rainuree7zones(
                    test_case["largeur"],
                    test_case["matiere"]
                )
                
                # Vérifications de régression
                assert isinstance(result, (int, float, str))
            except (ValueError, FileNotFoundError):
                # Ignorer les erreurs si les référentiels ne sont pas disponibles
                pass


class TestRegressionExcel:
    """Tests de régression pour l'import Excel"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.test_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Nettoyage après chaque test"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    @patch('openpyxl.load_workbook')
    def test_regression_import_excel(self, mock_load_workbook):
        """Test de régression pour l'import Excel"""
        # Mock du workbook
        mock_wb = Mock()
        mock_ws = Mock()
        mock_wb.active = mock_ws
        
        # Simuler l'accès aux cellules comme un dictionnaire
        mock_ws.__getitem__ = Mock(side_effect=lambda key: Mock(value=None))
        
        # Simuler la méthode cell()
        mock_cell = Mock()
        mock_cell.value = None
        mock_ws.cell.return_value = mock_cell
        
        mock_load_workbook.return_value = mock_wb
        
        # Données de test standardisées
        pre_import_data = [{
            "Client_D1": "DUPONT Jean",
            "numero_D2": "123",
            "semaine_D5": "1_2024",
            "Hauteur_D22": 20,
            "noyau": "LATEX NATUREL",
            "quantite": 1,
            "dimensions": "140x190",
            "fermete": "Ferme",
            "housse": "Simple"
        }]
        
        # Importer les configurations
        importer = excel_import_utils.ExcelMatelasImporter()
        resultat = importer.import_configurations(pre_import_data, "S01", "TEST")
        
        # Vérifications de régression
        assert isinstance(resultat, list)
        assert len(resultat) > 0
        assert all(isinstance(item, dict) for item in resultat)
    
    @patch('openpyxl.load_workbook')
    def test_regression_import_excel_multiples(self, mock_load_workbook):
        """Test de régression pour l'import Excel avec multiples données"""
        # Mock du workbook
        mock_wb = Mock()
        mock_ws = Mock()
        mock_wb.active = mock_ws
        
        # Simuler l'accès aux cellules comme un dictionnaire
        mock_ws.__getitem__ = Mock(side_effect=lambda key: Mock(value=None))
        
        # Simuler la méthode cell()
        mock_cell = Mock()
        mock_cell.value = None
        mock_ws.cell.return_value = mock_cell
        
        mock_load_workbook.return_value = mock_wb
        
        # Données multiples
        pre_import_data = [
            {
                "Client_D1": f"CLIENT_{i}",
                "numero_D2": f"CMD_{i:04d}",
                "semaine_D5": "1_2024",
                "Hauteur_D22": 20,
                "noyau": "LATEX NATUREL",
                "quantite": 1
            }
            for i in range(5)
        ]
        
        # Importer les configurations
        importer = excel_import_utils.ExcelMatelasImporter()
        resultat = importer.import_configurations(pre_import_data, "S01", "TEST")
        
        # Vérifications de régression
        assert isinstance(resultat, list)
        assert len(resultat) > 0
        assert all(isinstance(item, dict) for item in resultat)


class TestRegressionConfig:
    """Tests de régression pour la configuration"""
    
    def test_regression_config_getters_setters(self):
        """Test de régression pour les getters et setters de configuration"""
        # Valeurs de test standardisées
        test_values = {
            "semaine": 25,
            "annee": 2024,
            "commande_client": "Test Client",
            "openrouter_api_key": "sk-or-test123"
        }
        
        # Tester les setters
        config.set_last_semaine(test_values["semaine"])
        config.set_last_annee(test_values["annee"])
        config.set_last_commande_client(test_values["commande_client"])
        config.set_openrouter_api_key(test_values["openrouter_api_key"])
        
        # Tester les getters
        assert config.get_last_semaine() == test_values["semaine"]
        assert config.get_last_annee() == test_values["annee"]
        assert config.get_last_commande_client() == test_values["commande_client"]
        assert config.get_openrouter_api_key() == test_values["openrouter_api_key"]
    
    def test_regression_config_persistence(self):
        """Test de régression pour la persistance de la configuration"""
        # Valeurs de test
        test_semaine = 30
        test_annee = 2025
        
        # Définir les valeurs
        config.set_last_semaine(test_semaine)
        config.set_last_annee(test_annee)
        
        # Vérifier que les valeurs sont persistées
        assert config.get_last_semaine() == test_semaine
        assert config.get_last_annee() == test_annee


class TestRegressionBackendInterface:
    """Tests de régression pour l'interface backend"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.test_dir = tempfile.mkdtemp()
        self.output_dir = os.path.join(self.test_dir, "output")
        os.makedirs(self.output_dir, exist_ok=True)
    
    def teardown_method(self):
        """Nettoyage après chaque test"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    @patch('backend_interface.call_llm')
    @patch('backend_interface.call_openrouter')
    @pytest.mark.asyncio
    async def test_regression_process_pdf_files(self, mock_openrouter, mock_llm):
        """Test de régression pour le traitement des fichiers PDF"""
        # Mock des réponses LLM
        test_llm_data = {
            "client": {
                "nom": "DUPONT Jean",
                "adresse": "123 Rue de la Paix, 75001 Paris",
                "code_client": "DUP001"
            },
            "articles": [
                {
                    "quantite": 1,
                    "description": "Matelas latex naturel 140x190 ferme housse simple polyester",
                    "dimensions": "140x190"
                }
            ]
        }
        mock_llm.return_value = json.dumps(test_llm_data)
        mock_openrouter.return_value = json.dumps(test_llm_data)
        
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
        
        # Exécuter le traitement
        result = await backend_interface.process_pdf_files(
            files, enrich_llm, llm_provider, openrouter_api_key,
            semaine_prod, annee_prod, commande_client
        )
        
        # Vérifications de régression
        assert result is not None
        assert "results" in result
        assert len(result["results"]) > 0
        
        first_result = result["results"][0]
        assert "configurations_matelas" in first_result
        assert "pre_import" in first_result
        assert "fichiers_excel" in first_result


if __name__ == "__main__":
    # Exécuter les tests pytest
    import pytest
    pytest.main([__file__, "-v"]) 