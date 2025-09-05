# 📦 Guide d'Installation - Structure Renforcée Sommiers

## 🎯 Vue d'ensemble

Cette mise à jour ajoute la détection automatique de **"structure renforcée"** dans les descriptions de sommiers et génère automatiquement le champ `renforce_B550` avec la valeur `"X"` dans le pré-import Excel.

**Version**: v1.1.0_structure_renforcee  
**Date**: 2025-09-03  
**Compatibilité**: Toutes versions MATELAS_FINAL ≥ 3.10.0

## 🚀 Installation Rapide

### Option 1: Installation Automatique (Recommandée)

```bash
# 1. Extraire le ZIP dans le répertoire MATELAS_FINAL
unzip MATELAS_UPDATE_v1.1.0_structure_renforcee_*.zip

# 2. Exécuter le script d'installation
chmod +x install.sh
./install.sh
```

### Option 2: Installation Manuelle

```bash
# 1. Sauvegarde de sécurité
cp -r backend/ backend_backup_$(date +%Y%m%d)/

# 2. Copie des fichiers mis à jour
cp backend/sommier_utils.py backend/sommier_utils.py
cp backend/pre_import_utils.py backend/pre_import_utils.py

# 3. Test de validation
python3 -c "
from backend.sommier_utils import detecter_structure_renforcee_sommier
print('Test:', detecter_structure_renforcee_sommier('SOMMIER STRUCTURE RENFORCÉE'))
"
```

## ✨ Nouvelles Fonctionnalités

### 1. Détection Structure Renforcée

```python
from backend.sommier_utils import detecter_structure_renforcee_sommier

# Exemples de détection
detecter_structure_renforcee_sommier("SOMMIER STRUCTURE RENFORCÉE")     # → "OUI"
detecter_structure_renforcee_sommier("SOMMIER STRUCTURE RENFORCEE")     # → "OUI" 
detecter_structure_renforcee_sommier("SOMMIER STRUCTURES RENFORCÉES")   # → "OUI"
detecter_structure_renforcee_sommier("sommier structure renforcée")     # → "OUI"
detecter_structure_renforcee_sommier("SOMMIER STANDARD")                # → "NON"
```

**Caractéristiques**:
- ✅ Insensible à la casse (majuscule/minuscule)
- ✅ Suppression automatique des accents
- ✅ Support singulier et pluriel
- ✅ Détection robuste dans toute la description

### 2. Pré-import Sommier Amélioré

```python
from backend.pre_import_utils import creer_pre_import_sommier

configurations_sommier = [{
    'description': 'SOMMIER TAPISSIER STRUCTURE RENFORCÉE 160x200',
    'quantite': 1,
    'dimensions': {'largeur': '160', 'longueur': '200'},
    'type_sommier': 'SOMMIER TAPISSIER'
}]

donnees_client = {
    'nom': 'Client Test',
    'adresse': '123 Rue de la Paix'
}

# Génération du pré-import
pre_import = creer_pre_import_sommier(configurations_sommier, donnees_client)

# Résultat automatique:
# {
#   "structure_renforces": "OUI",
#   "renforce_B550": "X",        # ← Nouveau champ Excel automatique
#   "Client_D1": "Client Test",
#   "dimensions": "160 x 200",
#   ...
# }
```

## 🔧 Intégration dans le Workflow

### Dans le traitement LLM
La détection s'intègre automatiquement dans votre pipeline existant:

```python
# Après extraction LLM des données sommier
for config in configurations_sommier:
    description = config.get('description', '')
    
    # La détection est automatique dans creer_pre_import_sommier()
    pre_import = creer_pre_import_sommier([config], donnees_client)
    
    # Le champ renforce_B550 est automatiquement ajouté si nécessaire
    if pre_import[0]['renforce_B550'] == 'X':
        print(f"Structure renforcée détectée: {description}")
```

### Dans l'interface utilisateur
Ajoutez l'affichage du statut structure renforcée:

```python
# Affichage dans l'interface
for item in pre_import_data:
    if item.get('structure_renforces') == 'OUI':
        print(f"🔧 Structure renforcée détectée")
        print(f"📋 Champ Excel: renforce_B550 = {item.get('renforce_B550')}")
```

