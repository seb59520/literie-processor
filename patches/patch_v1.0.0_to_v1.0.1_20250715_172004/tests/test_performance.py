"""
Tests de performance pour l'application Matelas
Utilisation: pytest tests/test_performance.py -v
"""

import pytest
import sys
import os
import json
import tempfile
import shutil
import time
import psutil
import asyncio
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Imports des modules à tester
from backend_interface import backend_interface
from backend import pre_import_utils, excel_import_utils, client_utils
from backend import dimensions_utils, hauteur_utils, fermete_utils
from config import config


class TestPerformanceTraitement:
    """Tests de performance pour le traitement des données"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.test_dir = tempfile.mkdtemp()
        self.output_dir = os.path.join(self.test_dir, "output")
        os.makedirs(self.output_dir, exist_ok=True)
    
    def teardown_method(self):
        """Nettoyage après chaque test"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_performance_extraction_client(self):
        """Test de performance de l'extraction des données client"""
        # Créer un grand nombre de données LLM
        llm_data_list = []
        for i in range(1000):
            llm_data = {
                "client": {
                    "nom": f"CLIENT_{i}",
                    "adresse": f"123 Rue Test, 75001 VILLE_{i}",
                    "code_client": f"CODE_{i:04d}"
                }
            }
            llm_data_list.append(llm_data)
        
        # Mesurer le temps d'extraction
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        for llm_data in llm_data_list:
            client_utils.extraire_donnees_client(llm_data)
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        processing_time = end_time - start_time
        memory_used = end_memory - start_memory
        
        # Vérifications de performance
        assert processing_time < 2.0  # Moins de 2 secondes pour 1000 extractions
        assert memory_used < 100  # Moins de 100 MB de mémoire utilisée
        
        print(f"Performance extraction client: {processing_time:.3f}s, {memory_used:.1f}MB")
    
    def test_performance_detection_dimensions(self):
        """Test de performance de la détection des dimensions"""
        # Créer un grand nombre de descriptions
        descriptions = []
        for i in range(1000):
            descriptions.append(f"Matelas {140 + i % 20}x{190 + i % 10} cm")
        
        # Mesurer le temps de détection
        start_time = time.time()
        
        for description in descriptions:
            dimensions_utils.detecter_dimensions(description)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Vérifications de performance
        assert processing_time < 1.0  # Moins d'1 seconde pour 1000 détections
        
        print(f"Performance détection dimensions: {processing_time:.3f}s")
    
    def test_performance_calcul_hauteur(self):
        """Test de performance du calcul de hauteur"""
        # Créer un grand nombre de descriptions
        descriptions = []
        for i in range(1000):
            descriptions.append(f"Matelas hauteur {18 + i % 5}cm")
        
        # Mesurer le temps de calcul
        start_time = time.time()
        
        for description in descriptions:
            hauteur_utils.calculer_hauteur_matelas(description)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Vérifications de performance
        assert processing_time < 1.0  # Moins d'1 seconde pour 1000 calculs
        
        print(f"Performance calcul hauteur: {processing_time:.3f}s")
    
    def test_performance_detection_fermete(self):
        """Test de performance de la détection de fermeté"""
        # Créer un grand nombre de descriptions
        descriptions = []
        fermetes = ["ferme", "medium", "confort"]
        for i in range(1000):
            descriptions.append(f"Matelas {fermetes[i % 3]}")
        
        # Mesurer le temps de détection
        start_time = time.time()
        
        for description in descriptions:
            fermete_utils.detecter_fermete_matelas(description)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Vérifications de performance
        assert processing_time < 1.0  # Moins d'1 seconde pour 1000 détections
        
        print(f"Performance détection fermeté: {processing_time:.3f}s")


