"""
Module de gestion des fournisseurs LLM
Gère OpenAI, Anthropic, Gemini, Mistral, OpenRouter avec une interface unifiée
"""

import logging
import requests
import json
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import sys
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Ajouter le répertoire parent au path pour importer config
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import config
from backend.retry_utils import retry_sync, RetryConfig, CircuitBreaker
from backend.timeout_manager import timeout_manager

logger = logging.getLogger(__name__)

class LLMProvider(ABC):
    """Classe abstraite pour les fournisseurs LLM avec retry et circuit breaker"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = self._create_session()
        self.circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=60.0)
        self.retry_config = RetryConfig(
            max_attempts=3,
            base_delay=1.0,
            max_delay=30.0
        )
    
    def _create_session(self) -> requests.Session:
        """Crée une session HTTP avec pool de connexions et retry automatique"""
        session = requests.Session()
        
        # Configuration du retry automatique au niveau HTTP
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            backoff_factor=1,
            respect_retry_after_header=True
        )
        
        adapter = HTTPAdapter(
            pool_connections=10,
            pool_maxsize=20,
            max_retries=retry_strategy
        )
        
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def calculate_dynamic_timeout(self, prompt_length: int, provider: str = "", model: str = "") -> float:
        """Calcule un timeout dynamique basé sur l'historique et la taille"""
        return timeout_manager.calculate_timeout(
            provider or self.__class__.__name__.replace('Provider', '').lower(),
            model,
            request_size_chars=prompt_length
        )
    
    @abstractmethod
    def call_llm(self, prompt: str, model: str = None, **kwargs) -> Dict[str, Any]:
        """Appelle l'API LLM et retourne la réponse"""
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """Teste la connexion à l'API"""
        pass

class OpenAIProvider(LLMProvider):
    """Provider pour OpenAI avec retry et circuit breaker"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://api.openai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    @retry_sync()
    def call_llm(self, prompt: str, model: str = "gpt-4o", **kwargs) -> Dict[str, Any]:
        """Appelle l'API OpenAI avec retry automatique"""
        if not self.circuit_breaker.can_execute():
            return {"success": False, "error": "Circuit breaker ouvert"}
        
        start_time = time.time()
        request_id = ""
        
        try:
            url = f"{self.base_url}/chat/completions"
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": kwargs.get("max_tokens", 8000),
                "temperature": kwargs.get("temperature", 0.7)
            }
            
            timeout = self.calculate_dynamic_timeout(len(prompt), "openai", model)
            request_id = timeout_manager.record_request_start("openai", model, timeout)
            
            response = self.session.post(url, headers=self.headers, json=payload, timeout=timeout)
            response.raise_for_status()
            
            result = response.json()
            processing_time = time.time() - start_time
            
            self.circuit_breaker.record_success()
            timeout_manager.record_request_success(request_id, processing_time, "openai", model)
            
            logger.info(f"OpenAI call successful in {processing_time:.2f}s")
            
            return {
                "success": True,
                "content": result["choices"][0]["message"]["content"],
                "usage": result.get("usage", {}),
                "model": model,
                "processing_time": processing_time
            }
            
        except Exception as e:
            self.circuit_breaker.record_failure()
            
            # Enregistrer le type d'erreur pour le timeout manager
            if "timeout" in str(e).lower() or "timed out" in str(e).lower():
                timeout_manager.record_request_timeout(request_id, "openai", model)
            else:
                timeout_manager.record_request_error(request_id, "openai", model, str(e))
            
            logger.error(f"Erreur OpenAI: {e}")
            return {"success": False, "error": str(e)}
    
    @retry_sync(RetryConfig(max_attempts=2, base_delay=0.5))
    def test_connection(self) -> bool:
        """Teste la connexion OpenAI avec retry"""
        try:
            url = f"{self.base_url}/models"
            response = self.session.get(url, headers=self.headers, timeout=15)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Test connexion OpenAI échoué: {e}")
            return False

