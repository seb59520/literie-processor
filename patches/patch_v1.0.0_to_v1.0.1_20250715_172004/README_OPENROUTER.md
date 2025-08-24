# Guide d'utilisation OpenRouter

## Configuration

### 1. Obtenir une clé API OpenRouter

1. Allez sur [OpenRouter.ai](https://openrouter.ai)
2. Créez un compte ou connectez-vous
3. Allez dans la section "API Keys"
4. Créez une nouvelle clé API
5. Copiez la clé (elle commence par `sk-or-`)

### 2. Utilisation dans l'application

#### Option A : Variable d'environnement (recommandé)
```bash
export OPENROUTER_API_KEY="sk-or-votre-cle-api-ici"
```

#### Option B : Interface utilisateur
1. Lancez l'application
2. Cochez "🤖 Enrichir avec LLM"
3. Sélectionnez "OpenRouter (cloud)"
4. Entrez votre clé API dans le champ qui apparaît
5. Uploadez votre PDF

## Test de l'intégration

Pour vérifier que tout fonctionne :

```bash
# Définir la clé API
export OPENROUTER_API_KEY="sk-or-votre-cle-api-ici"

# Lancer le test
python test_openrouter.py
```

## Modèles disponibles

L'application utilise actuellement :
- **openai/gpt-4-turbo** : Modèle GPT-4 Turbo via OpenRouter

## Avantages d'OpenRouter vs Ollama

### OpenRouter (Cloud)
- ✅ Modèles de pointe (GPT-4, Claude, etc.)
- ✅ Pas d'installation locale requise
- ✅ Performance optimale
- ❌ Nécessite une connexion internet
- ❌ Coût par requête
- ❌ Dépendance à un service tiers

### Ollama (Local)
- ✅ Gratuit (après installation)
- ✅ Fonctionne hors ligne
- ✅ Contrôle total des données
- ❌ Nécessite une installation locale
- ❌ Performance variable selon le matériel
- ❌ Modèles moins avancés

## Dépannage

### Erreur "Clé API OpenRouter manquante"
- Vérifiez que la clé API est correctement saisie
- Assurez-vous qu'elle commence par `sk-or-`

### Erreur "Impossible de se connecter à OpenRouter"
- Vérifiez votre connexion internet
- Vérifiez que l'URL `https://openrouter.ai` est accessible

### Erreur "Timeout lors de l'appel à OpenRouter"
- Le modèle prend trop de temps à répondre
- Essayez avec un texte plus court
- Vérifiez votre connexion internet

### Erreur "Erreur parsing JSON"
- Le modèle a retourné une réponse mal formatée
- Vérifiez le "Résultat brut de l'analyse LLM" dans l'interface
- Le problème peut être temporaire, réessayez

## Logs et débogage

Les logs de l'application incluent :
- `Préparation appel OpenRouter avec résultat`
- `Payload OpenRouter`
- `Envoi requête à OpenRouter...`
- `Réponse OpenRouter reçue - status`
- `Données OpenRouter`
- `Nettoyage de la réponse OpenRouter...`

Pour voir les logs en temps réel :
```bash
docker-compose logs -f backend
```

## Coûts

OpenRouter facture par token utilisé. Pour un devis typique :
- **Entrée** : ~500-1000 tokens
- **Sortie** : ~200-500 tokens
- **Coût estimé** : ~0.01-0.05€ par devis

Vérifiez les tarifs actuels sur [OpenRouter.ai/pricing](https://openrouter.ai/pricing)

## Sécurité

- La clé API est transmise via HTTPS
- Elle n'est pas stockée en base de données
- Elle n'est utilisée que pour l'appel à OpenRouter
- Les données du devis sont envoyées à OpenRouter pour analyse

## Support

En cas de problème :
1. Vérifiez les logs de l'application
2. Testez avec le script `test_openrouter.py`
3. Vérifiez votre compte OpenRouter pour les quotas/limites
4. Contactez le support OpenRouter si nécessaire 