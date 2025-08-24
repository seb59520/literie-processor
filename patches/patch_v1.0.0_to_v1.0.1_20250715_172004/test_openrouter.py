#!/usr/bin/env python3
"""
Script de test pour vérifier l'intégration d'OpenRouter
"""

import asyncio
import httpx
import json
import os

async def test_openrouter_integration():
    """Test l'intégration d'OpenRouter avec un exemple simple"""
    
    # Vérifier si la clé API est disponible
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("❌ Erreur: Clé API OpenRouter manquante")
        print("Définissez la variable d'environnement OPENROUTER_API_KEY")
        return False
    
    # Exemple de texte de devis
    test_text = """
    DEVIS N° 2024-001
    
    Client: Jean Dupont
    Adresse: 123 Rue de la Paix, 75001 Paris
    
    Literie: 160/200
    
    MATELAS JUMEAUX - LATEX 100% NATUREL - 160x200cm    2,00
    HOUSSE DE MATELAS - COTON 100% - 160x200cm          2,00
    SOMMIER À LATTES - BOIS MASSIF - 160x200cm          1,00
    PACK DE 4 PIEDS - CHÊNE MASSIF                       1,00
    
    Remise: 5% enlèvement par vos soins
    """
    
    # Prompt spécialisé (même que dans l'application)
    prompt = f"""Tu es un assistant chargé d'analyser le texte brut d'un devis et d'en extraire uniquement les éléments suivants :

0. Tu identifies les dimensions du projet dans la ligne qui commence par "Literie" ou contenant un format de type "XXX / XXX".
1. Pour chaque matelas : la description complète (sans rien omettre) et la quantité. Si plusieurs matelas sont regroupés sur une ligne, identifie correctement la quantité même si elle est écrite sous forme "2x", "x2", "2,00", ou "2.00". Si deux matelas différents apparaissent dans deux lignes séparées, détecte-les individuellement.
Important : parfois, la quantité est indiquée dans une colonne séparée, en début ou fin de ligne, par exemple :
698,50     2,00   MATELAS JUMEAUX - LATEX 100% NATUREL ...
Dans ce cas, tu dois associer la valeur `2,00` à cette ligne de description comme la quantité, même si le nombre est sur une ligne au-dessus ou décalée.
2. Pour chaque housse : la description complète (sans rien omettre) et la quantité.
3. Pour les pieds : la description complète (en tenant compte des packs, ex: "pack de 4 pieds") et la quantité.
4. Pour chaque sommier : la description complète (sans rien omettre) et la quantité. **Un sommier commence toujours par le mot "SOMMIER" ou "SOMMIERS".** Ne considère jamais un "LIT MOTORISÉ" comme un sommier, même s'il contient "motorisé" ou "moteur".
5. Toutes les informations client (nom, adresse, email, téléphone, etc.).
6. Tous les autres articles non listés ci-dessus doivent être regroupés dans une catégorie **"Autres"**, avec leur description complète et quantité. **N'inclus pas les lignes contenant uniquement une remise, une mention administrative, ou des informations contractuelles.**
⚠️ IMPORTANT : Ne supprime jamais une ligne contenant le mot "remise" si elle contient également les mots "enlèvement", "livraison" ou "expédition".
Dans ce cas, conserve cette ligne dans "Autres" avec sa description complète, et détecte la valeur "mode de mise à disposition" selon les règles suivantes :
- Si elle contient "enlèvement" ou "par vos soins" → "ENLÈVEMENT CLIENT"
- Si elle contient "livraison", "livrer" ou "livré" → "LIVRAISON"
- Si elle contient "expédition" ou "expédié" → "EXPÉDITION"
6bis. Si une ligne contient une remise ET une mention de livraison, d'enlèvement ou d'expédition (ex : "remise : 5% enlèvement par vos soins"), utilise cette ligne pour déterminer le champ `"mode de mise à disposition"` avec les valeurs suivantes :
- Si elle contient "enlèvement" ou "par vos soins" → `"ENLÈVEMENT CLIENT"`
- Si elle contient "livraison", "livrer" ou "livré" → `"LIVRAISON"`
- Si elle contient "expédition" ou "expédié" → `"EXPÉDITION"`
7. Tu identifies si tu trouves des articles DOSSERET ou TETE (attention : majuscules ou minuscules, avec ou sans accents) et tu indiques `"dosseret / tete"` en fonction de ce que tu trouves.
8. Pour chaque matelas, tu identifies s'il s'agit de `"jumeaux"` ou de `"1 pièce"` dans un champ `"jumeau ou 1 pièce"`.
9. Si une taille au format `XX/XXX` est présente à la fin de la ligne de description (ex : `69/ 189` ou `69 / 189`), transforme-la en `"XX x XXX"` et place-la dans un champ `"dimension_housse"`.
10. Si la description du matelas contient un motif de type `XX/XXX"/` (avec ou sans guillemets, slash, ou espaces), transforme-le en `"XX x XXX"` et stocke cette valeur dans le champ `"dimension_housse"`.
11. Si une taille au format `XX/XXX"` ou `XX / XXX"` ou similaire (avec ou sans slash, espace ou guillemet) est présente dans la description du matelas, transforme-la en `"XX x XXX"` et place-la dans le champ `"dimension_housse"`.

Tu dois toujours inclure le champ `"dimension_housse"` dans les matelas si une telle information est détectée.

Tu ne dois **jamais inclure de prix, montants, remises ou délais.**

Renvoie le résultat sous forme JSON **exactement** dans ce format :

```json
{{
  "Matelas": [
    {{
      "description": "...",
      "quantité": ...,
      "jumeau ou 1 pièce": "...",
      "dosseret / tete": "...",
      "dimension_housse": "..."
    }}
  ],
  "Housse": [
    {{
      "description": "...",
      "quantité": ...
    }}
  ],
  "Pieds": [
    {{
      "description": "...",
      "quantité": ...
    }}
  ],
  "Sommier": [
    {{
      "description": "...",
      "quantité": ...
    }}
  ],
  "Autres": [
    {{
      "description": "...",
      "quantité": ...
    }}
  ],
  "Client": {{
    "nom": "...",
    "adresse": "...",
    "Dimension projet": "..."
  }}
}}
```

le texte est: {test_text}"""
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "openai/gpt-4-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1
    }
    
    try:
        print("🚀 Test de l'intégration OpenRouter...")
        print(f"📝 Texte de test: {len(test_text)} caractères")
        
        async with httpx.AsyncClient() as client:
            print("📡 Envoi de la requête à OpenRouter...")
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions", 
                headers=headers, 
                json=payload, 
                timeout=60
            )
            
            print(f"📥 Réponse reçue - Status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"❌ Erreur HTTP: {response.status_code}")
                print(f"Réponse: {response.text}")
                return False
            
            data = response.json()
            raw_response = data["choices"][0]["message"]["content"]
            
            print("✅ Réponse OpenRouter reçue avec succès")
            print(f"📄 Longueur de la réponse: {len(raw_response)} caractères")
            
            # Test du parsing JSON
            try:
                # Nettoyage basique (comme dans l'application)
                import re
                cleaned = re.sub(r'^[\s\S]*?```json', '', raw_response, flags=re.IGNORECASE)
                cleaned = re.sub(r'```[\s\S]*$', '', cleaned)
                cleaned = cleaned.strip()
                
                parsed = json.loads(cleaned)
                print("✅ JSON parsé avec succès")
                
                # Affichage du résultat
                print("\n📊 Résultat de l'analyse:")
                print(f"  - Matelas: {len(parsed.get('Matelas', []))}")
                print(f"  - Housses: {len(parsed.get('Housse', []))}")
                print(f"  - Sommiers: {len(parsed.get('Sommier', []))}")
                print(f"  - Pieds: {len(parsed.get('Pieds', []))}")
                print(f"  - Autres: {len(parsed.get('Autres', []))}")
                
                if parsed.get('Client'):
                    print(f"  - Client: {parsed['Client'].get('nom', 'N/A')}")
                
                print("\n📋 Détails:")
                print(json.dumps(parsed, indent=2, ensure_ascii=False))
                
                return True
                
            except json.JSONDecodeError as e:
                print(f"❌ Erreur parsing JSON: {e}")
                print(f"📄 Réponse brute: {raw_response}")
                return False
                
    except httpx.ConnectError as e:
        print(f"❌ Erreur de connexion: {e}")
        return False
    except httpx.TimeoutException as e:
        print(f"❌ Timeout: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Test d'intégration OpenRouter")
    print("=" * 50)
    
    success = asyncio.run(test_openrouter_integration())
    
    if success:
        print("\n✅ Test réussi! L'intégration OpenRouter fonctionne correctement.")
    else:
        print("\n❌ Test échoué. Vérifiez la configuration d'OpenRouter.") 