#!/usr/bin/env python3
"""
Diagnostic de l'interface Ollama
"""

import sys
import os
import json

# Ajouter le répertoire backend au path
sys.path.append('backend')

from config import config

def diagnostic_ollama_interface():
    """Diagnostic complet de l'interface Ollama"""
    
    print("=== DIAGNOSTIC INTERFACE OLLAMA ===")
    
    # 1. Vérifier la configuration actuelle
    print("\n📋 1. Configuration actuelle:")
    current_provider = config.get_current_llm_provider()
    print(f"   Provider actuel: {current_provider}")
    
    # 2. Vérifier tous les providers et leurs clés
    print("\n📋 2. État des providers et clés API:")
    
    providers = ["openrouter", "openai", "anthropic", "gemini", "mistral", "ollama"]
    
    for provider in providers:
        api_key = config.get_llm_api_key(provider)
        status = "✅ Configuré" if api_key else "❌ Non configuré"
        
        if provider == "ollama":
            if not api_key:
                status = "✅ Correct (pas de clé)"
            else:
                status = "⚠️ Incorrect (clé trouvée)"
        
        print(f"   {provider:12}: {status}")
        if api_key:
            print(f"              Clé: {api_key[:20]}...")
    
    # 3. Vérifier la configuration des modèles
    print("\n📋 3. Configuration des modèles:")
    
    for provider in providers:
        model = config.get_llm_model(provider)
        if model:
            print(f"   {provider:12}: {model}")
        else:
            print(f"   {provider:12}: Modèle par défaut")
    
    # 4. Vérifier la configuration Ollama spécifique
    print("\n📋 4. Configuration Ollama spécifique:")
    
    ollama_base_url = config.get_ollama_base_url()
    print(f"   URL de base: {ollama_base_url or 'localhost:11434 (défaut)'}")
    
    ollama_model = config.get_llm_model("ollama")
    print(f"   Modèle: {ollama_model or 'mistral:latest (défaut)'}")
    
    # 5. Vérifier le fichier de configuration
    print("\n📋 5. Fichier de configuration:")
    
    config_file = "matelas_config.json"
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            print(f"   Fichier: {config_file}")
            print(f"   Taille: {os.path.getsize(config_file)} octets")
            
            # Vérifier les clés importantes
            important_keys = [
                "current_llm_provider",
                "llm_api_key_ollama",
                "llm_model_ollama",
                "ollama_base_url"
            ]
            
            for key in important_keys:
                value = config_data.get(key, "Non défini")
                if key == "llm_api_key_ollama":
                    if value:
                        print(f"   ⚠️ {key}: {value[:20]}... (devrait être vide)")
                    else:
                        print(f"   ✅ {key}: Aucune (correct)")
                else:
                    print(f"   {key}: {value}")
                    
        except Exception as e:
            print(f"   ❌ Erreur lecture fichier: {e}")
    else:
        print(f"   ❌ Fichier {config_file} non trouvé")
    
    # 6. Test de changement de provider
    print("\n📋 6. Test de changement de provider:")
    
    try:
        # Sauvegarder le provider actuel
        original_provider = config.get_current_llm_provider()
        print(f"   Provider original: {original_provider}")
        
        # Changer vers OpenRouter
        config.set_current_llm_provider("openrouter")
        openrouter_provider = config.get_current_llm_provider()
        print(f"   Changement vers OpenRouter: {openrouter_provider}")
        
        # Changer vers Ollama
        config.set_current_llm_provider("ollama")
        ollama_provider = config.get_current_llm_provider()
        print(f"   Changement vers Ollama: {ollama_provider}")
        
        # Restaurer le provider original
        config.set_current_llm_provider(original_provider)
        restored_provider = config.get_current_llm_provider()
        print(f"   Restauration: {restored_provider}")
        
        if (openrouter_provider == "openrouter" and 
            ollama_provider == "ollama" and 
            restored_provider == original_provider):
            print("   ✅ Changements de provider réussis")
        else:
            print("   ❌ Problème avec les changements de provider")
            
    except Exception as e:
        print(f"   ❌ Erreur lors des tests: {e}")
    
    # 7. Recommandations
    print("\n📋 7. Recommandations:")
    
    if current_provider == "ollama":
        print("   ✅ Ollama est le provider actuel")
        
        # Vérifier qu'il n'y a pas de clé API pour Ollama
        ollama_key = config.get_llm_api_key("ollama")
        if ollama_key:
            print("   ⚠️ Supprimer la clé API pour Ollama")
            print("   🔧 Commande: config.set_llm_api_key('ollama', '')")
        else:
            print("   ✅ Aucune clé API pour Ollama (correct)")
            
        # Vérifier que le modèle est configuré
        ollama_model = config.get_llm_model("ollama")
        if not ollama_model:
            print("   💡 Définir un modèle par défaut pour Ollama")
            print("   🔧 Commande: config.set_llm_model('ollama', 'mistral:latest')")
        else:
            print(f"   ✅ Modèle configuré: {ollama_model}")
    else:
        print(f"   🔄 Changer vers Ollama: config.set_current_llm_provider('ollama')")
    
    print("\n=== FIN DU DIAGNOSTIC ===")

