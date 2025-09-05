#!/usr/bin/env python3
"""
Script pour forcer la configuration Ollama avec gpt-oss:20b
et éviter le fallback automatique sur mistral:latest
"""

import json
import os
import shutil

def forcer_configuration_gpt_oss():
    """Force la configuration Ollama avec gpt-oss:20b"""
    
    print("🚀 FORÇAGE DE LA CONFIGURATION OLLAMA AVEC GPT-OSS:20B")
    print("=" * 60)
    
    # 1. Vérifier le fichier de configuration actuel
    print("\n📁 1. Vérification de la configuration actuelle:")
    
    config_file = 'matelas_config.json'
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"   ✅ {config_file} trouvé et lu")
        except Exception as e:
            print(f"   ❌ Erreur lecture {config_file}: {e}")
            config = {}
    else:
        print(f"   ❌ {config_file} non trouvé, création d'une nouvelle configuration")
        config = {}
    
    # 2. Sauvegarder l'ancienne configuration
    print("\n💾 2. Sauvegarde de l'ancienne configuration:")
    
    backup_file = f"{config_file}.backup.{int(os.path.getmtime(config_file) if os.path.exists(config_file) else 0)}"
    if os.path.exists(config_file):
        shutil.copy2(config_file, backup_file)
        print(f"   ✅ Sauvegarde créée: {backup_file}")
    else:
        print("   ℹ️ Pas de sauvegarde nécessaire (nouveau fichier)")
    
    # 3. Forcer la configuration Ollama
    print("\n🔧 3. Application de la configuration forcée:")
    
    # Configuration forcée
    config_forcee = {
        "llm_provider": "ollama",
        "ollama": {
            "model": "gpt-oss:20b",
            "base_url": "http://localhost:11434",
            "timeout": 120
        },
        "openai": config.get("openai", {}),
        "anthropic": config.get("anthropic", {}),
        "gemini": config.get("gemini", {}),
        "mistral": config.get("mistral", {}),
        "openrouter": config.get("openrouter", {})
    }
    
    print("   📝 Configuration appliquée:")
    print(f"      - Provider LLM: {config_forcee['llm_provider']}")
    print(f"      - Modèle Ollama: {config_forcee['ollama']['model']}")
    print(f"      - URL: {config_forcee['ollama']['base_url']}")
    print(f"      - Timeout: {config_forcee['ollama']['timeout']}s")
    
    # 4. Sauvegarder la nouvelle configuration
    print("\n💾 4. Sauvegarde de la nouvelle configuration:")
    
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_forcee, f, indent=2, ensure_ascii=False)
        print(f"   ✅ Configuration sauvegardée dans {config_file}")
    except Exception as e:
        print(f"   ❌ Erreur sauvegarde: {e}")
        return False
    
    # 5. Vérifier que la configuration est bien appliquée
    print("\n🔍 5. Vérification de la configuration appliquée:")
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config_verif = json.load(f)
        
        if (config_verif.get('llm_provider') == 'ollama' and 
            config_verif.get('ollama', {}).get('model') == 'gpt-oss:20b'):
            print("   ✅ Configuration vérifiée avec succès!")
            print("   🎯 Ollama est configuré pour utiliser gpt-oss:20b")
        else:
            print("   ❌ Configuration incorrecte après sauvegarde")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur vérification: {e}")
        return False
    
    # 6. Instructions de test
    print("\n📋 6. INSTRUCTIONS DE TEST:")
    
    print("   🚀 Maintenant testez votre application:")
    print("   1. 📱 Ouvrir MatelasApp")
    print("   2. 🔧 Vérifier dans 'Gestion des clés API' que Ollama est sélectionné")
    print("   3. 📄 Sélectionner votre PDF COSTENOBLE")
    print("   4. ✅ Cocher 'Utiliser l'enrichissement LLM'")
    print("   5. 🚀 Cliquer sur 'Traiter les fichiers'")
    
    print("\n   🔍 Vérifications à faire:")
    print("   - Dans les logs: 'ollama run gpt-oss:20b' (pas mistral:latest)")
    print("   - Parsing JSON réussi")
    print("   - Dimensions extraites correctement")
    print("   - Fourgon détecté et rempli")
    print("   - Fichiers Excel générés avec succès")
    
    # 7. Test rapide de la configuration
    print("\n🧪 7. Test rapide de la configuration:")
    
    try:
        import subprocess
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        
        if result.returncode == 0:
            if 'gpt-oss:20b' in result.stdout:
                print("   ✅ gpt-oss:20b est disponible sur votre système")
            else:
                print("   ⚠️ gpt-oss:20b n'est pas dans la liste des modèles")
                print("   💡 Vérifiez que le modèle est bien installé")
        else:
            print("   ❌ Impossible de vérifier les modèles Ollama")
            
    except Exception as e:
        print(f"   ❌ Erreur lors de la vérification des modèles: {e}")
    
    return True

def instructions_depannage():
    """Instructions de dépannage si le problème persiste"""
    
    print("\n🔧 INSTRUCTIONS DE DÉPANNAGE:")
    
    print("   Si le problème persiste avec mistral:latest:")
    print("   1. 🔍 Vérifier que gpt-oss:20b est bien installé:")
    print("      ollama list | grep gpt-oss")
    print("   2. 🚀 Démarrer le modèle gpt-oss:20b:")
    print("      ollama run gpt-oss:20b")
    print("   3. 🔄 Redémarrer l'application MatelasApp")
    print("   4. 📝 Vérifier que la configuration est bien sauvegardée")
    
    print("\n   📊 Vérification des logs:")
    print("   - Chercher 'ollama run gpt-oss:20b' dans debug_llm.log")
    print("   - Éviter 'ollama run mistral:latest'")
    print("   - S'assurer que le parsing JSON réussit")

if __name__ == "__main__":
    print("🎯 FORÇAGE DE LA CONFIGURATION OLLAMA")
    print("Ce script va forcer l'utilisation de gpt-oss:20b")
    
    # Application de la configuration forcée
    success = forcer_configuration_gpt_oss()
    
    # Instructions de dépannage
    instructions_depannage()
    
    if success:
        print("\n🎉 RÉSUMÉ:")
        print("✅ Configuration Ollama forcée avec gpt-oss:20b")
        print("✅ Sauvegarde de l'ancienne configuration créée")
        print("🚀 Prêt pour tester avec votre PDF COSTENOBLE")
        print("🔍 Vérifiez que gpt-oss:20b est utilisé au lieu de mistral:latest")
    else:
        print("\n❌ Problème lors de la configuration forcée")
        print("🔧 Vérifiez les erreurs et réessayez")
    
    print("\n=== FIN DU FORÇAGE DE CONFIGURATION ===")

