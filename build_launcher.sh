#!/bin/bash

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "========================================"
echo "    🔨 LANCEUR DE BUILD MATELAS APP"
echo "========================================"
echo -e "${NC}"
echo
echo "📁 Nouvelle structure organisée"
echo
echo "Options disponibles :"
echo "1. 🔨 Build complet (Cross-platform)"
echo "2. 🍎 Build Mac"
echo "3. 🧪 Tests"
echo "4. 🔧 Administration"
echo "5. 📚 Documentation"
echo "6. ❌ Quitter"
echo
read -p "Choisissez une option (1-6) : " choice

case $choice in
    1) cd build_scripts/common && python3 build_complet_avec_referentiels.py ;;
    2) cd build_scripts/macos && python3 build_mac_complet.py ;;
    3) cd utilities/tests && python3 test_eula_inclusion.py ;;
    4) cd utilities/admin && python3 admin_builder_gui.py ;;
    5) open docs/build 2>/dev/null || xdg-open docs/build 2>/dev/null || echo "Ouvrez manuellement le dossier docs/build" ;;
    6) echo "Au revoir !"; exit 0 ;;
    *) echo "Choix invalide" ;;
esac
