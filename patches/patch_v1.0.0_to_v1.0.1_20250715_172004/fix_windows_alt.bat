@echo off
echo ========================================
echo    Correction Executable Windows
echo    (Version alternative)
echo ========================================
echo.

echo Correction de l'executable Windows...
echo.

REM Verifier PyInstaller
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo Installation de PyInstaller...
    python -m pip install pyinstaller
)

REM Nettoyer les anciens fichiers
echo Nettoyage des anciens fichiers...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del "*.spec"

REM Creer le fichier spec directement
echo Creation du fichier spec...
(
echo # -*- mode: python ; coding: utf-8 -*-
echo.
echo block_cipher = None
echo.
echo a = Analysis(
echo     ['run_gui.py'],
echo     pathex=[],
echo     binaries=[],
echo     datas=[
echo         ('backend', 'backend'),
echo         ('assets', 'assets'),
echo         ('template', 'template'),
echo         ('config', 'config'),
echo         ('Référentiels', 'Référentiels'),
echo         ('Commandes', 'Commandes'),
echo         ('EULA.txt', '.'),
echo     ],
echo     hiddenimports=[
echo         'PyQt6.QtCore',
echo         'PyQt6.QtWidgets',
echo         'PyQt6.QtGui',
echo         'PyQt6.QtPrintSupport',
echo         'fitz',
echo         'openpyxl',
echo         'httpx',
echo         'jinja2',
echo         'cryptography',
echo         'pandas',
echo         'numpy',
echo         'PIL',
echo         'requests',
echo         'backend_interface',
echo         'config',
echo     ],
echo     hookspath=[],
echo     hooksconfig={},
echo     runtime_hooks=[],
echo     excludes=['tkinter', 'matplotlib', 'scipy'],
echo     win_no_prefer_redirects=False,
echo     win_private_assemblies=False,
echo     cipher=block_cipher,
echo     noarchive=False,
echo )
echo.
echo pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
echo.
echo exe = EXE(
echo     pyz,
echo     a.scripts,
echo     a.binaries,
echo     a.zipfiles,
echo     a.datas,
echo     [],
echo     name='MatelasApp',
echo     debug=False,
echo     bootloader_ignore_signals=False,
echo     strip=False,
echo     upx=False,
echo     upx_exclude=[],
echo     runtime_tmpdir=None,
echo     console=False,
echo     disable_windowed_traceback=False,
echo     argv_emulation=False,
echo     target_arch=None,
echo     codesign_identity=None,
echo     entitlements_file=None,
echo )
) > matelas_fixed.spec

echo Compilation en cours...
python -m PyInstaller matelas_fixed.spec

if errorlevel 1 (
    echo ERREUR lors de la compilation
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Correction Terminee !
echo ========================================
echo.
echo Votre application corrigee se trouve dans: dist\MatelasApp\
echo.
echo Pour lancer l'application:
echo   1. Double-cliquez sur dist\MatelasApp\MatelasApp.exe
echo   2. Ou utilisez launch_simple.bat
echo.
pause 