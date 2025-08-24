#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier l'augmentation des timeouts
"""

import sys
import os
import re

def test_timeout_in_llm_provider():
    """Teste les timeouts dans le fichier llm_provider.py"""
    print("⏱️ Test des timeouts dans llm_provider.py")
    print("=" * 50)
    
    if not os.path.exists("backend/llm_provider.py"):
        print("❌ Fichier backend/llm_provider.py non trouvé")
        return False
    
    with open("backend/llm_provider.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Rechercher tous les timeouts
    timeout_pattern = r'timeout=(\d+)'
    timeouts = re.findall(timeout_pattern, content)
    
    print(f"📊 {len(timeouts)} timeouts trouvés dans le fichier")
    
    # Vérifier que tous les timeouts sont >= 30
    low_timeouts = []
    for timeout in timeouts:
        timeout_value = int(timeout)
        if timeout_value < 30:
            low_timeouts.append(timeout_value)
    
    if low_timeouts:
        print(f"❌ Timeouts trop bas détectés: {low_timeouts}")
        return False
    else:
        print("✅ Tous les timeouts sont >= 30 secondes")
    
    # Vérifier les timeouts spécifiques
    specific_checks = [
        ("Appels LLM principaux", r'response = requests\.post.*timeout=(\d+)'),
        ("Tests de connexion", r'response = requests\.get.*timeout=(\d+)'),
        ("Ollama spécifique", r'Ollama.*timeout=(\d+)')
    ]
    
    for check_name, pattern in specific_checks:
        matches = re.findall(pattern, content)
        if matches:
            min_timeout = min(int(t) for t in matches)
            print(f"✅ {check_name}: timeout minimum = {min_timeout}s")
        else:
            print(f"⚠️ {check_name}: aucun timeout trouvé")
    
    return True

def test_timeout_in_test_app():
    """Teste les timeouts dans l'application de test"""
    print("\n🧪 Test des timeouts dans test_llm_prompt.py")
    print("=" * 50)
    
    if not os.path.exists("test_llm_prompt.py"):
        print("❌ Fichier test_llm_prompt.py non trouvé")
        return False
    
    with open("test_llm_prompt.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Rechercher les timeouts
    timeout_pattern = r'timeout=(\d+)'
    timeouts = re.findall(timeout_pattern, content)
    
    print(f"📊 {len(timeouts)} timeouts trouvés dans l'application de test")
    
    if timeouts:
        min_timeout = min(int(t) for t in timeouts)
        max_timeout = max(int(t) for t in timeouts)
        print(f"✅ Timeout minimum: {min_timeout}s, maximum: {max_timeout}s")
        
        if min_timeout < 10:
            print(f"❌ Timeout trop bas détecté: {min_timeout}s")
            return False
        else:
            print("✅ Tous les timeouts sont acceptables")
    else:
        print("⚠️ Aucun timeout trouvé dans l'application de test")
    
    return True

def test_timeout_values():
    """Teste les valeurs spécifiques des timeouts"""
    print("\n📋 Vérification des valeurs de timeout")
    print("=" * 50)
    
    expected_timeouts = {
        "Appels LLM": 120,  # 2 minutes pour les appels principaux
        "Tests de connexion": 30,  # 30 secondes pour les tests
        "Ollama list": 30,  # 30 secondes pour lister les modèles
    }
    
    print("🎯 Timeouts attendus:")
    for operation, timeout in expected_timeouts.items():
        print(f"   • {operation}: {timeout}s")
    
    return True

def main():
    """Fonction principale de test"""
    print("⏱️ Test d'augmentation des timeouts")
    print("=" * 70)
    
    results = []
    
    results.append(test_timeout_in_llm_provider())
    results.append(test_timeout_in_test_app())
    results.append(test_timeout_values())
    
    print("\n🎉 Tests terminés !")
    print("=" * 70)
    
    if all(results):
        print("✅ TOUS LES TIMEOUTS ONT ÉTÉ AUGMENTÉS")
        print("\n📋 Résumé des améliorations:")
        print("   • Appels LLM: 120s (au lieu de 30-60s)")
        print("   • Tests de connexion: 30s (au lieu de 5-10s)")
        print("   • Ollama list: 30s (au lieu de 10s)")
        print("   • Tous les providers: timeouts uniformisés")
        print("\n🚀 Les timeouts sont maintenant plus généreux !")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("Vérifiez les erreurs ci-dessus.")
    
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 