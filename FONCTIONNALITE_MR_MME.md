# 🧑‍💼 Extraction Automatique de Mr/Mme depuis les Produits

## 📋 Description de la fonctionnalité

Cette nouvelle fonctionnalité permet d'extraire automatiquement le titre (Mr ou Mme) depuis les **descriptions des produits** (matelas ou sommiers) extraites par le LLM et de l'ajouter comme nouveau champ dans le pré-import Excel.

## 🎯 Cas d'usage

Lorsque la description d'un produit (matelas ou sommier) contient "Mr" ou "Mme" (ex: "MATELAS 1 PIÈCE - Mr LOUCHART FREDERIC - HOUSSE MATELASSÉE", "SOMMIER RELAXATION - Mme DUBRULLE MARIE - 5 plis"), le système détecte automatiquement ce titre et l'inscrit dans le champ `MrMME_D4` du pré-import.

## ✅ Exemples de fonctionnement

| Description du produit | Titre extrait | Champ MrMME_D4 |
|----------------------|---------------|----------------|
| `MATELAS 1 PIÈCE - Mr LOUCHART FREDERIC - HOUSSE MATELASSÉE` | `Mr` | ✅ `Mr` |
| `SOMMIER RELAXATION - Mme DUBRULLE MARIE - 5 plis télescopique` | `Mme` | ✅ `Mme` |
| `MATELAS LATEX MIXTE - MR DEVERSENNE CLAUDE - 7 zones` | `Mr` | ✅ `Mr` |
| `SOMMIER À LATTES - MME BILAND JEAN - Structure en bois` | `Mme` | ✅ `Mme` |
| `MATELAS MOUSSE VISCO - 160x200 - Confort optimal` | `` | ✅ `` (aucun titre) |

## 🔧 Implémentation technique

### 1. **Fonction d'extraction** : `extraire_titre_depuis_produits()`

```python
def extraire_titre_depuis_produits(articles_llm: list) -> str:
    """
    Extrait le titre (Mr ou Mme) depuis les descriptions des produits (matelas/sommiers)
    
    Args:
        articles_llm (list): Liste des articles extraits par le LLM
        
    Returns:
        str: Titre extrait ("Mr", "Mme") ou chaîne vide si aucun titre trouvé
    """
    # Recherche dans toutes les descriptions d'articles
    for article in articles_llm:
        if isinstance(article, dict):
            description = article.get('description', '')
            if description:
                # Rechercher "Mr" ou "Mme" dans la description
                match = re.search(r'\b(Mr|Mme)\b', description, re.IGNORECASE)
                if match:
                    titre = match.group(1).upper()
                    # Normaliser "MR" en "Mr" et "MME" en "Mme"
                    if titre == "MR":
                        return "Mr"
                    elif titre == "MME":
                        return "Mme"
                    return titre
    
    return ""
```

### 2. **Intégration dans les données client**

Le titre extrait est ajouté au champ `titre` dans la structure des données client :

```python
def extraire_donnees_client(llm_data: dict) -> dict:
    # ... extraction des autres données client ...
    
    # Extraction du titre depuis les descriptions des produits
    articles_llm = []
    if isinstance(llm_data, dict):
        for key in llm_data:
            if isinstance(llm_data[key], list):
                articles_llm.extend(llm_data[key])
    
    client_data["titre"] = extraire_titre_depuis_produits(articles_llm)
    
    return client_data
```

### 3. **Ajout dans le pré-import**

Le nouveau champ `MrMME_D4` est ajouté dans la structure du pré-import :

```python
pre_import_item = {
    # Champs client
    "Client_D1": donnees_client.get("nom", ""),
    "Adresse_D3": donnees_client.get("adresse", ""),
    "MrMME_D4": donnees_client.get("titre", ""),  # Nouveau champ pour Mr/Mme
    
    # ... autres champs ...
}
```

### 4. **Affichage dans l'interface**

Le nouveau champ est affiché dans l'interface utilisateur :

```html
<li><strong>MrMME_D4:</strong> <span style="color:#1976d2;">{{ item.MrMME_D4 }}</span></li>
```

## 🎯 Avantages

1. **Automatisation** : Plus besoin de saisir manuellement "Mr" ou "Mme"
2. **Précision** : Extraction depuis les données réelles des produits
3. **Flexibilité** : Fonctionne avec "Mr", "Mme", "MR", "MME"
4. **Intégration** : Complètement intégré dans le workflow existant
5. **Mapping** : Disponible pour le mapping dans l'outil de configuration

## 🔄 Workflow complet

1. **Extraction LLM** : Le LLM extrait les descriptions des produits
2. **Détection titre** : La fonction `extraire_titre_depuis_produits()` analyse toutes les descriptions
3. **Intégration données** : Le titre est ajouté aux données client
4. **Pré-import** : Le champ `MrMME_D4` est créé avec la valeur extraite
5. **Affichage** : L'utilisateur voit le titre extrait dans l'interface
6. **Export** : Le titre est inclus dans l'export Excel final

## 📝 Notes importantes

- **Source des données** : L'extraction se fait depuis les descriptions des produits, pas depuis le nom du client
- **Priorité** : Le premier "Mr" ou "Mme" trouvé dans les descriptions est utilisé
- **Normalisation** : "MR" et "MME" sont automatiquement convertis en "Mr" et "Mme"
- **Cas d'absence** : Si aucun titre n'est trouvé, le champ reste vide
- **Validation** : Le champ est validé comme les autres champs du pré-import

## 🎉 Résultat

Cette fonctionnalité permet d'automatiser complètement l'extraction des titres "Mr" ou "Mme" depuis les descriptions des produits, améliorant l'efficacité et la précision du processus de pré-import.

## 🔄 Logique conditionnelle Excel

### **Nouvelle fonctionnalité ajoutée**
En plus de l'extraction automatique, une **logique conditionnelle** a été implémentée pour l'export Excel :

- **Si** une cellule de C28 à C44 contient "X"
- **Alors** la cellule D correspondante récupère automatiquement la valeur de `MrMME_D4`

### **Exemple concret**
```
Matelas 1: description = "MATELAS Mr DUPONT - LATEX NATUREL"
Matelas 2: description = "MATELAS Mme MARTIN - MOUSSE VISCO"

Cellule C28 = "X" → Cellule D28 = "Mr" (extraite de la description du matelas 1)
Cellule C30 = "X" → Cellule D30 = "Mme" (extraite de la description du matelas 2)
```

### **Documentation complète**
Voir le fichier `LOGIQUE_CONDITIONNELLE_MR_MME.md` pour tous les détails techniques. 