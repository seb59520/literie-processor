#!/bin/bash

echo "🔨 LANCEMENT CONSTRUCTION COMPLÈTE - MATELAS APP"
echo "================================================"
echo

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "app_gui.py" ]; then
    echo "❌ Erreur: app_gui.py non trouvé"
    echo "   Assurez-vous d'être dans le répertoire MATELAS_FINAL"
    exit 1
fi

echo "✅ Répertoire correct détecté"
echo

# Vérifier les référentiels avant construction
echo "🔍 Vérification des référentiels..."
python3 test_referentiels_inclus.py
if [ $? -ne 0 ]; then
    echo "❌ Erreur: Référentiels manquants"
    echo "   Corrigez les fichiers manquants avant la construction"
    exit 1
fi

echo
echo "✅ Tous les référentiels sont présents"
echo

# Détecter la plateforme
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🍎 Plateforme macOS détectée"
    echo "   Utilisation du script de construction Mac"
    echo
    python3 build_mac_complet.py
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "🪟 Plateforme Windows détectée"
    echo "   Utilisation du script de construction Windows/Linux"
    echo
    python3 build_complet_avec_referentiels.py
else
    echo "🐧 Plateforme Linux détectée"
    echo "   Utilisation du script de construction Windows/Linux"
    echo
    python3 build_complet_avec_referentiels.py
fi

echo
echo "🎉 Construction terminée!"
echo
echo "📋 Prochaines étapes:"
echo "   1. Vérifiez le dossier dist/"
echo "   2. Testez l'exécutable créé"
echo "   3. Distribuez le package complet"
echo 