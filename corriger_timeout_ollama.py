#!/usr/bin/env python3
"""
Script pour corriger le timeout Ollama et optimiser la configuration
"""

import json
import subprocess
import time
import os

def verifier_ollama_status():
    """Vérifie le statut d'Ollama"""
    print("🔍 VÉRIFICATION DU STATUT OLLAMA")
    print("=" * 50)
    
    try:
        # Vérifier si Ollama est en cours d'exécution
        result = subprocess.run(['ollama', 'ps'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Ollama est en cours d'exécution")
            print("📋 Modèles chargés :")
            print(result.stdout)
            return True
        else:
            print("❌ Ollama ne répond pas")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏱️ Timeout lors de la vérification d'Ollama")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def augmenter_timeout():
    """Augmente le timeout dans matelas_config.json"""
    print("\n🔧 AUGMENTATION DU TIMEOUT")
    print("=" * 50)
    
    config_file = 'matelas_config.json'
    
    try:
        # Lire la configuration actuelle
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Augmenter le timeout de 120 à 300 secondes (5 minutes)
        old_timeout = config.get('ollama', {}).get('timeout', 120)
        new_timeout = 300
        
        config['ollama']['timeout'] = new_timeout
        
        # Sauvegarder
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Timeout modifié : {old_timeout}s → {new_timeout}s")
        print("📝 Configuration sauvegardée")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la modification : {e}")
        return False

def tester_modele_simple():
    """Test simple du modèle gpt-oss:20b"""
    print("\n🧪 TEST SIMPLE DU MODÈLE")
    print("=" * 50)
    
    test_prompt = "Réponds juste par 'OK' si tu me comprends."
    
    print(f"📤 Envoi du prompt : '{test_prompt}'")
    start_time = time.time()
    
    try:
        result = subprocess.run([
            'ollama', 'run', 'gpt-oss:20b', test_prompt
        ], capture_output=True, text=True, timeout=180)
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ Test réussi en {duration:.1f}s")
            print(f"📤 Réponse : {result.stdout.strip()}")
            return True, duration
        else:
            print(f"❌ Erreur : {result.stderr}")
            return False, duration
            
    except subprocess.TimeoutExpired:
        end_time = time.time()
        duration = end_time - start_time
        print(f"⏱️ Timeout après {duration:.1f}s")
        return False, duration
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False, 0

def recommander_modele_alternatif():
    """Recommande d'utiliser mistral:latest si gpt-oss:20b est trop lent"""
    print("\n💡 RECOMMANDATIONS")
    print("=" * 50)
    
    print("🎯 Options disponibles :")
    print("1. 🚀 mistral:latest (4.4 GB) - Plus rapide")
    print("2. 🐌 gpt-oss:20b (13 GB) - Plus précis mais lent")
    
    print("\n🔧 Pour changer de modèle :")
    print("1. Ouvrir MatelasApp")
    print("2. Aller dans 'Gestion des clés API'")
    print("3. Changer le modèle Ollama")
    
    return True

def corriger_configuration_complete():
    """Correction complète de la configuration"""
    print("🔧 CORRECTION COMPLÈTE DE LA CONFIGURATION OLLAMA")
    print("=" * 60)
    
    # 1. Vérifier Ollama
    ollama_ok = verifier_ollama_status()
    
    # 2. Augmenter timeout
    timeout_ok = augmenter_timeout()
    
    # 3. Tester le modèle
    if ollama_ok:
        test_ok, duration = tester_modele_simple()
        
        if test_ok and duration < 60:
            print("\n✅ SUCCÈS : gpt-oss:20b fonctionne correctement")
            print("🚀 Vous pouvez continuer à l'utiliser")
        elif test_ok and duration >= 60:
            print("\n⚠️ ATTENTION : gpt-oss:20b fonctionne mais est lent")
            print("💡 Considérez mistral:latest pour plus de rapidité")
            recommander_modele_alternatif()
        else:
            print("\n❌ PROBLÈME : gpt-oss:20b ne fonctionne pas")
            print("🔄 Passage recommandé à mistral:latest")
            recommander_modele_alternatif()
    else:
        print("\n❌ PROBLÈME : Ollama ne répond pas")
        print("🔄 Redémarrez Ollama et réessayez")
    
    # 4. Instructions finales
    print("\n📋 INSTRUCTIONS FINALES :")
    if timeout_ok:
        print("✅ Timeout augmenté à 5 minutes")
    print("🔄 Redémarrez votre application MatelasApp")
    print("🧪 Testez à nouveau avec un fichier PDF")
    
    return True

if __name__ == "__main__":
    corriger_configuration_complete()

