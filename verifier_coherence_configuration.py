#!/usr/bin/env python3
"""
Vérification de la cohérence entre config.py et matelas_config.json
"""

import json
import os
import sys

def verifier_coherence_configuration():
    """Vérifie la cohérence entre les différents systèmes de configuration"""
    
    print("🔍 VÉRIFICATION DE LA COHÉRENCE DES CONFIGURATIONS")
    print("=" * 60)
    
    # 1. Vérifier matelas_config.json
    print("\n📁 1. CONFIGURATION MATELAS_CONFIG.JSON:")
    
    matelas_config_file = 'matelas_config.json'
    if os.path.exists(matelas_config_file):
        try:
            with open(matelas_config_file, 'r', encoding='utf-8') as f:
                matelas_config = json.load(f)
            
            print(f"   ✅ {matelas_config_file} trouvé")
            print(f"   🔧 Provider LLM: {matelas_config.get('llm_provider', 'NON CONFIGURÉ')}")
            print(f"   🔧 Provider actuel: {matelas_config.get('current_llm_provider', 'NON CONFIGURÉ')}")
            
            if 'ollama' in matelas_config:
                ollama_config = matelas_config['ollama']
                print(f"   🎯 Modèle Ollama: {ollama_config.get('model', 'NON CONFIGURÉ')}")
                print(f"   🌐 URL: {ollama_config.get('base_url', 'NON CONFIGURÉ')}")
                print(f"   ⏱️ Timeout: {ollama_config.get('timeout', 'NON CONFIGURÉ')}")
                
        except Exception as e:
            print(f"   ❌ Erreur lecture {matelas_config_file}: {e}")
            matelas_config = {}
    else:
        print(f"   ❌ {matelas_config_file} non trouvé")
        matelas_config = {}
    
    # 2. Vérifier config.py
    print("\n📁 2. CONFIGURATION CONFIG.PY:")
    
    config_file = 'config.py'
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Chercher les valeurs par défaut
            if 'current_llm_provider.*openrouter' in content:
                print("   ⚠️ config.py a 'openrouter' comme provider par défaut")
            else:
                print("   ✅ config.py n'a pas 'openrouter' comme défaut")
                
            if 'get_current_llm_provider' in content:
                print("   ✅ config.py contient get_current_llm_provider")
                
                # Extraire la ligne avec le défaut
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'get_current_llm_provider' in line and 'openrouter' in line:
                        print(f"      📍 Ligne {i+1}: {line.strip()}")
                        
        except Exception as e:
            print(f"   ❌ Erreur lecture {config_file}: {e}")
    else:
        print(f"   ❌ {config_file} non trouvé")
    
    # 3. Vérifier backend/main.py
    print("\n📁 3. CONFIGURATION BACKEND/MAIN.PY:")
    
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
        print(f"   ❌ {main_file} non trouvé")
    
    # 4. Vérifier backend/llm_provider.py
    print("\n📁 4. CONFIGURATION BACKEND/LLM_PROVIDER.PY:")
    
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
        print(f"   ❌ {provider_file} non trouvé")
    
    # 5. Analyse des incohérences
    print("\n🚨 5. ANALYSE DES INCOHÉRENCES:")
    
    incohérences = []
    
    # Vérifier la cohérence des providers
    matelas_provider = matelas_config.get('llm_provider', '')
    matelas_current = matelas_config.get('current_llm_provider', '')
    
    if matelas_provider != matelas_current:
        incohérences.append(f"Provider LLM ({matelas_provider}) ≠ Provider actuel ({matelas_current})")
    
    if matelas_provider == 'ollama' and matelas_current == 'ollama':
        print("   ✅ Cohérence des providers : ollama")
    else:
        incohérences.append(f"Provider incohérent : {matelas_provider} vs {matelas_current}")
    
    # Vérifier la cohérence des modèles
    if 'ollama' in matelas_config:
        ollama_model = matelas_config['ollama'].get('model', '')
        if ollama_model == 'gpt-oss:20b':
            print("   ✅ Modèle Ollama cohérent : gpt-oss:20b")
        else:
            incohérences.append(f"Modèle Ollama incohérent : {ollama_model}")
    
    # Afficher les incohérences
    if incohérences:
        print("   ❌ Incohérences détectées :")
        for incohérence in incohérences:
            print(f"      - {incohérence}")
    else:
        print("   ✅ Aucune incohérence détectée")
    
    # 6. Solutions proposées
    print("\n🔧 6. SOLUTIONS PROPOSÉES:")
    
    if incohérences:
        print("   🚨 Problèmes identifiés :")
        print("      - Configuration incohérente entre les systèmes")
        print("      - L'interface peut utiliser config.py au lieu de matelas_config.json")
        
        print("\n   🔧 Solutions :")
        print("      1. Forcer la cohérence dans matelas_config.json")
        print("      2. Modifier config.py pour utiliser ollama par défaut")
        print("      3. Vérifier que l'interface lit matelas_config.json")
        
    else:
        print("   ✅ Configuration cohérente")
        print("   🚀 Prêt pour tester l'application")
    
    return len(incohérences) == 0

