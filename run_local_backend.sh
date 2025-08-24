#!/usr/bin/env bash
set -euo pipefail

# Script de lancement local du backend FastAPI
# - configure l'URL Ollama si non définie
# - installe les dépendances backend si besoin (option --install)
# - lance uvicorn sur 0.0.0.0:8000

usage() {
  echo "Usage: $0 [--install] [--ollama-url URL]" >&2
}

INSTALL=0
OLLAMA_URL="${OLLAMA_BASE_URL:-}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --install)
      INSTALL=1
      shift
      ;;
    --ollama-url)
      OLLAMA_URL="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown arg: $1" >&2
      usage
      exit 1
      ;;
  esac
done

# Définir une URL par défaut si non fournie
if [[ -z "$OLLAMA_URL" ]]; then
  # Par défaut en local, Ollama écoute sur 11434
  OLLAMA_URL="http://localhost:11434"
fi
export OLLAMA_BASE_URL="$OLLAMA_URL"

echo "Using OLLAMA_BASE_URL=$OLLAMA_BASE_URL"

# Option d'installation des dépendances backend
if [[ $INSTALL -eq 1 ]]; then
  echo "Installing backend dependencies..."
  pip3 install -r backend/requirements.txt
fi

# Lancer uvicorn avec le module backend.main
exec python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
