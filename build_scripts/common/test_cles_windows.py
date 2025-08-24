#!/usr/bin/env python3
"""
Script de test rapide pour Windows - Vérification clé API OpenRouter
"""

import os
import json
import sys
from pathlib import Path

def test_cles_windows():
    """Test rapide de la configuration des clés API sous Windows"""
    
    print("🧪 TEST RAPIDE CLÉS API WINDOWS")
    print("=" * 40)
    
    # Test 1: Vérifier le fichier de configuration
    print("1. 📁 Test fichier de configuration...")
    home_dir = Path.home()
    config_file = home_dir / ".matelas_config.json"
    
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            openrouter_key = config.get('openrouter_api_key')
            if openrouter_key:
                print(f"   ✅ Clé trouvée: {openrouter_key[:10]}...")
            else:
                print("   ❌ Clé OpenRouter non trouvée")
                return False
        except Exception as e:
            print(f"   ❌ Erreur lecture: {e}")
            return False
    else:
        print("   ❌ Fichier de configuration non trouvé")
        return False
    
    # Test 2: Vérifier la variable d'environnement
    print("2. 🌍 Test variable d'environnement...")
    env_key = os.environ.get('OPENROUTER_API_KEY')
    if env_key:
        print(f"   ✅ Variable trouvée: {env_key[:10]}...")
    else:
        print("   ⚠️  Variable d'environnement non définie")
    
    # Test 3: Tester l'import du module config
    print("3. 🔧 Test module de configuration...")
    try:
        import config
        print("   ✅ Module config importé")
        
        # Tester la fonction get_openrouter_api_key
        api_key = config.get_openrouter_api_key()
        if api_key:
            print(f"   ✅ Clé API récupérée: {api_key[:10]}...")
        else:
            print("   ❌ Aucune clé API récupérée")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur module config: {e}")
        return False
    
    # Test 4: Test de connexion OpenRouter (optionnel)
    print("4. 🌐 Test de connexion OpenRouter...")
    try:
        import requests
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # Test simple avec l'API OpenRouter
        response = requests.get('https://openrouter.ai/api/v1/models', headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("   ✅ Connexion OpenRouter réussie")
        else:
            print(f"   ⚠️  Erreur API: {response.status_code}")
            
    except Exception as e:
        print(f"   ⚠️  Erreur connexion: {e}")
    
    print("\n✅ TOUS LES TESTS PRINCIPAUX RÉUSSIS")
    print("🎯 L'application devrait fonctionner correctement")
    
    return True

def afficher_instructions():
    """Affiche les instructions si le test échoue"""
    print("\n📋 INSTRUCTIONS DE CORRECTION:")
    print("1. Exécuter: python diagnostic_cles_windows.py")
    print("2. Exécuter: python corriger_cles_windows.py")
    print("3. Suivre le guide: GUIDE_CORRECTION_WINDOWS.md")

if __name__ == "__main__":
    success = test_cles_windows()
    
    if not success:
        afficher_instructions()
    else:
        print("\n🚀 Prêt à utiliser l'application !") 