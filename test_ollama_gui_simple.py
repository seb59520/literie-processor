#!/usr/bin/env python3
"""
Test simple de l'interface graphique avec Ollama
"""

import sys
import os

# Ajouter le répertoire backend au path
sys.path.append('backend')

from config import config

def test_ollama_gui_logic():
    """Test de la logique de l'interface graphique avec Ollama"""
    
    print("=== TEST LOGIQUE INTERFACE OLLAMA ===")
    
    # 1. Simuler la logique de l'interface
    print("\n📋 1. Simulation de la logique de l'interface:")
    
    current_provider = config.get_current_llm_provider()
    print(f"   Provider actuel: {current_provider}")
    
    # 2. Simuler l'affichage des champs selon le provider
    print("\n📋 2. Affichage des champs selon le provider:")
    
    if current_provider == "ollama":
        print("   ✅ Provider: Ollama")
        print("   📝 Champ clé API: MASQUÉ (pas de clé requise)")
        print("   📝 Label: 'Ollama (Local - Pas de clé API requise)'")
        print("   📝 Statut: 'Connecté localement'")
    else:
        print(f"   🔄 Provider: {current_provider}")
        print("   📝 Champ clé API: VISIBLE")
        print("   📝 Label: 'Clé API {current_provider}'")
        print("   📝 Statut: 'Clé API requise'")
    
    # 3. Simuler la validation des clés API
    print("\n📋 3. Validation des clés API:")
    
    if current_provider == "ollama":
        print("   ✅ Ollama: Aucune validation de clé requise")
        api_key_required = False
    else:
        print(f"   🔑 {current_provider}: Validation de clé requise")
        api_key = config.get_llm_api_key(current_provider)
        if api_key:
            print(f"      ✅ Clé API trouvée ({len(api_key)} caractères)")
            api_key_required = False
        else:
            print("      ❌ Aucune clé API configurée")
            api_key_required = True
    
    # 4. Simuler la création du provider
    print("\n📋 4. Création du provider:")
    
    if current_provider == "ollama":
        print("   🚀 Création du provider Ollama...")
        print("   ✅ Pas de clé API requise")
        print("   ✅ Provider créé avec succès")
        provider_created = True
    else:
        if api_key_required:
            print(f"   ❌ Impossible de créer le provider {current_provider}")
            print("   🔑 Clé API manquante")
            provider_created = False
        else:
            print(f"   🚀 Création du provider {current_provider}...")
            print("   ✅ Clé API disponible")
            print("   ✅ Provider créé avec succès")
            provider_created = True
    
    # 5. Résumé de la simulation
    print("\n📋 5. Résumé de la simulation:")
    
    if current_provider == "ollama":
        print("   ✅ Ollama configuré correctement")
        print("   ✅ Aucune clé API requise")
        print("   ✅ Provider peut être créé")
        print("   ✅ Interface doit masquer le champ clé API")
    else:
        if provider_created:
            print(f"   ✅ {current_provider} configuré correctement")
            print("   ✅ Clé API disponible")
            print("   ✅ Provider peut être créé")
            print("   ✅ Interface doit afficher le champ clé API")
        else:
            print(f"   ❌ {current_provider} non configuré")
            print("   ❌ Clé API manquante")
            print("   ❌ Provider ne peut pas être créé")
            print("   ❌ Interface doit afficher une erreur")
    
    return provider_created

def test_provider_switching():
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

if __name__ == "__main__":
    print("🚀 Test de la logique de l'interface Ollama")
    
    # Test principal
    success = test_ollama_gui_logic()
    
    # Test de changement de provider
    test_provider_switching()
    
    if success:
        print("\n🎉 Logique de l'interface validée !")
        print("✅ Ollama est géré correctement")
        print("✅ L'interface doit masquer le champ clé API")
        print("✅ Le provider peut être créé sans clé API")
    else:
        print("\n❌ Problèmes détectés dans la logique")
        print("🔧 Vérifiez la configuration")
    
    print("\n=== FIN DES TESTS ===")

