#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de configuration automatique pour l'intégration Notion avec Cursor
Guide l'utilisateur à travers la configuration étape par étape
"""

import os
import json
import webbrowser
from pathlib import Path
import requests

def print_header():
    """Affiche l'en-tête du script"""
    print("=" * 60)
    print("🚀 Configuration de l'intégration Notion avec Cursor")
    print("=" * 60)
    print()

def print_step(step_num, title):
    """Affiche une étape de configuration"""
    print(f"📋 Étape {step_num}: {title}")
    print("-" * 40)

def get_user_input(prompt, default=""):
    """Obtient une entrée utilisateur avec une valeur par défaut"""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    else:
        return input(f"{prompt}: ").strip()

def create_notion_integration():
    """Crée une intégration Notion"""
    print_step(1, "Création d'une intégration Notion")
    
    print("Pour commencer, vous devez créer une intégration dans Notion:")
    print("1. Allez sur https://www.notion.so/my-integrations")
    print("2. Cliquez sur 'New integration'")
    print("3. Donnez un nom à votre intégration (ex: 'Cursor Integration')")
    print("4. Sélectionnez votre workspace")
    print("5. Cliquez sur 'Submit'")
    print()
    
    input("Appuyez sur Entrée quand vous avez créé l'intégration...")
    
    # Ouvrir la page des intégrations
    webbrowser.open("https://www.notion.so/my-integrations")
    
    print("\nUne fois l'intégration créée, copiez la clé API (Internal Integration Token)")
    api_key = get_user_input("Entrez votre clé API Notion")
    
    return api_key

def get_database_info(api_key):
    """Obtient les informations de la base de données"""
    print_step(2, "Configuration de la base de données")
    
    print("Maintenant, vous devez créer une base de données dans Notion:")
    print("1. Créez une nouvelle page dans Notion")
    print("2. Tapez '/database' et sélectionnez 'Table'")
    print("3. Ajoutez les propriétés suivantes:")
    print("   - Nom (Title)")
    print("   - Chemin (Text)")
    print("   - Description (Text)")
    print("   - Langage (Select)")
    print("   - Framework (Text)")
    print("   - Dernière modification (Date)")
    print("   - Statut Git (Select)")
    print("   - Workspace Cursor (Text)")
    print("   - Statut (Select)")
    print("   - Date de création (Date)")
    print()
    
    input("Appuyez sur Entrée quand vous avez créé la base de données...")
    
    # Obtenir l'ID de la base de données
    print("\nPour obtenir l'ID de la base de données:")
    print("1. Ouvrez la base de données dans Notion")
    print("2. L'URL sera de la forme: https://notion.so/[workspace]/[database-id]?v=...")
    print("3. Copiez la partie [database-id] (32 caractères)")
    print()
    
    database_id = get_user_input("Entrez l'ID de la base de données")
    
    # Obtenir l'ID du workspace
    print("\nPour obtenir l'ID du workspace:")
    print("1. L'URL de votre workspace est de la forme: https://notion.so/[workspace]")
    print("2. Copiez la partie [workspace]")
    print()
    
    workspace_id = get_user_input("Entrez l'ID du workspace")
    
    return database_id, workspace_id

