# Système de Tests Automatisés - Application Matelas

## 📋 Vue d'ensemble

Ce document décrit le système complet de tests automatisés pour l'application Matelas de LITERIE WESTEYLYNCK. Le système comprend des tests unitaires, d'intégration, de performance et de régression.

## 🏗️ Architecture des Tests

```
tests/
├── __init__.py                 # Package de tests
├── conftest.py                 # Configuration pytest et fixtures
├── test_unitaires.py           # Tests unitaires complets
├── test_integration.py         # Tests d'intégration
├── test_performance.py         # Tests de performance
├── test_regression.py          # Tests de régression
├── run_all_tests.py            # Script d'exécution principal
└── requirements_test.txt       # Dépendances pour les tests
```

## 🚀 Installation et Configuration

### 1. Installation des dépendances

```bash
# Installer les dépendances de test
pip install -r tests/requirements_test.txt

# Ou utiliser le script d'installation
python tests/run_all_tests.py --install-deps
```

### 2. Configuration

Le fichier `tests/conftest.py` contient toutes les configurations et fixtures communes :
- Répertoires temporaires
- Données de test standardisées
- Mocks pour Excel et LLM
- Seuils de performance
- Cas de test de régression

## 🧪 Types de Tests

### 1. Tests Unitaires (`test_unitaires.py`)

**Objectif** : Tester chaque fonction individuellement

**Modules testés** :
- `client_utils` : Extraction et validation des données client
- `dimensions_utils` : Détection des dimensions
- `hauteur_utils` : Calcul de hauteur
- `fermete_utils` : Détection de fermeté
- `housse_utils` : Détection du type de housse
- `matiere_housse_utils` : Détection de la matière
- `poignees_utils` : Détection des poignées
- `matelas_utils` : Détection du noyau
- `pre_import_utils` : Création et validation du pré-import
- `excel_import_utils` : Import Excel
- `config` : Gestion de la configuration
- Référentiels : Consultation des prix

**Exemple d'utilisation** :
```bash
# Tests unitaires avec détails
pytest tests/test_unitaires.py -v

# Tests unitaires avec couverture
pytest tests/test_unitaires.py --cov=backend --cov-report=html
```

### 2. Tests d'Intégration (`test_integration.py`)

**Objectif** : Tester le flux complet de l'application

**Fonctionnalités testées** :
- Traitement complet de fichiers PDF
- Intégration LLM (avec et sans enrichissement)
- Création de pré-import et export Excel
- Traitement de multiples fichiers
- Gestion d'erreurs
- Performance avec grand volume

**Exemple d'utilisation** :
```bash
# Tests d'intégration
pytest tests/test_integration.py -v

# Tests d'intégration avec mocks
pytest tests/test_integration.py -v --tb=short
```

### 3. Tests de Performance (`test_performance.py`)

**Objectif** : Mesurer et valider les performances

**Métriques mesurées** :
- Temps de traitement
- Utilisation mémoire
- Performance avec grand volume de données
- Benchmark complet

**Seuils de performance** :
- Extraction client : < 2s pour 1000 extractions
- Détection dimensions : < 1s pour 1000 détections
- Création pré-import : < 10s pour 500 configurations
- Import Excel : < 5s pour 200 configurations
- Traitement complet : < 30s pour 10 fichiers

**Exemple d'utilisation** :
```bash
# Tests de performance
pytest tests/test_performance.py -v

# Benchmark complet
python tests/test_performance.py
```

### 4. Tests de Régression (`test_regression.py`)

**Objectif** : Détecter les régressions dans les fonctionnalités

**Fonctionnalités surveillées** :
- Extraction de données client
- Détection de dimensions
- Calcul de hauteur
- Détection de fermeté
- Création de pré-import
- Validation des données
- Consultation des référentiels
- Import Excel
- Configuration

**Exemple d'utilisation** :
```bash
# Tests de régression
pytest tests/test_regression.py -v

# Suite complète de régression
python tests/test_regression.py
```

## 🎯 Exécution des Tests

### Script Principal

Le script `run_all_tests.py` permet d'exécuter tous les types de tests :

```bash
# Tous les tests
python tests/run_all_tests.py --all

# Tests unitaires avec détails
python tests/run_all_tests.py --unit --verbose

# Tests de performance
python tests/run_all_tests.py --performance

# Tests de régression
python tests/run_all_tests.py --regression

# Avec couverture de code
python tests/run_all_tests.py --all --coverage

# Générer un rapport
python tests/run_all_tests.py --all --report
```

### Options Disponibles

- `--all` : Exécute tous les tests
- `--unit` : Tests unitaires uniquement
- `--integration` : Tests d'intégration uniquement
- `--performance` : Tests de performance uniquement
- `--regression` : Tests de régression uniquement
- `--benchmark` : Benchmark de performance
- `--verbose` : Mode verbeux
- `--coverage` : Génère un rapport de couverture
- `--report` : Génère un rapport JSON
- `--install-deps` : Installe les dépendances

### Exécution Directe avec Pytest

