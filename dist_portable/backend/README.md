# Application d'extraction PDF & calcul métier

## Installation rapide

1. Cloner le projet et placer-vous à la racine.
2. Lancer :

```bash
docker-compose up --build
```

3. Accéder à l'application :

[http://localhost:8000](http://localhost:8000)

- Le service Ollama (LLM local) est lancé automatiquement avec le modèle llama3.
- Le backend FastAPI est accessible sur le port 8000.

## Structure

- `main.py` : Backend FastAPI
- `calculs.py` : Règles métier
- `templates/index.html` : Interface web
- `requirements.txt` : Dépendances Python
- `Dockerfile` : Image backend
- `docker-compose.yml` : Orchestration backend + LLM 