def test_notion_connection(api_key, database_id):
    """Teste la connexion à Notion"""
    print_step(3, "Test de la connexion")
    
    print("Test de la connexion à Notion...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    try:
        # Tenter de récupérer la base de données
        response = requests.get(
            f"https://api.notion.com/v1/databases/{database_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            print("✅ Connexion réussie à Notion!")
            return True
        else:
            print(f"❌ Erreur de connexion: {response.status_code}")
            print(f"Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def create_config_file(api_key, database_id, workspace_id):
    """Crée le fichier de configuration"""
    print_step(4, "Création du fichier de configuration")
    
    config = {
        "api_key": api_key,
        "database_id": database_id,
        "workspace_id": workspace_id
    }
    
    config_path = Path("notion_config.json")
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Fichier de configuration créé: {config_path}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur création fichier: {e}")
        return False

def create_sample_database_structure():
    """Crée un exemple de structure de base de données"""
    print_step(5, "Structure de base de données recommandée")
    
    print("Voici la structure recommandée pour votre base de données Notion:")
    print()
    
    structure = {
        "Propriétés": {
            "Nom": "Title (obligatoire)",
            "Chemin": "Text - Chemin du projet sur le disque",
            "Description": "Text - Description du projet",
            "Langage": "Select - Python, JavaScript, Java, C++, Go, Rust, PHP, Autre",
            "Framework": "Text - Framework utilisé (Django, React, Spring, etc.)",
            "Dernière modification": "Date - Date de dernière modification",
            "Statut Git": "Select - Git initialisé, Non versionné",
            "Workspace Cursor": "Text - Chemin du workspace Cursor",
            "Statut": "Select - En cours, Terminé, En pause, Abandonné",
            "Date de création": "Date - Date de création de la page"
        }
    }
    
    for prop, desc in structure["Propriétés"].items():
        print(f"  • {prop}: {desc}")
    
    print()
    print("Vous pouvez ajouter d'autres propriétés selon vos besoins.")
    print()

def install_dependencies():
    """Installe les dépendances nécessaires"""
    print_step(6, "Installation des dépendances")
    
    print("Installation des packages Python nécessaires...")
    
    try:
        import subprocess
        import sys
        
        packages = ["requests"]
        
        for package in packages:
            print(f"Installation de {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installé avec succès")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur installation: {e}")
        print("Vous pouvez installer manuellement avec: pip install requests")
        return False

def create_quick_start_guide():
    """Crée un guide de démarrage rapide"""
    print_step(7, "Guide de démarrage rapide")
    
    guide_content = """# Guide de démarrage rapide - Intégration Notion avec Cursor

## 🚀 Démarrage rapide

1. **Lancer l'interface graphique:**
   ```bash
   python notion_manager_gui.py
   ```

2. **Configuration initiale:**
   - Allez dans l'onglet "⚙️ Configuration"
   - Vérifiez que vos clés sont correctes
   - Cliquez sur "Tester la connexion"

3. **Première synchronisation:**
   - Allez dans l'onglet "🔄 Synchronisation"
   - Sélectionnez votre workspace Cursor
   - Cliquez sur "Scanner le workspace"
   - Puis "Synchroniser avec Notion"

## 📁 Utilisation des onglets

- **⚙️ Configuration**: Gestion des clés API Notion
- **📁 Projets**: Visualisation et gestion des projets détectés
- **📝 Modifications**: Suivi des changements dans vos fichiers
- **📚 Notices d'utilisation**: Création de documentation
- **🔗 Liens externes**: Gestion des ressources externes
- **🔄 Synchronisation**: Synchronisation avec Notion

## 🔧 Commandes utiles

- **Scan manuel**: `python notion_integration.py`
- **Test de connexion**: Vérifiez la configuration dans l'interface

## 📚 Documentation complète

Consultez le fichier `notion_integration.py` pour plus de détails sur l'API.
"""
    
    try:
        with open("GUIDE_DEMARRAGE_NOTION.md", 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        print("✅ Guide de démarrage créé: GUIDE_DEMARRAGE_NOTION.md")
        return True
        
    except Exception as e:
        print(f"❌ Erreur création guide: {e}")
        return False

def main():
    """Fonction principale"""
    print_header()
    
    print("Ce script vous guide à travers la configuration de l'intégration Notion.")
    print("Assurez-vous d'avoir un compte Notion et d'être connecté.")
    print()
    
    # Vérifier si la configuration existe déjà
    config_path = Path("notion_config.json")
    if config_path.exists():
        print("⚠️  Une configuration existe déjà.")
        overwrite = input("Voulez-vous la remplacer? (o/N): ").strip().lower()
        if overwrite not in ['o', 'oui', 'y', 'yes']:
            print("Configuration annulée.")
            return
    
    try:
        # Étape 1: Création de l'intégration
        api_key = create_notion_integration()
        if not api_key:
            print("❌ Clé API manquante. Configuration annulée.")
            return
        
        # Étape 2: Informations de la base de données
        database_id, workspace_id = get_database_info(api_key)
        if not database_id or not workspace_id:
            print("❌ Informations de base de données manquantes. Configuration annulée.")
            return
        
        # Étape 3: Test de connexion
        if not test_notion_connection(api_key, database_id):
            print("❌ Échec de la connexion. Vérifiez vos clés.")
            return
        
        # Étape 4: Création du fichier de configuration
        if not create_config_file(api_key, database_id, workspace_id):
            print("❌ Échec de la création du fichier de configuration.")
            return
        
        # Étape 5: Structure recommandée
        create_sample_database_structure()
        
        # Étape 6: Installation des dépendances
        install_dependencies()
        
        # Étape 7: Guide de démarrage
        create_quick_start_guide()
        
        print("\n" + "=" * 60)
        print("🎉 Configuration terminée avec succès!")
        print("=" * 60)
        print()
        print("Prochaines étapes:")
        print("1. Vérifiez que votre base de données Notion a la bonne structure")
        print("2. Lancez l'interface graphique: python notion_manager_gui.py")
        print("3. Testez la synchronisation avec votre workspace Cursor")
        print()
        print("Consultez le fichier GUIDE_DEMARRAGE_NOTION.md pour plus de détails.")
        
    except KeyboardInterrupt:
        print("\n\n❌ Configuration annulée par l'utilisateur.")
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        print("Vérifiez vos paramètres et réessayez.")

if __name__ == "__main__":
    main()


