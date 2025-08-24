# 📊 Accès à l'Outil de Mapping Excel

## 🎯 Vue d'ensemble

L'outil de configuration des mappings Excel est maintenant accessible via **deux menus différents** pour une meilleure ergonomie et facilité d'accès.

## 🚀 Accès rapide

### **Option 1 : Menu Diagnostic**
```
Diagnostic → 📊 Outil de Mapping Excel
```

### **Option 2 : Menu Réglages**
```
Réglages → 📊 Configuration des Mappings Excel
Réglages → 🔢 Ordre des Noyaux
```

**Note :** Les deux options ouvrent le même dialogue de configuration.

## 🎨 Interface de l'outil

### **Fonctionnalités principales**
- **Configuration des mappings** : Associer les champs pré-import aux cellules Excel
- **Prévisualisation Excel** : Voir l'impact des modifications en temps réel
- **Validation stricte** : Vérification que les cellules existent dans le template
- **Sauvegarde sécurisée** : Configuration persistante en JSON

### **Types de produits supportés**
- **Matelas** : 20+ champs configurables
- **Sommiers** : 35+ champs configurables

## 🔧 Utilisation

### **1. Accéder à l'outil**
- **Méthode 1** : Menu `Diagnostic` → `📊 Outil de Mapping Excel`
- **Méthode 2** : Menu `Réglages` → `📊 Configuration des Mappings Excel`
- **Méthode 3** : Menu `Réglages` → `🔢 Ordre des Noyaux` (pour configurer l'ordre d'affichage des noyaux)

### **2. Configurer les mappings**
1. **Sélectionner le type** : Matelas ou Sommiers
2. **Modifier les cellules** : Changer les références dans le tableau
3. **Valider les changements** : Vérifier la prévisualisation
4. **Sauvegarder** : Cliquer sur "Sauvegarder"

### **3. Prévisualisation Excel**
- **Onglet Prévisualisation** : Voir l'impact des modifications
- **Cellules mappées** : Surlignées en vert
- **Navigation** : Scroll dans le template

## 📋 Mappings disponibles

### **Matelas (exemples)**
```json
{
  "Client_D1": "D1",
  "Adresse_D3": "D3",
  "MrMME_D4": "D4",  // Nouveau champ Mr/Mme
  "numero_D2": "D2",
  "semaine_D5": "D5",
  "Hauteur_D22": "D22",
  "dimension_housse_D23": "D23"
}
```

### **Sommiers (exemples)**
```json
{
  "Client_D1": "D1",
  "Adresse_D3": "D3",
  "Type_Sommier_D20": "D20",
  "Materiau_D25": "D25",
  "Hauteur_D30": "D30",
  "Dimensions_D35": "D35"
}
```

## ✅ Avantages de cette approche

### **1. Accessibilité améliorée**
- **Triple accès** : Via Diagnostic ET Réglages (mappings + ordre des noyaux)
- **Logique intuitive** : Réglages pour la configuration, Diagnostic pour les outils
- **Visibilité** : Icônes 📊 et 🔢 distinctives

### **2. Ergonomie optimisée**
- **Accès rapide** : Pas besoin de chercher dans les menus
- **Cohérence** : Même dialogue depuis les deux menus
- **Flexibilité** : Choix selon le contexte d'utilisation

### **3. Intégration parfaite**
- **Interface native** : PyQt6 intégré
- **Gestion d'erreurs** : Messages informatifs
- **Compatibilité** : Fonctionne en mode développement et production

## 🔍 Validation et sécurité

### **Validation du format**
- **Format requis** : Lettre(s) + chiffre(s) (ex: C1, D25, AB123)
- **Validation regex** : `^[A-Z]+\d+$`
- **Feedback immédiat** : Indicateur visuel en temps réel

### **Validation d'existence**
- **Vérification template** : La cellule doit exister dans le template Excel
- **Prévention d'erreurs** : Évite les erreurs d'écriture
- **Validation stricte** : Seules les cellules existantes acceptées

## 🎮 Actions disponibles

### **Dans l'interface de mapping**
- **Sauvegarder** : Enregistrer les modifications
- **Restaurer défauts** : Revenir aux valeurs par défaut
- **Fermer** : Quitter sans sauvegarder
- **Ignorer** : Ne pas mapper un champ spécifique

### **Prévisualisation**
- **Scroll** : Navigation dans le template
- **Zoom** : Ajuster la vue
- **Légende** : Explication des couleurs

## 📝 Notes importantes

### **Sauvegarde automatique**
- **Format JSON** : Configuration lisible et modifiable
- **Métadonnées** : Horodatage et versioning
- **Gestion d'erreurs** : Récupération automatique

### **Compatibilité**
- **Mode développement** : Fonctionne avec les fichiers sources
- **Mode production** : Fonctionne avec l'exécutable compilé
- **Templates** : Compatible avec les templates Excel existants

## 🔧 Problème résolu

### **Erreur d'import corrigée**
- **Problème** : `Module de configuration des mappings non disponible: No module named 'mapping_manager'`
- **Cause** : Chemin d'import incorrect dans `utilities/admin/mapping_config_dialog_qt.py`
- **Solution** : Correction des imports avec fallbacks multiples pour la compatibilité

### **Correction technique**
```python
# Avant (incorrect)
backend_dir = os.path.join(os.path.dirname(__file__), "backend")
from mapping_manager import MappingManager

# Après (corrigé avec fallbacks)
backend_dir = os.path.join(os.path.dirname(__file__), "..", "..", "backend")
try:
    from mapping_manager import MappingManager
except ImportError:
    try:
        from backend.mapping_manager import MappingManager
    except ImportError:
        sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
        from backend.mapping_manager import MappingManager
```

## 🎉 Résultat

L'outil de mapping Excel est maintenant **parfaitement fonctionnel** et **facilement accessible** via deux menus différents, offrant une **flexibilité maximale** pour configurer les mappings entre les champs du pré-import et les cellules Excel, avec une **interface intuitive** et des **fonctionnalités avancées** de validation et prévisualisation.

### **Tests validés**
- ✅ Import du dialogue de mapping
- ✅ Fonctionnement du MappingManager
- ✅ Création du dialogue PyQt6
- ✅ Intégration dans les menus
- ✅ Compatibilité mode développement et production
- ✅ Outil d'ordre des noyaux accessible via menu Réglages 