class OpenRouterProvider(LLMProvider):
    """Provider pour OpenRouter avec retry et circuit breaker"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/your-repo",
            "X-Title": "MatelasApp"
        }
    
    @retry_sync()
    def call_llm(self, prompt: str, model: str = "openai/gpt-4o", **kwargs) -> Dict[str, Any]:
        """Appelle l'API OpenRouter avec retry automatique"""
        if not self.circuit_breaker.can_execute():
            return {"success": False, "error": "Circuit breaker ouvert"}
        
        start_time = time.time()
        
        try:
            url = f"{self.base_url}/chat/completions"
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": kwargs.get("max_tokens", 8000),
                "temperature": kwargs.get("temperature", 0.7)
            }
            
            timeout = self.calculate_dynamic_timeout(len(prompt))
            response = self.session.post(url, headers=self.headers, json=payload, timeout=timeout)
            response.raise_for_status()
            
            result = response.json()
            processing_time = time.time() - start_time
            
            self.circuit_breaker.record_success()
            
            logger.info(f"OpenRouter call successful in {processing_time:.2f}s")
            
            return {
                "success": True,
                "content": result["choices"][0]["message"]["content"],
                "usage": result.get("usage", {}),
                "model": model,
                "processing_time": processing_time
            }
            
        except Exception as e:
            self.circuit_breaker.record_failure()
            logger.error(f"Erreur OpenRouter: {e}")
            return {"success": False, "error": str(e)}
    
    @retry_sync(RetryConfig(max_attempts=2, base_delay=0.5))
    def test_connection(self) -> bool:
        """Teste la connexion OpenRouter avec retry"""
        try:
            url = f"{self.base_url}/auth/key"
            response = self.session.get(url, headers=self.headers, timeout=15)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Test connexion OpenRouter échoué: {e}")
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
                "max_tokens": kwargs.get("max_tokens", 8000),
                "messages": [{"role": "user", "content": prompt}]
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=120)
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
            response = requests.get(url, headers=self.headers, timeout=30)
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
                    "maxOutputTokens": kwargs.get("max_tokens", 8000),
                    "temperature": kwargs.get("temperature", 0.7)
                }
            }
            
            response = requests.post(url, json=payload, timeout=120)
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
            response = requests.get(url, timeout=30)
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
                "max_tokens": kwargs.get("max_tokens", 8000),
                "temperature": kwargs.get("temperature", 0.7)
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=120)
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
            response = requests.get(url, headers=self.headers, timeout=30)
            return response.status_code == 200
        except:
            return False

class OllamaProvider(LLMProvider):
    """Provider pour Ollama (local)"""
    
    def __init__(self, api_key: str = None):
        # Ollama ne nécessite pas de clé API
        # Base URL configurable via variable d'environnement ou fichier de config
        env_url = os.getenv("OLLAMA_BASE_URL")
        cfg_url = ""
        try:
            # Utiliser la config applicative si disponible
            from config import config as app_config
            cfg_url = app_config.config.get("ollama_base_url", "")
        except Exception:
            cfg_url = ""
        # Fallback localhost si rien n'est fourni
        self.base_url = (env_url or cfg_url or "http://localhost:11434").rstrip('/')
    
    def call_llm(self, prompt: str, model: str = "gpt-oss:20b", **kwargs) -> Dict[str, Any]:
        """Appelle Ollama via subprocess (compatible avec Ollama 0.6.3)"""
        try:
            import subprocess
            
            # Utiliser subprocess pour appeler ollama run directement
            cmd = ["ollama", "run", model, prompt]
            
            # Exécuter la commande
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "content": result.stdout.strip(),
                    "usage": {"total_tokens": 0},  # Ollama ne fournit pas ces infos
                    "model": model
                }
            else:
                logger.error(f"Erreur Ollama subprocess: {result.stderr}")
                return {"success": False, "error": result.stderr}
                
        except Exception as e:
            logger.error(f"Erreur Ollama: {e}")
            return {"success": False, "error": str(e)}
    
    def test_connection(self) -> bool:
        """Teste la connexion Ollama via subprocess"""
        try:
            import subprocess
            
            # Tester si ollama est accessible
            result = subprocess.run(
                ["ollama", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
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
            "ollama": OllamaProvider,
            "openrouter": OpenRouterProvider  # Vrai provider OpenRouter
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
    
    def get_models_for_provider(self, provider_name: str) -> list:
        """Retourne la liste des modèles disponibles pour un provider"""
        models = {
            "openai": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
            "anthropic": ["claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022", "claude-3-opus-20240229"],
            "gemini": ["models/gemini-1.5-pro", "models/gemini-1.5-flash", "models/gemini-pro"],
            "mistral": ["mistral-large-latest", "mistral-medium-latest", "mistral-small-latest"],
            "ollama": ["llama2", "mistral", "codellama", "llama2:13b", "mistral:7b"],
            "openrouter": ["openai/gpt-4o", "openai/gpt-4o-mini", "anthropic/claude-3-5-sonnet", "anthropic/claude-3-5-haiku", "google/gemini-1.5-pro"]
        }
        return models.get(provider_name, [])

# Instance globale
llm_manager = LLMProviderManager()

# Fonctions utilitaires pour l'interface
def get_available_providers() -> list:
    """Fonction utilitaire pour récupérer les providers disponibles"""
    return llm_manager.get_available_providers()

def get_models_for_provider(provider_name: str) -> list:
    """Fonction utilitaire pour récupérer les modèles d'un provider"""
    return llm_manager.get_models_for_provider(provider_name) 