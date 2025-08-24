# 🧠 Noyaux de Traitement et Prompt LLM - Literie Processor

## 🎯 Vue d'ensemble

Literie Processor utilise une architecture modulaire avec des **noyaux spécialisés** pour chaque type de matelas et un **prompt LLM intelligent** pour l'analyse des devis. Cette approche garantit une précision maximale et une adaptabilité aux différents formats de devis.

## 🔧 Noyaux de Traitement Spécialisés

### 1. Latex Naturel (LN) - `latex_naturel_longueur_housse_utils.py`

#### **Fonctionnalités :**
- **Calcul automatique** des longueurs de housse selon la matière
- **Support des matières** : LUXE 3D, TENCEL, POLYESTER
- **Référentiel JSON** avec correspondances longueur/matière
- **Gestion des housses** simples et matelassées
- **Validation des dimensions** et formats

#### **Calculs effectués :**
```python
def get_latex_naturel_longueur_housse_value(longueur, matiere_housse):
    # Recherche dans le référentiel JSON
    # Correspondance longueur → matière housse
    # Retour de la valeur appropriée
```

#### **Référentiel utilisé :**
- **Fichier** : `latex_naturel_longueur_housse.json`
- **Structure** : `{"LONGUEUR": X, "LUXE_3D": Y, "TENCEL": Z, "POLYESTER": W}`
- **Logique** : Selon la longueur du matelas et la matière housse

---

### 2. Latex Mixte 7 Zones (LM7z) - `latex_mixte7zones_longueur_housse_utils.py`

#### **Fonctionnalités :**
- **Calcul des longueurs** de housse pour latex mixte
- **Support des 7 zones** de confort
- **Gestion des matières** housse : LUXE 3D, TENCEL, POLYESTER
- **Référentiel spécialisé** 7 zones
- **Validation des formats** de housse

#### **Calculs effectués :**
```python
def get_latex_mixte7zones_longueur_housse_value(longueur, matiere_housse):
    # Recherche dans le référentiel 7 zones
    # Correspondance longueur → matière housse
    # Retour de la valeur appropriée
```

#### **Référentiel utilisé :**
- **Fichier** : `latex_mixte7zones_longueur_housse.json`
- **Spécificité** : Optimisé pour les 7 zones de confort
- **Logique** : Adaptation selon la matière housse

---

### 3. Latex Mixte 3 Zones (LM3z) - `latex_mixte3zones_longueur_housse_utils.py`

#### **Fonctionnalités :**
- **Calcul des longueurs** de housse pour latex mixte 3 zones
- **Support des 3 zones** de confort
- **Gestion des matières** housse standard
- **Référentiel spécialisé** 3 zones
- **Validation des formats** de housse

#### **Calculs effectués :**
```python
def get_latex_mixte3zones_longueur_housse_value(longueur, matiere_housse):
    # Recherche dans le référentiel 3 zones
    # Correspondance longueur → matière housse
    # Retour de la valeur appropriée
```

#### **Référentiel utilisé :**
- **Fichier** : `latex_mixte3zones_longueur_housse.json`
- **Spécificité** : Optimisé pour les 3 zones de confort
- **Logique** : Adaptation selon la matière housse

---

### 4. Mousse Viscoélastique (MV) - `mousse_visco_utils.py`

#### **Fonctionnalités :**
- **Calcul automatique** selon la largeur du matelas
- **Support exclusif** de la matière TENCEL
- **Arrondi automatique** de la largeur pour correspondance
- **Préfixes automatiques** : 2x (1 pièce), 4x (jumeaux)
- **Référentiel spécialisé** viscoélastique

#### **Calculs effectués :**
```python
def get_mousse_visco_value(largeur, matiere_housse):
    # Arrondi de la largeur à l'entier le plus proche
    # Recherche dans le référentiel viscoélastique
    # Support exclusif TENCEL
    # Retour de la valeur appropriée

def get_mousse_visco_display_value(largeur, matiere_housse, quantite):
    # Application des préfixes selon la quantité
    # 2x pour 1 pièce, 4x pour jumeaux
    # Formatage pour l'affichage
```

#### **Référentiel utilisé :**
- **Fichier** : `mousse_visco_tencel.json`
- **Structure** : `{"MATELAS": X, "TENCEL": Y}`
- **Logique** : Largeur arrondie → valeur TENCEL

---

