#!/bin/bash

echo "========================================"
echo "   Génération Documentation PDF"
echo "========================================"
echo

echo "Installation des dépendances..."
pip3 install reportlab

echo
echo "Génération de la documentation PDF..."
python3 create_documentation_pdf.py

if [ $? -eq 0 ]; then
    echo
    echo "========================================"
    echo "   Documentation générée avec succès!"
    echo "========================================"
    echo
    echo "Le fichier PDF se trouve dans:"
    echo "  Documentation_MatelasApp_Westelynck.pdf"
    echo
    echo "Pour ouvrir le PDF:"
    echo "  open Documentation_MatelasApp_Westelynck.pdf"
    echo
else
    echo
    echo "========================================"
    echo "   Erreur lors de la génération"
    echo "========================================"
    echo
    echo "Vérifiez que:"
    echo "  1. Python 3.8+ est installé"
    echo "  2. Le logo Westelynck est présent dans assets/"
    echo "  3. Tous les fichiers du projet sont présents"
    echo
fi

read -p "Appuyez sur Entrée pour continuer..." 