# 📏 Documentation - Tableau de Hauteur des Matelas

## 🎯 Vue d'Ensemble

Le **Tableau de Hauteur des Matelas** est un système complet de gestion des hauteurs standardisées pour tous les types de matelas. Il remplace l'ancien système simple par une solution plus robuste et extensible.

## 📁 Fichiers Créés

### 1. **`backend/tableau_hauteur.py`**
- Tableau de référence en Python avec toutes les hauteurs
- Fonctions utilitaires pour la gestion des hauteurs
- Compatible avec l'ancien système

### 2. **`backend/Référentiels/tableau_hauteur_matelas.json`**
- Données structurées en JSON
- Métadonnées complètes pour chaque type de noyau
- Catégorisation et statistiques

### 3. **`backend/tableau_hauteur_utils.py`**
- Gestionnaire principal pour charger et utiliser les données JSON
- Fonctions avancées de recherche et d'analyse
- Export CSV et autres fonctionnalités

### 4. **`test_tableau_hauteur.py`**
- Script de test complet
- Vérification de compatibilité avec l'ancien système
- Tests de performance et fonctionnalités

## 📊 Structure des Données

### Hauteurs par Type de Noyau

| Type de Noyau | Hauteur (cm) | Catégorie | Densité | Zones |
|---------------|--------------|-----------|---------|-------|
| **LATEX NATUREL** | 10 | LATEX | haute | Non |
| **LATEX MIXTE 7 ZONES** | 9 | LATEX | moyenne | Oui |
| **LATEX RENFORCE** | 8 | LATEX | très haute | Non |
| **MOUSSE RAINUREE 7 ZONES** | 9 | MOUSSE | moyenne | Oui |
| **MOUSSE VISCO** | 10 | MOUSSE | haute | Non |
| **SELECT 43** | 8 | SELECT | très haute | Non |

### Détails Techniques

Chaque type de noyau contient :
- **hauteur_cm** : Hauteur totale en centimètres
- **description** : Description détaillée du type
- **epaisseur_noyau** : Épaisseur du noyau en cm
- **epaisseur_housse** : Épaisseur de la housse en cm
- **categorie** : Catégorie (LATEX, MOUSSE, SELECT)
- **densite** : Niveau de densité
- **zones** : Présence de zones de confort

## 🔧 Utilisation

### Import et Utilisation Simple

```python
# Import du nouveau système
from backend.tableau_hauteur_utils import calculer_hauteur_matelas

# Utilisation identique à l'ancien système
hauteur = calculer_hauteur_matelas("LATEX NATUREL")  # Retourne 10
```

### Utilisation Avancée

```python
from backend.tableau_hauteur_utils import tableau_hauteur

# Informations complètes
info = tableau_hauteur.obtenir_info_complete("LATEX MIXTE 7 ZONES")
print(info)
# {
#     'hauteur_cm': 9,
#     'description': 'Matelas latex mixte avec zones de confort',
#     'epaisseur_noyau': 7,
#     'epaisseur_housse': 2,
#     'categorie': 'LATEX',
#     'densite': 'moyenne',
#     'zones': True
# }

# Recherche par hauteur
noyaux_10cm = tableau_hauteur.lister_noyaux_par_hauteur(10)
# ['LATEX NATUREL', 'MOUSSE VISCO']

# Statistiques par catégorie
stats_latex = tableau_hauteur.obtenir_statistiques_categorie("LATEX")
# {'hauteur_min': 8, 'hauteur_max': 10, 'hauteur_moyenne': 9, ...}
```

## 🚀 Nouvelles Fonctionnalités

### 1. **Recherche et Filtrage**
```python
# Tous les noyaux disponibles
tous_noyaux = tableau_hauteur.lister_tous_noyaux()

# Noyaux par catégorie
categorie = tableau_hauteur.obtenir_categorie_noyau("LATEX NATUREL")
```

### 2. **Export de Données**
```python
# Export en CSV
tableau_hauteur.exporter_tableau_csv("hauteurs_matelas.csv")
```

### 3. **Affichage Complet**
```python
# Affichage formaté du tableau complet
tableau_hauteur.afficher_tableau_complet()
```

