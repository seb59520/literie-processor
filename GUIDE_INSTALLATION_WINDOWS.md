# 🚀 GUIDE INSTALLATION WINDOWS - MATELAS v3.11.12

## 🔧 Solution aux Problèmes Rencontrés

### ❌ **Problème 1: "Python est introuvable"**
```
PS C:\Users\SEBASTIEN\Desktop\MATELAS_v3.11.12_PORTABLE_20250905_210130> python3 install.py
Python est introuvable ; exécutez sans arguments à installer à partir du Microsoft Store...
```

**✅ Solution :**

#### Étape 1 : Installation de Python
1. Aller sur **https://python.org/downloads**
2. Télécharger **Python 3.11** ou plus récent
3. **⚠️ TRÈS IMPORTANT :** Cocher **"Add Python to PATH"**
4. Installer Python
5. **Redémarrer** l'invite de commande PowerShell

#### Étape 2 : Vérification
```powershell
python --version
# Doit afficher : Python 3.11.x
```

### ❌ **Problème 2: "ModuleNotFoundError"**
```
ModuleNotFoundError: No module named 'aide_generateur_preimport'
```

**✅ Solution :** Utilisez le **nouveau package corrigé**

## 📦 **Nouveau Package Corrigé**

**Utilisez maintenant :** `MATELAS_v3.11.12_PORTABLE_20250905_211203.zip`

**Corrections apportées :**
- ✅ Fichier `aide_generateur_preimport.py` inclus
- ✅ Script d'installation Windows optimisé
- ✅ Script de lancement `lancer_matelas.bat` amélioré
- ✅ Guide Windows détaillé inclus

## 🔄 **Installation Pas à Pas**

### 1. **Télécharger le Nouveau Package**
```
MATELAS_v3.11.12_PORTABLE_20250905_211203.zip (1.0 MB)
```

### 2. **Installer Python (si pas fait)**
- **Site :** https://python.org/downloads
- **Version :** Python 3.11 ou plus récent
- **⚠️ Cocher "Add Python to PATH"**
- **Redémarrer** PowerShell après installation

### 3. **Extraction**
```powershell
# Extraire dans un dossier dédié
# Exemple : C:\MATELAS\
```

### 4. **Installation**
```powershell
# Ouvrir PowerShell dans le dossier extrait
cd C:\MATELAS\MATELAS_v3.11.12_PORTABLE_20250905_211203

# Installer les dépendances
python install.py
```

### 5. **Lancement**
```powershell
# Méthode 1 : PowerShell
python app_gui.py

# Méthode 2 : Double-clic sur le fichier
lancer_matelas.bat
```

## 🛠️ **Scripts de Lancement Windows**

### **lancer_matelas.bat** (recommandé)
- Double-clic pour lancer
- Vérifie Python et dépendances
- Messages d'erreur clairs
- Gestion automatique des problèmes

### **PowerShell**
```powershell
python app_gui.py
```

## 🚨 **Dépannage Avancé**

### **Python non reconnu après installation**
```powershell
# Vérifier les variables d'environnement
echo $env:PATH

# Si Python n'apparaît pas, ajouter manuellement :
# Panneau de configuration > Système > Variables d'environnement
# Ajouter à PATH : C:\Python311\ et C:\Python311\Scripts\
```

### **Erreur de permissions**
```powershell
# Exécuter PowerShell en tant qu'Administrateur
# Clic droit sur PowerShell > "Exécuter en tant qu'administrateur"
```

### **Modules manquants**
```powershell
# Réinstaller les dépendances
python -m pip install --upgrade pip
python install.py
```

## 📋 **Vérification Complète**

### **Test Python**
```powershell
python --version          # Doit afficher Python 3.11.x
python -m pip --version   # Doit afficher pip version
```

### **Test Modules**
```powershell
python -c "import PyQt6; print('PyQt6 OK')"
python -c "import requests; print('requests OK')"
python -c "import openpyxl; print('openpyxl OK')"
```

### **Test Application**
```powershell
python -c "import config; print('Config OK')"
python -c "import version; print('Version OK')"
```

## 🎯 **Structure Finale**

Après installation réussie :
```
C:\MATELAS\MATELAS_v3.11.12_PORTABLE_20250905_211203\
├── install.py                 ✅ Installateur Windows
├── lancer_matelas.bat        ✅ Lanceur Windows  
├── app_gui.py                ✅ Application principale
├── aide_generateur_preimport.py  ✅ Module corrigé
├── README_WINDOWS.md         ✅ Guide Windows
├── logs\                     📁 Logs d'erreurs
├── output\                   📁 Fichiers Excel générés
└── ...                       📁 Autres fichiers
```

## 🏆 **Résultat Final**

**Après ces étapes, vous devriez voir :**
```
[OK] Python detecte
Python 3.11.x

Verification des dependances...
[OK] Dependances OK

Lancement de l'application...

# L'interface PyQt6 s'ouvre avec MATELAS v3.11.12
```

## 📞 **Support**

**Si problème persiste :**
1. Consulter `logs\app.log`
2. Consulter `logs\errors.log` 
3. Vérifier `matelas_config.json`
4. Réessayer installation : `python install.py`

---

**✅ Avec ce nouveau package et ces instructions, MATELAS v3.11.12 fonctionnera parfaitement sur Windows !**

**Package corrigé :** `MATELAS_v3.11.12_PORTABLE_20250905_211203.zip`