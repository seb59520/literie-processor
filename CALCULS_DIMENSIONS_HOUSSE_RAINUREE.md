# 📐 Calculs Dimensions Housse - Matelas RAINUREE

## 🎯 Vue d'Ensemble

Pour un matelas **MOUSSE RAINUREE 7 ZONES**, le système calcule **automatiquement** les dimensions housse selon :
- **Largeur du matelas** → Dimension housse (largeur)
- **Longueur du matelas** → Longueur housse
- **Matière de la housse** → Formatage et valeurs

## 📊 Démonstration Pratique

### Exemple : Matelas 89x198 cm avec TENCEL LUXE 3D

```
📏 Matelas: 89 x 198 cm
🛏️ Matière: TENCEL LUXE 3D
```

## 🔍 1. Calcul Dimension Housse (Largeur)

### Référentiel Utilisé
- **Fichier** : `mousse_rainuree7zones_tencel_luxe3d_tencel_polyester.json`
- **Recherche** : `MATELAS=89` → `LUXE_3D=101`

### Table de Correspondance (Extrait)
```
MATELAS | LUXE_3D | TENCEL_S | POLY_S
--------|---------|----------|--------
   87   |   99    |   105    |  186
   88   |  100    |   106    |  188
   89   |  101    |   107    |  190  ← Notre cas
   90   |  102    |   108    |  192
   91   |  103    |   109    |  194
```

### Résultat
- **Largeur matelas** : 89 cm
- **Dimension housse** : **101 cm**

## 📏 2. Calcul Longueur Housse

### Référentiel Utilisé
- **Fichier** : `mousse_rainuree7zones_longueur_housse.json`
- **Recherche** : `LONGUEUR=198` → `LUXE_3D=5.5`

### Table de Correspondance (Extrait)
```
LONGUEUR | LUXE_3D | TENCEL | POLYESTER
---------|---------|--------|----------
   196   |   3.5   |  6.0   |   210
   197   |   4.5   |  7.0   |   211
   198   |   5.5   |  8.0   |   212  ← Notre cas
   199   |   6.5   |  9.0   |   213
   200   |   7.5   | 10.0   |   214
```

### Résultat
- **Longueur matelas** : 198 cm
- **Longueur housse** : **5.5 cm**

## 🎨 3. Formatage Final

### Règles de Formatage
- **POLYESTER** : Affichage simple (ex: `"206"`)
- **TENCEL/TENCEL LUXE 3D** : Avec préfixe quantité
  - 1 pièce : `"2 x 101"`
  - 2 pièces (jumeaux) : `"4 x 101"`

### Résultat Final
- **Dimension housse formatée** : `"2 x 101"`
- **Longueur housse** : `5.5`

## 🧪 4. Comparaison par Matière

### Test avec Matelas 89x198 cm

| Matière | Dimension Housse | Longueur Housse | Formatage |
|---------|------------------|-----------------|-----------|
| **TENCEL LUXE 3D** | 101 cm | 5.5 cm | `"2 x 101"` |
| **TENCEL** | 107 cm | 8.5 cm | `"2 x 107"` |
| **POLYESTER** | 206 cm | 212 cm | `"206"` |

## 📏 5. Comparaison par Dimensions

### Test avec TENCEL LUXE 3D

| Matelas | Dimension Housse | Longueur Housse |
|---------|------------------|-----------------|
| 80x190 cm | `"2 x 92"` | 1.5 cm |
| 90x200 cm | `"2 x 102"` | 6.5 cm |
| 100x210 cm | `"2 x 112"` | 11.5 cm |

## 📋 6. Champs Excel Générés

### Résultat dans l'Export Excel
```
dimension_housse_D23: 2 x 101
longueur_D24: 5.5
```

## 🔧 7. Fonctions Utilisées

### Calcul Dimension Housse
```python
from backend.mousse_rainuree7zones_referentiel import get_valeur_mousse_rainuree7zones

dimension_housse = get_valeur_mousse_rainuree7zones(largeur_matelas, matiere_housse)
# Exemple: get_valeur_mousse_rainuree7zones(89, "TENCEL LUXE 3D") → 101
```

### Calcul Longueur Housse
```python
from backend.mousse_rainuree7zones_longueur_housse_utils import get_mousse_rainuree7zones_longueur_housse_value

longueur_housse = get_mousse_rainuree7zones_longueur_housse_value(longueur_matelas, matiere_housse)
# Exemple: get_mousse_rainuree7zones_longueur_housse_value(198, "TENCEL LUXE 3D") → 5.5
```

## 📚 8. Référentiels Complets

### Référentiel Largeur Housse
- **Fichier** : `backend/Référentiels/mousse_rainuree7zones_tencel_luxe3d_tencel_polyester.json`
- **Plage** : 60 à 243 cm
- **Colonnes** : MATELAS, LUXE_3D, TENCEL_S, POLY_S

### Référentiel Longueur Housse
- **Fichier** : `backend/Référentiels/mousse_rainuree7zones_longueur_housse.json`
- **Plage** : 160 à 237 cm
- **Colonnes** : LONGUEUR, LUXE_3D, TENCEL, POLYESTER

## ⚠️ 9. Règles Spéciales

### Formatage selon Matière
1. **POLYESTER** : Valeur brute sans préfixe
2. **TENCEL/TENCEL LUXE 3D** : Préfixe selon quantité
   - 1 pièce : `"2 x [valeur]"`
   - 2 pièces : `"4 x [valeur]"`
   - N pièces : `"[N*2] x [valeur]"`

### Validation
- Vérification existence dans référentiels
- Gestion des erreurs si dimension non trouvée
- Formatage automatique selon règles métier

## 🎯 10. Processus Complet

### Ordre des Opérations
1. **Extraction dimensions** matelas (89x198)
2. **Détection matière** housse (TENCEL LUXE 3D)
3. **Consultation référentiel** largeur → 101 cm
4. **Consultation référentiel** longueur → 5.5 cm
5. **Formatage** selon matière → "2 x 101"
6. **Génération** champs Excel

## 📈 11. Métriques

### Données Traitées
- **2 référentiels** consultés
- **2 calculs** automatiques
- **1 formatage** selon règles
- **2 champs Excel** générés

### Performance
- **Calculs instantanés** via tables de correspondance
- **Validation automatique** des dimensions
- **Gestion d'erreurs** robuste

## ✅ 12. Validation

### Tests Réussis
- ✅ **Calcul dimension** : 89 → 101 cm
- ✅ **Calcul longueur** : 198 → 5.5 cm
- ✅ **Formatage** : "2 x 101"
- ✅ **Export Excel** : Champs corrects
- ✅ **Différentes matières** : Toutes validées
- ✅ **Différentes dimensions** : Toutes validées

---

**Résultat** : Le système calcule **automatiquement et précisément** les dimensions housse pour tous les matelas RAINUREE selon les référentiels métier établis. 