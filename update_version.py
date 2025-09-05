#!/usr/bin/env python3
"""
Script de mise à jour automatique de la version de l'application Matelas Processor
"""

import re
import os
from datetime import datetime

VERSION_FILE = "version.py"

def update_version_file(new_version, new_date, new_build, changelog_entry):
    """Met à jour le fichier version.py avec les nouvelles informations"""
    try:
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        # Remplacement version, date, build
        content = re.sub(r'VERSION = ".*?"', f'VERSION = "{new_version}"', content)
        content = re.sub(r'BUILD_DATE = ".*?"', f'BUILD_DATE = "{new_date}"', content)
        content = re.sub(r'BUILD_NUMBER = ".*?"', f'BUILD_NUMBER = "{new_build}"', content)

        # Ajout du changelog en tête
        changelog_entry = changelog_entry.strip() + "\n\n"
        
        # Rechercher le début du changelog avec plusieurs patterns
        patterns_to_try = [
            # Pattern principal
            (r'(def get_changelog\(\):\s+"""Retourne le changelog de l\'application"""\s+return """\n# Changelog - Matelas Processor\n)', r'\1' + changelog_entry),
            # Pattern alternatif 1
            (r'(return """\n# Changelog - Matelas Processor\n)', r'\1' + changelog_entry),
            # Pattern alternatif 2
            (r'(def get_changelog\(\):\s+"""Retourne le changelog de l\'application"""\s+return """\n)', r'\1' + changelog_entry),
            # Pattern alternatif 3
            (r'(return """\n)', r'\1' + changelog_entry),
        ]
        
        changelog_updated = False
        for pattern, replacement in patterns_to_try:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content, count=1)
                changelog_updated = True
                print(f"✅ Changelog mis à jour avec le pattern: {pattern[:50]}...")
                break
        
        if not changelog_updated:
            print("⚠️ Impossible de trouver le bon endroit pour insérer le changelog")
            print("📋 Patterns essayés:")
            for pattern, _ in patterns_to_try:
                print(f"  - {pattern[:50]}...")
            return False

        with open(VERSION_FILE, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✅ Fichier {VERSION_FILE} mis à jour avec la version {new_version}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {e}")
        return False

def get_current_version():
    """Récupère la version actuelle depuis le fichier version.py"""
    try:
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        version_match = re.search(r'VERSION = "(.*?)"', content)
        if version_match:
            return version_match.group(1)
        return "Inconnue"
    except:
        return "Erreur"

def interactive_update():
    """Interface interactive pour la mise à jour de version"""
    print("=== Mise à jour automatique de la version ===")
    print(f"Version actuelle: {get_current_version()}")
    print()
    
    new_version = input("Nouvelle version (ex: 2.3.0) : ").strip()
    if not new_version:
        print("❌ Version requise")
        return False
    
    today = datetime.today().strftime("%Y-%m-%d")
    new_date = input(f"Date du build [{today}] : ").strip() or today
    new_build = input(f"Numéro de build [{new_date.replace('-', '')}] : ").strip() or new_date.replace("-", "")
    
    print("\nEntrée du changelog (finir par une ligne vide) :")
    changelog_lines = []
    while True:
        line = input()
        if not line.strip():
            break
        changelog_lines.append(line)
    
    if not changelog_lines:
        changelog_lines = ["- Mise à jour de version"]
    
    changelog_entry = f"## Version {new_version} ({new_date})\n" + "\n".join(changelog_lines)
    
    return update_version_file(new_version, new_date, new_build, changelog_entry)

if __name__ == "__main__":
    interactive_update() 