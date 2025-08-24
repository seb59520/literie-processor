"""
Tests unitaires pour l'application Matelas
Utilisation: pytest tests/test_unitaires.py -v
"""

import pytest
import sys
import os
import json
import tempfile
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Imports des modules à tester
from backend import client_utils, dimensions_utils, hauteur_utils, fermete_utils
from backend import housse_utils, matiere_housse_utils, poignees_utils
from backend import matelas_utils, latex_naturel_referentiel, latex_mixte7zones_referentiel
from backend import mousse_rainuree7zones_referentiel, select43_utils
from backend import latex_renforce_utils, mousse_visco_utils
from backend import decoupe_noyau_utils, pre_import_utils
from backend import excel_import_utils
from config import config


class TestClientUtils:
    """Tests unitaires pour client_utils"""
    
    def test_extraire_ville_adresse(self):
        """Test de l'extraction de ville depuis une adresse"""
        from backend.client_utils import extraire_ville_adresse
        
        # Test avec adresse complète
        adresse = "123 Rue de la Paix, 75001 Paris"
        ville = extraire_ville_adresse(adresse)
        assert ville == "Paris"
        
        # Test avec adresse simple
        adresse = "456 Avenue des Champs, 69000 Lyon"
        ville = extraire_ville_adresse(adresse)
        assert ville == "Lyon"
        
        # Test avec adresse sans code postal (retourne l'adresse complète)
        adresse = "789 Boulevard Central, Marseille"
        ville = extraire_ville_adresse(adresse)
        assert ville == "789 Boulevard Central, Marseille"
    
    def test_extraire_donnees_client(self):
        """Test de l'extraction des données client"""
        llm_data = {
            "client": {
                "nom": "DUPONT Jean",
                "adresse": "123 Rue de la Paix, 75001 Paris",
                "code_client": "DUP001"
            }
        }
        
        resultat = client_utils.extraire_donnees_client(llm_data)
        
        assert resultat["nom"] == "DUPONT Jean"
        assert resultat["adresse"] == "Paris"
        assert resultat["code_client"] == "DUP001"
    
    def test_valider_donnees_client(self):
        """Test de la validation des données client"""
        # Données valides
        donnees_valides = {
            "nom": "DUPONT Jean",
            "adresse": "Paris",
            "code_client": "DUP001"
        }
        assert client_utils.valider_donnees_client(donnees_valides) == True
        
        # Données invalides
        donnees_invalides = {
            "nom": "",
            "adresse": "Paris",
            "code_client": "DUP001"
        }
        assert client_utils.valider_donnees_client(donnees_invalides) == False


class TestDimensionsUtils:
    """Tests unitaires pour dimensions_utils"""
    
    def test_detecter_dimensions(self):
        """Test de la détection des dimensions"""
        # Test avec dimensions standard (format avec /)
        description = "Matelas 140/190 cm"
        dimensions = dimensions_utils.detecter_dimensions(description)
        assert dimensions["largeur"] == 140
        assert dimensions["longueur"] == 190
        
        # Test avec dimensions en mètres (format avec /)
        description = "Matelas 1.60/2.00 m"
        dimensions = dimensions_utils.detecter_dimensions(description)
        assert dimensions["largeur"] == 1.6
        assert dimensions["longueur"] == 2.0
        
        # Test avec dimensions jumeaux
        description = "Matelas jumeaux 80/200"
        dimensions = dimensions_utils.detecter_dimensions(description)
        assert dimensions["largeur"] == 80
        assert dimensions["longueur"] == 200


class TestHauteurUtils:
    """Tests unitaires pour hauteur_utils"""
    
    def test_calculer_hauteur_matelas(self):
        """Test du calcul de hauteur"""
        # Test avec noyau latex naturel
        hauteur = hauteur_utils.calculer_hauteur_matelas("LATEX NATUREL")
        assert hauteur == 10
        
        # Test avec noyau mousse visco
        hauteur = hauteur_utils.calculer_hauteur_matelas("MOUSSE VISCO")
        assert hauteur == 10
        
        # Test avec noyau inconnu
        hauteur = hauteur_utils.calculer_hauteur_matelas("NOYAU INCONNU")
        assert hauteur == 0


class TestFermeteUtils:
    """Tests unitaires pour fermete_utils"""
    
    def test_detecter_fermete_matelas(self):
        """Test de la détection de fermeté"""
        # Test ferme
        description = "Matelas ferme"
        fermete = fermete_utils.detecter_fermete_matelas(description)
        assert fermete == "FERME"
        
        # Test medium
        description = "Matelas medium"
        fermete = fermete_utils.detecter_fermete_matelas(description)
        assert fermete == "MEDIUM"
        
        # Test confort
        description = "Matelas confort"
        fermete = fermete_utils.detecter_fermete_matelas(description)
        assert fermete == "CONFORT"


