#!/usr/bin/env python3
"""
Test simple d'Ollama
"""

import asyncio
import httpx

async def test_ollama():
    """Test simple d'Ollama"""
    
    try:
        print("🤖 Test simple d'Ollama...")
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "mistral:latest",
                    "prompt": "Dis-moi juste 'OK'",
                    "stream": False
                }
            )
            response.raise_for_status()
            result = response.json()
            llm_response = result.get("response", "")
            
            print(f"✅ Réponse reçue: {llm_response}")
            return True
                
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_ollama())
    
    if success:
        print("✅ Ollama fonctionne !")
    else:
        print("❌ Problème avec Ollama") 