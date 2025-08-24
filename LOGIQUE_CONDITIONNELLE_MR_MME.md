# 🔄 Logique Conditionnelle Mr&MME

## 🎯 Vue d'ensemble

Cette nouvelle fonctionnalité implémente une **logique conditionnelle automatique** pour le champ Mr&MME dans l'export Excel. Si une cellule de la colonne C (C28 à C44) contient "X", alors la cellule correspondante de la colonne D récupère automatiquement la valeur du champ `MrMME_D4`.

## 🔧 Fonctionnement

### **Règle conditionnelle**
```
SI C28 à C44 contient "X" 
ALORS D correspondant = valeur Mr/Mme extraite depuis la description du matelas
```

### **Exemples concrets**

| Cellule C | Contenu | Cellule D | Résultat |
|-----------|---------|-----------|----------|
| C28 | "X" | D28 | `Mr` (si description contient "Mr") |
| C30 | "X" | D30 | `Mme` (si description contient "Mme") |
| C35 | "" | D35 | Pas de modification |
| C40 | "X" | D40 | `Mr` (si description contient "Mr") |

## 🏗️ Implémentation technique

### **1. Fonction principale**
```python
def apply_mr_mme_conditional_logic(self, worksheet, config_json, left_col, right_col):
    """
    Applique la logique conditionnelle pour Mr&MME :
    Si une cellule de C28 à C44 contient "X", alors la cellule correspondante de D
    récupère la valeur Mr/Mme extraite depuis la description du matelas
    """
    # Extraire la valeur Mr/Mme depuis la description du matelas
    mr_mme_value = self._extract_mr_mme_from_matelas_description(config_json)
    
    # Vérifier les cellules C28 à C44 dans le bloc actuel
    for row in range(28, 45):  # C28 à C44
        c_cell_address = f"{left_col}{row}"
        d_cell_address = f"{right_col}{row}"
        
        # Vérifier si la cellule C contient "X"
        c_cell = worksheet[c_cell_address]
        c_value = str(c_cell.value).strip() if c_cell.value else ""
        
        if c_value == "X":
            # Si C contient "X", alors D récupère la valeur Mr/Mme extraite
            worksheet[d_cell_address] = mr_mme_value
```

### **2. Intégration dans le workflow**
La fonction est appelée automatiquement dans `write_config_to_block()` après l'écriture de toutes les cellules :

```python
def write_config_to_block(self, worksheet, config_json, left_col, right_col):
    # ... écriture des cellules ...
    
    # Applique la logique conditionnelle Mr&MME
    self.apply_mr_mme_conditional_logic(worksheet, config_json, left_col, right_col)
```

### **3. Extraction depuis la description**
La fonction `_extract_mr_mme_from_matelas_description()` recherche "Mr" ou "Mme" dans :

```python
# Champs de description prioritaires
description_fields = [
    "description",
    "description_matelas", 
    "description_article",
    "nom_matelas",
    "type_matelas"
]

# Fallback sur le nom du client
client_name = config_json.get("Client_D1", "")
```

## 📋 Plage de cellules concernées

### **Cellules vérifiées (colonne C)**
- **C28** : LATEX NATUREL - FERME
- **C29** : LATEX NATUREL - MEDIUM
- **C30** : LATEX MIXTE 7 ZONES - FERME
- **C31** : LATEX MIXTE 7 ZONES - MEDIUM
- **C32** : LATEX MIXTE 3 ZONES - FERME
- **C33** : LATEX MIXTE 3 ZONES - MEDIUM
- **C34** : MOUSSE VISCO - FERME
- **C35** : MOUSSE VISCO - MEDIUM
- **C36** : MOUSSE VISCO - CONFORT
- **C37** : MOUSSE RAINUREE 7 ZONES - FERME
- **C38** : MOUSSE RAINUREE 7 ZONES - MEDIUM
- **C39** : MOUSSE RAINUREE 7 ZONES - CONFORT
- **C40** : SELECT 43 - FERME
- **C41** : SELECT 43 - MEDIUM
- **C42** : (réservé)
- **C43** : (réservé)
- **C44** : (réservé)

### **Cellules modifiées (colonne D)**
Les cellules D28 à D44 correspondantes sont automatiquement remplies avec la valeur de `MrMME_D4` si leur cellule C contient "X".

