#!/usr/bin/env python3
"""
Script pour définir directement la clé API dans la configuration
"""

import json
import sys
import shutil
from pathlib import Path

def backup_config():
    """Sauvegarde la configuration"""
    config_file = Path("matelas_config.json")
    backup_file = Path(f"matelas_config.json.backup")
    
    if config_file.exists():
        shutil.copy(config_file, backup_file)
        print(f"✅ Sauvegarde: {backup_file}")

def set_openrouter_key(api_key):
    """Met à jour la clé API OpenRouter"""
    config_file = Path("matelas_config.json")
    
    # Charger la configuration
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    print("📋 Configuration actuelle:")
    print(f"   Provider: {config.get('current_llm_provider')}")
    print(f"   Clé actuelle: {config.get('llm_api_key_openrouter')}")
    
    # Mettre à jour
    config['llm_api_key_openrouter'] = api_key
    config['current_llm_provider'] = 'openrouter'
    
    # Sauvegarder avec indentation propre
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Clé mise à jour: {api_key[:15]}...")
    
    # Vérification
    with open(config_file, 'r') as f:
        verify_config = json.load(f)
    
    if verify_config.get('llm_api_key_openrouter') == api_key:
        print("✅ Vérification: Clé sauvegardée correctement")
        return True
    else:
        print("❌ Erreur: Clé non sauvegardée")
        return False

def test_api_key(api_key):
    """Teste la clé API"""
    print(f"\n🧪 Test de la clé API: {api_key[:15]}...")
    
    try:
        import requests
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        
        data = {
            "model": "microsoft/phi-3-mini-128k-instruct:free",
            "messages": [{"role": "user", "content": "Test"}],
            "max_tokens": 5
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=15
        )
        
        print(f"📊 Réponse API: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Clé API valide et fonctionnelle!")
            return True
        elif response.status_code == 401:
            print("❌ Erreur 401: Clé API invalide")
            return False
        else:
            print(f"⚠️ Erreur {response.status_code}: {response.text[:100]}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur test API: {e}")
        return False

def main():
    """Fonction principale"""
    print("=" * 60)
    print("CONFIGURATION DIRECTE CLÉ API OPENROUTER")
    print("=" * 60)
    
    if len(sys.argv) != 2:
        print("\nUsage: python set_api_key.py <votre_cle_api>")
        print("\nExemple:")
        print("python set_api_key.py sk-or-v1-abcd1234567890...")
        print("\n💡 Pour obtenir une clé gratuite:")
        print("https://openrouter.ai/ → Account → Keys → Create Key")
        sys.exit(1)
    
    api_key = sys.argv[1].strip()
    
    # Validations basiques
    if api_key == "VOTRE_CLE_API_ICI":
        print("❌ Vous devez utiliser votre vraie clé, pas le placeholder!")
        sys.exit(1)
    
    if len(api_key) < 20:
        print("⚠️ La clé semble très courte. Êtes-vous sûr?")
    
    # Sauvegarde
    backup_config()
    
    # Mise à jour
    if set_openrouter_key(api_key):
        
        # Test
        if test_api_key(api_key):
            print("\n" + "=" * 60)
            print("🎉 SUCCÈS! CLÉ API CONFIGURÉE ET TESTÉE")
            print("=" * 60)
            print("\nMaintenant:")
            print("1. Fermez l'application si elle est ouverte")
            print("2. Nettoyez le cache: find . -name '__pycache__' -exec rm -rf {} +")
            print("3. Relancez: python app_gui.py")
            print("4. Vos fichiers Excel seront générés!")
            
        else:
            print("\n" + "=" * 60)
            print("⚠️ CLÉ SAUVEGARDÉE MAIS TEST ÉCHOUÉ")
            print("=" * 60)
            print("\nLa clé a été sauvegardée mais le test API a échoué.")
            print("Essayez quand même de lancer l'application.")
    else:
        print("❌ Erreur lors de la sauvegarde")

if __name__ == "__main__":
    main()