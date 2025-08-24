"""
Module de gestion des fournisseurs LLM
Gère OpenAI, Anthropic, Gemini, Mistral avec une interface unifiée
"""

import logging
import requests
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import sys
import os

# Ajouter le répertoire parent au path pour importer config
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import config

logger = logging.getLogger(__name__)

class LLMProvider(ABC):
    """Classe abstraite pour les fournisseurs LLM"""
    
    @abstractmethod
    def call_llm(self, prompt: str, model: str = None, **kwargs) -> Dict[str, Any]:
        """Appelle l'API LLM et retourne la réponse"""
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """Teste la connexion à l'API"""
        pass

class OpenAIProvider(LLMProvider):
    """Provider pour OpenAI"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def call_llm(self, prompt: str, model: str = "gpt-4o", **kwargs) -> Dict[str, Any]:
        """Appelle l'API OpenAI"""
        try:
            url = f"{self.base_url}/chat/completions"
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": kwargs.get("max_tokens", 4000),
                "temperature": kwargs.get("temperature", 0.7)
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "content": result["choices"][0]["message"]["content"],
                "usage": result.get("usage", {}),
                "model": model
            }
            
        except Exception as e:
            logger.error(f"Erreur OpenAI: {e}")
            return {"success": False, "error": str(e)}
    
    def test_connection(self) -> bool:
        """Teste la connexion OpenAI"""
        try:
            url = f"{self.base_url}/models"
            response = requests.get(url, headers=self.headers, timeout=10)
            return response.status_code == 200
        except:
            return False

class AnthropicProvider(LLMProvider):
    """Provider pour Anthropic"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com/v1"
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
    
    def call_llm(self, prompt: str, model: str = "claude-3-5-sonnet-20241022", **kwargs) -> Dict[str, Any]:
        """Appelle l'API Anthropic"""
        try:
            url = f"{self.base_url}/messages"
            payload = {
                "model": model,
                "max_tokens": kwargs.get("max_tokens", 4000),
                "messages": [{"role": "user", "content": prompt}]
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "content": result["content"][0]["text"],
                "usage": result.get("usage", {}),
                "model": model
            }
            
        except Exception as e:
            logger.error(f"Erreur Anthropic: {e}")
            return {"success": False, "error": str(e)}
    
    def test_connection(self) -> bool:
        """Teste la connexion Anthropic"""
        try:
            url = f"{self.base_url}/models"
            response = requests.get(url, headers=self.headers, timeout=10)
            return response.status_code == 200
        except:
            return False

class GeminiProvider(LLMProvider):
    """Provider pour Google Gemini"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
    
    def call_llm(self, prompt: str, model: str = "models/gemini-1.5-pro", **kwargs) -> Dict[str, Any]:
        """Appelle l'API Gemini"""
        try:
            url = f"{self.base_url}/{model}:generateContent?key={self.api_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "maxOutputTokens": kwargs.get("max_tokens", 4000),
                    "temperature": kwargs.get("temperature", 0.7)
                }
            }
            
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "content": result["candidates"][0]["content"]["parts"][0]["text"],
                "usage": result.get("usageMetadata", {}),
                "model": model
            }
            
        except Exception as e:
            logger.error(f"Erreur Gemini: {e}")
            return {"success": False, "error": str(e)}
    
    def test_connection(self) -> bool:
        """Teste la connexion Gemini"""
        try:
            url = f"{self.base_url}/models?key={self.api_key}"
            response = requests.get(url, timeout=10)
            return response.status_code == 200
        except:
            return False

