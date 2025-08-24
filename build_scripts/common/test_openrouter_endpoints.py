#!/usr/bin/env python3
"""
Script pour tester différents endpoints de l'API OpenRouter
"""

import requests
import json
import sys

def test_endpoint(api_key, endpoint, description=""):
    """Teste un endpoint spécifique"""
    print(f"\n🔍 Test: {description}")
    print(f"📡 Endpoint: {endpoint}")
    print("-" * 60)
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(endpoint, headers=headers, timeout=10)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ Réponse JSON:")
                print(json.dumps(data, indent=2, ensure_ascii=False))
                
                # Chercher des informations de solde
                balance_info = extract_balance_info(data)
                if balance_info:
                    print("💰 Informations de solde trouvées:")
                    for key, value in balance_info.items():
                        print(f"  - {key}: {value}")
                else:
                    print("⚠️ Aucune information de solde trouvée")
                    
            except json.JSONDecodeError:
                print(f"⚠️ Réponse non-JSON: {response.text[:200]}...")
        else:
            print(f"❌ Erreur: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

def extract_balance_info(data, prefix=""):
    """Extrait les informations de solde d'un objet JSON"""
    balance_info = {}
    
    if isinstance(data, dict):
        # Champs directs
        balance_fields = ['credits', 'balance', 'total_spent', 'spent', 'remaining', 'amount', 'available']
        for field in balance_fields:
            if field in data:
                balance_info[f"{prefix}{field}" if prefix else field] = data[field]
        
        # Champs imbriqués
        for key, value in data.items():
            if isinstance(value, dict):
                nested_info = extract_balance_info(value, f"{key}.")
                balance_info.update(nested_info)
            elif isinstance(value, list) and len(value) > 0:
                # Premier élément d'une liste
                if isinstance(value[0], dict):
                    nested_info = extract_balance_info(value[0], f"{key}[0].")
                    balance_info.update(nested_info)
    
    return balance_info

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 test_openrouter_endpoints.py <votre_clé_api>")
        print("Exemple: python3 test_openrouter_endpoints.py sk-or-v1-...")
        sys.exit(1)
    
    api_key = sys.argv[1]
    
    print("🔍 Test des endpoints OpenRouter")
    print("=" * 60)
    
    # Endpoints à tester (basés sur la documentation OpenRouter)
    endpoints = [
        ("https://openrouter.ai/api/v1/auth/key", "Informations de la clé API"),
        ("https://openrouter.ai/api/v1/auth/keys", "Liste des clés API"),
        ("https://openrouter.ai/api/v1/account", "Informations du compte"),
        ("https://openrouter.ai/api/v1/user", "Informations utilisateur"),
        ("https://openrouter.ai/api/v1/account/usage", "Utilisation du compte"),
        ("https://openrouter.ai/api/v1/account/billing", "Facturation"),
        ("https://openrouter.ai/api/v1/account/credits", "Crédits du compte"),
        ("https://openrouter.ai/api/v1/account/balance", "Solde du compte"),
        ("https://openrouter.ai/api/v1/account/spending", "Dépenses"),
        ("https://openrouter.ai/api/v1/account/limits", "Limites du compte"),
    ]
    
    for endpoint, description in endpoints:
        test_endpoint(api_key, endpoint, description)
    
    print("\n🎯 Test terminé!")
    print("\n💡 Conseils:")
    print("- Si aucun endpoint ne fonctionne, vérifiez votre clé API")
    print("- Certains endpoints peuvent nécessiter des permissions spéciales")
    print("- Consultez la documentation OpenRouter pour les endpoints à jour")

if __name__ == "__main__":
    main() 