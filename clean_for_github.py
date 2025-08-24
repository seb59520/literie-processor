#!/usr/bin/env python3
"""
Script pour nettoyer les données sensibles avant de pousser sur GitHub
"""

import json
import shutil
import os
from pathlib import Path

def backup_config():
    """Sauvegarde la configuration actuelle"""
    config_file = Path('matelas_config.json')
    if config_file.exists():
        backup_file = Path('matelas_config.json.backup')
        shutil.copy(config_file, backup_file)
        print(f"[OK] Sauvegarde créée: {backup_file}")
        return True
    return False

def create_template_config():
    """Crée un template de configuration sans clés API"""
    config_file = Path('matelas_config.json')
    template_file = Path('matelas_config.json.template')
    
    if not config_file.exists():
        print("[INFO] matelas_config.json non trouvé")
        return False
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Nettoyer les clés API
        sensitive_keys = []
        for key, value in config.items():
            if 'api_key' in key.lower() and value:
                if value != "VOTRE_CLE_API_ICI" and len(value) > 10:
                    sensitive_keys.append(key)
                    config[key] = "VOTRE_CLE_API_ICI"
        
        # Sauvegarder le template
        with open(template_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        if sensitive_keys:
            print(f"[OK] Template créé avec {len(sensitive_keys)} clés masquées")
            print(f"Clés masquées: {sensitive_keys}")
        else:
            print("[OK] Template créé (pas de clés sensibles détectées)")
        
        return True
        
    except Exception as e:
        print(f"[ERREUR] Impossible de créer le template: {e}")
        return False

def update_gitignore():
    """Met à jour .gitignore pour exclure les fichiers sensibles"""
    gitignore_file = Path('.gitignore')
    
    sensitive_patterns = [
        "# Fichiers de configuration avec clés API",
        "matelas_config.json.backup",
        "*_private.json",
        "*_secret.json",
        "*.key",
        "*.pem"
    ]
    
    if gitignore_file.exists():
        with open(gitignore_file, 'r') as f:
            content = f.read()
        
        # Ajouter les patterns manquants
        added = []
        for pattern in sensitive_patterns:
            if pattern not in content:
                content += f"\n{pattern}"
                added.append(pattern)
        
        if added:
            with open(gitignore_file, 'w') as f:
                f.write(content)
            print(f"[OK] .gitignore mis à jour avec {len(added)} patterns")
        else:
            print("[OK] .gitignore déjà à jour")
    else:
        # Créer .gitignore
        with open(gitignore_file, 'w') as f:
            f.write("\n".join(sensitive_patterns))
        print("[OK] .gitignore créé")

def clean_temporary_files():
    """Supprime les fichiers temporaires"""
    temp_patterns = [
        "*.tmp",
        "*.temp", 
        "*_test.html",
        "rapport_*.html",
        "test_*.json"
    ]
    
    removed = []
    for pattern in temp_patterns:
        for file in Path('.').glob(pattern):
            if file.is_file():
                file.unlink()
                removed.append(str(file))
    
    if removed:
        print(f"[OK] {len(removed)} fichiers temporaires supprimés")
    else:
        print("[OK] Pas de fichiers temporaires à supprimer")

def check_large_files():
    """Vérifie la présence de gros fichiers"""
    large_files = []
    max_size = 100 * 1024 * 1024  # 100 MB
    
    for file in Path('.').rglob('*'):
        if file.is_file() and not any(skip in str(file) for skip in ['.git', '__pycache__', 'node_modules']):
            try:
                if file.stat().st_size > max_size:
                    large_files.append((str(file), file.stat().st_size))
            except:
                continue
    
    if large_files:
        print(f"[!] {len(large_files)} gros fichiers détectés:")
        for file, size in large_files:
            print(f"  - {file}: {size / (1024*1024):.1f} MB")
        print("Considérez utiliser Git LFS pour ces fichiers")
    else:
        print("[OK] Pas de gros fichiers détectés")

def create_readme_template():
    """Met à jour le README avec des informations génériques"""
    readme_file = Path('README.md')
    if readme_file.exists():
        with open(readme_file, 'r') as f:
            content = f.read()
        
        # Remplacer les références sensibles
        replacements = [
            ('[votre-username]', 'votre-username'),
            ('sebastien', '[votre-nom]'),
            ('SEBASTIEN', '[VOTRE-NOM]'),
        ]
        
        updated = False
        for old, new in replacements:
            if old in content and old != new:
                content = content.replace(old, new)
                updated = True
        
        if updated:
            with open(readme_file, 'w') as f:
                f.write(content)
            print("[OK] README.md mis à jour")
        else:
            print("[OK] README.md déjà générique")

def main():
    """Fonction principale de nettoyage"""
    print("="*50)
    print("NETTOYAGE POUR GITHUB")
    print("="*50)
    
    steps = [
        ("Sauvegarde configuration", backup_config),
        ("Création template config", create_template_config),
        ("Mise à jour .gitignore", update_gitignore),
        ("Suppression fichiers temporaires", clean_temporary_files),
        ("Vérification gros fichiers", check_large_files),
        ("Généralisation README", create_readme_template),
    ]
    
    for description, func in steps:
        print(f"\n--- {description} ---")
        try:
            func()
        except Exception as e:
            print(f"[ERREUR] {description}: {e}")
    
    print("\n" + "="*50)
    print("NETTOYAGE TERMINÉ")
    print("="*50)
    print("\n[OK] Votre projet est prêt pour GitHub!")
    print("\nFichiers importants créés:")
    print("- matelas_config.json.template (template de configuration)")
    print("- matelas_config.json.backup (sauvegarde de votre config)")
    print("- .gitignore mis à jour")
    print("\nProchaines étapes:")
    print("1. Vérifiez que vos clés API sont bien masquées")
    print("2. Testez avec: git status")
    print("3. Poussez avec: python git_setup.py")

if __name__ == "__main__":
    main()