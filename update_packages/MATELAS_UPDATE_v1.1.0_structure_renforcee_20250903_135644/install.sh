#!/bin/bash
# Script d'installation - Structure Renforcée Sommiers
# Version: v1.1.0_structure_renforcee

echo "🚀 Installation de la mise à jour Structure Renforcée Sommiers"
echo "Version: v1.1.0_structure_renforcee"
echo "Date: 2025-09-03 13:56:44"
echo

# Vérification de l'environnement
if [ ! -d "backend" ]; then
    echo "❌ Erreur: Répertoire 'backend' non trouvé"
    echo "Veuillez exécuter ce script depuis la racine du projet MATELAS_FINAL"
    exit 1
fi

# Sauvegarde recommandée
echo "📦 Création d'une sauvegarde..."
backup_dir="backup_before_structure_renforcee_$(date +%Y%m%d_%H%M%S)"
cp -r backend "$backup_dir"
echo "✓ Sauvegarde créée: $backup_dir"

# Installation des fichiers
echo
echo "📥 Installation des nouveaux fichiers..."
cp -v backend/sommier_utils.py backend/sommier_utils.py
cp -v backend/pre_import_utils.py backend/pre_import_utils.py
echo "✓ Fichiers installés"

# Test de validation
echo
echo "🧪 Test de validation..."
python3 -c "
try:
    from backend.sommier_utils import detecter_structure_renforcee_sommier
    from backend.pre_import_utils import creer_pre_import_sommier
    
    # Test basique
    result = detecter_structure_renforcee_sommier('SOMMIER STRUCTURE RENFORCÉE')
    assert result == 'OUI', f'Expected OUI, got {result}'
    
    result2 = detecter_structure_renforcee_sommier('SOMMIER STANDARD')
    assert result2 == 'NON', f'Expected NON, got {result2}'
    
    print('✓ Tests de validation réussis')
except Exception as e:
    print(f'❌ Erreur lors des tests: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    echo
    echo "🎉 Mise à jour installée avec succès!"
    echo "📋 Nouvelles fonctionnalités disponibles:"
    echo "  - detecter_structure_renforcee_sommier()"
    echo "  - creer_pre_import_sommier() avec support structure renforcée"
    echo "  - Génération automatique du champ renforce_B550"
    echo
    echo "📚 Consultez CHANGELOG.md pour plus de détails"
else
    echo "❌ Erreur lors de l'installation"
    exit 1
fi
