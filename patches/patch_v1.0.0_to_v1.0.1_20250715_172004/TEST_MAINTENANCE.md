# Test de Maintenance

## Description

Ce fichier a été créé pour tester le système de maintenance de l'application Matelas. Il permet de vérifier que :

- Les nouveaux fichiers Markdown sont automatiquement détectés
- L'extraction du titre fonctionne correctement
- L'affichage du contenu est correct

## Fonctionnalités testées

### 1. Détection automatique
- ✅ Scan du répertoire racine
- ✅ Scan des sous-répertoires
- ✅ Filtrage des fichiers `.md`

### 2. Extraction du titre
- ✅ Titre principal (`# Titre`)
- ✅ Sous-titre (`## Sous-titre`)
- ✅ Fallback sur le nom de fichier

### 3. Affichage du contenu
- ✅ Conversion Markdown vers HTML
- ✅ Affichage des métadonnées
- ✅ Navigation dans les fichiers

## Utilisation

1. Ouvrir l'application Matelas
2. Aller dans **Réglages** → **📚 Maintenance - Documentation**
3. Vérifier que ce fichier apparaît dans la liste
4. Cliquer sur le fichier pour voir son contenu

## Code d'exemple

```python
# Exemple de code pour tester
def test_maintenance():
    print("Test de maintenance réussi !")
    return True
```

## Liens utiles

- [Documentation principale](AIDE_COMPLETE.md)
- [Guide d'installation](GUIDE_INSTALLATION.md)
- [Tests automatisés](README_TESTS.md)

---

*Fichier créé le : $(date)* 