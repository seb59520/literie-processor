#!/usr/bin/env python3
"""
Serveur de mise à jour sur le port 8080 (celui attendu par le client)
"""

import sys
from pathlib import Path

# Ajouter le backend au path
sys.path.insert(0, str(Path.cwd() / "backend"))

def main():
    print("🎯 MATELAS - Serveur de Mise à Jour (Port 8080)")
    print("=" * 60)
    
    from update_admin_interface import UpdateAdminInterface
    
    # Créer l'interface d'administration sur port 8080
    storage_path = "admin_update_storage"
    admin = UpdateAdminInterface(storage_path)
    
    print("🔧 Configuration:")
    print(f"   📁 Stockage: {storage_path}")
    print(f"   🌐 Interface: http://localhost:8080")
    print(f"   📱 API Client: http://localhost:8080/api/v1/")
    print("")
    print("🚀 Fonctionnalités:")
    print("   🔄 API de mise à jour pour clients")
    print("   📊 Interface d'administration web")
    print("   📦 Téléchargement de packages")
    print("")
    print("🛑 Arrêter avec Ctrl+C")
    print("=" * 60)
    
    try:
        # Démarrer sur port 8080 (celui attendu par votre client)
        admin.run(host="0.0.0.0", port=8080)
    except KeyboardInterrupt:
        print("\n🛑 Serveur arrêté")

if __name__ == "__main__":
    main()