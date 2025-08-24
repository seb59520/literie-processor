# 🔑 PROBLÈME CLÉS API SOUS WINDOWS - SOLUTIONS

## 🚨 Problème identifié

L'utilisateur signale que les clés LLM OpenRouter ne sont pas détectées sous Windows, alors qu'elles fonctionnent sur macOS.

## 📍 Localisation des fichiers de stockage

### 1. **Stockage sécurisé (recommandé)**
- **Fichier clés chiffrées** : `config/secure_keys.dat`
- **Fichier salt** : `config/salt.dat`
- **Chiffrement** : AES-256 avec PBKDF2
- **Mot de passe** : Variable d'environnement `MATELAS_MASTER_PASSWORD` ou mot de passe par défaut

### 2. **Configuration classique (fallback)**
- **Fichier** : `~/.matelas_config.json` (dossier utilisateur)
- **Format** : JSON non chiffré
- **Clé OpenRouter** : `openrouter_api_key`

### 3. **Variables d'environnement**
- **OpenRouter** : `OPENROUTER_API_KEY`
- **Mot de passe maître** : `MATELAS_MASTER_PASSWORD`

## 🔍 Diagnostic effectué

Le diagnostic a révélé :
- ✅ Stockage sécurisé fonctionnel
- ✅ Configuration classique avec clé OpenRouter présente
- ❌ L'application ne charge pas automatiquement la clé depuis la configuration classique
- ✅ Migration réussie vers le stockage sécurisé

## 🛠️ Solutions pour Windows

### Solution 1 : Migration automatique (recommandée)

```bash
# Exécuter le script de migration
python3 migrer_cles_api.py
```

**Avantages :**
- ✅ Transfert automatique des clés existantes
- ✅ Chiffrement des clés
- ✅ Compatible avec toutes les plateformes
- ✅ Gestion via l'interface graphique

### Solution 2 : Installation de cryptography

```bash
# Installer la dépendance requise
pip install cryptography

# Puis utiliser le gestionnaire de clés API dans l'application
```

### Solution 3 : Variables d'environnement

**Windows (PowerShell) :**
```powershell
$env:MATELAS_MASTER_PASSWORD = "VotreMotDePasseSecurise123!"
$env:OPENROUTER_API_KEY = "sk-or-votre-cle-api-ici"
```

**Windows (CMD) :**
```cmd
set MATELAS_MASTER_PASSWORD=VotreMotDePasseSecurise123!
set OPENROUTER_API_KEY=sk-or-votre-cle-api-ici
```

### Solution 4 : Configuration manuelle

1. **Lancer l'application**
2. **Menu Aide** → **🔐 Gestionnaire de Clés API**
3. **Ajouter une clé** → Service : `openrouter`
4. **Saisir la clé API** et sauvegarder

## 🔧 Dépannage Windows spécifique

### Problème de permissions
```cmd
# Exécuter en tant qu'administrateur
# Ou vérifier les permissions sur le dossier config/
```

### Problème de chemin
```cmd
# Vérifier que le dossier config/ existe
# Créer s'il n'existe pas : mkdir config
```

### Problème de cryptography
```cmd
# Désinstaller et réinstaller
pip uninstall cryptography
pip install cryptography
```

## 📊 Comparaison des méthodes

| Méthode | Sécurité | Facilité | Compatibilité |
|---------|----------|----------|---------------|
| Stockage sécurisé | 🔒🔒🔒 | ⭐⭐⭐ | ✅ Toutes plateformes |
| Configuration classique | 🔒 | ⭐⭐⭐⭐ | ✅ Toutes plateformes |
| Variables d'environnement | 🔒🔒 | ⭐⭐ | ⚠️ Configuration requise |

## 🎯 Recommandations

### Pour Windows
1. **Installer cryptography** : `pip install cryptography`
2. **Migrer les clés existantes** : `python3 migrer_cles_api.py`
3. **Utiliser le gestionnaire de clés API** dans l'application
4. **Vérifier les permissions** sur le dossier `config/`

### Pour la production
1. **Définir MATELAS_MASTER_PASSWORD** comme variable d'environnement
2. **Utiliser le stockage sécurisé** exclusivement
3. **Nettoyer la configuration classique** après migration

## 🔄 Processus de migration

### Étape 1 : Diagnostic
```bash
python3 diagnostic_cles_api_windows.py
```

### Étape 2 : Migration
```bash
python3 migrer_cles_api.py
```

### Étape 3 : Vérification
1. Lancer l'application
2. Aller dans **Menu Aide** → **🔐 Gestionnaire de Clés API**
3. Vérifier que la clé OpenRouter est présente

### Étape 4 : Test
1. Traiter un fichier PDF avec LLM activé
2. Vérifier que la clé est utilisée correctement

## 📝 Fichiers créés

- `diagnostic_cles_api_windows.py` : Script de diagnostic
- `migrer_cles_api.py` : Script de migration
- `RESUME_CLES_API_WINDOWS.md` : Ce document

## 🎉 Résultat attendu

Après la migration :
- ✅ La clé OpenRouter est stockée de manière sécurisée
- ✅ L'application la charge automatiquement
- ✅ Compatible avec Windows, macOS et Linux
- ✅ Interface graphique pour la gestion des clés
- ✅ Chiffrement AES-256 pour la sécurité

## 🆘 Support

En cas de problème :
1. Exécuter le diagnostic : `python3 diagnostic_cles_api_windows.py`
2. Vérifier les logs de l'application
3. Contrôler les permissions sur le dossier `config/`
4. Réinstaller cryptography si nécessaire 