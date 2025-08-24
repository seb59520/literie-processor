# Importateur Excel pour Configurations de Matelas

## 📋 Description

Script Python pour automatiser l'import de configurations de matelas dans des fichiers Excel selon un template spécifique.

## 🎯 Fonctionnalités

- ✅ Import automatique depuis des données JSON
- ✅ Respect de l'ordre des blocs de colonnes (C-D, E-F, G-H, I-J, K-L, O-P, Q-R, S-T, U-V, W-X)
- ✅ Saut automatique du bloc verrouillé M-N
- ✅ Création automatique de nouveaux fichiers au-delà de 10 cas
- ✅ Nommage automatique des fichiers : `Matelas_Sxx_XXXX_N.xlsx`
- ✅ Mapping complet des champs JSON vers les cellules Excel

## 📁 Structure des Fichiers

```
backend/
├── excel_import_utils.py      # Script principal d'import
├── test_excel_import.py       # Script de test et démonstration
├── template/
│   └── template_matelas.xlsx  # Template Excel
├── output/                    # Dossier de sortie (créé automatiquement)
└── README_EXCEL_IMPORT.md     # Ce fichier
```

## 🚀 Installation

1. **Installer les dépendances :**
```bash
cd backend
pip install -r requirements.txt
```

2. **Vérifier que le template existe :**
```bash
ls template/template_matelas.xlsx
```

## 📖 Utilisation

### 1. Utilisation Basique

```python
from excel_import_utils import ExcelMatelasImporter

# Créer l'importateur
importer = ExcelMatelasImporter()

# Données JSON (exemple)
configurations = [
    {
        "Client_D1": "DUPONT Jean",
        "Client_D2": "123 Rue de la Paix",
        "Article_D6": "Matelas Premium",
        "Quantite_D11": "2",
        "Dimensions_D15": "160x200",
        "Prix_D26": "1500.00"
    }
]

# Import
created_files = importer.import_configurations(configurations, "S01", "1234")
print(f"Fichiers créés: {created_files}")
```

### 2. Test avec Données d'Exemple

```bash
cd backend
python test_excel_import.py
```

### 3. Test avec Fichier JSON

```python
from test_excel_import import test_with_json_file

# Test avec un fichier JSON existant
created_files = test_with_json_file("test_housse.json", "S02", "5678")
```

## 📊 Mapping des Champs

### Structure JSON Attendue

```json
{
    "Client_D1": "Nom du client",
    "Client_D2": "Adresse",
    "Client_D3": "Code postal + Ville",
    "Client_D4": "Téléphone",
    "Client_D5": "Email",
    
    "Article_D6": "Nom de l'article",
    "Article_D7": "Référence",
    "Article_D8": "Gamme",
    "Article_D9": "Couleur",
    "Article_D10": "Garantie",
    
    "Quantite_D11": "Quantité",
    
    "Housse_D12": "Type de housse",
    "Matiere_Housse_D13": "Matière de la housse",
    
    "Poignees_D14": "Description des poignées",
    
    "Dimensions_D15": "Dimensions complètes",
    "Longueur_D16": "Longueur",
    "Largeur_D17": "Largeur",
    "Hauteur_D18": "Hauteur",
    
    "Noyau_D19": "Type de noyau",
    "Fermete_D20": "Fermeté",
    "Surmatelas_D21": "Surmatelas",
    
    "Operations_D22": "Opération 1",
    "Operations_D23": "Opération 2",
    "Operations_D24": "Opération 3",
    "Operations_D25": "Opération 4",
    
    "Prix_D26": "Prix unitaire",
    "Prix_Total_D27": "Prix total"
}
```

### Mapping vers Excel

Chaque clé JSON est mappée vers une cellule spécifique dans le bloc actif :

- **Client_D1** → Cellule D1 du bloc actif
- **Article_D6** → Cellule D6 du bloc actif
- **Quantite_D11** → Cellule D11 du bloc actif
- etc.

## 🔄 Ordre des Blocs

