# Extraction des Données Client

## Vue d'ensemble

Ce module permet d'extraire et de traiter automatiquement les informations client depuis l'extraction LLM des devis PDF. Les données client sont intégrées dans le JSON variable `Client` et affichées dans l'interface utilisateur.

## Fonctionnalités

### 1. Extraction du nom du client
- Récupération automatique du nom depuis l'extraction LLM
- Stockage dans le champ `client.nom`

### 2. Extraction et traitement de l'adresse
- Récupération de l'adresse complète depuis l'extraction LLM
- **Traitement spécial** : extraction de la ville uniquement (ce qui suit le code postal)
- Exemple : `"7 RUE DU MILIEU 59190 HAZEBROUCK"` → `"HAZEBROUCK"`
- Stockage dans le champ `client.adresse`

### 3. Extraction du code client
- Récupération du code client depuis l'extraction LLM
- Stockage dans le champ `client.code_client`

## Structure des données

```json
{
  "donnees_client": {
    "nom": "Mr LOUCHART FREDERIC",
    "adresse": "HAZEBROUCK",
    "code_client": "LOUCFSE"
  }
}
```

## Fichiers implémentés

### 1. `backend/client_utils.py`
Nouveau module utilitaire contenant :
- `extraire_donnees_client(llm_data)`: Fonction principale d'extraction
- `extraire_ville_adresse(adresse_complete)`: Extraction de la ville depuis l'adresse complète
- `valider_donnees_client(client_data)`: Validation des données client

### 2. `backend/main.py`
Modifications apportées :
- Import du module `client_utils`
- Intégration de l'extraction des données client dans le processus LLM
- Ajout des données client dans la structure de résultat

### 3. `backend/templates/index.html`
Modifications apportées :
- Affichage des données client extraites dans l'interface
- Section dédiée avec mise en forme visuelle

## Règles de traitement de l'adresse

### Format attendu
- Code postal français : 5 chiffres
- Format : `[ADRESSE] [CODE_POSTAL] [VILLE]`
- Exemple : `"7 RUE DU MILIEU 59190 HAZEBROUCK"`

### Extraction de la ville
- Pattern regex : `\b\d{5}\s+(.+)$`
- Extraction de tout ce qui suit le code postal de 5 chiffres
- Si pas de code postal détecté, retourne l'adresse complète

### Cas particuliers gérés
- Adresses sans code postal : retourne l'adresse complète
- Codes postaux étrangers (4 ou 6 chiffres) : non reconnus comme codes postaux français
- Espaces multiples : normalisés automatiquement

## Tests

### Fichiers de test créés
1. `test_client_extraction.py` : Tests unitaires des fonctions d'extraction
2. `test_integration_client.py` : Tests d'intégration avec le backend complet

### Exécution des tests
```bash
python3 test_client_extraction.py
python3 test_integration_client.py
```

### Exemples de tests
```python
# Test d'extraction basique
llm_data = {
    "client": {
        "nom": "Mr LOUCHART FREDERIC",
        "adresse": "7 RUE DU MILIEU 59190 HAZEBROUCK",
        "code_client": "LOUCFSE"
    }
}
donnees_client = extraire_donnees_client(llm_data)
# Résultat: {'nom': 'Mr LOUCHART FREDERIC', 'adresse': 'HAZEBROUCK', 'code_client': 'LOUCFSE'}
```

## Intégration dans le workflow

1. **Upload PDF** : L'utilisateur upload un devis PDF
2. **Extraction LLM** : Le LLM extrait les données structurées (incluant les données client)
3. **Traitement client** : Les données client sont extraites et traitées
4. **Affichage** : Les données client sont affichées dans l'interface avec les autres résultats

## Validation des données

La fonction `valider_donnees_client()` vérifie :
- Présence du nom du client (obligatoire)
- Présence de l'adresse (obligatoire)
- Cohérence générale des données

## Logs et monitoring

Le module génère des logs détaillés :
- Extraction réussie des données client
- Erreurs de parsing ou d'extraction
- Cas où aucun code postal n'est détecté
- Validation des données

## Compatibilité

- Compatible avec les formats d'adresse français
- Gestion gracieuse des cas d'erreur
- Rétrocompatible avec l'existant
- Pas d'impact sur les autres fonctionnalités

## Utilisation

Les données client sont automatiquement extraites lors de l'analyse LLM d'un devis. Aucune action supplémentaire n'est requise de la part de l'utilisateur.

### Affichage dans l'interface
Les données client apparaissent dans une section dédiée avec :
- Nom du client
- Ville (extrait de l'adresse)
- Code client

### Accès programmatique
```python
# Dans le résultat du backend
result = {
    "donnees_client": {
        "nom": "Mr LOUCHART FREDERIC",
        "adresse": "HAZEBROUCK",
        "code_client": "LOUCFSE"
    }
}
``` 