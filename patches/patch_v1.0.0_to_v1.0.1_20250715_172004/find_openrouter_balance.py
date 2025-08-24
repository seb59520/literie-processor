#!/usr/bin/env python3
"""
Script pour trouver l'endpoint correct pour le solde OpenRouter
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
                
                # Chercher des informations de solde/argent
                money_info = extract_money_info(data)
                if money_info:
                    print("💰 Informations financières trouvées:")
                    for key, value in money_info.items():
                        print(f"  - {key}: {value}")
                else:
                    print("⚠️ Aucune information financière trouvée")
                    
            except json.JSONDecodeError:
                print(f"⚠️ Réponse non-JSON: {response.text[:200]}...")
        else:
            print(f"❌ Erreur: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

def extract_money_info(data, prefix=""):
    """Extrait les informations financières d'un objet JSON"""
    money_info = {}
    
    if isinstance(data, dict):
        # Champs liés à l'argent
        money_fields = [
            'balance', 'credits', 'total_spent', 'spent', 'remaining', 'amount', 'available',
            'dollars', 'usd', 'eur', 'money', 'funds', 'account_balance', 'wallet_balance',
            'credit_balance', 'debit_balance', 'current_balance', 'total_balance'
        ]
        
        for field in money_fields:
            if field in data:
                money_info[f"{prefix}{field}" if prefix else field] = data[field]
        
        # Champs imbriqués
        for key, value in data.items():
            if isinstance(value, dict):
                nested_info = extract_money_info(value, f"{key}.")
                money_info.update(nested_info)
            elif isinstance(value, list) and len(value) > 0:
                if isinstance(value[0], dict):
                    nested_info = extract_money_info(value[0], f"{key}[0].")
                    money_info.update(nested_info)
    
    return money_info

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 find_openrouter_balance.py <votre_clé_api>")
        print("Exemple: python3 find_openrouter_balance.py sk-or-v1-...")
        sys.exit(1)
    
    api_key = sys.argv[1]
    
    print("🔍 Recherche de l'endpoint de solde OpenRouter")
    print("=" * 60)
    
    # Endpoints à tester (basés sur la documentation et les forums)
    endpoints = [
        ("https://openrouter.ai/api/v1/auth/key", "Informations de la clé API (limites)"),
        ("https://openrouter.ai/api/v1/account", "Informations du compte"),
        ("https://openrouter.ai/api/v1/user", "Informations utilisateur"),
        ("https://openrouter.ai/api/v1/account/usage", "Utilisation du compte"),
        ("https://openrouter.ai/api/v1/account/billing", "Facturation"),
        ("https://openrouter.ai/api/v1/account/credits", "Crédits du compte"),
        ("https://openrouter.ai/api/v1/account/balance", "Solde du compte"),
        ("https://openrouter.ai/api/v1/account/spending", "Dépenses"),
        ("https://openrouter.ai/api/v1/account/limits", "Limites du compte"),
        ("https://openrouter.ai/api/v1/account/wallet", "Portefeuille"),
        ("https://openrouter.ai/api/v1/account/funds", "Fonds"),
        ("https://openrouter.ai/api/v1/account/payment", "Paiements"),
        ("https://openrouter.ai/api/v1/account/transactions", "Transactions"),
        ("https://openrouter.ai/api/v1/account/history", "Historique"),
        ("https://openrouter.ai/api/v1/account/statistics", "Statistiques"),
    ]
    
    for endpoint, description in endpoints:
        test_endpoint(api_key, endpoint, description)
    
    print("\n🎯 Test terminé!")
    print("\n💡 Conseils:")
    print("- Si aucun endpoint ne donne le solde, vérifiez votre dashboard OpenRouter")
    print("- Le solde peut être accessible uniquement via le dashboard web")
    print("- Certains endpoints peuvent nécessiter des permissions spéciales")

if __name__ == "__main__":
    main() 