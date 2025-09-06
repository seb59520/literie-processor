# MatelasProcessor v3.11.9 - Version Portable

## 🚀 Lancement rapide

### Windows
Double-cliquez sur `lancer_matelas.bat`

### Linux/Mac
```bash
./lancer_matelas.sh
```

## 📡 Système de mise à jour automatique

Cette version inclut un système de mise à jour automatique qui :

✅ **Vérifie automatiquement** les nouvelles versions
✅ **Affiche un indicateur** dans la barre de statut
✅ **Propose le téléchargement** des mises à jour
✅ **Préserve vos configurations** lors des mises à jour

### Fonctionnement

- 🔍 **Vérification** : Toutes les 24h + au démarrage
- 📊 **Indicateur** : Visible en bas à droite de l'application
- 🎯 **Cliquable** : Cliquez sur l'indicateur pour voir les détails
- 🔒 **Sécurisé** : Téléchargement depuis serveur officiel

### États de l'indicateur

- 🔄 **Bleu** : Vérification en cours
- ✅ **Vert** : Application à jour
- 🆕 **Rouge** : Nouvelle version disponible
- ⚠️ **Gris** : Erreur de connexion

## 📁 Structure

```
MatelasProcessor/
├── app_gui.py              # Application principale
├── backend/                # Logique métier
├── config/                 # Configurations
├── template/               # Templates Excel
├── update_config.json      # Configuration mise à jour
├── lancer_matelas.bat      # Lanceur Windows
├── lancer_matelas.sh       # Lanceur Linux/Mac
└── README.md              # Ce fichier
```

## 🔧 Configuration

Le fichier `update_config.json` permet de configurer :

- **Activation/désactivation** des mises à jour automatiques
- **Fréquence** de vérification
- **Serveur** de mise à jour
- **Notifications**

## 🆘 Dépannage

### L'application ne démarre pas
1. Vérifiez que Python 3.8+ est installé
2. Lancez `pip install -r requirements_gui.txt`
3. Utilisez les scripts de lancement fournis

### L'indicateur de mise à jour ne s'affiche pas
1. Vérifiez votre connexion Internet
2. L'indicateur apparaît en bas à droite après quelques secondes
3. Redémarrez l'application si nécessaire

### Erreur de mise à jour
1. Vérifiez votre connexion Internet
2. L'application fonctionne normalement même sans mise à jour
3. Vous pouvez désactiver les mises à jour dans `update_config.json`

## 📞 Support

- Version : 3.11.9
- Build : 2025-09-02
- Type : Portable avec mise à jour automatique

---
🎯 **Conseil** : Gardez l'application à jour pour bénéficier des dernières améliorations !
