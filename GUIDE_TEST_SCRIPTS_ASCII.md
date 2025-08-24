# GUIDE DE TEST - SCRIPTS ASCII WINDOWS

## 🎯 OBJECTIF
Tester que les scripts ASCII fonctionnent correctement sur Windows sans erreurs d'encodage.

## ❌ PROBLÈMES RÉSOLUS
- `'ho' n'est pas reconnu en tant que commande interne`
- `'nstallation' n'est pas reconnu en tant que commande interne`
- `'gnostic' n'est pas reconnu en tant que commande interne`
- `'pplication' n'est pas reconnu en tant que commande interne`

## ✅ SOLUTION APPLIQUÉE
Création de scripts .bat **complètement ASCII** sans aucun caractère spécial.

## 📁 FICHIERS À TESTER

### Scripts Principaux
```
build_scripts/windows/
├── menu_ascii.bat                    # MENU PRINCIPAL
├── install_ascii.bat                 # Installation complète
├── lancer_ascii.bat                  # Lancement de l'application
└── diagnostic_ascii.bat              # Diagnostic complet
```

### Script de Lancement Principal
```
Lancer_MatelasApp_ASCII.bat           # Lanceur principal (racine)
```

## 🧪 PROCÉDURE DE TEST

### Étape 1: Test de Base
1. **Double-cliquez** sur `test_scripts_ascii_windows.bat`
2. Vérifiez que tous les scripts sont trouvés
3. Vérifiez que le format est correct

### Étape 2: Test du Menu Principal
1. **Double-cliquez** sur `Lancer_MatelasApp_ASCII.bat`
2. Ou naviguez vers `build_scripts\windows\` et lancez `menu_ascii.bat`
3. Vérifiez que le menu s'affiche correctement

### Étape 3: Test de l'Installation
1. Dans le menu, choisissez l'option **1** (Installation complète)
2. Vérifiez qu'aucune erreur d'encodage n'apparaît
3. L'installation doit se dérouler normalement

### Étape 4: Test du Lancement
1. Dans le menu, choisissez l'option **2** (Lancer l'application)
2. Vérifiez que l'application se lance correctement

### Étape 5: Test du Diagnostic
1. Dans le menu, choisissez l'option **3** (Diagnostic complet)
2. Vérifiez que le diagnostic s'exécute sans erreur

## ✅ RÉSULTATS ATTENDUS

### Avant (Problèmes)
```
'ho' n'est pas reconnu en tant que commande interne
'nstallation' n'est pas reconnu en tant que commande interne
'gnostic' n'est pas reconnu en tant que commande interne
'pplication' n'est pas reconnu en tant que commande interne
```

### Après (Solution)
```
========================================
   MATELASAPP - MENU PRINCIPAL
========================================

Dossier: C:\Users\SEBASTIEN\Desktop\MATELAS_FINAL\build_scripts\windows

Choisissez une option:

[1] Installation complete (recommandee)
[2] Lancer l'application
[3] Diagnostic complet
[4] Nettoyer les builds
[5] Informations
[6] Quitter

Votre choix (1-6):
```

## 🔧 CARACTÉRISTIQUES DES SCRIPTS ASCII

### ✅ Caractéristiques Correctes
- Commencent par `@echo off`
- Utilisent `chcp 65001 >nul` pour UTF-8
- **Aucun caractère spécial** (émojis, accents, symboles)
- **Aucun caractère non-ASCII**
- Syntaxe batch standard Windows

### ❌ Caractéristiques Évitées
- Pas d'émojis (🚀, ✅, ❌, etc.)
- Pas de caractères accentués spéciaux
- Pas de symboles Unicode
- Pas de caractères de contrôle

## 📋 CHECKLIST DE VALIDATION

- [ ] `test_scripts_ascii_windows.bat` s'exécute sans erreur
- [ ] `Lancer_MatelasApp_ASCII.bat` lance le menu principal
- [ ] Le menu principal s'affiche correctement
- [ ] L'option 1 (Installation) fonctionne
- [ ] L'option 2 (Lancement) fonctionne
- [ ] L'option 3 (Diagnostic) fonctionne
- [ ] Aucune erreur d'encodage n'apparaît
- [ ] Tous les messages sont lisibles

## 🚨 EN CAS DE PROBLÈME

Si vous rencontrez encore des erreurs d'encodage :

1. **Vérifiez l'encodage des fichiers** :
   ```cmd
   file "build_scripts\windows\menu_ascii.bat"
   ```

2. **Ouvrez les fichiers dans un éditeur de texte** et vérifiez qu'il n'y a pas de caractères spéciaux

3. **Recréez les scripts** si nécessaire avec un éditeur ASCII pur

4. **Testez sur une machine Windows propre** pour éliminer les problèmes d'environnement

## 📞 SUPPORT

Si les problèmes persistent, fournissez :
- Le contenu exact des erreurs
- La version de Windows
- Le résultat de `test_scripts_ascii_windows.bat`
- Une capture d'écran du menu principal 