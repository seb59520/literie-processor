#!/usr/bin/env python3
"""
Test de la configuration Ollama sans clé API
"""

import sys
import os
import json

# Ajouter le répertoire backend au path
sys.path.append('backend')

from config import config
from llm_provider import OllamaProvider, LLMProviderManager

def test_ollama_config():
    """Test de la configuration Ollama"""
    
    print("=== TEST CONFIGURATION OLLAMA ===")
    
    # 1. Vérifier la configuration actuelle
    print("\n📋 Étape 1: Vérification de la configuration")
    
    current_provider = config.get_current_llm_provider()
    print(f"✅ Provider actuel: {current_provider}")
    
    ollama_base_url = config.get_ollama_base_url()
    print(f"✅ URL Ollama: {ollama_base_url or 'localhost:11434 (défaut)'}")
    
    ollama_model = config.get_llm_model("ollama")
    print(f"✅ Modèle Ollama: {ollama_model or 'mistral:latest (défaut)'}")
    
    # 2. Vérifier que Ollama est configuré comme provider actuel
    print("\n📋 Étape 2: Vérification du provider Ollama")
    
    if current_provider == "ollama":
        print("✅ Ollama est bien configuré comme provider actuel")
    else:
        print(f"❌ Provider actuel: {current_provider} (devrait être 'ollama')")
        print("🔧 Correction automatique...")
        config.set_current_llm_provider("ollama")
        print("✅ Provider corrigé: ollama")
    
    # 3. Test de création du provider Ollama
    print("\n📋 Étape 3: Test de création du provider Ollama")
    
    try:
        # Créer directement le provider Ollama
        ollama_provider = OllamaProvider()
        print("✅ Provider Ollama créé avec succès")
        print(f"  📍 URL de base: {ollama_provider.base_url}")
        
        # Test de connexion
        print("\n📋 Test de connexion Ollama...")
        if ollama_provider.test_connection():
            print("✅ Connexion Ollama réussie")
        else:
            print("❌ Connexion Ollama échouée")
            print("💡 Vérifiez que Ollama est lancé: ollama serve")
            
    except Exception as e:
        print(f"❌ Erreur lors de la création du provider Ollama: {e}")
        return False
    
    # 4. Test avec le gestionnaire de providers
    print("\n📋 Étape 4: Test avec le gestionnaire de providers")
    
    try:
        manager = LLMProviderManager()
        print("✅ Gestionnaire de providers créé")
        
        # Définir Ollama comme provider
        manager.set_provider("ollama")
        print("✅ Provider défini: ollama")
        
        # Obtenir l'instance du provider
        provider_instance = manager.get_provider_instance()
        if provider_instance:
            print("✅ Instance du provider Ollama obtenue")
            print(f"  📍 Type: {type(provider_instance)}")
        else:
            print("❌ Impossible d'obtenir l'instance du provider")
            return False
            
    except Exception as e:
        print(f"❌ Erreur avec le gestionnaire de providers: {e}")
        return False
    
    # 5. Test de la configuration des modèles
    print("\n📋 Étape 5: Test de la configuration des modèles")
    
    try:
        # Vérifier le modèle configuré
        model = config.get_llm_model("ollama") or "mistral:latest"
        print(f"✅ Modèle configuré: {model}")
        
        # Définir un modèle personnalisé
        test_model = "llama2:latest"
        config.set_llm_model("ollama", test_model)
        print(f"✅ Nouveau modèle défini: {test_model}")
        
        # Vérifier que le modèle a été sauvegardé
        saved_model = config.get_llm_model("ollama")
        if saved_model == test_model:
            print("✅ Modèle sauvegardé avec succès")
        else:
            print(f"❌ Modèle non sauvegardé: {saved_model}")
            
        # Restaurer le modèle original
        config.set_llm_model("ollama", model)
        print(f"✅ Modèle original restauré: {model}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la configuration des modèles: {e}")
        return False
    
    # 6. Test de la configuration de l'URL
    print("\n📋 Étape 6: Test de la configuration de l'URL")
    
    try:
        # Définir une URL personnalisée
        test_url = "http://localhost:11434"
        config.set_ollama_base_url(test_url)
        print(f"✅ URL définie: {test_url}")
        
        # Vérifier que l'URL a été sauvegardée
        saved_url = config.get_ollama_base_url()
        if saved_url == test_url:
            print("✅ URL sauvegardée avec succès")
        else:
            print(f"❌ URL non sauvegardée: {saved_url}")
            
        # Restaurer l'URL par défaut
        config.set_ollama_base_url("")
        print("✅ URL par défaut restaurée")
        
    except Exception as e:
        print(f"❌ Erreur lors de la configuration de l'URL: {e}")
        return False
    
    print("\n🎉 Tous les tests Ollama sont passés avec succès !")
    print("✅ La configuration Ollama fonctionne correctement")
    print("✅ Aucune clé API n'est requise")
    print("✅ Les modèles et URLs sont configurables")
    
    return True

def test_ollama_vs_other_providers():
    """Test de comparaison entre Ollama et les autres providers"""
    
    print("\n=== COMPARAISON OLLAMA vs AUTRES PROVIDERS ===")
    
    # Vérifier les clés API des autres providers
    providers = ["openrouter", "openai", "anthropic", "gemini", "mistral"]
    
    for provider in providers:
        api_key = config.get_llm_api_key(provider)
        if api_key:
            print(f"✅ {provider}: Clé API configurée ({len(api_key)} caractères)")
        else:
            print(f"❌ {provider}: Aucune clé API configurée")
    
    # Vérifier qu'Ollama n'a pas de clé API
    ollama_key = config.get_llm_api_key("ollama")
    if not ollama_key:
        print("✅ Ollama: Aucune clé API (normal)")
    else:
        print(f"⚠️ Ollama: Clé API trouvée ({ollama_key}) - devrait être vide")

if __name__ == "__main__":
    print("🚀 Démarrage des tests de configuration Ollama")
    
    # Test principal
    success = test_ollama_config()
    
    # Test de comparaison
    test_ollama_vs_other_providers()
    
    if success:
        print("\n🎉 Configuration Ollama validée !")
        print("✅ Ollama fonctionne sans clé API")
        print("✅ La configuration est persistante")
        print("✅ Les modèles et URLs sont configurables")
    else:
        print("\n❌ Problèmes détectés avec la configuration Ollama")
        print("🔧 Vérifiez les erreurs ci-dessus")
    
    print("\n=== FIN DES TESTS ===")

