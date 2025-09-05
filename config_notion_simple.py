#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration simple et robuste pour l'intégration Notion
"""

import json
import requests
from pathlib import Path

def print_header():
    """Affiche l'en-tête"""
    print("🔧 Configuration simple Notion")
    print("=" * 40)
    print()

def get_api_key():
    """Obtient la clé API"""
    print("🔑 Étape 1: Clé API Notion")
    print("-" * 30)
    
    print("1. Allez sur: https://www.notion.so/my-integrations")
    print("2. Cliquez sur 'New integration'")
    print("3. Nom: 'Cursor Integration'")
    print("4. Sélectionnez votre workspace")
    print("5. Cliquez sur 'Submit'")
    print("6. Copiez la clé API (Internal Integration Token)")
    print()
    
    while True:
        api_key = input("Entrez votre clé API Notion: ").strip()
        
        if not api_key:
            print("❌ Clé API requise")
            continue
            
        if not api_key.startswith("ntn_"):
            print("❌ Format de clé invalide (doit commencer par 'ntn_')")
            continue
            
        if len(api_key) < 50:
            print("❌ Clé API trop courte")
            continue
            
        print("✅ Clé API valide")
        return api_key

def test_api_key(api_key):
    """Teste la clé API"""
    print("\n🔄 Test de la clé API...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    try:
        response = requests.get(
            "https://api.notion.com/v1/users/me",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            user_info = response.json()
            print(f"✅ Connexion réussie! Utilisateur: {user_info.get('name', 'Inconnu')}")
            return True
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"💡 Réponse: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def get_database_info(api_key):
    """Obtient les informations de la base de données"""
    print("\n🗄️  Étape 2: Base de données")
    print("-" * 30)
    
    print("1. Créez une nouvelle page dans Notion")
    print("2. Tapez '/database' et sélectionnez 'Table'")
    print("3. Ajoutez ces propriétés:")
    print("   • Nom (Title)")
    print("   • Chemin (Text)")
    print("   • Description (Text)")
    print("   • Langage (Select)")
    print("   • Framework (Text)")
    print("   • Dernière modification (Date)")
    print("   • Statut Git (Select)")
    print("   • Workspace Cursor (Text)")
    print("   • Statut (Select)")
    print("   • Date de création (Date)")
    print()
    
    input("Appuyez sur Entrée quand c'est fait...")
    
    # Obtenir l'ID de la base de données
    while True:
        print("\nPour obtenir l'ID de la base de données:")
        print("1. Ouvrez la base de données dans Notion")
        print("2. L'URL est: https://notion.so/[workspace]/[database-id]?v=...")
        print("3. Copiez la partie [database-id] (32 caractères hexadécimaux)")
        print()
        
        database_id = input("ID de la base de données: ").strip()
        
        if not database_id:
            print("❌ ID requis")
            continue
            
        if len(database_id) != 32:
            print(f"❌ ID incorrect (longueur: {len(database_id)}, attendu: 32)")
            continue
            
        # Vérifier que c'est un ID valide (hexadécimal)
        try:
            int(database_id, 16)
        except ValueError:
            print("❌ Format d'ID invalide (doit être hexadécimal)")
            continue
            
        print("✅ ID de base de données valide")
        break
    
    # Obtenir l'ID du workspace
    while True:
        print("\nPour obtenir l'ID du workspace:")
        print("1. L'URL de votre workspace est: https://notion.so/[workspace]")
        print("2. Copiez la partie [workspace]")
        print()
        
        workspace_id = input("ID du workspace: ").strip()
        
        if not workspace_id:
            print("❌ ID de workspace requis")
            continue
            
        if len(workspace_id) < 5:
            print("❌ ID de workspace trop court")
            continue
            
        print("✅ ID de workspace valide")
        break
    
    return database_id, workspace_id

def test_database_access(api_key, database_id):
    """Teste l'accès à la base de données"""
    print("\n🔄 Test d'accès à la base de données...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    try:
        response = requests.get(
            f"https://api.notion.com/v1/databases/{database_id}",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            db_info = response.json()
            db_title = db_info.get('title', [{}])[0].get('plain_text', 'Sans titre')
            print(f"✅ Base accessible: {db_title}")
            return True
        elif response.status_code == 404:
            print("❌ Base introuvable")
            print("💡 Vérifiez l'ID ou créez une nouvelle base")
            return False
        elif response.status_code == 403:
            print("❌ Accès refusé")
            print("💡 Partagez la base avec votre intégration")
            print("   - Ouvrez la base dans Notion")
            print("   - Cliquez sur 'Share'")
            print("   - Invitez votre intégration 'Cursor Integration'")
            return False
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"💡 Réponse: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def create_config_file(api_key, database_id, workspace_id):
    """Crée le fichier de configuration"""
    print("\n💾 Création du fichier de configuration...")
    
    config = {
        "api_key": api_key,
        "database_id": database_id,
        "workspace_id": workspace_id
    }
    
    config_path = Path("notion_config.json")
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Configuration sauvegardée: {config_path}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur sauvegarde: {e}")
        return False

def main():
    """Fonction principale"""
    print_header()
    
    try:
        # Étape 1: Clé API
        api_key = get_api_key()
        
        # Test de la clé API
        if not test_api_key(api_key):
            print("\n❌ Échec du test de la clé API")
            print("💡 Vérifiez votre clé et réessayez")
            return
        
        # Étape 2: Base de données
        database_id, workspace_id = get_database_info(api_key)
        
        # Test d'accès à la base
        if not test_database_access(api_key, database_id):
            print("\n❌ Échec du test d'accès à la base")
            print("💡 Vérifiez les permissions et réessayez")
            return
        
        # Étape 3: Sauvegarde
        if create_config_file(api_key, database_id, workspace_id):
            print("\n🎉 Configuration terminée avec succès!")
            print("\n🚀 Vous pouvez maintenant lancer:")
            print("   python3 notion_manager_gui.py")
            print("   ou")
            print("   python3 lancer_notion_integration.py")
        else:
            print("\n❌ Erreur lors de la sauvegarde")
            
    except KeyboardInterrupt:
        print("\n\n❌ Configuration annulée")
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")

if __name__ == "__main__":
    main()


