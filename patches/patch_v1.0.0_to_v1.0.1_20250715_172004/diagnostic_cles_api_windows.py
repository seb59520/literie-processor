#!/usr/bin/env python3

"""
Script de diagnostic pour les clés API sous Windows
"""

import sys
import os
import platform
from pathlib import Path

def diagnostic_cles_api_windows():
    """Diagnostique le problème de stockage des clés API sous Windows"""
    
    print("🔍 DIAGNOSTIC CLÉS API - PROBLÈME WINDOWS")
    print("=" * 60)
    
    # Informations système
    print(f"🖥️  Système d'exploitation: {platform.system()}")
    print(f"📋 Version: {platform.version()}")
    print(f"🏗️  Architecture: {platform.architecture()}")
    
    # Vérifier les fichiers de stockage
    print("\n📁 VÉRIFICATION DES FICHIERS DE STOCKAGE:")
    print("-" * 40)
    
    # Fichiers de stockage sécurisé
    config_dir = Path("config")
    secure_keys_file = config_dir / "secure_keys.dat"
    salt_file = config_dir / "salt.dat"
    
    print(f"📂 Dossier config: {config_dir.absolute()}")
    print(f"  ✅ Existe: {config_dir.exists()}")
    if config_dir.exists():
        print(f"  📏 Taille: {len(list(config_dir.iterdir()))} fichiers")
    
    print(f"🔐 Fichier clés sécurisées: {secure_keys_file.absolute()}")
    print(f"  ✅ Existe: {secure_keys_file.exists()}")
    if secure_keys_file.exists():
        print(f"  📏 Taille: {secure_keys_file.stat().st_size} octets")
    
    print(f"🧂 Fichier salt: {salt_file.absolute()}")
    print(f"  ✅ Existe: {salt_file.exists()}")
    if salt_file.exists():
        print(f"  📏 Taille: {salt_file.stat().st_size} octets")
    
    # Fichier de configuration classique
    home_dir = Path.home()
    config_file = home_dir / ".matelas_config.json"
    
    print(f"\n📄 Fichier config classique: {config_file.absolute()}")
    print(f"  ✅ Existe: {config_file.exists()}")
    if config_file.exists():
        print(f"  📏 Taille: {config_file.stat().st_size} octets")
        try:
            import json
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            print(f"  📋 Contenu: {list(config_data.keys())}")
            if 'openrouter_api_key' in config_data:
                key = config_data['openrouter_api_key']
                print(f"  🔑 Clé OpenRouter: {key[:10]}...{key[-4:] if len(key) > 14 else '***'}")
        except Exception as e:
            print(f"  ❌ Erreur lecture: {e}")
    
    # Vérifier les variables d'environnement
    print("\n🌍 VÉRIFICATION DES VARIABLES D'ENVIRONNEMENT:")
    print("-" * 40)
    
    env_vars = [
        'MATELAS_MASTER_PASSWORD',
        'OPENROUTER_API_KEY',
        'OPENAI_API_KEY',
        'ANTHROPIC_API_KEY'
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value[:10]}...{value[-4:] if len(value) > 14 else '***'}")
        else:
            print(f"❌ {var}: Non définie")
    
    # Test du module de stockage sécurisé
    print("\n🔐 TEST DU MODULE DE STOCKAGE SÉCURISÉ:")
    print("-" * 40)
    
    try:
        sys.path.append('backend')
        from secure_storage import secure_storage
        print("✅ Module secure_storage importé avec succès")
        
        # Test de chiffrement
        if secure_storage.test_encryption():
            print("✅ Test de chiffrement réussi")
        else:
            print("❌ Test de chiffrement échoué")
        
        # Lister les services
        services = secure_storage.list_services()
        print(f"📋 Services trouvés: {services}")
        
        # Vérifier la clé OpenRouter
        openrouter_key = secure_storage.load_api_key("openrouter")
        if openrouter_key:
            print(f"✅ Clé OpenRouter trouvée: {openrouter_key[:10]}...{openrouter_key[-4:]}")
        else:
            print("❌ Aucune clé OpenRouter trouvée")
            
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("💡 Solution: pip install cryptography")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Vérifier les permissions
    print("\n🔒 VÉRIFICATION DES PERMISSIONS:")
    print("-" * 40)
    
    if config_dir.exists():
        try:
            # Test d'écriture
            test_file = config_dir / "test_write.tmp"
            test_file.write_text("test")
            test_file.unlink()
            print("✅ Permissions d'écriture OK")
        except Exception as e:
            print(f"❌ Erreur permissions: {e}")
    
    # Recommandations
    print("\n💡 RECOMMANDATIONS POUR WINDOWS:")
    print("-" * 40)
    
    print("1. 🔐 Stockage sécurisé (recommandé):")
    print("   - Installez cryptography: pip install cryptography")
    print("   - Utilisez le gestionnaire de clés API dans l'application")
    print("   - Les clés sont stockées dans config/secure_keys.dat")
    
    print("\n2. 📄 Configuration classique:")
    print("   - Les clés sont stockées dans ~/.matelas_config.json")
    print("   - Format JSON non chiffré")
    print("   - Moins sécurisé mais plus simple")
    
    print("\n3. 🌍 Variables d'environnement:")
    print("   - Définissez MATELAS_MASTER_PASSWORD pour le stockage sécurisé")
    print("   - Définissez OPENROUTER_API_KEY pour la configuration classique")
    
    print("\n4. 🔧 Dépannage Windows:")
    print("   - Vérifiez les permissions sur le dossier config/")
    print("   - Exécutez l'application en tant qu'administrateur si nécessaire")
    print("   - Vérifiez que le dossier config/ est accessible en écriture")
    
    # Test de création de clé
    print("\n🧪 TEST DE CRÉATION DE CLÉ:")
    print("-" * 40)
    
    try:
        sys.path.append('backend')
        from secure_storage import secure_storage
        
        # Test de sauvegarde
        test_key = "sk-test-windows-diagnostic-12345"
        if secure_storage.save_api_key("test_windows", test_key, "Test Windows"):
            print("✅ Sauvegarde de clé de test réussie")
            
            # Test de chargement
            loaded_key = secure_storage.load_api_key("test_windows")
            if loaded_key == test_key:
                print("✅ Chargement de clé de test réussi")
                
                # Nettoyer
                secure_storage.delete_api_key("test_windows")
                print("✅ Suppression de clé de test réussie")
            else:
                print("❌ Erreur lors du chargement de la clé de test")
        else:
            print("❌ Erreur lors de la sauvegarde de la clé de test")
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
    
    print("\n🎯 RÉSUMÉ:")
    print("-" * 20)
    
    if secure_keys_file.exists():
        print("✅ Stockage sécurisé disponible")
    else:
        print("❌ Stockage sécurisé non configuré")
    
    if config_file.exists():
        print("✅ Configuration classique disponible")
    else:
        print("❌ Configuration classique non configurée")
    
    print("\n📝 PROCHAINES ÉTAPES:")
    print("1. Installez cryptography si nécessaire")
    print("2. Utilisez le gestionnaire de clés API dans l'application")
    print("3. Ou configurez les variables d'environnement")
    print("4. Relancez l'application")

if __name__ == "__main__":
    diagnostic_cles_api_windows() 