def fix_ollama_config():
    """Corriger la configuration Ollama si nécessaire"""
    
    print("\n=== CORRECTION CONFIGURATION OLLAMA ===")
    
    # 1. Vérifier et corriger le provider
    current_provider = config.get_current_llm_provider()
    if current_provider != "ollama":
        print(f"🔧 Changement du provider de {current_provider} vers ollama...")
        config.set_current_llm_provider("ollama")
        print("✅ Provider changé vers ollama")
    else:
        print("✅ Ollama est déjà le provider actuel")
    
    # 2. Supprimer la clé API pour Ollama
    ollama_key = config.get_llm_api_key("ollama")
    if ollama_key:
        print(f"🔧 Suppression de la clé API pour Ollama...")
        config.set_llm_api_key("ollama", "")
        print("✅ Clé API supprimée")
    else:
        print("✅ Aucune clé API pour Ollama (correct)")
    
    # 3. Définir un modèle par défaut si nécessaire
    ollama_model = config.get_llm_model("ollama")
    if not ollama_model:
        print("🔧 Définition du modèle par défaut...")
        config.set_llm_model("ollama", "mistral:latest")
        print("✅ Modèle défini: mistral:latest")
    else:
        print(f"✅ Modèle déjà configuré: {ollama_model}")
    
    # 4. Vérifier la configuration finale
    print("\n📋 Configuration finale:")
    final_provider = config.get_current_llm_provider()
    final_key = config.get_llm_api_key("ollama")
    final_model = config.get_llm_model("ollama")
    
    print(f"   Provider: {final_provider}")
    print(f"   Clé API: {'Aucune' if not final_key else final_key}")
    print(f"   Modèle: {final_model}")
    
    if final_provider == "ollama" and not final_key and final_model:
        print("✅ Configuration Ollama corrigée avec succès !")
        return True
    else:
        print("❌ Configuration Ollama encore incorrecte")
        return False

if __name__ == "__main__":
    print("🚀 Diagnostic de l'interface Ollama")
    
    # Diagnostic
    diagnostic_ollama_interface()
    
    # Correction si nécessaire
    print("\n" + "="*50)
    response = input("Voulez-vous corriger automatiquement la configuration ? (o/n): ")
    
    if response.lower() in ['o', 'oui', 'y', 'yes']:
        success = fix_ollama_config()
        if success:
            print("\n🎉 Configuration corrigée !")
            print("✅ Relancez l'application pour tester")
        else:
            print("\n❌ Correction échouée")
            print("🔧 Vérifiez manuellement la configuration")
    else:
        print("\n⏭️ Aucune correction automatique effectuée")
    
    print("\n=== FIN DU PROGRAMME ===")

