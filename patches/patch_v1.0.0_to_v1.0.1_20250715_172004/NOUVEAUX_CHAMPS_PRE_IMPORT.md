# Nouveaux Champs Pré-Import

## Vue d'ensemble

Ce document décrit les nouveaux champs ajoutés au JSON de pré-import pour l'étape d'import Excel.

## Nouveaux Champs Ajoutés

### 1. `numero_D2` - Numéro de commande client
- **Source**: `commande_client` dans la configuration matelas
- **Description**: Numéro de commande du client
- **Exemple**: "LOUCHART", "DEVERSENNE", "BILAND"

### 2. `semaine_D5` - Semaine de l'année
- **Source**: `semaine_annee` dans la configuration matelas
- **Description**: Semaine de production au format "XX_YYYY"
- **Exemple**: "25_2025", "26_2025"

### 3. `lundi_D6` - Date du lundi
- **Source**: `lundi` dans la configuration matelas
- **Description**: Date du lundi de la semaine de production
- **Format**: "YYYY-MM-DD"
- **Exemple**: "2025-06-16", "2025-06-23"

### 4. `vendredi_D7` - Date du vendredi
- **Source**: `vendredi` dans la configuration matelas
- **Description**: Date du vendredi de la semaine de production
- **Format**: "YYYY-MM-DD"
- **Exemple**: "2025-06-20", "2025-06-27"

### 5. `dosseret_tete_C8` - Détection dosseret/tête
- **Source**: Paramètre `contient_dosseret_tete` (booléen)
- **Description**: Indique si DOSSERET ou TETE a été détecté
- **Valeurs**: 
  - `"X"` si DOSSERET ou TETE détecté
  - `""` (chaîne vide) sinon

## Structure JSON Complète

```json
{
  "Client_D1": "Mr LOUCHART FREDERIC",
  "Adresse_D3": "HAZEBROUCK",
  "numero_D2": "LOUCHART",
  "semaine_D5": "25_2025",
  "lundi_D6": "2025-06-16",
  "vendredi_D7": "2025-06-20",
  "Hauteur_D22": 20,
  "dosseret_tete_C8": "",
  "matelas_index": 1,
  "noyau": "LATEX MIXTE 7 ZONES",
  "quantite": 1
}
```

## Intégration dans le Backend

### Modification de `pre_import_utils.py`

1. **Fonction `creer_pre_import`**:
   - Ajout du paramètre `contient_dosseret_tete`
   - Intégration des nouveaux champs dans la structure JSON

2. **Fonction `valider_pre_import`**:
   - Mise à jour de la liste des champs obligatoires
   - Validation de la présence de tous les nouveaux champs

3. **Fonction `formater_pre_import_pour_affichage`**:
   - Ajout des nouveaux champs dans l'affichage

### Modification de `main.py`

- Passage du paramètre `contient_dosseret_tete` à la fonction de création du pré-import

### Modification de `templates/index.html`

- Affichage des nouveaux champs dans l'interface utilisateur

## Tests

### Fichier de Test: `test_pre_import_nouveaux_champs.py`

Le fichier de test couvre :

1. **Test des nouveaux champs**:
   - Création avec et sans dosseret/tete
   - Validation de la structure
   - Formatage pour affichage

2. **Test avec cas réels**:
   - Mr DEVERSENNE avec dosseret/tete
   - Mr BILAND sans dosseret/tete

3. **Test de validation**:
   - Données complètes
   - Données manquantes

## Exemples d'Utilisation

### Cas 1: Avec DOSSERET/TETE détecté
```python
pre_import_data = creer_pre_import(
    configurations_matelas, 
    donnees_client, 
    contient_dosseret_tete=True
)
# Résultat: dosseret_tete_C8 = "X"
```

### Cas 2: Sans DOSSERET/TETE détecté
```python
pre_import_data = creer_pre_import(
    configurations_matelas, 
    donnees_client, 
    contient_dosseret_tete=False
)
# Résultat: dosseret_tete_C8 = ""
```

## Validation

La validation vérifie que tous les champs sont présents :
- `Client_D1`
- `Adresse_D3`
- `numero_D2`
- `semaine_D5`
- `lundi_D6`
- `vendredi_D7`
- `Hauteur_D22`
- `dosseret_tete_C8`

## Prochaines Étapes

1. **Intégration dans l'extraction LLM**:
   - Extraction automatique de `commande_client`
   - Extraction automatique de `semaine_annee`
   - Extraction automatique de `lundi` et `vendredi`
   - Détection automatique de DOSSERET/TETE

2. **Écriture Excel**:
   - Utilisation des champs nommés pour l'écriture dans Excel
   - Mapping des champs vers les cellules appropriées

## Résumé des Modifications

✅ **Nouveaux champs ajoutés**:
- `numero_D2`: commande_client
- `semaine_D5`: semaine_annee
- `lundi_D6`: lundi
- `vendredi_D7`: vendredi
- `dosseret_tete_C8`: détection DOSSERET/TETE

✅ **Validation mise à jour**:
- Tous les nouveaux champs sont validés

✅ **Interface mise à jour**:
- Affichage des nouveaux champs dans l'interface

✅ **Tests complets**:
- Tests unitaires et d'intégration
- Validation des cas réels

✅ **Documentation**:
- Documentation complète des nouveaux champs
- Exemples d'utilisation 