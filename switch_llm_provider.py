#!/usr/bin/env python3
"""
Script pour switcher rapidement entre les providers LLM
Usage: python3 switch_llm_provider.py [ollama|openrouter]
"""

import json
import sys
import os

def read_config():
    """Lit la configuration actuelle"""
    config_file = 'matelas_config.json'
    if not os.path.exists(config_file):
        print(f"❌ Fichier {config_file} non trouvé")
        return None
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Erreur lecture config: {e}")
        return None

def write_config(config):
    """Sauvegarde la configuration"""
    config_file = 'matelas_config.json'
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Erreur sauvegarde config: {e}")
        return False

def show_current_status():
    """Affiche le statut actuel"""
    config = read_config()
    if not config:
        return
    
    current_provider = config.get('llm_provider', 'NON CONFIGURÉ')
    current_llm = config.get('current_llm_provider', 'NON CONFIGURÉ')
    
    print("📋 STATUT ACTUEL:")
    print(f"   🔧 Provider LLM: {current_provider}")
    print(f"   🔧 Provider actuel: {current_llm}")
    
    if current_provider == 'ollama':
        ollama_config = config.get('ollama', {})
        print(f"   🎯 Modèle: {ollama_config.get('model', 'NON CONFIGURÉ')}")
        print(f"   ⏱️ Timeout: {ollama_config.get('timeout', 'NON CONFIGURÉ')}s")
    elif current_provider == 'openrouter':
        openrouter_key = config.get('llm_api_key_openrouter', '')
        key_status = "✅ Configurée" if openrouter_key else "❌ Manquante"
        print(f"   🔑 Clé API: {key_status}")

def switch_to_ollama(config):
    """Switch vers Ollama"""
    print("🔄 Passage à Ollama...")
    
    config['llm_provider'] = 'ollama'
    config['current_llm_provider'] = 'ollama'
    
    # S'assurer que la config Ollama existe
    if 'ollama' not in config:
        config['ollama'] = {
            'model': 'gpt-oss:20b',
            'base_url': 'http://localhost:11434',
            'timeout': 300
        }
    
    print("✅ Configuré pour Ollama")
    print(f"   🎯 Modèle: {config['ollama']['model']}")
    print(f"   ⏱️ Timeout: {config['ollama']['timeout']}s")

def switch_to_openrouter(config):
    """Switch vers OpenRouter"""
    print("🔄 Passage à OpenRouter...")
    
    config['llm_provider'] = 'openrouter'
    config['current_llm_provider'] = 'openrouter'
    
    # Vérifier la clé API
    api_key = config.get('llm_api_key_openrouter', '')
    if not api_key:
        print("⚠️ ATTENTION: Aucune clé API OpenRouter configurée")
        print("   📝 Configurez-la dans MatelasApp > Gestion des clés API")
    else:
        print("✅ Clé API OpenRouter présente")
    
    print("✅ Configuré pour OpenRouter")

def main():
    """Fonction principale"""
    print("🔄 SWITCH LLM PROVIDER")
    print("=" * 30)
    
    # Afficher le statut actuel
    show_current_status()
    print()
    
    # Vérifier les arguments
    if len(sys.argv) < 2:
        print("💡 USAGE:")
        print(f"   python3 {sys.argv[0]} ollama")
        print(f"   python3 {sys.argv[0]} openrouter")
        print()
        return
    
    target_provider = sys.argv[1].lower()
    
    if target_provider not in ['ollama', 'openrouter']:
        print("❌ Provider invalide. Utilisez: ollama ou openrouter")
        return
    
    # Lire la config
    config = read_config()
    if not config:
        return
    
    # Switch
    if target_provider == 'ollama':
        switch_to_ollama(config)
    elif target_provider == 'openrouter':
        switch_to_openrouter(config)
    
    # Sauvegarder
    if write_config(config):
        print("\n💾 Configuration sauvegardée!")
        print()
        print("🚀 PROCHAINES ÉTAPES:")
        print("   1. Redémarrer MatelasApp si elle est ouverte")
        print("   2. Vérifier dans 'Gestion des clés API'")
        print("   3. Tester avec un fichier PDF")
    else:
        print("\n❌ Erreur lors de la sauvegarde")

if __name__ == "__main__":
    main()

