# 🚀 Guide de résolution rapide - Problème de connexion Notion

## ❌ Problème identifié

**Erreur 404** : L'intégration Notion ne peut pas accéder à votre base de données.

## 🔍 Cause principale

**Permissions manquantes** : Votre intégration n'a pas été invitée à accéder à la base de données.

## ✅ Solution en 3 étapes

### Étape 1 : Vérifier l'intégration
1. Allez sur [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Cliquez sur votre intégration "Cursor Integration"
3. Vérifiez que le **Workspace** est correctement sélectionné
4. Assurez-vous que l'intégration est **active** (pas en pause)

### Étape 2 : Partager la base de données
1. **Ouvrez votre base de données** dans Notion
2. Cliquez sur le bouton **"Share"** (en haut à droite)
3. Cliquez sur **"Invite"**
4. Dans le champ de recherche, tapez : **"Cursor Integration"**
5. Sélectionnez votre intégration dans la liste
6. Cliquez sur **"Invite"**
7. Vérifiez que l'intégration apparaît dans la liste

### Étape 3 : Vérifier les permissions
1. Dans la liste des personnes ayant accès, cliquez sur votre intégration
2. Vérifiez que les permissions sont sur **"Can edit"** ou **"Full access"**
3. Si c'est sur "No access", changez-le

## 🆘 Si le partage ne fonctionne pas

### Option A : Créer une nouvelle base de données
1. **Créez une nouvelle page** dans Notion
2. Tapez `/database` et sélectionnez **"Table"**
3. **Ajoutez immédiatement** ces propriétés :

| Propriété | Type | Description |
|-----------|------|-------------|
| Nom | **Title** | Nom du projet |
| Chemin | **Text** | Chemin du projet |
| Description | **Text** | Description du projet |
| Langage | **Select** | Python, JavaScript, etc. |
| Framework | **Text** | Framework utilisé |
| Dernière modification | **Date** | Date de modification |
| Statut Git | **Select** | Git initialisé, Non versionné |
| Workspace Cursor | **Text** | Chemin du workspace |
| Statut | **Select** | En cours, Terminé, etc. |
| Date de création | **Date** | Date de création |

4. **Partagez immédiatement** cette base avec votre intégration
5. **Copiez le nouvel ID** de la base de données

### Option B : Vérifier l'ID de la base
1. **Ouvrez votre base de données** dans Notion
2. **Copiez l'URL complète** depuis la barre d'adresse
3. L'URL est de la forme : `https://notion.so/[workspace]/[database-id]?v=...`
4. **Copiez uniquement** la partie `[database-id]` (32 caractères)
5. Vérifiez que c'est bien un ID hexadécimal (0-9, a-f)

## 🔧 Scripts de résolution

### 1. Configuration simple et robuste
```bash
python3 config_notion_simple.py
```

### 2. Test de connexion rapide
```bash
python3 test_connexion_notion.py
```

### 3. Diagnostic complet
```bash
python3 diagnostic_notion.py
```

## 🚨 Vérifications obligatoires

- [ ] L'intégration est dans le bon workspace
- [ ] La base de données est partagée avec l'intégration
- [ ] L'intégration a les permissions "Can edit" ou "Full access"
- [ ] L'ID de la base de données est correct (32 caractères hexadécimaux)
- [ ] L'intégration est active (pas en pause)

## 💡 Conseils de dépannage

1. **Commencez simple** : Créez une base de données basique d'abord
2. **Partagez immédiatement** : Invitez l'intégration dès la création
3. **Testez étape par étape** : Vérifiez chaque composant séparément
4. **Utilisez les scripts** : Ils valident automatiquement chaque étape

## 🔄 Relancer après correction

Une fois les permissions corrigées :

```bash
# Option 1 : Configuration simple
python3 config_notion_simple.py

# Option 2 : Test de connexion
python3 test_connexion_notion.py

# Option 3 : Lancement direct
python3 lancer_notion_integration.py
```

## 📞 Support

Si le problème persiste :

1. **Vérifiez les logs** de l'intégration dans Notion
2. **Testez avec une base simple** d'abord
3. **Consultez la documentation** : `README_NOTION_INTEGRATION.md`
4. **Utilisez le diagnostic** : `python3 diagnostic_notion.py`

---

**🎯 Objectif** : Une fois la connexion réussie, vous pourrez synchroniser automatiquement vos projets Cursor avec Notion !


