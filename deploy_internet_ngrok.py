#!/usr/bin/env python3
"""
Script de déploiement rapide sur Internet avec ngrok
"""

import os
import subprocess
import sys
import time
import requests
import json
from pathlib import Path

def check_ngrok_installed():
    """Vérifier si ngrok est installé"""
    try:
        result = subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ ngrok déjà installé: {result.stdout.strip()}")
            return True
        else:
            return False
    except FileNotFoundError:
        return False

def install_ngrok_mac():
    """Installer ngrok sur macOS"""
    print("📦 Installation de ngrok sur macOS...")
    
    try:
        # Vérifier si Homebrew est disponible
        subprocess.run(['brew', '--version'], capture_output=True, check=True)
        print("🍺 Installation via Homebrew...")
        subprocess.run(['brew', 'install', 'ngrok/ngrok/ngrok'], check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️ Homebrew non trouvé, installation manuelle requise")
        print("Visitez https://ngrok.com/download et suivez les instructions")
        return False

def setup_ngrok_auth():
    """Configurer l'authentification ngrok"""
    print("\\n🔑 Configuration de l'authentification ngrok...")
    print("1. Visitez: https://dashboard.ngrok.com/get-started/your-authtoken")
    print("2. Copiez votre authtoken")
    
    authtoken = input("3. Collez votre authtoken ici: ").strip()
    
    if authtoken:
        try:
            subprocess.run(['ngrok', 'config', 'add-authtoken', authtoken], check=True)
            print("✅ Authtoken configuré avec succès")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de la configuration: {e}")
            return False
    else:
        print("❌ Authtoken requis pour continuer")
        return False

def start_matelas_server():
    """Démarrer le serveur MATELAS si pas déjà en cours"""
    print("\\n🚀 Vérification du serveur MATELAS...")
    
    try:
        # Tester si le serveur local fonctionne
        response = requests.get("http://localhost:8091", timeout=3)
        if response.status_code == 200:
            print("✅ Serveur MATELAS déjà en cours")
            return True
    except:
        print("🔄 Démarrage du serveur MATELAS...")
        
        # Démarrer le serveur en arrière-plan
        server_path = Path("online_admin_interface/enhanced_admin_with_telemetry.py")
        if server_path.exists():
            try:
                # Changer vers le bon répertoire et démarrer le serveur
                os.chdir("online_admin_interface")
                subprocess.Popen([sys.executable, "enhanced_admin_with_telemetry.py"])
                os.chdir("..")  # Revenir au répertoire parent
                
                # Attendre que le serveur démarre
                for i in range(10):
                    try:
                        response = requests.get("http://localhost:8091", timeout=2)
                        if response.status_code == 200:
                            print("✅ Serveur MATELAS démarré avec succès")
                            return True
                    except:
                        time.sleep(1)
                        print(f"   Attente du démarrage... {i+1}/10")
                
                print("⚠️ Le serveur met plus de temps que prévu à démarrer")
                return True  # Continuer quand même
                
            except Exception as e:
                print(f"❌ Erreur lors du démarrage du serveur: {e}")
                return False
        else:
            print("❌ Fichier serveur non trouvé")
            return False

def start_ngrok_tunnel():
    """Démarrer le tunnel ngrok"""
    print("\\n🌐 Démarrage du tunnel ngrok...")
    
    try:
        # Démarrer ngrok en arrière-plan
        process = subprocess.Popen(
            ['ngrok', 'http', '8091', '--log=stdout'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Attendre que ngrok démarre et récupérer l'URL
        time.sleep(3)
        
        # Récupérer l'URL du tunnel via l'API locale de ngrok
        try:
            api_response = requests.get("http://127.0.0.1:4040/api/tunnels", timeout=5)
            if api_response.status_code == 200:
                data = api_response.json()
                tunnels = data.get('tunnels', [])
                
                if tunnels:
                    public_url = tunnels[0]['public_url']
                    print(f"✅ Tunnel ngrok créé avec succès!")
                    print(f"🌐 URL publique: {public_url}")
                    
                    return public_url, process
                else:
                    print("⚠️ Aucun tunnel trouvé dans l'API ngrok")
            else:
                print("⚠️ Impossible d'accéder à l'API ngrok")
                
        except Exception as e:
            print(f"⚠️ Erreur API ngrok: {e}")
        
        print("ℹ️  Consultez manuellement la sortie de ngrok pour l'URL")
        return None, process
        
    except Exception as e:
        print(f"❌ Erreur lors du démarrage de ngrok: {e}")
        return None, None

def test_public_access(public_url):
    """Tester l'accès public au serveur"""
    if not public_url:
        print("⚠️ URL publique non disponible, test manuel requis")
        return
        
    print(f"\\n🧪 Test de l'accès public à {public_url}...")
    
    try:
        # Tester l'API de mise à jour
        api_url = f"{public_url}/api/v1/check-updates"
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API de mise à jour accessible depuis Internet!")
            print(f"📦 Version disponible: {data.get('latest_version', 'Inconnue')}")
            
            # Tester l'interface admin
            admin_url = f"{public_url}/admin"
            admin_response = requests.get(admin_url, timeout=10)
            
            if admin_response.status_code in [200, 401]:  # 401 = auth requise (normal)
                print("✅ Interface d'administration accessible!")
                print(f"🔧 URL admin: {admin_url}")
                print("   Identifiants: admin / matelas2025")
            
        else:
            print(f"⚠️ Réponse inattendue: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")

def show_usage_instructions(public_url):
    """Afficher les instructions d'utilisation"""
    print("\\n📋 VOTRE SERVEUR EST MAINTENANT PUBLIC!")
    print("=" * 40)
    
    if public_url:
        print(f"🌐 URL publique: {public_url}")
        print(f"🔧 Interface admin: {public_url}/admin")
        print(f"📡 API clients: {public_url}/api/v1/check-updates")
        print(f"👥 Gestion clients: {public_url}/admin/clients")
        
    else:
        print("🌐 URL publique: Consultez la fenêtre ngrok")
        print("🔧 Interface admin: https://VOTRE_URL/admin")
        print("📡 API clients: https://VOTRE_URL/api/v1/check-updates")
    
    print("\\n🔑 IDENTIFIANTS ADMIN:")
    print("   Utilisateur: admin")
    print("   Mot de passe: matelas2025")
    print("   ⚠️ CHANGEZ CES IDENTIFIANTS EN PRODUCTION!")
    
    print("\\n💻 CONFIGURATION DES CLIENTS:")
    print("Pour que vos clients utilisent ce serveur, modifiez dans:")
    print("• app_gui.py (méthode check_for_updates_async)")
    print("• backend/auto_updater.py")
    
    if public_url:
        print(f'Remplacez "http://localhost:8091" par "{public_url}"')
    else:
        print('Remplacez "http://localhost:8091" par votre URL ngrok')
    
    print("\\n⚠️ LIMITATIONS NGROK GRATUIT:")
    print("• URL change à chaque redémarrage de ngrok")
    print("• Limite de 20 connexions/minute") 
    print("• Session expire après 8 heures")
    print("• Pour la production, utilisez un VPS")
    
    print("\\n🛑 ARRÊT DU SERVICE:")
    print("• Ctrl+C pour arrêter ngrok")
    print("• Le serveur local continuera de fonctionner")

def main():
    """Fonction principale"""
    print("🚀 DÉPLOIEMENT INTERNET RAPIDE - SERVEUR MATELAS")
    print("=" * 50)
    
    # 1. Vérifier/installer ngrok
    if not check_ngrok_installed():
        print("📦 ngrok n'est pas installé")
        if sys.platform == "darwin":  # macOS
            if not install_ngrok_mac():
                print("❌ Installation de ngrok échouée")
                return False
        else:
            print("ℹ️  Visitez https://ngrok.com/download pour installer ngrok")
            return False
    
    # 2. Configurer l'authentification
    try:
        # Tester si l'authtoken est déjà configuré
        result = subprocess.run(['ngrok', 'config', 'check'], capture_output=True)
        if result.returncode != 0:
            if not setup_ngrok_auth():
                return False
        else:
            print("✅ Authentification ngrok déjà configurée")
    except:
        if not setup_ngrok_auth():
            return False
    
    # 3. Démarrer le serveur MATELAS
    if not start_matelas_server():
        print("❌ Impossible de démarrer le serveur MATELAS")
        return False
    
    # 4. Créer le tunnel ngrok
    public_url, ngrok_process = start_ngrok_tunnel()
    
    # 5. Tester l'accès public
    test_public_access(public_url)
    
    # 6. Afficher les instructions
    show_usage_instructions(public_url)
    
    # 7. Maintenir le service actif
    print("\\n🔄 Service actif! Appuyez sur Ctrl+C pour arrêter...")
    try:
        while True:
            time.sleep(60)
            # Vérifier périodiquement que les services fonctionnent
            try:
                requests.get("http://localhost:8091", timeout=3)
            except:
                print("⚠️ Serveur local non accessible")
                break
                
    except KeyboardInterrupt:
        print("\\n🛑 Arrêt demandé...")
        if ngrok_process:
            ngrok_process.terminate()
        print("✅ Services arrêtés")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\\n🎉 Déploiement terminé avec succès!")
    else:
        print("\\n❌ Échec du déploiement")
        print("Consultez les erreurs ci-dessus et réessayez")