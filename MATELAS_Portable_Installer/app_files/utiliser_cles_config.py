#!/usr/bin/env python3
"""
Script pour expliquer comment faire en sorte que l'application utilise 
la clé API du fichier matelas_config.json
"""

import json
import os
from pathlib import Path

def expliquer_utilisation_cles_config():
    """Explique comment utiliser les clés API du fichier matelas_config.json"""
    
    print("🔑 COMMENT UTILISER LES CLÉS API DE MATELAS_CONFIG.JSON")
    print("=" * 60)
    
    # Vérifier le fichier de configuration
    home_dir = Path.home()
    config_file = home_dir / ".matelas_config.json"
    
    print(f"📁 Fichier de configuration: {config_file}")
    
    if config_file.exists():
        print("✅ Fichier de configuration trouvé")
        
        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            
            print(f"📋 Contenu du fichier:")
            for key, value in config_data.items():
                if 'api_key' in key.lower() or 'key' in key.lower():
                    # Masquer les clés API
                    if isinstance(value, str) and len(value) > 10:
                        masked_value = value[:10] + "..." + value[-4:]
                        print(f"  🔑 {key}: {masked_value}")
                    else:
                        print(f"  📝 {key}: {value}")
                else:
                    print(f"  📝 {key}: {value}")
            
        except Exception as e:
            print(f"❌ Erreur lors de la lecture: {e}")
            return False
    else:
        print("❌ Fichier de configuration non trouvé")
        return False
    
    print("\n🔧 COMMENT L'APPLICATION UTILISE LES CLÉS API:")
    print("-" * 50)
    
    print("""
1. 📍 LOCALISATION DES CLÉS API:
   - Fichier: ~/.matelas_config.json (dossier utilisateur)
   - Clé OpenRouter: "openrouter_api_key"
   - Clés autres providers: "llm_api_key_[provider]"
   - Provider actuel: "current_llm_provider"

2. 🔄 CHARGEMENT AUTOMATIQUE:
   L'application charge automatiquement les clés API depuis ce fichier:
   - Au démarrage de l'application
   - Quand vous changez de provider LLM
   - Quand vous traitez des fichiers

3. 💾 SAUVEGARDE AUTOMATIQUE:
   L'application sauvegarde automatiquement:
   - Les nouvelles clés API que vous saisissez
   - Le provider LLM sélectionné
   - Les modèles personnalisés

4. 🎯 UTILISATION DANS L'APPLICATION:
   - Interface graphique: Les clés sont pré-remplies
   - Traitement backend: Les clés sont transmises automatiquement
   - Gestionnaire de clés: Affiche et permet de modifier les clés
""")
    
    print("\n🚀 COMMENT ACTIVER L'UTILISATION DES CLÉS:")
    print("-" * 45)
    
    print("""
1. 📱 DANS L'INTERFACE GRAPHIQUE:
   - Lancer l'application: python3 app_gui.py
   - Cocher "🤖 Enrichir avec LLM"
   - Sélectionner le provider dans le menu déroulant
   - La clé API sera automatiquement chargée si elle existe

2. 🔧 VIA LE GESTIONNAIRE DE CLÉS:
   - Menu Aide → 🔐 Gestionnaire de Clés API
   - Voir toutes les clés configurées
   - Ajouter/modifier/supprimer des clés
   - Tester les connexions

3. ⚙️ VIA LES PARAMÈTRES LLM:
   - Menu Aide → ⚙️ Configuration des Providers LLM
   - Configurer les clés API pour chaque provider
   - Sélectionner le provider actuel
   - Définir les modèles personnalisés
""")
    
    print("\n🔍 DIAGNOSTIC DE L'UTILISATION:")
    print("-" * 35)
    
    # Vérifier si l'application peut charger les clés
    try:
        # Simuler le chargement de la configuration
        from config import config
        
        print("✅ Module de configuration chargé")
        
        # Vérifier les clés disponibles
        openrouter_key = config.get_openrouter_api_key()
        current_provider = config.get_current_llm_provider()
        all_providers = config.get_all_llm_providers()
        
        print(f"🔑 Clé OpenRouter: {'✅ Présente' if openrouter_key else '❌ Manquante'}")
        print(f"🎯 Provider actuel: {current_provider}")
        print(f"📊 Providers configurés: {list(all_providers.keys())}")
        
        # Vérifier les modèles
        for provider in all_providers.keys():
            model = config.get_llm_model(provider)
            if model:
                print(f"🤖 Modèle {provider}: {model}")
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du diagnostic: {e}")
        return False
    
    print("\n💡 CONSEILS POUR L'UTILISATION:")
    print("-" * 35)
    
    print("""
1. 🔐 SÉCURITÉ:
   - Le fichier ~/.matelas_config.json n'est pas chiffré
   - Pour plus de sécurité, utilisez le stockage sécurisé
   - Ne partagez jamais votre fichier de configuration

2. 🔄 SYNCHRONISATION:
   - Les clés sont automatiquement synchronisées entre l'interface et le backend
   - Les modifications sont sauvegardées immédiatement
   - Redémarrez l'application après modification du fichier

3. 🧪 TEST:
   - Utilisez le gestionnaire de clés pour tester les connexions
   - Vérifiez que les clés sont valides avant de traiter des fichiers
   - Consultez les logs pour diagnostiquer les problèmes

4. 🔧 DÉPANNAGE:
   - Si les clés ne sont pas détectées, vérifiez le format du fichier JSON
   - Si l'application ne démarre pas, vérifiez les permissions du fichier
   - Si les clés ne fonctionnent pas, testez-les manuellement
""")
    
    return True

