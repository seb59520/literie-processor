#!/usr/bin/env python3
"""
Script de compilation PyInstaller robuste pour l'application MatelasApp
Inclut explicitement tous les modules backend pour éviter les erreurs d'import
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

def build_executable():
    """Compile l'exécutable avec PyInstaller"""
    print("🔨 Compilation de l'exécutable...")
    
    # Récupération des modules backend
    backend_modules = get_backend_modules()
    
    # Construction de la commande PyInstaller
    cmd = [
        'pyinstaller',
        '--onefile',
        '--noconfirm',
        '--name=MatelasApp',
        '--icon=assets/lit-double.ico',
        '--add-data=assets:assets',
        '--add-data=template:template',
        '--add-data=backend/template:backend/template',
        '--add-data=backend/Référentiels:backend/Référentiels',
        '--add-data=config:config',
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
    ]
    
    # Ajout des modules backend
    for module in backend_modules:
        cmd.extend(['--hidden-import', module])
    
    # Ajout du script principal
    cmd.append('app_gui.py')
    
    print(f"Commande PyInstaller: {' '.join(cmd)}")
    
    # Exécution de la compilation
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Compilation réussie!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la compilation:")
        print(f"  Sortie d'erreur: {e.stderr}")
        return False

def test_executable():
    """Teste l'exécutable compilé"""
    print("🧪 Test de l'exécutable...")
    
    exe_path = "dist/MatelasApp"
    if not os.path.exists(exe_path):
        print(f"❌ Exécutable non trouvé: {exe_path}")
        return False
    
    print(f"✅ Exécutable trouvé: {exe_path}")
    print("💡 Pour tester, lancez: ./dist/MatelasApp")
    return True

def main():
    """Fonction principale"""
    print("🚀 Script de compilation MatelasApp")
    print("=" * 50)
    
    # Nettoyage
    clean_build_dirs()
    
    # Compilation
    if build_executable():
        test_executable()
        print("\n🎉 Compilation terminée avec succès!")
        print("📁 L'exécutable se trouve dans: dist/MatelasApp")
    else:
        print("\n💥 Échec de la compilation")
        sys.exit(1)

if __name__ == "__main__":
    main() 