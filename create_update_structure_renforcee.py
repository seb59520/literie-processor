#!/usr/bin/env python3
"""
Script de création du package de mise à jour pour la détection de structure renforcée des sommiers
Version: 1.0.0
Date: 2025-09-03
"""

import os
import shutil
import zipfile
from datetime import datetime
import json

def create_update_package():
    """Crée le package de mise à jour pour la détection de structure renforcée"""
    
    # Configuration du package
    update_version = "v1.1.0_structure_renforcee"
    package_name = f"MATELAS_UPDATE_{update_version}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Créer le répertoire de travail
    update_dir = f"update_packages/{package_name}"
    os.makedirs(update_dir, exist_ok=True)
    os.makedirs(f"{update_dir}/backend", exist_ok=True)
    
    print(f"Création du package de mise à jour: {package_name}")
    
    # Fichiers modifiés à inclure
    files_to_update = [
        {
            "source": "backend/sommier_utils.py",
            "target": "backend/sommier_utils.py",
            "description": "Ajout de la fonction detecter_structure_renforcee_sommier()"
        },
        {
            "source": "backend/pre_import_utils.py", 
            "target": "backend/pre_import_utils.py",
            "description": "Ajout de la fonction creer_pre_import_sommier() avec support structure renforcée"
        }
    ]
    
    # Copier les fichiers modifiés
    for file_info in files_to_update:
        source_path = file_info["source"]
        target_path = os.path.join(update_dir, file_info["target"])
        
        if os.path.exists(source_path):
            # Créer les répertoires parents si nécessaire
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            shutil.copy2(source_path, target_path)
            print(f"✓ Copié: {source_path} -> {target_path}")
        else:
            print(f"✗ Fichier non trouvé: {source_path}")
    
    # Créer le changelog
    changelog_content = f"""# CHANGELOG - Structure Renforcée Sommiers
## Version {update_version} - {datetime.now().strftime('%Y-%m-%d')}

### 🆕 Nouvelles Fonctionnalités

#### Détection Structure Renforcée Sommiers
- **Nouvelle fonction**: `detecter_structure_renforcee_sommier()`
  - Détecte "structure renforcée" dans les descriptions de sommiers
  - Insensible à la casse et aux accents
  - Supporte singulier et pluriel
  
- **Pré-import sommier amélioré**: `creer_pre_import_sommier()`
  - Génère automatiquement le champ `structure_renforces = "OUI"`
  - Crée le champ Excel `renforce_B550 = "X"` si structure renforcée détectée

### 🔧 Modifications Techniques

#### backend/sommier_utils.py
- Ajout de `detecter_structure_renforcee_sommier(description)`
- Tests intégrés pour validation de la détection

#### backend/pre_import_utils.py  
- Ajout de `creer_pre_import_sommier(configurations_sommier, donnees_client, mots_operation_trouves)`
- Support complet du workflow sommier avec structure renforcée

### 📝 Instructions d'Installation

1. **Sauvegarde recommandée**
   ```bash
   cp -r backend/ backend_backup_$(date +%Y%m%d)/
   ```

2. **Installation des fichiers**
   ```bash
   cp -r backend/* /path/to/MATELAS_FINAL/backend/
   ```

3. **Vérification**
   ```python
   from backend.sommier_utils import detecter_structure_renforcee_sommier
   from backend.pre_import_utils import creer_pre_import_sommier
   
   # Test de base
   result = detecter_structure_renforcee_sommier("SOMMIER STRUCTURE RENFORCÉE")
   assert result == "OUI"
   ```

### 🧪 Tests Inclus

Les fonctions incluent des tests automatisés pour:
- Détection avec/sans accents
- Variations de casse (majuscule/minuscule/mixte)
- Singulier et pluriel
- Génération correcte des champs pré-import

### 🔒 Compatibilité

- Compatible avec toutes les versions existantes
- Pas de breaking changes
- Ajout de fonctionnalités uniquement

### 🎯 Utilisation

```python
# Détection simple
from backend.sommier_utils import detecter_structure_renforcee_sommier
result = detecter_structure_renforcee_sommier("SOMMIER TAPISSIER STRUCTURE RENFORCÉE")
# Retourne: "OUI"

# Pré-import complet
from backend.pre_import_utils import creer_pre_import_sommier
configurations = [{{
    'description': 'SOMMIER STRUCTURE RENFORCÉE 160x200',
    'quantite': 1,
    'dimensions': {{'largeur': '160', 'longueur': '200'}}
}}]
donnees_client = {{'nom': 'Client Test', 'adresse': '123 Rue Test'}}
pre_import = creer_pre_import_sommier(configurations, donnees_client)
# Génère: renforce_B550: "X" automatiquement
```
"""
    
    # Écrire le changelog
    with open(os.path.join(update_dir, "CHANGELOG.md"), "w", encoding="utf-8") as f:
        f.write(changelog_content)
    
    # Créer les métadonnées du package
    metadata = {
        "version": update_version,
        "date": datetime.now().isoformat(),
        "description": "Ajout détection structure renforcée pour sommiers",
        "files_updated": files_to_update,
        "compatibility": {
            "min_version": "3.10.0",
            "breaking_changes": False
        },
        "features": [
            "Détection structure renforcée sommiers",
            "Pré-import sommier avec champ renforce_B550",
            "Support complet accents/casse/pluriel"
        ]
    }
    
    with open(os.path.join(update_dir, "update_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    # Script d'installation
    install_script = f"""#!/bin/bash
# Script d'installation - Structure Renforcée Sommiers
# Version: {update_version}

echo "🚀 Installation de la mise à jour Structure Renforcée Sommiers"
echo "Version: {update_version}"
echo "Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
echo

# Vérification de l'environnement
if [ ! -d "backend" ]; then
    echo "❌ Erreur: Répertoire 'backend' non trouvé"
    echo "Veuillez exécuter ce script depuis la racine du projet MATELAS_FINAL"
    exit 1
fi

# Sauvegarde recommandée
echo "📦 Création d'une sauvegarde..."
backup_dir="backup_before_structure_renforcee_$(date +%Y%m%d_%H%M%S)"
cp -r backend "$backup_dir"
echo "✓ Sauvegarde créée: $backup_dir"

# Installation des fichiers
echo
echo "📥 Installation des nouveaux fichiers..."
cp -v backend/sommier_utils.py backend/sommier_utils.py
cp -v backend/pre_import_utils.py backend/pre_import_utils.py
echo "✓ Fichiers installés"

# Test de validation
echo
echo "🧪 Test de validation..."
python3 -c "
try:
    from backend.sommier_utils import detecter_structure_renforcee_sommier
    from backend.pre_import_utils import creer_pre_import_sommier
    
    # Test basique
    result = detecter_structure_renforcee_sommier('SOMMIER STRUCTURE RENFORCÉE')
    assert result == 'OUI', f'Expected OUI, got {{result}}'
    
    result2 = detecter_structure_renforcee_sommier('SOMMIER STANDARD')
    assert result2 == 'NON', f'Expected NON, got {{result2}}'
    
    print('✓ Tests de validation réussis')
except Exception as e:
    print(f'❌ Erreur lors des tests: {{e}}')
    exit(1)
"

if [ $? -eq 0 ]; then
    echo
    echo "🎉 Mise à jour installée avec succès!"
    echo "📋 Nouvelles fonctionnalités disponibles:"
    echo "  - detecter_structure_renforcee_sommier()"
    echo "  - creer_pre_import_sommier() avec support structure renforcée"
    echo "  - Génération automatique du champ renforce_B550"
    echo
    echo "📚 Consultez CHANGELOG.md pour plus de détails"
else
    echo "❌ Erreur lors de l'installation"
    exit 1
fi
"""
    
    with open(os.path.join(update_dir, "install.sh"), "w", encoding="utf-8") as f:
        f.write(install_script)
    
    # Rendre le script exécutable
    os.chmod(os.path.join(update_dir, "install.sh"), 0o755)
    
    # Créer le fichier ZIP
    zip_path = f"{package_name}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(update_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, update_dir)
                zipf.write(file_path, arcname)
    
    print(f"\n✅ Package créé: {zip_path}")
    print(f"📁 Contenu temporaire: {update_dir}")
    
    # Résumé
    print(f"\n📋 RÉSUMÉ DU PACKAGE")
    print(f"Version: {update_version}")
    print(f"Fichier ZIP: {zip_path}")
    print(f"Taille: {os.path.getsize(zip_path)} bytes")
    print(f"\n📦 Contenu:")
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        for info in zipf.filelist:
            print(f"  - {info.filename}")
    
    return zip_path, update_dir

if __name__ == "__main__":
    try:
        zip_path, temp_dir = create_update_package()
        print(f"\n🎉 Package de mise à jour créé avec succès!")
        print(f"📥 Fichier prêt pour distribution: {zip_path}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()