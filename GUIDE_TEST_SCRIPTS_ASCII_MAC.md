# GUIDE DE TEST - SCRIPTS ASCII (VERSION MAC)

## 🎯 OBJECTIF
Tester que les scripts ASCII Windows sont correctement créés depuis Mac.

## ❌ PROBLÈME IDENTIFIÉ
Le script de test Windows ne fonctionne pas sur Mac car il utilise des chemins Windows (`build_scripts\windows\`) au lieu des chemins Unix (`build_scripts/windows/`).

## ✅ SOLUTION CRÉÉE
Script de test adapté pour Mac : `test_scripts_ascii_mac.sh`

## 🧪 PROCÉDURE DE TEST SUR MAC

### Étape 1: Test des Scripts ASCII
```bash
./test_scripts_ascii_mac.sh
```

### Étape 2: Vérification Manuelle
```bash
# Vérifier que les fichiers existent
ls -la build_scripts/windows/*ascii*.bat

# Vérifier l'encodage
file build_scripts/windows/menu_ascii.bat

# Afficher le contenu
head -20 build_scripts/windows/menu_ascii.bat
```

## 📁 FICHIERS À VÉRIFIER

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

## ✅ RÉSULTATS ATTENDUS

### Test sur Mac
```
========================================
   TEST DES SCRIPTS ASCII (MAC)
========================================

[1/5] Verification des fichiers...
menu_ascii.bat: OK
install_ascii.bat: OK
lancer_ascii.bat: OK
diagnostic_ascii.bat: OK
Lancer_MatelasApp_ASCII.bat: OK

[2/5] Verification du format ASCII...
menu_ascii.bat: FORMAT ASCII OK
install_ascii.bat: FORMAT ASCII OK

[3/5] Verification de l'encodage...
menu_ascii.bat: ENCODAGE ASCII OK
install_ascii.bat: ENCODAGE ASCII OK

[4/5] Apercu du contenu...
Premieres lignes de menu_ascii.bat:
@echo off
chcp 65001 >nul

:menu
cls
echo ========================================
echo    MATELASAPP - MENU PRINCIPAL
echo ========================================

[5/5] Verification des caracteres speciaux...
menu_ascii.bat: AUCUN caractere special detecte
install_ascii.bat: AUCUN caractere special detecte
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

## 📋 CHECKLIST DE VALIDATION SUR MAC

- [ ] `test_scripts_ascii_mac.sh` s'exécute sans erreur
- [ ] Tous les fichiers `.bat` sont trouvés
- [ ] Le format ASCII est correct (`@echo off` présent)
- [ ] L'encodage est ASCII
- [ ] Aucun caractère spécial n'est détecté
- [ ] Le contenu est lisible et correct

## 🚀 PROCHAINES ÉTAPES

### Pour Tester sur Windows
1. **Copiez le dossier** `MATELAS_FINAL` sur un PC Windows
2. **Double-cliquez** sur `Lancer_MatelasApp_ASCII.bat`
3. **Ou lancez** `build_scripts\windows\menu_ascii.bat`
4. **Vérifiez** qu'aucune erreur d'encodage n'apparaît

### Résultats Attendus sur Windows
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

## 🚨 EN CAS DE PROBLÈME

Si vous rencontrez des problèmes sur Mac :

1. **Vérifiez les permissions** :
   ```bash
   chmod +x test_scripts_ascii_mac.sh
   ```

2. **Vérifiez l'encodage** :
   ```bash
   file build_scripts/windows/menu_ascii.bat
   ```

3. **Vérifiez le contenu** :
   ```bash
   cat build_scripts/windows/menu_ascii.bat
   ```

## 📞 SUPPORT

Si les problèmes persistent, fournissez :
- Le résultat de `./test_scripts_ascii_mac.sh`
- Le résultat de `file build_scripts/windows/menu_ascii.bat`
- Les premières lignes du fichier avec `head -10 build_scripts/windows/menu_ascii.bat` 