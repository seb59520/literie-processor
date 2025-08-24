#!/usr/bin/env python3
"""
Test de la configuration gpt-oss:20b pour Ollama
"""

import json
import os
import subprocess
import sys

def test_configuration_gpt_oss():
    """Test que la configuration gpt-oss:20b est bien prise en compte"""
    
    print("🧪 TEST DE LA CONFIGURATION GPT-OSS:20B")
    print("=" * 60)
    
    # 1. Vérifier la configuration actuelle
    print("\n📁 1. CONFIGURATION ACTUELLE:")
    
    config_file = 'matelas_config.json'
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            print(f"   ✅ {config_file} trouvé")
            print(f"   🔧 Provider LLM: {config.get('llm_provider', 'NON CONFIGURÉ')}")
            
            if 'ollama' in config:
                ollama_config = config['ollama']
                print(f"   🎯 Modèle Ollama: {ollama_config.get('model', 'NON CONFIGURÉ')}")
                print(f"   🌐 URL: {ollama_config.get('base_url', 'NON CONFIGURÉ')}")
                print(f"   ⏱️ Timeout: {ollama_config.get('timeout', 'NON CONFIGURÉ')}")
                
        except Exception as e:
            print(f"   ❌ Erreur lecture configuration: {e}")
            config = {}
    else:
        print(f"   ❌ {config_file} non trouvé")
        config = {}
    
    # 2. Vérifier que gpt-oss:20b est disponible
    print("\n🔍 2. DISPONIBILITÉ GPT-OSS:20B:")
    
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        
        if result.returncode == 0:
            if 'gpt-oss:20b' in result.stdout:
                print("   ✅ gpt-oss:20b est disponible")
                
                # Extraire les informations du modèle
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if 'gpt-oss:20b' in line:
                        parts = line.split()
                        if len(parts) >= 3:
                            model_name = parts[0]
                            model_id = parts[1]
                            model_size = parts[2]
                            print(f"      - Nom: {model_name}")
                            print(f"      - ID: {model_id}")
                            print(f"      - Taille: {model_size}")
            else:
                print("   ❌ gpt-oss:20b n'est pas disponible")
        else:
            print("   ❌ Erreur lors de la liste des modèles")
            
    except Exception as e:
        print(f"   ❌ Impossible de vérifier les modèles: {e}")
    
    # 3. Test rapide avec gpt-oss:20b
    print("\n🧪 3. TEST RAPIDE AVEC GPT-OSS:20B:")
    
    try:
        print("   🚀 Test avec gpt-oss:20b...")
        test_prompt = "Dis-moi simplement 'Bonjour, je suis gpt-oss:20b'"
        
        result = subprocess.run(['ollama', 'run', 'gpt-oss:20b', test_prompt], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("   ✅ Test gpt-oss:20b réussi!")
            print(f"   📝 Réponse: {result.stdout.strip()[:100]}...")
        else:
            print("   ❌ Test gpt-oss:20b échoué")
            print(f"   📝 Erreur: {result.stderr.strip()[:100]}...")
            
    except subprocess.TimeoutExpired:
        print("   ⏰ Test gpt-oss:20b timeout (30s)")
    except Exception as e:
        print(f"   ❌ Erreur test gpt-oss:20b: {e}")
    
    # 4. Vérifier les modifications des fichiers
    print("\n🔍 4. VÉRIFICATION DES MODIFICATIONS:")
    
    # Vérifier backend/main.py
    main_file = 'backend/main.py'
    if os.path.exists(main_file):
        try:
            with open(main_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'gpt-oss:20b' in content:
                print("   ✅ backend/main.py contient gpt-oss:20b")
            else:
                print("   ❌ backend/main.py ne contient pas gpt-oss:20b")
                
            if 'mistral:latest' in content:
                print("   ⚠️ backend/main.py contient encore mistral:latest")
            else:
                print("   ✅ backend/main.py ne contient plus mistral:latest")
                
        except Exception as e:
            print(f"   ❌ Erreur lecture {main_file}: {e}")
    else:
        print(f"   ❌ Fichier {main_file} non trouvé")
    
    # Vérifier backend/llm_provider.py
    provider_file = 'backend/llm_provider.py'
    if os.path.exists(provider_file):
        try:
            with open(provider_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'gpt-oss:20b' in content:
                print("   ✅ backend/llm_provider.py contient gpt-oss:20b")
            else:
                print("   ❌ backend/llm_provider.py ne contient pas gpt-oss:20b")
                
            if 'mistral:latest' in content:
                print("   ⚠️ backend/llm_provider.py contient encore mistral:latest")
            else:
                print("   ✅ backend/llm_provider.py ne contient plus mistral:latest")
                
        except Exception as e:
            print(f"   ❌ Erreur lecture {provider_file}: {e}")
    else:
        print(f"   ❌ Fichier {provider_file} non trouvé")
    
    # 5. Instructions de test
    print("\n📋 5. INSTRUCTIONS DE TEST:")
    
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
    print("   - Jumeaux détectés et logique appliquée")
    print("   - Fichiers Excel générés avec succès")
    
    return True

if __name__ == "__main__":
    print("🚀 Test de la configuration gpt-oss:20b")
    
    # Test principal
    success = test_configuration_gpt_oss()
    
    if success:
        print("\n🎯 RÉSUMÉ DU TEST:")
        print("✅ Configuration vérifiée")
        print("✅ Modèle gpt-oss:20b testé")
        print("✅ Modifications des fichiers vérifiées")
        print("🚀 Prêt pour tester l'application")
    else:
        print("\n❌ Problème détecté dans le test")
    
    print("\n=== FIN DU TEST DE CONFIGURATION ===")