```bash
# Tous les tests
pytest tests/ -v

# Tests unitaires
pytest tests/test_unitaires.py -v

# Tests avec marqueurs
pytest tests/ -m "unit" -v
pytest tests/ -m "performance" -v
pytest tests/ -m "regression" -v

# Tests avec couverture
pytest tests/ --cov=backend --cov=config --cov-report=html

# Tests parallèles
pytest tests/ -n auto
```

## 📊 Rapports et Métriques

### Rapports de Couverture

```bash
# Générer un rapport HTML
pytest tests/ --cov=backend --cov-report=html:test_reports/coverage_html

# Générer un rapport XML
pytest tests/ --cov=backend --cov-report=xml:test_reports/coverage.xml

# Afficher les lignes manquantes
pytest tests/ --cov=backend --cov-report=term-missing
```

### Rapports de Performance

Les tests de performance génèrent automatiquement des rapports avec :
- Temps d'exécution
- Utilisation mémoire
- Comparaison avec les seuils
- Graphiques de performance

### Rapports JSON

Le script principal génère des rapports JSON détaillés dans `test_reports/` :
- Résumé des tests
- Durée d'exécution
- Codes de retour
- Sorties et erreurs

## 🔧 Configuration Avancée

### Fixtures Personnalisées

Les fixtures dans `conftest.py` peuvent être étendues :

```python
@pytest.fixture(scope="function")
def custom_test_data():
    """Fixture personnalisée pour des données de test"""
    return {
        "custom_field": "custom_value"
    }
```

### Marqueurs Pytest

```bash
# Exécuter les tests lents
pytest tests/ -m "slow" -v

# Exclure les tests de performance
pytest tests/ -m "not performance" -v

# Combiner les marqueurs
pytest tests/ -m "unit and not slow" -v
```

### Configuration des Seuils

Modifier les seuils de performance dans `conftest.py` :

```python
@pytest.fixture(scope="function")
def performance_thresholds():
    return {
        "extraction_client": {"time": 1.5, "memory": 80},  # Seuils ajustés
        # ...
    }
```

## 🐛 Débogage des Tests

### Mode Débogage

```bash
# Arrêter au premier échec
pytest tests/ -x

# Afficher les variables locales en cas d'échec
pytest tests/ -l

# Mode traceback complet
pytest tests/ --tb=long

# Mode interactif
pytest tests/ --pdb
```

### Logs Détaillés

```bash
# Logs de debug
pytest tests/ --log-cli-level=DEBUG

# Logs dans un fichier
pytest tests/ --log-file=test.log --log-file-level=DEBUG
```

### Tests Spécifiques

```bash
# Test spécifique
pytest tests/test_unitaires.py::TestClientUtils::test_extraire_ville_adresse -v

# Classe de tests spécifique
pytest tests/test_unitaires.py::TestClientUtils -v

# Tests avec pattern
pytest tests/ -k "client" -v
```

## 🔄 Intégration Continue

### GitHub Actions

Exemple de workflow GitHub Actions :

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r tests/requirements_test.txt
    - name: Run tests
      run: python tests/run_all_tests.py --all --coverage --report
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    stages {
        stage('Install') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pip install -r tests/requirements_test.txt'
            }
        }
        stage('Test') {
            steps {
                sh 'python tests/run_all_tests.py --all --coverage --report'
            }
        }
        stage('Report') {
            steps {
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'test_reports/coverage_html',
                    reportFiles: 'index.html',
                    reportName: 'Coverage Report'
                ])
            }
        }
    }
}
```

## 📈 Métriques et KPIs

### Métriques de Qualité

- **Couverture de code** : Objectif > 80%
- **Temps d'exécution** : < 5 minutes pour tous les tests
- **Taux de réussite** : Objectif 100%
- **Tests de régression** : 0 régression détectée

### Métriques de Performance

- **Temps de traitement** : Respect des seuils définis
- **Utilisation mémoire** : < 500 MB pour les tests complets
- **Scalabilité** : Tests avec grand volume de données

## 🛠️ Maintenance

### Ajout de Nouveaux Tests

1. **Tests unitaires** : Ajouter dans `test_unitaires.py`
2. **Tests d'intégration** : Ajouter dans `test_integration.py`
3. **Tests de performance** : Ajouter dans `test_performance.py`
4. **Tests de régression** : Ajouter dans `test_regression.py`

### Mise à Jour des Fixtures

Modifier `conftest.py` pour ajouter de nouvelles fixtures communes.

### Mise à Jour des Seuils

Ajuster les seuils de performance selon l'évolution de l'application.

## 📚 Ressources

- [Documentation Pytest](https://docs.pytest.org/)
- [Pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
- [Meilleures pratiques de test](https://realpython.com/python-testing/)

## 🤝 Contribution

Pour contribuer aux tests :

1. Suivre les conventions de nommage
2. Ajouter des docstrings pour tous les tests
3. Utiliser les fixtures existantes
4. Respecter les seuils de performance
5. Mettre à jour la documentation

---

**Note** : Ce système de tests garantit la qualité et la fiabilité de l'application Matelas en détectant automatiquement les régressions et en validant les performances. 