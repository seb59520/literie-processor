#!/bin/bash
echo "🚀 Démarrage de MatelasProcessor v3.11.9"
echo "📡 Mise à jour automatique activée"
echo

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé"
    echo "Veuillez installer Python 3.8 ou plus récent"
    exit 1
fi

# Vérifier les dépendances
echo "📦 Vérification des dépendances..."
python3 -c "import PyQt6" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📥 Installation de PyQt6..."
    pip3 install PyQt6
fi

# Lancer l'application
echo "▶️ Lancement de l'application..."
python3 app_gui.py
