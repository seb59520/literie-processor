#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier la synchronisation des clés API
"""

import sys
import os

# Ajouter le répertoire backend au path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from config import config
    print("✅ Module config importé avec succès")
except ImportError as e:
    print(f"❌ Erreur d'import config: {e}")
    sys.exit(1)

def test_api_sync():
    """Teste la synchronisation des clés API"""
    print("🧪 Test de synchronisation des clés API")
    print("=" * 50)
    
    # Test des providers disponibles
    providers = ["ollama", "openrouter", "openai", "anthropic"]
    
    for provider in providers:
        print(f"\n📡 Test du provider: {provider}")
        
        # Vérifier si le provider est configuré
        try:
            current_provider = config.get_current_llm_provider()
            print(f"   Provider actuel: {current_provider}")
        except Exception as e:
            print(f"   ❌ Erreur récupération provider actuel: {e}")
            continue
        
        # Vérifier la clé API
        try:
            if provider == "ollama":
                api_key = None
                print(f"   ✅ {provider}: Pas de clé API requise")
            else:
                api_key = config.get_llm_api_key(provider)
                if api_key:
                    # Masquer la clé pour la sécurité
                    masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
                    print(f"   ✅ {provider}: Clé API trouvée ({masked_key})")
                else:
                    print(f"   ⚠️ {provider}: Aucune clé API configurée")
        except Exception as e:
            print(f"   ❌ Erreur récupération clé API {provider}: {e}")
    
    print("\n🎯 Test de configuration complète")
    print("-" * 30)
    
    try:
        # Test de la configuration complète
        current_provider = config.get_current_llm_provider()
        print(f"Provider actuel: {current_provider}")
        
        if current_provider != "ollama":
            api_key = config.get_llm_api_key(current_provider)
            if api_key:
                print(f"✅ Configuration valide pour {current_provider}")
                return True
            else:
                print(f"❌ Aucune clé API configurée pour {current_provider}")
                return False
        else:
            print("✅ Configuration valide pour Ollama (pas de clé requise)")
            return True
            
    except Exception as e:
        print(f"❌ Erreur lors du test de configuration: {e}")
        return False

if __name__ == "__main__":
    success = test_api_sync()
    print(f"\n{'🎉 Test réussi' if success else '❌ Test échoué'}")
    sys.exit(0 if success else 1) 