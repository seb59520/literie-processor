#!/bin/bash

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "========================================"
echo "    🔨 LANCEUR DE BUILD MATELAS APP"
echo "========================================"
echo -e "${NC}"

# Vérifier que Python est installé
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 n'est pas installé${NC}"
    echo "Veuillez installer Python3 et le redémarrer"
    exit 1
fi

# Vérifier que PyInstaller est installé
if ! python3 -c "import PyInstaller" &> /dev/null; then
    echo -e "${YELLOW}⚠️ PyInstaller n'est pas installé${NC}"
    echo "Installation de PyInstaller..."
    pip3 install pyinstaller
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Échec de l'installation de PyInstaller${NC}"
        exit 1
    fi
fi

show_menu() {
    clear
    echo -e "${BLUE}"
    echo "========================================"
    echo "    🔨 LANCEUR DE BUILD MATELAS APP"
    echo "========================================"
    echo -e "${NC}"
    echo
    echo "📋 Options de build disponibles :"
    echo
    echo "1. 🔨 Build complet avec référentiels (Recommandé)"
    echo "2. 🍎 Build Mac complet (Package .app)"
    echo "3. 🧪 Build de test rapide"
    echo "4. 🔧 Build avec console de debug"
    echo "5. 📦 Build standalone sans Python"
    echo "6. 🎯 Build optimisé pour Windows"
    echo "7. 🔍 Vérifier les fichiers requis"
    echo "8. 🧹 Nettoyer les anciens builds"
    echo "9. ❌ Quitter"
    echo
}

build_complet() {
    echo
    echo -e "${GREEN}🚀 Lancement du build complet avec référentiels...${NC}"
    echo "⏳ Cela peut prendre plusieurs minutes..."
    echo
    python3 build_complet_avec_referentiels.py
}

build_mac() {
    echo
    echo -e "${GREEN}🍎 Lancement du build Mac complet...${NC}"
    echo "⚠️ Ce build est destiné à macOS uniquement"
    echo
    python3 build_mac_complet.py
}

build_test() {
    echo
    echo -e "${GREEN}🧪 Lancement du build de test rapide...${NC}"
    echo
    python3 build_test_rapide.py
}

build_debug() {
    echo
    echo -e "${GREEN}🔧 Lancement du build avec console de debug...${NC}"
    echo
    python3 build_debug_console.py
}

build_standalone() {
    echo
    echo -e "${GREEN}📦 Lancement du build standalone...${NC}"
    echo
    python3 build_standalone_exe.py
}

build_windows() {
    echo
    echo -e "${GREEN}🎯 Lancement du build optimisé Windows...${NC}"
    echo
    python3 build_windows_optimized.py
}

check_files() {
    echo
    echo -e "${GREEN}🔍 Vérification des fichiers requis...${NC}"
    echo
    python3 test_eula_inclusion.py
    if [ $? -ne 0 ]; then
        echo
        echo -e "${YELLOW}⚠️ Certains fichiers sont manquants${NC}"
        echo "Vérifiez que tous les fichiers requis sont présents"
    fi
}

clean_builds() {
    echo
    echo -e "${GREEN}🧹 Nettoyage des anciens builds...${NC}"
    echo
    if [ -d "build" ]; then
        echo "Suppression du dossier build..."
        rm -rf build
    fi
    if [ -d "dist" ]; then
        echo "Suppression du dossier dist..."
        rm -rf dist
    fi
    for spec in *.spec; do
        if [ -f "$spec" ]; then
            echo "Suppression de $spec..."
            rm "$spec"
        fi
    done
    echo -e "${GREEN}✅ Nettoyage terminé${NC}"
}

# Boucle principale
while true; do
    show_menu
    read -p "Choisissez une option (1-9) : " choice
    
    case $choice in
        1) build_complet ;;
        2) build_mac ;;
        3) build_test ;;
        4) build_debug ;;
        5) build_standalone ;;
        6) build_windows ;;
        7) check_files ;;
        8) clean_builds ;;
        9) 
            echo
            echo "👋 Au revoir !"
            exit 0
            ;;
        *) 
            echo
            echo -e "${RED}❌ Choix invalide. Veuillez choisir une option entre 1 et 9.${NC}"
            echo
            read -p "Appuyez sur Entrée pour continuer..."
            ;;
    esac
    
    echo
    echo -e "${BLUE}========================================"
    echo "           BUILD TERMINÉ"
    echo "========================================"
    echo -e "${NC}"
    echo
    echo "📁 Les fichiers générés se trouvent dans le dossier 'dist'"
    echo
    read -p "Appuyez sur Entrée pour continuer..."
done 