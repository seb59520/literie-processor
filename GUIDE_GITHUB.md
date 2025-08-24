# 📋 Guide : Pousser le Projet sur GitHub

## 🎯 **Méthodes disponibles**

### **Option 1 : Script Automatique (Recommandé) 🚀**
```bash
python git_setup.py
```
Ce script fait tout automatiquement :
- Initialise Git
- Nettoie les données sensibles  
- Crée le commit initial
- Configure le remote GitHub
- Pousse le code

### **Option 2 : Nettoyage puis Manual**
```bash
python clean_for_github.py  # Nettoie les données sensibles
# Puis suivez les étapes manuelles ci-dessous
```

### **Option 3 : Méthode Manuelle Complète**

## 📋 **Étapes Manuelles**

### **1. Nettoyage des données sensibles**
```bash
# Sauvegardez votre config actuelle
cp matelas_config.json matelas_config.json.backup

# Créez un template sans clés API
python clean_for_github.py
```

### **2. Initialisation Git**
```bash
# Initialiser le repository
git init

# Ajouter tous les fichiers
git add .

# Premier commit
git commit -m "Initial commit - Processeur de Devis Literie

- Interface PyQt6 complète
- Support multi-LLM (OpenRouter, OpenAI, Anthropic)
- Export Excel automatisé  
- Compilation Windows avec PyInstaller
- Monitoring système en temps réel
- Documentation complète"
```

### **3. Création du Repository GitHub**

**Sur GitHub.com :**
1. Allez sur https://github.com/new
2. **Nom** : `matelas-processor` (ou votre choix)
3. **Description** : `Processeur de Devis Literie avec IA - Interface PyQt6`
4. **Visibilité** : Public ou Privé (votre choix)
5. **⚠️ NE cochez PAS "Add README"** (on l'a déjà)
6. Cliquez "Create repository"

### **4. Connexion et Push**
```bash
# Ajouter le remote (remplacez par votre URL)
git remote add origin https://github.com/votre-username/matelas-processor.git

# Configurer la branche principale
git branch -M main

# Push initial
git push -u origin main
```

## 🔒 **Sécurité des Données**

### **Fichiers automatiquement exclus (.gitignore) :**
- Clés API privées
- Fichiers de logs
- Cache Python
- Fichiers temporaires
- Dossiers de compilation

### **Template de configuration créé :**
- `matelas_config.json.template` - Version sans clés API
- `matelas_config.json.backup` - Votre config sauvegardée

## 🚀 **Fonctionnalités GitHub**

### **GitHub Actions (Compilation Automatique)**
Votre repo inclut `.github/workflows/build-windows.yml` pour :
- Compilation automatique d'exécutables Windows
- Déclenchement sur push de tags (`v1.0.0`, etc.)
- Téléchargement des exécutables depuis Actions

### **Utilisation des Actions :**
1. Allez dans l'onglet "Actions" de votre repo
2. Cliquez "Build Windows Executable"
3. "Run workflow" → "Run workflow"
4. Attendez 10-15 minutes
5. Téléchargez l'artifact "MatelasProcessor-Windows"

## 📦 **Structure du Repository**

Après push, votre repo contiendra :
```
matelas-processor/
├── README.md                    # Documentation principale
├── LICENSE                      # Licence MIT
├── requirements.txt             # Dépendances Python
├── .gitignore                   # Fichiers à ignorer
├── app_gui.py                   # Application principale
├── config.py                    # Gestion configuration
├── matelas_config.json.template # Template de config
├── build_windows.py             # Compilation Windows
├── .github/workflows/           # CI/CD automatisé
└── docs/                        # Documentation
```

## 🔧 **Après le Push**

### **1. Vérifications**
- Allez sur votre repository GitHub
- Vérifiez que tous les fichiers sont présents
- Testez la compilation avec GitHub Actions

### **2. Configuration**
- Ajoutez une description au repository
- Ajoutez des topics : `python`, `pyqt6`, `ai`, `pdf-processing`
- Configurez les permissions si nécessaire

### **3. Collaboration**
- Invitez des collaborateurs si nécessaire  
- Configurez les branch protections
- Définissez des rules pour les pull requests

## 🆘 **Résolution de Problèmes**

### **"Permission denied" lors du push**
```bash
# Vérifiez vos identifiants GitHub
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@example.com"

# Ou utilisez SSH au lieu de HTTPS
git remote set-url origin git@github.com:username/repo.git
```

### **"Repository already exists"**
```bash
# Si le repo existe déjà sur GitHub
git remote add origin https://github.com/username/existing-repo.git
git push --set-upstream origin main
```

### **Fichiers sensibles accidentellement ajoutés**
```bash
# Supprimer du git mais garder localement
git rm --cached matelas_config.json
git commit -m "Remove sensitive config file"
git push
```

## ✅ **Checklist Finale**

Avant de pousser, vérifiez :
- [ ] Clés API supprimées/masquées
- [ ] .gitignore configuré
- [ ] README.md informatif
- [ ] Fichiers temporaires supprimés
- [ ] Tests passent (`python test_windows.py`)
- [ ] Compilation fonctionne (`python build_windows.py`)

## 🎉 **Après le Push Réussi**

Votre projet est maintenant sur GitHub avec :
- ✅ **Code source complet** et documenté
- ✅ **Compilation automatique** Windows via GitHub Actions
- ✅ **Documentation** comprehensive
- ✅ **Sécurité** des données respectée
- ✅ **Collaboration** possible avec d'autres développeurs

---

**Félicitations ! Votre Processeur de Devis Literie est maintenant sur GitHub ! 🎉**