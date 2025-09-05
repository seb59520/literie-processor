#!/usr/bin/env python3
"""
Script de lancement de l'interface d'administration des mises à jour
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire backend au path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from update_admin_interface import UpdateAdminInterface

def main():
    print("🎯 MATELAS - Interface d'Administration des Mises à Jour")
    print("=" * 60)
    
    # Créer et lancer l'interface d'administration
    storage_path = "admin_update_storage"
    admin = UpdateAdminInterface(storage_path)
    
    print("🔧 Configuration:")
    print(f"   📁 Stockage: {storage_path}")
    print(f"   🌐 Interface: http://localhost:8081")
    print(f"   📱 API: http://localhost:8081/api/v1/")
    print("")
    print("🚀 Fonctionnalités disponibles:")
    print("   ✨ Création automatique de versions")
    print("   📤 Upload manuel de packages")
    print("   📊 Statistiques en temps réel")
    print("   🗑️ Suppression de versions")
    print("   📥 Téléchargement de packages")
    print("")
    print("🛑 Arrêter avec Ctrl+C")
    print("=" * 60)
    
    try:
        admin.run(host="0.0.0.0", port=8081)
    except KeyboardInterrupt:
        print("\n🛑 Interface d'administration arrêtée")

if __name__ == "__main__":
    main()