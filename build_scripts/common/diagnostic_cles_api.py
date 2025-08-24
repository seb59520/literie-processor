#!/usr/bin/env python3
"""
Script de diagnostic pour les clés API LLM
Teste la validité des clés API configurées et propose des solutions
"""

import sys
import os
import json
from datetime import datetime

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from config import config
    from backend.llm_provider import llm_manager
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    print("Assurez-vous d'exécuter ce script depuis le répertoire racine du projet")
    sys.exit(1)

def test_api_key(provider, api_key):
    """Teste une clé API spécifique"""
    print(f"\n🔍 Test de la clé API {provider.upper()}")
    print("=" * 50)
    
    if not api_key:
        print("❌ Aucune clé API fournie")
        return False
    
    # Vérifier le format
    print(f"📝 Format de la clé: {api_key[:10]}...")
    
    format_valid = True
    if provider == "openai":
        if not api_key.startswith("sk-"):
            print("❌ Format invalide: doit commencer par 'sk-'")
            format_valid = False
        elif len(api_key) < 20:
            print("❌ Clé trop courte")
            format_valid = False
        else:
            print("✅ Format valide")
            
    elif provider == "anthropic":
        if not api_key.startswith("sk-ant-"):
            print("❌ Format invalide: doit commencer par 'sk-ant-'")
            format_valid = False
        else:
            print("✅ Format valide")
            
    elif provider == "gemini":
        if not api_key.startswith("AIza"):
            print("❌ Format invalide: doit commencer par 'AIza'")
            format_valid = False
        else:
            print("✅ Format valide")
            
    elif provider == "mistral":
        if not api_key.startswith("mist-"):
            print("❌ Format invalide: doit commencer par 'mist-'")
            format_valid = False
        else:
            print("✅ Format valide")
            
    elif provider == "openrouter":
        if not api_key.startswith("sk-or-"):
            print("❌ Format invalide: doit commencer par 'sk-or-'")
            format_valid = False
        else:
            print("✅ Format valide")
    
    if not format_valid:
        return False
    
    # Tester la connexion
    print("🌐 Test de connexion...")
    try:
        llm_manager.set_provider(provider, api_key)
        if llm_manager.test_connection():
            print("✅ Connexion réussie")
            return True
        else:
            print("❌ Connexion échouée")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def show_help(provider):
    """Affiche l'aide pour obtenir une clé API"""
    help_links = {
        "openai": "https://platform.openai.com/api-keys",
        "anthropic": "https://console.anthropic.com/",
        "gemini": "https://makersuite.google.com/app/apikey",
        "mistral": "https://console.mistral.ai/api-keys/",
        "openrouter": "https://openrouter.ai/keys"
    }
    
    print(f"\n💡 Pour obtenir une clé API {provider.upper()}:")
    print(f"   Visitez: {help_links.get(provider, 'Documentation officielle')}")

def main():
    """Fonction principale de diagnostic"""
    print("🔧 DIAGNOSTIC DES CLÉS API LLM")
    print("=" * 60)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Récupérer le provider actuel
    current_provider = config.get_current_llm_provider()
    print(f"Provider actuel: {current_provider}")
    
    # Tester la clé du provider actuel
    if current_provider in ["openai", "anthropic", "gemini", "mistral", "openrouter"]:
        api_key = config.get_llm_api_key(current_provider)
        success = test_api_key(current_provider, api_key)
        
        if not success:
            show_help(current_provider)
    elif current_provider == "ollama":
        print("\n🔍 Test d'Ollama (local)")
        print("=" * 30)
        try:
            llm_manager.set_provider("ollama")
            if llm_manager.test_connection():
                print("✅ Ollama connecté et fonctionnel")
            else:
                print("❌ Ollama non accessible")
                print("💡 Assurez-vous qu'Ollama est installé et en cours d'exécution")
        except Exception as e:
            print(f"❌ Erreur Ollama: {e}")
    else:
        print(f"❌ Provider inconnu: {current_provider}")
    
    # Lister toutes les clés configurées
    print(f"\n📋 CLÉS API CONFIGURÉES")
    print("=" * 40)
    
    providers = ["openai", "anthropic", "gemini", "mistral", "openrouter"]
    for provider in providers:
        api_key = config.get_llm_api_key(provider)
        if api_key:
            status = "✅" if test_api_key(provider, api_key) else "❌"
            print(f"{status} {provider.upper()}: {api_key[:10]}...")
        else:
            print(f"⚠️  {provider.upper()}: Non configuré")
    
    print(f"\n🎯 RECOMMANDATIONS")
    print("=" * 30)
    
    if current_provider == "ollama":
        print("✅ Ollama est configuré - Aucune clé API requise")
    elif current_provider in providers:
        api_key = config.get_llm_api_key(current_provider)
        if not api_key:
            print(f"❌ Aucune clé API configurée pour {current_provider}")
            show_help(current_provider)
        else:
            success = test_api_key(current_provider, api_key)
            if not success:
                print(f"❌ Clé API {current_provider} invalide")
                show_help(current_provider)
            else:
                print(f"✅ Clé API {current_provider} valide")
    else:
        print(f"❌ Provider {current_provider} non supporté")
    
    print(f"\n✨ Diagnostic terminé")

if __name__ == "__main__":
    main() 