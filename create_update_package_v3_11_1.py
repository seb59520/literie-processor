#!/usr/bin/env python3
"""
Créateur de package de mise à jour v3.11.1 avec onglets colorés
"""

import os
import zipfile
import shutil
from pathlib import Path
from datetime import datetime

def create_update_package_v3_11_1():
    """Créer le package de mise à jour v3.11.1 avec onglets colorés"""
    print("🎨 CRÉATION DU PACKAGE DE MISE À JOUR v3.11.1")
    print("=" * 60)
    print("🌈 Nouvelle fonctionnalité: Onglets colorés et interface modernisée")
    
    # Nom du package
    package_name = f"matelas_v3.11.1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    
    # Fichiers à inclure dans la mise à jour
    files_to_include = [
        # Fichier de version mis à jour
        "version.py",
        
        # Application principale avec onglets colorés
        "app_gui.py",
        
        # Module auto_updater (pour compatibilité)
        "backend/auto_updater.py",
        
        # Interface utilisateur et configuration
        "backend_interface.py",
        
        # Autres fichiers de support si nécessaire
        "config.py",
    ]
    
    # Créer le répertoire temporaire pour le package
    temp_dir = Path("temp_update_package_v3_11_1")
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
                    print(f"    🎨 Contient les nouveaux styles d'onglets colorés")
                elif file_path == "version.py":
                    print(f"    🏷️ Version mise à jour: 3.11.1")
            else:
                print(f"  ⚠️ Fichier non trouvé: {file_path}")
        
        # Ajouter un fichier README spécifique à cette mise à jour
        readme_content = f"""# Mise à jour MATELAS v3.11.1 - Onglets Colorés

## 🎨 Nouvelles fonctionnalités visuelles
- **Onglets colorés** : Chaque onglet a maintenant sa propre couleur distinctive
- **Design moderne** : Dégradés et effets visuels améliorés
- **Navigation intuitive** : Identification rapide des sections par couleur

## 🌈 Palette de couleurs
- 🔵 **Résumé** - Bleu clair (vue d'ensemble)
- 🟣 **Configurations** - Violet clair (paramètres)
- 🟢 **Pré-import** - Vert clair (préparation)
- 🟠 **Logs** - Orange clair (monitoring)
- 🩷 **Debug** - Rose clair (débogage)
- 🟡 **JSON/Excel** - Couleurs spécialisées

## ✨ Améliorations techniques
- Styles CSS modernes avec dégradés Qt
- Méthodes utilitaires pour manipulation des couleurs
- Performance optimisée sans impact sur la vitesse
- Effets de survol et sélection fluides

## 📅 Installation
Cette mise à jour sera installée automatiquement par le système de mise à jour.
Les nouveaux styles s'appliqueront immédiatement après le redémarrage.

## Date de création: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
## Fichiers inclus: {files_copied}

---
*Mise à jour créée automatiquement par le système de packaging MATELAS*
"""
        
        readme_path = temp_dir / "README_UPDATE.txt"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"  📄 Créé: README_UPDATE.txt")
        
        # Créer un fichier de démonstration des couleurs
        color_demo_content = f"""# 🎨 Démonstration des Couleurs - MATELAS v3.11.1

## Aperçu des nouvelles couleurs d'onglets

### 🔵 Onglet Résumé
- **Couleur primaire**: Bleu clair (#E3F2FD)
- **Usage**: Vue d'ensemble des résultats de traitement
- **Style**: Professionnel et apaisant

### 🟣 Onglet Configurations  
- **Couleur primaire**: Violet clair (#F3E5F5)
- **Usage**: Paramètres et réglages de l'application
- **Style**: Distinctif pour les paramètres importants

### 🟢 Onglet Pré-import
- **Couleur primaire**: Vert clair (#E8F5E8)
- **Usage**: Préparation et validation des données
- **Style**: Couleur positive pour la préparation

### 🟠 Onglet Logs
- **Couleur primaire**: Orange clair (#FFF3E0)
- **Usage**: Surveillance et monitoring du système
- **Style**: Attention et vigilance

### 🩷 Onglet Debug
- **Couleur primaire**: Rose clair (#FCE4EC)
- **Usage**: Débogage et diagnostic technique
- **Style**: Doux mais distinct pour les développeurs

### 🔷 Onglet JSON
- **Couleur primaire**: Turquoise clair (#E0F2F1)
- **Usage**: Affichage des données structurées
- **Style**: Tech et moderne

### 🟡 Onglet Excel
- **Couleur primaire**: Vert lime clair (#F1F8E9)
- **Usage**: Résultats et exports Excel
- **Style**: Couleur productive et positive

## Effets visuels
- **Survol**: Éclaircissement automatique de 10%
- **Sélection**: Bordure colorée de 3px
- **Dégradés**: Transition fluide de clair à foncé
- **Animation**: Transitions CSS fluides

Profitez de cette nouvelle interface colorée et moderne !
"""
        
        color_demo_path = temp_dir / "COULEURS_DEMO.txt"
        with open(color_demo_path, 'w', encoding='utf-8') as f:
            f.write(color_demo_content)
        print(f"  🌈 Créé: COULEURS_DEMO.txt")
        
        # Créer le fichier ZIP
        print(f"\\n🗜️ Création de l'archive ZIP: {package_name}")
        
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
        
        print(f"\\n✅ PACKAGE v3.11.1 CRÉÉ AVEC SUCCÈS!")
        print(f"📦 Nom: {package_name}")
        print(f"📏 Taille: {package_size:,} octets ({package_size/1024/1024:.2f} MB)")
        print(f"📁 Fichiers inclus: {files_copied + 2} (+ fichiers de documentation)")
        print(f"🕒 Date de création: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Afficher les améliorations de cette version
        print(f"\\n🎨 AMÉLIORATIONS v3.11.1:")
        print("• 🌈 Onglets colorés avec palette harmonieuse")
        print("• ✨ Dégradés CSS modernes et effets de survol")
        print("• 🔧 Méthodes utilitaires pour manipulation des couleurs")
        print("• 💫 Interface plus moderne et professionnelle")
        print("• 🎯 Navigation intuitive par codes couleur")
        
        return package_name, package_size
        
    finally:
        # Nettoyer le répertoire temporaire
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
            print(f"🧹 Nettoyage du répertoire temporaire terminé")

if __name__ == "__main__":
    try:
        package_name, size = create_update_package_v3_11_1()
        print(f"\\n🎉 Package de mise à jour v3.11.1 prêt!")
        print(f"\\n📋 PROCHAINES ÉTAPES:")
        print(f"1. Uploadez le package via l'interface: http://localhost:8091/admin/upload")
        print(f"   (ou votre URL ngrok: https://edceecf7fdaf.ngrok-free.app/admin/upload)")
        print(f"2. Utilisez le fichier: {package_name}")
        print(f"3. Version: 3.11.1")
        print(f"4. Description: 'Interface modernisée avec onglets colorés'")
        print(f"5. Les clients verront les nouveaux onglets colorés après mise à jour!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du package: {e}")
        raise