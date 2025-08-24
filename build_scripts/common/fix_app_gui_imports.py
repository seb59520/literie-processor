#!/usr/bin/env python3
"""
Script pour corriger les imports dans app_gui.py pour PyInstaller
"""

import os
import shutil

def fix_app_gui_imports():
    """Corrige les imports dans app_gui.py pour PyInstaller"""
    
    print("🔧 Correction des imports dans app_gui.py...")
    
    # Sauvegarder l'original
    if os.path.exists('app_gui.py'):
        shutil.copy2('app_gui.py', 'app_gui.py.backup')
        print("✅ Sauvegarde créée: app_gui.py.backup")
    
    # Lire le fichier original
    with open('app_gui.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remplacer la section problématique
    old_imports = """# Import des modules backend existants
sys.path.append('backend')"""
    
    new_imports = """# Configuration du path pour PyInstaller
if hasattr(sys, '_MEIPASS'):
    # Mode PyInstaller
    base_path = sys._MEIPASS
else:
    # Mode développement
    base_path = os.path.dirname(os.path.abspath(__file__))

# Ajouter le backend au path de manière compatible PyInstaller
backend_path = os.path.join(base_path, 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Imports absolus pour PyInstaller"""
    
    # Effectuer le remplacement
    if old_imports in content:
        fixed_content = content.replace(old_imports, new_imports)
        
        # Écrire le fichier corrigé
        with open('app_gui.py', 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print("✅ Imports corrigés dans app_gui.py")
        print("   - Suppression de sys.path.append('backend')")
        print("   - Ajout de la gestion PyInstaller")
        print("   - Imports absolus configurés")
        
    else:
        print("⚠️ Section d'imports non trouvée, vérifiez manuellement")
        return False
    
    return True

def create_fixed_run_gui():
    """Crée une version corrigée de run_gui.py"""
    
    print("🔧 Création de run_gui_fixed.py...")
    
    fixed_run_gui = '''#!/usr/bin/env python3
"""
Script de lancement pour l'application graphique de traitement de devis matelas
Version corrigée pour PyInstaller
"""

import sys
import os

# Configuration du path pour PyInstaller
if hasattr(sys, '_MEIPASS'):
    # Mode PyInstaller
    base_path = sys._MEIPASS
else:
    # Mode développement
    base_path = os.path.dirname(os.path.abspath(__file__))

# Ajouter le backend au path de manière compatible PyInstaller
backend_path = os.path.join(base_path, 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

def main():
    """Lance l'application graphique"""
    try:
        from app_gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"Erreur d'import: {e}")
        print("Assurez-vous d'avoir installé PyQt6: pip install PyQt6")
        sys.exit(1)
    except Exception as e:
        print(f"Erreur lors du lancement: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    with open('run_gui_fixed.py', 'w', encoding='utf-8') as f:
        f.write(fixed_run_gui)
    
    print("✅ Fichier run_gui_fixed.py créé")

def create_fixed_spec():
    """Crée un fichier .spec corrigé"""
    
    print("🔧 Création du fichier .spec corrigé...")
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run_gui_fixed.py'],  # Utilise la version corrigée
    pathex=['backend'],
    binaries=[],
    datas=[
        ('backend/template', 'backend/template'),
        ('backend/templates', 'backend/templates'),
        ('backend/Référentiels', 'backend/Référentiels'),
        ('template', 'template'),
        ('config', 'config'),
        ('assets', 'assets'),
    ],
    hiddenimports=[
        'backend.asset_utils',
        'PyQt6.QtCore',
        'PyQt6.QtWidgets',
        'PyQt6.QtGui',
        'PyQt6.QtPrintSupport',
        'fastapi',
        'jinja2',
        'uvicorn',
        'pandas',
        'openpyxl',
        'requests',
        'cryptography',
        'backend_interface',
        'config',
        'backend.article_utils',
        'backend.client_utils',
        'backend.date_utils',
        'backend.decoupe_noyau_utils',
        'backend.dimensions_sommiers',
        'backend.dimensions_utils',
        'backend.excel_import_utils',
        'backend.excel_sommier_import_utils',
        'backend.fermete_utils',
        'backend.hauteur_utils',
        'backend.housse_utils',
        'backend.latex_mixte7zones_longueur_housse_utils',
        'backend.latex_mixte7zones_referentiel',
        'backend.latex_naturel_longueur_housse_utils',
        'backend.latex_naturel_referentiel',
        'backend.latex_renforce_longueur_utils',
        'backend.latex_renforce_utils',
        'backend.llm_provider',
        'backend.mapping_manager',
        'backend.matelas_utils',
        'backend.matiere_housse_utils',
        'backend.mousse_rainuree7zones_longueur_housse_utils',
        'backend.mousse_rainuree7zones_referentiel',
        'backend.mousse_visco_longueur_utils',
        'backend.mousse_visco_utils',
        'backend.operation_utils',
        'backend.poignees_utils',
        'backend.pre_import_utils',
        'backend.select43_longueur_housse_utils',
        'backend.select43_utils',
        'backend.sommier_analytics_utils',
        'backend.sommier_utils',
        'backend.secure_storage',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MatelasApp_Fixed',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
    
    with open('MatelasApp_Fixed.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Fichier MatelasApp_Fixed.spec créé")

def main():
    """Fonction principale"""
    
    print("=" * 50)
    print("CORRECTION DES IMPORTS POUR PYINSTALLER")
    print("=" * 50)
    
    # Corriger app_gui.py
    if fix_app_gui_imports():
        print()
        
        # Créer run_gui_fixed.py
        create_fixed_run_gui()
        print()
        
        # Créer le fichier .spec corrigé
        create_fixed_spec()
        print()
        
        print("🎉 Correction terminée!")
        print()
        print("📋 Prochaines étapes:")
        print("1. Compilez avec: pyinstaller MatelasApp_Fixed.spec --clean")
        print("2. Testez l'exécutable: dist/MatelasApp_Fixed.exe")
        print("3. Si ça fonctionne, remplacez les fichiers originaux")
        print()
        print("💡 Si vous voulez revenir en arrière:")
        print("   cp app_gui.py.backup app_gui.py")
        
    else:
        print("❌ Erreur lors de la correction")

if __name__ == "__main__":
    main() 