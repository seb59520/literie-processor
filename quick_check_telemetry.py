#!/usr/bin/env python3
"""
Vérification rapide de l'état de la télémétrie
"""

import requests
import json
from pathlib import Path

def check_telemetry_data():
    """Vérifier les données de télémétrie"""
    print("🔍 VÉRIFICATION DE LA TÉLÉMÉTRIE")
    print("=" * 40)
    
    # Vérifier les fichiers de télémétrie
    telemetry_dir = Path("online_admin_interface/update_storage/telemetry")
    
    if telemetry_dir.exists():
        client_files = list(telemetry_dir.glob("client_*.json"))
        
        print(f"📊 Clients enregistrés: {len(client_files)}")
        
        for client_file in client_files:
            try:
                with open(client_file, 'r', encoding='utf-8') as f:
                    client_data = json.load(f)
                
                print(f"\n🖥️ Client {client_data['client_id'][:8]}...")
                print(f"   Poste: {client_data['system_info'].get('hostname', 'Inconnu')}")
                print(f"   Utilisateur: {client_data['system_info'].get('username', 'Inconnu')}")
                print(f"   OS: {client_data['system_info'].get('platform', 'Inconnu')}")
                print(f"   Version: {client_data.get('current_version', 'Inconnue')}")
                print(f"   Dernière connexion: {client_data.get('last_seen', 'Jamais')}")
                
            except Exception as e:
                print(f"❌ Erreur lecture {client_file}: {e}")
    else:
        print("❌ Dossier de télémétrie non trouvé")
        return False
    
    # Test de l'API
    print(f"\n🌐 Test de l'API sur http://localhost:8091...")
    
    try:
        response = requests.get("http://localhost:8091/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Serveur actif: {data.get('message', 'Unknown')}")
        else:
            print(f"⚠️ Serveur répond avec code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur")
    except Exception as e:
        print(f"❌ Erreur API: {e}")
    
    print(f"\n📱 Interface d'administration:")
    print(f"   Dashboard: http://localhost:8091/admin")
    print(f"   Gestion clients: http://localhost:8091/admin/clients")
    print(f"   Identifiants: admin / matelas2025")
    
    return True

if __name__ == "__main__":
    check_telemetry_data()