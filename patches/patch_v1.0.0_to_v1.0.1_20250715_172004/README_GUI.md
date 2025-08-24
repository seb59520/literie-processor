# Interface Graphique - Application Traitement Devis Matelas

## Installation

### 1. Installer PyQt6
```bash
pip install PyQt6
```

Ou installer toutes les dépendances :
```bash
pip install -r requirements_gui.txt
```

### 2. Vérifier les dépendances backend
Assurez-vous que toutes les dépendances du backend sont installées :
```bash
pip install -r backend/requirements.txt
```

## Lancement

### Méthode 1 : Script de lancement
```bash
python run_gui.py
```

### Méthode 2 : Direct
```bash
python app_gui.py
```

## Utilisation

### Interface principale
L'application se compose de deux panneaux :

**Panneau gauche (Configuration) :**
- **Fichiers PDF** : Sélectionnez un ou plusieurs fichiers PDF à traiter
- **Enrichissement LLM** : Activez/désactivez l'utilisation du LLM
- **Provider** : Choisissez entre Ollama et OpenRouter
- **Clé API** : Entrez votre clé API OpenRouter si nécessaire
- **Paramètres de production** : Semaine et année de production
- **Commande client** : Nom du client

**Panneau droit (Résultats) :**
- **Onglet Résumé** : Vue d'ensemble du traitement
- **Onglet Configurations** : Tableau des configurations matelas détectées
- **Onglet Pré-import** : Données structurées pour l'import Excel
- **Onglet JSON** : Données brutes au format JSON

### Étapes de traitement
1. Sélectionnez vos fichiers PDF
2. Configurez les paramètres (LLM, production, client)
3. Cliquez sur "Traiter les fichiers"
4. Consultez les résultats dans les différents onglets

## Fonctionnalités

### ✅ Fonctionnalités implémentées
- Interface graphique moderne avec PyQt6
- Sélection multiple de fichiers PDF
- Configuration complète des paramètres
- Affichage des résultats en temps réel
- Gestion des erreurs
- Interface responsive avec onglets

### 🔄 Intégration avec le backend
- Utilise toute la logique backend existante
- Traitement LLM (Ollama/OpenRouter)
- Détection des noyaux matelas
- Calcul des dimensions et configurations
- Génération du pré-import Excel

### 📊 Affichage des résultats
- **Résumé** : Statistiques du traitement
- **Configurations** : Tableau des matelas détectés
- **Pré-import** : Données structurées pour Excel
- **JSON** : Données brutes pour debug

## Avantages par rapport à l'interface web

### 🎯 Interface native
- Pas besoin de navigateur web
- Interface plus réactive
- Intégration native au système

### 🚀 Performance
- Pas de surcharge HTTP
- Traitement direct des fichiers
- Interface plus fluide

### 🔧 Facilité d'utilisation
- Interface intuitive
- Gestion des erreurs améliorée
- Affichage structuré des résultats

## Dépannage

### Erreur "Module not found"
```bash
pip install PyQt6
```

### Erreur backend
Vérifiez que tous les modules backend sont installés :
```bash
pip install -r backend/requirements.txt
```

### Problème de permissions
Sur macOS/Linux, rendez le script exécutable :
```bash
chmod +x run_gui.py
```

## Développement

### Structure des fichiers
```
├── app_gui.py              # Interface graphique principale
├── backend_interface.py    # Interface avec le backend
├── run_gui.py             # Script de lancement
├── requirements_gui.txt   # Dépendances GUI
└── README_GUI.md         # Ce fichier
```

### Personnalisation
L'interface peut être facilement personnalisée en modifiant :
- Les styles CSS dans `app_gui.py`
- Les layouts et widgets
- L'affichage des résultats

## Support

Pour toute question ou problème, consultez :
1. Les logs de l'application
2. La documentation du backend
3. Les erreurs affichées dans l'interface 