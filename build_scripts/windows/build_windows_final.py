#!/usr/bin/env python3
"""
Script de compilation PyInstaller pour Windows
Optimisé pour créer un exécutable Windows robuste
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def clean_build_dirs():
    """Nettoie les dossiers de build et dist"""
    print("🧹 Nettoyage des dossiers de build...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['*.spec']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  ✓ Supprimé: {dir_name}")
    
    for pattern in files_to_clean:
        for file_path in Path('.').glob(pattern):
            file_path.unlink()
            print(f"  ✓ Supprimé: {file_path}")

def get_backend_modules():
    """Liste tous les modules backend nécessaires"""
    backend_modules = [
        # Modules principaux
        'backend.main',
        'backend.llm_provider',
        'backend.backend_interface',
        
        # Modules utils
        'backend.date_utils',
        'backend.pre_import_utils',
        'backend.excel_import_utils',
        'backend.sommier_utils',
        'backend.client_utils',
        'backend.article_utils',
        'backend.matelas_utils',
        'backend.operation_utils',
        'backend.dimensions_utils',
        'backend.hauteur_utils',
        'backend.fermete_utils',
        'backend.poignees_utils',
        'backend.housse_utils',
        'backend.matiere_housse_utils',
        'backend.decoupe_noyau_utils',
        'backend.mapping_manager',
        'backend.secure_storage',
        'backend.excel_sommier_import_utils',
        'backend.sommier_analytics_utils',
        'backend.dimensions_sommiers',
        'backend.asset_utils',
        
        # Modules latex
        'backend.latex_renforce_utils',
        'backend.latex_renforce_longueur_utils',
        'backend.latex_naturel_utils',
        'backend.latex_naturel_longueur_housse_utils',
        'backend.latex_mixte7zones_utils',
        'backend.latex_mixte7zones_longueur_housse_utils',
        'backend.latex_naturel_referentiel',
        'backend.latex_mixte7zones_referentiel',
        
        # Modules mousse
        'backend.mousse_visco_utils',
        'backend.mousse_visco_longueur_utils',
        'backend.mousse_rainuree7zones_utils',
        'backend.mousse_rainuree7zones_longueur_housse_utils',
        'backend.mousse_rainuree7zones_referentiel',
        
        # Modules select43
        'backend.select43_utils',
        'backend.select43_longueur_housse_utils',
        
        # Modules de configuration
        'config',
        'version',
    ]
    return backend_modules

def build_windows_executable():
    """Compile l'exécutable Windows avec PyInstaller"""
    print("🔨 Compilation de l'exécutable Windows...")
    
    # Récupération des modules backend
    backend_modules = get_backend_modules()
    
    # Construction de la commande PyInstaller pour Windows
    cmd = [
        'pyinstaller',
        '--onefile',
        '--noconfirm',
        '--name=MatelasApp',
        '--icon=assets/lit-double.ico',
        '--add-data=assets;assets',
        '--add-data=template;template',
        '--add-data=backend/template;backend/template',
        '--add-data=backend/Référentiels;backend/Référentiels',
        '--add-data=config;config',
        '--hidden-import=PyQt6',
        '--hidden-import=PyQt6.QtCore',
        '--hidden-import=PyQt6.QtGui',
        '--hidden-import=PyQt6.QtWidgets',
        '--hidden-import=PyQt6.QtPrintSupport',
        '--hidden-import=openpyxl',
        '--hidden-import=pandas',
        '--hidden-import=numpy',
        '--hidden-import=requests',
        '--hidden-import=json',
        '--hidden-import=logging',
        '--hidden-import=asyncio',
        '--hidden-import=aiohttp',
        '--hidden-import=tempfile',
        '--hidden-import=shutil',
        '--hidden-import=os',
        '--hidden-import=sys',
        '--hidden-import=pathlib',
        '--hidden-import=datetime',
        '--hidden-import=math',
        '--hidden-import=re',
        '--hidden-import=base64',
        '--hidden-import=hashlib',
        '--hidden-import=cryptography',
        '--hidden-import=fitz',  # PyMuPDF
        '--hidden-import=urllib3',
        '--hidden-import=openai',
        '--hidden-import=ollama',
        # Options spécifiques Windows
        '--windowed',  # Pas de console pour l'application GUI
        '--uac-admin',  # Demande les privilèges admin si nécessaire
        '--clean',  # Nettoie le cache PyInstaller
    ]
    
    # Ajout des modules backend
    for module in backend_modules:
        cmd.extend(['--hidden-import', module])
    
    # Ajout du script principal
    cmd.append('app_gui.py')
    
    print(f"Commande PyInstaller Windows: {' '.join(cmd)}")
    
    # Exécution de la compilation
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Compilation Windows réussie!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la compilation Windows:")
        print(f"  Sortie d'erreur: {e.stderr}")
        return False

