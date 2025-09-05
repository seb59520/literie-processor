#!/usr/bin/env python3
"""
Créateur de package v3.11.4 avec indicateur de mise à jour bien visible
"""

import os
import zipfile
import shutil
from pathlib import Path
from datetime import datetime

def create_update_package_v3_11_4():
    """Créer le package v3.11.4 avec indicateur de mise à jour redesigné"""
    print("🔍 CRÉATION DU PACKAGE v3.11.4 - INDICATEUR VISIBLE")
    print("=" * 55)
    print("🎯 Correction: Indicateur de mise à jour avec style moderne")
    
    # Nom du package
    package_name = f"matelas_v3.11.4_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    
    # Fichiers à inclure
    files_to_include = [
        "version.py",
        "app_gui.py",
        "backend/auto_updater.py",
        "backend_interface.py",
        "config.py",
    ]
    
    # Créer le répertoire temporaire
    temp_dir = Path("temp_update_v3_11_4")
    temp_dir.mkdir(exist_ok=True)
    
    try:
        # Copier les fichiers
        files_copied = 0
        for file_path in files_to_include:
            source_path = Path(file_path)
            
            if source_path.exists():
                dest_path = temp_dir / file_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_path, dest_path)
                files_copied += 1
                print(f"  ✅ {file_path}")
        
        # Créer un README
        readme_content = f"""# Mise à jour MATELAS v3.11.4 - Indicateur de mise à jour visible

## 🔍 Problème résolu
L'indicateur de mise à jour n'était pas visible dans la barre de statut.

## ✨ Améliorations apportées
- **Indicateur coloré** : Fond coloré avec bordure pour une meilleure visibilité
- **Emojis distinctifs** :
  - 🔄 En cours de vérification (bleu)
  - ✅ Version à jour (vert)
  - 🆕 Mise à jour disponible (rouge)
  - ⚠️ Erreur de vérification (gris)
  
## 🎨 Nouveau design
- **Fond coloré** : Chaque état a sa propre couleur de fond
- **Bordures** : Contour foncé pour délimiter l'indicateur
- **Padding augmenté** : Plus d'espace pour une meilleure lisibilité
- **Texte blanc** : Contraste élevé sur fond coloré

## 🚀 États possibles
1. **🔄 Mise à jour: Vérification...** (bleu) - Pendant la vérification
2. **✅ Mise à jour: v3.11.4** (vert) - Version à jour
3. **🆕 Mise à jour: 3.11.3 → 3.11.4** (rouge) - Nouvelle version disponible
4. **⚠️ Mise à jour: Erreur** (gris) - Problème de connexion

## 📍 Position
L'indicateur apparaît dans la barre de statut en bas à droite de l'application.

Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        readme_path = temp_dir / "README_INDICATEUR.txt"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"  📄 Créé: README_INDICATEUR.txt")
        
        # Créer le ZIP
        with zipfile.ZipFile(package_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(temp_dir)
                    zipf.write(file_path, arcname)
        
        # Statistiques
        package_size = Path(package_name).stat().st_size
        
        print(f"\n✅ PACKAGE v3.11.4 CRÉÉ!")
        print(f"📦 Nom: {package_name}")
        print(f"📏 Taille: {package_size:,} octets ({package_size/1024/1024:.2f} MB)")
        print(f"📁 Fichiers: {files_copied + 1}")
        
        print(f"\n🔍 AMÉLIORATIONS:")
        print("• 🎨 Indicateur avec fond coloré et bordure")
        print("• 📍 Position fixe dans la barre de statut")
        print("• 🔄 Emojis pour identification rapide")
        print("• ✨ Meilleur contraste et visibilité")
        
        return package_name, package_size
        
    finally:
        # Nettoyer
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    try:
        package_name, size = create_update_package_v3_11_4()
        print(f"\n🎯 PROCHAINES ÉTAPES:")
        print("1. Uploadez ce package sur votre serveur admin")
        print("2. Votre client v3.11.3 devrait afficher '🆕 Mise à jour: 3.11.3 → 3.11.4' en ROUGE")
        print("3. L'indicateur sera maintenant bien visible dans la barre de statut!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")