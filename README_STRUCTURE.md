# Structure du Projet MatelasApp

## 📁 Organisation des répertoires

### 🔨 build_scripts/
Scripts de construction de l'application

- **windows/** - Scripts spécifiques à Windows (.bat, .py)
- **macos/** - Scripts spécifiques à macOS (.py, .sh)
- **linux/** - Scripts spécifiques à Linux (.py)
- **common/** - Scripts multi-plateformes

### 🛠️ utilities/
Scripts utilitaires

- **tests/** - Scripts de test et validation
- **admin/** - Scripts d'administration et configuration
- **launchers/** - Scripts de lancement spécialisés

### 📚 docs/
Documentation du projet

- **build/** - Documentation des builds et installation
- **admin/** - Documentation d'administration
- **installation/** - Guides d'installation

## 🚀 Utilisation

### Windows
```batch
build_launcher.bat
```

### macOS/Linux
```bash
./build_launcher.sh
```

## 📋 Scripts principaux

### Build
- `build_complet_avec_referentiels.py` - Build complet avec tous les référentiels
- `build_mac_complet.py` - Build package .app pour macOS
- `build_test_rapide.py` - Build de test rapide

### Administration
- `admin_builder_gui.py` - Interface d'administration
- `admin_dialog.py` - Dialogue d'administration

### Tests
- `test_eula_inclusion.py` - Test de l'inclusion EULA
- `test_integration_admin_builder.py` - Test d'intégration Admin Builder

## 🔧 Intégration dans l'application

L'application principale (`app_gui.py`) peut maintenant accéder aux scripts via :

```python
# Pour l'Admin Builder
from utilities.admin.admin_builder_gui import AdminBuilderGUI

# Pour les tests
from utilities.tests.test_eula_inclusion import test_eula_inclusion
```

## 📦 Build avec la nouvelle structure

Les scripts de build ont été mis à jour pour inclure les nouveaux répertoires dans l'exécutable final.
