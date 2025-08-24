#!/usr/bin/env python3
"""
Script pour créer un exécutable standalone SANS avoir besoin de Python sur la machine cible
Ce script doit être exécuté sur une machine qui a Python installé
"""

import os
import sys
import subprocess
import shutil
import platform
from datetime import datetime

def check_python_installation():
    """Vérifie que Python est installé"""
    try:
        version = sys.version_info
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} détecté")
        return True
    except:
        print("❌ Python non détecté")
        return False

def install_pyinstaller():
    """Installe PyInstaller si nécessaire"""
    try:
        import PyInstaller
        print("✅ PyInstaller est déjà installé")
        return True
    except ImportError:
        print("📦 Installation de PyInstaller...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
            print("✅ PyInstaller installé avec succès")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'installation de PyInstaller: {e}")
            return False

def create_standalone_executable():
    """Crée un exécutable standalone complet"""
    
    print("=== Création d'un Exécutable Standalone ===")
    print("Cet exécutable fonctionnera sur n'importe quel PC Windows sans Python")
    
    # Vérifications
    if not check_python_installation():
        print("❌ Python doit être installé pour créer l'exécutable")
        return False
    
    if not install_pyinstaller():
        print("❌ Impossible d'installer PyInstaller")
        return False
    
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
)
'''
    
    # Écrire le fichier spec
    with open('matelas_standalone.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Fichier spec créé")
    
    # Construire l'exécutable
    print("🔨 Construction de l'exécutable (cela peut prendre plusieurs minutes)...")
    
    try:
        result = subprocess.run(['pyinstaller', 'matelas_standalone.spec', '--clean'], 
                              capture_output=True, text=True, timeout=600)  # 10 minutes timeout
        
        if result.returncode == 0:
            print("✅ Exécutable construit avec succès!")
            
            # Créer un package d'installation
            create_install_package()
            
        else:
            print("❌ Erreur lors de la construction:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout - La construction a pris trop de temps")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    return True

def create_install_package():
    """Crée un package d'installation pour l'exécutable"""
    
    exe_dir = "dist/Matelas_Processor_Standalone"
    if not os.path.exists(exe_dir):
        print("❌ Répertoire de l'exécutable non trouvé")
        return
    
    # Créer un dossier d'installation
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    install_dir = f"Matelas_Processor_Standalone_{timestamp}"
    if os.path.exists(install_dir):
        shutil.rmtree(install_dir)
    
    os.makedirs(install_dir)
    
    # Copier l'exécutable et les fichiers nécessaires
    shutil.copytree(exe_dir, f"{install_dir}/Matelas_Processor_Standalone")
    
    # Créer un script d'installation
    create_install_script(install_dir)
    
    # Créer un fichier README
    create_readme(install_dir)
    
    # Créer une archive ZIP
    create_zip_archive(install_dir)
    
    print(f"✅ Package d'installation créé: {install_dir}")
    print(f"📦 Archive ZIP créée: {install_dir}.zip")

def create_install_script(install_dir):
    """Crée un script d'installation"""
    
    system = platform.system()
    
    if system == "Windows":
        install_script = f"""@echo off
echo ========================================
echo Installation de Matelas Processor
echo ========================================
echo.

REM Créer le raccourci sur le bureau
echo Création du raccourci sur le bureau...
set DESKTOP=%USERPROFILE%\\Desktop
set SCRIPT_PATH=%~dp0

echo @echo off > "%DESKTOP%\\Matelas Processor.bat"
echo cd /d "%SCRIPT_PATH%Matelas_Processor_Standalone" >> "%DESKTOP%\\Matelas Processor.bat"
echo Matelas_Processor_Standalone.exe >> "%DESKTOP%\\Matelas Processor.bat"

echo.
echo ========================================
echo ✅ Installation terminée avec succès!
echo ========================================
echo.
echo 🖥️  Raccourci créé sur le bureau: "Matelas Processor"
echo 💡 Double-cliquez sur le raccourci pour lancer l'application
echo.
echo 📁 Application installée dans: %SCRIPT_PATH%Matelas_Processor_Standalone
echo.
pause
"""
        
        with open(f"{install_dir}/INSTALLER.bat", 'w', encoding='utf-8') as f:
            f.write(install_script)
    
    else:  # macOS/Linux
        install_script = f"""#!/bin/bash

echo "========================================"
echo "Installation de Matelas Processor"
echo "========================================"
echo

# Créer le raccourci sur le bureau
echo "Création du raccourci sur le bureau..."
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
echo "========================================"
echo "✅ Installation terminée avec succès!"
echo "========================================"
echo
echo "🖥️  Raccourci créé sur le bureau"
echo "💡 Double-cliquez sur le raccourci pour lancer l'application"
echo
echo "📁 Application installée dans: $SCRIPT_PATH/Matelas_Processor_Standalone"
echo
"""
        
        with open(f"{install_dir}/install.sh", 'w', encoding='utf-8') as f:
            f.write(install_script)
        
        # Rendre le script exécutable
        os.chmod(f"{install_dir}/install.sh", 0o755)

def create_readme(install_dir):
    """Crée un fichier README"""
    
    readme_content = """# Matelas Processor - Version Standalone

## 🎉 Félicitations !

Vous avez maintenant une version **standalone** de Matelas Processor qui fonctionne **SANS avoir besoin d'installer Python** !

## 📋 Installation

### Windows
1. **Double-cliquez sur `INSTALLER.bat`**
2. Suivez les instructions à l'écran
3. Un raccourci sera créé sur votre bureau

### macOS/Linux
1. Ouvrez un terminal dans ce dossier
2. Exécutez : `./install.sh`
3. Un raccourci sera créé sur votre bureau

## 🚀 Utilisation

1. **Double-cliquez sur le raccourci "Matelas Processor" sur votre bureau**
2. L'application se lance immédiatement
3. Sélectionnez vos fichiers PDF de commandes
4. Configurez les paramètres (semaine, année, etc.)
5. Cliquez sur "Traiter les fichiers"
6. Les fichiers Excel seront générés dans le dossier output/

## ✅ Avantages de cette Version

- **Aucune installation de Python requise**
- **Aucune installation de dépendances requise**
- **Fonctionne sur n'importe quel PC Windows**
- **Double-clic pour lancer**
- **Portable** - Copiez le dossier où vous voulez

## 📁 Structure

```
Matelas_Processor_Standalone/
├── Matelas_Processor_Standalone.exe  # Application principale
├── _internal/                        # Bibliothèques incluses
└── [fichiers de support]
```

## 🔧 Support

Si vous rencontrez des problèmes :
1. Vérifiez que votre antivirus n'a pas bloqué l'exécutable
2. Essayez de lancer l'exécutable en tant qu'administrateur
3. Contactez l'équipe de développement

## 📝 Note

Cette version inclut tout ce qui est nécessaire pour faire fonctionner l'application :
- Python 3.11 embarqué
- Toutes les dépendances (openpyxl, PyMuPDF, httpx, etc.)
- Interface graphique (tkinter)

**Aucune installation supplémentaire n'est requise !**
"""
    
    with open(f"{install_dir}/README.txt", 'w', encoding='utf-8') as f:
        f.write(readme_content)

def create_zip_archive(install_dir):
    """Crée une archive ZIP du package d'installation"""
    
    import zipfile
    
    zip_filename = f"{install_dir}.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(install_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, install_dir)
                zipf.write(file_path, arcname)
    
    print(f"📦 Archive ZIP créée: {zip_filename}")

def main():
    """Fonction principale"""
    print("🚀 Création d'un Exécutable Standalone")
    print("Cet exécutable fonctionnera sur n'importe quel PC sans Python")
    print()
    
    success = create_standalone_executable()
    
    if success:
        print("\n🎉 SUCCÈS !")
        print("L'exécutable standalone a été créé avec succès.")
        print("Vous pouvez maintenant distribuer cet exécutable à n'importe qui,")
        print("même s'ils n'ont pas Python installé !")
    else:
        print("\n❌ ÉCHEC")
        print("La création de l'exécutable a échoué.")
        print("Vérifiez que Python et PyInstaller sont correctement installés.")

if __name__ == "__main__":
    main() 