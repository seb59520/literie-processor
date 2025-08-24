#!/usr/bin/env python3
"""
Test de diagnostic pour le problème JSON avec Ollama
"""

import asyncio
import httpx
import json
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_ollama_json():
    """Test simple pour diagnostiquer le problème JSON avec Ollama"""
    
    # Texte de test simple
    test_text = """DEVIS LITERIE
Client: Mr et Me YVOZ DAVID ET MARIE-PIERRE
Adresse: 1780 CHEMIN DE ZERMEZEELE, 59470 WORMHOUT
Date: 15/12/2024

MATELAS LATEX 100% NATUREL PERFORÉ 7 ZONES DIFFÉRENCIÉES FERME - HOUSSE MATELASSÉE TENCEL LUXE 3D LAVABLE A 40°
139/189/22
1
1213,00€
1213,00€"""

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

    try:
        print("🤖 Test de diagnostic Ollama JSON...")
        print("📝 Envoi de la requête à Ollama...")
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "mistral:latest",
                    "prompt": prompt,
                    "stream": False
                }
            )
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ Réponse HTTP reçue: {response.status_code}")
            print(f"📋 Structure de la réponse: {list(result.keys())}")
            
            # Vérification de la structure de la réponse
            if "response" not in result:
                print(f"❌ Champ 'response' manquant dans la réponse")
                print(f"📄 Réponse complète: {result}")
                return False
            
            llm_response = result.get("response", "")
            print(f"📏 Longueur de la réponse: {len(llm_response)}")
            
            if not llm_response or llm_response.strip() == "":
                print("❌ Réponse Ollama vide")
                return False
            
            print(f"📄 Réponse Ollama (premiers 500 caractères):")
            print("-" * 50)
            print(llm_response[:500])
            print("-" * 50)
            
            # Test de parsing JSON
            try:
                parsed_json = json.loads(llm_response)
                print("✅ JSON valide !")
                print(f"📊 Structure JSON: {list(parsed_json.keys())}")
                return True
            except json.JSONDecodeError as e:
                print(f"❌ Erreur parsing JSON: {e}")
                print(f"📄 Contenu problématique: {llm_response}")
                return False
                
    except Exception as e:
        print(f"❌ Erreur lors de l'appel à Ollama: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_ollama_json())
    if success:
        print("\n🎉 Test réussi !")
    else:
        print("\n💥 Test échoué !") 