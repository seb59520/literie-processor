# Étape de Pré-Import Excel

## Vue d'ensemble

L'étape de pré-import est la **nouvelle étape avant-dernière** du processus qui transforme les configurations matelas en un format JSON structuré avec des champs nommés pour l'import Excel ultérieur.

## Objectif

Transformer les données des configurations matelas en un format JSON standardisé avec des champs nommés qui pourront être facilement mappés vers des cellules Excel spécifiques lors de l'étape finale d'écriture.

## Fonctionnalités

### 1. Création du JSON pré-import
- Transformation des configurations matelas en format structuré
- Un élément de pré-import par configuration matelas
- Mapping des champs avec des noms standardisés

### 2. Champs mappés actuellement
- **`Client_D1`** : Nom du client (ex: "Mr LOUCHART FREDERIC")
- **`Adresse_D3`** : Ville du client (ex: "HAZEBROUCK")
- **`Hauteur_D22`** : Hauteur du matelas (ex: 20)

### 3. Validation des données
- Vérification de la présence des champs obligatoires
- Validation de la cohérence des données
- Gestion des cas d'erreur

## Structure des données

### Format d'entrée (configurations matelas)
```json
[
  {
    "matelas_index": 1,
    "noyau": "LATEX MIXTE 7 ZONES",
    "quantite": 1,
    "hauteur": 20,
    "fermete": "MÉDIUM",
    "housse": "MATELASSÉE",
    "matiere_housse": "TENCEL SIMPLE",
    "poignees": "OREILLES",
    "dimensions": {"largeur": 89, "longueur": 198},
    "semaine_annee": "25_2025",
    "lundi": "2025-06-16",
    "vendredi": "2025-06-20",
    "commande_client": "LOUCHART"
  }
]
```

### Format de sortie (pré-import)
```json
[
  {
    "Client_D1": "Mr LOUCHART FREDERIC",
    "Adresse_D3": "HAZEBROUCK",
    "Hauteur_D22": 20,
    "matelas_index": 1,
    "noyau": "LATEX MIXTE 7 ZONES",
    "quantite": 1
  }
]
```

## Fichiers implémentés

### 1. `backend/pre_import_utils.py`
Nouveau module utilitaire contenant :
- `creer_pre_import(configurations_matelas, donnees_client)`: Fonction principale de création
- `valider_pre_import(pre_import_data)`: Validation des données
- `formater_pre_import_pour_affichage(pre_import_data)`: Formatage pour l'interface

### 2. `backend/main.py`
Modifications apportées :
- Import du module `pre_import_utils`
- Intégration de l'étape de pré-import après la création des configurations matelas
- Ajout des données de pré-import dans la structure de résultat

### 3. `backend/templates/index.html`
Modifications apportées :
- Affichage des données de pré-import dans l'interface
- Section dédiée avec mise en forme visuelle
- Affichage des champs mappés pour chaque configuration

## Workflow complet

1. **Upload PDF** → Extraction du texte
2. **Analyse LLM** → Extraction des données structurées
3. **Extraction client** → Récupération des données client
4. **Détection matelas** → Création des configurations matelas
5. **🆕 Pré-import** → Transformation en format structuré
6. **Écriture Excel** → (étape finale à venir)

## Mapping des champs

### Champs client
- `Client_D1` ← `donnees_client.nom`
- `Adresse_D3` ← `donnees_client.adresse`

### Champs matelas
- `Hauteur_D22` ← `config.hauteur`

### Champs de référence (pour debug)
- `matelas_index` ← `config.matelas_index`
- `noyau` ← `config.noyau`
- `quantite` ← `config.quantite`

## Tests

### Fichiers de test créés
1. `test_pre_import.py` : Tests unitaires des fonctions de pré-import
2. `test_integration_pre_import.py` : Tests d'intégration avec le backend complet

### Exécution des tests
```bash
python3 test_pre_import.py
python3 test_integration_pre_import.py
```