## 🔄 Compatibilité

### Migration depuis l'Ancien Système

Le nouveau système est **100% compatible** avec l'ancien :

```python
# Ancien système (toujours fonctionnel)
from backend.hauteur_utils import calculer_hauteur_matelas

# Nouveau système (même interface)
from backend.tableau_hauteur_utils import calculer_hauteur_matelas

# Les deux retournent exactement les mêmes résultats
```

### Tests de Compatibilité

Le script `test_tableau_hauteur.py` vérifie automatiquement :
- ✅ Identité des résultats entre ancien et nouveau système
- ✅ Fonctionnement de toutes les nouvelles fonctionnalités
- ✅ Performance et rapidité d'exécution
- ✅ Export et import des données

## 📈 Avantages du Nouveau Système

### 1. **Données Structurées**
- Informations complètes pour chaque type de noyau
- Métadonnées détaillées (densité, zones, etc.)
- Catégorisation automatique

### 2. **Flexibilité**
- Données stockées en JSON (facilement modifiables)
- Fonctions de recherche avancées
- Export dans différents formats

### 3. **Maintenabilité**
- Code modulaire et extensible
- Documentation intégrée
- Tests automatisés

### 4. **Performance**
- Chargement rapide des données JSON
- Cache automatique des données
- Optimisé pour les appels répétés

## 🛠️ Maintenance et Évolution

### Ajout d'un Nouveau Type de Noyau

1. **Modifier le fichier JSON** :
```json
{
  "NOUVEAU NOYAU": {
    "hauteur_cm": 11,
    "description": "Description du nouveau noyau",
    "epaisseur_noyau": 9,
    "epaisseur_housse": 2,
    "categorie": "LATEX",
    "densite": "haute",
    "zones": false
  }
}
```

2. **Mettre à jour les catégories** si nécessaire
3. **Lancer les tests** pour vérifier la compatibilité

### Modification des Hauteurs Existantes

1. Modifier directement le fichier JSON
2. Les changements sont automatiquement pris en compte
3. Aucune modification de code requise

## 📋 Exemples d'Utilisation

### Dans l'Interface GUI

```python
# Dans app_gui.py ou aide_generateur_preimport.py
from backend.tableau_hauteur_utils import calculer_hauteur_matelas

# Calcul automatique de la hauteur
if noyau:
    hauteur_calc = calculer_hauteur_matelas(noyau)
    if hauteur_calc:
        self.input_hauteur.setText(str(hauteur_calc))
```

### Dans les Utilitaires Backend

```python
# Dans matelas_utils.py ou autres modules
from backend.tableau_hauteur_utils import tableau_hauteur

# Validation des données
def valider_hauteur_matelas(noyau, hauteur_saisie):
    hauteur_standard = tableau_hauteur.obtenir_hauteur(noyau)
    if hauteur_saisie != hauteur_standard:
        return f"Hauteur non standard: {hauteur_standard}cm attendu"
    return "OK"
```

## 🔍 Dépannage

### Problèmes Courants

1. **Fichier JSON non trouvé**
   - Vérifier le chemin : `backend/Référentiels/tableau_hauteur_matelas.json`
   - Le système utilise des données par défaut si le fichier est manquant

2. **Erreur de décodage JSON**
   - Vérifier la syntaxe JSON
   - Utiliser un validateur JSON en ligne

3. **Résultats différents de l'ancien système**
   - Lancer `python3 test_tableau_hauteur.py`
   - Vérifier la compatibilité automatiquement

### Logs et Debug

```python
# Activer les logs détaillés
import logging
logging.basicConfig(level=logging.DEBUG)

# Vérifier le chargement des données
print(f"Données chargées: {tableau_hauteur._data is not None}")
```

## 📞 Support

Pour toute question ou problème :
1. Consulter les tests : `python3 test_tableau_hauteur.py`
2. Vérifier la documentation JSON
3. Utiliser les fonctions de debug intégrées

---

**Version** : 1.0  
**Date** : 2025-07-22  
**Auteur** : MatelasApp System 