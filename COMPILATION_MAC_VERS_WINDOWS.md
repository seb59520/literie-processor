# 🍎→🪟 Compilation Windows depuis Mac

## ⚠️ **Limitation importante**
PyInstaller **NE PEUT PAS** créer des .exe Windows depuis macOS. Il faut un environnement Windows pour compiler.

## 🎯 **Solutions pratiques**

### **Option 1: GitHub Actions (RECOMMANDÉE) 🌟**

#### Avantages :
- ✅ **Gratuit** (2000 minutes/mois)
- ✅ **Automatique** (aucun Windows requis)
- ✅ **Environnement propre** (pas de conflits)
- ✅ **Stockage des versions**

#### Étapes :
1. **Créez un repo GitHub** (public ou privé)
2. **Uploadez votre code** (incluant `.github/workflows/build-windows.yml`)
3. **Allez dans "Actions"** → "Build Windows Executable"  
4. **Cliquez "Run workflow"**
5. **Attendez 10-15 minutes**
6. **Téléchargez l'artifact** "MatelasProcessor-Windows"

### **Option 2: Machine Virtuelle Windows**

#### Si vous avez souvent besoin de compiler :
1. **VMware Fusion** (~80€) ou **Parallels Desktop** (~100€)
2. **Windows 11** (gratuit en développement)
3. **Python + PyInstaller** dans la VM
4. **Copiez le code** → **Compilez** → **Récupérez l'exe**

### **Option 3: PC Windows temporaire**
- Ami/collègue avec Windows
- PC Windows dans un FabLab/espace de coworking
- Location cloud Windows (AWS/Azure)

## 🚀 **Test immédiat sur Mac**

Vous pouvez quand même tester la compilation (créera un .app) :

```bash
# Test de compilation (créera un exécutable Mac)
python build_windows.py

# Vérification que tout fonctionne
python app_gui.py
```

## 📋 **Préparation pour Windows**

Votre code est **déjà prêt** ! Tous ces fichiers fonctionneront sur Windows :

```
✅ build_windows.py          # Script de compilation
✅ matelas_processor.spec    # Configuration PyInstaller  
✅ version_info.txt          # Infos version Windows
✅ requirements_build.txt    # Dépendances
✅ windows_config.py         # Config spécifique Windows
✅ .github/workflows/...     # Workflow GitHub Actions
```

## 🎯 **Recommandation finale**

**Pour un usage ponctuel → GitHub Actions**
1. Créez un repo GitHub
2. Uploadez le code 
3. Lancez le workflow
4. Récupérez l'exe

**Pour un usage régulier → Machine virtuelle**
- VMware Fusion + Windows 11
- Installation permanente Python/PyInstaller

## ⚡ **Script de démarrage rapide**

```bash
# Sur votre Mac
python build_cloud.py
# → Affiche toutes les options avec instructions détaillées
```

---

💡 **En résumé** : Impossible de compiler directement sur Mac, mais GitHub Actions est une excellente alternative gratuite et automatique !