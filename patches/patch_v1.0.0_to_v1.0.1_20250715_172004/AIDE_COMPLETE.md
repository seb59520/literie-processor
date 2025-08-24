# 🛏️ Guide d'Aide Complet - Matelas Processor

## 📋 Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Installation](#installation)
3. [Premiers pas](#premiers-pas)
4. [Interface utilisateur](#interface-utilisateur)
5. [Traitement des fichiers](#traitement-des-fichiers)
6. [Fonctionnalités avancées](#fonctionnalités-avancées)
7. [Résultats et export](#résultats-et-export)
8. [Dépannage](#dépannage)
9. [FAQ](#faq)
10. [Support technique](#support-technique)

---

## 🎯 Vue d'ensemble

### Qu'est-ce que Matelas Processor ?

Matelas Processor est un outil automatisé de traitement de commandes de matelas qui :

- **Extrait automatiquement** les données des devis PDF
- **Analyse intelligemment** le contenu avec l'IA (LLM)
- **Calcule automatiquement** les dimensions et configurations
- **Génère des fichiers Excel** prêts pour la production
- **Gère les données clients** et les informations de commande

### Fonctionnalités principales

✅ **Extraction PDF automatique** - Lecture et analyse des devis PDF  
✅ **Intelligence artificielle** - Analyse LLM pour extraction précise  
✅ **Calculs automatiques** - Dimensions, housses, fermeté  
✅ **Gestion des clients** - Extraction et traitement des données client  
✅ **Pré-import Excel** - Formatage des données pour import  
✅ **Interface graphique** - Interface moderne et intuitive  
✅ **Export Excel** - Génération de fichiers de production  

### Types de matelas supportés

- **Latex Mixte 7 Zones** - Matelas latex avec zones de confort
- **Latex Naturel** - Matelas latex 100% naturel
- **Latex Renforcé** - Matelas latex avec renfort
- **Mousse Viscoélastique** - Matelas mousse mémoire
- **Mousse Rainurée 7 Zones** - Mousse avec zones de confort
- **Select 43** - Matelas spécialisé

---

## 🚀 Installation

### Option 1 : Installation simple (Recommandée)

#### Windows
1. Téléchargez le fichier ZIP de l'application
2. Extrayez le contenu dans un dossier
3. Double-cliquez sur `install_windows.bat`
4. L'application se lance automatiquement

#### macOS/Linux
1. Téléchargez le fichier TAR.GZ de l'application
2. Extrayez le contenu : `tar -xzf MatelasProcessor_*.tar.gz`
3. Ouvrez un terminal dans le dossier
4. Exécutez : `./install_unix.sh`

### Option 2 : Installation avec Python existant

Si vous avez Python 3.8+ installé :

```bash
# Installer les dépendances
pip install -r requirements_gui.txt

# Lancer l'application
python run_gui.py
```

### Option 3 : Installation Docker

```bash
# Cloner le projet
git clone [URL_DU_PROJET]

# Lancer avec Docker
docker-compose up --build

# Accéder à l'interface web
# Ouvrir http://localhost:8000
```

### Vérification de l'installation

Après installation, vous devriez voir :
- ✅ Interface graphique qui se lance
- ✅ Message "Application prête" dans la console
- ✅ Aucune erreur de dépendances

---

## 🎯 Premiers pas

### 1. Lancement de l'application

#### Interface graphique (Recommandée)
```bash
python run_gui.py
```

#### Interface web (Docker)
```bash
docker-compose up
# Puis ouvrir http://localhost:8000
```

### 2. Configuration initiale

#### Paramètres LLM
- **Enrichissement LLM** : Activé par défaut (recommandé)
- **Provider** : 
  - `Ollama` : LLM local (gratuit, plus lent)
  - `OpenRouter` : LLM cloud (payant, plus rapide)
- **Clé API** : Requise uniquement pour OpenRouter

#### Paramètres de production
- **Semaine** : Semaine de production (ex: 25)
- **Année** : Année de production (ex: 2025)
- **Commande client** : Nom du client (ex: "LOUCHART")

### 3. Premier traitement

1. **Sélectionnez un fichier PDF** de devis
2. **Configurez les paramètres** (LLM, production, client)
3. **Cliquez sur "Traiter les fichiers"**
4. **Consultez les résultats** dans les onglets

---

## 🖥️ Interface utilisateur

### Panneau de configuration (Gauche)

#### Section Fichiers
- **Sélection PDF** : Bouton pour choisir un ou plusieurs fichiers
- **Liste des fichiers** : Affichage des fichiers sélectionnés
- **Suppression** : Bouton pour retirer un fichier

#### Section LLM
- **Enrichissement LLM** : Case à cocher pour activer l'IA
- **Provider** : Menu déroulant Ollama/OpenRouter
- **Clé API** : Champ texte pour la clé OpenRouter
- **Statut** : Indicateur de connexion au LLM

#### Section Production
- **Semaine** : Champ numérique (1-53)
- **Année** : Champ numérique (2024+)
- **Commande client** : Champ texte libre

### Panneau de résultats (Droite)

#### Onglet Résumé
- **Statistiques** : Nombre de fichiers traités
- **Temps de traitement** : Durée totale
- **Erreurs** : Liste des problèmes rencontrés
- **Succès** : Nombre de traitements réussis

#### Onglet Configurations
- **Tableau des matelas** : Toutes les configurations détectées
- **Colonnes** : Type, dimensions, housse, fermeté, quantité
- **Actions** : Modifier, supprimer, dupliquer

#### Onglet Pré-import
- **Données structurées** : Format prêt pour Excel
- **Mapping des champs** : Client_D1, Adresse_D3, Hauteur_D22
- **Validation** : Vérification des données

#### Onglet JSON
- **Données brutes** : Format JSON complet
- **Debug** : Pour le développement
- **Export** : Copier/coller des données

### Barre d'outils

- **Traiter** : Lancer le traitement des fichiers
- **Arrêter** : Interrompre le traitement en cours
- **Exporter** : Sauvegarder les résultats
- **Aide** : Ouvrir ce guide
- **Paramètres** : Configuration avancée

---

## 📄 Traitement des fichiers

### Types de fichiers supportés

#### PDF de devis
- **Format** : PDF standard
- **Contenu** : Devis de matelas avec spécifications
- **Taille** : Jusqu'à 50MB par fichier
- **Encodage** : UTF-8 recommandé

#### Structure attendue
Le PDF doit contenir :
- Informations client (nom, adresse)
- Spécifications matelas (type, dimensions)
- Quantités et options
- Prix et conditions

### Processus de traitement

#### 1. Upload et validation
- Vérification du format PDF
- Contrôle de la taille du fichier
- Validation de l'encodage

#### 2. Extraction du texte
- Lecture du contenu PDF
- Extraction du texte brut
- Nettoyage des caractères spéciaux

#### 3. Analyse LLM
- Envoi du texte au LLM
- Extraction des données structurées
- Validation de la cohérence

#### 4. Traitement métier
- Détection du type de matelas
- Calcul des dimensions
- Détermination de la housse
- Validation de la fermeté

#### 5. Génération des résultats
- Création des configurations
- Extraction des données client
- Formatage pour l'export

### Gestion des erreurs

#### Erreurs courantes
- **Fichier corrompu** : Vérifiez l'intégrité du PDF
- **Format non reconnu** : Assurez-vous que c'est un devis de matelas
- **LLM indisponible** : Vérifiez la connexion internet
- **Données manquantes** : Le PDF peut être incomplet

#### Solutions
- **Relancez le traitement** après correction
- **Vérifiez les logs** dans la console
- **Contactez le support** si le problème persiste

---

## ⚙️ Fonctionnalités avancées

### Configuration LLM

#### Ollama (Local)
```bash
# Installation
curl -fsSL https://ollama.ai/install.sh | sh

# Lancement
ollama serve

# Téléchargement du modèle
ollama pull llama3
```

#### OpenRouter (Cloud)
1. Créez un compte sur [openrouter.ai](https://openrouter.ai)
2. Générez une clé API
3. Entrez la clé dans l'interface
4. Sélectionnez le modèle souhaité

### Personnalisation des règles

#### Fichiers de configuration
- `backend/Référentiels/` : Règles métier et référentiels
- `config.py` : Configuration générale
- `backend/*_utils.py` : Modules de traitement

#### Modification des règles
```python
# Exemple : Ajouter un nouveau type de matelas
# Dans backend/matelas_utils.py
NOYAUX_SUPPORTES = [
    "LATEX MIXTE 7 ZONES",
    "LATEX NATUREL",
    "NOUVEAU TYPE",  # Ajoutez ici
]
```

### Traitement par lot

#### Fichiers multiples
1. Sélectionnez plusieurs fichiers PDF
2. Configurez les paramètres globaux
3. Lancez le traitement
4. Consultez les résultats par fichier

#### Scripts automatisés
```python
# Exemple de script de traitement
from backend_interface import traiter_fichiers

resultats = traiter_fichiers(
    fichiers=["devis1.pdf", "devis2.pdf"],
    semaine=25,
    annee=2025,
    client="CLIENT_TEST"
)
```

### Intégration API

#### Endpoint REST
```bash
# Traitement via API
curl -X POST http://localhost:8000/traiter \
  -F "fichier=@devis.pdf" \
  -F "semaine=25" \
  -F "annee=2025"
```

#### Réponse JSON
```json
{
  "success": true,
  "configurations": [...],
  "donnees_client": {...},
  "pre_import": [...]
}
```

---

## 📊 Résultats et export

### Types de résultats

#### Configurations matelas
```json
{
  "matelas_index": 1,
  "noyau": "LATEX MIXTE 7 ZONES",
  "quantite": 1,
  "hauteur": 20,
  "fermete": "MÉDIUM",
  "housse": "MATELASSÉE",
  "dimensions": {"largeur": 89, "longueur": 198}
}
```

#### Données client
```json
{
  "nom": "Mr LOUCHART FREDERIC",
  "adresse": "HAZEBROUCK",
  "code_client": "LOUCFSE"
}
```

#### Pré-import Excel
```json
{
  "Client_D1": "Mr LOUCHART FREDERIC",
  "Adresse_D3": "HAZEBROUCK",
  "Hauteur_D22": 20
}
```

### Export Excel

#### Génération automatique
- **Template** : Basé sur `template/template_matelas.xlsx`
- **Nommage** : `Matelas_[CLIENT]_[DATE].xlsx`
- **Emplacement** : Dossier `output/`

#### Structure du fichier
- **Onglet 1** : Données client
- **Onglet 2** : Configurations matelas
- **Onglet 3** : Pré-import structuré
- **Onglet 4** : Métadonnées

#### Personnalisation
```python
# Modification du template
# Copiez template_matelas.xlsx
# Modifiez la structure
# Mettez à jour le mapping dans pre_import_utils.py
```

### Sauvegarde des résultats

#### Format JSON
```bash
# Export des données brutes
# Onglet JSON → Copier → Coller dans un fichier .json
```

#### Format CSV
```bash
# Conversion des configurations
# Utilisez un outil externe pour convertir JSON → CSV
```

---

## 🔧 Dépannage

### Problèmes d'installation

#### Erreur "Python non trouvé"
```bash
# Windows
# Téléchargez Python depuis python.org
# Cochez "Add to PATH" lors de l'installation

# macOS
brew install python3

# Linux
sudo apt-get install python3
```

#### Erreur de dépendances
```bash
# Mise à jour de pip
pip install --upgrade pip

# Installation des dépendances
pip install -r requirements_gui.txt

# Vérification
python -c "import PyQt6; print('OK')"
```

#### Erreur de permissions
```bash
# macOS/Linux
chmod +x install_unix.sh
chmod +x run_gui.py

# Windows
# Exécutez en tant qu'administrateur
```

### Problèmes de traitement

#### LLM non disponible
```bash
# Ollama
ollama serve
ollama list  # Vérifier les modèles

# OpenRouter
# Vérifiez votre clé API
# Testez la connexion internet
```

#### Fichier PDF non traité
- **Vérifiez le format** : Doit être un PDF valide
- **Vérifiez la taille** : Maximum 50MB
- **Vérifiez le contenu** : Doit être un devis de matelas
- **Vérifiez l'encodage** : UTF-8 recommandé

#### Données manquantes
- **Relancez le traitement** avec un LLM différent
- **Vérifiez les logs** pour les erreurs spécifiques
- **Contactez le support** avec le fichier PDF

### Problèmes d'interface

#### Interface qui ne se lance pas
```bash
# Vérifiez les logs
python run_gui.py 2>&1 | tee debug.log

# Vérifiez les dépendances
pip list | grep -i qt
```

#### Interface qui se fige
- **Attendez** : Le traitement peut prendre du temps
- **Vérifiez l'activité** : CPU, mémoire, réseau
- **Redémarrez** : Fermez et relancez l'application

#### Résultats non affichés
- **Vérifiez les onglets** : Résultats dans différents onglets
- **Vérifiez les logs** : Erreurs dans la console
- **Relancez le traitement** : Parfois nécessaire

### Logs et diagnostic

#### Activation des logs détaillés
```python
# Dans config.py
DEBUG = True
LOG_LEVEL = "DEBUG"
```

#### Fichiers de log
- `debug.log` : Logs de l'application
- `error.log` : Erreurs uniquement
- `access.log` : Accès et requêtes

#### Analyse des logs
```bash
# Erreurs récentes
tail -f debug.log | grep ERROR

# Temps de traitement
grep "Temps" debug.log

# Erreurs LLM
grep "LLM" debug.log
```

---

## ❓ FAQ

### Questions générales

**Q : L'application est-elle gratuite ?**
R : Oui, l'application est gratuite. Seuls les services LLM cloud (OpenRouter) peuvent avoir des coûts.

**Q : Quels types de fichiers sont supportés ?**
R : Seuls les fichiers PDF contenant des devis de matelas sont supportés.

**Q : L'application fonctionne-t-elle hors ligne ?**
R : Oui, avec Ollama (LLM local). OpenRouter nécessite une connexion internet.

**Q : Combien de fichiers puis-je traiter ?**
R : Aucune limite théorique. La limite pratique dépend de votre mémoire et espace disque.

### Questions techniques

**Q : Pourquoi le traitement prend-il du temps ?**
R : L'analyse LLM est intensive. Ollama est plus lent mais gratuit, OpenRouter est plus rapide mais payant.

**Q : Comment améliorer la précision ?**
R : Utilisez des PDF de bonne qualité, avec du texte clair et des spécifications détaillées.

**Q : Puis-je personnaliser les règles métier ?**
R : Oui, en modifiant les fichiers dans `backend/Référentiels/` et les modules `*_utils.py`.

**Q : Comment sauvegarder mes configurations ?**
R : Les résultats sont automatiquement sauvegardés dans le dossier `output/`.

### Questions d'utilisation

**Q : Que faire si un matelas n'est pas détecté ?**
R : Vérifiez que le type de matelas est dans la liste supportée. Contactez le support si nécessaire.

**Q : Comment corriger une erreur de dimension ?**
R : Modifiez manuellement dans l'onglet Configurations, puis relancez l'export.

**Q : Puis-je traiter des commandes en lot ?**
R : Oui, sélectionnez plusieurs fichiers PDF et traitez-les ensemble.

**Q : Comment exporter vers d'autres formats ?**
R : Utilisez l'onglet JSON pour récupérer les données brutes, puis convertissez selon vos besoins.

### Questions de support

**Q : Où trouver de l'aide supplémentaire ?**
R : Consultez ce guide, les logs de l'application, ou contactez le support technique.

**Q : Comment signaler un bug ?**
R : Incluez le fichier PDF, les logs d'erreur, et une description détaillée du problème.

**Q : L'application sera-t-elle mise à jour ?**
R : Oui, des mises à jour régulières sont prévues pour améliorer la précision et ajouter des fonctionnalités.

**Q : Puis-je contribuer au développement ?**
R : Oui, les contributions sont les bienvenues. Contactez l'équipe de développement.

---

## 🆘 Support technique

### Ressources disponibles

#### Documentation
- **Ce guide** : Guide complet d'utilisation
- **README_GUI.md** : Documentation de l'interface
- **README_PRE_IMPORT.md** : Documentation du pré-import
- **README_CLIENT_EXTRACTION.md** : Documentation de l'extraction client

#### Outils de diagnostic
- **Logs détaillés** : Activation via `config.py`
- **Mode debug** : Interface avec informations techniques
- **Tests unitaires** : Validation des fonctionnalités

#### Exemples et templates
- **Fichiers de test** : `test_*.py` dans le projet
- **Templates Excel** : `template/template_matelas.xlsx`
- **Exemples PDF** : Dossier `Commandes/`

### Contact et assistance

#### Informations de contact
- **Email** : [VOTRE_EMAIL]
- **Téléphone** : [VOTRE_TELEPHONE]
- **Horaires** : [HORAIRES_SUPPORT]

#### Informations requises
Lors d'une demande de support, fournissez :
- **Version** de l'application
- **Système d'exploitation** et version
- **Fichier PDF** problématique (si applicable)
- **Logs d'erreur** complets
- **Description détaillée** du problème

#### Processus de support
1. **Diagnostic** : Analyse du problème
2. **Solution** : Proposition de correction
3. **Test** : Validation de la solution
4. **Suivi** : Vérification du bon fonctionnement

### Mises à jour et maintenance

#### Versions disponibles
- **Version stable** : Recommandée pour la production
- **Version beta** : Nouvelles fonctionnalités
- **Version développement** : Pour les tests

#### Processus de mise à jour
1. **Sauvegarde** de vos données
2. **Téléchargement** de la nouvelle version
3. **Installation** selon le guide
4. **Test** de fonctionnement
5. **Migration** des données si nécessaire

#### Planification des mises à jour
- **Mises à jour mineures** : Mensuelles
- **Mises à jour majeures** : Trimestrielles
- **Corrections de bugs** : Selon les besoins

---

## 📝 Notes de version

### Version 1.0.0 (Date)
- ✅ Interface graphique complète
- ✅ Traitement LLM (Ollama/OpenRouter)
- ✅ Extraction des données client
- ✅ Détection automatique des matelas
- ✅ Pré-import Excel
- ✅ Export des résultats

### Prochaines fonctionnalités
- 🔄 Interface web améliorée
- 🔄 Support de nouveaux types de matelas
- 🔄 Intégration avec ERP
- 🔄 Traitement par lot avancé
- 🔄 API REST complète

---

*Ce guide est régulièrement mis à jour. Dernière mise à jour : [DATE]* 