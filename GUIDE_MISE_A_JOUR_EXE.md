# 🔄 Guide des Mises à Jour pour Exécutables (.exe)

## Vue d'ensemble

Votre application est packagée dans un exécutable unique (.exe). Le système de mise à jour automatique télécharge et installe des **nouveaux EXE complets** au lieu de mettre à jour des fichiers individuels.

## 🎯 Processus de Mise à Jour

### **Pour le Client (Utilisateur Final) :**

1. **Lance normalement** son `MatelasProcessor.exe`
2. **Notification automatique** : "Mise à jour disponible v3.10.0"
3. **Clique "Installer"** dans le dialog
4. **Téléchargement** du nouveau .exe (quelques MB)
5. **Installation automatique** : ancien exe sauvegardé → nouveau exe installé
6. **Redémarrage** automatique de l'application

### **Pour le Développeur :**

## 🔨 Création et Publication d'une Nouvelle Version

### **Option A : Script Automatique** (Recommandé)

```bash
# Créer une version patch (3.9.0 → 3.9.1)
python3 build_and_publish.py --type patch --description "Correction bugs critiques"

# Créer une version minor (3.9.0 → 3.10.0)  
python3 build_and_publish.py --type minor --description "Nouvelles fonctionnalités"

# Créer une version major (3.9.0 → 4.0.0)
python3 build_and_publish.py --type major --description "Refonte complète"
```

**Ce script fait TOUT automatiquement :**
1. ✅ Incrémente la version
2. ✅ Compile le nouvel EXE avec PyInstaller  
3. ✅ Crée le package de mise à jour
4. ✅ Publie via l'interface d'administration
5. ✅ Les clients reçoivent immédiatement

### **Option B : Interface d'Administration Web**

1. **Compilez** votre EXE manuellement :
   ```bash
   pyinstaller --onefile --windowed app_gui.py
   ```

2. **Ouvrez** l'interface : http://localhost:8081

3. **Upload Manuel** :
   - Glissez votre nouveau `MatelasProcessor.exe` 
   - Ou créez un ZIP contenant l'exe
   - Ajoutez version et description
   - Publiez

## 🏗️ Structure du Package de Mise à Jour

### **Contenu du ZIP publié :**
```
MatelasProcessor_v3.10.0_20250901.zip
├── MatelasProcessor.exe          # Nouvel exécutable complet
├── update_metadata.json          # Métadonnées d'installation
└── install.bat                   # Script d'installation Windows
```

### **Métadonnées d'installation :**
```json
{
  "version": "3.10.0",
  "package_type": "executable_update",
  "executable_name": "MatelasProcessor.exe", 
  "requires_restart": true,
  "backup_current": true,
  "install_instructions": [
    "Fermer l'application courante",
    "Sauvegarder l'ancien exécutable",
    "Extraire le nouveau MatelasProcessor.exe",
    "Remplacer l'ancien fichier",
    "Redémarrer l'application"
  ]
}
```

## 🔧 Configuration du Build

### **Personnalisation de PyInstaller :**

Modifiez `build_and_publish.py` pour votre configuration :

```python
build_command = [
    "pyinstaller",
    "--onefile",                    # Un seul .exe
    "--windowed",                   # Sans console  
    "--icon=votre_icone.ico",       # Votre icône
    "--name=VotreAppNom",           # Nom de l'exe
    
    # Inclure vos dossiers
    "--add-data=backend;backend",
    "--add-data=config;config", 
    "--add-data=assets;assets",
    
    # Dépendances cachées  
    "--hidden-import=PyQt6",
    "--hidden-import=openpyxl",
    
    "app_gui.py"                    # Script principal
]
```

## 🛡️ Sécurité et Sauvegarde

### **Sauvegarde Automatique :**
- Avant chaque mise à jour : `MatelasProcessor.exe.backup`
- En cas de problème : renommez le `.backup` en `.exe`

### **Installation Sécurisée sur Windows :**
- L'exe en cours ne peut pas s'auto-remplacer
- Utilisation d'un script batch externe
- Redémarrage automatique après remplacement

### **Validation de l'Installation :**
- Vérification de l'intégrité du téléchargement
- Validation du nouvel exe avant installation
- Rollback automatique en cas d'échec

## 🎯 Avantages de cette Approche

### **✅ Pour les Utilisateurs :**
- **Simple** : Un clic pour mettre à jour
- **Rapide** : Téléchargement d'un seul fichier
- **Sûr** : Sauvegarde automatique de l'ancien exe
- **Transparent** : Redémarrage automatique

### **✅ Pour les Développeurs :**
- **Complet** : Tout est inclus dans l'exe
- **Fiable** : Pas de dépendances externes à gérer
- **Automatisé** : Build + Publication en une commande
- **Contrôlé** : Interface d'administration complète

## 🔄 Workflow de Développement

### **Cycle de développement typique :**

```mermaid
graph LR
    A[Code] --> B[Test Local]
    B --> C[Build Script]
    C --> D[EXE Généré]
    D --> E[Publication Auto]
    E --> F[Clients MAJ]
```

1. **Développez** vos nouvelles fonctionnalités
2. **Testez** localement avec `python app_gui.py`
3. **Compilez** avec `python3 build_and_publish.py`
4. **✅ Les clients** reçoivent automatiquement

### **Déploiement en production :**

```bash
# Environnement de production
python3 build_and_publish.py \
  --type minor \
  --description "Version de production avec nouvelles fonctionnalités"
```

## 📊 Monitoring et Statistiques

### **Via l'Interface d'Administration :**
- 📈 Nombre de téléchargements par version
- 💾 Espace de stockage utilisé
- 📅 Historique des releases
- 🔍 Logs de mise à jour

### **APIs de monitoring :**
```bash
# Statistiques globales
curl http://localhost:8081/api/admin/stats

# Liste des versions
curl http://localhost:8081/api/v1/versions
```

## 🆘 Dépannage

### **Le build échoue :**
1. Vérifiez PyInstaller : `pip install pyinstaller`
2. Testez manuellement : `pyinstaller app_gui.py`
3. Vérifiez les dépendances manquantes

### **La mise à jour échoue côté client :**
1. Vérifiez la connexion réseau
2. L'exe est-il fermé complètement ?
3. Permissions d'écriture dans le dossier
4. Antivirus bloque-t-il l'installation ?

### **Rollback d'urgence :**
```bash
# Restaurer l'ancienne version
copy MatelasProcessor.exe.backup MatelasProcessor.exe
```

## 🎊 Résultat Final

**Vos clients auront :**
- 🔄 **Mises à jour automatiques** sans effort
- 📥 **Un seul .exe** toujours à jour  
- 🛡️ **Sauvegardes automatiques** en cas de problème
- 🚀 **Redémarrage transparent**

**Vous aurez :**
- 🎯 **Déploiement en une commande**
- 📊 **Interface d'administration complète**
- 🔧 **Contrôle total du processus**
- 📈 **Statistiques de déploiement**

---

🎉 **Votre système de mise à jour d'EXE est opérationnel !**