# 🔧 GUIDE DE DÉPANNAGE WINDOWS - VERSION FINALE

## ❌ Problèmes Rencontrés et Solutions

### **Problème 1 : Fichier requirements_gui.txt non trouvé**
```
ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements_gui.txt'
```

**Solution :** Utilisez `install_ultra_simple.bat` qui :
- Se déplace automatiquement dans le dossier racine
- Vérifie l'existence du fichier requirements
- Installe les packages individuellement si nécessaire

### **Problème 2 : Erreurs d'encodage 'cho' non reconnu**
```
'cho' n'est pas reconnu en tant que commande interne
```

**Solution :** Utilisez `build_launcher_ultra_fixe.bat` qui :
- Utilise un encodage UTF-8 propre
- Supprime tous les caractères spéciaux
- Utilise une syntaxe batch simplifiée

## ✅ Scripts Recommandés

### **Pour Installation (Recommandé)**
```batch
# Double-cliquez sur build_scripts/windows/install_ultra_simple.bat
```

### **Pour Lancement**
```batch
# Double-cliquez sur build_scripts/windows/build_launcher_ultra_fixe.bat
```

### **Pour Diagnostic**
```batch
# Double-cliquez sur build_scripts/common/diagnostic_windows_fixe.bat
```

## 🔧 Scripts Créés

### **Scripts Ultra-Simplifiés (Recommandés)**
1. **`install_ultra_simple.bat`** - Installation sans caractères spéciaux
2. **`build_launcher_ultra_fixe.bat`** - Lancement ultra-simplifié

### **Scripts Corrigés**
3. **`install_windows_fixe.bat`** - Installation avec gestion des chemins
4. **`build_launcher_fixe.bat`** - Lancement corrigé (peut avoir des problèmes d'encodage)
5. **`build_windows_optimized_fixe.bat`** - Build optimisé corrigé
6. **`diagnostic_windows_fixe.bat`** - Diagnostic complet

## 📋 Procédure d'Installation Recommandée

### **Étape 1 : Diagnostic**
```batch
build_scripts/common/diagnostic_windows_fixe.bat
```

### **Étape 2 : Installation**
```batch
build_scripts/windows/install_ultra_simple.bat
```

### **Étape 3 : Test**
```batch
build_scripts/windows/build_launcher_ultra_fixe.bat
```

## 🎯 Résultats Attendus

### **Installation Réussie**
```
Installation MatelasApp Windows
========================================

[1/4] Verifier Python...
Python 3.11.1
OK: Python trouve

[2/4] Installer dependances...
OK: Dependances installees

[3/4] Compiler application...
OK: Compilation terminee

[4/4] Verifier executable...
OK: Executable cree: dist\MatelasApp.exe

========================================
Installation reussie!
========================================
```

### **Lancement Réussi**
```
========================================
   LANCEUR DE BUILD MATELAS APP
========================================

OK: Python trouve

Options disponibles:

1. Build complet avec referentiels
2. Build Mac complet
3. Build de test rapide
4. Build avec console debug
5. Build standalone
6. Build optimise Windows
7. Verifier fichiers
8. Nettoyer builds
9. Quitter

Choisissez une option (1-9):
```

## 🚨 En Cas de Problème Persistant

### **Solution 1 : Installation Manuelle**
```batch
# Ouvrir cmd en tant qu'administrateur
cd /d "C:\chemin\vers\MATELAS_FINAL"
pip install PyQt6 openpyxl requests pyinstaller
python build_scripts/windows/build_windows_optimized_fixe.bat
```

### **Solution 2 : Vérification Python**
```batch
python --version
pip --version
pip list | findstr PyQt6
```

### **Solution 3 : Nettoyage et Réinstallation**
```batch
# Supprimer les anciens builds
rmdir /s /q build
rmdir /s /q dist
del *.spec

# Réinstaller
pip install --upgrade PyQt6 openpyxl requests pyinstaller
```

## 📁 Structure des Fichiers

```
MATELAS_FINAL/
├── build_scripts/
│   ├── windows/
│   │   ├── install_ultra_simple.bat          ← RECOMMANDÉ
│   │   ├── build_launcher_ultra_fixe.bat     ← RECOMMANDÉ
│   │   ├── install_windows_fixe.bat
│   │   ├── build_launcher_fixe.bat
│   │   └── build_windows_optimized_fixe.bat
│   └── common/
│       └── diagnostic_windows_fixe.bat
├── requirements_gui.txt
└── GUIDE_DEPANNAGE_WINDOWS_FINAL.md
```

## ✅ Validation Finale

Testez dans cet ordre :

1. **Diagnostic** : `diagnostic_windows_fixe.bat`
2. **Installation** : `install_ultra_simple.bat`
3. **Lancement** : `build_launcher_ultra_fixe.bat`
4. **Test Build** : Option 1 dans le lanceur

**Si tous les tests passent, l'installation est réussie !** 🎉

## 📞 Support

En cas de problème persistant :
1. Vérifiez que Python 3.9+ est installé
2. Vérifiez que pip est dans le PATH
3. Essayez l'installation manuelle
4. Consultez les logs d'erreur détaillés

**Les scripts ultra-simplifiés devraient résoudre tous les problèmes d'encodage !** 🚀 