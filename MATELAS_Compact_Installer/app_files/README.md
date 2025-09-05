# 🛏️ Processeur de Devis Literie

Application PyQt6 pour le traitement automatisé des devis de matelas et sommiers avec intelligence artificielle.

## 🎯 **Fonctionnalités**

- ✅ **Interface graphique intuitive** avec PyQt6
- ✅ **Traitement automatique des PDFs** de devis
- ✅ **Extraction de données** avec IA (OpenRouter, Anthropic, OpenAI, etc.)
- ✅ **Export Excel** automatisé avec formatage avancé
- ✅ **Génération de rapports HTML** complets
- ✅ **Monitoring système** en temps réel
- ✅ **Support multi-LLM** (configuration flexible)
- ✅ **Mode portable** (aucune installation requise)

## 🖥️ **Interface**

L'application dispose d'une interface complète avec :
- **Panneau de sélection** : Choix des fichiers PDF
- **Onglets de résultats** : Résumé, Configurations, Pré-import, Logs, Debug
- **Actions rapides** : Ouverture dossiers, génération rapports, export données
- **Monitoring** : Métriques système et logs en temps réel

## 🚀 **Installation et Utilisation**

### **Prérequis**
- Python 3.8+
- Windows 10/11, macOS, ou Linux

### **Installation**
```bash
git clone https://github.com/votre-username/matelas-processor
cd matelas-processor
pip install -r requirements.txt
```

### **Configuration**
1. Configurez votre API LLM dans `matelas_config.json`
2. Choisissez votre provider : OpenRouter, OpenAI, Anthropic, etc.

### **Lancement**
```bash
python app_gui.py
```

## 📦 **Compilation Exécutable Windows**

### **Méthode automatique**
```bash
python build_windows.py
```

### **Méthode rapide**
```bash
python quick_build.py
```

### **Avec GitHub Actions**
- Push votre code sur GitHub
- Actions → "Build Windows Executable" → Run workflow
- Téléchargez l'exécutable depuis les artifacts

## 🛠️ **Architecture**

```
matelas-processor/
├── app_gui.py              # Interface principale
├── config.py               # Gestion configuration
├── matelas_config.json     # Configuration LLM
├── backend/                # Logique métier
├── utilities/              # Utilitaires
├── build_windows.py        # Compilation Windows
└── .github/workflows/      # CI/CD automatisé
```

## ⚙️ **Configuration LLM**

L'application supporte plusieurs providers :

```json
{
  "current_llm_provider": "openrouter",
  "llm_api_key_openrouter": "votre-clé-api",
  "llm_api_key_openai": "votre-clé-api",
  "llm_api_key_anthropic": "votre-clé-api"
}
```

## 📊 **Fonctionnalités Avancées**

### **Export Multi-format**
- Excel avec formatage avancé
- CSV pour import dans d'autres outils
- JSON pour intégrations techniques
- Rapports HTML interactifs

### **Monitoring en Temps Réel**
- Métriques système (CPU, RAM, Disque)
- Logs détaillés avec niveaux configurables
- Debug et diagnostic automatique

### **Mode Portable**
- Configuration stockée localement
- Aucune installation système requise
- Compatible avec clé USB/réseau

## 🔧 **Développement**

### **Structure du Code**
- **PyQt6** pour l'interface graphique
- **Requests** pour les API LLM
- **Pandas/OpenPyXL** pour l'export Excel
- **Threading** pour les opérations longues

### **Tests**
```bash
python test_windows.py      # Test environnement
python test_buttons.py      # Test fonctionnalités
```

### **Débogage**
- Onglet Debug avec informations système
- Logs détaillés dans l'interface
- Monitoring des performances

## 📋 **Documentation**

- `README_Windows_Build.md` - Guide compilation Windows
- `COMPILATION_MAC_VERS_WINDOWS.md` - Compilation depuis Mac
- `CORRECTION_ERREUR_ENCODAGE.md` - Résolution problèmes encodage
- `INSTRUCTIONS_COMPILATION.md` - Instructions simplifiées

## 🤝 **Contribution**

1. Forkez le projet
2. Créez votre branche (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Committez vos changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrez une Pull Request

## 📄 **Licence**

Ce projet est sous licence privée. Tous droits réservés.

## 🆘 **Support**

- **Issues** : Utilisez les GitHub Issues pour les bugs
- **Documentation** : Consultez les fichiers `.md` du projet
- **Tests** : Lancez les scripts de test pour diagnostiquer

## 🏷️ **Versions**

- **v1.0.0** - Version initiale avec interface complète
- Interface PyQt6, support multi-LLM, export Excel, compilation Windows

---

**Développé avec ❤️ pour l'automatisation du traitement des devis literie**