### 5. Mousse Rainurée 7 Zones (MR) - `mousse_rainuree7zones_longueur_housse_utils.py`

#### **Fonctionnalités :**
- **Calcul des longueurs** de housse pour mousse rainurée
- **Support des 7 zones** de confort
- **Gestion des matières** housse : LUXE 3D, TENCEL, POLYESTER
- **Référentiel spécialisé** rainuré 7 zones
- **Validation des formats** de housse

#### **Calculs effectués :**
```python
def get_mousse_rainuree7zones_longueur_housse_value(longueur, matiere_housse):
    # Recherche dans le référentiel rainuré 7 zones
    # Correspondance longueur → matière housse
    # Retour de la valeur appropriée
```

#### **Référentiel utilisé :**
- **Fichier** : `mousse_rainuree7zones_longueur_housse.json`
- **Spécificité** : Optimisé pour mousse rainurée 7 zones
- **Logique** : Adaptation selon la matière housse

---

### 6. Select 43 (SL43) - `select43_utils.py`

#### **Fonctionnalités :**
- **Calcul selon la largeur** et matière housse
- **Support des matières** : LUXE 3D, TENCEL, POLYESTER
- **Préfixes automatiques** selon matière et quantité
- **POLYESTER** : pas de préfixe
- **TENCEL/LUXE 3D** : 2x (1 pièce), 4x (jumeaux)
- **Référentiel spécialisé** Select 43

#### **Calculs effectués :**
```python
def get_select43_value(largeur, matiere_housse):
    # Recherche dans le référentiel Select 43
    # Mapping des matières vers les colonnes JSON
    # Retour de la valeur appropriée

def get_select43_display_value(largeur, matiere_housse, quantite):
    # Application des préfixes selon matière et quantité
    # POLYESTER : pas de préfixe
    # TENCEL/LUXE 3D : 2x/4x selon quantité
    # Formatage pour l'affichage
```

#### **Référentiel utilisé :**
- **Fichier** : `select43_tencel_luxe3d_tencel_polyester.json`
- **Structure** : `{"MATELAS": X, "LUXE_3D": Y, "TENCEL_S": Z, "POLY_S": W}`
- **Logique** : Largeur + matière → valeur avec préfixe

---

## 🤖 Prompt LLM - Intelligence Artificielle

### **Objectif Principal**
Analyser le texte brut d'un devis et extraire automatiquement toutes les informations pertinentes pour la production.

### **Instructions Détaillées du Prompt**

#### **0. Identification des dimensions du projet**
- **Format recherché** : `XXX/XXX` (ex: 160/200)
- **Localisation** : Ligne contenant "Literie" ou format de type "XXX / XXX"
- **Stockage** : Champ `"Dimension projet"`

#### **1. Extraction des matelas**
- **Description complète** : Sans rien omettre
- **Quantité** : Détection même si format "2x", "x2", "2,00", "2.00"
- **Gestion des colonnes** : Quantité dans colonne séparée
- **Stockage** : Section `"Matelas"` avec description + quantité

#### **2. Extraction des housses**
- **Description complète** : Sans rien omettre
- **Quantité** : Détection automatique
- **Stockage** : Section `"Housse"` avec description + quantité

#### **3. Extraction des pieds**
- **Description complète** : En tenant compte des packs (ex: "pack de 4 pieds")
- **Quantité** : Détection automatique
- **Stockage** : Section `"Pieds"` avec description + quantité

#### **4. Extraction des sommiers**
- **Critère principal** : Commence par "SOMMIER" ou "SOMMIERS"
- **Exclusion** : Ne jamais considérer un "LIT MOTORISÉ" comme sommier
- **Description complète** : Sans rien omettre
- **Stockage** : Section `"Sommier"` avec description + quantité

#### **5. Extraction des informations client**
- **Données recherchées** : Nom, adresse, email, téléphone, etc.
- **Stockage** : Section `"Client"` avec nom + adresse + dimension projet

#### **6. Regroupement des autres articles**
- **Catégorie** : `"Autres"`
- **Exclusion** : Lignes contenant uniquement remise, mention administrative, informations contractuelles
- **Inclusion** : Tous les articles non listés ci-dessus

#### **7. Détection des articles DOSSERET/TETE**
- **Recherche** : Articles contenant "DOSSERET" ou "TETE"
- **Gestion** : Majuscules/minuscules, avec/sans accents
- **Stockage** : Champ `"dosseret / tete"`

