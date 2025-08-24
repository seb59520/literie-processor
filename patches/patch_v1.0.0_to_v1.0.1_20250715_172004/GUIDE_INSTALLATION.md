# Guide d'Installation - Matelas Processor

## Options d'Installation Disponibles

Vous avez plusieurs options pour installer et distribuer votre application Matelas Processor :

### 🎯 Option 1 : Package Distributable avec Python (Recommandé)

**Pour qui :** Distribution simple aux utilisateurs finaux

**Avantages :**
- Installation en un clic
- **Python 3.11 embarqué pour Windows** - Aucune installation requise
- Scripts automatiques pour Windows/macOS/Linux
- Pas besoin de connaissances techniques

**Utilisation :**
```bash
# Créer le package avec Python embarqué
python3 create_package_with_python.py

# Distribuer les fichiers ZIP/TAR.GZ créés dans dist/
```

**Installation par l'utilisateur :**
- Windows : Double-cliquer sur `install_windows.bat` (Python inclus)
- macOS/Linux : Exécuter `./install_unix.sh`

---

### 🚀 Option 2 : Exécutable Standalone avec PyInstaller

**Pour qui :** Utilisateurs sans Python installé

**Avantages :**
- Exécutable unique (.exe sur Windows, .app sur macOS)
- **Python et dépendances complètement embarqués**
- Pas de dépendance externe
- Distribution très simple

**Inconvénients :**
- ❌ Taille importante (~50-100MB)
- ❌ Plus complexe à maintenir

**Utilisation :**
```bash
# Construire l'exécutable standalone
python3 build_standalone_exe.py

# L'exécutable sera dans dist/Matelas_Processor_Standalone/
```

**Installation :**
- Copier le dossier `Matelas_Processor_Standalone` où vous voulez
- Double-cliquer sur l'exécutable

---

### 📦 Option 3 : Package Distributable Classique

**Pour qui :** Utilisateurs avec Python installé

**Avantages :**
- Installation en un clic
- Scripts automatiques pour Windows/macOS/Linux
- Taille réduite

**Inconvénients :**
- ❌ Nécessite Python 3.8+ installé

**Utilisation :**
```bash
# Créer le package
python3 create_package.py

# Distribuer les fichiers ZIP/TAR.GZ créés dans dist/
```

---

### 📦 Option 4 : Package Python avec setuptools

**Pour qui :** Développeurs et utilisateurs techniques

**Avantages :**
- Installation via pip
- Gestion automatique des dépendances
- Intégration avec l'écosystème Python

**Utilisation :**
```bash
# Créer le package
python3 setup.py sdist bdist_wheel

# Installer
pip install dist/matelas-processor-1.0.0.tar.gz

# Utiliser
matelas-processor-gui
```

---

### 🔧 Option 5 : Installation Manuelle

**Pour qui :** Développement et tests

**Avantages :**
- Contrôle total
- Facile à modifier
- Idéal pour le développement

**Utilisation :**
```bash
# Installer les dépendances
pip install -r requirements_gui.txt

# Lancer l'application
python3 run_gui.py
```

---

## Comparaison des Options

| Option | Facilité d'installation | Taille | Dépendances | Maintenance |
|--------|------------------------|--------|-------------|-------------|
| Package avec Python | ⭐⭐⭐⭐⭐ | Moyenne | Aucune | Facile |
| Exécutable Standalone | ⭐⭐⭐⭐⭐ | Grande | Aucune | Moyenne |
| Package Classique | ⭐⭐⭐⭐ | Petite | Python | Facile |
| Package Python | ⭐⭐⭐ | Petite | Python | Facile |
| Installation Manuelle | ⭐⭐ | Petite | Python + pip | Difficile |

## Recommandations

### Pour la Distribution Générale
**Utilisez l'Option 1 (Package avec Python)** car elle offre le meilleur équilibre entre facilité d'installation et flexibilité, avec Python embarqué pour Windows.

### Pour les Utilisateurs Non-Techniques
**Utilisez l'Option 2 (Exécutable Standalone)** si vous voulez une installation encore plus simple avec tout embarqué.

### Pour les Utilisateurs avec Python
**Utilisez l'Option 3 (Package Classique)** pour une installation légère si Python est déjà installé.

### Pour les Développeurs
**Utilisez l'Option 4 (Package Python)** pour une intégration professionnelle.

## Détails Techniques

### Structure du Package Distributable
```
MatelasProcessor_1.0.0_YYYYMMDD_HHMMSS/
├── run_gui.py              # Application principale
├── backend_interface.py    # Interface backend
├── config.py              # Configuration
├── backend/               # Modules de traitement
├── template/              # Templates Excel
├── requirements_gui.txt   # Dépendances
├── install_windows.bat    # Script d'installation Windows
├── install_unix.sh        # Script d'installation Unix
└── README.txt            # Instructions
```

### Dépendances Incluses
- `openpyxl` : Manipulation Excel
- `fitz` (PyMuPDF) : Lecture PDF
- `httpx` : Requêtes HTTP
- `tkinter` : Interface graphique

### Compatibilité
- **Python :** 3.8+
- **OS :** Windows 10+, macOS 10.14+, Linux
- **Architecture :** x86_64, ARM64 (macOS)

## Dépannage

### Erreur "Python non trouvé"
- Installez Python 3.8+ depuis python.org
- Ajoutez Python au PATH système

### Erreur de dépendances
- Vérifiez votre connexion internet
- Essayez : `pip install --upgrade pip`
- Puis : `pip install -r requirements_gui.txt`

### Erreur de permissions (macOS/Linux)
- Exécutez : `chmod +x install_unix.sh`
- Ou utilisez : `sudo ./install_unix.sh`

## Support

Pour toute question technique, consultez :
1. Le fichier `README_GUI.md`
2. Les logs d'erreur dans la console
3. La documentation Python des modules utilisés 