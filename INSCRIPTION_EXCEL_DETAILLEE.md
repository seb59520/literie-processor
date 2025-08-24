# 📊 Inscription Excel Détaillée - MatelasApp

## 🎯 Vue d'ensemble

Ce document détaille le processus d'inscription Excel automatique de MatelasApp, incluant tous les champs disponibles pour les matelas et la structure des fichiers générés.

## 📋 Structure des fichiers Excel

### Organisation des blocs de colonnes

Chaque fichier Excel contient **10 cas de matelas** répartis en blocs de colonnes :

| Cas | Colonnes | Description |
|-----|----------|-------------|
| 1 | C-D | Premier matelas |
| 2 | E-F | Deuxième matelas |
| 3 | G-H | Troisième matelas |
| 4 | I-J | Quatrième matelas |
| 5 | K-L | Cinquième matelas |
| 6 | O-P | Sixième matelas (M-N verrouillées) |
| 7 | Q-R | Septième matelas |
| 8 | S-T | Huitième matelas |
| 9 | U-V | Neuvième matelas |
| 10 | W-X | Dixième matelas |

### Numérotation continue

- **Fichier 1** : Cas 1-10
- **Fichier 2** : Cas 11-20
- **Fichier 3** : Cas 21-30
- etc.

## 📝 Champs disponibles pour les matelas

### 1. Informations client et commande

| Champ | Position | Description |
|-------|----------|-------------|
| `Client_D1` | D1 | Nom du client |
| `Adresse_D3` | D3 | Adresse complète du client |
| `numero_D2` | D2 | Numéro de commande |
| `semaine_D5` | D5 | Semaine de production |
| `lundi_D6` | D6 | Date du lundi de la semaine |
| `vendredi_D7` | D7 | Date du vendredi de la semaine |

### 2. Dimensions et mesures

| Champ | Position | Description |
|-------|----------|-------------|
| `Hauteur_D22` | D22 | Hauteur du matelas |
| `dimension_housse_D23` | D23 | Dimensions de la housse |
| `longueur_D24` | D24 | Longueur du matelas |
| `decoupe_noyau_D25` | D25 | Découpe du noyau |

### 3. Quantités et détection

| Champ | Position | Description |
|-------|----------|-------------|
| `jumeaux_C10` | C10 | Indication jumeaux (colonne C) |
| `jumeaux_D10` | D10 | Indication jumeaux (colonne D) |
| `1piece_C11` | C11 | Quantité 1 pièce (colonne C) |
| `1piece_D11` | D11 | Quantité 1 pièce (colonne D) |
| `dosseret_tete_C8` | C8 | Détection dosseret/tête |

### 4. Housse et matière

| Champ | Position | Description |
|-------|----------|-------------|
| `HSimple_polyester_C13` | C13 | Housse simple polyester (C) |
| `HSimple_polyester_D13` | D13 | Housse simple polyester (D) |
| `HSimple_tencel_C14` | C14 | Housse simple tencel (C) |
| `HSimple_tencel_D14` | D14 | Housse simple tencel (D) |
| `HSimple_autre_C15` | C15 | Housse simple autre (C) |
| `HSimple_autre_D15` | D15 | Housse simple autre (D) |
| `Hmat_polyester_C17` | C17 | Housse matelassée polyester (C) |
| `Hmat_polyester_D17` | D17 | Housse matelassée polyester (D) |
| `Hmat_tencel_C18` | C18 | Housse matelassée tencel (C) |
| `Hmat_tencel_D18` | D18 | Housse matelassée tencel (D) |
| `Hmat_luxe3D_C19` | C19 | Housse matelassée luxe 3D (C) |
| `Hmat_luxe3D_D19` | D19 | Housse matelassée luxe 3D (D) |
| `poignees_C20` | C20 | Poignées |

### 5. Types de noyau et fermeté

