#!/usr/bin/env python3
"""
Configuration pour l'application de traitement de devis matelas
Mode portable : le fichier matelas_config.json est stocké dans le dossier de l'exécutable
"""

import os
import sys
import json
from pathlib import Path
import shutil

class Config:
    """Gestionnaire de configuration portable"""
    def __init__(self):
        # Déterminer le dossier de base (portable)
        if hasattr(sys, '_MEIPASS'):
            # Mode PyInstaller
            base_dir = Path(sys._MEIPASS)
        else:
            base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        self.config_file = base_dir / "matelas_config.json"
        self._migrate_from_home()
        self.config = self._load_config()

    def _migrate_from_home(self):
        """Si un ancien fichier existe dans le HOME, le copier ici (migration automatique)"""
        old_file = Path.home() / ".matelas_config.json"
        if old_file.exists() and not self.config_file.exists():
            try:
                shutil.copy(str(old_file), str(self.config_file))
                print(f"[INFO] Migration de la config depuis {old_file} vers {self.config_file}")
            except Exception as e:
                print(f"[WARN] Impossible de migrer l'ancienne config: {e}")

    def _load_config(self):
        """Charge la configuration depuis le fichier"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_config(self):
        """Sauvegarde la configuration dans le fichier"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Erreur sauvegarde config: {e}")

    def get_openrouter_api_key(self):
        """Récupère la clé API OpenRouter"""
        return self.config.get('openrouter_api_key', '')

    def set_openrouter_api_key(self, api_key):
        """Définit la clé API OpenRouter"""
        api_key = api_key.strip()
        self.config['openrouter_api_key'] = api_key
        self._save_config()

    def get_last_commande_client(self):
        return self.config.get('last_commande_client', '')

    def set_last_commande_client(self, client_name):
        self.config['last_commande_client'] = client_name
        self._save_config()

    def get_last_semaine(self):
        return self.config.get('last_semaine', 1)

    def set_last_semaine(self, semaine):
        self.config['last_semaine'] = semaine
        self._save_config()

    def get_last_annee(self):
        return self.config.get('last_annee', 2025)

    def set_last_annee(self, annee):
        self.config['last_annee'] = annee
        self._save_config()

    def get_noyau_order(self):
        return self.config.get('noyau_order', [])

    def set_noyau_order(self, noyau_order):
        self.config['noyau_order'] = noyau_order
        self._save_config()

    def get_current_llm_provider(self):
        return self.config.get('current_llm_provider', 'openrouter')

    def set_current_llm_provider(self, provider):
        self.config['current_llm_provider'] = provider
        self._save_config()

    def get_llm_api_key(self, provider):
        return self.config.get(f'llm_api_key_{provider}', '')

    def set_llm_api_key(self, provider, api_key):
        self.config[f'llm_api_key_{provider}'] = api_key
        self._save_config()

    def get_all_llm_providers(self):
        providers = {}
        for key, value in self.config.items():
            if key.startswith('llm_api_key_'):
                provider = key.replace('llm_api_key_', '')
                providers[provider] = value
        return providers

    def get_llm_model(self, provider):
        return self.config.get(f'llm_model_{provider}', '')

    def set_llm_model(self, provider, model):
        self.config[f'llm_model_{provider}'] = model
        self._save_config()

    # --- Configuration avancée LLM / Réseau ---
    def get_ollama_base_url(self):
        """URL de base pour le service Ollama (ex: http://ollama:11434 en Docker)"""
        # Variable d'environnement prioritaire si définie
        env_val = os.getenv('OLLAMA_BASE_URL')
        if env_val:
            return env_val
        return self.config.get('ollama_base_url', '')

    def set_ollama_base_url(self, url: str):
        url = (url or '').strip()
        self.config['ollama_base_url'] = url
        self._save_config()

    def get_excel_output_directory(self):
        default_output = os.path.join(os.getcwd(), "output")
        return self.config.get('excel_output_directory', default_output)

    def set_excel_output_directory(self, directory):
        directory = os.path.abspath(directory)
        self.config['excel_output_directory'] = directory
        self._save_config()

# Instance globale
config = Config() 