class TestHousseUtils:
    """Tests unitaires pour housse_utils"""
    
    def test_detecter_type_housse(self):
        """Test de la détection du type de housse"""
        # Test housse simple
        description = "Housse simple polyester"
        type_housse = housse_utils.detecter_type_housse(description)
        assert type_housse == "SIMPLE"
        
        # Test housse matelassée
        description = "Housse matelassée tencel"
        type_housse = housse_utils.detecter_type_housse(description)
        assert type_housse == "MATELASSEE"
        
        # Test housse inconnue
        description = "Housse luxe 3D"
        type_housse = housse_utils.detecter_type_housse(description)
        assert type_housse == "INCONNUE"


class TestMatiereHousseUtils:
    """Tests unitaires pour matiere_housse_utils"""
    
    def test_detecter_matiere_housse(self):
        """Test de la détection de la matière de housse"""
        # Test polyester
        description = "Housse polyester"
        matiere = matiere_housse_utils.detecter_matiere_housse(description)
        assert matiere == "POLYESTER"
        
        # Test tencel
        description = "Housse tencel"
        matiere = matiere_housse_utils.detecter_matiere_housse(description)
        assert matiere == "TENCEL"


class TestPoigneesUtils:
    """Tests unitaires pour poignees_utils"""
    
    def test_detecter_poignees(self):
        """Test de la détection des poignées"""
        # Test avec poignées
        description = "Matelas avec poignées"
        poignees = poignees_utils.detecter_poignees(description)
        assert poignees == "OUI"
        
        # Test sans poignées
        description = "Matelas standard"
        poignees = poignees_utils.detecter_poignees(description)
        assert poignees == "NON"


class TestMatelasUtils:
    """Tests unitaires pour matelas_utils"""
    
    def test_detecter_noyau_matelas(self):
        """Test de la détection du noyau de matelas"""
        # Test latex naturel
        matelas = [{"description": "Matelas 100% latex naturel"}]
        resultat = matelas_utils.detecter_noyau_matelas(matelas)
        assert resultat[0]["noyau"] == "LATEX NATUREL"
        
        # Test latex mixte 7 zones
        matelas = [{"description": "Matelas latex mixte 7 zones"}]
        resultat = matelas_utils.detecter_noyau_matelas(matelas)
        assert resultat[0]["noyau"] == "LATEX MIXTE 7 ZONES"
        
        # Test mousse visco
        matelas = [{"description": "Matelas mousse visco"}]
        resultat = matelas_utils.detecter_noyau_matelas(matelas)
        assert resultat[0]["noyau"] == "MOUSSE VISCO"


class TestReferentiels:
    """Tests unitaires pour les référentiels"""
    
    def test_latex_naturel_referentiel(self):
        """Test du référentiel latex naturel"""
        # Test avec paramètres valides
        try:
            resultat = latex_naturel_referentiel.get_valeur_latex_naturel(
                largeur=140, matiere="POLYESTER"
            )
            assert isinstance(resultat, (int, float, str))
        except (ValueError, FileNotFoundError):
            # Ignorer les erreurs si les référentiels ne sont pas disponibles
            pass
    
    def test_latex_mixte7zones_referentiel(self):
        """Test du référentiel latex mixte 7 zones"""
        try:
            resultat = latex_mixte7zones_referentiel.get_valeur_latex_mixte7zones(
                largeur=140, matiere="POLYESTER"
            )
            assert isinstance(resultat, (int, float, str))
        except (ValueError, FileNotFoundError):
            # Ignorer les erreurs si les référentiels ne sont pas disponibles
            pass
    
    def test_mousse_rainuree7zones_referentiel(self):
        """Test du référentiel mousse rainurée 7 zones"""
        try:
            resultat = mousse_rainuree7zones_referentiel.get_valeur_mousse_rainuree7zones(
                largeur=140, matiere="POLYESTER"
            )
            assert isinstance(resultat, (int, float, str))
        except (ValueError, FileNotFoundError):
            # Ignorer les erreurs si les référentiels ne sont pas disponibles
            pass


class TestDecoupeNoyauUtils:
    """Tests unitaires pour decoupe_noyau_utils"""
    
    def test_calcul_decoupe_noyau(self):
        """Test du calcul de découpe du noyau"""
        # Test avec dimensions standard
        largeur_corr, longueur_corr = decoupe_noyau_utils.calcul_decoupe_noyau(
            "LATEX NATUREL", "FERME", 140, 190
        )
        assert isinstance(largeur_corr, int)
        assert isinstance(longueur_corr, int)
        
        # Test avec dimensions jumeaux
        largeur_corr, longueur_corr = decoupe_noyau_utils.calcul_decoupe_noyau(
            "LATEX NATUREL", "MEDIUM", 80, 200
        )
        assert isinstance(largeur_corr, int)
        assert isinstance(longueur_corr, int)


