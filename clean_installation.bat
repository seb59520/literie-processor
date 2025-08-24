@echo off
chcp 65001 >nul
echo ========================================
echo    Nettoyage Installation Matelas
echo ========================================
echo.

echo Nettoyage des fichiers de compilation...

if exist "build" (
    echo Suppression du dossier build...
    rmdir /s /q "build"
    echo OK: Dossier build supprime
)

if exist "dist" (
    echo Suppression du dossier dist...
    rmdir /s /q "dist"
    echo OK: Dossier dist supprime
)

if exist "*.spec" (
    echo Suppression des fichiers .spec...
    del /q "*.spec"
    echo OK: Fichiers .spec supprimes
)

if exist "__pycache__" (
    echo Suppression des caches Python...
    rmdir /s /q "__pycache__"
    echo OK: Cache Python supprime
)

if exist "backend\__pycache__" (
    echo Suppression des caches backend...
    rmdir /s /q "backend\__pycache__"
    echo OK: Cache backend supprime
)

echo.
echo Nettoyage termine !
echo.
echo Pour reinstaller, lancez: install_windows.bat
echo.
pause 