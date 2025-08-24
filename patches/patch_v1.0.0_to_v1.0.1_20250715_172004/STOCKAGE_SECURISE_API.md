# 🔐 Système de Stockage Sécurisé des Clés API

## 📋 Vue d'Ensemble

Le système de stockage sécurisé des clés API permet de sauvegarder et gérer les clés API de manière chiffrée et sécurisée directement dans l'application Matelas Processor.

### ✨ Fonctionnalités Principales

- **🔒 Chiffrement AES** : Protection des clés API avec chiffrement AES-256
- **🛡️ Sécurité renforcée** : Utilisation de PBKDF2 avec salt pour la dérivation de clé
- **💾 Stockage local** : Sauvegarde sécurisée sur votre machine
- **🎛️ Interface graphique** : Gestion intuitive via l'application
- **📝 Traçabilité** : Historique des clés avec dates de création/modification
- **🔄 Intégration transparente** : Chargement automatique au démarrage

## 🚀 Installation

### Prérequis

```bash
pip install cryptography>=41.0.0
```

### Vérification de l'Installation

```bash
python3 test_secure_storage.py
```

## 🎯 Utilisation

### Accès au Gestionnaire

1. **Menu Aide** → **🔐 Gestionnaire de Clés API** (raccourci F3)
2. Ou via l'interface principale

### Interface du Gestionnaire

#### 📊 Tableau des Clés API
- **Service** : Nom du service (OpenRouter, Ollama, etc.)
- **Description** : Description personnalisée de la clé
- **Créée le** : Date de création de la clé
- **Actions** : Boutons pour modifier/supprimer

#### 🔧 Boutons d'Action
- **➕ Ajouter une Clé** : Créer une nouvelle clé API
- **🔄 Actualiser** : Recharger la liste des clés
- **🧪 Tester Chiffrement** : Vérifier le bon fonctionnement
- **Fermer** : Fermer le gestionnaire

### Ajout d'une Clé API

1. Cliquez sur **➕ Ajouter une Clé**
2. Remplissez le formulaire :
   - **Service** : Sélectionnez ou saisissez le nom du service
   - **Description** : Description optionnelle
   - **Clé API** : Saisissez votre clé API
3. Cliquez sur **OK** pour sauvegarder

### Modification d'une Clé API

1. Cliquez sur **✏️** dans la colonne Actions
2. Modifiez les champs souhaités
3. Cliquez sur **OK** pour sauvegarder

### Suppression d'une Clé API

1. Cliquez sur **🗑️** dans la colonne Actions
2. Confirmez la suppression
3. La clé est définitivement supprimée

## 🔧 Configuration Avancée

### Variables d'Environnement

Pour une sécurité maximale en production, définissez :

```bash
export MATELAS_MASTER_PASSWORD="VotreMotDePasseSecurise123!"
```

### Fichiers de Stockage

- **Clés chiffrées** : `config/secure_keys.dat`
- **Salt de chiffrement** : `config/salt.dat`

⚠️ **Important** : Ne partagez jamais ces fichiers !

## 🛡️ Sécurité

### Chiffrement Utilisé

- **Algorithme** : AES-256 en mode Fernet
- **Dérivation de clé** : PBKDF2-HMAC-SHA256
- **Salt** : 16 bytes aléatoires
- **Itérations** : 100,000 (recommandé par NIST)

### Bonnes Pratiques

1. **Mot de passe fort** : Utilisez un mot de passe complexe
2. **Variables d'environnement** : En production, utilisez `MATELAS_MASTER_PASSWORD`
3. **Sauvegarde sécurisée** : Sauvegardez les fichiers de configuration
4. **Accès restreint** : Limitez l'accès aux fichiers de configuration

## 🔄 Intégration avec l'Application

### Chargement Automatique

L'application charge automatiquement les clés API au démarrage :

1. **Priorité 1** : Stockage sécurisé
2. **Priorité 2** : Configuration classique
3. **Fallback** : Saisie manuelle

