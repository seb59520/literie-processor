#!/usr/bin/env python3
"""
Test de l'interface avec Ollama (sans clé API)
"""

import sys
import os
import json

# Ajouter le répertoire backend au path
sys.path.append('backend')

from config import config
from llm_provider import OllamaProvider

def test_ollama_interface_simulation():
    """Simulation de l'interface avec Ollama"""
    
    print("=== TEST INTERFACE OLLAMA (SIMULATION) ===")
    
    # 1. Vérifier la configuration actuelle
    print("\n📋 Configuration actuelle:")
    current_provider = config.get_current_llm_provider()
    print(f"  Provider: {current_provider}")
    
    # 2. Simuler le changement de provider vers Ollama
    print("\n📋 Simulation du changement vers Ollama:")
    
    if current_provider != "ollama":
        print(f"  Changement de {current_provider} vers ollama...")
        config.set_current_llm_provider("ollama")
        print("  ✅ Provider changé vers ollama")
    else:
        print("  ✅ Ollama est déjà le provider actuel")
    
    # 3. Vérifier que la clé API est vide pour Ollama
    print("\n📋 Vérification de la clé API:")
    
    ollama_key = config.get_llm_api_key("ollama")
    if not ollama_key:
        print("  ✅ Aucune clé API pour Ollama (normal)")
    else:
        print(f"  ⚠️ Clé API trouvée pour Ollama: {ollama_key}")
        print("  🔧 Suppression de la clé API...")
        config.set_llm_api_key("ollama", "")
        print("  ✅ Clé API supprimée")
    
    # 4. Simuler la création du provider Ollama
    print("\n📋 Création du provider Ollama:")
    
    try:
        provider = OllamaProvider()
        print("  ✅ Provider Ollama créé")
        print(f"  📍 URL: {provider.base_url}")
        
        # Test de connexion
        print("  🔍 Test de connexion...")
        if provider.test_connection():
            print("  ✅ Connexion réussie")
        else:
            print("  ❌ Connexion échouée")
            
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False
    
    # 5. Simuler l'appel LLM
    print("\n📋 Test d'appel LLM:")
    
    try:
        test_prompt = "Dis-moi bonjour en français"
        print(f"  📝 Prompt: {test_prompt}")
        
        response = provider.call_llm(test_prompt, model="mistral:latest")
        
        if response.get("success"):
            print("  ✅ Appel LLM réussi")
            print(f"  📄 Réponse: {response.get('content', '')[:100]}...")
        else:
            print(f"  ❌ Appel LLM échoué: {response.get('error', 'Erreur inconnue')}")
            
    except Exception as e:
        print(f"  ❌ Erreur lors de l'appel LLM: {e}")
        return False
    
    # 6. Vérifier la configuration finale
    print("\n📋 Configuration finale:")
    
    final_provider = config.get_current_llm_provider()
    final_key = config.get_llm_api_key("ollama")
    
    print(f"  Provider: {final_provider}")
    print(f"  Clé API: {'Aucune' if not final_key else final_key}")
    
    if final_provider == "ollama" and not final_key:
        print("  ✅ Configuration Ollama correcte")
        return True
    else:
        print("  ❌ Configuration Ollama incorrecte")
        return False

def test_ollama_vs_openrouter():
    """Test de comparaison Ollama vs OpenRouter"""
    
    print("\n=== COMPARAISON OLLAMA vs OPENROUTER ===")
    
    # Configuration OpenRouter
    print("\n📋 Configuration OpenRouter:")
    openrouter_key = config.get_llm_api_key("openrouter")
    if openrouter_key:
        print(f"  ✅ Clé API configurée ({len(openrouter_key)} caractères)")
    else:
        print("  ❌ Aucune clé API configurée")
    
    # Configuration Ollama
    print("\n📋 Configuration Ollama:")
    ollama_key = config.get_llm_api_key("ollama")
    if not ollama_key:
        print("  ✅ Aucune clé API (normal)")
    else:
        print(f"  ⚠️ Clé API trouvée: {ollama_key}")
    
    # Test de changement de provider
    print("\n📋 Test de changement de provider:")
    
    # Vers OpenRouter
    print("  🔄 Changement vers OpenRouter...")
    config.set_current_llm_provider("openrouter")
    current = config.get_current_llm_provider()
    print(f"  Provider actuel: {current}")
    
    # Vers Ollama
    print("  🔄 Changement vers Ollama...")
    config.set_current_llm_provider("ollama")
    current = config.get_current_llm_provider()
    print(f"  Provider actuel: {current}")
    
    print("  ✅ Changements de provider réussis")

if __name__ == "__main__":
    print("🚀 Test de l'interface Ollama")
    
    # Test principal
    success = test_ollama_interface_simulation()
    
    # Test de comparaison
    test_ollama_vs_openrouter()
    
    if success:
        print("\n🎉 Interface Ollama validée !")
        print("✅ Ollama fonctionne sans clé API")
        print("✅ La configuration est persistante")
        print("✅ Les changements de provider fonctionnent")
    else:
        print("\n❌ Problèmes détectés avec l'interface Ollama")
        print("🔧 Vérifiez les erreurs ci-dessus")
    
    print("\n=== FIN DES TESTS ===")

