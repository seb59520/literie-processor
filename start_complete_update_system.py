#!/usr/bin/env python3
"""
Lance le système complet de mise à jour :
- Serveur de mise à jour (API) sur le port 8080
- Interface d'administration sur le port 8081
"""

import sys
import os
import threading
import time
from pathlib import Path

# Ajouter le répertoire backend au path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

def start_update_server():
    """Lance le serveur de mise à jour"""
    from update_server import UpdateServer
    server = UpdateServer("shared_update_storage")
    server.run(host="localhost", port=8080)

def start_admin_interface():
    """Lance l'interface d'administration"""
    from update_admin_interface import UpdateAdminInterface
    admin = UpdateAdminInterface("shared_update_storage")
    admin.run(host="localhost", port=8081)

def main():
    print("🎯 MATELAS - Système Complet de Mise à Jour")
    print("=" * 70)
    print("🚀 Démarrage des services...")
    print("")
    
    print("📡 Service 1: Serveur API de mise à jour")
    print("   🌐 URL: http://localhost:8080")
    print("   📋 API: /api/v1/check-updates, /api/v1/download/{version}")
    print("   🎯 Utilisation: Pour les clients de l'application")
    print("")
    
    print("🖥️ Service 2: Interface d'administration")  
    print("   🌐 URL: http://localhost:8081")
    print("   📊 Dashboard avec statistiques")
    print("   📤 Upload et gestion des versions")
    print("   🎯 Utilisation: Pour les administrateurs")
    print("")
    
    print("📁 Stockage partagé: shared_update_storage/")
    print("🛑 Arrêter avec Ctrl+C")
    print("=" * 70)
    
    try:
        # Démarrer le serveur de mise à jour dans un thread
        update_thread = threading.Thread(target=start_update_server, daemon=True)
        update_thread.start()
        
        # Attendre un peu que le serveur démarre
        time.sleep(2)
        print("✅ Serveur API démarré sur http://localhost:8080")
        
        # Démarrer l'interface d'administration dans le thread principal
        print("✅ Interface admin démarrée sur http://localhost:8081")
        print("")
        print("🎉 Système complet opérationnel !")
        print("👉 Ouvrez http://localhost:8081 pour administrer")
        
        start_admin_interface()
        
    except KeyboardInterrupt:
        print("\n🛑 Système de mise à jour arrêté")

if __name__ == "__main__":
    main()