class TestPerformancePreImport:
    """Tests de performance pour le pré-import"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.test_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Nettoyage après chaque test"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_performance_creation_pre_import(self):
        """Test de performance de la création du pré-import"""
        # Créer un grand nombre de configurations
        configurations = []
        for i in range(500):
            configurations.append({
                "matelas_index": i + 1,
                "noyau": "LATEX NATUREL",
                "quantite": 1 + (i % 3),
                "dimensions": {"largeur": 140 + (i % 20), "longueur": 190 + (i % 10)},
                "hauteur": 18 + (i % 5),
                "fermete": ["Ferme", "Medium", "Confort"][i % 3],
                "housse": ["Simple", "Matelassée", "Luxe 3D"][i % 3],
                "matiere_housse": ["Polyester", "Tencel"][i % 2]
            })
        
        donnees_client = {
            "nom": "CLIENT_TEST",
            "adresse": "VILLE_TEST",
            "code_client": "CODE_TEST"
        }
        
        # Mesurer le temps de création
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        pre_import = pre_import_utils.creer_pre_import(
            configurations, donnees_client, False, []
        )
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        processing_time = end_time - start_time
        memory_used = end_memory - start_memory
        
        # Vérifications de performance
        assert len(pre_import) == 500
        assert processing_time < 10.0  # Moins de 10 secondes pour 500 configurations
        assert memory_used < 200  # Moins de 200 MB de mémoire utilisée
        
        print(f"Performance création pré-import: {processing_time:.3f}s, {memory_used:.1f}MB")
    
    def test_performance_validation_pre_import(self):
        """Test de performance de la validation du pré-import"""
        # Créer un grand nombre de données de pré-import
        pre_import_data = []
        for i in range(1000):
            pre_import_data.append({
                "Client_D1": f"CLIENT_{i}",
                "numero_D2": f"CMD_{i:04d}",
                "semaine_D5": f"{1 + i % 52}_{2024}",
                "Hauteur_D22": 18 + (i % 5),
                "noyau": "LATEX NATUREL",
                "quantite": 1 + (i % 3)
            })
        
        # Mesurer le temps de validation
        start_time = time.time()
        
        is_valid = pre_import_utils.valider_pre_import(pre_import_data)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Vérifications de performance
        assert processing_time < 2.0  # Moins de 2 secondes pour 1000 validations
        
        print(f"Performance validation pré-import: {processing_time:.3f}s")


class TestPerformanceExcel:
    """Tests de performance pour l'import Excel"""
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.test_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Nettoyage après chaque test"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    @patch('openpyxl.load_workbook')
    def test_performance_import_excel(self, mock_load_workbook):
        """Test de performance de l'import Excel"""
        # Mock du workbook
        mock_wb = Mock()
        mock_ws = Mock()
        mock_wb.active = mock_ws
        mock_ws.cell.return_value.value = None  # Cellules vides
        mock_load_workbook.return_value = mock_wb
        
        # Créer un grand nombre de données de pré-import
        pre_import_data = []
        for i in range(200):
            pre_import_data.append({
                "Client_D1": f"CLIENT_{i}",
                "numero_D2": f"CMD_{i:04d}",
                "semaine_D5": f"{1 + i % 52}_{2024}",
                "Hauteur_D22": 18 + (i % 5),
                "noyau": "LATEX NATUREL",
                "quantite": 1 + (i % 3),
                "dimensions": f"{140 + i % 20}x{190 + i % 10}",
                "fermete": ["Ferme", "Medium", "Confort"][i % 3],
                "housse": ["Simple", "Matelassée", "Luxe 3D"][i % 3]
            })
        
        # Mesurer le temps d'import
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        importer = excel_import_utils.ExcelMatelasImporter()
        resultat = importer.import_configurations(pre_import_data, "S01", "TEST")
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        processing_time = end_time - start_time
        memory_used = end_memory - start_memory
        
        # Vérifications de performance
        assert len(resultat) > 0
        assert processing_time < 5.0  # Moins de 5 secondes pour 200 configurations
        assert memory_used < 150  # Moins de 150 MB de mémoire utilisée
        
        print(f"Performance import Excel: {processing_time:.3f}s, {memory_used:.1f}MB")


class TestPerformanceBackend:
    """Tests de performance pour le backend complet"""
    
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
    async def test_performance_traitement_complet(self, mock_openrouter, mock_llm):
        """Test de performance du traitement complet"""
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
        
        # Créer plusieurs fichiers de test
        test_files = []
        for i in range(10):
            test_pdf = os.path.join(self.test_dir, f"test_{i}.pdf")
            with open(test_pdf, 'w') as f:
                f.write(f"Test PDF content {i}")
            test_files.append(test_pdf)
        
        # Paramètres de test
        files = test_files
        enrich_llm = True
        llm_provider = "ollama"
        openrouter_api_key = None
        semaine_prod = 1
        annee_prod = 2024
        commande_client = ["Test Client"] * len(files)
        
        # Mesurer le temps de traitement
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        result = await backend_interface.process_pdf_files(
            files, enrich_llm, llm_provider, openrouter_api_key,
            semaine_prod, annee_prod, commande_client
        )
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        processing_time = end_time - start_time
        memory_used = end_memory - start_memory
        
        # Vérifications de performance
        assert result is not None
        assert "results" in result
        assert len(result["results"]) == 10
        assert processing_time < 30.0  # Moins de 30 secondes pour 10 fichiers
        assert memory_used < 300  # Moins de 300 MB de mémoire utilisée
        
        print(f"Performance traitement complet: {processing_time:.3f}s, {memory_used:.1f}MB")

    def test_performance_memoire_referentiels(self):
        """Test de performance mémoire pour les référentiels"""
        from backend import latex_naturel_referentiel, latex_mixte7zones_referentiel
        
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        # Effectuer de nombreuses consultations de référentiels
        matieres = ["LUXE 3D", "TENCEL", "POLYESTER"]
        for i in range(1000):
            largeur = 140 + (i % 20)
            matiere = matieres[i % 3]
            
            try:
                latex_naturel_referentiel.get_valeur_latex_naturel(
                    largeur, matiere
                )
            except (ValueError, FileNotFoundError):
                # Ignorer les erreurs si les référentiels ne sont pas disponibles
                pass
            
            try:
                latex_mixte7zones_referentiel.get_valeur_latex_mixte7zones(
                    largeur, 190, "Ferme"
                )
            except (ValueError, FileNotFoundError):
                # Ignorer les erreurs si les référentiels ne sont pas disponibles
                pass
        
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        memory_used = end_memory - start_memory
        
        # Vérifications de performance mémoire
        assert memory_used < 100  # Moins de 100 MB de mémoire utilisée
        
        print(f"Performance mémoire référentiels: {memory_used:.1f}MB")


if __name__ == "__main__":
    # Exécuter les tests pytest
    import pytest
    pytest.main([__file__, "-v"]) 