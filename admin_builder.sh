#!/bin/bash

echo "🔨 ADMIN BUILDER - LANCEUR RAPIDE"
echo "=================================="
echo

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "admin_builder_gui.py" ]; then
    echo "❌ Erreur: admin_builder_gui.py non trouvé"
    echo "   Assurez-vous d'être dans le répertoire MATELAS_FINAL"
    exit 1
fi

echo "✅ Répertoire correct détecté"
echo

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Erreur: Python3 non trouvé"
    echo "   Installez Python3 avant de continuer"
    exit 1
fi

echo "✅ Python3 détecté"
echo

# Lancer l'Admin Builder
echo "🚀 Lancement de l'Admin Builder..."
echo "   Interface graphique en cours d'ouverture..."
echo

python3 admin_builder_gui.py

echo
echo "✅ Admin Builder fermé" 