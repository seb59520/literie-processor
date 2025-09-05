#!/usr/bin/env python3
"""
Serveur de mise à jour correct qui respecte l'ordre des versions
"""

from flask import Flask, jsonify, send_file
import json
from pathlib import Path

app = Flask(__name__)

def load_manifest():
    """Charger le manifest avec l'ordre correct"""
    manifest_path = Path("admin_update_storage/metadata/manifest.json")
    if manifest_path.exists():
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        return manifest
    return {"versions": [], "statistics": {}}

@app.route('/api/v1/versions')
def get_versions():
    """API versions - ordre correct (plus récente en premier)"""
    try:
        manifest = load_manifest()
        versions = manifest.get("versions", [])
        
        # Trier par version (plus récente en premier)
        def version_key(v):
            return tuple(map(int, v["version"].split('.')))
        
        sorted_versions = sorted(versions, key=version_key, reverse=True)
        
        return jsonify({
            "versions": sorted_versions,
            "total": len(sorted_versions)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/download/<version>')
def download_version(version):
    """Télécharger une version"""
    try:
        manifest = load_manifest()
        versions = manifest.get("versions", [])
        
        # Trouver la version demandée
        for v in versions:
            if v["version"] == version:
                file_path = Path("admin_update_storage/versions") / v["filename"]
                if file_path.exists():
                    return send_file(str(file_path), as_attachment=True)
                else:
                    return jsonify({"error": f"Fichier non trouvé: {v['filename']}"}), 404
        
        return jsonify({"error": f"Version non trouvée: {version}"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/check-updates')
def check_updates():
    """Endpoint utilisé par votre client pour vérifier les mises à jour"""
    from flask import request
    
    try:
        current_version = request.args.get('current_version')
        if not current_version:
            return jsonify({"error": "current_version parameter required"}), 400
        
        manifest = load_manifest()
        versions = manifest.get("versions", [])
        
        if not versions:
            return jsonify({
                "update_available": False,
                "message": "Aucune version disponible"
            })
        
        # Trier par version (plus récente en premier)
        def version_key(v):
            return tuple(map(int, v["version"].split('.')))
        
        sorted_versions = sorted(versions, key=version_key, reverse=True)
        latest = sorted_versions[0]  # Version la plus récente
        
        # Comparaison des versions
        current_tuple = version_key({"version": current_version})
        latest_tuple = version_key(latest)
        
        update_available = latest_tuple > current_tuple
        
        if update_available:
            return jsonify({
                "update_available": True,
                "latest_version": latest["version"],
                "current_version": current_version,
                "download_url": f"http://localhost:8080/api/v1/download/{latest['version']}",
                "size": latest["size"],
                "description": latest["description"],
                "changelog": latest.get("changelog", ""),
                "message": f"Mise à jour disponible: {current_version} → {latest['version']}"
            })
        else:
            return jsonify({
                "update_available": False,
                "latest_version": latest["version"],
                "current_version": current_version,
                "message": f"Client à jour (version {current_version})"
            })
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/stats')
def get_stats():
    """Statistiques pour l'interface admin"""
    try:
        manifest = load_manifest()
        stats = manifest.get("statistics", {})
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    """Page d'accueil"""
    manifest = load_manifest()
    versions = manifest.get("versions", [])
    
    # Trier par version (plus récente en premier)
    def version_key(v):
        return tuple(map(int, v["version"].split('.')))
    
    sorted_versions = sorted(versions, key=version_key, reverse=True)
    
    html = f"""
    <h1>🔄 Serveur de Mise à Jour</h1>
    <p><strong>Port:</strong> 8080 (pour clients)</p>
    <p><strong>Versions disponibles:</strong> {len(sorted_versions)}</p>
    <ul>
    """
    
    for v in sorted_versions:
        html += f"<li><strong>v{v['version']}</strong> - {v['description']}</li>"
    
    html += """
    </ul>
    <h2>APIs:</h2>
    <ul>
        <li><a href="/api/v1/versions">/api/v1/versions</a> - Liste des versions</li>
        <li><a href="/api/admin/stats">/api/admin/stats</a> - Statistiques</li>
    </ul>
    """
    
    return html

if __name__ == "__main__":
    print("🔄 SERVEUR DE MISE À JOUR CORRECT")
    print("=" * 50)
    print("🌐 URL: http://localhost:8080")
    print("📱 API Client: /api/v1/versions")
    print("📥 Téléchargement: /api/v1/download/<version>")
    print("🛑 Arrêter avec Ctrl+C")
    print("")
    
    # Afficher les versions au démarrage
    manifest = load_manifest()
    versions = manifest.get("versions", [])
    
    if versions:
        def version_key(v):
            return tuple(map(int, v["version"].split('.')))
        
        sorted_versions = sorted(versions, key=version_key, reverse=True)
        
        print("📦 Versions chargées (ordre correct):")
        for i, v in enumerate(sorted_versions):
            print(f"  {i+1}. v{v['version']} - {v['description']}")
    else:
        print("❌ Aucune version trouvée")
    
    print("")
    
    app.run(host='0.0.0.0', port=8080, debug=False)