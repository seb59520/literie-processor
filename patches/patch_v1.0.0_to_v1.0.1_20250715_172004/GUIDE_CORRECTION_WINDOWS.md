# 🔧 GUIDE DE CORRECTION WINDOWS - CLÉ API OPENROUTER

## 🎯 PROBLÈME IDENTIFIÉ

**Symptôme** : Sous Windows, vous recevez le message "Clé API OpenRouter requise" alors que la clé est configurée.

**Cause probable** : Différences dans la gestion des fichiers de configuration entre Windows et macOS/Linux.

## 🔍 DIAGNOSTIC RAPIDE

### 1. Vérifier le fichier de configuration
```bash
# Ouvrir l'Explorateur de fichiers
# Aller dans : C:\Users\[votre_nom]\.matelas_config.json
```

**Le fichier doit contenir** :
```json
{
  "openrouter_api_key": "sk-or-v1-votre-clé-ici",
  "provider": "openrouter"
}
```

### 2. Vérifier les variables d'environnement
```cmd
# Ouvrir l'invite de commande et taper :
echo %OPENROUTER_API_KEY%
```

## 🛠️ SOLUTIONS

### Solution 1 : Correction automatique (Recommandée)

1. **Exécuter le script de diagnostic** :
   ```cmd
   python diagnostic_cles_windows.py
   ```

2. **Exécuter le script de correction** :
   ```cmd
   python corriger_cles_windows.py
   ```

3. **Suivre les instructions** pour configurer votre clé API

### Solution 2 : Configuration manuelle

#### Étape 1 : Créer/Modifier le fichier de configuration

1. Ouvrir le Bloc-notes en tant qu'administrateur
2. Créer le fichier : `C:\Users\[votre_nom]\.matelas_config.json`
3. Ajouter le contenu :
   ```json
   {
     "openrouter_api_key": "sk-or-v1-votre-clé-ici",
     "provider": "openrouter"
   }
   ```
4. Sauvegarder avec l'encodage UTF-8

#### Étape 2 : Définir la variable d'environnement

**Méthode A - Interface graphique** :
1. Clic droit sur "Ce PC" → Propriétés
2. Paramètres système avancés
3. Variables d'environnement
4. Nouvelle variable utilisateur :
   - Nom : `OPENROUTER_API_KEY`
   - Valeur : `sk-or-v1-votre-clé-ici`

**Méthode B - Ligne de commande** :
```cmd
setx OPENROUTER_API_KEY "sk-or-v1-votre-clé-ici"
```

**Méthode C - PowerShell** :
```powershell
[Environment]::SetEnvironmentVariable("OPENROUTER_API_KEY", "sk-or-v1-votre-clé-ici", "User")
```

### Solution 3 : Scripts automatiques

#### Script Batch (configurer_openrouter_windows.bat)
```batch
@echo off
echo Configuration de la variable d'environnement OPENROUTER_API_KEY...
set OPENROUTER_API_KEY=sk-or-v1-votre-clé-ici
setx OPENROUTER_API_KEY "sk-or-v1-votre-clé-ici"
echo Variable configurée ! Redémarrez l'application.
pause
```

#### Script PowerShell (configurer_openrouter_windows.ps1)
```powershell
Write-Host "Configuration OpenRouter..." -ForegroundColor Green
$env:OPENROUTER_API_KEY = "sk-or-v1-votre-clé-ici"
[Environment]::SetEnvironmentVariable("OPENROUTER_API_KEY", "sk-or-v1-votre-clé-ici", "User")
Write-Host "Configuration terminée !" -ForegroundColor Green
```

## 🔄 ÉTAPES DE VÉRIFICATION

### 1. Redémarrer l'application
```cmd
python app_gui.py
```

### 2. Vérifier dans l'interface
- Onglet "Configuration" → Provider LLM = "openrouter"
- Aucun message d'erreur de clé API

### 3. Tester avec un fichier PDF
- Charger un fichier PDF de commande
- Vérifier que le traitement fonctionne

## 🚨 DÉPANNAGE

### Problème : "Fichier non trouvé"
**Solution** : Vérifier le chemin du fichier de configuration
```cmd
dir C:\Users\%USERNAME%\.matelas_config.json
```

### Problème : "Permission refusée"
**Solution** : Exécuter en tant qu'administrateur
1. Clic droit sur l'invite de commande
2. "Exécuter en tant qu'administrateur"

### Problème : "Clé invalide"
**Solution** : Vérifier la clé API
1. Aller sur https://openrouter.ai/keys
2. Vérifier que la clé est active
3. Copier la clé complète (commence par `sk-or-v1-`)

### Problème : "Encodage incorrect"
**Solution** : Sauvegarder en UTF-8
1. Bloc-notes → Fichier → Enregistrer sous
2. Encodage : UTF-8
3. Nom : `.matelas_config.json`

## 📋 CHECKLIST DE VÉRIFICATION

- [ ] Fichier `C:\Users\[votre_nom]\.matelas_config.json` existe
- [ ] Contient `"openrouter_api_key": "sk-or-v1-..."`
- [ ] Variable d'environnement `OPENROUTER_API_KEY` définie
- [ ] Application redémarrée
- [ ] Provider LLM = "openrouter" dans l'interface
- [ ] Test avec fichier PDF réussi

## 🆘 CONTACT SUPPORT

Si le problème persiste après avoir suivi ce guide :

1. **Exécuter le diagnostic complet** :
   ```cmd
   python diagnostic_cles_windows.py > diagnostic_windows.txt
   ```

2. **Joindre les fichiers** :
   - `diagnostic_windows.txt`
   - `logs/matelas_app.log`
   - `logs/matelas_errors.log`

3. **Décrire précisément** :
   - Version de Windows
   - Version de Python
   - Étapes suivies
   - Message d'erreur exact

## 💡 CONSEILS PRÉVENTIFS

1. **Sauvegarder la configuration** :
   ```cmd
   copy C:\Users\%USERNAME%\.matelas_config.json C:\Users\%USERNAME%\.matelas_config.json.backup
   ```

2. **Vérifier régulièrement** :
   ```cmd
   python -c "import config; print('Clé API:', config.get_openrouter_api_key()[:10] + '...')"
   ```

3. **Utiliser des variables d'environnement** plutôt que des fichiers pour plus de sécurité 