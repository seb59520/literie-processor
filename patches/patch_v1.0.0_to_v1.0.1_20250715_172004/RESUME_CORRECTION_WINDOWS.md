# 🔧 RÉSUMÉ CORRECTION WINDOWS - CLÉ API OPENROUTER

## 🎯 PROBLÈME

**Message d'erreur** : "Clé API OpenRouter requise" sous Windows alors que la clé est configurée.

## 🚀 SOLUTION RAPIDE (5 minutes)

### Étape 1 : Diagnostic
```cmd
python diagnostic_cles_windows.py
```

### Étape 2 : Correction automatique
```cmd
python corriger_cles_windows.py
```

### Étape 3 : Test
```cmd
python test_cles_windows.py
```

### Étape 4 : Redémarrer l'application
```cmd
python app_gui.py
```

## 📁 FICHIERS CRÉÉS

- `diagnostic_cles_windows.py` - Diagnostic complet
- `corriger_cles_windows.py` - Correction automatique
- `test_cles_windows.py` - Test rapide
- `GUIDE_CORRECTION_WINDOWS.md` - Guide détaillé
- `configurer_openrouter_windows.bat` - Script batch
- `configurer_openrouter_windows.ps1` - Script PowerShell

## 🔍 CAUSES POSSIBLES

1. **Fichier de configuration manquant** : `C:\Users\[nom]\.matelas_config.json`
2. **Encodage incorrect** : Fichier non sauvegardé en UTF-8
3. **Permissions** : Droits d'accès insuffisants
4. **Variable d'environnement** : `OPENROUTER_API_KEY` non définie
5. **Chemin Windows** : Différences de gestion des chemins

## 🛠️ SOLUTIONS ALTERNATIVES

### Solution A : Configuration manuelle
1. Créer `C:\Users\[nom]\.matelas_config.json`
2. Ajouter : `{"openrouter_api_key": "sk-or-v1-...", "provider": "openrouter"}`
3. Sauvegarder en UTF-8

### Solution B : Variable d'environnement
```cmd
setx OPENROUTER_API_KEY "sk-or-v1-votre-clé-ici"
```

### Solution C : PowerShell
```powershell
[Environment]::SetEnvironmentVariable("OPENROUTER_API_KEY", "sk-or-v1-votre-clé-ici", "User")
```

## ✅ VÉRIFICATION

### Test rapide
```cmd
python -c "import config; print('Clé:', config.get_openrouter_api_key()[:10] + '...')"
```

### Test complet
```cmd
python test_cles_windows.py
```

### Dans l'application
- Onglet "Configuration" → Provider = "openrouter"
- Aucun message d'erreur
- Test avec fichier PDF réussi

## 🚨 DÉPANNAGE

### "Fichier non trouvé"
```cmd
dir C:\Users\%USERNAME%\.matelas_config.json
```

### "Permission refusée"
- Exécuter en tant qu'administrateur
- Vérifier les droits d'accès

### "Clé invalide"
- Vérifier sur https://openrouter.ai/keys
- Copier la clé complète (sk-or-v1-...)

### "Encodage incorrect"
- Bloc-notes → Fichier → Enregistrer sous → UTF-8

## 📋 CHECKLIST FINALE

- [ ] Fichier `.matelas_config.json` existe et contient la clé
- [ ] Variable d'environnement `OPENROUTER_API_KEY` définie
- [ ] Application redémarrée
- [ ] Provider LLM = "openrouter" dans l'interface
- [ ] Test avec fichier PDF réussi
- [ ] Aucun message d'erreur de clé API

## 🆘 SUPPORT

Si le problème persiste :

1. **Générer un rapport** :
   ```cmd
   python diagnostic_cles_windows.py > rapport_windows.txt
   ```

2. **Joindre les fichiers** :
   - `rapport_windows.txt`
   - `logs/matelas_app.log`
   - `logs/matelas_errors.log`

3. **Informations requises** :
   - Version Windows
   - Version Python
   - Étapes suivies
   - Message d'erreur exact

## 💡 CONSEILS

1. **Sauvegarder** la configuration avant modification
2. **Utiliser des variables d'environnement** pour plus de sécurité
3. **Vérifier régulièrement** que la clé API est active
4. **Redémarrer l'application** après toute modification

## 🎉 RÉSULTAT ATTENDU

Après correction, l'application devrait :
- ✅ Démarrer sans erreur de clé API
- ✅ Afficher "openrouter" comme provider
- ✅ Traiter les fichiers PDF normalement
- ✅ Générer les fichiers Excel attendus 