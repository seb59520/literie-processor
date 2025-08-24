#!/usr/bin/env python3
"""
Test de l'analyse avec Mistral dans l'application complète
"""

import sys
import os
import asyncio

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import config

async def test_mistral_analysis():
    """Test de l'analyse avec Mistral"""
    
    print("🧪 Test de l'analyse avec Mistral")
    print("=" * 50)
    
    # 1. Vérifier que Mistral est configuré
    print("🔍 Vérification de la configuration Mistral...")
    api_key = config.get_llm_api_key("mistral")
    if not api_key:
        print("❌ Aucune clé API Mistral configurée")
        return False
    
    current_provider = config.get_current_llm_provider()
    print(f"📋 Provider actuel: {current_provider}")
    
    # 2. Forcer Mistral comme provider actuel
    print("🔧 Configuration de Mistral comme provider actuel...")
    config.set_current_llm_provider("mistral")
    
    # 3. Test de connexion
    print("🔍 Test de connexion Mistral...")
    import requests
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
    
    # 4. Test d'analyse avec le backend
    print("🔍 Test d'analyse avec le backend...")
    
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
    
    # Importer et tester la fonction call_llm
    try:
        from backend.main import call_llm
        
        print("📤 Appel de l'analyse Mistral...")
        result = await call_llm(test_text)
        
        print("✅ Réponse reçue !")
        print(f"📝 Type de résultat: {type(result)}")
        print(f"📝 Longueur: {len(str(result))}")
        print(f"📝 Début: {str(result)[:200]}...")
        
        # Vérifier si c'est une erreur
        if isinstance(result, str) and result.startswith("Erreur"):
            print(f"❌ Erreur détectée: {result}")
            return False
        
        # Tester le parsing JSON
        try:
            from backend.main import clean_and_parse_json
            cleaned_result = clean_and_parse_json(result)
            import json
            json_data = json.loads(cleaned_result)
            print("✅ JSON valide !")
            print(f"📊 Structure: {list(json_data.keys())}")
            return True
        except Exception as e:
            print(f"❌ Erreur parsing JSON: {e}")
            print(f"📝 Contenu brut: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'appel: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_mistral_analysis())
    
    print("=" * 50)
    if success:
        print("🎉 Test réussi ! L'analyse Mistral fonctionne correctement.")
    else:
        print("💥 Test échoué ! Vérifiez la configuration Mistral.") 