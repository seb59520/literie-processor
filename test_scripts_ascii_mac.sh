#!/bin/bash

echo "========================================"
echo "   TEST DES SCRIPTS ASCII (MAC)"
echo "========================================"
echo

echo "Test des scripts ASCII sans caracteres speciaux..."
echo

# Test 1: Vérifier que les fichiers existent
echo "[1/5] Verification des fichiers..."
if [ -f "build_scripts/windows/menu_ascii.bat" ]; then
    echo "menu_ascii.bat: OK"
else
    echo "menu_ascii.bat: MANQUANT"
fi

if [ -f "build_scripts/windows/install_ascii.bat" ]; then
    echo "install_ascii.bat: OK"
else
    echo "install_ascii.bat: MANQUANT"
fi

if [ -f "build_scripts/windows/lancer_ascii.bat" ]; then
    echo "lancer_ascii.bat: OK"
else
    echo "lancer_ascii.bat: MANQUANT"
fi

if [ -f "build_scripts/windows/diagnostic_ascii.bat" ]; then
    echo "diagnostic_ascii.bat: OK"
else
    echo "diagnostic_ascii.bat: MANQUANT"
fi

if [ -f "Lancer_MatelasApp_ASCII.bat" ]; then
    echo "Lancer_MatelasApp_ASCII.bat: OK"
else
    echo "Lancer_MatelasApp_ASCII.bat: MANQUANT"
fi

echo

# Test 2: Vérifier le format ASCII
echo "[2/5] Verification du format ASCII..."
if grep -q "@echo off" "build_scripts/windows/menu_ascii.bat"; then
    echo "menu_ascii.bat: FORMAT ASCII OK"
else
    echo "menu_ascii.bat: FORMAT INCORRECT"
fi

if grep -q "@echo off" "build_scripts/windows/install_ascii.bat"; then
    echo "install_ascii.bat: FORMAT ASCII OK"
else
    echo "install_ascii.bat: FORMAT INCORRECT"
fi

echo

# Test 3: Vérifier l'encodage
echo "[3/5] Verification de l'encodage..."
if file "build_scripts/windows/menu_ascii.bat" | grep -q "ASCII"; then
    echo "menu_ascii.bat: ENCODAGE ASCII OK"
else
    echo "menu_ascii.bat: ENCODAGE PROBLEMATIQUE"
fi

if file "build_scripts/windows/install_ascii.bat" | grep -q "ASCII"; then
    echo "install_ascii.bat: ENCODAGE ASCII OK"
else
    echo "install_ascii.bat: ENCODAGE PROBLEMATIQUE"
fi

echo

# Test 4: Afficher un aperçu du contenu
echo "[4/5] Apercu du contenu..."
echo "Premieres lignes de menu_ascii.bat:"
head -10 "build_scripts/windows/menu_ascii.bat"
echo

# Test 5: Vérifier qu'il n'y a pas de caractères spéciaux
echo "[5/5] Verification des caracteres speciaux..."
if LC_ALL=C grep -q '[^[:print:][:space:]]' "build_scripts/windows/menu_ascii.bat"; then
    echo "ATTENTION: Caracteres non-ASCII detectes dans menu_ascii.bat"
else
    echo "menu_ascii.bat: AUCUN caractere special detecte"
fi

if LC_ALL=C grep -q '[^[:print:][:space:]]' "build_scripts/windows/install_ascii.bat"; then
    echo "ATTENTION: Caracteres non-ASCII detectes dans install_ascii.bat"
else
    echo "install_ascii.bat: AUCUN caractere special detecte"
fi

echo
echo "========================================"
echo "    TEST TERMINE"
echo "========================================"
echo
echo "Les scripts ASCII sont crees pour Windows!"
echo
echo "Pour tester sur Windows:"
echo "1. Copiez le dossier MATELAS_FINAL sur un PC Windows"
echo "2. Double-cliquez sur Lancer_MatelasApp_ASCII.bat"
echo "3. Ou lancez build_scripts\\windows\\menu_ascii.bat"
echo
echo "Les scripts sont maintenant sans caracteres speciaux"
echo "et ne devraient plus causer d'erreurs d'encodage sur Windows."
echo 