class MistralProvider(LLMProvider):
    """Provider pour Mistral AI"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.mistral.ai/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def call_llm(self, prompt: str, model: str = "mistral-large-latest", **kwargs) -> Dict[str, Any]:
        """Appelle l'API Mistral"""
        try:
            url = f"{self.base_url}/chat/completions"
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": kwargs.get("max_tokens", 4000),
                "temperature": kwargs.get("temperature", 0.7)
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            if response.status_code == 429:
                logger.error("Erreur Mistral: Limite de requêtes atteinte (429 Too Many Requests)")
                return {"success": False, "error": "Limite de requêtes atteinte (429 Too Many Requests). Attendez ou vérifiez votre quota Mistral."}
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "content": result["choices"][0]["message"]["content"],
                "usage": result.get("usage", {}),
                "model": model
            }
            
        except Exception as e:
            logger.error(f"Erreur Mistral: {e}")
            return {"success": False, "error": str(e)}
    
    def test_connection(self) -> bool:
        """Teste la connexion Mistral"""
        try:
            url = f"{self.base_url}/models"
            response = requests.get(url, headers=self.headers, timeout=10)
            return response.status_code == 200
        except:
            return False

class OllamaProvider(LLMProvider):
    """Provider pour Ollama (local)"""
    
    def __init__(self, api_key: str = None):
        # Ollama ne nécessite pas de clé API
        self.api_key = api_key
        self.base_url = "http://localhost:11434"
        self.headers = {"Content-Type": "application/json"}
    
    def call_llm(self, prompt: str, model: str = "mistral:latest", **kwargs) -> Dict[str, Any]:
        """Appelle l'API Ollama locale"""
        try:
            url = f"{self.base_url}/api/generate"
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": kwargs.get("temperature", 0.7),
                    "num_predict": kwargs.get("max_tokens", 4000)
                }
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "content": result["response"],
                "usage": result.get("usage", {}),
                "model": model
            }
            
        except Exception as e:
            logger.error(f"Erreur Ollama: {e}")
            return {"success": False, "error": str(e)}
    
    def test_connection(self) -> bool:
        """Teste la connexion Ollama locale"""
        try:
            url = f"{self.base_url}/api/tags"
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except:
            return False

class LLMProviderManager:
    """Gestionnaire central des fournisseurs LLM"""
    
    def __init__(self):
        self.providers = {
            "openai": OpenAIProvider,
            "anthropic": AnthropicProvider,
            "gemini": GeminiProvider,
            "mistral": MistralProvider,
            "ollama": OllamaProvider
        }
        self.current_provider = None
        self.current_api_key = None
    
    def set_provider(self, provider_name: str, api_key: str = None):
        """Définit le provider actuel"""
        if provider_name in self.providers:
            self.current_provider = provider_name
            self.current_api_key = api_key
            logger.info(f"Provider défini: {provider_name}")
        else:
            raise ValueError(f"Provider inconnu: {provider_name}")
    
    def get_provider_instance(self) -> Optional[LLMProvider]:
        """Retourne l'instance du provider actuel"""
        if not self.current_provider:
            return None
        
        # Pour Ollama, pas besoin de clé API
        if self.current_provider == "ollama":
            provider_class = self.providers[self.current_provider]
            return provider_class()  # Pas de clé API
        
        # Pour les autres providers, clé API requise
        if not self.current_api_key:
            return None
        
        provider_class = self.providers[self.current_provider]
        return provider_class(self.current_api_key)
    
    def call_llm(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Appelle le LLM avec le provider actuel et le modèle personnalisé si défini"""
        provider_instance = self.get_provider_instance()
        if not provider_instance:
            return {"success": False, "error": "Aucun provider configuré"}
        
        # Récupérer le modèle personnalisé depuis la config
        try:
            from config import config
            model = config.get_llm_model(self.current_provider)
            if model:
                kwargs["model"] = model
        except Exception as e:
            logger.warning(f"Impossible de charger le modèle personnalisé: {e}")
        
        logger.info(f"Appel LLM avec provider: {self.current_provider} (modèle: {kwargs.get('model', 'défaut')})")
        return provider_instance.call_llm(prompt, **kwargs)
    
    def test_connection(self) -> bool:
        """Teste la connexion du provider actuel"""
        provider_instance = self.get_provider_instance()
        if not provider_instance:
            return False
        
        return provider_instance.test_connection()
    
    def get_available_providers(self) -> list:
        """Retourne la liste des providers disponibles"""
        return list(self.providers.keys())

# Instance globale
llm_manager = LLMProviderManager() 