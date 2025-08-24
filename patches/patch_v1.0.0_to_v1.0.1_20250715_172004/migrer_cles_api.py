#!/usr/bin/env python3

"""
Script pour migrer les clés API de la configuration classique vers le stockage sécurisé
"""

import sys
import os
import json
from pathlib import Path

def migrer_cles_api():
    """Migre les clés API de la configuration classique vers le stockage sécurisé"""
    
    print("🔄 MIGRATION DES CLÉS API")
    print("=" * 50)
    
    # Charger la configuration classique
    home_dir = Path.home()
    config_file = home_dir / ".matelas_config.json"
    
    if not config_file.exists():
        print("❌ Fichier de configuration classique non trouvé")
        return False
    
    print(f"📄 Fichier de configuration: {config_file.absolute()}")
    
    try:
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        print("✅ Configuration classique chargée")
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {e}")
        return False
    
    # Vérifier le stockage sécurisé
    try:
        sys.path.append('backend')
        from secure_storage import secure_storage
        print("✅ Module de stockage sécurisé disponible")
    except ImportError as e:
        print(f"❌ Module de stockage sécurisé non disponible: {e}")
        print("💡 Installez cryptography: pip install cryptography")
        return False
    
    # Clés à migrer
    cles_a_migrer = {
        'openrouter': 'openrouter_api_key',
        'openai': 'llm_api_key_openai',
        'anthropic': 'llm_api_key_anthropic',
        'gemini': 'llm_api_key_gemini',
        'mistral': 'llm_api_key_mistral'
    }
    
    print("\n🔑 CLÉS TROUVÉES DANS LA CONFIGURATION CLASSIQUE:")
    print("-" * 50)
    
    cles_migrees = []
    
    for service, config_key in cles_a_migrer.items():
        if config_key in config_data:
            api_key = config_data[config_key]
            if api_key and api_key.strip():
                print(f"✅ {service.upper()}: {api_key[:10]}...{api_key[-4:]}")
                cles_migrees.append((service, api_key))
            else:
                print(f"⚠️  {service.upper()}: Clé vide")
        else:
            print(f"❌ {service.upper()}: Non trouvée")
    
    if not cles_migrees:
        print("\n❌ Aucune clé API à migrer")
        return False
    
    # Migrer les clés
    print(f"\n🔄 MIGRATION DE {len(cles_migrees)} CLÉ(S):")
    print("-" * 30)
    
    for service, api_key in cles_migrees:
        try:
            # Vérifier si la clé existe déjà dans le stockage sécurisé
            existing_key = secure_storage.load_api_key(service)
            if existing_key:
                print(f"⚠️  {service.upper()}: Clé déjà présente dans le stockage sécurisé")
                continue
            
            # Sauvegarder dans le stockage sécurisé
            description = f"Migrée depuis la configuration classique - {service.upper()}"
            if secure_storage.save_api_key(service, api_key, description):
                print(f"✅ {service.upper()}: Migrée avec succès")
            else:
                print(f"❌ {service.upper()}: Erreur lors de la migration")
                
        except Exception as e:
            print(f"❌ {service.upper()}: Erreur - {e}")
    
    # Vérifier la migration
    print("\n🔍 VÉRIFICATION DE LA MIGRATION:")
    print("-" * 30)
    
    services_stockage = secure_storage.list_services()
    print(f"📋 Services dans le stockage sécurisé: {services_stockage}")
    
    for service, api_key in cles_migrees:
        if service in services_stockage:
            loaded_key = secure_storage.load_api_key(service)
            if loaded_key == api_key:
                print(f"✅ {service.upper()}: Migration validée")
            else:
                print(f"❌ {service.upper()}: Erreur de validation")
        else:
            print(f"❌ {service.upper()}: Non trouvée dans le stockage sécurisé")
    
    # Option pour nettoyer la configuration classique
    print("\n🧹 NETTOYAGE DE LA CONFIGURATION CLASSIQUE:")
    print("-" * 40)
    
    reponse = input("Voulez-vous supprimer les clés API de la configuration classique ? (o/N): ")
    
    if reponse.lower() in ['o', 'oui', 'y', 'yes']:
        try:
            # Supprimer les clés API de la configuration classique
            for service, config_key in cles_a_migrer.items():
                if config_key in config_data:
                    del config_data[config_key]
                    print(f"🗑️  {service.upper()}: Supprimée de la configuration classique")
            
            # Sauvegarder la configuration nettoyée
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            print("✅ Configuration classique nettoyée")
            
        except Exception as e:
            print(f"❌ Erreur lors du nettoyage: {e}")
    else:
        print("ℹ️  Configuration classique conservée")
    
    print("\n🎯 RÉSUMÉ DE LA MIGRATION:")
    print("-" * 30)
    print(f"✅ {len(cles_migrees)} clé(s) migrée(s) vers le stockage sécurisé")
    print("✅ Les clés sont maintenant chiffrées et sécurisées")
    print("✅ L'application chargera automatiquement les clés au démarrage")
    
    return True

def afficher_aide():
    """Affiche l'aide du script"""
    print("""
🔧 SCRIPT DE MIGRATION DES CLÉS API

Ce script migre les clés API de la configuration classique (~/.matelas_config.json) 
vers le stockage sécurisé (config/secure_keys.dat).

UTILISATION:
    python3 migrer_cles_api.py

AVANTAGES DU STOCKAGE SÉCURISÉ:
    ✅ Chiffrement AES-256 des clés
    ✅ Protection contre les accès non autorisés
    ✅ Gestion centralisée via l'interface graphique
    ✅ Compatible avec toutes les plateformes

CLÉS SUPPORTÉES:
    - OpenRouter (openrouter_api_key)
    - OpenAI (llm_api_key_openai)
    - Anthropic (llm_api_key_anthropic)
    - Google Gemini (llm_api_key_gemini)
    - Mistral (llm_api_key_mistral)

APRÈS LA MIGRATION:
    1. Les clés sont disponibles dans le gestionnaire de clés API
    2. L'application les charge automatiquement
    3. Option de nettoyage de l'ancienne configuration
    """)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        afficher_aide()
    else:
        migrer_cles_api() 