class TestPreImportUtils:
    """Tests unitaires pour pre_import_utils"""
    
    def test_creer_pre_import(self):
        """Test de la création du pré-import"""
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
        
        pre_import = pre_import_utils.creer_pre_import(
            configurations, donnees_client, False, []
        )
        
        assert isinstance(pre_import, list)
        assert len(pre_import) > 0
        assert "Client_D1" in pre_import[0]
    
    def test_valider_pre_import(self):
        """Test de la validation du pré-import"""
        # Test avec pré-import complet
        pre_import_valide = [{
            "Client_D1": "DUPONT Jean",
            "Adresse_D3": "123 Rue de la Paix, 75001 Paris",
            "numero_D2": "123",
            "semaine_D5": "1_2024",
            "lundi_D6": "Lundi",
            "vendredi_D7": "Vendredi",
            "Hauteur_D22": 20,
            "dosseret_tete_C8": "",
            "jumeaux_C10": "",
            "jumeaux_D10": "",
            "1piece_C11": "",
            "1piece_D11": "",
            "HSimple_polyester_C13": "",
            "HSimple_tencel_C14": "",
            "HSimple_autre_C15": "",
            "Hmat_polyester_C17": "",
            "Hmat_tencel_C18": "",
            "Hmat_luxe3D_C19": "",
            "poignees_C20": "",
            "dimension_housse_D23": "",
            "longueur_D24": "",
            "decoupe_noyau_D25": "",
            "LN_Ferme_C28": "",
            "LN_Medium_C29": "",
            "LM7z_Ferme_C30": "",
            "LM7z_Medium_C31": "",
            "LM3z_Ferme_C32": "",
            "LM3z_Medium_C33": "",
            "MV_Ferme_C34": "",
            "MV_Medium_C35": "",
            "MV_Confort_C36": "",
            "MR_Ferme_C37": "",
            "MR_Medium_C38": "",
            "MR_Confort_C39": "",
            "SL43_Ferme_C40": "",
            "SL43_Medium_C41": "",
            "Surmatelas_C45": "",
            "emporte_client_C57": "",
            "fourgon_C58": "",
            "transporteur_C59": ""
        }]
        
        assert pre_import_utils.valider_pre_import(pre_import_valide) == True
        
        # Test avec pré-import vide
        assert pre_import_utils.valider_pre_import([]) == False
        
        # Test avec pré-import incomplet
        pre_import_invalide = [{
            "Client_D1": "",
            "numero_D2": "123"
        }]
        
        assert pre_import_utils.valider_pre_import(pre_import_invalide) == False


class TestExcelImportUtils:
    """Tests unitaires pour excel_import_utils"""
    
    def test_excel_importer_creation(self):
        """Test de la création de l'importateur Excel"""
        importer = excel_import_utils.ExcelMatelasImporter()
        assert importer is not None
        assert hasattr(importer, 'template_path')
        assert hasattr(importer, 'max_cases_per_file')
    
    @patch('openpyxl.load_workbook')
    def test_import_configurations(self, mock_load_workbook):
        """Test de l'import de configurations"""
        # Mock du workbook
        mock_wb = Mock()
        mock_ws = Mock()
        mock_wb.active = mock_ws
        mock_ws.cell.return_value.value = None  # Cellules vides
        mock_load_workbook.return_value = mock_wb
        
        importer = excel_import_utils.ExcelMatelasImporter()
        
        configurations = [{
            "Client_D1": "Test Client",
            "numero_D2": "123",
            "semaine_D5": "1_2024"
        }]
        
        resultat = importer.import_configurations(configurations, "S01", "TEST")
        
        assert isinstance(resultat, list)
        assert len(resultat) > 0


class TestConfig:
    """Tests unitaires pour config"""
    
    def test_config_getters_setters(self):
        """Test des getters et setters de configuration"""
        # Test semaine
        config.set_last_semaine(25)
        assert config.get_last_semaine() == 25
        
        # Test année
        config.set_last_annee(2024)
        assert config.get_last_annee() == 2024
        
        # Test commande client
        config.set_last_commande_client("Test Client")
        assert config.get_last_commande_client() == "Test Client"
        
        # Test clé API OpenRouter
        config.set_openrouter_api_key("sk-or-test123")
        assert config.get_openrouter_api_key() == "sk-or-test123"


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 