# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MATELAS_FINAL is a comprehensive mattress and bedding processing application that extracts data from PDF documents and generates Excel output files. The application consists of:

- **PyQt6 GUI Frontend** (`app_gui.py`) - Main desktop application interface
- **FastAPI Backend** (`backend/main.py`) - Web API for document processing
- **LLM Integration** - Uses various AI providers (OpenRouter, Ollama) for PDF text extraction
- **Excel Generation** - Creates structured Excel files for mattress specifications

## Key Commands

### Backend Development
```bash
# Install backend dependencies
make install-backend

# Run FastAPI backend server
make run-backend

# Test local upload simulation
make test-upload-sim

# Test HTTP upload against running server
make test-upload-http
```

### GUI Development
```bash
# Install GUI dependencies
pip install -r requirements_gui.txt

# Launch main GUI application
python app_gui.py

# Debug mode (Windows)
diagnostic.bat

# Quick test (Windows)
test_simple.bat
```

### Testing
```bash
# Run LLM tests
python lancer_test_llm.py

# Integration tests
python test_integration_finale.py

# Backend tests
python test_backend_complet.py
```

## Architecture

### Core Components

1. **Frontend (`app_gui.py`)**
   - PyQt6-based desktop application
   - Handles PDF upload, processing interface, and Excel export
   - Integrates with real-time alert system and secure storage

2. **Backend (`backend/`)**
   - FastAPI web service for PDF processing
   - Modular utilities for different mattress types and calculations
   - LLM provider abstraction layer

3. **Configuration System**
   - `config/mappings_matelas.json` - Excel cell mappings for mattresses
   - `config/mappings_sommiers.json` - Excel cell mappings for bed bases
   - `matelas_config.json` - Main application configuration
   - `config/secure_keys.dat` - Encrypted API keys storage

4. **Reference Data (`backend/Référentiels/`)**
   - JSON files containing pricing and specification lookup tables
   - Separate files for different mattress types (latex, foam, visco, etc.)

### Processing Pipeline

1. **PDF Upload** → FastAPI endpoint receives file
2. **Text Extraction** → PyMuPDF extracts text content
3. **LLM Processing** → AI models parse and structure data
4. **Data Validation** → Backend utilities validate extracted information
5. **Excel Generation** → Structured output using openpyxl templates
6. **GUI Display** → Results shown in PyQt6 interface

### Key Modules

- `backend/llm_provider.py` - LLM abstraction (OpenRouter, Ollama)
- `backend/*_utils.py` - Specialized processing for different mattress components
- `backend_interface.py` - Bridge between GUI and backend
- `version.py` - Version management and changelog
- `real_time_alerts.py` - Alert system for processing status

## Configuration

### LLM Providers
The application supports multiple AI providers configured in `matelas_config.json`:
- OpenRouter (default)
- Ollama (local)
- Various model options (GPT, Claude, Mistral, etc.)

### Excel Templates
Located in `template/` and `backend/template/`:
- `template_matelas.xlsx` - Mattress output template
- `template_sommier.xlsx` - Bed base output template

## Development Notes

- The codebase uses both French and English, with French predominant in business logic
- Configuration files use cell mappings (e.g., "D1", "C10") for Excel positioning
- The application handles both mattress ("matelas") and bed base ("sommier") processing
- LLM integration includes fallback providers and error handling
- File paths are configured for both development and PyInstaller packaging

## Testing Strategy

- Unit tests for individual backend utilities
- Integration tests for full processing pipeline
- LLM-specific tests for AI provider functionality
- GUI tests using Qt test framework

## Optimisations Récentes

### Robustesse et Performance
- **Système de retry** : Backoff exponentiel avec circuit breaker
- **Validation des fichiers** : Contrôles préalables de taille, format et contenu
- **Timeouts dynamiques** : Adaptation basée sur l'historique de performance
- **Cache LLM** : Cache LRU intelligent avec persistance sur disque
- **Pool de connexions** : Réutilisation des connexions HTTP

### Nouveaux Modules
- `backend/retry_utils.py` - Gestion des retry et circuit breakers
- `backend/file_validation.py` - Validation robuste des fichiers PDF
- `backend/timeout_manager.py` - Timeouts adaptatifs basés sur l'historique
- `backend/llm_cache.py` - Cache intelligent pour les appels LLM

### Commandes de Test
```bash
# Tester toutes les optimisations
python3 test_optimizations.py

# Vérifier les métriques de performance
python3 -c "from backend.llm_cache import llm_cache; print(llm_cache.get_stats())"
```


## Optimisations Interface Utilisateur

### Modules UI Avancés
- `ui_optimizations.py` - Optimisations de base (animations, responsive, performance)
- `enhanced_processing_ui.py` - Interface de traitement moderne avec progression détaillée
- `gui_enhancements.py` - Améliorations ergonomiques et UX
- `test_ui_simple.py` - Tests des optimisations UI

### Améliorations Implémentées
- **Interface responsive** : Adaptation automatique à la taille d'écran
- **Progression intelligente** : ETA en temps réel et détail des étapes
- **Animations fluides** : Transitions visuelles modernes
- **Sélecteur de fichiers avancé** : Drag & drop et prévisualisation
- **Tooltips intelligents** : Aide contextuelle intégrée
- **Monitoring performance** : Métriques temps réel dans la barre de statut

### Tests Interface
```bash
# Test complet des optimisations UI
python3 test_ui_simple.py

# Test interface PyQt6 (si PyQt6 installé)
python3 test_ui_enhancements.py
```

### Intégration
Les optimisations peuvent être intégrées via:
```python
from gui_enhancements import MatelasAppEnhancements
enhancements = MatelasAppEnhancements(app_instance)
enhancements.apply_all_enhancements()
```
