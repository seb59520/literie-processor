# 🚀 MATELAS Application v3.11.12 - Guide d'Installation

## 📦 Package Portable Complet

**Fichier:** `MATELAS_v3.11.12_PORTABLE_20250905_210130.zip`
- **Taille:** 1.0 MB (compressé à 58.5%)
- **Fichiers:** 166 composants
- **Version:** 3.11.12 avec toutes les nouvelles fonctionnalités

## 🎯 Nouvelles Fonctionnalités v3.11.12

### 📦 **Générateur de Packages Correctifs**
- **Création manuelle** de packages ZIP avec sélection de fichiers
- **Suggestions automatiques** basées sur les modifications récentes
- **Consolidation intelligente** de packages par version
- **Upload automatique** vers VPS via SFTP
- **Protection par mot de passe** : `matelas_dev_2025`

### 🤖 **Système Automatique**
- **Détection des changements** : Interface, Backend, Configuration, Scripts, Référentiels, Templates
- **Categorisation intelligente** des modifications
- **Priorisation automatique** (critique, important, normal)
- **Changelog détaillé** généré automatiquement

### 🌐 **Intégration VPS**
- **Serveur dédié** : http://72.60.47.183/
- **Interface d'administration** : http://72.60.47.183/admin
- **Upload SFTP** automatique des packages
- **Configuration centralisée** des mises à jour

## 🔧 Installation sur Nouveau Poste

### Prérequis
- **Python 3.8+** (recommandé : Python 3.9+)
- **Connexion Internet** (pour installation des dépendances)
- **10 Go d'espace libre** sur le disque

### Étapes d'Installation

#### 1. **Transfert du Package**
```bash
# Copier le fichier ZIP sur le nouveau poste
scp MATELAS_v3.11.12_PORTABLE_20250905_210130.zip user@hostname:/path/to/install/
```

#### 2. **Extraction**
```bash
# Créer un répertoire d'installation
mkdir ~/MATELAS
cd ~/MATELAS

# Ou sur Windows
md C:\MATELAS
cd C:\MATELAS

# Extraire l'archive
unzip MATELAS_v3.11.12_PORTABLE_20250905_210130.zip
```

#### 3. **Installation Automatique**
```bash
# Exécuter le script d'installation
python3 install.py
```

Le script installe automatiquement :
- PyQt6 (interface graphique)
- requests (communication HTTP)
- PyMuPDF (traitement PDF)
- openpyxl (génération Excel)
- paramiko (SFTP pour upload)
- cryptography (sécurité)

#### 4. **Lancement**
```bash
# Démarrage de l'application
python3 app_gui.py

# Ou utiliser les scripts de lancement
# Windows : lancer_matelas.bat
# Unix/Mac : ./lancer_matelas.sh
```

## 🛠️ Configuration Initiale

### 1. **Vérification du Serveur**
- Menu **Configuration** → **Configuration Serveur**
- URL par défaut : `http://72.60.47.183/`
- Tester la connexion

### 2. **Configuration LLM**
- Menu **Configuration** → **Configurer les clés API**
- Choisir le fournisseur (OpenRouter recommandé)
- Saisir la clé API

### 3. **Test de Fonctionnement**
- Charger un PDF test
- Vérifier la génération Excel
- Tester les nouvelles fonctionnalités

## 📋 Nouvelles Fonctionnalités Développeur

### 🔑 **Accès Protégé**
**Mot de passe développeur:** `matelas_dev_2025`

### 📦 **Menu Diagnostic**
- **Créer Package Correctif…** : Création manuelle de packages
- **Suggestions Automatiques…** : Analyse et suggestions intelligentes  
- **Consolidation & Upload VPS…** : Regroupement et upload vers serveur

### 🤖 **Détection Automatique**
Le système détecte et catégorise automatiquement :

| Type | Description | Icône |
|------|-------------|-------|
| Interface | app_gui.py, interfaces utilisateur | 🖥️ |
| Backend | backend/*.py, utilitaires de traitement | ⚙️ |
| Configuration | *.json, paramètres système | 📋 |
| Scripts | outils et utilitaires | 🛠️ |
| Référentiels | backend/Référentiels/*.json | 📊 |
| Templates | template/*.xlsx | 📄 |

### 📤 **Upload VPS**
Configuration automatique pour :
- **Host:** 72.60.47.183
- **User:** root
- **Protocole:** SFTP
- **Répertoire distant:** `/var/www/html/update_storage/updates/`

## 🎉 **Exemple de Package Consolidé**

Le système a automatiquement créé :
**`matelas_v3.11.12_consolidated_20250905_205250.zip`**

**Changelog généré :**
```
MISE À JOUR CONSOLIDÉE v3.11.12:

⚙️ BACKEND/TRAITEMENT:
   • Améliorations des utilitaires de traitement
   • Optimisations des performances
   • Corrections de bugs système

📋 CONFIGURATION:
   • Mise à jour des paramètres système
   • Correction des URLs de serveur
   • Optimisation des configurations LLM

🖥️ INTERFACE UTILISATEUR:
   • Nouvelles fonctionnalités GUI
   • Générateur de packages correctifs
   • Améliorations ergonomiques

🛠️ SCRIPTS/UTILITAIRES:
   • Nouveaux outils de maintenance
   • Scripts d'automatisation
   • Utilitaires de diagnostic

⚠️ IMPORTANT:
   • Redémarrage de l'application requis
   • Sauvegarde automatique avant installation
   • 5 packages consolidés
```

## 🚨 Dépannage

### Erreurs Communes

#### **"Module PyQt6 not found"**
```bash
pip3 install --upgrade PyQt6
```

#### **"Permission denied"**
```bash
# Linux/Mac
sudo python3 install.py

# Windows : Exécuter en tant qu'Administrateur
```

#### **"Connection refused to VPS"**
- Vérifier la configuration réseau
- Tester : `ping 72.60.47.183`
- Vérifier les paramètres proxy

### Logs de Débogage
```bash
# Consulter les logs
ls logs/
cat logs/app.log
cat logs/errors.log
```

## 📞 Support

- **Documentation** : Menu Aide → Guide utilisateur (F1)
- **Logs** : Répertoire `logs/` pour diagnostic
- **Configuration** : Fichier `matelas_config.json`
- **Réinitialisation** : Supprimer `config/secure_keys.dat`

---

**✅ Installation terminée avec succès !**
**L'application MATELAS v3.11.12 est maintenant prête à l'emploi avec toutes les nouvelles fonctionnalités de génération de packages correctifs.**