| Champ | Position | Description |
|-------|----------|-------------|
| `LN_Ferme_C28` | C28 | Latex Naturel Ferme |
| `LN_Medium_C29` | C29 | Latex Naturel Medium |
| `LM7z_Ferme_C30` | C30 | Latex Mixte 7 Zones Ferme |
| `LM7z_Medium_C31` | C31 | Latex Mixte 7 Zones Medium |
| `LM3z_Ferme_C32` | C32 | Latex Mixte 3 Zones Ferme |
| `LM3z_Medium_C33` | C33 | Latex Mixte 3 Zones Medium |
| `MV_Ferme_C34` | C34 | Mousse Viscoélastique Ferme |
| `MV_Medium_C35` | C35 | Mousse Viscoélastique Medium |
| `MV_Confort_C36` | C36 | Mousse Viscoélastique Confort |
| `MR_Ferme_C37` | C37 | Mousse Rainurée Ferme |
| `MR_Medium_C38` | C38 | Mousse Rainurée Medium |
| `MR_Confort_C39` | C39 | Mousse Rainurée Confort |
| `SL43_Ferme_C40` | C40 | Select 43 Ferme |
| `SL43_Medium_C41` | C41 | Select 43 Medium |

### 6. Options supplémentaires

| Champ | Position | Description |
|-------|----------|-------------|
| `Surmatelas_C45` | C45 | Surmatelas |
| `emporte_client_C57` | C57 | Emporté client |
| `fourgon_C58` | C58 | Fourgon |
| `transporteur_C59` | C59 | Transporteur |

## 🔧 Fonctionnalités d'inscription

### Alignement automatique
- **Toutes les cellules** sont automatiquement centrées
- **Alignement intelligent** selon le type de données
- **Préservation** de la mise en forme du template

### Coloration conditionnelle
- **Activation automatique** selon les valeurs
- **Désactivation** quand les champs sont vides
- **Cohérence visuelle** entre les blocs

### Numérotation continue
- **Cas 1-10** dans le premier fichier
- **Cas 11-20** dans le deuxième fichier
- **Continuation automatique** pour les gros volumes

### Validation des données
- **Vérification** avant inscription
- **Gestion des erreurs** automatique
- **Logs détaillés** des opérations

## 📊 Processus d'inscription

### 1. Préparation des données
```
Extraction PDF → Analyse LLM → Structuration JSON → Validation
```

### 2. Mapping des champs
```
JSON → Mapping → Cellules Excel → Alignement → Coloration
```

### 3. Écriture dans Excel
```
Template → Bloc vide → Écriture → Validation → Sauvegarde
```

## 🎨 Formatage automatique

### Styles appliqués
- **Police** : Arial 11pt
- **Alignement** : Centré horizontal et vertical
- **Bordures** : Selon le template
- **Couleurs** : Selon les règles de coloration

### Règles de coloration
- **Activation** : Quand la valeur est présente
- **Désactivation** : Quand la cellule est vide
- **Cohérence** : Entre colonnes C et D du même bloc

## 📁 Gestion des fichiers

### Nommage automatique
```
Format : Matelas_S{XX}_{YYYY}_{N}.xlsx
Exemple : Matelas_S29_2025_1.xlsx
```

### Organisation
- **Un fichier** par 10 matelas maximum
- **Numérotation** continue entre fichiers
- **Sauvegarde** dans le dossier Downloads

## 🔍 Dépannage

### Problèmes courants
1. **Template manquant** : Vérifier `template/template_matelas.xlsx`
2. **Permissions** : Vérifier les droits d'écriture
3. **Espace disque** : Vérifier l'espace disponible

### Logs de diagnostic
- **Fichier** : `logs/matelas_app.log`
- **Niveau** : DEBUG pour les détails
- **Informations** : Chaque opération d'écriture

## 📞 Support technique

### Contact SCINNOVA
- **Email** : sebastien.confrere@scinnova.fr
- **Téléphone** : 06.66.05.72.47
- **Éditeur** : SCINNOVA

### Informations de version
- **MatelasApp** : v3.8.0
- **Template Excel** : Compatible Excel 2016+
- **Dernière mise à jour** : 17/07/2025

---

*Documentation technique - Développé par SCINNOVA pour SAS Literie Westelynck* 