# 🔢 Extraction Automatique des Numéros de Commande

## 📋 Description de la fonctionnalité

Cette nouvelle fonctionnalité permet d'extraire automatiquement le numéro de commande du nom de fichier PDF et de pré-remplir le champ "Commande/Client" correspondant dans l'interface.

## 🎯 Cas d'usage

Lorsque vous sélectionnez des fichiers PDF dont le nom contient un numéro (ex: "Commande GALOO 435.pdf"), le système détecte automatiquement ce numéro et l'inscrit dans le champ de commande correspondant.

## ✅ Exemples de fonctionnement

| Nom de fichier | Numéro extrait | Champ pré-rempli |
|----------------|----------------|------------------|
| `Commande GALOO 435.pdf` | `435` | ✅ `435` |
| `Commande BECUE 427.pdf` | `427` | ✅ `427` |
| `Commande CANFIN 418.pdf` | `418` | ✅ `418` |
| `Commande Dethoor.pdf` | (aucun) | ✅ (vide) |
| `Devis test 2.pdf` | `2` | ✅ `2` |
| `Commande 12345.pdf` | `12345` | ✅ `12345` |

## 🔧 Implémentation technique

### Fonction utilitaire

```python
def extract_commande_number(filename):
    """
    Extrait le numéro de commande du nom de fichier.
    Recherche un chiffre dans le nom de fichier (ex: 'Commande GALOO 435' -> '435')
    
    Args:
        filename (str): Nom du fichier
        
    Returns:
        str: Numéro de commande trouvé ou chaîne vide si aucun numéro trouvé
    """
    # Rechercher un ou plusieurs chiffres dans le nom de fichier
    match = re.search(r'\d+', filename)
    if match:
        return match.group()
    return ""
```

### Intégration dans l'interface

La fonction est appelée dans `select_files()` lors de la création des champs de commande :

```python
# Extraire le numéro de commande du nom de fichier et pré-remplir le champ
filename = os.path.basename(file)
commande_number = extract_commande_number(filename)
if commande_number:
    lineedit.setText(commande_number)
    if hasattr(self, 'app_logger') and self.app_logger:
        self.app_logger.info(f"Numéro de commande extrait automatiquement: {commande_number} pour {filename}")
```

## 📝 Logs

L'extraction automatique est loggée dans les fichiers de log de l'application :

```
2025-07-21 22:45:30 - LiterieApp - INFO - Numéro de commande extrait automatiquement: 435 pour Commande GALOO 435.pdf
```

## 🎨 Avantages

1. **Gain de temps** : Plus besoin de saisir manuellement les numéros de commande
2. **Réduction d'erreurs** : Évite les erreurs de saisie
3. **Cohérence** : Assure que le numéro de commande correspond exactement au fichier
4. **Flexibilité** : Fonctionne avec tous les formats de noms contenant des chiffres

## 🔍 Détails techniques

- **Expression régulière** : `r'\d+'` pour détecter un ou plusieurs chiffres consécutifs
- **Première occurrence** : Si plusieurs chiffres sont présents, seul le premier groupe est extrait
- **Gestion des cas limites** : Retourne une chaîne vide si aucun chiffre n'est trouvé
- **Compatibilité** : Fonctionne avec ou sans extension de fichier

## 🧪 Tests

La fonctionnalité a été testée avec les cas suivants :
- ✅ Fichiers avec numéros de commande classiques
- ✅ Fichiers sans numéro
- ✅ Fichiers avec plusieurs chiffres
- ✅ Fichiers avec années (2024, 2025)
- ✅ Fichiers avec numéros simples (2, 3, etc.)

## 📅 Version

Cette fonctionnalité a été ajoutée dans la version actuelle de l'application. 