#!/bin/bash

echo "========================================"
echo "COMPILATION PYINSTALLER OPTIMISEE"
echo "Gestion des Assets - Matelas App"
echo "========================================"
echo

echo "🧹 Nettoyage des repertoires de build..."
rm -rf build dist __pycache__ *.spec
echo "✅ Nettoyage termine."
echo

echo "🔍 Verification des assets requis..."
missing_assets=0

check_asset() {
    if [ ! -f "$1" ]; then
        echo "   ❌ $1"
        missing_assets=1
    else
        echo "   ✅ $1"
    fi
}

check_asset "assets/lit-double.png"
check_asset "assets/logo_westelynck.png"
check_asset "template/template_matelas.xlsx"
check_asset "template/template_sommier.xlsx"
check_asset "config/mappings_matelas.json"
check_asset "config/mappings_sommiers.json"

if [ $missing_assets -eq 1 ]; then
    echo
    echo "⚠️  ATTENTION: Certains assets sont manquants!"
    echo "   La compilation peut echouer."
    echo
else
    echo
    echo "✅ Tous les assets requis sont presents."
    echo
fi

echo "🚀 Compilation avec PyInstaller optimise..."
echo

pyinstaller run_gui.py \
  --onefile \
  --windowed \
  --name MatelasApp \
  --paths=backend \
  --collect-all PyQt6 \
  --add-data "backend/template/*:backend/template" \
  --add-data "backend/templates/*:backend/templates" \
  --add-data "backend/Référentiels/*:backend/Référentiels" \
  --add-data "template/*:template" \
  --add-data "config/*:config" \
  --add-data "assets/*:assets" \
  --hidden-import=backend.asset_utils \
  --hidden-import=PyQt6.QtCore \
  --hidden-import=PyQt6.QtWidgets \
  --hidden-import=PyQt6.QtGui \
  --hidden-import=PyQt6.QtPrintSupport \
  --hidden-import=fastapi \
  --hidden-import=jinja2 \
  --hidden-import=uvicorn \
  --hidden-import=pandas \
  --hidden-import=openpyxl \
  --hidden-import=requests \
  --hidden-import=cryptography \
  --hidden-import=backend_interface \
  --hidden-import=config \
  --clean

echo
echo "========================================"
echo "COMPILATION TERMINEE"
echo "========================================"
echo

if [ -f "dist/MatelasApp" ]; then
    echo "✅ SUCCES! Executable cree: dist/MatelasApp"
    
    size_mb=$(du -m "dist/MatelasApp" | cut -f1)
    echo "   Taille: ${size_mb} MB"
    
    echo
    echo "🧪 Test de l'executable (10 secondes)..."
    echo
    
    # Rendre l'exécutable exécutable
    chmod +x "dist/MatelasApp"
    
    # Lancer l'exécutable en arrière-plan
    ./dist/MatelasApp &
    app_pid=$!
    
    # Attendre 10 secondes
    sleep 10
    
    # Arrêter l'application
    kill $app_pid 2>/dev/null
    
    echo "✅ Executable teste avec succes!"
    echo
    echo "L'application est prete a etre distribuee."
    echo "Tous les assets sont integres dans l'executable."
    
else
    echo "❌ ERREUR: Executable non cree"
    echo
    echo "Verifiez les erreurs de compilation ci-dessus."
    echo "Assurez-vous que tous les assets sont presents."
fi

echo 