Le script respecte strictement cet ordre :

1. **Cas 1** → Colonnes C & D
2. **Cas 2** → Colonnes E & F
3. **Cas 3** → Colonnes G & H
4. **Cas 4** → Colonnes I & J
5. **Cas 5** → Colonnes K & L
6. **⚠️ Bloc verrouillé** → Colonnes M & N (sauté)
7. **Cas 6** → Colonnes O & P
8. **Cas 7** → Colonnes Q & R
9. **Cas 8** → Colonnes S & T
10. **Cas 9** → Colonnes U & V
11. **Cas 10** → Colonnes W & X

## 📁 Gestion des Fichiers

### Nommage Automatique

- **Format :** `Matelas_Sxx_XXXX_N.xlsx`
- **Exemple :** `Matelas_S01_1234_1.xlsx`

### Création de Nouveaux Fichiers

- **Déclencheur :** 10 cas atteints OU tous les blocs pleins
- **Action :** Création automatique d'un nouveau fichier
- **Index :** Incrémentation automatique (_1, _2, _3, etc.)

## 🔧 Configuration

### Paramètres Modifiables

Dans `excel_import_utils.py` :

```python
class ExcelMatelasImporter:
    def __init__(self, template_path: str = "template/template_matelas.xlsx"):
        self.max_cases_per_file = 10  # Nombre max de cas par fichier
        # ...
```

### Personnalisation du Mapping

Pour ajouter de nouveaux champs :

```python
self.json_to_cell_mapping = {
    # ... champs existants ...
    'Nouveau_Champ_D28': ('D', 28),  # Nouveau champ
}
```

## 🐛 Dépannage

### Erreurs Courantes

1. **Template non trouvé :**
   ```
   FileNotFoundError: template/template_matelas.xlsx
   ```
   **Solution :** Vérifier que le fichier template existe

2. **Dépendance manquante :**
   ```
   ModuleNotFoundError: No module named 'openpyxl'
   ```
   **Solution :** `pip install openpyxl`

3. **Dossier output inexistant :**
   **Solution :** Le script crée automatiquement le dossier

### Logs

Le script génère des logs détaillés :

```
2024-01-01 10:00:00 - INFO - Chargement du template: template/template_matelas.xlsx
2024-01-01 10:00:01 - INFO - Vérification bloc C-D: cellule D1 = ''
2024-01-01 10:00:01 - INFO - Bloc vide trouvé: C-D
2024-01-01 10:00:01 - INFO - Écriture: D1 = DUPONT Jean
```

## 📝 Exemples Complets

### Exemple 1 : Import Simple

```python
from excel_import_utils import ExcelMatelasImporter

importer = ExcelMatelasImporter()

config = {
    "Client_D1": "Test Client",
    "Article_D6": "Matelas Test",
    "Quantite_D11": "1",
    "Prix_D26": "1000.00"
}

files = importer.import_configurations([config], "S01", "TEST")
```

### Exemple 2 : Import Multiple

```python
configurations = [
    {"Client_D1": "Client 1", "Article_D6": "Matelas 1"},
    {"Client_D1": "Client 2", "Article_D6": "Matelas 2"},
    # ... jusqu'à 10+ configurations
]

files = importer.import_configurations(configurations, "S01", "MULTI")
```

## 🤝 Intégration avec le Backend

Pour intégrer avec votre système existant :

```python
# Dans votre code de traitement PDF
from excel_import_utils import ExcelMatelasImporter

def process_pdf_to_excel(pdf_data, semaine, id_client):
    # Votre logique d'extraction PDF...
    configurations = extract_configurations(pdf_data)
    
    # Import Excel
    importer = ExcelMatelasImporter()
    return importer.import_configurations(configurations, semaine, id_client)
```

## 📞 Support

Pour toute question ou problème :

1. Vérifiez les logs pour identifier l'erreur
2. Consultez la section dépannage
3. Testez avec les exemples fournis
4. Vérifiez la structure du template Excel 