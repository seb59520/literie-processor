#!/usr/bin/env python3
"""
Script pour tester et diagnostiquer les connexions API
"""

import json
import requests
import sys
from pathlib import Path

def load_config():
    """Charge la configuration depuis matelas_config.json"""
    config_file = Path("matelas_config.json")
    if not config_file.exists():
        print("❌ Fichier matelas_config.json non trouvé")
        return None
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"❌ Erreur lecture config: {e}")
        return None

def test_openrouter_api(api_key):
    """Test de l'API OpenRouter"""
    print("\n🔧 Test OpenRouter API...")
    
    if not api_key or api_key == "VOTRE_CLE_API_ICI":
        print("❌ Clé API OpenRouter manquante ou non configurée")
        return False
    
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        
        # Test simple avec un modèle gratuit
        data = {
            "model": "microsoft/phi-3-mini-128k-instruct:free",
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 10
        }
        
        print(f"🔑 Clé API: {api_key[:20]}...")
        print("📡 Test de connexion...")
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        print(f"📊 Code de réponse: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API OpenRouter: CONNEXION RÉUSSIE")
            return True
        elif response.status_code == 401:
            print("❌ ERREUR 401 - AUTHENTIFICATION ÉCHOUÉE")
            print("   Causes possibles:")
            print("   • Clé API invalide ou incorrecte")
            print("   • Clé expirée") 
            print("   • Permissions insuffisantes")
            print("   • Format de clé incorrect")
            return False
        elif response.status_code == 429:
            print("⚠️ ERREUR 429 - LIMITE DE TAUX ATTEINTE")
            print("   Attendez quelques minutes avant de réessayer")
            return False
        else:
            print(f"❌ ERREUR {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Message: {error_data.get('error', {}).get('message', 'Erreur inconnue')}")
            except:
                print(f"   Réponse: {response.text[:200]}...")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT - Connexion trop lente")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ ERREUR DE CONNEXION - Vérifiez votre internet")
        return False
    except Exception as e:
        print(f"❌ ERREUR INATTENDUE: {e}")
        return False

def test_openai_api(api_key):
    """Test de l'API OpenAI"""
    print("\n🔧 Test OpenAI API...")
    
    if not api_key or api_key == "VOTRE_CLE_API_ICI":
        print("❌ Clé API OpenAI manquante ou non configurée")
        return False
    
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 10
        }
        
        print(f"🔑 Clé API: {api_key[:20]}...")
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        print(f"📊 Code de réponse: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API OpenAI: CONNEXION RÉUSSIE")
            return True
        elif response.status_code == 401:
            print("❌ ERREUR 401 - AUTHENTIFICATION ÉCHOUÉE")
            return False
        else:
            print(f"❌ ERREUR {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        return False

def test_anthropic_api(api_key):
    """Test de l'API Anthropic"""
    print("\n🔧 Test Anthropic API...")
    
    if not api_key or api_key == "VOTRE_CLE_API_ICI":
        print("❌ Clé API Anthropic manquante ou non configurée")
        return False
    
    try:
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 10,
            "messages": [{"role": "user", "content": "Hello"}]
        }
        
        print(f"🔑 Clé API: {api_key[:20]}...")
        
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=data,
            timeout=30
        )
        
        print(f"📊 Code de réponse: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API Anthropic: CONNEXION RÉUSSIE")
            return True
        elif response.status_code == 401:
            print("❌ ERREUR 401 - AUTHENTIFICATION ÉCHOUÉE")
            return False
        else:
            print(f"❌ ERREUR {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        return False

def main():
    """Fonction principale de test des APIs"""
    print("=" * 60)
    print("DIAGNOSTIC DES CONNEXIONS API")
    print("=" * 60)
    
    # Charger la configuration
    config = load_config()
    if not config:
        return
    
    print(f"\n📋 Provider actuel: {config.get('current_llm_provider', 'non défini')}")
    
    # Tester les APIs selon la configuration
    current_provider = config.get('current_llm_provider', '')
    tested = False
    
    if current_provider == 'openrouter':
        api_key = config.get('llm_api_key_openrouter', '')
        tested = test_openrouter_api(api_key)
    elif current_provider == 'openai':
        api_key = config.get('llm_api_key_openai', '')
        tested = test_openai_api(api_key)
    elif current_provider == 'anthropic':
        api_key = config.get('llm_api_key_anthropic', '')
        tested = test_anthropic_api(api_key)
    else:
        print(f"⚠️ Provider '{current_provider}' non reconnu")
    
    # Résumé et recommandations
    print("\n" + "=" * 60)
    print("RÉSUMÉ ET SOLUTIONS")
    print("=" * 60)
    
    if not tested:
        print("\n❌ ÉCHEC DE LA CONNEXION API")
        print("\n🔧 SOLUTIONS:")
        print("1. Vérifiez votre clé API dans matelas_config.json")
        print("2. Assurez-vous que le provider est correct")
        print("3. Vérifiez que votre clé n'a pas expiré")
        print("4. Testez votre connexion internet")
        print("5. Vérifiez les permissions de votre clé API")
        print("\n📝 Pour obtenir une clé API:")
        if current_provider == 'openrouter':
            print("   • OpenRouter: https://openrouter.ai/keys")
        elif current_provider == 'openai':
            print("   • OpenAI: https://platform.openai.com/api-keys")
        elif current_provider == 'anthropic':
            print("   • Anthropic: https://console.anthropic.com/")
    else:
        print("\n✅ CONNEXION API RÉUSSIE!")
        print("Votre application devrait maintenant fonctionner correctement.")

if __name__ == "__main__":
    main()