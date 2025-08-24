"""
Configuration pytest pour les tests de l'application Matelas
"""

import pytest
import sys
import os
import tempfile
import shutil
from unittest.mock import Mock, patch

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(scope="function")
def temp_dir():
    """Fixture pour créer un répertoire temporaire pour les tests"""
    test_dir = tempfile.mkdtemp()
    yield test_dir
    # Nettoyage après le test
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)


@pytest.fixture(scope="function")
def temp_output_dir(temp_dir):
    """Fixture pour créer un répertoire de sortie temporaire"""
    output_dir = os.path.join(temp_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


@pytest.fixture(scope="function")
def sample_llm_data():
    """Fixture pour des données LLM de test standardisées"""
    return {
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


@pytest.fixture(scope="function")
def sample_configurations():
    """Fixture pour des configurations de matelas de test"""
    return [{
        "matelas_index": 1,
        "noyau": "LATEX NATUREL",
        "quantite": 1,
        "dimensions": {"largeur": 140, "longueur": 190},
        "hauteur": 20,
        "fermete": "Ferme",
        "housse": "Simple",
        "matiere_housse": "Polyester"
    }]


@pytest.fixture(scope="function")
def sample_client_data():
    """Fixture pour des données client de test"""
    return {
        "nom": "DUPONT Jean",
        "adresse": "Paris",
        "code_client": "DUP001"
    }


@pytest.fixture(scope="function")
def sample_pre_import_data():
    """Fixture pour des données de pré-import de test"""
    return [{
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


@pytest.fixture(scope="function")
def mock_excel_workbook():
    """Fixture pour mocker un workbook Excel"""
    with patch('openpyxl.load_workbook') as mock_load_workbook:
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
        yield mock_load_workbook


@pytest.fixture(scope="function")
def mock_llm_response(sample_llm_data):
    """Fixture pour mocker les réponses LLM"""
    import json
    with patch('backend_interface.backend_interface.call_llm') as mock_llm, \
         patch('backend_interface.backend_interface.call_openrouter') as mock_openrouter:
        
        mock_llm.return_value = json.dumps(sample_llm_data)
        mock_openrouter.return_value = json.dumps(sample_llm_data)
        
        yield {
            'llm': mock_llm,
            'openrouter': mock_openrouter
        }


@pytest.fixture(scope="function")
def test_pdf_file(temp_dir):
    """Fixture pour créer un fichier PDF de test"""
    test_pdf = os.path.join(temp_dir, "test.pdf")
    with open(test_pdf, 'w') as f:
        f.write("Test PDF content")
    return test_pdf


@pytest.fixture(scope="function")
def multiple_test_pdfs(temp_dir):
    """Fixture pour créer plusieurs fichiers PDF de test"""
    test_files = []
    for i in range(3):
        test_pdf = os.path.join(temp_dir, f"test_{i}.pdf")
        with open(test_pdf, 'w') as f:
            f.write(f"Test PDF content {i}")
        test_files.append(test_pdf)
    return test_files


# Configuration des marqueurs pytest
def pytest_configure(config):
    """Configuration des marqueurs pytest"""
    # Configuration pour les tests
    pytest.test_data_dir = os.path.join(os.path.dirname(__file__), "test_data")
    
    # Créer le répertoire de données de test s'il n'existe pas
    if not os.path.exists(pytest.test_data_dir):
        os.makedirs(pytest.test_data_dir, exist_ok=True)
    
    # Ajouter les marqueurs
    config.addinivalue_line(
        "markers", "unit: marque les tests unitaires"
    )
    config.addinivalue_line(
        "markers", "integration: marque les tests d'intégration"
    )
    config.addinivalue_line(
        "markers", "performance: marque les tests de performance"
    )
    config.addinivalue_line(
        "markers", "regression: marque les tests de régression"
    )
    config.addinivalue_line(
        "markers", "slow: marque les tests lents"
    )


# Configuration pour les tests asynchrones
@pytest.fixture(scope="function")
def event_loop():
    """Fixture pour les tests asynchrones"""
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# Configuration pour les tests de performance
@pytest.fixture(scope="function")
def performance_thresholds():
    """Fixture pour les seuils de performance"""
    return {
        "extraction_client": {"time": 2.0, "memory": 100},  # secondes, MB
        "detection_dimensions": {"time": 1.0, "memory": 50},
        "calcul_hauteur": {"time": 1.0, "memory": 50},
        "detection_fermete": {"time": 1.0, "memory": 50},
        "creation_pre_import": {"time": 10.0, "memory": 200},
        "validation_pre_import": {"time": 2.0, "memory": 100},
        "import_excel": {"time": 5.0, "memory": 150},
        "traitement_complet": {"time": 30.0, "memory": 300}
    }


# Configuration pour les tests de régression
@pytest.fixture(scope="function")
def regression_test_cases():
    """Fixture pour les cas de test de régression"""
    return {
        "extraction_client": [
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
            }
        ],
        "detection_dimensions": [
            {
                "input": "Matelas 140x190 cm",
                "expected": {"largeur": 140, "longueur": 190}
            }
        ],
        "calcul_hauteur": [
            {
                "input": "Matelas hauteur 20cm",
                "expected": 20
            }
        ],
        "detection_fermete": [
            {
                "input": "Matelas ferme",
                "expected": "Ferme"
            }
        ]
    }


# Configuration pour les tests d'intégration
@pytest.fixture(scope="function")
def integration_test_config():
    """Fixture pour la configuration des tests d'intégration"""
    return {
        "enrich_llm": True,
        "llm_provider": "ollama",
        "openrouter_api_key": None,
        "semaine_prod": 1,
        "annee_prod": 2024,
        "commande_client": ["Test Client"]
    } 