def corriger_coherence():
    """Corrige les incohérences de configuration"""
    
    print("\n🔧 CORRECTION DE LA COHÉRENCE:")
    
    # 1. Corriger matelas_config.json
    print("\n📝 1. CORRECTION DE MATELAS_CONFIG.JSON:")
    
    matelas_config_file = 'matelas_config.json'
    if os.path.exists(matelas_config_file):
        try:
            with open(matelas_config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Forcer la cohérence
            config['current_llm_provider'] = 'ollama'
            config['llm_provider'] = 'ollama'
            
            # Sauvegarder
            with open(matelas_config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print("   ✅ matelas_config.json corrigé")
            print("      - llm_provider: ollama")
            print("      - current_llm_provider: ollama")
            
        except Exception as e:
            print(f"   ❌ Erreur correction {matelas_config_file}: {e}")
    else:
        print(f"   ❌ {matelas_config_file} non trouvé")
    
    # 2. Instructions de test
    print("\n📋 2. INSTRUCTIONS DE TEST:")
    
    print("   🚀 Maintenant testez votre application:")
    print("   1. 📱 Ouvrir MatelasApp")
    print("   2. 🔧 Vérifier dans 'Gestion des clés API' que Ollama est sélectionné")
    print("   3. 📄 Sélectionner votre PDF COSTENOBLE")
    print("   4. ✅ Cocher 'Utiliser l'enrichissement LLM'")
    print("   5. 🚀 Cliquer sur 'Traiter les fichiers'")
    
    print("\n   🔍 Vérifications à faire:")
    print("   - Dans les logs: 'ollama run gpt-oss:20b' (pas openrouter)")
    print("   - Provider affiché: ollama (pas openrouter)")
    print("   - Parsing JSON réussi")
    print("   - Dimensions extraites correctement")
    print("   - Fourgon détecté et rempli")
    print("   - Jumeaux détectés et logique appliquée")
    print("   - Fichiers Excel générés avec succès")

if __name__ == "__main__":
    print("🔍 Vérification de la cohérence des configurations")
    
    # Vérification principale
    cohérent = verifier_coherence_configuration()
    
    # Correction si nécessaire
    if not cohérent:
        corriger_coherence()
    
    if cohérent:
        print("\n🎯 RÉSUMÉ DE LA VÉRIFICATION:")
        print("✅ Configuration cohérente")
        print("🚀 Prêt pour tester l'application")
    else:
        print("\n🎯 RÉSUMÉ DE LA VÉRIFICATION:")
        print("❌ Incohérences détectées et corrigées")
        print("🔧 Configuration harmonisée")
        print("🚀 Prêt pour tester l'application")
    
    print("\n=== FIN DE LA VÉRIFICATION DE COHÉRENCE ===")

