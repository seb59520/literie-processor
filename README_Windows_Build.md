# 🏗️ Compilation Windows - Processeur de Devis Literie

Ce guide explique comment créer un exécutable Windows (.exe) de l'application Matelas Processor.

## 📋 Prérequis

### Système requis
- **Python 3.8+** installé
- **pip** pour l'installation des packages
- **Windows 10/11** ou machine virtuelle Windows (pour tester)
- **~500 MB** d'espace libre pour la compilation

### Packages Python nécessaires
```bash
pip install -r requirements_build.txt
```

## 🚀 Compilation automatique

### Méthode simple (recommandée)
```bash
python build_windows.py
```

Ce script automatique va :
1. ✅ Vérifier les dépendances
2. ✅ Créer les fichiers de configuration PyInstaller
3. ✅ Compiler l'exécutable
4. ✅ Créer un script d'installation Windows
5. ✅ Générer tous les fichiers dans le dossier `dist/`

### Résultat attendu
```
dist/
├── MatelasProcessor.exe    # Exécutable principal (~100-200 MB)
└── install.bat            # Script d'installation Windows
```

## 🔧 Compilation manuelle

Si vous préférez contrôler chaque étape :

### 1. Installation de PyInstaller
```bash
pip install pyinstaller
```

### 2. Création du fichier .spec
```bash
python -c "from build_windows import create_spec_file; create_spec_file()"
```

### 3. Compilation
```bash
pyinstaller --clean matelas_processor.spec
```

## 📦 Distribution

### Installation sur Windows cible

**Option 1 : Installation automatique**
1. Copiez le dossier `dist/` sur la machine Windows
2. Clic droit sur `install.bat` → "Exécuter en tant qu'administrateur"
3. L'application sera installée dans `C:\Program Files\MatelasProcessor\`

**Option 2 : Exécution portable**
1. Copiez `MatelasProcessor.exe` où vous voulez
2. Double-cliquez pour lancer (portable, aucune installation)

### Premier lancement
⚠️ **Important** : Le premier lancement peut prendre 10-30 secondes (extraction interne des fichiers)

## 🎯 Configuration Windows

L'application s'adapte automatiquement à Windows :

### Répertoires utilisés
- **Configuration** : `%USERPROFILE%\MatelasProcessor\`
- **Sortie Excel** : `%USERPROFILE%\Documents\MatelasProcessor\`
- **Logs** : `%USERPROFILE%\AppData\Local\MatelasProcessor\logs\`
- **Temporaire** : `%TEMP%\MatelasProcessor\`

### Fonctionnalités Windows
- ✅ Ouverture automatique des dossiers avec l'Explorateur
- ✅ Icône d'application personnalisable
- ✅ Informations de version dans les propriétés du fichier
- ✅ Support des chemins Windows avec espaces
- ✅ Gestion des permissions utilisateur

## 🛠️ Personnalisation

### Icône personnalisée
1. Ajoutez votre icône : `assets/icon.ico` (16x16 à 256x256 pixels)
2. Recompilez avec `python build_windows.py`

### Informations de version
Modifiez `version_info.txt` pour changer :
- Version de l'application
- Nom de la société  
- Description du produit
- Copyright

### Taille de l'exécutable
L'exécutable fait ~100-200 MB car il inclut :
- Python runtime complet
- PyQt6 framework
- Toutes les dépendances Python
- Assets et fichiers de configuration

**Pour réduire la taille :**
- Activez UPX compression (`upx=True` dans .spec)
- Excluez les modules non utilisés dans `excludes=[]`

## 🐛 Résolution de problèmes

### L'exécutable ne se lance pas
1. **Vérifiez les permissions** : Clic droit → Propriétés → Débloquer
2. **Antivirus** : Ajoutez une exception pour MatelasProcessor.exe
3. **Dépendances manquantes** : Installez Visual C++ Redistributable

### Erreur "Module not found"
- Ajoutez le module manquant dans `hiddenimports=[]` (fichier .spec)
- Recompilez

### Lancement très lent
- Normal au premier lancement (extraction)
- Les lancements suivants sont rapides

### Erreur de certificat/signature
- Windows peut bloquer les exécutables non signés
- Clic droit → "Exécuter quand même" ou ajouter une exception

## 📊 Test de l'exécutable

### Liste de vérification
- [ ] L'exécutable se lance sans erreur
- [ ] L'interface graphique s'affiche correctement  
- [ ] Les boutons d'action fonctionnent
- [ ] L'ouverture des dossiers fonctionne
- [ ] La génération de rapports HTML marche
- [ ] Les onglets (Configuration, Logs, Debug) sont accessibles
- [ ] L'application se ferme proprement

### Test sur machine propre
Testez idéalement sur une machine Windows sans Python installé pour vérifier l'autonomie complète.

## 📚 Références

- [PyInstaller Documentation](https://pyinstaller.readthedocs.io/)
- [PyQt6 Deployment](https://doc.qt.io/qtforpython/deployment.html)
- [Windows Executable Guide](https://realpython.com/pyinstaller-python/)

## ⚡ Raccourcis utiles

```bash
# Compilation rapide
python build_windows.py

# Nettoyage complet
rm -rf build/ dist/ *.spec

# Test local (sans compilation)
python app_gui.py

# Vérification des imports
python -c "import app_gui; print('OK')"
```