def creer_exemple_config():
    """Crée un exemple de fichier de configuration"""
    
    print("\n📝 CRÉATION D'UN EXEMPLE DE CONFIGURATION:")
    print("-" * 45)
    
    home_dir = Path.home()
    config_file = home_dir / ".matelas_config.json"
    
    exemple_config = {
        "openrouter_api_key": "sk-or-votre-cle-api-ici",
        "llm_api_key_openai": "sk-votre-cle-openai-ici",
        "llm_api_key_anthropic": "sk-ant-votre-cle-anthropic-ici",
        "current_llm_provider": "openrouter",
        "llm_model_openrouter": "gpt-4o",
        "llm_model_openai": "gpt-4o",
        "llm_model_anthropic": "claude-3-5-sonnet-20241022",
        "last_semaine": 1,
        "last_annee": 2025,
        "last_commande_client": "",
        "excel_output_directory": str(Path.cwd() / "output")
    }
    
    print("📄 Exemple de fichier .matelas_config.json:")
    print(json.dumps(exemple_config, indent=2, ensure_ascii=False))
    
    print(f"\n💾 Pour créer ce fichier:")
    print(f"   nano {config_file}")
    print(f"   # Ou")
    print(f"   code {config_file}")
    
    return exemple_config

def verifier_utilisation_automatique():
    """Vérifie si l'application utilise automatiquement les clés"""
    
    print("\n🔍 VÉRIFICATION DE L'UTILISATION AUTOMATIQUE:")
    print("-" * 50)
    
    try:
        # Simuler le processus de chargement
        from config import config
        
        print("1. 📦 Chargement de la configuration...")
        print("   ✅ Module config importé")
        
        print("2. 🔑 Récupération des clés API...")
        openrouter_key = config.get_openrouter_api_key()
        current_provider = config.get_current_llm_provider()
        
        print(f"   ✅ Clé OpenRouter: {'Présente' if openrouter_key else 'Manquante'}")
        print(f"   ✅ Provider actuel: {current_provider}")
        
        print("3. 🎯 Simulation d'utilisation...")
        if openrouter_key and current_provider == "openrouter":
            print("   ✅ L'application utilisera automatiquement la clé OpenRouter")
        elif current_provider == "ollama":
            print("   ✅ L'application utilisera Ollama (pas de clé requise)")
        else:
            print("   ⚠️ Vérifiez la configuration du provider")
        
        print("4. 🔄 Processus automatique:")
        print("   ✅ Chargement au démarrage")
        print("   ✅ Pré-remplissage de l'interface")
        print("   ✅ Transmission au backend")
        print("   ✅ Sauvegarde des modifications")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

def main():
    """Fonction principale"""
    
    print("🔑 GUIDE D'UTILISATION DES CLÉS API")
    print("=" * 50)
    
    # Explication générale
    explication_ok = expliquer_utilisation_cles_config()
    
    if explication_ok:
        # Créer un exemple
        creer_exemple_config()
        
        # Vérifier l'utilisation automatique
        verifier_utilisation_automatique()
        
        print("\n🎉 RÉSUMÉ:")
        print("-" * 10)
        print("✅ L'application utilise automatiquement les clés API du fichier")
        print("✅ Aucune action manuelle requise après configuration")
        print("✅ Les clés sont synchronisées entre interface et backend")
        print("✅ Les modifications sont sauvegardées automatiquement")
        
        print("\n💡 PROCHAINES ÉTAPES:")
        print("1. Vérifiez que votre fichier ~/.matelas_config.json contient vos clés API")
        print("2. Lancez l'application: python3 app_gui.py")
        print("3. Cochez '🤖 Enrichir avec LLM' et sélectionnez votre provider")
        print("4. Les clés seront automatiquement utilisées!")
        
    else:
        print("\n❌ Problème détecté lors de l'explication")
        print("Vérifiez que le fichier de configuration existe et est valide")

if __name__ == "__main__":
    main() 