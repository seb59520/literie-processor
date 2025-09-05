# Guide d'utilisation du système de mise à jour automatique

## Vue d'ensemble

Le système de mise à jour automatique pour MATELAS_FINAL comprend :

1. **Serveur de mise à jour** (`backend/update_server.py`)
2. **Client de mise à jour** (`backend/auto_updater.py`)
3. **Intégration dans l'application** (ajouts dans `app_gui.py`)

## Démarrage rapide

### 1. Démarrer le serveur de mise à jour

```bash
# Option 1: Directement
python backend/update_server.py

# Option 2: Script de démo
python start_demo_server.py
```

Le serveur démarre sur http://localhost:8080

### 2. Tester avec l'application

1. Lancez l'application principale :
   ```bash
   python app_gui.py
   ```

2. Dans le menu "Documentation & Aide", cliquez sur "🔄 Vérifier les mises à jour..."

### 3. Créer un package de mise à jour

```bash
# Créer un package pour la version 3.10.0
python -c "
from backend.update_server import create_update_package
create_update_package('.', '3.10.0')
"
```

### 4. Uploader un package via API

```bash
# Uploader un package (nécessite curl)
curl -X POST "http://localhost:8080/api/v1/upload" \
  -F "version=3.10.0" \
  -F "description=Nouvelle version de test" \
  -F "file=@matelas_v3.10.0_*.zip"
```

## API du serveur

### Endpoints disponibles

- `GET /` - Page d'accueil
- `GET /api/v1/check-updates?current_version=X.X.X` - Vérifier les mises à jour
- `GET /api/v1/versions` - Lister toutes les versions
- `GET /api/v1/download/{version}` - Télécharger une version
- `POST /api/v1/upload` - Uploader une nouvelle version
- `DELETE /api/v1/versions/{version}` - Supprimer une version
- `GET /api/v1/statistics` - Statistiques du serveur

### Exemple de réponse check-updates

```json
{
  "update_available": true,
  "current_version": "3.9.0",
  "latest_version": "3.10.0",
  "release_date": "2025-09-01T10:00:00",
  "description": "Nouvelle version avec améliorations",
  "download_url": "/api/v1/download/3.10.0",
  "file_size": 12345678,
  "changelog": "- Amélioration X\n- Correction Y"
}
```

## Configuration côté client

Le client peut être configuré via l'interface ou par programmation :

```python
from backend.auto_updater import AutoUpdater

updater = AutoUpdater(
    server_url="http://votre-serveur:8080",
    current_version="3.9.0"
)

# Configurer
updater.set_auto_check(True)
updater.set_check_interval(3600)  # 1 heure

# Vérifier manuellement
update_info = updater.check_for_updates()
if update_info and update_info.available:
    print(f"Mise à jour disponible: {update_info.latest_version}")
```

## Déploiement en production

### 1. Serveur de mise à jour

Déployez le serveur sur votre infrastructure :

```bash
# Avec un reverse proxy (nginx, etc.)
python backend/update_server.py --host 0.0.0.0 --port 8080
```

### 2. Configuration client

Modifiez l'URL du serveur dans `app_gui.py` :

```python
self.auto_updater = AutoUpdater(
    server_url="https://votre-domaine.com/updates",
    current_version=current_version
)
```

### 3. Sécurité

- Utilisez HTTPS en production
- Implémentez une authentification si nécessaire
- Vérifiez les signatures des packages (à implémenter)
- Limitez les taux de téléchargement

## Workflow de release

1. **Développement** : Modifiez le code source
2. **Version** : Incrémentez la version avec `version_manager.py`
3. **Package** : Créez le package avec `create_update_package()`
4. **Upload** : Uploadez vers le serveur via l'API
5. **Test** : Vérifiez que les clients reçoivent la mise à jour
6. **Distribution** : Les clients installeront automatiquement

## Dépannage

### Le client ne trouve pas de mises à jour

1. Vérifiez que le serveur est démarré
2. Vérifiez l'URL de connexion
3. Consultez les logs de l'application

### Erreur de téléchargement

1. Vérifiez l'espace disque disponible
2. Vérifiez les permissions d'écriture
3. Vérifiez la connectivité réseau

### Erreur d'installation

1. Fermez complètement l'application avant la mise à jour
2. Vérifiez que les fichiers ne sont pas verrouillés
3. Exécutez l'application en tant qu'administrateur si nécessaire

## Support

Pour obtenir de l'aide ou signaler des problèmes :

1. Consultez les logs de l'application
2. Vérifiez ce guide d'utilisation
3. Contactez l'équipe de développement
