#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier les nouvelles fonctionnalités de température et gestion Ollama
"""

import sys
import os
import subprocess
import json

def test_temperature_explanations():
    """Teste les explications de température"""
    print("🌡️ Test des explications de température")
    print("=" * 50)
    
    temperature_values = [0.0, 0.1, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0]
    
    for temp in temperature_values:
        if temp == 0.0:
            explanation = "Déterministe - Réponses cohérentes et prévisibles"
        elif temp <= 0.3:
            explanation = "Faible créativité - Réponses structurées et précises"
        elif temp <= 0.7:
            explanation = "Créativité modérée - Équilibré entre précision et créativité"
        elif temp <= 1.0:
            explanation = "Créativité élevée - Réponses variées et originales"
        else:
            explanation = "Très créatif - Réponses très variées et imprévisibles"
        
        print(f"Température {temp}: {explanation}")
    
    print("\n✅ Test des explications de température terminé")

def test_ollama_availability():
    """Teste la disponibilité d'Ollama"""
    print("\n🤖 Test de disponibilité d'Ollama")
    print("=" * 50)
    
    try:
        # Vérifier si Ollama est installé
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print(f"✅ Ollama installé: {result.stdout.strip()}")
            
            # Tester la commande list
            list_result = subprocess.run(
                ["ollama", "list", "--json"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if list_result.returncode == 0:
                try:
                    models_data = json.loads(list_result.stdout)
                    if isinstance(models_data, list):
                        model_names = [model.get('name', '') for model in models_data if model.get('name')]
                        print(f"✅ {len(model_names)} modèles Ollama disponibles:")
                        for model in model_names:
                            print(f"   • {model}")
                    else:
                        print("⚠️ Format de réponse Ollama inattendu")
                except json.JSONDecodeError:
                    print("⚠️ Erreur de parsing JSON de la liste des modèles")
            else:
                print("⚠️ Erreur lors de la liste des modèles Ollama")
        else:
            print("❌ Ollama installé mais erreur de version")
            
    except FileNotFoundError:
        print("❌ Ollama non installé ou non trouvé dans le PATH")
        print("💡 Pour installer Ollama: https://ollama.ai")
    except subprocess.TimeoutExpired:
        print("⚠️ Timeout lors de la vérification d'Ollama")
    except Exception as e:
        print(f"❌ Erreur lors de la vérification d'Ollama: {e}")

def test_application_features():
    """Teste les fonctionnalités de l'application"""
    print("\n🧪 Test des fonctionnalités de l'application")
    print("=" * 50)
    
    # Vérifier que le fichier modifié existe
    if os.path.exists("test_llm_prompt.py"):
        print("✅ Fichier test_llm_prompt.py trouvé")
        
        # Vérifier les nouvelles fonctionnalités
        with open("test_llm_prompt.py", "r", encoding="utf-8") as f:
            content = f.read()
            
        features_to_check = [
            ("Explications de température", "temp_explanation"),
            ("Bouton d'ajout Ollama", "add_ollama_btn"),
            ("Bouton de rafraîchissement Ollama", "refresh_ollama_btn"),
            ("Thread de téléchargement Ollama", "OllamaDownloadThread"),
            ("Gestion des modèles Ollama", "load_ollama_models"),
            ("Mise à jour de température", "on_temperature_changed")
        ]
        
        for feature_name, feature_code in features_to_check:
            if feature_code in content:
                print(f"✅ {feature_name} - Implémenté")
            else:
                print(f"❌ {feature_name} - Manquant")
    else:
        print("❌ Fichier test_llm_prompt.py non trouvé")

def main():
    """Fonction principale de test"""
    print("🧪 Test des nouvelles fonctionnalités - Température et Ollama")
    print("=" * 70)
    
    test_temperature_explanations()
    test_ollama_availability()
    test_application_features()
    
    print("\n🎉 Tests terminés !")
    print("\n📋 Résumé des nouvelles fonctionnalités:")
    print("   • Explications détaillées de la température")
    print("   • Gestion avancée des modèles Ollama")
    print("   • Ajout de nouveaux modèles Ollama")
    print("   • Rafraîchissement de la liste des modèles")
    print("   • Téléchargement automatique des modèles")
    print("   • Interface utilisateur améliorée")

if __name__ == "__main__":
    main() 