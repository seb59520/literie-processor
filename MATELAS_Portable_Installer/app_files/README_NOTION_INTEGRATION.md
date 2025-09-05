# 🔗 Intégration Notion avec Cursor

## 📋 Vue d'ensemble

Cette intégration permet de connecter Cursor et vos projets à Notion pour une gestion complète de projet, incluant :

- **Suivi des projets** : Détection automatique des projets dans vos workspaces Cursor
- **Journal des modifications** : Suivi des changements dans vos fichiers
- **Notices d'utilisation** : Création et gestion de documentation
- **Liens externes** : Gestion des ressources et références
- **Synchronisation automatique** : Mise à jour en temps réel avec Notion

## 🚀 Installation rapide

### 1. Démarrage automatique
```bash
python lancer_notion_integration.py
```

### 2. Configuration manuelle
```bash
python setup_notion_integration.py
```

### 3. Lancement de l'interface
```bash
python notion_manager_gui.py
```

## ⚙️ Configuration

### Prérequis
- Compte Notion
- Python 3.7+
- Accès à l'API Notion

### Étapes de configuration

#### 1. Créer une intégration Notion
1. Allez sur [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Cliquez sur "New integration"
3. Donnez un nom (ex: "Cursor Integration")
4. Sélectionnez votre workspace
5. Cliquez sur "Submit"
6. Copiez la clé API (Internal Integration Token)

#### 2. Créer une base de données Notion
1. Créez une nouvelle page dans Notion
2. Tapez `/database` et sélectionnez "Table"
3. Ajoutez les propriétés suivantes :

| Propriété | Type | Description |
|-----------|------|-------------|
| Nom | Title | Nom du projet |
| Chemin | Text | Chemin du projet sur le disque |
| Description | Text | Description du projet |
| Langage | Select | Langage principal (Python, JavaScript, etc.) |
| Framework | Text | Framework utilisé |
| Dernière modification | Date | Date de dernière modification |
| Statut Git | Select | Git initialisé / Non versionné |
| Workspace Cursor | Text | Chemin du workspace Cursor |
| Statut | Select | En cours / Terminé / En pause / Abandonné |
| Date de création | Date | Date de création de la page |

#### 3. Obtenir les IDs
- **Database ID** : Dans l'URL de votre base de données, copiez la partie après le workspace (32 caractères)
- **Workspace ID** : Dans l'URL de votre workspace Notion, copiez la partie après `notion.so/`

## 📁 Structure des fichiers

```
notion_integration.py          # Module principal d'intégration
notion_manager_gui.py          # Interface graphique
setup_notion_integration.py    # Script de configuration
lancer_notion_integration.py   # Lanceur automatique
requirements_notion.txt        # Dépendances Python
notion_config.json            # Configuration (créé automatiquement)
GUIDE_DEMARRAGE_NOTION.md     # Guide de démarrage
README_NOTION_INTEGRATION.md  # Cette documentation
```

## 🔧 Utilisation

### Interface graphique

L'interface est organisée en 6 onglets :

#### ⚙️ Configuration
- Gestion des clés API Notion
- Test de connexion
- Sauvegarde de la configuration

#### 📁 Projets
- Visualisation des projets détectés
- Scan du workspace
- Synchronisation avec Notion

#### 📝 Modifications
- Ajout manuel de modifications
- Suivi des changements
- Historique des modifications

#### 📚 Notices d'utilisation
- Création de documentation
- Gestion des catégories et tags
- Versioning des notices

#### 🔗 Liens externes
- Ajout de ressources externes
- Catégorisation des liens
- Association avec les projets

#### 🔄 Synchronisation
- Sélection du workspace
- Scan automatique
- Synchronisation complète
- Logs de synchronisation

### Commandes en ligne

#### Scan manuel du workspace
```bash
python notion_integration.py
```

#### Test de connexion
```bash
python -c "
from notion_integration import NotionIntegration, NotionConfig
import json

with open('notion_config.json', 'r') as f:
    config_data = json.load(f)
    
config = NotionConfig(**config_data)
notion = NotionIntegration(config)
results = notion.search_projects('test')
print('Connexion réussie!' if results is not None else 'Erreur de connexion')
"
```

## 🔄 Synchronisation automatique

### Détection des projets
Le système détecte automatiquement les projets en recherchant :
- `package.json` (Node.js)
- `requirements.txt` (Python)
- `pom.xml` (Java Maven)
- `build.gradle` (Java Gradle)
- `Cargo.toml` (Rust)
- `go.mod` (Go)
- `composer.json` (PHP)
- `.git` (Repository Git)

### Langages supportés
- **Python** : Détection via `.py`, `requirements.txt`, `setup.py`
- **JavaScript/Node.js** : Détection via `.js`, `package.json`
- **Java** : Détection via `.java`, `pom.xml`, `build.gradle`
- **C++** : Détection via `.cpp`, `.h`, `CMakeLists.txt`
- **Go** : Détection via `.go`, `go.mod`
- **Rust** : Détection via `.rs`, `Cargo.toml`
- **PHP** : Détection via `.php`, `composer.json`

## 📊 Fonctionnalités avancées

### Suivi des modifications
- Enregistrement automatique des changements
- Association avec les commits Git
- Historique détaillé des modifications

### Gestion des notices
- Création de documentation structurée
- Système de tags et catégories
- Versioning automatique

### Liens externes
- Organisation par catégorie
- Association avec les projets
- Recherche et filtrage

## 🛠️ Développement

### Architecture
```
NotionIntegration          # Interface avec l'API Notion
├── create_project_page   # Création de pages projet
├── update_project_status # Mise à jour des statuts
├── log_change           # Enregistrement des modifications
├── create_user_guide    # Création de notices
└── add_external_link    # Ajout de liens

CursorNotionSync          # Synchronisation Cursor-Notion
├── scan_cursor_workspace # Scan des workspaces
├── _detect_language     # Détection du langage
├── _detect_framework    # Détection du framework
└── sync_workspace_to_notion # Synchronisation complète
```

### Extension
Pour ajouter de nouvelles fonctionnalités :

1. **Nouveaux types de données** : Créez de nouvelles dataclasses dans `notion_integration.py`
2. **Nouveaux onglets** : Ajoutez des méthodes dans `NotionManagerGUI`
3. **Nouveaux langages** : Étendez `_detect_language` dans `CursorNotionSync`

## 🔒 Sécurité

### Gestion des clés API
- Les clés API sont stockées localement dans `notion_config.json`
- Le fichier de configuration n'est pas versionné par défaut
- Utilisez des variables d'environnement pour la production

### Permissions Notion
- L'intégration nécessite l'accès aux bases de données
- Vérifiez les permissions dans les paramètres de votre intégration
- Limitez l'accès aux workspaces nécessaires

## 🐛 Dépannage

### Problèmes courants

#### Erreur de connexion
```
❌ Erreur de connexion: 401
```
- Vérifiez que votre clé API est correcte
- Assurez-vous que l'intégration a accès au workspace

#### Base de données introuvable
```
❌ Erreur de connexion: 404
```
- Vérifiez l'ID de la base de données
- Assurez-vous que l'intégration a accès à la base

#### Permissions insuffisantes
```
❌ Erreur de connexion: 403
```
- Vérifiez les permissions de votre intégration
- Assurez-vous que la base de données est partagée avec l'intégration

### Logs et débogage
- Les logs sont affichés dans l'onglet Synchronisation
- Utilisez le bouton "Nettoyer les logs" pour effacer l'historique
- Vérifiez la console Python pour les erreurs détaillées

## 📚 Ressources

### Documentation officielle
- [API Notion](https://developers.notion.com/)
- [Intégrations Notion](https://www.notion.so/my-integrations)

### Support
- Vérifiez les logs dans l'interface
- Consultez le fichier `GUIDE_DEMARRAGE_NOTION.md`
- Vérifiez la configuration dans `notion_config.json`

## 🤝 Contribution

Pour contribuer à ce projet :

1. Fork le repository
2. Créez une branche pour votre fonctionnalité
3. Testez vos modifications
4. Soumettez une pull request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

Si vous rencontrez des problèmes :

1. Vérifiez la configuration
2. Consultez les logs
3. Testez la connexion
4. Vérifiez les permissions Notion

---

**Note** : Cette intégration est conçue pour fonctionner avec l'API officielle de Notion. Assurez-vous de respecter les limites d'utilisation de l'API.


