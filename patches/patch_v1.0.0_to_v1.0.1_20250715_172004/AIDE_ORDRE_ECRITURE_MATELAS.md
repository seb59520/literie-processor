# Aide - Ordre d'Écriture des Matelas dans Excel

## 📋 Vue d'Ensemble

Ce document explique comment les matelas sont organisés et écrits dans les fichiers Excel lors de l'export automatique. L'ordre d'écriture suit une logique précise pour garantir la cohérence et la lisibilité des données de production.

## 🎯 Principe de Tri

Les matelas sont écrits dans le fichier Excel selon **deux niveaux de tri** :

### 1. **Tri par type de noyau** (Ordre configurable)
Les matelas sont d'abord triés selon l'ordre des noyaux défini dans la configuration. Cet ordre peut être personnalisé via l'interface graphique.

### 2. **Ordre des blocs dans Excel** (Ordre fixe)
Une fois triés par noyau, les matelas sont écrits dans les blocs Excel selon un ordre strict prédéfini.

## 📊 Ordre par Défaut des Noyaux

L'ordre standard des noyaux (du premier au dernier) :

1. **MOUSSE VISCO**
2. **LATEX NATUREL** 
3. **LATEX MIXTE 7 ZONES**
4. **MOUSSE RAINUREE 7 ZONES**
5. **LATEX RENFORCÉ**
6. **SELECT 43**

## 🔄 Ordre des Blocs Excel

Les matelas sont écrits dans les blocs Excel selon cet ordre strict :

| Position | Bloc Excel | Colonnes | Description |
|----------|------------|----------|-------------|
| 1 | **Cas 1** | C & D | Premier matelas |
| 2 | **Cas 2** | E & F | Deuxième matelas |
| 3 | **Cas 3** | G & H | Troisième matelas |
| 4 | **Cas 4** | I & J | Quatrième matelas |
| 5 | **Cas 5** | K & L | Cinquième matelas |
| 6 | **⚠️ Bloc verrouillé** | M & N | **Sauté** (protégé) |
| 7 | **Cas 6** | O & P | Sixième matelas |
| 8 | **Cas 7** | Q & R | Septième matelas |
| 9 | **Cas 8** | S & T | Huitième matelas |
| 10 | **Cas 9** | U & V | Neuvième matelas |
| 11 | **Cas 10** | W & X | Dixième matelas |

## 📝 Exemple Concret

### Données d'entrée
Supposons que vous ayez 4 matelas avec ces caractéristiques :

| Client | Noyau | Description |
|--------|-------|-------------|
| Client A | **LATEX NATUREL** | Matelas 160x200 |
| Client B | **MOUSSE VISCO** | Matelas 140x190 |
| Client C | **LATEX MIXTE 7 ZONES** | Matelas 180x200 |
| Client D | **SELECT 43** | Matelas 90x190 |

### Ordre d'écriture dans Excel

**Résultat dans le fichier Excel :**

| Bloc | Colonnes | Noyau | Client | Raison |
|------|----------|-------|--------|--------|
| **Cas 1** | C & D | **LATEX NATUREL** | Client A | 1er dans l'ordre des noyaux |
| **Cas 2** | E & F | **MOUSSE VISCO** | Client B | 2ème dans l'ordre des noyaux |
| **Cas 3** | G & H | **LATEX MIXTE 7 ZONES** | Client C | 3ème dans l'ordre des noyaux |
| **Cas 4** | I & J | **SELECT 43** | Client D | 6ème dans l'ordre des noyaux |

## ⚙️ Personnalisation de l'Ordre

### Comment modifier l'ordre des noyaux

1. **Ouvrir l'interface graphique** de l'application
2. Aller dans le menu **Configuration**
3. Sélectionner **Classement des noyaux**
4. **Glisser-déposer** les noyaux pour les réorganiser
5. Cliquer sur **OK** pour sauvegarder

### Exemple de réorganisation

