# 📚 Module de Maintenance - Documentation

## Vue d'ensemble

Le module de maintenance de l'application Matelas permet d'accéder facilement à toute la documentation technique et de maintenance du projet. Il scanne automatiquement tous les fichiers Markdown (`.md`) du projet et les présente dans une interface graphique conviviale.

## Fonctionnalités

### 🔍 Détection automatique
- **Scan récursif** : Parcourt automatiquement tous les répertoires du projet
- **Filtrage intelligent** : Ignore les répertoires système (`.git`, `__pycache__`, etc.)
- **Actualisation en temps réel** : Bouton "Actualiser" pour recharger la liste

### 📖 Affichage enrichi
- **Extraction de titre** : Lit automatiquement le premier titre (`#` ou `##`) du fichier
- **Métadonnées** : Affiche le chemin, la date de modification et la taille
- **Tri chronologique** : Les fichiers les plus récents apparaissent en premier

### 🎨 Interface utilisateur
- **Vue en deux panneaux** : Liste des fichiers à gauche, aperçu à droite
- **Conversion Markdown** : Affiche le contenu formaté en HTML
- **Navigation intuitive** : Clic pour sélectionner, boutons d'action

### 🛠️ Actions disponibles
- **Ouvrir le fichier** : Lance l'application par défaut pour éditer le fichier
- **Copier le chemin** : Copie le chemin complet dans le presse-papiers
- **Aperçu intégré** : Visualise le contenu sans quitter l'application

## Comment utiliser

### Accès au module
1. Ouvrir l'application Matelas
2. Aller dans le menu **Réglages**
3. Cliquer sur **📚 Maintenance - Documentation**

### Navigation
1. **Sélectionner un fichier** : Cliquer sur un fichier dans la liste de gauche
2. **Voir l'aperçu** : Le contenu s'affiche automatiquement à droite
3. **Ouvrir le fichier** : Utiliser le bouton "📂 Ouvrir le fichier"
4. **Actualiser la liste** : Cliquer sur "🔄 Actualiser"

### Ajouter de nouveaux fichiers
1. Créer un nouveau fichier `.md` dans le projet
2. Ajouter un titre principal avec `# Titre du fichier`
3. Cliquer sur "🔄 Actualiser" dans le dialogue de maintenance
4. Le nouveau fichier apparaîtra automatiquement dans la liste

## Structure technique

### Classes principales
- **`MaintenanceDialog`** : Dialogue principal de maintenance
- **`MatelasApp.show_maintenance_dialog()`** : Méthode d'ouverture

### Méthodes clés
- **`scan_md_files()`** : Scan et détection des fichiers Markdown
- **`extract_title_from_md()`** : Extraction du titre depuis le contenu
- **`markdown_to_html()`** : Conversion Markdown vers HTML
- **`display_file_content()`** : Affichage du contenu formaté

### Intégration
- **Menu** : Ajouté dans le menu "Réglages"
- **Raccourci** : Accessible via l'interface graphique
- **Logs** : Intégré au système de logging de l'application

## Fichiers supportés

### Types de fichiers
- ✅ Fichiers `.md` (Markdown standard)
- ✅ Fichiers `.markdown` (extension alternative)

### Contenu supporté
- ✅ Titres (`#`, `##`, `###`)
- ✅ Code inline (`` `code` ``)
- ✅ Blocs de code (``` ```)
- ✅ Liens (`[texte](url)`)
- ✅ Gras (`**texte**`)
- ✅ Italique (`*texte*`)
- ✅ Listes (`-` ou `*`)

### Répertoires ignorés
- `.git/`
- `__pycache__/`
- `node_modules/`
- `venv/`
- `env/`
- Tous les répertoires commençant par `.`

## Exemples d'utilisation

### Fichier de documentation typique
```markdown
# Guide d'installation

## Prérequis
- Python 3.8+
- PyQt6

## Installation
1. Cloner le repository
2. Installer les dépendances
3. Lancer l'application

## Utilisation
Voir la documentation complète...
```

### Structure recommandée
```
projet/
├── README.md
├── GUIDE_INSTALLATION.md
├── MAINTENANCE.md
├── backend/
│   └── README.md
└── docs/
    ├── API.md
    └── DEPLOIEMENT.md
```

## Avantages

### Pour les développeurs
- **Accès centralisé** : Toute la documentation en un seul endroit
- **Navigation rapide** : Pas besoin de chercher dans l'arborescence
- **Aperçu instantané** : Voir le contenu sans ouvrir d'éditeur

### Pour les utilisateurs
- **Interface intuitive** : Pas besoin de connaissances techniques
- **Actualisation automatique** : Nouveaux fichiers détectés automatiquement
- **Intégration native** : Fonctionne avec l'application existante

## Maintenance

### Ajout de nouveaux fichiers
- Créer le fichier `.md` dans le projet
- Ajouter un titre principal
- Actualiser la liste dans l'interface

### Mise à jour du système
- Le système se met à jour automatiquement
- Aucune configuration supplémentaire requise
- Compatible avec tous les fichiers Markdown standard

## Support

### Problèmes courants
- **Fichier non détecté** : Vérifier l'extension `.md`
- **Titre non extrait** : Ajouter un titre `#` au début du fichier
- **Erreur d'affichage** : Vérifier l'encodage UTF-8

### Logs
- Les erreurs sont enregistrées dans `logs/matelas_app.log`
- Utiliser le mode debug pour plus de détails

---

*Module créé pour améliorer l'accessibilité de la documentation technique* 