#### **8. Identification jumeaux/1 pièce**
- **Analyse** : Description du matelas
- **Détection** : Mots-clés "jumeaux", "1 pièce", etc.
- **Stockage** : Champ `"jumeau ou 1 pièce"`

#### **9. Transformation des dimensions**
- **Format d'entrée** : `XX/XXX` ou `XX / XXX`
- **Format de sortie** : `XX x XXX`
- **Stockage** : Champ `"dimension_housse"`

#### **10. Gestion des modes de mise à disposition**
- **Règles de détection** :
  - "enlèvement" ou "par vos soins" → `"ENLÈVEMENT CLIENT"`
  - "livraison", "livrer", "livré" → `"LIVRAISON"`
  - "expédition", "expédié" → `"EXPÉDITION"`

#### **11. Exclusion des éléments non pertinents**
- **Prix** : Montants, euros, etc.
- **Remises** : Pourcentages, réductions
- **Délais** : Dates de livraison, échéances
- **Mentions administratives** : Conditions, termes contractuels

### **Format de Sortie JSON Structuré**

```json
{
  "Matelas": [
    {
      "description": "...",
      "quantité": ...,
      "jumeau ou 1 pièce": "...",
      "dosseret / tete": "...",
      "dimension_housse": "..."
    }
  ],
  "Housse": [
    {
      "description": "...",
      "quantité": ...
    }
  ],
  "Pieds": [
    {
      "description": "...",
      "quantité": ...
    }
  ],
  "Sommier": [
    {
      "description": "...",
      "quantité": ...
    }
  ],
  "Autres": [
    {
      "description": "...",
      "quantité": ...
    }
  ],
  "Client": {
    "nom": "...",
    "adresse": "...",
    "Dimension projet": "..."
  }
}
```

### **Règles Spéciales de Traitement**

#### **Gestion des quantités dans colonnes séparées**
```
Exemple : 698,50     2,00   MATELAS JUMEAUX - LATEX 100% NATUREL ...
Résultat : Quantité = 2,00 associée à la description
```

#### **Détection des formats de dimensions variés**
```
Formats acceptés : 69/189, 69 / 189, 69/ 189
Transformation : 69 x 189
```

#### **Préservation des lignes de livraison/enlèvement**
```
Règle : Ne jamais supprimer une ligne contenant "remise" si elle contient 
également "enlèvement", "livraison" ou "expédition"
```

#### **Exclusion des mentions administratives**
```
Exclusions : Conditions générales, mentions légales, 
informations contractuelles non liées aux produits
```

#### **Validation des formats de sortie JSON**
```
Vérification : Structure JSON valide
Nettoyage : Suppression des caractères spéciaux
Formatage : Indentation et structure cohérente
```

---

## 🔄 Flux de Traitement Complet

### **1. Extraction PDF**
```
PDF → Texte brut → Nettoyage → Préparation pour LLM
```

### **2. Analyse LLM**
```
Texte brut → Prompt LLM → Réponse JSON → Parsing → Validation
```

### **3. Traitement par Noyaux**
```
Données JSON → Sélection noyau → Calculs spécialisés → Résultats formatés
```

### **4. Génération Excel**
```
Résultats → Mapping Excel → Écriture → Formatage → Sauvegarde
```

---

## 📊 Avantages de l'Architecture

### **Pour SCINNOVA (Développeur)**
- **Modularité** : Noyaux indépendants et réutilisables
- **Maintenabilité** : Code organisé et documenté
- **Évolutivité** : Ajout facile de nouveaux types de matelas
- **Testabilité** : Tests unitaires par noyau

### **Pour Westelynck (Utilisateur)**
- **Précision** : Calculs spécialisés par type de matelas
- **Fiabilité** : Validation automatique des données
- **Efficacité** : Traitement automatisé et rapide
- **Flexibilité** : Adaptation aux différents formats de devis

---

## 📞 Support Technique

### **Contact SCINNOVA**
- **Email** : sebastien.confrere@scinnova.fr
- **Téléphone** : 06.66.05.72.47
- **Éditeur** : SCINNOVA

### **Informations de Version**
- **Literie Processor** : v3.8.0
- **Noyaux** : 6 types spécialisés
- **Prompt LLM** : Optimisé pour devis matelas
- **Dernière mise à jour** : 17/07/2025

---

*Documentation technique - Développé par SCINNOVA pour SAS Literie Westelynck* 