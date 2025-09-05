#!/usr/bin/env python3
"""
Script de démonstration du serveur de mise à jour
"""

if __name__ == "__main__":
    import sys
    sys.path.append('.')
    
    from backend.update_server import UpdateServer
    
    print("🚀 Démarrage du serveur de mise à jour de démonstration")
    print("📍 URL: http://localhost:8080")
    print("🛑 Arrêter avec Ctrl+C")
    
    server = UpdateServer("demo_update_storage")
    try:
        server.run(host="localhost", port=8080)
    except KeyboardInterrupt:
        print("\n🛑 Serveur arrêté")
