#!/usr/bin/env python3
"""
Script pour utiliser des services cloud pour compiler l'exécutable Windows
Utilise GitHub Actions ou d'autres services de CI/CD
"""

import os
import subprocess
import sys
from pathlib import Path

def create_github_repo_instructions():
    """Instructions pour utiliser GitHub Actions"""
    print("""
🌐 COMPILATION CLOUD AVEC GITHUB ACTIONS
========================================

📋 Étapes à suivre :

1️⃣ **Créer un repository GitHub**
   - Allez sur https://github.com
   - Créez un nouveau repository (public ou privé)
   - Uploadez tout votre code

2️⃣ **Activer GitHub Actions**
   - Le fichier .github/workflows/build-windows.yml est déjà créé
   - GitHub détectera automatiquement le workflow

3️⃣ **Lancer la compilation**
   - Allez dans l'onglet "Actions" de votre repo
   - Cliquez sur "Build Windows Executable" 
   - Cliquez "Run workflow" → "Run workflow"

4️⃣ **Récupérer l'exécutable**
   - Attendez ~10-15 minutes (compilation)
   - Téléchargez l'artifact "MatelasProcessor-Windows"
   - Décompressez → vous avez votre MatelasProcessor.exe

✅ **Avantages :**
   - Gratuit (2000 minutes/mois)
   - Automatique
   - Pas besoin de Windows
   - Compilation dans un environnement propre

📁 **Alternative pour release :**
   git tag v1.0.0
   git push origin v1.0.0
   → Créera automatiquement une release avec l'exe

🔗 **Autres services cloud :**
   - GitLab CI/CD (gratuit)
   - Azure DevOps (gratuit)  
   - CircleCI (gratuit avec limites)
""")

def create_docker_build():
    """Crée un Dockerfile pour compilation Windows"""
    dockerfile_content = """# Dockerfile pour compilation Windows avec Wine
FROM ubuntu:22.04

# Installer Wine et dépendances
RUN apt-get update && \\
    apt-get install -y wget software-properties-common && \\
    wget -nc https://dl.winehq.org/wine-builds/winehq.key && \\
    apt-key add winehq.key && \\
    add-apt-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ jammy main' && \\
    apt-get update && \\
    apt-get install -y winehq-stable python3 python3-pip

# Installer Python dans Wine
RUN wget https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe && \\
    wine python-3.11.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1

# Copier le code
COPY . /app
WORKDIR /app

# Installer les dépendances Python
RUN wine python -m pip install pyinstaller PyQt6 requests pandas openpyxl psutil

# Compiler l'exécutable
RUN wine python build_windows.py

# L'exécutable sera dans /app/dist/MatelasProcessor.exe
"""
    
    with open('Dockerfile.windows', 'w') as f:
        f.write(dockerfile_content)
    
    print("✅ Dockerfile.windows créé")
    print("💡 Utilisez: docker build -f Dockerfile.windows -t matelas-build .")
    print("💡 Puis: docker run --rm -v $(pwd)/dist:/app/dist matelas-build")

def check_mac_alternatives():
    """Vérifie les alternatives sur Mac"""
    print("""
🍎 ALTERNATIVES SUR MAC
======================

❌ **Ce qui NE marche PAS :**
   - PyInstaller direct (crée .app, pas .exe)
   - Cross-compilation native Python

✅ **Ce qui MARCHE :**
   1. **Machine virtuelle** (VMware/Parallels + Windows)
   2. **GitHub Actions** (gratuit, automatique) 
   3. **Docker + Wine** (complexe mais possible)
   4. **PC Windows** d'un ami/collègue

🎯 **Recommandation :**
   → Utilisez GitHub Actions (plus simple)
   → Ou VM si vous avez souvent besoin de compiler
""")

def main():
    print("🍎→🪟 COMPILATION WINDOWS DEPUIS MAC")
    print("=" * 50)
    
    if sys.platform == 'darwin':
        print("✅ Détection: Vous êtes sur macOS")
    else:
        print("⚠️ Ce script est prévu pour macOS")
    
    print("\n📋 Options disponibles :")
    print("1. GitHub Actions (recommandé)")
    print("2. Instructions Docker + Wine")
    print("3. Alternatives générales")
    
    choice = input("\nChoisissez (1-3) : ").strip()
    
    if choice == "1":
        create_github_repo_instructions()
    elif choice == "2":
        create_docker_build()
    elif choice == "3":
        check_mac_alternatives()
    else:
        print("🤔 Choix invalide, affichage de toutes les options...")
        create_github_repo_instructions()
        create_docker_build() 
        check_mac_alternatives()

if __name__ == "__main__":
    main()