### Services Supportés

- **OpenRouter** : `openrouter`
- **Ollama** : `ollama`
- **Anthropic** : `anthropic`
- **OpenAI** : `openai`
- **Google** : `google`
- **Personnalisé** : `custom`

## 🧪 Tests et Validation

### Test de Chiffrement

Le bouton **🧪 Tester Chiffrement** vérifie :

- Génération du salt
- Dérivation de clé
- Chiffrement/déchiffrement
- Intégrité des données

### Script de Test Complet

```bash
python3 test_secure_storage.py
```

Ce script teste :
- Import du module
- Test de chiffrement
- Sauvegarde/chargement
- Gestion des informations
- Liste des services
- Suppression
- Gestion multiple

## 📝 Logs et Debugging

### Messages de Log

L'application enregistre toutes les opérations :

```
INFO - Clé API OpenRouter chargée depuis le stockage sécurisé
INFO - Clé API 'openrouter' sauvegardée avec succès
INFO - Gestionnaire de clés API affiché
```

### Dépannage

#### Erreur d'Import
```
Module de stockage sécurisé non disponible
```
**Solution** : `pip install cryptography`

#### Erreur de Chiffrement
```
Test de chiffrement échoué
```
**Solution** : Vérifiez les permissions sur le dossier `config/`

#### Clé Non Trouvée
```
Aucune clé API OpenRouter trouvée
```
**Solution** : Ajoutez la clé via le gestionnaire

## 🔄 Migration depuis l'Ancien Système

### Migration Automatique

L'application migre automatiquement :

1. **Détection** : Vérifie la présence de clés dans l'ancien système
2. **Migration** : Transfère vers le stockage sécurisé
3. **Validation** : Vérifie l'intégrité des données
4. **Nettoyage** : Supprime les anciennes données

### Migration Manuelle

Si nécessaire, vous pouvez migrer manuellement :

1. Ouvrez le gestionnaire de clés API
2. Ajoutez vos clés existantes
3. Supprimez les anciennes configurations

## 📊 Avantages

### Sécurité
- ✅ Chiffrement AES-256
- ✅ Salt unique par installation
- ✅ Dérivation de clé sécurisée
- ✅ Protection contre les attaques par force brute

### Facilité d'Usage
- ✅ Interface graphique intuitive
- ✅ Chargement automatique
- ✅ Gestion centralisée
- ✅ Traçabilité complète

### Flexibilité
- ✅ Support de multiples services
- ✅ Descriptions personnalisées
- ✅ Migration transparente
- ✅ Configuration avancée

## 🚨 Limitations et Recommandations

### Limitations
- ⚠️ Stockage local uniquement
- ⚠️ Dépendance à la bibliothèque cryptography
- ⚠️ Mot de passe maître requis

### Recommandations
- 🔐 Utilisez un mot de passe fort
- 🔐 Sauvegardez les fichiers de configuration
- 🔐 Limitez l'accès aux fichiers
- 🔐 Testez régulièrement le chiffrement

## 🔮 Évolutions Futures

### Fonctionnalités Prévues
- 🔄 Synchronisation cloud sécurisée
- 🔑 Rotation automatique des clés
- 📊 Audit trail complet
- 🔐 Support de clés hardware (HSM)

### Améliorations Techniques
- 🚀 Performance optimisée
- 🔒 Chiffrement multi-couches
- 📱 Interface mobile
- 🌐 Support multi-utilisateurs

## 📞 Support

### Documentation
- Ce fichier : `STOCKAGE_SECURISE_API.md`
- Guide d'aide intégré dans l'application
- Tests de validation : `test_secure_storage.py`

### Dépannage
1. Vérifiez l'installation : `pip install cryptography`
2. Testez le système : `python3 test_secure_storage.py`
3. Consultez les logs de l'application
4. Vérifiez les permissions des fichiers

---

**Version** : 1.0  
**Date** : 2025-07-10  
**Auteur** : Matelas Processor Team 