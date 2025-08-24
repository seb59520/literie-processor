#!/usr/bin/env python3
"""
Script de diagnostic spécifique pour Windows - Problème clé API OpenRouter
"""

import os
import json
import sys
from pathlib import Path

def diagnostiquer_cles_windows():
    """Diagnostique le problème de clés API sous Windows"""
    
    print("🔍 DIAGNOSTIC CLÉS API WINDOWS")
    print("=" * 50)
    
    # Vérifier le système d'exploitation
    print(f"🖥️  Système: {sys.platform}")
    print(f"🐍 Python: {sys.version}")
    
    # 1. Vérifier le fichier de configuration classique
    home_dir = Path.home()
    config_file = home_dir / ".matelas_config.json"
    
    print(f"\n📁 Fichier de configuration: {config_file}")
    
    if config_file.exists():
        print("✅ Fichier de configuration trouvé")
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            print(f"📄 Contenu du fichier:")
            for key, value in config.items():
                if 'api_key' in key.lower() or 'openrouter' in key.lower():
                    masked_value = value[:10] + "..." if value else "VIDE"
                    print(f"   {key}: {masked_value}")
                else:
                    print(f"   {key}: {value}")
                    
            # Vérifier spécifiquement OpenRouter
            openrouter_key = config.get('openrouter_api_key') or config.get('OPENROUTER_API_KEY')
            if openrouter_key:
                print(f"✅ Clé OpenRouter trouvée: {openrouter_key[:10]}...")
            else:
                print("❌ Clé OpenRouter non trouvée dans le fichier")
                
        except Exception as e:
            print(f"❌ Erreur lecture fichier: {e}")
    else:
        print("❌ Fichier de configuration non trouvé")
    
    # 2. Vérifier les variables d'environnement
    print(f"\n🌍 Variables d'environnement:")
    env_vars = [
        'OPENROUTER_API_KEY',
        'MATELAS_OPENROUTER_API_KEY',
        'MATELAS_MASTER_PASSWORD'
    ]
    
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            masked_value = value[:10] + "..." if len(value) > 10 else value
            print(f"   {var}: {masked_value}")
        else:
            print(f"   {var}: Non définie")
    
    # 3. Vérifier le stockage sécurisé
    print(f"\n🔐 Stockage sécurisé:")
    secure_keys_file = Path("config/secure_keys.dat")
    salt_file = Path("config/salt.dat")
    
    if secure_keys_file.exists():
        print(f"✅ Fichier clés sécurisées: {secure_keys_file}")
        print(f"   Taille: {secure_keys_file.stat().st_size} octets")
    else:
        print(f"❌ Fichier clés sécurisées non trouvé")
    
    if salt_file.exists():
        print(f"✅ Fichier salt: {salt_file}")
        print(f"   Taille: {salt_file.stat().st_size} octets")
    else:
        print(f"❌ Fichier salt non trouvé")
    
    # 4. Tester l'import du module de configuration
    print(f"\n🔧 Test du module de configuration:")
    try:
        import config
        print("✅ Module config importé avec succès")
        
        # Tester la fonction get_openrouter_api_key
        try:
            api_key = config.get_openrouter_api_key()
            if api_key:
                print(f"✅ Clé API récupérée: {api_key[:10]}...")
            else:
                print("❌ Aucune clé API récupérée")
        except Exception as e:
            print(f"❌ Erreur récupération clé: {e}")
            
    except Exception as e:
        print(f"❌ Erreur import module config: {e}")
    
    # 5. Vérifier les permissions de fichiers
    print(f"\n🔒 Permissions de fichiers:")
    files_to_check = [
        config_file,
        secure_keys_file,
        salt_file,
        Path("config.py")
    ]
    
    for file_path in files_to_check:
        if file_path.exists():
            try:
                # Tester la lecture
                with open(file_path, 'r', encoding='utf-8') as f:
                    f.read(1)
                print(f"✅ Lecture OK: {file_path.name}")
            except Exception as e:
                print(f"❌ Erreur lecture {file_path.name}: {e}")
        else:
            print(f"⚠️  Fichier non trouvé: {file_path.name}")
    
    # 6. Recommandations
    print(f"\n💡 RECOMMANDATIONS:")
    print("1. Vérifiez que le fichier ~/.matelas_config.json contient 'openrouter_api_key'")
    print("2. Assurez-vous que la clé API est valide et active")
    print("3. Vérifiez les permissions de lecture du fichier")
    print("4. Si problème persiste, utilisez la variable d'environnement OPENROUTER_API_KEY")
    print("5. Redémarrez l'application après modification")

if __name__ == "__main__":
    diagnostiquer_cles_windows() 