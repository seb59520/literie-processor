#!/bin/bash
echo "Lancement MATELAS Application v3.11.12..."
cd "$(dirname "$0")"

# Essayer python3 d'abord, puis python
if command -v python3 &> /dev/null; then
    python3 app_gui.py
elif command -v python &> /dev/null; then
    python app_gui.py
else
    echo "Erreur: Python non trouvé"
    echo "Installez Python 3.8+ et exécutez: python3 install.py"
    exit 1
fi
