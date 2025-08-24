# 🔧 GUIDE DE DÉPANNAGE WINDOWS

## 🚀 Lancement de l'Application

### Scripts Disponibles

1. **`build_launcher.bat`** - Menu principal avec toutes les options
2. **`lancer_app_windows.bat`** - Lancement direct de l'application
3. **`diagnostic_pyqt6_windows.bat`** - Diagnostic des problèmes PyQt6

### Utilisation Recommandée

```batch
# Double-cliquez sur build_launcher.bat
# Puis choisissez l'option 1 : "Lancer l'application"
```

## ❌ Problèmes Courants

### 1. Erreur PyQt6.QtWidgets.QAction

**Symptôme :**
```
ImportError: cannot import name 'QAction' from 'PyQt6.QtWidgets'
```

**Solution :**
```batch
# Exécutez le diagnostic
diagnostic_pyqt6_windows.bat

# Ou réinstallez PyQt6 manuellement
pip uninstall PyQt6 -y
pip install PyQt6==6.5.0
```

### 2. Python Non Trouvé

**Symptôme :**
```
'python' n'est pas reconnu comme une commande interne
```

**Solution :**
1. Installez Python depuis https://python.org
2. Cochez "Add Python to PATH" lors de l'installation
3. Redémarrez l'invite de commande

### 3. Dépendances Manquantes

**Symptôme :**
```
ModuleNotFoundError: No module named 'openpyxl'
```

**Solution :**
```batch
pip install openpyxl requests PyQt6
```

### 4. Erreur de Permissions

**Symptôme :**
```
PermissionError: [Errno 13] Permission denied
```

**Solution :**
1. Exécutez l'invite de commande en tant qu'administrateur
2. Ou installez les packages avec `--user` :
   ```batch
   pip install --user PyQt6
   ```

## 🔍 Diagnostic Automatique

Le script `diagnostic_pyqt6_windows.bat` vérifie automatiquement :

- ✅ Version de Windows
- ✅ Installation de Python
- ✅ Installation de pip
- ✅ Installation de PyQt6
- ✅ Modules PyQt6 spécifiques
- ✅ Import de l'application
- ✅ Autres dépendances

## 📋 Checklist de Dépannage

### Étape 1 : Vérifications de Base
- [ ] Python 3.8+ installé
- [ ] Python dans le PATH
- [ ] pip fonctionnel

### Étape 2 : Dépendances
- [ ] PyQt6 installé
- [ ] openpyxl installé
- [ ] requests installé

### Étape 3 : Test d'Import
- [ ] Import PyQt6.QtWidgets fonctionne
- [ ] Import app_gui fonctionne

### Étape 4 : Lancement
- [ ] Application se lance sans erreur
- [ ] Interface graphique s'affiche

## 🛠️ Solutions Avancées

### Réinstallation Complète de PyQt6

```batch
pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip -y
pip install PyQt6
```

### Utilisation de PySide6 (Alternative)

Si PyQt6 pose problème, essayez PySide6 :

```batch
pip uninstall PyQt6 -y
pip install PySide6
```

Puis modifiez les imports dans `app_gui.py` :
```python
# Remplacer
from PyQt6.QtWidgets import ...
from PyQt6.QtCore import ...
from PyQt6.QtGui import ...

# Par
from PySide6.QtWidgets import ...
from PySide6.QtCore import ...
from PySide6.QtGui import ...
```

### Environnement Virtuel

Pour éviter les conflits :

```batch
# Créer un environnement virtuel
python -m venv matelas_env

# Activer l'environnement
matelas_env\Scripts\activate

# Installer les dépendances
pip install PyQt6 openpyxl requests

# Lancer l'application
python app_gui.py
```

## 📞 Support

En cas de problème persistant :

1. **Exécutez le diagnostic :** `diagnostic_pyqt6_windows.bat`
2. **Notez les erreurs exactes** affichées
3. **Vérifiez la version de Python :** `python --version`
4. **Vérifiez la version de PyQt6 :** `pip show PyQt6`

## 🎯 Commandes Utiles

```batch
# Vérifier Python
python --version

# Vérifier pip
pip --version

# Lister les packages installés
pip list

# Vérifier PyQt6
python -c "import PyQt6; print(PyQt6.QtCore.PYQT_VERSION_STR)"

# Tester l'import de l'application
python -c "from app_gui import MatelasApp; print('OK')"
```

---

**Note :** Ce guide couvre les problèmes les plus courants. Si votre problème persiste, consultez les logs d'erreur détaillés fournis par le script de diagnostic. 