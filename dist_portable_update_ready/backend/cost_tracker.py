"""
Module de tracking des coûts API et historique des fichiers traités
Gère les calculs de coûts, l'historique et les statistiques d'utilisation
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import sqlite3
import threading

logger = logging.getLogger(__name__)

@dataclass
class ApiCall:
    """Représente un appel API avec ses coûts"""
    timestamp: str
    provider: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost_prompt: float
    cost_completion: float
    total_cost: float
    file_name: str
    file_size: int
    processing_time: float
    success: bool
    error_message: str = ""

@dataclass
class ProcessingSession:
    """Représente une session de traitement complète d'un fichier"""
    session_id: str
    timestamp: str
    file_name: str
    file_path: str
    file_size: int
    total_api_calls: int
    total_cost: float
    processing_time: float
    success: bool
    error_message: str = ""
    api_calls: List[ApiCall] = None

class CostTracker:
    """Tracker des coûts API et historique des fichiers"""
    
    # Tarifs par provider (en USD pour 1K tokens)
    PRICING = {
        'openrouter': {
            'openai/gpt-4o': {'prompt': 0.0025, 'completion': 0.01},
            'openai/gpt-4o-mini': {'prompt': 0.000150, 'completion': 0.000600},
            'anthropic/claude-3-5-sonnet': {'prompt': 0.003, 'completion': 0.015},
            'anthropic/claude-3-5-haiku': {'prompt': 0.00025, 'completion': 0.00125},
            'google/gemini-1.5-pro': {'prompt': 0.00125, 'completion': 0.005},
            'deepseek/deepseek-chat-v3.1': {'prompt': 0.0002, 'completion': 0.0008},
        },
        'openai': {
            'gpt-4o': {'prompt': 0.0025, 'completion': 0.01},
            'gpt-4o-mini': {'prompt': 0.000150, 'completion': 0.000600},
            'gpt-4-turbo': {'prompt': 0.01, 'completion': 0.03},
        },
        'anthropic': {
            'claude-3-5-sonnet-20241022': {'prompt': 0.003, 'completion': 0.015},
            'claude-3-5-haiku-20241022': {'prompt': 0.00025, 'completion': 0.00125},
        },
        'ollama': {
            # Ollama est gratuit (local)
            'default': {'prompt': 0.0, 'completion': 0.0}
        }
    }
    
    def __init__(self, db_path: str = "data/cost_tracking.db"):
        """Initialise le tracker avec base de données SQLite"""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._init_database()
    
    def _init_database(self):
        """Initialise les tables de la base de données"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS api_calls (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        provider TEXT NOT NULL,
                        model TEXT NOT NULL,
                        prompt_tokens INTEGER NOT NULL,
                        completion_tokens INTEGER NOT NULL,
                        total_tokens INTEGER NOT NULL,
                        cost_prompt REAL NOT NULL,
                        cost_completion REAL NOT NULL,
                        total_cost REAL NOT NULL,
                        file_name TEXT NOT NULL,
                        file_size INTEGER NOT NULL,
                        processing_time REAL NOT NULL,
                        success BOOLEAN NOT NULL,
                        error_message TEXT,
                        session_id TEXT
                    )
                ''')
                
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS processing_sessions (
                        session_id TEXT PRIMARY KEY,
                        timestamp TEXT NOT NULL,
                        file_name TEXT NOT NULL,
                        file_path TEXT NOT NULL,
                        file_size INTEGER NOT NULL,
                        total_api_calls INTEGER NOT NULL,
                        total_cost REAL NOT NULL,
                        processing_time REAL NOT NULL,
                        success BOOLEAN NOT NULL,
                        error_message TEXT
                    )
                ''')
                
                conn.execute('''
                    CREATE INDEX IF NOT EXISTS idx_timestamp ON api_calls(timestamp)
                ''')
                conn.execute('''
                    CREATE INDEX IF NOT EXISTS idx_session ON api_calls(session_id)
                ''')
                
                conn.commit()
                logger.info("Base de données de tracking initialisée")
                
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de la base: {e}")
    
    def calculate_cost(self, provider: str, model: str, usage: Dict[str, Any]) -> Dict[str, float]:
        """
        Calcule le coût d'un appel API basé sur l'usage
        
        Args:
            provider: Nom du provider (openrouter, openai, etc.)
            model: Nom du modèle utilisé
            usage: Dictionnaire avec prompt_tokens, completion_tokens, total_tokens
            
        Returns:
            Dict avec cost_prompt, cost_completion, total_cost
        """
        try:
            prompt_tokens = usage.get('prompt_tokens', 0)
            completion_tokens = usage.get('completion_tokens', 0)
            
            # Récupérer les tarifs
            provider_pricing = self.PRICING.get(provider, {})
            model_pricing = provider_pricing.get(model)
            
            if not model_pricing:
                # Essayer avec un modèle générique ou le premier disponible
                if provider == 'ollama':
                    model_pricing = {'prompt': 0.0, 'completion': 0.0}
                else:
                    # Utiliser les tarifs du premier modèle disponible comme fallback
                    model_pricing = next(iter(provider_pricing.values()), {'prompt': 0.001, 'completion': 0.002})
                    logger.warning(f"Tarifs non trouvés pour {provider}/{model}, utilisation de tarifs par défaut")
            
            # Calculs (tarifs pour 1K tokens)
            cost_prompt = (prompt_tokens / 1000.0) * model_pricing['prompt']
            cost_completion = (completion_tokens / 1000.0) * model_pricing['completion']
            total_cost = cost_prompt + cost_completion
            
            return {
                'cost_prompt': round(cost_prompt, 6),
                'cost_completion': round(cost_completion, 6),
                'total_cost': round(total_cost, 6)
            }
            
        except Exception as e:
            logger.error(f"Erreur calcul coût: {e}")
            return {'cost_prompt': 0.0, 'cost_completion': 0.0, 'total_cost': 0.0}
    
    def record_api_call(self, provider: str, model: str, usage: Dict[str, Any], 
                       file_name: str, file_size: int, processing_time: float,
                       success: bool, session_id: str = None, error_message: str = "") -> ApiCall:
        """
        Enregistre un appel API dans l'historique
        
        Args:
            provider: Provider utilisé
            model: Modèle utilisé
            usage: Statistiques d'usage (tokens)
            file_name: Nom du fichier traité
            file_size: Taille du fichier en bytes
            processing_time: Temps de traitement en secondes
            success: Succès de l'appel
            session_id: ID de session (optionnel)
            error_message: Message d'erreur (optionnel)
            
        Returns:
            ApiCall: Objet représentant l'appel enregistré
        """
        try:
            with self._lock:
                # Calculer les coûts
                costs = self.calculate_cost(provider, model, usage)
                
                # Créer l'objet ApiCall
                api_call = ApiCall(
                    timestamp=datetime.now().isoformat(),
                    provider=provider,
                    model=model,
                    prompt_tokens=usage.get('prompt_tokens', 0),
                    completion_tokens=usage.get('completion_tokens', 0),
                    total_tokens=usage.get('total_tokens', 0),
                    cost_prompt=costs['cost_prompt'],
                    cost_completion=costs['cost_completion'],
                    total_cost=costs['total_cost'],
                    file_name=file_name,
                    file_size=file_size,
                    processing_time=processing_time,
                    success=success,
                    error_message=error_message
                )
                
                # Enregistrer en base
                with sqlite3.connect(self.db_path) as conn:
                    conn.execute('''
                        INSERT INTO api_calls 
                        (timestamp, provider, model, prompt_tokens, completion_tokens, total_tokens,
                         cost_prompt, cost_completion, total_cost, file_name, file_size, 
                         processing_time, success, error_message, session_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        api_call.timestamp, api_call.provider, api_call.model,
                        api_call.prompt_tokens, api_call.completion_tokens, api_call.total_tokens,
                        api_call.cost_prompt, api_call.cost_completion, api_call.total_cost,
                        api_call.file_name, api_call.file_size, api_call.processing_time,
                        api_call.success, api_call.error_message, session_id
                    ))
                    conn.commit()
                
                logger.info(f"Appel API enregistré: {provider}/{model} - ${api_call.total_cost:.4f}")
                return api_call
                
        except Exception as e:
            logger.error(f"Erreur enregistrement appel API: {e}")
            # Retourner un appel par défaut en cas d'erreur
            return ApiCall(
                timestamp=datetime.now().isoformat(),
                provider=provider, model=model, prompt_tokens=0, completion_tokens=0,
                total_tokens=0, cost_prompt=0.0, cost_completion=0.0, total_cost=0.0,
                file_name=file_name, file_size=file_size, processing_time=processing_time,
                success=False, error_message=str(e)
            )
    
    def start_session(self, file_name: str, file_path: str, file_size: int) -> str:
        """
        Démarre une nouvelle session de traitement
        
        Returns:
            str: ID de session unique
        """
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(file_path) % 10000}"
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT INTO processing_sessions 
                    (session_id, timestamp, file_name, file_path, file_size, 
                     total_api_calls, total_cost, processing_time, success)
                    VALUES (?, ?, ?, ?, ?, 0, 0.0, 0.0, 0)
                ''', (session_id, datetime.now().isoformat(), file_name, file_path, file_size))
                conn.commit()
            
            logger.info(f"Session démarrée: {session_id}")
            return session_id
            
        except Exception as e:
            logger.error(f"Erreur démarrage session: {e}")
            return session_id
    
    def end_session(self, session_id: str, success: bool, error_message: str = ""):
        """Termine une session de traitement et met à jour les statistiques"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Calculer les statistiques de la session
                cursor = conn.execute('''
                    SELECT COUNT(*), SUM(total_cost), SUM(processing_time)
                    FROM api_calls WHERE session_id = ?
                ''', (session_id,))
                
                stats = cursor.fetchone()
                total_calls = stats[0] or 0
                total_cost = stats[1] or 0.0
                total_time = stats[2] or 0.0
                
                # Mettre à jour la session
                conn.execute('''
                    UPDATE processing_sessions 
                    SET total_api_calls = ?, total_cost = ?, processing_time = ?, 
                        success = ?, error_message = ?
                    WHERE session_id = ?
                ''', (total_calls, total_cost, total_time, success, error_message, session_id))
                
                conn.commit()
                
            logger.info(f"Session terminée: {session_id} - {total_calls} appels, ${total_cost:.4f}")
            
        except Exception as e:
            logger.error(f"Erreur fin de session: {e}")
    
    def get_session_cost(self, session_id: str) -> float:
        """Récupère le coût total d'une session"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    SELECT SUM(total_cost) FROM api_calls WHERE session_id = ?
                ''', (session_id,))
                result = cursor.fetchone()
                return result[0] if result[0] else 0.0
        except Exception as e:
            logger.error(f"Erreur récupération coût session: {e}")
            return 0.0
    
    def get_daily_stats(self, date: str = None) -> Dict[str, Any]:
        """
        Récupère les statistiques quotidiennes
        
        Args:
            date: Date au format YYYY-MM-DD (aujourd'hui si None)
            
        Returns:
            Dict avec les statistiques du jour
        """
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    SELECT 
                        COUNT(*) as total_calls,
                        SUM(total_cost) as total_cost,
                        SUM(total_tokens) as total_tokens,
                        COUNT(DISTINCT session_id) as total_sessions,
                        AVG(processing_time) as avg_processing_time
                    FROM api_calls 
                    WHERE date(timestamp) = ?
                ''', (date,))
                
                stats = cursor.fetchone()
                
                # Stats par provider
                cursor = conn.execute('''
                    SELECT provider, COUNT(*), SUM(total_cost)
                    FROM api_calls 
                    WHERE date(timestamp) = ?
                    GROUP BY provider
                ''', (date,))
                
                provider_stats = {row[0]: {'calls': row[1], 'cost': row[2]} for row in cursor.fetchall()}
                
                return {
                    'date': date,
                    'total_calls': stats[0] or 0,
                    'total_cost': round(stats[1] or 0.0, 4),
                    'total_tokens': stats[2] or 0,
                    'total_sessions': stats[3] or 0,
                    'avg_processing_time': round(stats[4] or 0.0, 2),
                    'providers': provider_stats
                }
                
        except Exception as e:
            logger.error(f"Erreur récupération stats quotidiennes: {e}")
            return {'date': date, 'total_calls': 0, 'total_cost': 0.0}
    
    def get_file_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Récupère l'historique des fichiers traités
        
        Args:
            limit: Nombre maximum de sessions à retourner
            
        Returns:
            List des sessions de traitement
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    SELECT * FROM processing_sessions 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (limit,))
                
                columns = [desc[0] for desc in cursor.description]
                sessions = []
                
                for row in cursor.fetchall():
                    session_dict = dict(zip(columns, row))
                    sessions.append(session_dict)
                
                return sessions
                
        except Exception as e:
            logger.error(f"Erreur récupération historique: {e}")
            return []
    
    def export_statistics(self, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """
        Exporte les statistiques détaillées
        
        Args:
            start_date: Date de début (YYYY-MM-DD)
            end_date: Date de fin (YYYY-MM-DD)
            
        Returns:
            Dict avec statistiques détaillées
        """
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Stats globales
                cursor = conn.execute('''
                    SELECT 
                        COUNT(*) as total_calls,
                        SUM(total_cost) as total_cost,
                        SUM(total_tokens) as total_tokens,
                        COUNT(DISTINCT session_id) as total_files,
                        MIN(timestamp) as first_call,
                        MAX(timestamp) as last_call
                    FROM api_calls 
                    WHERE date(timestamp) BETWEEN ? AND ?
                ''', (start_date, end_date))
                
                global_stats = cursor.fetchone()
                
                # Top modèles
                cursor = conn.execute('''
                    SELECT provider, model, COUNT(*), SUM(total_cost)
                    FROM api_calls 
                    WHERE date(timestamp) BETWEEN ? AND ?
                    GROUP BY provider, model
                    ORDER BY SUM(total_cost) DESC
                    LIMIT 10
                ''', (start_date, end_date))
                
                top_models = cursor.fetchall()
                
                return {
                    'period': {'start': start_date, 'end': end_date},
                    'global_stats': {
                        'total_calls': global_stats[0] or 0,
                        'total_cost': round(global_stats[1] or 0.0, 4),
                        'total_tokens': global_stats[2] or 0,
                        'total_files': global_stats[3] or 0,
                        'first_call': global_stats[4],
                        'last_call': global_stats[5]
                    },
                    'top_models': [
                        {
                            'provider': row[0],
                            'model': row[1],
                            'calls': row[2],
                            'cost': round(row[3], 4)
                        } for row in top_models
                    ]
                }
                
        except Exception as e:
            logger.error(f"Erreur export statistiques: {e}")
            return {}


# Instance globale
cost_tracker = CostTracker()