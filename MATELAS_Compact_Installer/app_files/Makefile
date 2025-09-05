# Makefile utilitaire pour le backend

PY=python3
PIP=pip3
HOST?=http://localhost:8000
OLLAMA_BASE_URL?=http://localhost:11434

.PHONY: install-backend run-backend test-upload-sim test-upload-http

install-backend:
	$(PIP) install -r backend/requirements.txt

run-backend:
	OLLAMA_BASE_URL=$(OLLAMA_BASE_URL) $(PY) -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# Simule l'upload en appelant directement la coroutine Python (sans serveur)
test-upload-sim:
	$(PY) scripts/test_upload_local.py

# Test HTTP réel contre un serveur déjà démarré
# Option: HOST=... make test-upload-http
# Ex: HOST=http://localhost:8000 make test-upload-http
test-upload-http:
	HOST=$(HOST) $(PY) scripts/test_upload_http.py
