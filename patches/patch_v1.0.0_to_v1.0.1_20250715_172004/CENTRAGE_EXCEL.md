# Centrage des Cellules Excel - Documentation

## 📋 Vue d'Ensemble

Cette fonctionnalité permet de centrer automatiquement les valeurs dans les cellules Excel lors de l'export des configurations de matelas. Trois modes d'alignement sont disponibles pour répondre aux différents besoins.

## 🎯 Modes d'Alignement Disponibles

### 1. Mode "Intelligent" (Recommandé)
- **Description** : Alignement spécifique par type de données
- **Avantages** : Lisibilité optimale, respect des standards Excel
- **Utilisation** : Mode par défaut

### 2. Mode "Global"
- **Description** : Centrage de toutes les cellules
- **Avantages** : Cohérence visuelle maximale
- **Utilisation** : Pour une présentation uniforme

### 3. Mode "None"
- **Description** : Aucun alignement personnalisé
- **Avantages** : Respect des styles du template
- **Utilisation** : Pour conserver le formatage original

## 🔧 Implémentation Technique

### Fichiers Modifiés
- `backend/excel_import_utils.py` : Classe `ExcelMatelasImporter`

### Nouvelles Fonctionnalités

#### 1. Import d'openpyxl.styles
```python
from openpyxl.styles import Alignment
```

#### 2. Règles d'Alignement Intelligent
```python
self.alignment_rules = {
    'Client_D1': ('center', 'center'),
    'Adresse_D3': ('center', 'center'),
    # ... autres règles
}
```

#### 3. Méthode d'Application d'Alignement
```python
def apply_cell_alignment(self, worksheet, cell_address, json_key):
    # Applique l'alignement selon les règles définies
```

#### 4. Méthode de Centrage Global
```python
def center_block_cells(self, worksheet, left_col, right_col):
    # Centre toutes les cellules d'un bloc
```

## 📊 Règles d'Alignement Intelligent

### En-têtes et Informations Générales
- **Client, Adresse, Numéro de commande** : Centrés
- **Dates (semaine, lundi, vendredi)** : Centrés

### Dimensions et Mesures
- **Hauteur, Longueur** : Centrés
- **Dimensions housse** : Centrés
- **Découpe noyau** : Centrés

### Quantités et Types
- **Quantités (jumeaux, 1 pièce)** : Centrés
- **Types de housse** : Centrés
- **Types de noyau** : Centrés

### Opérations
- **Détection dosseret/tête** : Centrée
- **Surmatelas** : Centré
- **Opérations de transport** : Centrées

## 🚀 Utilisation

### Mode Intelligent (Par Défaut)
```python
importer = ExcelMatelasImporter(template_path)
# ou
importer = ExcelMatelasImporter(template_path, alignment_mode="intelligent")
```

### Mode Global
```python
importer = ExcelMatelasImporter(template_path, alignment_mode="global")
```

### Mode Aucun Alignement
```python
importer = ExcelMatelasImporter(template_path, alignment_mode="none")
```

## 📈 Avantages

### Mode Intelligent
- ✅ **Lisibilité optimale** : Chaque type de données a l'alignement approprié
- ✅ **Standards Excel** : Respect des conventions d'affichage
- ✅ **Professionnalisme** : Présentation soignée et cohérente
- ✅ **Flexibilité** : Règles personnalisables par type de données

### Mode Global
- ✅ **Cohérence visuelle** : Toutes les cellules centrées
- ✅ **Simplicité** : Aucune règle complexe
- ✅ **Uniformité** : Présentation identique partout

### Mode None
- ✅ **Respect du template** : Conserve le formatage original
- ✅ **Compatibilité** : Aucun changement de style
- ✅ **Performance** : Aucun traitement d'alignement

## 🔍 Logs et Debugging

### Logs d'Alignement
```python
logger.debug(f"Alignement appliqué à {cell_address}: {horizontal}/{vertical}")
logger.debug(f"Alignement par défaut appliqué à {cell_address}")
logger.info(f"Centrage global appliqué au bloc {left_col}-{right_col}")
```

### Gestion d'Erreurs
- **Cellules fusionnées** : Ignorées avec avertissement
- **Erreurs d'alignement** : Loggées sans arrêt du traitement
- **Cellules protégées** : Respectées

## 📝 Exemples d'Utilisation

### Exemple 1 : Mode Intelligent
```python
# Configuration par défaut
importer = ExcelMatelasImporter("template/template_matelas.xlsx")
fichiers = importer.import_configurations(configurations, "S01", "2024")
```

### Exemple 2 : Mode Global
```python
# Centrage de toutes les cellules
importer = ExcelMatelasImporter("template/template_matelas.xlsx", "global")
fichiers = importer.import_configurations(configurations, "S01", "2024")
```

### Exemple 3 : Mode Aucun Alignement
```python
# Respect du template original
importer = ExcelMatelasImporter("template/template_matelas.xlsx", "none")
fichiers = importer.import_configurations(configurations, "S01", "2024")
```

## 🧪 Tests

### Tests de Fonctionnalité
- Vérification de l'application des alignements
- Test des différents modes
- Validation de la gestion d'erreurs

### Tests de Performance
- Impact sur le temps d'export
- Gestion de la mémoire
- Optimisation des opérations

## 🔄 Évolutions Futures

### Fonctionnalités Possibles
1. **Alignement conditionnel** : Basé sur le contenu des cellules
2. **Styles personnalisés** : Couleurs, bordures, polices
3. **Règles dynamiques** : Chargement depuis un fichier de configuration
4. **Interface utilisateur** : Sélection du mode dans l'interface

### Améliorations Techniques
1. **Cache d'alignement** : Optimisation des performances
2. **Validation des règles** : Vérification de la cohérence
3. **Export des styles** : Sauvegarde des configurations

## 📞 Support

Pour toute question ou problème lié au centrage des cellules Excel :
1. Consultez les logs pour diagnostiquer les erreurs
2. Vérifiez le mode d'alignement utilisé
3. Testez avec différents modes pour identifier le problème
4. Contactez le support technique si nécessaire

---

**Version** : 1.0  
**Date** : 2024  
**Auteur** : Assistant IA  
**Statut** : Implémenté et testé 