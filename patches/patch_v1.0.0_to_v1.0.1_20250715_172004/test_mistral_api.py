#!/usr/bin/env python3
"""
Test de l'API Mistral pour l'envoi de contenu
"""

import requests
import json
import sys
import os

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import config

def test_mistral_api():
    """Test de l'API Mistral"""
    
    # Récupérer la clé API Mistral
    api_key = config.get_llm_api_key("mistral")
    if not api_key:
        print("❌ Aucune clé API Mistral configurée")
        return False
    
    # Test de connexion
    print("🔍 Test de connexion Mistral...")
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        resp = requests.get("https://api.mistral.ai/v1/models", headers=headers, timeout=5)
        if resp.status_code == 200:
            print("✅ Connexion Mistral OK")
        else:
            print(f"❌ Erreur connexion: {resp.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False
    
    # Test d'envoi de contenu
    print("🔍 Test d'envoi de contenu...")
    
    # Texte de test
    test_text = """
    DEVIS N° 2024-001
    
    Société: MATELAS EXPRESS
    Adresse: 123 Rue du Commerce, 75001 Paris
    Téléphone: 01 23 45 67 89
    
    Client: M. DUPONT Jean
    Adresse: 456 Avenue des Champs, 75008 Paris
    
    Articles:
    1. Matelas Latex Naturel 160x200 - 1 unité - 800€
    2. Sommier tapissier 160x200 - 1 unité - 400€
    
    Total TTC: 1200€
    """
    
    # Prompt identique à celui utilisé dans l'application
    prompt = f"""Tu es un assistant expert en extraction de données structurées à partir de documents PDF commerciaux.

Analyse le texte suivant : 

{test_text}

Extrais uniquement les informations sous forme de **JSON**.  
Respecte exactement cette structure :

{{
  "societe": {{
    "nom": "...",
    "capital": "...",
    "adresse": "...",
    "telephone": "...",
    "fax": "...",
    "email": "...",
    "siret": "...",
    "APE": "...",
    "CEE": "...",
    "banque": "...",
    "IBAN": "..."
  }},
  "client": {{
    "nom": "...",
    "adresse": "...",
    "code_client": "..."
  }},
  "commande": {{
    "numero": "...",
    "date": "...",
    "date_validite": "...",
    "commercial": "...",
    "origine": "..."
  }},
  "articles": [
    {{
      "quantite": ...,
      "description": "...",
      "dimensions": "...",
      "pu_ttc": ...,
      "eco_part": ...,
      "pu_ht": ...
    }},
    {{
      "quantite": ...,
      "description": "...",
      "montant": ...
    }}
  ],
  "paiement": {{
    "conditions": "...",
    "port_ht": ...,
    "base_ht": ...,
    "taux_tva": ...,
    "total_ttc": ...,
    "acompte": ...,
    "net_a_payer": ...
  }}
}}

N'invente aucune donnée manquante, laisse la valeur `null` si tu ne la trouves pas.  
Réponds uniquement avec le JSON valide, sans explication ni phrase autour."""

    # Appel API
    url = "https://api.mistral.ai/v1/chat/completions"
    payload = {
        "model": "mistral-large-latest",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 2000
    }
    
    try:
        print("📤 Envoi de la requête...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        
        print("✅ Réponse reçue !")
        print(f"📝 Contenu: {content[:200]}...")
        
        # Tester le parsing JSON
        try:
            json_data = json.loads(content)
            print("✅ JSON valide !")
            print(f"📊 Structure: {list(json_data.keys())}")
            return True
        except json.JSONDecodeError as e:
            print(f"❌ Erreur parsing JSON: {e}")
            print(f"📝 Contenu reçu: {content}")
            
            # Test avec nettoyage des balises markdown
            print("🔧 Test avec nettoyage des balises markdown...")
            cleaned_content = content
            for marker in ['```json', '```JSON', '```', '`']:
                cleaned_content = cleaned_content.replace(marker, '')
            cleaned_content = cleaned_content.strip()
            
            try:
                json_data = json.loads(cleaned_content)
                print("✅ JSON valide après nettoyage !")
                print(f"📊 Structure: {list(json_data.keys())}")
                return True
            except json.JSONDecodeError as e2:
                print(f"❌ Erreur parsing JSON après nettoyage: {e2}")
                return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'appel API: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Test de l'API Mistral")
    print("=" * 50)
    
    success = test_mistral_api()
    
    print("=" * 50)
    if success:
        print("🎉 Test réussi ! L'API Mistral fonctionne correctement.")
    else:
        print("💥 Test échoué ! Vérifiez la configuration.") 