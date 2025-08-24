#!/usr/bin/env python3
"""
Script de test pour vérifier le nouveau prompt avec Ollama
"""

import asyncio
import httpx
import json

async def test_new_prompt():
    """Test du nouveau prompt avec Ollama"""
    
    # Texte de test (extrait du PDF)
    test_text = """DEVIS LITERIE
Client:
Mr et Me YVOZ DAVID ET MARIE-PIERRE
Adresse:
1780 CHEMIN DE ZERMEZEELE, 59470 WORMHOUT
Date:
15/12/2024
Référence
Description
Quantité
Prix unitaire
Total
MATELAS LATEX 100% NATUREL PERFORÉ 7 ZONES DIFFÉRENCIÉES FERME - HOUSSE MATELASSÉE TENCEL LUXE 3D LAVABLE A 40°
139/189/22
1
1213,00€
1213,00€
OREILLER 100% LATEX PERFORÉ - HOUSSE TENCEL LAVABLE A 40°
60/60 PLAT
1
68,80€
68,80€
PROTÈGE MATELAS MOLLETON 200GR
1
42,00€
42,00€
PARTICIPATION A LA LIVRAISON ET A L'INSTALLATION
1
120,00€
120,00€
Total TTC: 1443,80€"""

    # Nouveau prompt
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

    try:
        print("🤖 Test du nouveau prompt avec Ollama...")
        print("📝 Prompt envoyé:")
        print("-" * 50)
        print(prompt)
        print("-" * 50)
        
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
            llm_response = result.get("response", "")
            
            print("\n✅ Réponse reçue:")
            print("-" * 50)
            print(llm_response)
            print("-" * 50)
            
            # Essayer de parser le JSON
            try:
                parsed_json = json.loads(llm_response)
                print("\n✅ JSON valide ! Structure détectée:")
                for key in parsed_json.keys():
                    if isinstance(parsed_json[key], list):
                        print(f"  - {key}: {len(parsed_json[key])} éléments")
                    else:
                        print(f"  - {key}: présent")
                return True
            except json.JSONDecodeError as e:
                print(f"\n❌ Erreur parsing JSON: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Erreur lors de l'appel à Ollama: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Test du nouveau prompt")
    print("=" * 50)
    
    success = asyncio.run(test_new_prompt())
    
    if success:
        print("\n✅ Test réussi ! Le nouveau prompt fonctionne.")
    else:
        print("\n❌ Test échoué ! Il y a un problème avec le nouveau prompt.") 