# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MATELAS_FINAL is a mattress/bedding PDF processing application. It extracts data from PDF quotes using LLM providers, then generates structured Excel output files. The codebase is primarily in French.

Two product types are handled: **matelas** (mattresses) and **sommiers** (bed bases), each with separate processing pipelines, Excel templates, and cell mappings.

## Key Commands

```bash
# Install and run backend (FastAPI on port 8000)
make install-backend
make run-backend

# Launch desktop GUI
pip install -r requirements_gui.txt
python app_gui.py

# Testing
make test-upload-sim          # Local upload simulation (no server needed)
make test-upload-http         # HTTP test against running server
python test_backend_complet.py
python test_integration_finale.py
python lancer_test_llm.py     # LLM provider tests
python3 test_optimizations.py # Backend optimization tests
python3 test_ui_simple.py     # UI optimization tests

# Web frontend (React/Vite)
cd pdf-extract-app && npm install && npm run dev

# Online admin interface (port 8080)
cd online_admin_interface && pip install -r requirements.txt && python main.py
```

## Architecture

### Data Flow

```
PDF → app_gui.py → backend_interface.py → backend/main.py
                                              ↓
                                    PyMuPDF text extraction
                                              ↓
                                    backend/llm_provider.py (LLM call)
                                              ↓
                                    backend/*_utils.py (29 modules)
                                    + backend/Référentiels/*.json (lookup tables)
                                              ↓
                                    backend/excel_import_utils.py
                                    (template + config/mappings_matelas.json)
                                              ↓
                                         Output Excel
```

### Three UIs

1. **Desktop GUI** (`app_gui.py`, 518 KB) — PyQt6 app, main production interface
2. **Web Frontend** (`pdf-extract-app/`) — React 18 + TypeScript + Vite, alternative web UI
3. **Admin Interface** (`online_admin_interface/`) — FastAPI web app for version/update management (port 8080, HTTP Basic auth)

### Core Layers

- **`backend_interface.py`** (80 KB) — Bridge between GUI and backend. Handles large PDF splitting (>15K chars per chunk), JSON result merging from multi-part LLM responses, and malformed JSON repair.
- **`backend/main.py`** (38 KB) — FastAPI server. Key endpoints: `POST /upload` (PDF processing), `GET /health`.
- **`backend/llm_provider.py`** (21 KB) — Abstract `LLMProvider` with implementations for OpenRouter (default), Ollama, OpenAI, Anthropic, Gemini, Mistral. Includes CircuitBreaker pattern (threshold: 5, recovery: 60s), exponential backoff retry, and HTTP connection pooling.
- **`backend/excel_import_utils.py`** (54 KB) — Populates mattress Excel templates using cell mappings from `config/mappings_matelas.json`.
- **`backend/excel_sommier_import_utils.py`** (77 KB) — Same for bed bases, using `config/mappings_sommiers.json`.

### Backend Utility Modules (`backend/*_utils.py`)

29 specialized modules organized by mattress component:
- **Type detection**: `matelas_utils.py` — identifies 8 mattress types (latex naturel, latex mixte 7 zones, mousse rainurée 7 zones, mousse visco, latex renforcé, select 43, etc.)
- **Component extraction**: `dimensions_utils.py`, `hauteur_utils.py`, `fermete_utils.py`, `housse_utils.py`, `matiere_housse_utils.py`, `poignees_utils.py`, `decoupe_noyau_utils.py`
- **Product-specific referential lookups**: Each mattress type has a `*_referentiel.py` and `*_longueur_housse_utils.py` pair that matches against JSON lookup tables in `backend/Référentiels/`
- **Data preparation**: `pre_import_utils.py`, `article_utils.py`, `client_utils.py`, `date_utils.py`, `operation_utils.py`
- **Infrastructure**: `retry_utils.py` (circuit breaker), `file_validation.py`, `timeout_manager.py`, `llm_cache.py` (LRU + disk persistence), `mapping_manager.py`, `batch_processor.py`

### Update System

A full version distribution system:
- **Server**: `backend/update_server.py` — serves version packages
- **Client**: `backend/auto_updater.py` — checks for updates with telemetry, downloads and installs
- **Admin**: `backend/update_admin_interface.py` + `online_admin_interface/` — web UI for uploading new versions
- **Storage**: `admin_update_storage/versions/` contains ZIP packages, `metadata/manifest.json` tracks all versions

### Configuration Files

- **`matelas_config.json`** — LLM provider choice, API keys, output directories
- **`config/mappings_matelas.json`** — Maps extracted fields to Excel cell positions (e.g., `"Client_D1": "D1"`)
- **`config/mappings_sommiers.json`** — Same for bed bases
- **`config/secure_keys.dat`** — Encrypted API key storage
- **`updater_config.json`** — Update server URL and check frequency
- **`VERSION.json`** — Current app version (semver)

### Excel Templates

Located in `template/` and `backend/template/`:
- `template_matelas.xlsx` — Mattress output template
- `template_sommier.xlsx` — Bed base output template

Cell mappings in config files use Excel coordinates (e.g., "D1", "C10") to position extracted data.

## Development Notes

- File paths support both development and PyInstaller packaging (check `config.py` for path resolution)
- Large PDFs are split into chunks of ~15K chars before LLM calls, then results are merged
- The `backend/Référentiels/` directory contains ~26 JSON lookup tables for pricing, dimensions, and material specifications — these are the source of truth for product rules
- `config.py` manages portable configuration storage (AppData on Windows, home dir on macOS/Linux)
- GUI enhancements can be applied via `MatelasAppEnhancements` from `gui_enhancements.py`
