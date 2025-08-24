# 🔧 Guide de Dépannage - Problèmes de Mappings

## ❌ Problème Identifié

**Symptôme :** En mode production (exécutable compilé), tous les champs ne sont pas remplis dans Excel, alors qu'ils fonctionnent en mode développement.

**Cause :** Les fichiers de configuration des mappings (`mappings_matelas.json`, `mappings_sommiers.json`) ne sont pas correctement chargés en mode PyInstaller.

## 🔍 Diagnostic

### **Test 1 : Vérifier les fichiers de configuration**
```bash
# Depuis le dossier racine
ls -la config/
```

**Résultat attendu :**
```
config/
├── mappings_matelas.json
├── mappings_sommiers.json
└── salt.dat
```

### **Test 2 : Tester le chargement des mappings**
```bash
python test_mappings_production.py
```

**Résultat attendu :**
```
=== TEST MAPPINGS PRODUCTION ===

✅ MappingManager importé avec succès

🔍 Test des chemins de configuration:
   mappings_matelas.json: /chemin/vers/config/mappings_matelas.json
   Existe: True
   mappings_sommiers.json: /chemin/vers/config/mappings_sommiers.json
   Existe: True

🔍 Test du MappingManager:
   matelas_mappings_file: /chemin/vers/config/mappings_matelas.json
   sommiers_mappings_file: /chemin/vers/config/mappings_sommiers.json

🔍 Test du chargement des mappings:
   Mappings matelas chargés: 20 entrées
   Mappings sommiers chargés: 35 entrées
```

## ✅ Solutions

### **Solution 1 : Recompiler avec les corrections**
```bash
# Utiliser le script Python corrigé
python build_scripts/windows/build_simple_python.py
```

### **Solution 2 : Vérifier manuellement les mappings**
1. **Lancer l'application**
2. **Aller dans Réglages → Configuration des mappings Excel**
3. **Vérifier que les mappings sont chargés**
4. **Sauvegarder les mappings si nécessaire**

### **Solution 3 : Recréer les fichiers de configuration**
```bash
# Supprimer les anciens fichiers
rm config/mappings_matelas.json
rm config/mappings_sommiers.json

# Relancer l'application pour recréer les mappings par défaut
python app_gui.py
```

## 🔧 Corrections Apportées

### **1. MappingManager.py**
- ✅ **Intégration d'asset_utils** pour la gestion des chemins PyInstaller
- ✅ **Fallback robuste** si asset_utils n'est pas disponible
- ✅ **Gestion des chemins de sauvegarde** en mode production
- ✅ **Logging amélioré** pour le diagnostic

### **2. Script de compilation**
- ✅ **Inclusion explicite** des fichiers de configuration
- ✅ **Vérification pré-compilation** des fichiers requis
- ✅ **Test post-compilation** de l'exécutable
- ✅ **Hidden imports** pour mapping_manager

### **3. Script de test**
- ✅ **Test complet** du chargement des mappings
- ✅ **Validation** des chemins et fichiers
- ✅ **Diagnostic détaillé** des problèmes

## 📋 Vérification Post-Correction

### **Étape 1 : Test en développement**
```bash
python test_mappings_production.py
```

### **Étape 2 : Compilation**
```bash
python build_scripts/windows/build_simple_python.py
```

### **Étape 3 : Test en production**
1. **Lancer l'exécutable** : `dist/MatelasApp.exe`
2. **Traiter un fichier PDF**
3. **Vérifier que tous les champs sont remplis** dans Excel
4. **Vérifier les logs** pour les messages de chargement des mappings

## 🚨 Messages d'Erreur Courants

### **"Fichier de mappings non trouvé"**
```
Mappings matelas chargés depuis None, utilisation des valeurs par défaut
```
**Solution :** Vérifier que `config/mappings_matelas.json` existe

### **"Erreur lors du chargement des mappings"**
```
Erreur lors du chargement des mappings matelas: [Errno 2] No such file or directory
```
**Solution :** Recompiler avec le script corrigé

### **"Mappings vides"**
```
Mappings matelas chargés: 0 entrées
```
**Solution :** Recréer les fichiers de configuration

## 🎯 Résultat Attendu

Après correction, vous devriez voir :

### **Dans les logs :**
```
Mappings matelas chargés depuis /chemin/vers/config/mappings_matelas.json
Mappings sommiers chargés depuis /chemin/vers/config/mappings_sommiers.json
```

### **Dans Excel :**
- ✅ **Tous les champs** sont correctement remplis
- ✅ **Même comportement** qu'en mode développement
- ✅ **Mappings personnalisés** respectés

### **Dans l'interface :**
- ✅ **Configuration des mappings** accessible
- ✅ **Mappings chargés** et affichés
- ✅ **Sauvegarde** fonctionnelle

## 🔄 Procédure de Test Complète

1. **Test en développement** : `python test_mappings_production.py`
2. **Compilation** : `python build_scripts/windows/build_simple_python.py`
3. **Test de l'exécutable** : `dist/MatelasApp.exe`
4. **Traitement d'un fichier** et vérification Excel
5. **Configuration des mappings** via l'interface

**Si tous les tests passent, le problème est résolu !** 🎉 