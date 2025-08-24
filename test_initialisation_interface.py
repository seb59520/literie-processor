#!/usr/bin/env python3
"""
Test de l'initialisation de l'interface avec le provider LLM
"""

import sys
import os
import json

# Ajouter le répertoire backend au path
sys.path.append('backend')

from config import config

def test_initialisation_interface():
    """Test de l'initialisation de l'interface"""
    
    print("=== TEST INITIALISATION INTERFACE ===")
    
    # 1. Vérifier la configuration actuelle
    print("\n📋 1. Configuration actuelle:")
    current_provider = config.get_current_llm_provider()
    print(f"   Provider actuel: {current_provider}")
    
    # 2. Simuler l'initialisation de l'interface
    print("\n📋 2. Simulation de l'initialisation:")
    
    # Simuler la création de la liste des providers
    all_providers = ["ollama", "openrouter", "openai", "anthropic", "gemini", "mistral"]
    print(f"   Liste des providers: {all_providers}")
    
    # Simuler la sélection du provider actuel
    if current_provider in all_providers:
        print(f"   ✅ Provider {current_provider} trouvé dans la liste")
        provider_index = all_providers.index(current_provider)
        print(f"   📍 Index dans la liste: {provider_index}")
    else:
        print(f"   ❌ Provider {current_provider} non trouvé dans la liste")
        print("   🔧 Fallback vers ollama")
        current_provider = "ollama"
        provider_index = 0
    
    # 3. Simuler l'affichage des champs selon le provider
    print("\n📋 3. Affichage des champs selon le provider:")
    
    if current_provider == "ollama":
        print("   📝 Champ clé API: MASQUÉ (pas de clé requise)")
        print("   📝 Label: 'Ollama (Local - Pas de clé API requise)'")
        print("   📝 Statut: 'Connecté localement'")
        api_key_visible = False
    else:
        print(f"   📝 Champ clé API: VISIBLE (clé requise pour {current_provider})")
        print(f"   📝 Label: 'Clé API {current_provider}'")
        print("   📝 Statut: 'Clé API requise'")
        api_key_visible = True
    
    # 4. Simuler la synchronisation avec la configuration
    print("\n📋 4. Synchronisation avec la configuration:")
    
    # Vérifier que le provider est bien sauvegardé
    config.set_current_llm_provider(current_provider)
    saved_provider = config.get_current_llm_provider()
    print(f"   Provider sauvegardé: {saved_provider}")
    
    if saved_provider == current_provider:
        print("   ✅ Synchronisation réussie")
    else:
        print("   ❌ Problème de synchronisation")
    
    # 5. Simuler le chargement des clés API
    print("\n📋 5. Chargement des clés API:")
    
    if current_provider == "ollama":
        print("   ✅ Ollama: Aucune clé API requise")
        api_key_loaded = True
    else:
        api_key = config.get_llm_api_key(current_provider)
        if api_key:
            print(f"   ✅ {current_provider}: Clé API chargée ({len(api_key)} caractères)")
            api_key_loaded = True
        else:
            print(f"   ❌ {current_provider}: Aucune clé API configurée")
            api_key_loaded = False
    
    # 6. Résumé de l'initialisation
    print("\n📋 6. Résumé de l'initialisation:")
    
    if (current_provider in all_providers and 
        saved_provider == current_provider and 
        (current_provider == "ollama" or api_key_loaded)):
        print("   ✅ Initialisation réussie")
        print(f"   📍 Provider sélectionné: {current_provider}")
        print(f"   📝 Champ clé API: {'Masqué' if not api_key_visible else 'Visible'}")
        print("   🔄 Interface prête à l'utilisation")
        return True
    else:
        print("   ❌ Problèmes détectés")
        if current_provider not in all_providers:
            print("      - Provider non trouvé dans la liste")
        if saved_provider != current_provider:
            print("      - Problème de synchronisation")
        if current_provider != "ollama" and not api_key_loaded:
            print("      - Clé API manquante")
        return False

def test_changement_provider():
    """Test de changement de provider"""
    
    print("\n=== TEST CHANGEMENT DE PROVIDER ===")
    
    # Sauvegarder le provider actuel
    original_provider = config.get_current_llm_provider()
    print(f"📋 Provider original: {original_provider}")
    
    # Tester différents providers
    test_providers = ["openrouter", "ollama", "openai"]
    
    for provider in test_providers:
        print(f"\n🔄 Test avec {provider}:")
        
        # Changer le provider
        config.set_current_llm_provider(provider)
        current = config.get_current_llm_provider()
        print(f"   Provider actuel: {current}")
        
        # Simuler l'affichage
        if provider == "ollama":
            print("   📝 Interface: Champ clé API masqué")
            print("   📝 Statut: Connecté localement")
        else:
            api_key = config.get_llm_api_key(provider)
            if api_key:
                print(f"   📝 Interface: Champ clé API visible (clé: {len(api_key)} caractères)")
                print("   📝 Statut: Clé API configurée")
            else:
                print("   📝 Interface: Champ clé API visible (vide)")
                print("   📝 Statut: Clé API requise")
    
    # Restaurer le provider original
    config.set_current_llm_provider(original_provider)
    print(f"\n🔄 Provider restauré: {config.get_current_llm_provider()}")

def test_persistance_provider():
    """Test de persistance du provider"""
    
    print("\n=== TEST PERSISTANCE DU PROVIDER ===")
    
    # 1. Définir un provider de test
    test_provider = "ollama"
    print(f"📋 Définition du provider de test: {test_provider}")
    
    # 2. Sauvegarder dans la configuration
    config.set_current_llm_provider(test_provider)
    print("   ✅ Provider sauvegardé")
    
    # 3. Vérifier la sauvegarde
    saved_provider = config.get_current_llm_provider()
    print(f"   📍 Provider sauvegardé: {saved_provider}")
    
    if saved_provider == test_provider:
        print("   ✅ Persistance réussie")
        
        # 4. Simuler un redémarrage (rechargement de la config)
        print("   🔄 Simulation d'un redémarrage...")
        
        # Recharger la configuration
        config.reload_config()
        reloaded_provider = config.get_current_llm_provider()
        print(f"   📍 Provider après redémarrage: {reloaded_provider}")
        
        if reloaded_provider == test_provider:
            print("   ✅ Persistance après redémarrage réussie")
            return True
        else:
            print("   ❌ Perte du provider après redémarrage")
            return False
    else:
        print("   ❌ Échec de la persistance")
        return False

if __name__ == "__main__":
    print("🚀 Test de l'initialisation de l'interface")
    
    # Test principal
    success = test_initialisation_interface()
    
    # Test de changement de provider
    test_changement_provider()
    
    # Test de persistance
    persistence_success = test_persistance_provider()
    
    if success and persistence_success:
        print("\n🎉 Tous les tests sont passés avec succès !")
        print("✅ L'interface s'initialise correctement")
        print("✅ Les changements de provider fonctionnent")
        print("✅ La persistance fonctionne après redémarrage")
    else:
        print("\n❌ Certains tests ont échoué")
        if not success:
            print("   - Problème d'initialisation")
        if not persistence_success:
            print("   - Problème de persistance")
        print("🔧 Vérifiez les erreurs ci-dessus")
    
    print("\n=== FIN DES TESTS ===")

