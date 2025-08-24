# 🧪 Application de Test LLM - MatelasApp

## 📋 Description

Application graphique pour tester les prompts LLM, providers et modèles utilisés dans MatelasApp. Permet de valider et optimiser les prompts avant leur déploiement en production.

## 🚀 Lancement

### Windows
```bash
lancer_test_llm.bat
```

### Linux/Mac
```bash
chmod +x lancer_test_llm.sh
./lancer_test_llm.sh
```

### Python direct
```bash
python lancer_test_llm.py
```

## 🎯 Fonctionnalités

### 🔧 Configuration des Providers
- **Ollama** : Modèles locaux avec gestion avancée
  - **Détection automatique** : Liste automatique des modèles installés
  - **Ajout de modèles** : Bouton ➕ pour ajouter de nouveaux modèles
  - **Rafraîchissement** : Bouton 🔄 pour actualiser la liste
  - **Téléchargement** : Téléchargement automatique des modèles
- **OpenRouter** : Accès à GPT-4, Claude, etc.
- **OpenAI** : API OpenAI directe
- **Anthropic** : API Claude directe

### 📝 Gestion des Prompts
- **Restaurer le prompt actuel** : Récupère automatiquement le prompt depuis `main.py`
- **Sauvegarder/Loader** : Gestion des prompts personnalisés
- **Édition en temps réel** : Modification du prompt pour les tests

### 📄 Gestion des Textes de Test
- **Chargement PDF** : Extraction automatique du texte
- **Chargement fichiers texte** : Support des formats .txt
- **Édition directe** : Saisie manuelle du texte de test

### 🧪 Tests LLM
- **Paramètres configurables** : Température, max_tokens
- **Explications de température** : Guide interactif pour comprendre l'impact
- **Tests asynchrones** : Interface non-bloquante
- **Résultats détaillés** : Affichage brut + JSON parsé
- **Gestion d'erreurs** : Messages d'erreur clairs

### 🌡️ Paramètres LLM

#### Température
La température contrôle la créativité et la prévisibilité des réponses :

- **0.0** : Déterministe - Réponses cohérentes et prévisibles
- **0.1-0.3** : Faible créativité - Réponses structurées et précises
- **0.4-0.7** : Créativité modérée - Équilibré entre précision et créativité
- **0.8-1.0** : Créativité élevée - Réponses variées et originales
- **1.1-2.0** : Très créatif - Réponses très variées et imprévisibles

#### Max Tokens
Nombre maximum de tokens dans la réponse générée (100-4000).

### 📊 Historique et Analyse
- **Historique des tests** : Sauvegarde de tous les tests
- **Export JSON** : Sauvegarde des résultats
- **Comparaison** : Visualisation des différences entre tests

## 🖥️ Interface

### Panneau Gauche - Configuration
1. **Configuration Provider**
   - Sélection du provider (Ollama, OpenRouter, etc.)
   - Saisie de la clé API
   - Choix du modèle
   - Paramètres (température, max_tokens)

2. **Gestion du Prompt**
   - Bouton "Restaurer Prompt Actuel"
   - Sauvegarde/Chargement de prompts
   - Éditeur de prompt avec coloration syntaxique

3. **Texte de Test**
   - Chargement PDF/TXT
   - Éditeur de texte
   - Bouton "Lancer Test LLM"

### Panneau Droit - Résultats
1. **Onglet Résultats**
   - Informations du test (provider, modèle, paramètres)
   - Résultat brut du LLM
   - JSON parsé et formaté

2. **Onglet Historique**
   - Tableau des tests effectués
   - Actions (voir, exporter)
   - Gestion de l'historique

3. **Onglet Configuration**
   - État de la configuration actuelle
   - Test de configuration
   - Clés API configurées

## 🔑 Configuration des Clés API

L'application utilise automatiquement les clés API configurées dans MatelasApp :