**Ordre personnalisé :**
1. **LATEX NATUREL** (priorité haute)
2. **LATEX MIXTE 7 ZONES** (priorité moyenne)
3. **MOUSSE VISCO** (priorité basse)
4. **MOUSSE RAINUREE 7 ZONES**
5. **LATEX RENFORCÉ**
6. **SELECT 43**

**Résultat :** Les matelas LATEX NATUREL apparaîtront toujours en premier dans Excel.

## 📁 Gestion des Fichiers Multiples

### Règle de création de nouveaux fichiers

- **Maximum 10 matelas** par fichier Excel
- **Nouveau fichier automatique** au-delà de 10 matelas
- **Même ordre respecté** dans tous les fichiers

### Exemple avec 15 matelas

| Fichier | Matelas | Blocs utilisés |
|---------|---------|----------------|
| **Matelas_S25_2025_1.xlsx** | 1 à 10 | Cas 1 à 10 |
| **Matelas_S25_2025_2.xlsx** | 11 à 15 | Cas 1 à 5 |

## 🔧 Fonctionnement Technique

### Algorithme de tri

1. **Collecte globale** : Tous les matelas de tous les fichiers PDF sont collectés
2. **Tri par noyau** : Application de l'ordre configuré des noyaux
3. **Écriture séquentielle** : Écriture dans les blocs Excel dans l'ordre fixe
4. **Gestion des fichiers** : Création automatique de nouveaux fichiers si nécessaire

### Avantages de cette approche

- ✅ **Cohérence** : Même ordre dans tous les exports
- ✅ **Lisibilité** : Organisation logique par type de noyau
- ✅ **Flexibilité** : Ordre personnalisable selon les besoins
- ✅ **Automatisation** : Aucune intervention manuelle requise

## 🚨 Cas Particuliers

### Noyaux non listés dans l'ordre

Si un noyau n'est pas défini dans l'ordre configuré :
- Il est placé **à la fin** de la liste
- Un message d'avertissement est affiché dans les logs

### Bloc M-N verrouillé

Le bloc M-N est **toujours sauté** car il est protégé dans le template Excel.

### Matelas sans noyau détecté

Les matelas avec le noyau "INCONNU" :
- Sont placés **à la fin** de la liste
- Un message d'avertissement est affiché

## 📋 Vérification de l'Ordre

### Dans les logs de l'application

```
2025-01-27 14:30:15 - backend_interface - INFO - Ordre des noyaux pour tri global: ['LATEX NATUREL', 'MOUSSE VISCO', 'LATEX MIXTE 7 ZONES']
2025-01-27 14:30:15 - backend_interface - INFO - Noyaux présents dans les pré-imports: ['LATEX MIXTE 7 ZONES', 'LATEX NATUREL', 'MOUSSE VISCO']
2025-01-27 14:30:15 - backend_interface - INFO - Pré-imports triés selon l'ordre global défini
```

### Dans l'interface graphique

L'ordre final est visible dans la section **Configurations Matelas** de l'interface.

## 🎯 Bonnes Pratiques

### Pour optimiser l'ordre

1. **Définir l'ordre des noyaux** selon vos priorités de production
2. **Tester avec quelques fichiers** avant de traiter de gros volumes
3. **Vérifier les logs** pour s'assurer du bon tri
4. **Documenter l'ordre choisi** pour l'équipe

### Pour la maintenance

1. **Sauvegarder la configuration** régulièrement
2. **Vérifier l'ordre** après chaque mise à jour
3. **Former les utilisateurs** sur la personnalisation de l'ordre

---

## 📞 Support

Si vous avez des questions sur l'ordre d'écriture des matelas :

1. **Consultez les logs** de l'application
2. **Vérifiez la configuration** des noyaux
3. **Testez avec un fichier simple** pour valider l'ordre
4. **Contactez l'équipe technique** si nécessaire

---

**Document créé le :** 2025-01-27  
**Version :** 1.0  
**Dernière mise à jour :** 2025-01-27 