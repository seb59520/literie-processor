# GUIDE DE DÉPANNAGE - PROBLÈMES DE LANCEMENT

## 🚨 PROBLÈMES IDENTIFIÉS ET SOLUTIONS

### **1. Erreur PyQt6 : `ImportError: cannot import name 'QAction'`**

**Problème :** `QAction` doit être importé depuis `PyQt6.QtGui`, pas depuis `PyQt6.QtWidgets`

**✅ Solution appliquée :**
- Correction des imports dans `app_gui.py`
- `QAction` importé depuis `PyQt6.QtGui`
- Suppression de `QMenu` des imports `QtWidgets` (déjà dans `QtGui`)

### **2. Erreur Excel : `cannot access local variable 'os'`**

**Problème :** Imports locaux dans la fonction `open_excel_file` créent des conflits

**✅ Solution appliquée :**
- Suppression des imports locaux redondants
- Utilisation des imports globaux déjà présents
- Correction de la gestion des chemins de fichiers

### **3. Erreur clé API : `401 Client Error: Unauthorized`**

**Problème :** Clé API OpenRouter invalide ou expirée

**💡 Solutions :**
1. **Vérifiez votre clé API** dans l'interface de gestion des providers
2. **Générez une nouvelle clé** sur [OpenRouter](https://openrouter.ai/)
3. **Utilisez un autre provider** (Ollama, Mistral, etc.)

## 🧪 TESTS DE VÉRIFICATION

### **Test 1 : Vérification des imports**
```bash
python3 test_lancement_simple.py
```

**Résultat attendu :**
```
✅ PyQt6 importé avec succès
✅ backend_interface importé
✅ config importé
✅ QApplication créée
✅ MatelasApp créée
✅ Application fermée proprement
✅ SUCCÈS: Tous les tests sont passés!
```

### **Test 2 : Lancement simplifié**
```bash
python3 lancer_test.py
```

**Résultat attendu :**
```
✅ Imports PyQt6 OK
✅ Import MatelasApp OK
✅ QApplication créée
✅ Fenêtre affichée
🎯 Application lancée avec succès!
```

## 🔧 CORRECTIONS APPLIQUÉES

### **1. Correction des imports PyQt6**
```python
# AVANT (incorrect)
from PyQt6.QtWidgets import (..., QAction, QMenu, ...)

# APRÈS (correct)
from PyQt6.QtWidgets import (..., QWidgetAction, ...)
from PyQt6.QtGui import QFont, QPixmap, QIcon, QAction, QColor
```

### **2. Correction de la fonction open_excel_file**
```python
# AVANT (problématique)
def open_excel_file(self, url):
    import subprocess  # Import local
    import platform   # Import local
    
# APRÈS (corrigé)
def open_excel_file(self, url):
    # Utilise les imports globaux
    system = platform.system()
    subprocess.run([...])
```

## 📋 PROCÉDURE DE LANCEMENT

### **Étape 1 : Vérification de l'environnement**
```bash
# Vérifier Python
python3 --version  # Doit être 3.8+

# Vérifier PyQt6
python3 -c "from PyQt6.QtWidgets import QApplication; print('PyQt6 OK')"

# Vérifier les dépendances
pip list | grep -E "(PyQt6|openpyxl|requests)"
```

### **Étape 2 : Test de lancement**
```bash
# Test simple
python3 test_lancement_simple.py

# Lancement complet
python3 lancer_test.py
```

### **Étape 3 : Lancement normal**
```bash
# Lancement standard
python3 app_gui.py
```

## 🚨 PROBLÈMES COURANTS ET SOLUTIONS

### **Problème : "Module not found"**
**Solution :**
```bash
pip install PyQt6 openpyxl requests
```

### **Problème : "Permission denied"**
**Solution :**
```bash
chmod +x app_gui.py
python3 app_gui.py
```

### **Problème : "Display not found" (Linux)**
**Solution :**
```bash
export DISPLAY=:0
python3 app_gui.py
```

### **Problème : "QApplication already exists"**
**Solution :**
```bash
# Redémarrer le terminal
# Ou utiliser un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

## 📊 DIAGNOSTIC AUTOMATIQUE

### **Script de diagnostic complet**
```bash
python3 test_scripts_ascii.bat  # Windows
# ou
python3 test_lancement_simple.py  # Tous systèmes
```

### **Vérification des logs**
```bash
# Consulter les logs d'erreur
cat logs/matelas_errors.log

# Consulter les logs généraux
cat logs/matelas_app.log
```

## 🎯 RÉSULTAT ATTENDU

Après application des corrections :

✅ **Application se lance sans erreur**
✅ **Interface graphique visible**
✅ **Fonctionnalités de base opérationnelles**
✅ **Gestion des fichiers PDF fonctionnelle**
✅ **Export Excel fonctionnel**

## 📞 SUPPORT

Si les problèmes persistent :

1. **Vérifiez les logs** dans le dossier `logs/`
2. **Testez avec les scripts de diagnostic**
3. **Vérifiez votre version de Python** (3.8+ requis)
4. **Réinstallez les dépendances** si nécessaire

**L'application devrait maintenant se lancer correctement !** 🚀 