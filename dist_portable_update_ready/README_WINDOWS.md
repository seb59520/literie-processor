# MATELAS Application v3.11.12 - Guide Windows

## 🚀 Installation Rapide

### ⚠️ IMPORTANT - Prérequis Windows
1. **Python 3.8+** depuis https://python.org/downloads
2. **Cocher "Add Python to PATH"** lors de l'installation Python
3. **Redémarrer** l'invite de commande après installation Python

### 🔧 Installation Automatique
```cmd
python install.py
```

### 🚀 Lancement
```cmd
python app_gui.py
```
**OU** cliquer sur **`lancer_matelas.bat`**

## 🚨 Résolution des Problèmes Windows

### "Python est introuvable"
1. Installer Python depuis https://python.org/downloads
2. ⚠️ **COCHER "Add Python to PATH"**
3. Redémarrer l'invite de commande
4. Tester: `python --version`

### "ModuleNotFoundError"
```cmd
python install.py
```

### "Permission denied" 
- Exécuter l'invite de commande **en tant qu'Administrateur**
- Clic droit sur cmd → "Exécuter en tant qu'administrateur"

### Scripts de Lancement
- **Windows**: `lancer_matelas.bat`
- **PowerShell**: `python app_gui.py`
- **Invite de commande**: `python app_gui.py`

## 📁 Structure Windows
```
MATELAS_v3.11.12/
├── install.py                 ← Installer d'abord
├── lancer_matelas.bat        ← Lancement Windows
├── app_gui.py                ← Application principale
├── README.md                 ← Ce fichier
└── ...                       ← Autres fichiers
```

## 🎯 Nouvelles Fonctionnalités

### 📦 Générateur de Packages (Développeurs)
- **Accès**: Menu Diagnostic
- **Mot de passe**: `matelas_dev_2025`
- **Fonctions**: Création, suggestions automatiques, consolidation

## 📞 Support Windows
- **Logs**: Dossier `logs/`
- **Configuration**: `matelas_config.json`
- **Erreurs**: `logs/errors.log`

---
**✅ Suivez ces étapes dans l'ordre et l'application fonctionnera parfaitement sur Windows !**
