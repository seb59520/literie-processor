# Résumé : Configuration du Répertoire de Sortie Excel

## Fonctionnalité implémentée

L'application permet maintenant de configurer le répertoire de sortie des fichiers Excel via l'interface graphique, au lieu d'utiliser un répertoire codé en dur.

## Modifications apportées

### 1. **Extension de la classe `Config` (`config.py`)**

**Nouvelles méthodes ajoutées :**
```python
def get_excel_output_directory(self):
    """Récupère le répertoire de sortie des fichiers Excel"""
    default_output = os.path.join(os.getcwd(), "output")
    return self.config.get('excel_output_directory', default_output)

def set_excel_output_directory(self, directory):
    """Définit le répertoire de sortie des fichiers Excel"""
    # Normaliser le chemin
    directory = os.path.abspath(directory)
    self.config['excel_output_directory'] = directory
    self._save_config()
```

**Avantages :**
- ✅ Répertoire par défaut intelligent (répertoire courant + "output")
- ✅ Normalisation automatique des chemins
- ✅ Persistance de la configuration
- ✅ Compatibilité avec l'existant

### 2. **Modification de `excel_import_utils.py`**

**Changements dans la méthode `save_workbook()` :**
```python
# Utiliser le répertoire de sortie configuré
try:
    from config import config
    output_dir = config.get_excel_output_directory()
except Exception as e:
    logger.warning(f"Impossible d'importer config: {e}. Utilisation du répertoire par défaut.")
    output_dir = "output"

filepath = os.path.join(output_dir, filename)
os.makedirs(output_dir, exist_ok=True)
```

**Changements dans la méthode `import_configurations()` :**
- Remplacement de tous les chemins codés en dur "output" par le répertoire configuré
- Gestion d'erreur robuste avec fallback vers le répertoire par défaut

**Avantages :**
- ✅ Utilisation du répertoire configuré partout
- ✅ Création automatique du répertoire si nécessaire
- ✅ Fallback sécurisé en cas d'erreur

### 3. **Nouvelle interface graphique (`app_gui.py`)**

**Nouvelle classe `GeneralSettingsDialog` :**
- Interface intuitive pour configurer le répertoire de sortie
- Bouton "Parcourir..." pour sélectionner facilement un répertoire
- Informations en temps réel sur le répertoire sélectionné
- Validation et feedback visuel

**Ajout au menu "Réglages" :**
```
Réglages
├── ⚙️ Paramètres généraux
├── ──────────────────────
├── Classer l'ordre des noyaux
└── 🔧 Configuration des Providers LLM
```

**Fonctionnalités de l'interface :**
- ✅ Sélection de répertoire via dialogue système
- ✅ Affichage du nombre de fichiers Excel existants
- ✅ Validation du répertoire en temps réel
- ✅ Sauvegarde automatique des paramètres
- ✅ Interface cohérente avec le reste de l'application

## Utilisation

### Via l'interface graphique :
1. **Menu** → **Réglages** → **⚙️ Paramètres généraux**
2. Cliquer sur **"Parcourir..."** pour sélectionner le répertoire
3. Cliquer sur **"OK"** pour sauvegarder

### Via le code :
```python
from config import config

# Définir le répertoire de sortie
config.set_excel_output_directory("/chemin/vers/repertoire")

# Récupérer le répertoire actuel
output_dir = config.get_excel_output_directory()
```

## Tests validés

### ✅ Test de configuration
- Modification du répertoire de sortie
- Persistance de la configuration
- Restauration du répertoire par défaut

### ✅ Test de création de fichiers
- Création de fichiers Excel dans le répertoire configuré
- Vérification de l'emplacement correct
- Gestion des erreurs

### ✅ Test de l'interface
- Création du dialogue de paramètres
- Intégration avec l'application principale

## Avantages de la solution

1. **Flexibilité** : L'utilisateur peut choisir où sauvegarder ses fichiers Excel
2. **Persistance** : La configuration est sauvegardée entre les sessions
3. **Robustesse** : Gestion d'erreur avec fallback vers le répertoire par défaut
4. **Intuitivité** : Interface graphique simple et claire
5. **Compatibilité** : Fonctionne avec l'existant sans casser les fonctionnalités
6. **Sécurité** : Normalisation des chemins pour éviter les problèmes

## Fichiers modifiés

- `config.py` : Ajout des méthodes de gestion du répertoire de sortie
- `backend/excel_import_utils.py` : Utilisation du répertoire configuré
- `app_gui.py` : Nouvelle interface de paramètres généraux

## Configuration par défaut

- **Répertoire par défaut** : `{répertoire_courant}/output`
- **Fichier de configuration** : `~/.matelas_config.json`
- **Persistance** : Automatique lors de la modification

La fonctionnalité est maintenant prête à être utilisée ! 🎯 