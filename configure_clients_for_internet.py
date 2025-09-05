#!/usr/bin/env python3
"""
Script pour configurer les clients MATELAS pour utiliser un serveur Internet
"""

import re
from pathlib import Path
import shutil
from datetime import datetime

def backup_files():
    """Créer des sauvegardes des fichiers modifiés"""
    backup_dir = Path("backups_before_internet_config")
    backup_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    files_to_backup = [
        "app_gui.py",
        "backend/auto_updater.py"
    ]
    
    print(f"💾 Création des sauvegardes dans {backup_dir}/")
    
    for file_path in files_to_backup:
        source = Path(file_path)
        if source.exists():
            backup_name = f"{source.name}_{timestamp}.bak"
            backup_path = backup_dir / backup_name
            shutil.copy2(source, backup_path)
            print(f"  ✅ {file_path} → {backup_name}")
    
    return backup_dir

def update_app_gui_server_url(new_url):
    """Mettre à jour l'URL du serveur dans app_gui.py"""
    file_path = Path("app_gui.py")
    
    if not file_path.exists():
        print(f"❌ Fichier {file_path} non trouvé")
        return False
    
    print(f"🔧 Mise à jour de {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remplacer les URLs localhost dans check_for_updates_async
    patterns_to_replace = [
        (r'check_for_updates_with_telemetry\\("http://localhost:8091"\\)', 
         f'check_for_updates_with_telemetry("{new_url}")'),
        (r'update_info = check_for_updates_with_telemetry\\("http://localhost:8091"\\)',
         f'update_info = check_for_updates_with_telemetry("{new_url}")'),
        (r'"http://localhost:8091"', f'"{new_url}"')
    ]
    
    changes_made = 0
    for pattern, replacement in patterns_to_replace:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            content = new_content
            changes_made += 1
    
    if changes_made > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ {changes_made} URL(s) mise(s) à jour dans app_gui.py")
        return True
    else:
        print(f"  ⚠️ Aucun changement nécessaire dans app_gui.py")
        return True

def update_auto_updater_server_url(new_url):
    """Mettre à jour l'URL du serveur dans backend/auto_updater.py"""
    file_path = Path("backend/auto_updater.py")
    
    if not file_path.exists():
        print(f"❌ Fichier {file_path} non trouvé")
        return False
    
    print(f"🔧 Mise à jour de {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remplacer les URLs localhost
    patterns_to_replace = [
        (r'server_url = "http://localhost:8091"',
         f'server_url = "{new_url}"'),
        (r'DEFAULT_SERVER_URL = "http://localhost:8091"',
         f'DEFAULT_SERVER_URL = "{new_url}"'),
        (r'"http://localhost:8091"', f'"{new_url}"'),
        (r'http://localhost:8091', new_url)
    ]
    
    changes_made = 0
    for pattern, replacement in patterns_to_replace:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            content = new_content
            changes_made += 1
    
    if changes_made > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ {changes_made} URL(s) mise(s) à jour dans auto_updater.py")
        return True
    else:
        print(f"  ⚠️ Aucun changement nécessaire dans auto_updater.py")
        return True

def create_config_file(server_url):
    """Créer un fichier de configuration pour l'URL du serveur"""
    config_content = f'''{{
    "update_server": {{
        "url": "{server_url}",
        "configured_at": "{datetime.now().isoformat()}",
        "type": "internet"
    }},
    "telemetry": {{
        "enabled": true,
        "collect_system_info": true,
        "collect_usage_stats": true
    }},
    "security": {{
        "verify_ssl": true,
        "timeout": 30
    }}
}}'''
    
    config_path = Path("update_server_config.json")
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print(f"✅ Configuration sauvée dans {config_path}")
    return config_path

def validate_server_url(url):
    """Valider l'URL du serveur"""
    if not url:
        return False, "URL vide"
    
    if not (url.startswith('http://') or url.startswith('https://')):
        return False, "URL doit commencer par http:// ou https://"
    
    if url.endswith('/'):
        url = url.rstrip('/')
    
    # Test de base de l'URL
    try:
        import requests
        response = requests.get(f"{url}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('message') and 'MATELAS' in data.get('message', ''):
                return True, url
            else:
                return False, "Ce ne semble pas être un serveur MATELAS"
        else:
            return False, f"Serveur non accessible (code {response.status_code})"
    except requests.exceptions.RequestException as e:
        return False, f"Erreur de connexion: {e}"

def test_client_connection(server_url):
    """Tester la connexion client au nouveau serveur"""
    print(f"\\n🧪 Test de connexion à {server_url}...")
    
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent / "backend"))
        from backend.auto_updater import check_for_updates_with_telemetry
        
        # Test de la fonction mise à jour
        update_info = check_for_updates_with_telemetry(server_url)
        
        if update_info:
            print("✅ Test de connexion réussi!")
            print(f"📦 Version serveur: {update_info.latest_version}")
            print(f"🔄 Mise à jour disponible: {'Oui' if update_info.available else 'Non'}")
            return True
        else:
            print("❌ Aucune réponse du serveur")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def show_deployment_summary(server_url, backup_dir):
    """Afficher le résumé du déploiement"""
    print("\\n🎉 CONFIGURATION TERMINÉE!")
    print("=" * 30)
    
    print(f"🌐 Serveur configuré: {server_url}")
    print(f"💾 Sauvegardes créées dans: {backup_dir}/")
    print(f"📝 Configuration sauvée dans: update_server_config.json")
    
    print("\\n📋 FICHIERS MODIFIÉS:")
    print("• app_gui.py - URLs mises à jour")
    print("• backend/auto_updater.py - URLs mises à jour")
    print("• update_server_config.json - Configuration créée")
    
    print("\\n🔄 PROCHAINES ÉTAPES:")
    print("1. Testez l'application: python3 app_gui.py")
    print("2. Vérifiez l'indicateur de mise à jour dans la barre de statut")
    print("3. Créez une nouvelle version avec ces modifications")
    print("4. Déployez cette version sur tous les postes clients")
    
    print("\\n⚠️ IMPORTANT:")
    print("• Les clients utiliseront maintenant le serveur Internet")
    print("• Assurez-vous que le serveur reste accessible")
    print("• Les identifiants admin par défaut doivent être changés")
    
    print("\\n🔙 RESTAURATION:")
    print(f"En cas de problème, restaurez depuis {backup_dir}/")

def main():
    """Fonction principale"""
    print("🌐 CONFIGURATION DES CLIENTS POUR SERVEUR INTERNET")
    print("=" * 55)
    
    print("\\nℹ️  Ce script va modifier les fichiers clients pour utiliser")
    print("   un serveur de mise à jour sur Internet au lieu de localhost")
    
    # Demander l'URL du serveur
    print("\\n🔗 Entrez l'URL de votre serveur Internet:")
    print("Exemples:")
    print("  • https://abc123.ngrok.io (tunnel ngrok)")
    print("  • https://updates.mondomaine.com (VPS avec domaine)")
    print("  • http://12.34.56.78:8091 (VPS avec IP)")
    
    server_url = input("\\nURL du serveur: ").strip()
    
    # Valider l'URL
    is_valid, message = validate_server_url(server_url)
    if not is_valid:
        print(f"❌ URL invalide: {message}")
        return False
    
    server_url = message  # URL nettoyée
    print(f"✅ URL validée: {server_url}")
    
    # Confirmer les modifications
    print(f"\\n⚠️  Cette opération va modifier les fichiers clients.")
    confirm = input("Continuer ? (oui/non): ").strip().lower()
    if confirm not in ['oui', 'yes', 'y', 'o']:
        print("❌ Opération annulée")
        return False
    
    try:
        # 1. Créer des sauvegardes
        backup_dir = backup_files()
        
        # 2. Mettre à jour les fichiers
        print(f"\\n🔧 Configuration pour le serveur: {server_url}")
        
        success1 = update_app_gui_server_url(server_url)
        success2 = update_auto_updater_server_url(server_url)
        
        if not (success1 and success2):
            print("❌ Erreurs lors de la mise à jour des fichiers")
            return False
        
        # 3. Créer le fichier de configuration
        create_config_file(server_url)
        
        # 4. Tester la connexion
        if test_client_connection(server_url):
            print("✅ Configuration réussie!")
        else:
            print("⚠️ Configuration appliquée mais test de connexion échoué")
            print("   Vérifiez que le serveur est accessible")
        
        # 5. Afficher le résumé
        show_deployment_summary(server_url, backup_dir)
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la configuration: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\\n🎉 Configuration terminée avec succès!")
    else:
        print("\\n❌ Échec de la configuration")
        print("Consultez les erreurs ci-dessus")