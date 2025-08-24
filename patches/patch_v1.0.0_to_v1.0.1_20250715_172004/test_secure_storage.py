#!/usr/bin/env python3
"""
Script de test pour le stockage sécurisé des clés API
"""

import sys
import os

# Ajouter le dossier backend au path
sys.path.append('backend')

def test_secure_storage():
    """Teste le système de stockage sécurisé"""
    print("🔐 Test du Système de Stockage Sécurisé")
    print("=" * 50)
    
    try:
        # Importer le module de stockage sécurisé
        from secure_storage import secure_storage
        print("✅ Module secure_storage importé avec succès")
        
        # Test 1: Test de chiffrement
        print("\n🧪 Test 1: Test de chiffrement")
        if secure_storage.test_encryption():
            print("✅ Test de chiffrement réussi")
        else:
            print("❌ Test de chiffrement échoué")
            return False
        
        # Test 2: Sauvegarde d'une clé API
        print("\n💾 Test 2: Sauvegarde d'une clé API")
        test_key = "sk-test-1234567890abcdef"
        if secure_storage.save_api_key("test_service", test_key, "Clé de test"):
            print("✅ Clé API sauvegardée avec succès")
        else:
            print("❌ Erreur lors de la sauvegarde")
            return False
        
        # Test 3: Chargement de la clé API
        print("\n📖 Test 3: Chargement de la clé API")
        loaded_key = secure_storage.load_api_key("test_service")
        if loaded_key == test_key:
            print("✅ Clé API chargée correctement")
        else:
            print(f"❌ Erreur lors du chargement: attendu '{test_key}', obtenu '{loaded_key}'")
            return False
        
        # Test 4: Récupération des informations
        print("\n📋 Test 4: Récupération des informations")
        info = secure_storage.get_api_key_info("test_service")
        if info and info.get('api_key') == test_key:
            print("✅ Informations récupérées correctement")
            print(f"   Description: {info.get('description')}")
            print(f"   Créée le: {info.get('created_at')}")
        else:
            print("❌ Erreur lors de la récupération des informations")
            return False
        
        # Test 5: Liste des services
        print("\n📝 Test 5: Liste des services")
        services = secure_storage.list_services()
        if "test_service" in services:
            print("✅ Service trouvé dans la liste")
            print(f"   Services disponibles: {services}")
        else:
            print("❌ Service non trouvé dans la liste")
            return False
        
        # Test 6: Suppression de la clé API
        print("\n🗑️ Test 6: Suppression de la clé API")
        if secure_storage.delete_api_key("test_service"):
            print("✅ Clé API supprimée avec succès")
        else:
            print("❌ Erreur lors de la suppression")
            return False
        
        # Test 7: Vérification de la suppression
        print("\n🔍 Test 7: Vérification de la suppression")
        remaining_services = secure_storage.list_services()
        if "test_service" not in remaining_services:
            print("✅ Suppression confirmée")
        else:
            print("❌ La clé API n'a pas été supprimée")
            return False
        
        print("\n🎉 Tous les tests sont passés avec succès !")
        print("Le système de stockage sécurisé fonctionne correctement.")
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("Installez la dépendance 'cryptography': pip install cryptography")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_multiple_keys():
    """Teste la gestion de plusieurs clés API"""
    print("\n🔑 Test de Gestion de Plusieurs Clés API")
    print("=" * 50)
    
    try:
        from secure_storage import secure_storage
        
        # Sauvegarder plusieurs clés
        keys_to_save = {
            "openrouter": ("sk-or-test-123456", "Clé OpenRouter de test"),
            "ollama": ("ollama-test-key", "Clé Ollama de test"),
            "anthropic": ("sk-ant-test-789", "Clé Anthropic de test")
        }
        
        for service, (key, description) in keys_to_save.items():
            if secure_storage.save_api_key(service, key, description):
                print(f"✅ Clé {service} sauvegardée")
            else:
                print(f"❌ Erreur lors de la sauvegarde de {service}")
                return False
        
        # Vérifier la liste
        services = secure_storage.list_services()
        print(f"📋 Services sauvegardés: {services}")
        
        # Vérifier chaque clé
        for service, (expected_key, description) in keys_to_save.items():
            loaded_key = secure_storage.load_api_key(service)
            if loaded_key == expected_key:
                print(f"✅ Clé {service} chargée correctement")
            else:
                print(f"❌ Erreur pour {service}: attendu '{expected_key}', obtenu '{loaded_key}'")
                return False
        
        # Nettoyer
        for service in keys_to_save.keys():
            secure_storage.delete_api_key(service)
        
        print("🎉 Test de gestion multiple réussi !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test multiple: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Démarrage des tests du stockage sécurisé")
    
    # Test principal
    if test_secure_storage():
        # Test de gestion multiple
        test_multiple_keys()
    else:
        print("\n❌ Les tests de base ont échoué, arrêt des tests")
        sys.exit(1)
    
    print("\n✨ Tests terminés avec succès !") 