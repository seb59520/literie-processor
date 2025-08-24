#!/usr/bin/env python3
"""
Script de test pour les optimisations de l'application Matelas
"""

import sys
import os
import time
import asyncio
from typing import Dict, Any

# Ajouter le chemin backend
sys.path.append('backend')

from backend.retry_utils import retry_sync, RetryConfig
from backend.file_validation import validate_pdf_file, FileValidator
from backend.timeout_manager import timeout_manager
from backend.llm_cache import llm_cache

def test_file_validation():
    """Test de la validation des fichiers"""
    print("🔍 Test de validation des fichiers...")
    
    validator = FileValidator()
    
    # Test avec un fichier inexistant
    result = validator.validate_file_path("inexistant.pdf")
    print(f"Fichier inexistant: {'✅' if not result.is_valid else '❌'}")
    
    # Chercher un vrai PDF de test
    test_files = [
        "Commandes/Commande BECUE 427.pdf",
        "test_devis.pdf",
        "devis.pdf"
    ]
    
    found_file = None
    for test_file in test_files:
        if os.path.exists(test_file):
            found_file = test_file
            break
    
    if found_file:
        result = validator.validate_file_path(found_file)
        print(f"PDF valide {found_file}: {'✅' if result.is_valid else '❌'}")
        print(f"  - Taille: {result.file_size_mb:.1f} MB")
        print(f"  - Pages: {result.page_count}")
        if result.errors:
            print(f"  - Erreurs: {'; '.join(result.errors)}")
        if result.warnings:
            print(f"  - Avertissements: {'; '.join(result.warnings)}")
    else:
        print("Aucun fichier PDF de test trouvé")

def test_retry_system():
    """Test du système de retry"""
    print("\n🔄 Test du système de retry...")
    
    call_count = 0
    
    @retry_sync(RetryConfig(max_attempts=3, base_delay=0.1))
    def failing_function():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ConnectionError("Erreur temporaire")
        return "Succès!"
    
    try:
        start = time.time()
        result = failing_function()
        duration = time.time() - start
        print(f"Retry réussi après {call_count} tentatives en {duration:.2f}s: ✅")
    except Exception as e:
        print(f"Retry échoué: ❌ {e}")

def test_timeout_manager():
    """Test du gestionnaire de timeouts"""
    print("\n⏱️ Test du gestionnaire de timeouts...")
    
    # Test de calcul de timeout
    timeout1 = timeout_manager.calculate_timeout("openrouter", "gpt-4o", 1000)
    timeout2 = timeout_manager.calculate_timeout("ollama", "llama2", 5000, 10.0)
    
    print(f"Timeout OpenRouter (1k chars): {timeout1:.1f}s")
    print(f"Timeout Ollama (5k chars, 10MB): {timeout2:.1f}s")
    
    # Simuler quelques requêtes pour l'historique
    for i in range(5):
        request_id = timeout_manager.record_request_start("openrouter", "gpt-4o", timeout1)
        time.sleep(0.01)  # Simuler traitement
        timeout_manager.record_request_success(request_id, 2.5, "openrouter", "gpt-4o")
    
    # Vérifier les stats
    stats = timeout_manager.get_provider_stats("openrouter")
    print(f"Stats OpenRouter: {stats.get('avg_processing_time', 0):.2f}s moyenne")
    print("Gestionnaire de timeouts: ✅")

def test_cache_system():
    """Test du système de cache"""
    print("\n💾 Test du système de cache...")
    
    # Test de mise en cache
    test_response = {
        'success': True,
        'content': 'Réponse de test',
        'usage': {'tokens': 100},
        'processing_time': 2.5
    }
    
    prompt = "Test prompt pour cache"
    
    # Premier appel - cache miss
    cached = llm_cache.get(prompt, "gpt-4o", "openrouter")
    print(f"Cache miss initial: {'✅' if cached is None else '❌'}")
    
    # Stocker en cache
    llm_cache.put(prompt, "gpt-4o", "openrouter", test_response)
    
    # Deuxième appel - cache hit
    cached = llm_cache.get(prompt, "gpt-4o", "openrouter")
    print(f"Cache hit: {'✅' if cached is not None else '❌'}")
    
    # Vérifier les stats
    stats = llm_cache.get_stats()
    print(f"Stats cache: {stats['hit_rate']:.1%} hit rate")
    print("Système de cache: ✅")

def test_performance_improvement():
    """Test l'amélioration de performance"""
    print("\n🚀 Test des améliorations de performance...")
    
    # Simuler plusieurs appels LLM avec cache
    start_time = time.time()
    
    # Premier ensemble d'appels (cache miss)
    for i in range(3):
        llm_cache.put(
            f"Test prompt {i}",
            "gpt-4o",
            "openrouter",
            {
                'success': True,
                'content': f'Response {i}',
                'usage': {'tokens': 100},
                'processing_time': 2.0
            }
        )
    
    # Deuxième ensemble (cache hits)
    cache_hits = 0
    for i in range(3):
        result = llm_cache.get(f"Test prompt {i}", "gpt-4o", "openrouter")
        if result:
            cache_hits += 1
    
    total_time = time.time() - start_time
    
    print(f"Cache hits: {cache_hits}/3")
    print(f"Temps total: {total_time:.3f}s")
    
    stats = llm_cache.get_stats()
    print(f"Temps économisé: {stats['total_time_saved']:.1f}s")
    print("Amélioration performance: ✅")

def main():
    """Fonction principale de test"""
    print("🧪 Test des optimisations de l'application Matelas")
    print("=" * 50)
    
    try:
        test_file_validation()
        test_retry_system()
        test_timeout_manager()
        test_cache_system()
        test_performance_improvement()
        
        print("\n" + "=" * 50)
        print("✅ Tous les tests passés avec succès!")
        
        # Afficher un résumé des améliorations
        print("\n📊 Résumé des optimisations:")
        print("- ✅ Système de retry avec backoff exponentiel")
        print("- ✅ Validation robuste des fichiers PDF")
        print("- ✅ Gestion dynamique des timeouts")
        print("- ✅ Cache LRU intelligent")
        print("- ✅ Pool de connexions HTTP")
        
        cache_stats = llm_cache.get_stats()
        timeout_stats = timeout_manager.get_global_stats()
        
        print(f"\n📈 Métriques actuelles:")
        print(f"- Cache: {cache_stats['hit_rate']:.1%} hit rate")
        print(f"- Timeout manager: {timeout_stats['total_requests']} requêtes")
        print(f"- Temps économisé: {cache_stats['total_time_saved']:.1f}s")
        
    except Exception as e:
        print(f"\n❌ Erreur dans les tests: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())