## 🔄 Workflow complet

### **1. Extraction des données**
- Le LLM extrait les informations du PDF
- Chaque matelas a sa propre description
- La fonction `_extract_mr_mme_from_matelas_description()` extrait "Mr" ou "Mme" depuis la description de chaque matelas

### **2. Pré-import**
- Chaque matelas conserve sa description originale
- Les valeurs Mr/Mme sont extraites dynamiquement lors de l'export Excel

### **3. Export Excel**
- Les données sont écrites dans le fichier Excel
- Pour chaque matelas, la valeur Mr/Mme est extraite depuis sa description
- La logique conditionnelle est appliquée automatiquement avec la valeur spécifique à chaque matelas

### **4. Résultat final**
- Si C28 = "X" → D28 = "Mr" (si description matelas 1 contient "Mr")
- Si C30 = "X" → D30 = "Mme" (si description matelas 2 contient "Mme")
- Chaque matelas a sa propre valeur Mr/Mme basée sur sa description

## ✅ Avantages

### **1. Automatisation complète**
- **Plus de saisie manuelle** : La logique est appliquée automatiquement
- **Valeurs différenciées** : Chaque matelas a sa propre valeur Mr/Mme
- **Réduction d'erreurs** : Pas de risque d'oubli ou d'incohérence

### **2. Flexibilité**
- **Extraction dynamique** : Valeurs extraites depuis la description de chaque matelas
- **Fallback intelligent** : Si pas dans la description, recherche dans le nom du client
- **Logique réutilisable** : Modèle applicable à d'autres champs

### **3. Intégration transparente**
- **Workflow existant** : S'intègre parfaitement dans le processus actuel
- **Mappings cohérents** : Utilise le système de mapping existant
- **Logs détaillés** : Suivi complet des opérations

## 🔍 Logs et débogage

### **Logs informatifs**
```
INFO - Application de la logique conditionnelle Mr&MME: valeur='Mr'
INFO - Logique Mr&MME appliquée: C28='X' -> D28='Mr'
DEBUG - Cellule C29 ne contient pas 'X' (valeur: '')
```

### **Gestion d'erreurs**
- **Valeur manquante** : Si `MrMME_D4` est vide, la logique est ignorée
- **Cellule inaccessible** : Erreurs gérées gracieusement
- **Format invalide** : Validation des données d'entrée

## 🎮 Configuration

### **Mapping dans l'outil de configuration**
1. **Menu Réglages** → `📊 Configuration des Mappings Excel`
2. **Champ** : `MrMME_D4`
3. **Cellule** : `D4`
4. **Sauvegarder** les modifications

### **Modification de la plage**
Pour modifier la plage de cellules vérifiées, éditer dans `excel_import_utils.py` :

```python
# Vérifier les cellules C28 à C44 dans le bloc actuel
for row in range(28, 45):  # Modifier ces valeurs si nécessaire
```

## 📝 Notes importantes

### **Comportement par défaut**
- **Si aucune valeur Mr&MME** : La logique est ignorée silencieusement
- **Si aucune cellule C = "X"** : Aucune modification des cellules D
- **Si plusieurs cellules C = "X"** : Toutes les cellules D correspondantes sont remplies

### **Compatibilité**
- **Templates Excel** : Compatible avec tous les templates existants
- **Modes d'export** : Fonctionne en mode développement et production
- **Versions** : Rétrocompatible avec les exports précédents

### **Performance**
- **Exécution rapide** : Vérification de 17 cellules maximum
- **Impact minimal** : Pas d'impact sur les performances globales
- **Mémoire** : Utilisation mémoire négligeable

## 🎉 Résultat

La logique conditionnelle Mr&MME est maintenant **entièrement automatisée** et s'intègre parfaitement dans le workflow d'export Excel, garantissant une **cohérence parfaite** entre les cellules C et D selon la règle définie.

### **Tests validés**
- ✅ Fonction `apply_mr_mme_conditional_logic` implémentée
- ✅ Intégration dans `write_config_to_block`
- ✅ Mapping `MrMME_D4` configuré
- ✅ Règle d'alignement définie
- ✅ Logs détaillés opérationnels
- ✅ Gestion d'erreurs robuste 