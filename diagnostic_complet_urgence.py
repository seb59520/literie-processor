#!/usr/bin/env python3
"""
Diagnostic d'urgence - Plus rien ne fonctionne après configuration forcée
"""

import json
import os
import subprocess
import sys

def diagnostic_urgence():
    """Diagnostic complet de la situation d'urgence"""
    
    print("🚨 DIAGNOSTIC D'URGENCE - PLUS RIEN NE FONCTIONNE")
    print("=" * 60)
    
    # 1. Vérifier l'état actuel de la configuration
    print("\n📁 1. ÉTAT ACTUEL DE LA CONFIGURATION:")
    
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
            else:
                print("   ❌ Configuration Ollama manquante")
                
        except Exception as e:
            print(f"   ❌ Erreur lecture configuration: {e}")
            config = {}
    else:
        print(f"   ❌ {config_file} non trouvé")
        config = {}
    
    # 2. Vérifier l'état d'Ollama
    print("\n🔍 2. ÉTAT D'OLLAMA:")
    
    try:
        # Vérifier si Ollama est en cours d'exécution
        result = subprocess.run(['ollama', 'ps'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Ollama est en cours d'exécution")
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
        print(f"   ❌ Impossible de vérifier Ollama: {e}")
    
    # 3. Vérifier les modèles disponibles
    print("\n🔍 3. MODÈLES OLLAMA DISPONIBLES:")
    
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Modèles disponibles:")
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
    
    # 4. Tester la connectivité Ollama
    print("\n🔍 4. TEST DE CONNECTIVITÉ OLLAMA:")
    
    try:
        import requests
        url = config.get('ollama', {}).get('base_url', 'http://localhost:11434')
        test_url = f"{url}/api/tags"
        
        print(f"   🌐 Test de connexion à: {test_url}")
        
        response = requests.get(test_url, timeout=5)
        if response.status_code == 200:
            print("   ✅ Connexion Ollama réussie")
        else:
            print(f"   ❌ Erreur HTTP: {response.status_code}")
            
    except ImportError:
        print("   ⚠️ Module requests non installé, test de connectivité impossible")
    except Exception as e:
        print(f"   ❌ Erreur de connexion: {e}")
    
    # 5. Vérifier les logs récents
    print("\n🔍 5. LOGS RÉCENTS:")
    
    log_file = 'debug_llm.log'
    if os.path.exists(log_file):
        try:
            # Lire les 10 dernières lignes du log
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                last_lines = lines[-10:] if len(lines) > 10 else lines
            
            print(f"   📊 Dernières {len(last_lines)} lignes du log:")
            for line in last_lines:
                line = line.strip()
                if line:
                    # Extraire l'heure et le message
                    if ' - ' in line:
                        parts = line.split(' - ', 2)
                        if len(parts) >= 3:
                            time = parts[0]
                            level = parts[1]
                            message = parts[2]
                            print(f"      [{time}] {level}: {message[:80]}...")
                    else:
                        print(f"      {line[:80]}...")
                        
        except Exception as e:
            print(f"   ❌ Erreur lecture log: {e}")
    else:
        print(f"   ❌ Fichier log {log_file} non trouvé")
    
    # 6. Vérifier l'état de l'application
    print("\n🔍 6. ÉTAT DE L'APPLICATION:")
    
    # Vérifier si des processus Python sont en cours
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        if result.returncode == 0:
            python_processes = [line for line in result.stdout.split('\n') if 'python' in line and 'app_gui' in line]
            if python_processes:
                print("   ✅ Processus Python MatelasApp détecté:")
                for proc in python_processes[:3]:  # Limiter à 3 processus
                    print(f"      - {proc[:80]}...")
            else:
                print("   ℹ️ Aucun processus Python MatelasApp détecté")
    except Exception as e:
        print(f"   ❌ Impossible de vérifier les processus: {e}")
    
    return config

def solutions_urgence():
    """Solutions d'urgence pour rétablir le fonctionnement"""
    
    print("\n🚨 SOLUTIONS D'URGENCE:")
    
    print("   🔄 Solution 1: Redémarrer Ollama")
    print("      - Arrêter: ollama stop")
    print("      - Redémarrer: ollama serve")
    
    print("\n   🔄 Solution 2: Redémarrer l'application")
    print("      - Fermer complètement MatelasApp")
    print("      - Relancer: python3 app_gui.py")
    
    print("\n   🔄 Solution 3: Restaurer la configuration précédente")
    print("      - Vérifier les fichiers de sauvegarde:")
    
    # Lister les sauvegardes
    backup_files = [f for f in os.listdir('.') if f.startswith('matelas_config.json.backup.')]
    if backup_files:
        print("      - Sauvegardes disponibles:")
        for backup in sorted(backup_files, reverse=True)[:3]:  # 3 plus récentes
            print(f"        * {backup}")
    else:
        print("      - Aucune sauvegarde trouvée")
    
    print("\n   🔄 Solution 4: Test rapide Ollama")
    print("      - Tester: ollama run gpt-oss:20b 'Hello'")
    print("      - Vérifier que le modèle répond")

def test_ollama_rapide():
    """Test rapide d'Ollama pour vérifier le fonctionnement"""
    
    print("\n🧪 TEST RAPIDE OLLAMA:")
    
    try:
        print("   🚀 Test avec gpt-oss:20b...")
        result = subprocess.run(['ollama', 'run', 'gpt-oss:20b', 'Hello, test simple'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("   ✅ Test Ollama réussi!")
            print(f"   📝 Réponse: {result.stdout.strip()[:100]}...")
        else:
            print("   ❌ Test Ollama échoué")
            print(f"   📝 Erreur: {result.stderr.strip()[:100]}...")
            
    except subprocess.TimeoutExpired:
        print("   ⏰ Test Ollama timeout (30s)")
    except Exception as e:
        print(f"   ❌ Erreur test Ollama: {e}")

if __name__ == "__main__":
    print("🚨 DIAGNOSTIC D'URGENCE ACTIVÉ")
    
    # Diagnostic principal
    config = diagnostic_urgence()
    
    # Test rapide Ollama
    test_ollama_rapide()
    
    # Solutions d'urgence
    solutions_urgence()
    
    print("\n🎯 RÉSUMÉ DU DIAGNOSTIC:")
    print("✅ Configuration analysée")
    print("🔍 État d'Ollama vérifié")
    print("📊 Logs examinés")
    print("🧪 Test Ollama effectué")
    print("🚨 Solutions d'urgence proposées")
    
    print("\n=== FIN DU DIAGNOSTIC D'URGENCE ===")

