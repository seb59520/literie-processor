"""
Système de cache intelligent pour les appels LLM
"""

import hashlib
import json
import time
import logging
from typing import Dict, Any, Optional, List
from functools import lru_cache
from dataclasses import dataclass, asdict
import threading
from collections import OrderedDict
import pickle
import os

logger = logging.getLogger(__name__)

@dataclass
class CacheEntry:
    """Entrée de cache pour un appel LLM"""
    content: str
    model: str
    provider: str
    timestamp: float
    usage: Dict[str, Any]
    processing_time: float
    cache_hits: int = 0
    
    def is_expired(self, ttl_seconds: int = 3600) -> bool:
        """Vérifie si l'entrée est expirée"""
        return time.time() - self.timestamp > ttl_seconds
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit en dictionnaire pour sérialisation"""
        return asdict(self)

class LLMCache:
    """Cache LRU intelligent pour les appels LLM"""
    
    def __init__(self, max_size: int = 500, ttl_seconds: int = 3600, 
                 persistence_file: Optional[str] = None):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.persistence_file = persistence_file
        
        # Cache principal avec OrderedDict pour LRU
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._lock = threading.RLock()
        
        # Statistiques
        self.stats = {
            'hits': 0,
            'misses': 0,
            'expired_entries': 0,
            'evictions': 0,
            'total_time_saved': 0.0
        }
        
        # Charger le cache depuis le disque si disponible
        self._load_from_disk()
        
        logger.info(f"Cache LLM initialisé: {max_size} entrées max, TTL {ttl_seconds}s")
    
    def _generate_cache_key(self, prompt: str, model: str, provider: str, **kwargs) -> str:
        """Génère une clé de cache unique"""
        # Normaliser le prompt (supprimer espaces en trop, etc.)
        normalized_prompt = ' '.join(prompt.split())
        
        # Inclure les paramètres importants dans la clé
        key_data = {
            'prompt': normalized_prompt,
            'model': model,
            'provider': provider,
            'temperature': kwargs.get('temperature', 0.7),
            'max_tokens': kwargs.get('max_tokens', 8000)
        }
        
        # Hacher pour obtenir une clé compacte
        key_str = json.dumps(key_data, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(key_str.encode('utf-8')).hexdigest()[:32]
    
    def get(self, prompt: str, model: str, provider: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Récupère une réponse du cache"""
        cache_key = self._generate_cache_key(prompt, model, provider, **kwargs)
        
        with self._lock:
            entry = self._cache.get(cache_key)
            
            if entry is None:
                self.stats['misses'] += 1
                return None
            
            # Vérifier l'expiration
            if entry.is_expired(self.ttl_seconds):
                del self._cache[cache_key]
                self.stats['expired_entries'] += 1
                self.stats['misses'] += 1
                return None
            
            # Déplacer vers la fin (LRU)
            self._cache.move_to_end(cache_key)
            
            # Incrémenter le compteur de hits
            entry.cache_hits += 1
            self.stats['hits'] += 1
            self.stats['total_time_saved'] += entry.processing_time
            
            logger.debug(f"Cache HIT pour {provider}/{model} (clé: {cache_key[:8]}...)")
            
            return {
                'success': True,
                'content': entry.content,
                'usage': entry.usage,
                'model': entry.model,
                'processing_time': 0.001,  # Temps cache négligeable
                'cached': True,
                'cache_hits': entry.cache_hits,
                'original_processing_time': entry.processing_time
            }
    
    def put(self, prompt: str, model: str, provider: str, response: Dict[str, Any], **kwargs):
        """Stocke une réponse dans le cache"""
        if not response.get('success', False):
            return  # Ne pas cacher les erreurs
        
        cache_key = self._generate_cache_key(prompt, model, provider, **kwargs)
        
        entry = CacheEntry(
            content=response['content'],
            model=model,
            provider=provider,
            timestamp=time.time(),
            usage=response.get('usage', {}),
            processing_time=response.get('processing_time', 0.0)
        )
        
        with self._lock:
            # Ajouter/remplacer l'entrée
            if cache_key in self._cache:
                # Mettre à jour l'entrée existante
                old_entry = self._cache[cache_key]
                entry.cache_hits = old_entry.cache_hits
            
            self._cache[cache_key] = entry
            self._cache.move_to_end(cache_key)
            
            # Appliquer la limite LRU
            while len(self._cache) > self.max_size:
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]
                self.stats['evictions'] += 1
            
            logger.debug(f"Cache STORE pour {provider}/{model} (clé: {cache_key[:8]}...)")
    
    def clear(self):
        """Vide le cache"""
        with self._lock:
            self._cache.clear()
            logger.info("Cache LLM vidé")
    
    def cleanup_expired(self) -> int:
        """Nettoie les entrées expirées"""
        with self._lock:
            expired_keys = []
            for key, entry in self._cache.items():
                if entry.is_expired(self.ttl_seconds):
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self._cache[key]
                self.stats['expired_entries'] += 1
            
            if expired_keys:
                logger.info(f"Nettoyage cache: {len(expired_keys)} entrées expirées supprimées")
            
            return len(expired_keys)
    
    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du cache"""
        with self._lock:
            total_requests = self.stats['hits'] + self.stats['misses']
            hit_rate = self.stats['hits'] / max(total_requests, 1)
            
            return {
                **self.stats,
                'cache_size': len(self._cache),
                'max_size': self.max_size,
                'hit_rate': hit_rate,
                'total_requests': total_requests,
                'memory_efficiency': len(self._cache) / max(self.max_size, 1)
            }
    
    def get_top_cached_models(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retourne les modèles les plus mis en cache"""
        with self._lock:
            model_stats = {}
            
            for entry in self._cache.values():
                key = f"{entry.provider}/{entry.model}"
                if key not in model_stats:
                    model_stats[key] = {
                        'provider': entry.provider,
                        'model': entry.model,
                        'entries': 0,
                        'total_hits': 0,
                        'avg_processing_time': 0.0
                    }
                
                model_stats[key]['entries'] += 1
                model_stats[key]['total_hits'] += entry.cache_hits
                model_stats[key]['avg_processing_time'] += entry.processing_time
            
            # Calculer les moyennes
            for stats in model_stats.values():
                if stats['entries'] > 0:
                    stats['avg_processing_time'] /= stats['entries']
            
            # Trier par nombre de hits
            sorted_models = sorted(
                model_stats.values(),
                key=lambda x: x['total_hits'],
                reverse=True
            )
            
            return sorted_models[:limit]
    
    def _save_to_disk(self):
        """Sauvegarde le cache sur disque"""
        if not self.persistence_file:
            return
        
        try:
            with self._lock:
                # Filtrer les entrées non expirées
                non_expired = {
                    key: entry for key, entry in self._cache.items()
                    if not entry.is_expired(self.ttl_seconds)
                }
                
                with open(self.persistence_file, 'wb') as f:
                    pickle.dump({
                        'cache': non_expired,
                        'stats': self.stats,
                        'timestamp': time.time()
                    }, f)
                
                logger.debug(f"Cache sauvé sur disque: {len(non_expired)} entrées")
        
        except Exception as e:
            logger.warning(f"Erreur sauvegarde cache: {e}")
    
    def _load_from_disk(self):
        """Charge le cache depuis le disque"""
        if not self.persistence_file or not os.path.exists(self.persistence_file):
            return
        
        try:
            with open(self.persistence_file, 'rb') as f:
                data = pickle.load(f)
            
            # Vérifier l'âge du fichier de cache (max 24h)
            file_age = time.time() - data.get('timestamp', 0)
            if file_age > 86400:  # 24 heures
                logger.info("Cache sur disque trop ancien, ignoré")
                return
            
            with self._lock:
                self._cache = OrderedDict(data.get('cache', {}))
                
                # Nettoyer les entrées expirées
                expired_count = self.cleanup_expired()
                
                # Restaurer les stats (partiellement)
                saved_stats = data.get('stats', {})
                for key in ['hits', 'misses', 'expired_entries']:
                    if key in saved_stats:
                        self.stats[key] = saved_stats[key]
                
                logger.info(
                    f"Cache chargé depuis disque: {len(self._cache)} entrées "
                    f"({expired_count} expirées nettoyées)"
                )
        
        except Exception as e:
            logger.warning(f"Erreur chargement cache: {e}")
    
    def __del__(self):
        """Destructeur - sauvegarde le cache"""
        try:
            self._save_to_disk()
        except:
            pass

# Cache global avec persistance
cache_file = os.path.join(os.path.dirname(__file__), '..', 'logs', 'llm_cache.pkl')
os.makedirs(os.path.dirname(cache_file), exist_ok=True)

llm_cache = LLMCache(
    max_size=1000,
    ttl_seconds=7200,  # 2 heures
    persistence_file=cache_file
)

def cached_llm_call(func):
    """Décorateur pour mettre en cache les appels LLM"""
    def wrapper(self, prompt: str, model: str = "", **kwargs) -> Dict[str, Any]:
        provider = getattr(self, 'provider_name', self.__class__.__name__.replace('Provider', '').lower())
        
        # Tenter de récupérer depuis le cache
        cached_result = llm_cache.get(prompt, model, provider, **kwargs)
        if cached_result:
            return cached_result
        
        # Appel réel à l'API
        result = func(self, prompt, model, **kwargs)
        
        # Stocker en cache si succès
        if result.get('success', False):
            llm_cache.put(prompt, model, provider, result, **kwargs)
        
        return result
    
    return wrapper