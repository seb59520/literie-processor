# Guide d'Installation Windows - Application Matelas

## 🚀 Installation Rapide (Recommandée)

### Prérequis
- Windows 10 ou 11
- Python 3.8 ou supérieur

### Étapes d'installation

1. **Installer Python** (si pas déjà fait)
   - Téléchargez Python depuis [python.org](https://www.python.org/downloads/)
   - **IMPORTANT** : Cochez "Add Python to PATH" lors de l'installation
   - Redémarrez votre terminal après l'installation

2. **Lancer l'installation automatique**
   ```cmd
   # Double-cliquez sur install_simple.bat (recommandé)
   # Ou sur install_windows.bat
   # Ou dans un terminal :
   install_simple.bat
   ```

3. **Attendre la compilation**
   - L'installation prend 5-10 minutes
   - Toutes les dépendances sont installées automatiquement
   - Un exécutable autonome est créé

4. **Résultat**
   - Votre application se trouve dans `dist/MatelasApp/`
   - Lancez `install.bat` pour créer un raccourci sur le bureau
   - Ou lancez directement `MatelasApp.exe`

## 🔧 Installation Manuelle (Avancée)

### Option 1 : Installation avec Python

```cmd
# 1. Installer les dépendances
pip install -r requirements_gui.txt
pip install -r backend/requirements.txt

# 2. Lancer l'application
python run_gui.py
```

### Option 2 : Création d'exécutable manuelle

```cmd
# 1. Installer PyInstaller
pip install pyinstaller

# 2. Créer l'exécutable
pyinstaller --onefile --windowed --name MatelasApp run_gui.py

# 3. L'exécutable sera dans dist/MatelasApp.exe
```

## 📦 Distribution

### Pour distribuer l'application

1. **Après l'installation automatique**
   - Copiez le dossier `dist/MatelasApp/`
   - Ce dossier contient tout ce qui est nécessaire

2. **Sur un autre PC Windows**
   - Copiez le dossier `MatelasApp/`
   - Lancez `install.bat` pour créer un raccourci
   - Ou lancez directement `MatelasApp.exe`

### Création d'un installateur MSI (Optionnel)

```cmd
# Installer WiX Toolset
# Puis utiliser le script setup_windows.py qui inclut cette option
```

## 🛠️ Dépannage

### Erreur "Python n'est pas reconnu"
- Réinstallez Python en cochant "Add Python to PATH"
- Redémarrez votre terminal

### Erreur de caractères spéciaux dans les scripts batch
- Utilisez `install_simple.bat` au lieu de `install_windows.bat`
- Ou lancez directement : `python setup_windows.py`

### Erreur de compilation PyInstaller
```cmd
# 1. Lancer le diagnostic
diagnostic.bat

# 2. Nettoyer et réessayer
clean_installation.bat
python setup_windows.py

# 3. Si problème persiste, réinstaller PyInstaller
pip install --force-reinstall pyinstaller
```

### Erreur de compilation PyInstaller (ancienne méthode)
```cmd
# Nettoyer et réessayer
rmdir /s build
rmdir /s dist
del *.spec
python setup_windows.py
```

### Erreur de dépendances
```cmd
# Mettre à jour pip
python -m pip install --upgrade pip

# Réinstaller les dépendances
pip install -r requirements_gui.txt --force-reinstall
```

### L'application ne démarre pas
- Vérifiez les logs dans `logs/matelas_app.log`
- Assurez-vous que tous les fichiers sont présents dans le dossier

## 📋 Vérification de l'installation

### Test rapide
```cmd
# Dans le dossier de l'application
MatelasApp.exe --test
```

### Vérification des composants
- ✅ Interface graphique PyQt6
- ✅ Traitement PDF (PyMuPDF)
- ✅ Export Excel (openpyxl)
- ✅ API LLM (httpx)
- ✅ Chiffrement (cryptography)

## 🔒 Sécurité

### Stockage des clés API
- Les clés API sont chiffrées localement
- Stockées dans `config/secure_keys.dat`
- Protégées par un salt unique

### Permissions
- L'application ne nécessite pas de droits administrateur
- Fonctionne en mode utilisateur standard

## 📞 Support

### Logs de débogage
- Logs principaux : `logs/matelas_app.log`
- Logs d'erreurs : `logs/matelas_errors.log`

### Informations système
```cmd
# Afficher les informations de l'application
MatelasApp.exe --info
```

### Mise à jour
- Téléchargez la nouvelle version
- Relancez `install_windows.bat`
- L'ancienne version sera remplacée

## 🎯 Fonctionnalités incluses

- ✅ Interface graphique complète
- ✅ Traitement de devis PDF
- ✅ Export Excel automatique
- ✅ Support LLM (Ollama, OpenRouter)
- ✅ Gestion des configurations
- ✅ Tests automatisés
- ✅ Logs détaillés
- ✅ Stockage sécurisé des clés API

## 📝 Notes importantes

- L'application est autonome après compilation
- Aucune installation de Python requise sur les PC cibles
- Compatible Windows 10/11 (32 et 64 bits)
- Taille finale : ~50-100 MB selon les dépendances 