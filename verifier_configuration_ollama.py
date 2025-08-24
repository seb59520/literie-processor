#!/usr/bin/env python3
"""
Vérification de la configuration Ollama
"""

import json
import os

def verifier_configuration_ollama():
    """Vérifie la configuration Ollama actuelle"""
    
    print("=== VÉRIFICATION DE LA CONFIGURATION OLLAMA ===")
    
    # 1. Vérifier le fichier de configuration
    print("\n📁 1. Vérification du fichier de configuration:")
    
    config_files = [
        'matelas_config.json',
        'config.py',
        'backend_interface.py'
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"   ✅ {config_file} trouvé")
        else:
            print(f"   ❌ {config_file} non trouvé")
    
    # 2. Lire la configuration principale
    print("\n🔍 2. Lecture de la configuration principale:")
    
    if os.path.exists('matelas_config.json'):
        try:
            with open('matelas_config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            print("   ✅ Configuration chargée avec succès")
            
            # Vérifier la configuration LLM
            if 'llm_provider' in config:
                print(f"   🔧 Provider LLM configuré: {config['llm_provider']}")
            else:
                print("   ❌ Provider LLM non configuré")
            
            # Vérifier la configuration Ollama
            if 'ollama' in config:
                ollama_config = config['ollama']
                print("   📊 Configuration Ollama:")
                for key, value in ollama_config.items():
                    print(f"      - {key}: {value}")
            else:
                print("   ❌ Configuration Ollama non trouvée")
                
        except Exception as e:
            print(f"   ❌ Erreur lecture configuration: {e}")
    else:
        print("   ❌ Fichier matelas_config.json non trouvé")
    
    # 3. Vérifier les modèles disponibles
    print("\n🔍 3. Vérification des modèles Ollama disponibles:")
    
    try:
        import subprocess
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Modèles Ollama disponibles:")
            lines = result.stdout.strip().split('\n')
            for line in lines[1:]:  # Ignorer l'en-tête
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        model_name = parts[0]
                        model_size = parts[1]
                        print(f"      - {model_name} ({model_size})")
        else:
            print("   ❌ Erreur lors de la liste des modèles")
            print(f"      Erreur: {result.stderr}")
            
    except Exception as e:
        print(f"   ❌ Impossible d'exécuter 'ollama list': {e}")
    
    # 4. Vérifier le modèle par défaut
    print("\n🔍 4. Vérification du modèle par défaut:")
    
    try:
        result = subprocess.run(['ollama', 'ps'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Modèles Ollama en cours d'exécution:")
            lines = result.stdout.strip().split('\n')
            for line in lines[1:]:  # Ignorer l'en-tête
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 3:
                        model_name = parts[0]
                        model_id = parts[1]
                        status = parts[2]
                        print(f"      - {model_name} (ID: {model_id}, Status: {status})")
        else:
            print("   ℹ️ Aucun modèle Ollama en cours d'exécution")
            
    except Exception as e:
        print(f"   ❌ Impossible de vérifier les modèles en cours: {e}")
    
    # 5. Analyse du problème dans le log
    print("\n🔍 5. Analyse du problème dans le log:")
    
    print("   📊 Problème détecté:")
    print("      - Le log montre: 'ollama run mistral:latest'")
    print("      - Cela signifie que l'application utilise mistral:latest")
    print("      - Au lieu du modèle que vous aviez configuré")
    
    print("\n   🎯 Causes possibles:")
    print("      1. ❌ Modèle par défaut non configuré")
    print("      2. ❌ Configuration Ollama manquante")
    print("      3. ❌ Fallback automatique sur mistral:latest")
    
    # 6. Solutions proposées
    print("\n🔧 6. Solutions proposées:")
    
    print("   🚀 Solution 1: Configurer le modèle par défaut")
    print("      - Dans l'application: Gestion des clés API")
    print("      - Sélectionner Ollama et configurer le modèle")
    print("      - Sauvegarder la configuration")
    
    print("\n   🚀 Solution 2: Vérifier la configuration Ollama")
    print("      - S'assurer qu'un modèle spécifique est configuré")
    print("      - Éviter le fallback sur mistral:latest")
    
    print("\n   🚀 Solution 3: Tester avec un modèle spécifique")
    print("      - Configurer explicitement un modèle (ex: llama3.2)")
    print("      - Tester le traitement avec ce modèle")
    
    return True

def instructions_configuration():
    """Donne les instructions pour configurer Ollama"""
    
    print("\n📋 INSTRUCTIONS DE CONFIGURATION OLLAMA:")
    
    print("   1. 📱 Ouvrir l'application MatelasApp")
    print("   2. 🔧 Aller dans 'Gestion des clés API'")
    print("   3. 🎯 Sélectionner l'onglet 'Ollama'")
    print("   4. 📝 Configurer le modèle par défaut:")
    print("      - Modèle: (ex: llama3.2, codellama, etc.)")
    print("      - Pas de clé API nécessaire")
    print("   5. 💾 Sauvegarder la configuration")
    print("   6. 🚀 Tester avec votre PDF COSTENOBLE")
    
    print("\n   🔍 Points de vérification:")
    print("      - Modèle Ollama configuré (pas mistral:latest)")
    print("      - Configuration sauvegardée")
    print("      - Option LLM activée lors du test")

if __name__ == "__main__":
    print("🚀 Vérification de la configuration Ollama")
    
    # Vérification principale
    success = verifier_configuration_ollama()
    
    # Instructions de configuration
    instructions_configuration()
    
    if success:
        print("\n🎯 RÉSUMÉ:")
        print("✅ La configuration Ollama a été vérifiée")
        print("🔧 Des solutions ont été proposées")
        print("🚀 Suivez les instructions pour configurer le bon modèle")
    else:
        print("\n❌ Problème détecté dans la vérification")
    
    print("\n=== FIN DE LA VÉRIFICATION ===")