## 🧪 Tests de Validation

### Test Automatique
```bash
python3 -c "
from backend.sommier_utils import detecter_structure_renforcee_sommier
from backend.pre_import_utils import creer_pre_import_sommier

# Tests de détection
tests = [
    ('SOMMIER STRUCTURE RENFORCÉE', 'OUI'),
    ('SOMMIER STRUCTURE RENFORCEE', 'OUI'),
    ('SOMMIER STRUCTURES RENFORCÉES', 'OUI'),
    ('sommier structure renforcée', 'OUI'),
    ('SOMMIER STANDARD', 'NON')
]

print('=== Tests Détection ===')
for desc, expected in tests:
    result = detecter_structure_renforcee_sommier(desc)
    status = '✅' if result == expected else '❌'
    print(f'{status} {desc} → {result}')

# Test pré-import
config = {
    'description': 'SOMMIER TAPISSIER STRUCTURE RENFORCÉE',
    'quantite': 1,
    'dimensions': {'largeur': '160', 'longueur': '200'}
}
client = {'nom': 'Test', 'adresse': 'Test Address'}
result = creer_pre_import_sommier([config], client)

print(f'\\n=== Test Pré-import ===')
print(f'✅ Structure détectée: {result[0][\"structure_renforces\"]}')
print(f'✅ Champ Excel: renforce_B550 = {result[0][\"renforce_B550\"]}')
"
```

### Tests Manuels Recommandés
Testez avec vos descriptions réelles:

```python
# Vos descriptions de sommiers
descriptions_test = [
    "SOMMIER 160X200 TAPISSIER STRUCTURE RENFORCÉE RELAXATION",
    "Sommier à lattes structure renforcée 140x190",
    "SOMMIER TAPISSIER STANDARD 160X200",
    # ... vos descriptions
]

for desc in descriptions_test:
    result = detecter_structure_renforcee_sommier(desc)
    print(f"'{desc}' → {result}")
```

## 📋 Vérification Post-Installation

### 1. Fonctions Disponibles
```python
# Vérification des imports
try:
    from backend.sommier_utils import detecter_structure_renforcee_sommier
    from backend.pre_import_utils import creer_pre_import_sommier
    print("✅ Toutes les fonctions sont disponibles")
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
```

### 2. Test Fonctionnel Complet
```python
# Test de bout en bout
config_test = {
    'description': 'SOMMIER STRUCTURE RENFORCÉE TEST',
    'quantite': 1,
    'dimensions': {'largeur': '160', 'longueur': '200'}
}

client_test = {'nom': 'Client Test', 'adresse': 'Adresse Test'}

pre_import = creer_pre_import_sommier([config_test], client_test)
assert pre_import[0]['renforce_B550'] == 'X'
print("✅ Test fonctionnel réussi")
```

## 🆘 Dépannage

### Erreur d'Import
```bash
# Si erreur "module not found"
python3 -c "import sys; print('\n'.join(sys.path))"
# Vérifier que le répertoire backend est dans le PYTHONPATH
```

### Fonction Non Reconnue
```bash
# Vérifier la version des fichiers
python3 -c "
import backend.sommier_utils as su
print(dir(su))
# Doit contenir 'detecter_structure_renforcee_sommier'
"
```

### Rollback si Nécessaire
```bash
# Restaurer la sauvegarde
cp -r backend_backup_*/ backend/
```

## 📞 Support

Pour toute question ou problème:

1. **Vérifiez les logs** dans le fichier de log de l'application
2. **Testez les exemples** fournis dans ce guide  
3. **Consultez le CHANGELOG.md** pour les détails techniques
4. **Utilisez la sauvegarde** pour revenir en arrière si nécessaire

## 🎯 Prochaines Étapes

Après installation réussie:

1. **Testez** avec vos propres descriptions de sommiers
2. **Vérifiez** la génération des fichiers Excel avec le champ `renforce_B550`  
3. **Adaptez** vos templates Excel si nécessaire pour afficher le nouveau champ
4. **Formez** les utilisateurs sur la nouvelle fonctionnalité

---

**Version du guide**: 1.0  
**Dernière mise à jour**: 2025-09-03