def create_windows_installer():
    """Crée un installateur Windows simple"""
    print("📦 Création de l'installateur Windows...")
    
    # Créer un dossier d'installation
    install_dir = "MatelasApp_Windows"
    if os.path.exists(install_dir):
        shutil.rmtree(install_dir)
    
    os.makedirs(install_dir)
    
    # Copier l'exécutable
    exe_source = "dist/MatelasApp.exe"
    if os.path.exists(exe_source):
        shutil.copy2(exe_source, install_dir)
        print(f"  ✓ Exécutable copié: {install_dir}/MatelasApp.exe")
    
    # Créer un fichier README
    readme_content = """MatelasApp - Application de gestion de matelas

Installation:
1. Double-cliquez sur MatelasApp.exe pour lancer l'application
2. L'application se lancera automatiquement

Utilisation:
- Sélectionnez vos fichiers PDF de commandes
- Configurez les paramètres (semaine, année, etc.)
- Lancez le traitement
- Les fichiers Excel seront générés dans le dossier Downloads

Support:
Pour toute question, contactez l'équipe de développement.
"""
    
    with open(f"{install_dir}/README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"  ✓ README créé: {install_dir}/README.txt")
    
    # Créer un script de lancement
    batch_content = """@echo off
echo Lancement de MatelasApp...
start MatelasApp.exe
"""
    
    with open(f"{install_dir}/Lancer_MatelasApp.bat", "w", encoding="utf-8") as f:
        f.write(batch_content)
    
    print(f"  ✓ Script de lancement créé: {install_dir}/Lancer_MatelasApp.bat")
    
    return install_dir

def test_windows_executable():
    """Teste l'exécutable Windows compilé"""
    print("🧪 Test de l'exécutable Windows...")
    
    exe_path = "dist/MatelasApp.exe"
    if not os.path.exists(exe_path):
        print(f"❌ Exécutable Windows non trouvé: {exe_path}")
        return False
    
    print(f"✅ Exécutable Windows trouvé: {exe_path}")
    print("💡 Pour tester sur Windows:")
    print("   1. Copiez le dossier 'dist' sur un PC Windows")
    print("   2. Double-cliquez sur MatelasApp.exe")
    return True

def main():
    """Fonction principale"""
    print("🚀 Script de compilation MatelasApp pour Windows")
    print("=" * 60)
    
    # Nettoyage
    clean_build_dirs()
    
    # Compilation Windows
    if build_windows_executable():
        test_windows_executable()
        install_dir = create_windows_installer()
        print("\n🎉 Compilation Windows terminée avec succès!")
        print(f"📁 L'exécutable se trouve dans: dist/MatelasApp.exe")
        print(f"📦 L'installateur se trouve dans: {install_dir}/")
        print("\n📋 Instructions pour Windows:")
        print("   1. Copiez le dossier 'dist' sur un PC Windows")
        print("   2. Double-cliquez sur MatelasApp.exe")
        print("   3. Ou utilisez le dossier d'installation créé")
    else:
        print("\n💥 Échec de la compilation Windows")
        sys.exit(1)

if __name__ == "__main__":
    main() 