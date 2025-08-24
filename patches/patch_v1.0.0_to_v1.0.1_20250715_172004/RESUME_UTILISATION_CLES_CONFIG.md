# 🔑 COMMENT UTILISER LES CLÉS API DE MATELAS_CONFIG.JSON

## 🎯 RÉPONSE À VOTRE QUESTION

**Pour faire en sorte que l'application utilise la clé API du fichier `matelas_config.json`, vous n'avez RIEN à faire !** 

L'application utilise **automatiquement** les clés API stockées dans ce fichier. Voici comment cela fonctionne :

## 📍 LOCALISATION DU FICHIER

- **Fichier** : `~/.matelas_config.json` (dossier utilisateur)
- **Sur macOS** : `/Users/sebastien/.matelas_config.json`
- **Sur Windows** : `C:\Users\[votre_nom]\.matelas_config.json`

## 🔄 UTILISATION AUTOMATIQUE

### 1. **Chargement automatique**
L'application charge automatiquement les clés API :
- ✅ **Au démarrage** de l'application
- ✅ **Quand vous changez** de provider LLM
- ✅ **Quand vous traitez** des fichiers

### 2. **Sauvegarde automatique**
L'application sauvegarde automatiquement :
- ✅ Les nouvelles clés API que vous saisissez
- ✅ Le provider LLM sélectionné
- ✅ Les modèles personnalisés

### 3. **Synchronisation automatique**
- ✅ Interface graphique : Les clés sont pré-remplies
- ✅ Traitement backend : Les clés sont transmises automatiquement
- ✅ Gestionnaire de clés : Affiche et permet de modifier les clés

## 🚀 COMMENT L'ACTIVER

### Option 1 : Interface graphique (recommandée)
1. **Lancer l'application** : `python3 app_gui.py`
2. **Cocher** "🤖 Enrichir avec LLM"
3. **Sélectionner** le provider dans le menu déroulant
4. **La clé API sera automatiquement chargée** si elle existe

### Option 2 : Gestionnaire de clés
1. **Menu Aide** → **🔐 Gestionnaire de Clés API**
2. **Voir** toutes les clés configurées
3. **Ajouter/modifier/supprimer** des clés
4. **Tester** les connexions

### Option 3 : Configuration des providers
1. **Menu Aide** → **⚙️ Configuration des Providers LLM**
2. **Configurer** les clés API pour chaque provider
3. **Sélectionner** le provider actuel
4. **Définir** les modèles personnalisés

## 📋 STRUCTURE DU FICHIER

```json
{
  "openrouter_api_key": "sk-or-votre-cle-api-ici",
  "llm_api_key_openai": "sk-votre-cle-openai-ici",
  "llm_api_key_anthropic": "sk-ant-votre-cle-anthropic-ici",
  "current_llm_provider": "openrouter",
  "llm_model_openrouter": "gpt-4o",
  "llm_model_openai": "gpt-4o",
  "llm_model_anthropic": "claude-3-5-sonnet-20241022",
  "last_semaine": 1,
  "last_annee": 2025,
  "last_commande_client": "",
  "excel_output_directory": "/chemin/vers/output"
}
```

## 🔍 VÉRIFICATION DE VOTRE CONFIGURATION

D'après le diagnostic, votre configuration actuelle est :

- ✅ **Fichier trouvé** : `/Users/sebastien/.matelas_config.json`
- ✅ **Clé OpenRouter** : Présente et valide
- ✅ **Provider actuel** : `openrouter`
- ✅ **Module de configuration** : Fonctionnel

## 🎯 RÉSULTAT

**Votre application utilise déjà automatiquement la clé API OpenRouter !**

Quand vous :
1. Lancez l'application
2. Cochez "🤖 Enrichir avec LLM"
3. Sélectionnez "OpenRouter" dans le menu déroulant

L'application :
- ✅ Charge automatiquement votre clé API depuis `~/.matelas_config.json`
- ✅ Pré-remplit le champ de clé API dans l'interface
- ✅ Transmet la clé au backend lors du traitement
- ✅ Sauvegarde automatiquement toute modification

## 🔧 DÉPANNAGE

### Si les clés ne sont pas détectées :
1. **Vérifiez le format** du fichier JSON
2. **Vérifiez les permissions** du fichier
3. **Redémarrez** l'application après modification

### Si l'application ne démarre pas :
1. **Vérifiez les imports** PyQt6
2. **Vérifiez les dépendances** Python
3. **Consultez les logs** dans `logs/matelas_errors.log`

### Si les clés ne fonctionnent pas :
1. **Testez les connexions** via le gestionnaire de clés
2. **Vérifiez la validité** des clés API
3. **Consultez les logs** pour les erreurs détaillées

## 💡 CONSEILS

### Sécurité
- 🔒 Le fichier `~/.matelas_config.json` n'est **pas chiffré**
- 🔐 Pour plus de sécurité, utilisez le **stockage sécurisé**
- 🚫 Ne partagez **jamais** votre fichier de configuration

### Synchronisation
- 🔄 Les clés sont **automatiquement synchronisées**
- 💾 Les modifications sont **sauvegardées immédiatement**
- 🔄 **Redémarrez** l'application après modification du fichier

### Test
- 🧪 Utilisez le **gestionnaire de clés** pour tester les connexions
- ✅ Vérifiez que les clés sont **valides** avant de traiter des fichiers
- 📋 Consultez les **logs** pour diagnostiquer les problèmes

## 🎉 CONCLUSION

**Votre application utilise déjà automatiquement la clé API du fichier `matelas_config.json` !**

Aucune action manuelle n'est requise. L'application :
- ✅ Détecte automatiquement votre clé OpenRouter
- ✅ L'utilise automatiquement lors du traitement
- ✅ Sauvegarde automatiquement les modifications

**Pour commencer à utiliser votre clé API :**
1. Lancez l'application : `python3 app_gui.py`
2. Cochez "🤖 Enrichir avec LLM"
3. Sélectionnez "OpenRouter" dans le menu déroulant
4. Traitez vos fichiers PDF - la clé sera automatiquement utilisée !

---

*Dernière mise à jour : 15 juillet 2025* 