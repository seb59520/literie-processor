#!/usr/bin/env python3
"""
Script pour créer un exécutable standalone avec Python embarqué
"""

import os
import sys
import subprocess
import shutil
import platform

def build_standalone_exe():
    """Construit un exécutable standalone avec PyInstaller"""
    
    print("=== Construction de l'exécutable standalone ===")
    
    # Vérifier si PyInstaller est installé
    try:
        import PyInstaller
        print("✅ PyInstaller est installé")
    except ImportError:
        print("❌ PyInstaller n'est pas installé")
        print("Installation de PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Créer le fichier spec pour PyInstaller
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('template', 'template'),
        ('backend', 'backend'),
        ('config.py', '.'),
    ],
    hiddenimports=[
        'openpyxl',
        'fitz',
        'httpx',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'json',
        'logging',
        'os',
        'sys',
        'tempfile',
        'shutil',
        'pathlib',
        'typing',
        'asyncio',
        'threading',
        'queue',
        'datetime',
        'unicodedata',
        'math',
        're',
        'csv',
        'openpyxl.utils',
        'openpyxl.workbook',
        'openpyxl.worksheet',
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
    name='Matelas_Processor_Standalone',
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
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
'''
    
    # Écrire le fichier spec
    with open('matelas_standalone.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Fichier spec créé")
    
    # Construire l'exécutable
    print("Construction de l'exécutable standalone...")
    result = subprocess.run(['pyinstaller', 'matelas_standalone.spec', '--clean'], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Exécutable construit avec succès")
        print("📁 L'exécutable se trouve dans: dist/Matelas_Processor_Standalone")
        
        # Créer un package d'installation
        create_install_package()
        
    else:
        print("❌ Erreur lors de la construction:")
        print(result.stderr)

def create_install_package():
    """Crée un package d'installation pour l'exécutable"""
    
    exe_dir = "dist/Matelas_Processor_Standalone"
    if not os.path.exists(exe_dir):
        print("❌ Répertoire de l'exécutable non trouvé")
        return
    
    # Créer un dossier d'installation
    install_dir = "Matelas_Processor_Standalone_Install"
    if os.path.exists(install_dir):
        shutil.rmtree(install_dir)
    
    os.makedirs(install_dir)
    
    # Copier l'exécutable et les fichiers nécessaires
    shutil.copytree(exe_dir, f"{install_dir}/Matelas_Processor_Standalone")
    
    # Créer un script d'installation
    create_install_script(install_dir)
    
    # Créer un fichier README
    create_readme(install_dir)
    
    print(f"✅ Package d'installation créé: {install_dir}")

def create_install_script(install_dir):
    """Crée un script d'installation"""
    
    system = platform.system()
    
    if system == "Windows":
        install_script = f"""@echo off
echo Installation de Matelas Processor Standalone...
echo.

REM Créer le raccourci sur le bureau
echo Création du raccourci...
set DESKTOP=%USERPROFILE%\\Desktop
set SCRIPT_PATH=%~dp0

echo @echo off > "%DESKTOP%\\Matelas Processor.bat"
echo cd /d "%SCRIPT_PATH%Matelas_Processor_Standalone" >> "%DESKTOP%\\Matelas Processor.bat"
echo Matelas_Processor_Standalone.exe >> "%DESKTOP%\\Matelas Processor.bat"

echo.
echo ✅ Installation terminée!
echo 🖥️  Raccourci créé sur le bureau
echo 💡 Double-cliquez sur "Matelas Processor" pour lancer l'application
echo.
pause
"""
        
        with open(f"{install_dir}/install.bat", 'w', encoding='utf-8') as f:
            f.write(install_script)
    
    else:  # macOS/Linux
        install_script = f"""#!/bin/bash

echo "Installation de Matelas Processor Standalone..."
echo

# Créer le raccourci sur le bureau
echo "Création du raccourci..."
DESKTOP="$HOME/Desktop"
SCRIPT_PATH="$(cd "$(dirname "$0")" && pwd)"

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    cat > "$DESKTOP/Matelas Processor.command" << EOF
#!/bin/bash
cd "$SCRIPT_PATH/Matelas_Processor_Standalone"
./Matelas_Processor_Standalone
EOF
    chmod +x "$DESKTOP/Matelas Processor.command"
else
    # Linux
    cat > "$DESKTOP/Matelas Processor.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Matelas Processor
Comment=Traitement automatique de commandes matelas
Exec=$SCRIPT_PATH/Matelas_Processor_Standalone/Matelas_Processor_Standalone
Terminal=false
Categories=Office;
EOF
    chmod +x "$DESKTOP/Matelas Processor.desktop"
fi

echo
echo "✅ Installation terminée!"
echo "🖥️  Raccourci créé sur le bureau"
echo
"""
        
        with open(f"{install_dir}/install.sh", 'w', encoding='utf-8') as f:
            f.write(install_script)
        
        # Rendre le script exécutable
        os.chmod(f"{install_dir}/install.sh", 0o755)

def create_readme(install_dir):
    """Crée un fichier README"""
    
    readme_content = """# Matelas Processor Standalone

## Description

Application de traitement automatique de commandes matelas avec interface graphique.
**Version standalone - Python inclus, aucune installation requise !**

## Installation

### Windows
1. Décompressez ce dossier
2. Double-cliquez sur `install.bat`
3. Suivez les instructions

### macOS/Linux
1. Décompressez ce dossier
2. Ouvrez un terminal dans le dossier
3. Exécutez: `./install.sh`

## Utilisation

1. Double-cliquez sur le raccourci "Matelas Processor" sur votre bureau
2. Sélectionnez vos fichiers PDF de commandes
3. Configurez les paramètres (semaine, année, etc.)
4. Cliquez sur "Traiter les fichiers"
5. Les fichiers Excel seront générés dans le dossier output/

## Avantages

- ✅ **Python inclus** - Aucune installation de Python requise
- ✅ **Dépendances incluses** - Tout est embarqué
- ✅ **Portable** - Fonctionne sur n'importe quel PC
- ✅ **Simple** - Double-clic pour lancer

## Support

Pour toute question, contactez l'équipe de développement.
"""
    
    with open(f"{install_dir}/README.txt", 'w', encoding='utf-8') as f:
        f.write(readme_content)

def main():
    """Fonction principale"""
    build_standalone_exe()

if __name__ == "__main__":
    main() 