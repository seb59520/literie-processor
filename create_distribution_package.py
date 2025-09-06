#!/usr/bin/env python3
"""
Créer un package de distribution complet pour installation sur autre poste
"""

import zipfile
import json
from pathlib import Path
from datetime import datetime

def create_distribution_zip():
    """Créer une archive ZIP complète pour distribution"""
    
    base_path = Path.cwd()
    portable_path = base_path / "dist_portable_update_ready"
    
    # Nom du package de distribution
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dist_name = f"MATELAS_v3.11.12_PORTABLE_{timestamp}.zip"
    dist_path = base_path / dist_name
    
    print(f"📦 Création package de distribution: {dist_name}")
    print("=" * 60)
    
    if not portable_path.exists():
        print("❌ Répertoire portable non trouvé")
        return None
    
    # Créer l'archive
    with zipfile.ZipFile(dist_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
        
        # Ajouter tous les fichiers du répertoire portable
        files_count = 0
        total_size = 0
        
        for file_path in portable_path.rglob('*'):
            if file_path.is_file():
                # Chemin relatif dans l'archive
                arc_path = file_path.relative_to(portable_path)
                
                # Ajouter le fichier
                zipf.write(file_path, arc_path)
                
                files_count += 1
                total_size += file_path.stat().st_size
                
                print(f"   📁 {arc_path}")
    
    # Informations sur le package créé
    final_size = dist_path.stat().st_size
    compression_ratio = (1 - final_size / total_size) * 100 if total_size > 0 else 0
    
    print("\n" + "=" * 60)
    print("✅ PACKAGE DE DISTRIBUTION CRÉÉ!")
    print(f"📦 Fichier: {dist_name}")
    print(f"📊 Taille: {final_size / 1024 / 1024:.1f} MB")
    print(f"📁 Fichiers: {files_count}")
    print(f"🗜️ Compression: {compression_ratio:.1f}%")
    
    # Créer un fichier d'informations
    info = {
        "nom": dist_name,
        "version": "3.11.12",
        "type": "portable",
        "created": datetime.now().isoformat(),
        "taille_mb": round(final_size / 1024 / 1024, 1),
        "fichiers_count": files_count,
        "compression_pct": round(compression_ratio, 1),
        "installation": {
            "etapes": [
                "1. Extraire l'archive dans un dossier",
                "2. Ouvrir un terminal dans ce dossier",
                "3. Exécuter: python3 install.py",
                "4. Lancer: python3 app_gui.py"
            ],
            "prerequis": [
                "Python 3.8+",
                "Connexion Internet (pour dépendances)",
                "10 Go d'espace libre"
            ]
        },
        "nouvelles_fonctionnalites": [
            "Générateur de packages correctifs",
            "Suggestions automatiques de packages", 
            "Consolidation et upload VPS",
            "Interface améliorée avec protections",
            "Configuration serveur VPS intégrée"
        ]
    }
    
    info_file = base_path / f"MATELAS_v3.11.12_INFO.json"
    with open(info_file, 'w', encoding='utf-8') as f:
        json.dump(info, f, indent=2, ensure_ascii=False)
    
    print(f"📋 Informations: {info_file.name}")
    
    print("\n🚀 INSTRUCTIONS POUR L'UTILISATEUR:")
    print("=" * 60)
    print("1. 📤 Transférer le fichier ZIP sur l'autre poste")
    print("2. 📂 Extraire dans un dossier (ex: C:\\MATELAS\\ ou ~/MATELAS/)")
    print("3. 🔧 Ouvrir un terminal dans ce dossier")
    print("4. 📦 Exécuter: python3 install.py")
    print("5. 🚀 Lancer: python3 app_gui.py")
    print("\n💡 Tout est inclus dans le package!")
    
    return dist_path

if __name__ == "__main__":
    create_distribution_zip()