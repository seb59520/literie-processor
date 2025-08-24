#!/usr/bin/env python3
"""
Script de test pour diagnostiquer l'API OpenRouter
"""

import requests
import json
import sys

def test_openrouter_api(api_key):
    """Teste l'API OpenRouter et affiche la réponse complète"""
    
    print("🔍 Test de l'API OpenRouter")
    print("=" * 50)
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        print("📡 Envoi de la requête à l'API...")
        response = requests.get("https://openrouter.ai/api/v1/auth/key", headers=headers)
        
        print(f"📊 Code de statut: {response.status_code}")
        print(f"📋 Headers de réponse: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ Réponse JSON complète:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            print("\n🔍 Analyse des champs:")
            print(f"  - Type de données: {type(data)}")
            print(f"  - Clés disponibles: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
            
            # Test des champs possibles
            possible_fields = ['credits', 'balance', 'total_spent', 'spent', 'remaining', 'amount']
            for field in possible_fields:
                if field in data:
                    print(f"  - {field}: {data[field]} (type: {type(data[field])})")
            
            # Test des champs imbriqués
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, dict):
                        print(f"  - {key} (objet): {list(value.keys())}")
                        for subkey in ['credits', 'balance', 'total_spent', 'spent', 'remaining', 'amount']:
                            if subkey in value:
                                print(f"    - {key}.{subkey}: {value[subkey]}")
            
        else:
            print(f"❌ Erreur API: {response.status_code}")
            print(f"📄 Contenu de la réponse: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur lors de la requête: {str(e)}")
        import traceback
        traceback.print_exc()

def test_alternative_endpoints(api_key):
    """Teste d'autres endpoints possibles"""
    
    print("\n🔄 Test d'autres endpoints possibles")
    print("=" * 50)
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    endpoints = [
        "https://openrouter.ai/api/v1/auth/key",
        "https://openrouter.ai/api/v1/auth/keys",
        "https://openrouter.ai/api/v1/auth/balance",
        "https://openrouter.ai/api/v1/auth/credits",
        "https://openrouter.ai/api/v1/account",
        "https://openrouter.ai/api/v1/user"
    ]
    
    for endpoint in endpoints:
        try:
            print(f"\n📡 Test de: {endpoint}")
            response = requests.get(endpoint, headers=headers)
            print(f"  Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"  Réponse: {json.dumps(data, indent=2)[:200]}...")
            else:
                print(f"  Erreur: {response.text[:100]}...")
                
        except Exception as e:
            print(f"  ❌ Erreur: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 test_openrouter_api.py <votre_clé_api>")
        print("Exemple: python3 test_openrouter_api.py sk-or-v1-...")
        sys.exit(1)
    
    api_key = sys.argv[1]
    
    # Test principal
    test_openrouter_api(api_key)
    
    # Test d'autres endpoints
    test_alternative_endpoints(api_key)
    
    print("\n🎯 Diagnostic terminé!") 