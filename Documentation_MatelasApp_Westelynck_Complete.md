# DOCUMENTATION COMPLÈTE - MATELASAPP WESTELYNCK

## 📋 TABLE DES MATIÈRES

1. [Vue d'ensemble](#vue-densemble)
2. [Système de dates et semaines](#système-de-dates-et-semaines)
3. [Système d'alertes en temps réel](#système-dalertes-en-temps-réel)
4. [Modules de création et construction](#modules-de-création-et-construction)
5. [Scripts de build manuels](#scripts-de-build-manuels)
6. [Installation et configuration](#installation-et-configuration)
7. [Utilisation](#utilisation)
8. [Dépannage](#dépannage)
9. [Maintenance](#maintenance)

---

## 🎯 VUE D'ENSEMBLE

**MatelasApp Westelynck** est une application de traitement automatisé de commandes de literie développée pour Westelynck. Elle permet d'analyser des fichiers PDF de commandes, d'extraire les informations de matelas et sommiers, et de générer des fichiers Excel formatés pour la production.

### Fonctionnalités principales
- 📄 **Analyse PDF** : Extraction automatique des données de commandes
- 🤖 **IA/LLM** : Enrichissement des données via intelligence artificielle
- 📊 **Génération Excel** : Création de fichiers de production formatés
- 🎨 **Coloration automatique** : Mise en forme visuelle des données
- 📅 **Gestion des semaines** : Organisation par semaines de production
- 🔔 **Alertes temps réel** : Notifications en temps réel
- 🏗️ **Build automatisé** : Compilation et déploiement simplifiés

---

## 📅 SYSTÈME DE DATES ET SEMAINES

### Format des semaines de production
```
S{numéro_semaine}_{année}
Exemple: S31_2025 (Semaine 31 de 2025)
```

### Gestion automatique des dates
- **Détection automatique** de la semaine courante
- **Calcul automatique** de la semaine suivante
- **Format standardisé** : `S{WW}_{YYYY}`

### Fonctionnalités de dates
```python
# Exemple de génération de nom de fichier
nom_fichier = f"Matelas_S{numero_semaine}_{annee}_{compteur}.xlsx"
# Résultat: Matelas_S31_2025_1.xlsx
```

### Configuration des semaines
- **Fichier de configuration** : `backend/Référentiels/semaines_production.json`
- **Format JSON** avec mapping semaine → dates
- **Mise à jour automatique** lors de la création de fichiers

---

## 🔔 SYSTÈME D'ALERTES EN TEMPS RÉEL

### Architecture des alertes
```
AlertSystem
├── AlertManager (Gestionnaire principal)
├── AlertWidget (Interface utilisateur)
├── AlertTypes (Types d'alertes)
└── AlertQueue (File d'attente)
```

### Types d'alertes disponibles
- ✅ **Success** : Opérations réussies
- ⚠️ **Warning** : Avertissements
- ❌ **Error** : Erreurs critiques
- ℹ️ **Info** : Informations générales
- 🔄 **Progress** : Progression des opérations

### Caractéristiques des alertes
- **Affichage automatique** en temps réel
- **Fermeture automatique** après délai configurable
- **Historique** des alertes récentes
- **Actions utilisateur** (fermer, effacer tout)
- **Intégration GUI** avec PyQt6

### Exemple d'utilisation
```python
# Ajout d'une alerte
self.alert_system.add_alert("success", "Traitement terminé")

# Alerte avec fermeture automatique
self.alert_system.add_alert("info", "Début du traitement", auto_close=True)
```

### Configuration des alertes
- **Durée d'affichage** : 5 secondes par défaut
- **Position** : Coin supérieur droit
- **Style** : Thème cohérent avec l'interface
- **Animations** : Apparition/disparition fluides

---

## 🏗️ MODULES DE CRÉATION ET CONSTRUCTION

### Architecture modulaire
```
MatelasApp/
├── app_gui.py                 # Interface principale
├── backend/                   # Modules backend
│   ├── llm_provider.py       # Fournisseurs IA
│   ├── excel_import_utils.py # Utilitaires Excel
│   ├── pdf_utils.py          # Traitement PDF
│   └── date_utils.py         # Gestion des dates
├── build_scripts/            # Scripts de build
│   └── windows/              # Scripts Windows
└── assets/                   # Ressources
```

### Modules principaux

#### 1. **LLM Provider** (`backend/llm_provider.py`)
- **Gestion multi-providers** : OpenAI, OpenRouter, Ollama
- **Configuration centralisée** des clés API
- **Fallback automatique** en cas d'erreur
- **Cache intelligent** des réponses

#### 2. **Excel Import Utils** (`backend/excel_import_utils.py`)
- **Génération Excel** avec formatage avancé
- **Coloration automatique** selon les données
- **Alignement intelligent** des cellules
- **Gestion des templates** matelas/sommiers

#### 3. **PDF Utils** (`backend/pdf_utils.py`)
- **Extraction de texte** depuis PDF
- **Pré-analyse** du contenu
- **Détection automatique** matelas/sommiers
- **Validation** des fichiers

#### 4. **Date Utils** (`backend/date_utils.py`)
- **Calcul des semaines** de production
- **Formatage des dates** standardisé
- **Gestion des référentiels** temporels

### Système de templates
```
backend/template/
├── template_matelas.xlsx     # Template matelas
└── template_sommier.xlsx     # Template sommiers
```

### Référentiels de données
```
backend/Référentiels/
├── dimensions_matelas.json   # Dimensions standard
├── longueurs_matelas.json    # Longueurs disponibles
├── configurations.json       # Configurations types
└── semaines_production.json  # Planning production
```

---

## 🔧 SCRIPTS DE BUILD MANUELS

### Scripts ASCII Windows (Recommandés)

#### 1. **Menu Principal** (`build_scripts/windows/menu_ascii.bat`)
```batch
@echo off
chcp 65001 >nul

:menu
cls
echo ========================================
echo    MATELASAPP - MENU PRINCIPAL
echo ========================================
echo.
echo Dossier: %CD%
echo.
echo Choisissez une option:
echo.
echo [1] Installation complete (recommandee)
echo [2] Lancer l'application
echo [3] Diagnostic complet
echo [4] Nettoyer les builds
echo [5] Informations
echo [6] Quitter
echo.
set /p choice="Votre choix (1-6): "
```

#### 2. **Installation Complète** (`build_scripts/windows/install_ascii.bat`)
- **Installation des dépendances** Python
- **Compilation PyInstaller** automatique
- **Vérification** de l'environnement
- **Test** de l'exécutable généré

#### 3. **Lancement** (`build_scripts/windows/lancer_ascii.bat`)
- **Détection** de l'exécutable
- **Lancement** automatique
- **Fallback** vers installation si nécessaire

#### 4. **Diagnostic** (`build_scripts/windows/diagnostic_ascii.bat`)
- **Vérification Python** et dépendances
- **Test** des fichiers de configuration
- **Validation** des ressources
- **Rapport** détaillé

### Scripts de test

#### Test Mac (`test_scripts_ascii_mac.sh`)
```bash
#!/bin/bash
echo "========================================"
echo "   TEST DES SCRIPTS ASCII (MAC)"
echo "========================================"

# Vérification des fichiers
if [ -f "build_scripts/windows/menu_ascii.bat" ]; then
    echo "menu_ascii.bat: OK"
else
    echo "menu_ascii.bat: MANQUANT"
fi
```

#### Test Windows (`test_scripts_ascii_windows.bat`)
```batch
@echo off
echo ========================================
echo    TEST DES SCRIPTS ASCII
echo ========================================
echo.
echo Test des scripts ASCII sans caracteres speciaux...
echo.

REM Test du menu principal
if exist "build_scripts\windows\menu_ascii.bat" (
    echo [1/4] Test du menu principal...
    echo OK: menu_ascii.bat trouve
) else (
    echo [1/4] Test du menu principal...
    echo ERREUR: menu_ascii.bat manquant
)
```

### Caractéristiques des scripts ASCII
- ✅ **Aucun caractère spécial** (émojis, accents, symboles)
- ✅ **Format ASCII pur** compatible Windows
- ✅ **Syntaxe batch standard** sans caractères problématiques
- ✅ **Encodage UTF-8** avec `chcp 65001`
- ✅ **Début correct** avec `@echo off`

---

## 📦 INSTALLATION ET CONFIGURATION

### Prérequis système
- **Python 3.8+** (recommandé 3.11+)
- **PyQt6** pour l'interface graphique
- **PyInstaller** pour la compilation
- **Windows 10/11** (pour les scripts batch)

### Installation automatique
```batch
# Double-cliquer sur
Lancer_MatelasApp_ASCII.bat

# Ou lancer directement
build_scripts\windows\menu_ascii.bat
```

### Installation manuelle
```bash
# 1. Cloner le projet
git clone [repository_url]
cd MATELAS_FINAL

# 2. Installer les dépendances
pip install -r requirements_gui.txt

# 3. Lancer l'application
python app_gui.py
```

### Configuration des clés API
```json
{
  "openrouter": {
    "api_key": "votre_clé_api_ici",
    "base_url": "https://openrouter.ai/api/v1"
  },
  "openai": {
    "api_key": "votre_clé_api_ici",
    "base_url": "https://api.openai.com/v1"
  }
}
```

---

## 🚀 UTILISATION

### Lancement de l'application
1. **Double-cliquer** sur `Lancer_MatelasApp_ASCII.bat`
2. **Choisir** l'option 1 pour l'installation complète
3. **Attendre** la compilation PyInstaller
4. **Lancer** l'application via l'option 2

### Interface utilisateur
- **Panneau gauche** : Contrôles et configuration
- **Panneau central** : Sélection de fichiers
- **Panneau droit** : Résultats et prévisualisation
- **Barre de statut** : Informations en temps réel

### Traitement des commandes
1. **Sélectionner** les fichiers PDF de commandes
2. **Configurer** le provider LLM (OpenRouter recommandé)
3. **Lancer** le traitement
4. **Vérifier** les résultats dans le panneau droit
5. **Ouvrir** les fichiers Excel générés

### Gestion des semaines
- **Détection automatique** de la semaine courante
- **Génération automatique** des noms de fichiers
- **Organisation** par semaines de production
- **Historique** des traitements

---

## 🔧 DÉPANNAGE

### Problèmes courants

#### 1. **Erreurs d'encodage Windows**
```
'ho' n'est pas reconnu en tant que commande interne
```
**Solution** : Utiliser les scripts ASCII (`*_ascii.bat`)

#### 2. **Erreurs de clé API**
```
401 Client Error: Unauthorized
```
**Solution** : Vérifier la clé API dans l'interface de gestion

#### 3. **Erreurs PyQt6**
```
ImportError: cannot import name 'QAction' from 'PyQt6.QtWidgets'
```
**Solution** : Réinstaller PyQt6 avec `pip install --upgrade PyQt6`

#### 4. **Erreurs de compilation**
```
PyInstaller: error: no module named 'backend'
```
**Solution** : Utiliser le script d'installation complet

### Scripts de diagnostic
```batch
# Diagnostic complet
build_scripts\windows\diagnostic_ascii.bat

# Test rapide
test_rapide_ascii.bat

# Test détaillé
test_scripts_ascii_windows.bat
```

### Logs et debugging
- **Fichier de log** : `logs/matelas_app.log`
- **Logs d'erreur** : `logs/matelas_errors.log`
- **Logs admin** : `logs/admin_operations.log`

---

## 🛠️ MAINTENANCE

### Mise à jour de l'application
1. **Sauvegarder** les configurations importantes
2. **Télécharger** la nouvelle version
3. **Remplacer** les fichiers (sauf config/)
4. **Relancer** l'installation

### Sauvegarde des données
- **Configuration** : `config/` (clés API, mappings)
- **Référentiels** : `backend/Référentiels/`
- **Templates** : `backend/template/`
- **Logs** : `logs/`

### Nettoyage des builds
```batch
# Option 4 du menu principal
build_scripts\windows\menu_ascii.bat

# Ou directement
build_scripts\windows\clean_ascii.bat
```

### Monitoring et performance
- **Vérification** des logs régulière
- **Nettoyage** des fichiers temporaires
- **Mise à jour** des dépendances
- **Sauvegarde** des configurations

---

## 📞 SUPPORT ET CONTACT

### Documentation disponible
- `GUIDE_INSTALLATION.md` - Guide d'installation
- `GUIDE_TEST_SCRIPTS_ASCII.md` - Test des scripts
- `RESUME_SCRIPTS_ASCII_FINAL.md` - Résumé des scripts
- `CHANGELOG.md` - Historique des versions

### En cas de problème
1. **Consulter** la documentation
2. **Exécuter** les scripts de diagnostic
3. **Vérifier** les logs d'erreur
4. **Contacter** le support technique

### Informations système
- **Version** : 3.0.1
- **Dernière mise à jour** : 19/07/2025
- **Compatibilité** : Windows 10/11, macOS, Linux
- **Langage** : Python 3.8+
- **Interface** : PyQt6

---

## ✅ CONCLUSION

MatelasApp Westelynck est une solution complète et robuste pour le traitement automatisé des commandes de literie. Avec son système d'alertes en temps réel, sa gestion intelligente des dates et ses scripts de build optimisés, elle offre une expérience utilisateur fluide et professionnelle.

Les scripts ASCII garantissent une compatibilité maximale avec Windows, éliminant les problèmes d'encodage courants. Le système modulaire permet une maintenance facile et des évolutions futures.

**Pour commencer** : Double-cliquez sur `Lancer_MatelasApp_ASCII.bat` et suivez les instructions du menu principal. 