### Synchronisation Automatique
- **Chargement automatique** : Les clés API sont automatiquement chargées au démarrage
- **Synchronisation par provider** : Les clés se synchronisent automatiquement lors du changement de provider
- **Bouton de synchronisation** : Cliquez sur le bouton 🔄 à côté du champ "Clé API" pour forcer la synchronisation
- **Messages informatifs** : La barre de statut indique l'état de la synchronisation

### Configuration des Providers

#### Ollama
Aucune clé requise, mais Ollama doit être installé et en cours d'exécution.

**Gestion des modèles :**
1. **Détection automatique** : Les modèles installés sont automatiquement listés
2. **Ajout de modèles** : Cliquez sur ➕ pour ajouter un nouveau modèle
3. **Téléchargement** : L'application peut télécharger automatiquement les modèles
4. **Rafraîchissement** : Cliquez sur 🔄 pour actualiser la liste des modèles

**Modèles populaires :**
- `mistral:latest` - Modèle rapide et efficace
- `llama2:latest` - Modèle équilibré
- `codellama:latest` - Spécialisé en code
- `llama2:7b` - Version légère
- `llama2:13b` - Version plus puissante

#### OpenRouter
1. Créer un compte sur [OpenRouter](https://openrouter.ai)
2. Générer une clé API
3. Configurer dans MatelasApp (Menu Réglages → Gestion des clés API)

#### OpenAI
1. Créer un compte sur [OpenAI](https://openai.com)
2. Générer une clé API
3. Configurer dans MatelasApp (Menu Réglages → Gestion des clés API)

#### Anthropic
1. Créer un compte sur [Anthropic](https://anthropic.com)
2. Générer une clé API
3. Configurer dans MatelasApp (Menu Réglages → Gestion des clés API)

## 📝 Utilisation

### 1. Test Rapide
1. Lancer l'application
2. Le prompt actuel est automatiquement chargé
3. Entrer un texte de test simple
4. Cliquer sur "Lancer Test LLM"

### 2. Test avec PDF
1. Cliquer sur "Charger PDF"
2. Sélectionner un devis PDF
3. Le texte est automatiquement extrait
4. Lancer le test

### 3. Optimisation de Prompt
1. Modifier le prompt dans l'éditeur
2. Tester avec différents textes
3. Comparer les résultats
4. Sauvegarder le meilleur prompt

### 4. Test de Configuration
1. Aller dans l'onglet "Configuration"
2. Cliquer sur "Tester Configuration"
3. Vérifier que tout fonctionne

## 🐛 Dépannage

### Erreur "PyQt non trouvé"
```bash
pip install PyQt6
# ou
pip install PyQt5
```

### Erreur "Modules backend"
- Vérifier d'être dans le répertoire racine du projet
- Vérifier que `config.py` et `backend/` existent

### Erreur "Clé API manquante"
- Configurer la clé API dans l'application
- Vérifier que la clé est valide

### Erreur "Provider non configuré"
- Vérifier que le provider est correctement configuré
- Tester la configuration dans l'onglet dédié

## 📁 Fichiers

- `test_llm_prompt.py` : Application principale
- `lancer_test_llm.py` : Script de lancement Python
- `lancer_test_llm.bat` : Lanceur Windows
- `lancer_test_llm.sh` : Lanceur Linux/Mac
- `README_TEST_LLM.md` : Cette documentation

## 🔄 Intégration avec MatelasApp

L'application utilise les mêmes modules que MatelasApp :
- `config.py` : Configuration des providers
- `backend/llm_provider.py` : Gestion des appels LLM
- `backend/main.py` : Récupération du prompt actuel

Les modifications de prompt testées peuvent être directement appliquées à `main.py`.

## 🎉 Avantages

1. **Tests rapides** : Validation immédiate des prompts
2. **Interface intuitive** : Pas besoin de ligne de commande
3. **Historique complet** : Traçabilité des tests
4. **Multi-providers** : Test de tous les providers configurés
5. **Intégration native** : Utilise la même configuration que MatelasApp 