# Guide de Mise à Jour pour Applications EXE

## 🔍 **Différences Mode Développement vs EXE**

### **Mode Développement (Python)**
- **Répertoire:** `Path.cwd()` → Répertoire source du projet
- **Fichiers:** Tous les fichiers Python (.py) peuvent être remplacés
- **Redémarrage:** `python app_gui.py`
- **Version:** Mise à jour directe de `version.py`

### **Mode EXE (Exécutable Compilé)**
- **Répertoire:** `Path(sys.executable).parent` → Dossier de l'EXE
- **Fichiers:** L'EXE principal ne peut pas être remplacé pendant l'exécution
- **Redémarrage:** Lancement direct de l'EXE
- **Version:** Intégrée dans l'EXE, mise à jour via ressources externes

## 🛠️ **Stratégies de Mise à Jour pour EXE**

### **1. Mise à Jour des Ressources (Recommandée)**
```python
# Structure pour EXE:
app_folder/
├── matelas.exe          # EXE principal (non remplaçable)
├── version.py           # Fichier de version externe
├── config/              # Configurations
├── backend/             # Modules Python
└── templates/           # Templates et ressources
```

### **2. Fichiers Gérés par les Mises à Jour**
✅ **Fichiers remplaçables pendant l'exécution:**
- `version.py` - Information de version
- `backend/*.py` - Modules backend
- `config/*.json` - Configurations
- `templates/*` - Templates HTML/CSS
- Documentation et fichiers de données

❌ **Fichiers NON remplaçables:**
- `matelas.exe` - Exécutable principal
- Fichiers DLL verrouillés par Windows
- Fichiers temporaires en cours d'utilisation

## 🔧 **Améliorations Implémentées**

### **Détection Automatique du Mode**
```python
is_exe = getattr(sys, 'frozen', False)
app_dir = Path(sys.executable).parent if is_exe else Path.cwd()
```

### **Extraction Intelligente**
- **Mode DEV:** Extraction complète du ZIP
- **Mode EXE:** Extraction sélective (skip les .exe)

### **Gestion des Permissions**
- Tentative de remplacement avec gestion des erreurs
- Skip automatique des fichiers verrouillés
- Logs détaillés des opérations

## 🚀 **Processus de Mise à Jour EXE**

### **Étape 1: Détection**
```
🔍 Vérification des mises à jour...
✅ Version 3.10.3 disponible
📦 Taille: 1.2 GB
```

### **Étape 2: Téléchargement**
```
📥 Téléchargement en cours...
[████████████████████████████████] 100%
✅ Téléchargement terminé
```

### **Étape 3: Installation**
```
🔧 Mode: EXE
📁 Répertoire app: C:\Users\...\Matelas\
💾 Sauvegarde: backup_20250902_164500/
📦 Extraction de la mise à jour...
🔒 Mode EXE détecté, exe principal: matelas.exe
⏭️ Ignoré (exe): matelas.exe
✅ Mis à jour: version.py
✅ Mis à jour: backend/auto_updater.py
... (mise à jour en cours)
✅ EXE: 350 fichiers mis à jour, 5 ignorés
🔄 Restauré: config/secure_keys.dat
✅ Version mise à jour: 3.10.3
```

### **Étape 4: Redémarrage**
```
🔄 Redémarrage de l'application...
📱 Redémarrage EXE: C:\Users\...\matelas.exe
✅ Nouvelle instance démarrée
🔚 Fermeture de l'ancienne instance...
```

## 📋 **Checklist Pré-Déploiement EXE**

### **Avant de Créer l'EXE:**
- [ ] ✅ Système de mise à jour intégré dans PyInstaller
- [ ] ✅ `version.py` accessible en externe
- [ ] ✅ Fichiers de configuration dans dossier séparé
- [ ] ✅ Templates et ressources accessibles

### **Structure de l'EXE:**
```
dist/
├── matelas.exe                 # EXE principal
├── version.py                  # Version externe (mise à jour auto)
├── config/
│   ├── secure_keys.dat        # Clés API (préservées)
│   └── mappings_*.json        # Configurations
├── backend/
│   ├── auto_updater.py        # Système de MAJ
│   └── *.py                   # Modules backend
└── admin_update_storage/       # Serveur MAJ local (optionnel)
```

### **Commandes de Build:**
```bash
# Créer l'EXE avec support des mises à jour
pyinstaller --onefile \
    --add-data "version.py:." \
    --add-data "config:config" \
    --add-data "backend:backend" \
    --add-data "templates:templates" \
    --hidden-import "backend.auto_updater" \
    app_gui.py
```

## 🧪 **Tests Recommandés pour EXE**

### **Test 1: Installation Basique**
1. Créer l'EXE
2. Lancer et vérifier version affichée
3. Tester fonctionnalités de base

### **Test 2: Mise à Jour EXE**
1. Lancer l'EXE version N
2. Déclencher mise à jour vers N+1
3. Vérifier installation sans erreur
4. Vérifier redémarrage automatique
5. Vérifier version N+1 affichée

### **Test 3: Préservation des Données**
1. Configurer clés API
2. Faire une mise à jour
3. Vérifier que les clés sont préservées

## ⚠️ **Limitations Mode EXE**

### **L'EXE Principal**
- Ne peut pas être mis à jour pendant qu'il s'exécute
- Mise à jour de l'EXE nécessite un processus externe
- Solution: Mise à jour des modules externes seulement

### **Chemins Absolus**
- PyInstaller modifie les chemins de fichiers
- Utiliser `sys._MEIPASS` pour les ressources intégrées
- Utiliser `Path(sys.executable).parent` pour les fichiers externes

### **Dépendances**
- Toutes les dépendances doivent être intégrées dans l'EXE
- Les imports dynamiques peuvent poser problème
- Tester l'EXE sur une machine "propre"

## 💡 **Recommandations**

### **Architecture Hybride**
- **EXE:** Interface utilisateur et logique métier
- **Modules Externes:** Fonctionnalités mises à jour fréquemment
- **Configurations:** Fichiers externes préservés

### **Versions de l'EXE**
- **Versions Majeures:** Nécessitent un nouvel EXE
- **Versions Mineures/Patches:** Mise à jour des modules externes
- **Hotfixes:** Mise à jour des configurations et templates

### **Distribution**
- EXE initial via installateur classique
- Mises à jour via système automatique
- Serveur de distribution pour les patches

## 🎯 **Résultat Attendu**

Avec ces améliorations, votre EXE pourra :
- ✅ Se mettre à jour automatiquement (modules externes)
- ✅ Préserver les configurations utilisateur
- ✅ Afficher la bonne version après mise à jour
- ✅ Redémarrer automatiquement
- ✅ Gérer les erreurs gracieusement
- ✅ Ignorer les fichiers verrouillés

**L'EXE sera donc aussi performant que le mode développement pour les mises à jour !** 🚀