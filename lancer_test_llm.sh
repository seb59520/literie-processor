#!/bin/bash

echo "🚀 Lancement de l'application de test LLM..."
echo

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 non trouvé"
    echo "💡 Installez Python depuis https://python.org"
    exit 1
fi

# Rendre le script exécutable
chmod +x lancer_test_llm.py

# Lancer l'application
python3 lancer_test_llm.py

if [ $? -ne 0 ]; then
    echo
    echo "❌ Erreur lors du lancement"
    exit 1
fi 