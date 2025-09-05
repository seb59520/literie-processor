#!/usr/bin/env python3
"""
Script de démarrage du serveur d'administration sur un port libre
"""

import socket
import subprocess
import sys
from pathlib import Path

def find_free_port(start_port=8090):
    """Trouve un port libre à partir de start_port"""
    for port in range(start_port, start_port + 10):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex(('localhost', port))
            if result != 0:  # Port libre
                return port
    raise Exception("Aucun port libre trouvé")

def start_admin_server():
    """Démarre le serveur d'administration"""
    print("🔍 Recherche d'un port libre...")
    
    try:
        free_port = find_free_port(8090)
        print(f"✅ Port libre trouvé: {free_port}")
        
        # Modifier temporairement le main.py pour utiliser le port libre
        main_py = Path(__file__).parent / "main.py"
        content = main_py.read_text(encoding='utf-8')
        
        # Remplacer le port dans uvicorn.run
        new_content = content.replace(
            'uvicorn.run(app, host="0.0.0.0", port=8080)',
            f'uvicorn.run(app, host="0.0.0.0", port={free_port})'
        )
        
        if new_content == content:
            # Si pas de uvicorn.run trouvé, l'ajouter à la fin
            new_content = content.replace(
                'if __name__ == "__main__":',
                f'''if __name__ == "__main__":
    import uvicorn'''
            ) + f'''
    
    uvicorn.run(app, host="0.0.0.0", port={free_port})'''
        
        main_py.write_text(new_content, encoding='utf-8')
        
        print(f"🚀 Démarrage du serveur d'administration MATELAS")
        print("=" * 55)
        print(f"🌐 Interface admin: http://localhost:{free_port}/admin")
        print(f"👤 Identifiants: admin / matelas2025")
        print(f"📦 API clients: http://localhost:{free_port}/api/v1/check-updates")
        print()
        print("💡 Pour arrêter le serveur: Ctrl+C")
        print()
        
        # Démarrer le serveur
        subprocess.run([sys.executable, str(main_py)], cwd=main_py.parent)
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    finally:
        # Restaurer le main.py original (si modifié)
        try:
            original_content = content.replace(
                f'uvicorn.run(app, host="0.0.0.0", port={free_port})',
                'uvicorn.run(app, host="0.0.0.0", port=8080)'
            )
            main_py.write_text(original_content, encoding='utf-8')
        except:
            pass
    
    return True

if __name__ == "__main__":
    print("🌐 SERVEUR D'ADMINISTRATION MATELAS")
    print("=" * 40)
    print("Détection automatique du port libre...")
    print()
    
    success = start_admin_server()
    
    if not success:
        print("\n❌ Impossible de démarrer le serveur")
        sys.exit(1)