### Exemples de tests
```python
# Test de création du pré-import
configurations_matelas = [...]
donnees_client = {"nom": "Mr LOUCHART", "adresse": "HAZEBROUCK"}
pre_import_data = creer_pre_import(configurations_matelas, donnees_client)

# Résultat attendu
[
  {
    "Client_D1": "Mr LOUCHART",
    "Adresse_D3": "HAZEBROUCK", 
    "Hauteur_D22": 20,
    "matelas_index": 1,
    "noyau": "LATEX MIXTE 7 ZONES",
    "quantite": 1
  }
]
```

## Intégration dans le backend

### Position dans le workflow
L'étape de pré-import est exécutée **après** la création des configurations matelas et **avant** la génération du résultat final.

### Conditions d'exécution
- Présence de configurations matelas
- Présence de données client
- Validation des données d'entrée

### Gestion des erreurs
- Logs détaillés des étapes
- Gestion gracieuse des cas d'erreur
- Validation des données de sortie

## Affichage dans l'interface

### Section pré-import
- Titre : "📋 Pré-Import Excel (X élément(s))"
- Style : Fond jaune clair avec bordure orange
- Affichage par configuration matelas

### Informations affichées
- Numéro et type de matelas
- Champs mappés (Client_D1, Adresse_D3, Hauteur_D22)
- Mise en forme claire et lisible

## Validation

### Champs obligatoires
- `Client_D1` : Nom du client (non vide)
- `Adresse_D3` : Ville du client (non vide)
- `Hauteur_D22` : Hauteur du matelas (présent)

### Règles de validation
- Vérification de la présence de tous les champs
- Validation de la non-vacuité des données client
- Cohérence entre configurations et pré-import

## Extensibilité

### Ajout de nouveaux champs
Pour ajouter un nouveau champ, il suffit de :
1. Modifier la fonction `creer_pre_import()`
2. Ajouter le mapping dans le dictionnaire
3. Mettre à jour la validation
4. Modifier l'affichage dans le template

### Exemple d'extension
```python
pre_import_item = {
    "Client_D1": donnees_client.get("nom", ""),
    "Adresse_D3": donnees_client.get("adresse", ""),
    "Hauteur_D22": config.get("hauteur", ""),
    "NouveauChamp_D5": config.get("nouvelle_valeur", ""),  # Nouveau champ
    # ...
}
```

## Logs et monitoring

Le module génère des logs détaillés :
- Création du pré-import
- Nombre d'éléments créés
- Validation des données
- Erreurs éventuelles

## Compatibilité

- ✅ **Rétrocompatible** avec l'existant
- ✅ **Pas d'impact** sur les autres fonctionnalités
- ✅ **Gestion gracieuse** des cas d'erreur
- ✅ **Prêt pour l'étape Excel** finale

## Utilisation

### Automatique
L'étape de pré-import est **automatiquement exécutée** lors du traitement d'un devis. Aucune action supplémentaire n'est requise.

### Affichage
Les données de pré-import apparaissent dans l'interface dans une section dédiée avec :
- 📋 **Nombre d'éléments** créés
- 🏷️ **Champs mappés** pour chaque configuration
- 📊 **Informations de référence** (noyau, quantité)

### Accès programmatique
```python
# Dans le résultat du backend
result = {
    "pre_import": [
        {
            "Client_D1": "Mr LOUCHART FREDERIC",
            "Adresse_D3": "HAZEBROUCK",
            "Hauteur_D22": 20,
            "matelas_index": 1,
            "noyau": "LATEX MIXTE 7 ZONES",
            "quantite": 1
        }
    ]
}
```

## Prochaines étapes

L'étape de pré-import est maintenant prête pour être utilisée dans l'étape finale d'écriture Excel, où les champs nommés (`Client_D1`, `Adresse_D3`, `Hauteur_D22`) pourront être mappés vers des cellules Excel spécifiques. 