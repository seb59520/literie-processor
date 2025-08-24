#!/usr/bin/env python3
"""
Configuration pour l'application de traitement de devis matelas
"""

import os
import json
from pathlib import Path

class Config:
    """Gestionnaire de configuration"""
    
    def __init__(self):
        self.config_file = Path.home() / ".matelas_config.json"
        self.config = self._load_config()
    
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
        # Nettoyer la clé API
        api_key = api_key.strip()
        self.config['openrouter_api_key'] = api_key
        self._save_config()
    
    def get_last_commande_client(self):
        """Récupère le dernier nom de client utilisé"""
        return self.config.get('last_commande_client', '')
    
    def set_last_commande_client(self, client_name):
        """Définit le dernier nom de client utilisé"""
        self.config['last_commande_client'] = client_name
        self._save_config()
    
    def get_last_semaine(self):
        """Récupère la dernière semaine utilisée"""
        return self.config.get('last_semaine', 1)
    
    def set_last_semaine(self, semaine):
        """Définit la dernière semaine utilisée"""
        self.config['last_semaine'] = semaine
        self._save_config()
    
    def get_last_annee(self):
        """Récupère la dernière année utilisée"""
        return self.config.get('last_annee', 2025)
    
    def set_last_annee(self, annee):
        """Définit la dernière année utilisée"""
        self.config['last_annee'] = annee
        self._save_config()

    def get_noyau_order(self):
        """Récupère l'ordre personnalisé des noyaux (liste de noms exacts)"""
        return self.config.get('noyau_order', [])

    def set_noyau_order(self, noyau_order):
        """Définit l'ordre personnalisé des noyaux (liste de noms exacts)"""
        self.config['noyau_order'] = noyau_order
        self._save_config()

    def get_current_llm_provider(self):
        """Récupère le provider LLM actuel"""
        return self.config.get('current_llm_provider', 'openrouter')

    def set_current_llm_provider(self, provider):
        """Définit le provider LLM actuel"""
        self.config['current_llm_provider'] = provider
        self._save_config()

    def get_llm_api_key(self, provider):
        """Récupère la clé API pour un provider LLM spécifique"""
        return self.config.get(f'llm_api_key_{provider}', '')

    def set_llm_api_key(self, provider, api_key):
        """Définit la clé API pour un provider LLM spécifique"""
        self.config[f'llm_api_key_{provider}'] = api_key
        self._save_config()

    def get_all_llm_providers(self):
        """Récupère tous les providers LLM configurés"""
        providers = {}
        for key, value in self.config.items():
            if key.startswith('llm_api_key_'):
                provider = key.replace('llm_api_key_', '')
                providers[provider] = value
        return providers

    def get_llm_model(self, provider):
        """Récupère le modèle LLM pour un provider spécifique"""
        return self.config.get(f'llm_model_{provider}', '')

    def set_llm_model(self, provider, model):
        """Définit le modèle LLM pour un provider spécifique"""
        self.config[f'llm_model_{provider}'] = model
        self._save_config()

    def get_excel_output_directory(self):
        """Récupère le répertoire de sortie des fichiers Excel"""
        default_output = os.path.join(os.getcwd(), "output")
        return self.config.get('excel_output_directory', default_output)

    def set_excel_output_directory(self, directory):
        """Définit le répertoire de sortie des fichiers Excel"""
        # Normaliser le chemin
        directory = os.path.abspath(directory)
        self.config['excel_output_directory'] = directory
        self._save_config()

# Instance globale
config = Config() 