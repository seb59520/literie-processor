@echo off
chcp 65001 >nul
echo ================================================
echo     DIAGNOSTIC COMPILATION WINDOWS
echo ================================================
echo.

echo [INFO] Verification de l'environnement...
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python non trouve dans le PATH
    echo Installez Python depuis https://python.org
    goto :end
) else (
    echo [OK] Python detecte:
    python --version
)

echo.

REM Vérifier pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] pip non trouve
    goto :end
) else (
    echo [OK] pip detecte:
    pip --version
)

echo.

REM Vérifier PyInstaller
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [!] PyInstaller non installe
    echo Installation en cours...
    pip install pyinstaller
    if errorlevel 1 (
        echo [ERREUR] Impossible d'installer PyInstaller
        goto :end
    )
) else (
    echo [OK] PyInstaller installe:
    pip show pyinstaller | findstr Version
)

echo.

REM Vérifier les fichiers nécessaires
echo [INFO] Verification des fichiers...

if exist "app_gui.py" (
    echo [OK] app_gui.py present
) else (
    echo [ERREUR] app_gui.py manquant
    goto :end
)

if exist "config.py" (
    echo [OK] config.py present
) else (
    echo [ERREUR] config.py manquant
    goto :end
)

if exist "matelas_config.json" (
    echo [OK] matelas_config.json present
) else (
    echo [ERREUR] matelas_config.json manquant
    goto :end
)

if exist "build_windows.py" (
    echo [OK] build_windows.py present
) else (
    echo [ERREUR] build_windows.py manquant
    goto :end
)

echo.
echo ================================================
echo [OK] DIAGNOSTIC REUSSI
echo ================================================
echo.
echo Vous pouvez maintenant compiler avec:
echo   python build_windows.py
echo.
echo Ou compilation rapide:
echo   python quick_build.py
echo.
goto :end

:end
echo ================================================
pause