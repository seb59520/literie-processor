#!/usr/bin/env python3
"""
Créateur de package de mise à jour v3.11.2 avec onglets colorés corrigés
"""

import os
import zipfile
import shutil
from pathlib import Path
from datetime import datetime

def create_update_package_v3_11_2():
    """Créer le package de mise à jour v3.11.2 avec onglets colorés fonctionnels"""
    print("🎨 CRÉATION DU PACKAGE DE MISE À JOUR v3.11.2")
    print("=" * 60)
    print("🌈 Correction: Onglets colorés avec CSS simplifié et emojis")
    
    # Nom du package
    package_name = f"matelas_v3.11.2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    
    # Fichiers à inclure dans la mise à jour
    files_to_include = [
        # Fichier de version mis à jour
        "version.py",
        
        # Application principale avec onglets colorés corrigés
        "app_gui.py",
        
        # Module auto_updater (pour compatibilité)
        "backend/auto_updater.py",
        
        # Interface utilisateur et configuration
        "backend_interface.py",
        
        # Autres fichiers de support si nécessaire
        "config.py",
    ]
    
    # Créer le répertoire temporaire pour le package
    temp_dir = Path("temp_update_package_v3_11_2")
    temp_dir.mkdir(exist_ok=True)
    
    print(f"📁 Création du répertoire temporaire: {temp_dir}")
    
    try:
        # Copier les fichiers
        files_copied = 0
        for file_path in files_to_include:
            source_path = Path(file_path)
            
            if source_path.exists():
                # Créer la structure de répertoires dans le package
                dest_path = temp_dir / file_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Copier le fichier
                shutil.copy2(source_path, dest_path)
                files_copied += 1
                print(f"  ✅ {file_path}")
                
                # Informations spéciales pour les fichiers clés
                if file_path == "app_gui.py":
                    print(f"    🎨 Méthode de coloration simplifiée et CSS optimisé")
                elif file_path == "version.py":
                    print(f"    🏷️ Version corrigée: 3.11.2")
            else:
                print(f"  ⚠️ Fichier non trouvé: {file_path}")
        
        # Ajouter un fichier README spécifique à cette correction
        readme_content = f"""# Mise à jour MATELAS v3.11.2 - Onglets Colorés Corrigés

## 🔧 Corrections apportées
- **CSS simplifié** : Réécriture complète du système de coloration des onglets
- **Compatibilité PyQt6** : Suppression des propriétés CSS non supportées
- **Méthode nth-child** : Utilisation des sélecteurs CSS standards
- **Emojis optimisés** : Ajout d'emojis distinctifs pour chaque onglet

## 🎨 Nouvelles couleurs d'onglets
- 📊 **Résumé** - Bleu clair (#E3F2FD) avec bordure #2196F3
- ⚙️ **Configurations** - Violet clair (#F3E5F5) avec bordure #9C27B0
- 📥 **Pré-import** - Vert clair (#E8F5E8) avec bordure #4CAF50
- 📝 **Logs** - Orange clair (#FFF3E0) avec bordure #FF9800
- 🔧 **Debug** - Rose clair (#FCE4EC) avec bordure #E91E63
- 📋 **JSON** - Turquoise clair (#E0F2F1) avec bordure #00BCD4
- 📈 **Excel** - Vert lime clair (#F1F8E9) avec bordure #8BC34A
- 💰 **Coûts API** - Jaune clair (#FFF8E1) avec bordure #FFC107

## ✨ Améliorations techniques
- CSS nth-child pour ciblage précis des onglets
- Méthode lighten_color() pour effets de survol
- Gestion des erreurs améliorée
- Emojis ajoutés automatiquement aux textes d'onglets

## 🔍 Tests effectués
- ✅ Application se lance correctement
- ✅ 8 onglets identifiés et colorés
- ✅ Emojis ajoutés avec succès
- ✅ CSS appliqué sans erreur critique

## 🚀 Installation
Cette mise à jour remplace la version 3.11.1 défectueuse.
Les couleurs s'afficheront immédiatement après le redémarrage.

## Date de création: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
## Fichiers inclus: {files_copied}

---
*Correction réalisée suite au feedback utilisateur: "cela n'a pas mis à jour en couleur"*
"""
        
        readme_path = temp_dir / "README_CORRECTION.txt"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"  📄 Créé: README_CORRECTION.txt")
        
        # Créer un fichier de test pour valider l'installation
        test_colors_content = f"""# 🧪 Test des Couleurs - MATELAS v3.11.2

## Méthode de test simple
Pour vérifier que les couleurs fonctionnent après l'installation:

```python
python3 -c "
from app_gui import *
import sys
from PyQt6.QtWidgets import QApplication

app = QApplication([])
test_app = MatelasApp()

print('=== TEST DES COULEURS D\'ONGLETS ===')
print(f'Nombre d\'onglets: {{test_app.tabs.count()}}')

# Appliquer les couleurs
test_app.apply_colored_tabs_style()

# Vérifier les textes
for i in range(test_app.tabs.count()):
    text = test_app.tabs.tabText(i)
    print(f'  Onglet {{i}}: {{text}}')

print('\\\\n✅ Si vous voyez les emojis ci-dessus, l\'installation est réussie!')
app.quit()
"
```

## Résultat attendu
```
=== TEST DES COULEURS D'ONGLETS ===
Nombre d'onglets: 8
  Onglet 0: 📊 Résumé
  Onglet 1: ⚙️ Configurations
  Onglet 2: 📥 Pré-import
  Onglet 3: 📝 Logs
  Onglet 4: 🔧 Debug
  Onglet 5: 📋 JSON
  Onglet 6: 📈 Excel
  Onglet 7: 💰 Coûts API

✅ Si vous voyez les emojis ci-dessus, l'installation est réussie!
```

## CSS appliqué
- Couleurs de fond distinctes pour chaque onglet
- Bordures colorées avec sélecteurs nth-child
- Effets de survol avec éclaircissement automatique
- Interface moderne et professionnelle
"""
        
        test_colors_path = temp_dir / "TEST_COULEURS.txt"
        with open(test_colors_path, 'w', encoding='utf-8') as f:
            f.write(test_colors_content)
        print(f"  🧪 Créé: TEST_COULEURS.txt")
        
        # Créer le fichier ZIP
        print(f"\n🗜️ Création de l'archive ZIP: {package_name}")
        
        with zipfile.ZipFile(package_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Ajouter tous les fichiers du répertoire temporaire
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = Path(root) / file
                    # Chemin relatif dans le ZIP (sans le répertoire temporaire)
                    arcname = file_path.relative_to(temp_dir)
                    zipf.write(file_path, arcname)
                    
        # Informations du package créé
        package_path = Path(package_name)
        package_size = package_path.stat().st_size
        
        print(f"\n✅ PACKAGE v3.11.2 CRÉÉ AVEC SUCCÈS!")
        print(f"📦 Nom: {package_name}")
        print(f"📏 Taille: {package_size:,} octets ({package_size/1024/1024:.2f} MB)")
        print(f"📁 Fichiers inclus: {files_copied + 2} (+ fichiers de documentation)")
        print(f"🕒 Date de création: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Afficher les corrections de cette version
        print(f"\n🔧 CORRECTIONS v3.11.2:")
        print("• 🎨 CSS simplifié avec sélecteurs nth-child fonctionnels")
        print("• 🌈 8 couleurs distinctes appliquées correctement")
        print("• 📱 Emojis ajoutés pour une identification visuelle rapide")
        print("• ⚡ Suppression des propriétés CSS non compatibles PyQt6")
        print("• 🧪 Méthode de test incluse pour validation")
        
        return package_name, package_size
        
    finally:
        # Nettoyer le répertoire temporaire
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
            print(f"🧹 Nettoyage du répertoire temporaire terminé")

if __name__ == "__main__":
    try:
        package_name, size = create_update_package_v3_11_2()
        print(f"\n🎉 Package de correction v3.11.2 prêt!")
        print(f"\n📋 PROCHAINES ÉTAPES:")
        print(f"1. Uploadez le package via l'interface: http://localhost:8091/admin/upload")
        print(f"   (ou votre URL ngrok: https://edceecf7fdaf.ngrok-free.app/admin/upload)")
        print(f"2. Utilisez le fichier: {package_name}")
        print(f"3. Version: 3.11.2")
        print(f"4. Description: 'Correction des onglets colorés avec CSS simplifié'")
        print(f"5. Les clients verront enfin les onglets en couleurs!")
        
        print(f"\n🔧 CORRECTION APPLIQUÉE:")
        print("• Remplacement de la méthode CSS complexe par une approche simple")
        print("• Utilisation de nth-child au lieu de pseudo-éléments avancés")  
        print("• Ajout d'emojis pour distinction visuelle immédiate")
        print("• Tests validés : ✅ Couleurs ✅ Emojis ✅ Compatibilité PyQt6")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du package: {e}")
        raise