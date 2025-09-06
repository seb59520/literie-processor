# MATELAS Application Portable v3.11.12

## 🚀 Installation Rapide

### Prérequis
- Python 3.8+
- Connexion Internet (pour l'installation des dépendances)

### Installation Automatique
```bash
python3 install.py
```

### Installation Manuelle
```bash
pip install PyQt6 requests PyMuPDF openpyxl paramiko cryptography
python3 app_gui.py
```

## 📁 Structure du Projet

```
MATELAS_PORTABLE/
├── app_gui.py                    # Application principale
├── install.py                    # Script d'installation
├── config.py                     # Configuration système
├── version.py                     # Gestion des versions
├── package_builder.py            # Générateur de packages
├── package_builder_gui.py        # Interface générateur manuel
├── auto_package_generator.py     # Générateur automatique
├── auto_package_gui.py          # Interface générateur auto
├── package_consolidator.py      # Consolidateur de packages
├── backend/                     # Modules de traitement
├── config/                      # Configurations
├── template/                    # Templates Excel
└── consolidated_packages/       # Packages consolidés
```

## 🎯 Nouvelles Fonctionnalités v3.11.12

### 📦 Générateur de Packages Correctifs
- **Création manuelle** : Menu Diagnostic → Créer Package Correctif
- **Suggestions automatiques** : Menu Diagnostic → Suggestions Automatiques
- **Consolidation** : Menu Diagnostic → Consolidation & Upload VPS
- **Protection** : Accès protégé par mot de passe développeur

### 🌐 Configuration Serveur
- **VPS intégré** : Serveur de mise à jour sur VPS dédié
- **Upload automatique** : Envoi des packages vers le serveur
- **Configuration** : Menu Configuration → Configuration Serveur

## 🔧 Configuration

### Premier Lancement
1. Lancer `python3 app_gui.py`
2. Configurer les clés API (Menu Configuration)
3. Vérifier l'URL du serveur (72.60.47.183)
4. Tester avec un PDF exemple

### URLs et Serveurs
- **Serveur principal** : http://72.60.47.183/
- **Interface admin** : http://72.60.47.183/admin
- **API** : http://72.60.47.183/api/v1/

## 🛠️ Outils Développeur

### Générateur de Packages
- **Mot de passe** : `matelas_dev_2025`
- **Packages manuels** : Sélection de fichiers personnalisée
- **Packages automatiques** : Détection des modifications récentes
- **Consolidation** : Fusion de packages par version

### Types de Packages Détectés
- 🖥️ **Interface** : Modifications GUI et interfaces
- ⚙️ **Backend** : Utilitaires et traitement
- 📋 **Configuration** : Paramètres système
- 🛠️ **Scripts** : Outils et utilitaires
- 📊 **Référentiels** : Données métier
- 📄 **Templates** : Modèles Excel

## 🚨 Dépannage

### Problèmes Courants
- **Erreur PyQt6** : `pip install --upgrade PyQt6`
- **Connexion serveur** : Vérifier l'URL dans Configuration
- **Permissions** : Exécuter en tant qu'administrateur si nécessaire
- **Dépendances** : Relancer `python3 install.py`

### Logs
Les logs sont dans le répertoire `logs/` :
- `app.log` : Log principal de l'application
- `errors.log` : Erreurs système
- `processing.log` : Traitement des PDFs

### Support
- Consulter les logs en cas de problème
- Vérifier la configuration réseau
- Tester avec un PDF simple d'abord

## 📋 Changelog v3.11.12

### ⚙️ Backend/Traitement
- Améliorations des utilitaires de traitement
- Optimisations des performances
- Corrections de bugs système

### 📋 Configuration  
- Mise à jour des paramètres système
- Correction des URLs de serveur
- Optimisation des configurations LLM

### 🖥️ Interface Utilisateur
- Nouvelles fonctionnalités GUI
- Générateur de packages correctifs
- Améliorations ergonomiques

### 🛠️ Scripts/Utilitaires
- Nouveaux outils de maintenance
- Scripts d'automatisation
- Utilitaires de diagnostic

## 📞 Contact
- Documentation complète dans l'application
- Aide contextuelle via F1
- Support technique via les logs système
