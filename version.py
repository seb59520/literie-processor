#!/usr/bin/env python3
"""
Fichier de version centralisé pour l'application Matelas Processor
"""

# Version principale de l'application
VERSION = "3.12.0"

# Informations de build
BUILD_DATE = "2025-09-02"
BUILD_NUMBER = "20250902_13"

# Informations complètes
VERSION_INFO = {
    "version": VERSION,
    "build_date": BUILD_DATE,
    "build_number": BUILD_NUMBER,
    "full_version": f"{VERSION} (Build {BUILD_NUMBER})"
}

def get_version():
    """Retourne la version de l'application"""
    return VERSION

def get_full_version():
    """Retourne la version complète avec build"""
    return VERSION_INFO["full_version"]

def get_version_info():
    """Retourne toutes les informations de version"""
    return VERSION_INFO.copy()

def get_changelog():
    """Retourne le changelog de l'application depuis NOTES_DE_VERSION.md"""
    import os
    # Chercher le fichier NOTES_DE_VERSION.md à côté de ce script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    notes_path = os.path.join(base_dir, "NOTES_DE_VERSION.md")
    if os.path.exists(notes_path):
        with open(notes_path, "r", encoding="utf-8") as f:
            return f.read()
    # Fallback : changelog historique intégré
    return _get_changelog_legacy()


def _get_changelog_legacy():
    """Changelog historique intégré (fallback)"""
    return """
# Changelog - Matelas Processor

## Version 3.11.11 (2025-09-02)

### 🔧 Corrections des problèmes de mise à jour
- **Erreur 500 corrigée** : Résolution du problème de téléchargement depuis le serveur distant
- **Interface de mise à jour améliorée** : Fenêtre plus visible avec styles CSS modernes
- **Serveur robuste** : Correction du chemin de téléchargement des packages
- **Visibilité optimisée** : Suppression de la transparence problématique des dialogs

### ✨ Améliorations visuelles
- **Dialog stylé** : Bordure bleue, fond opaque, boutons modernes
- **Contraste amélioré** : Texte plus lisible, couleurs professionnelles
- **Expérience utilisateur** : Interface plus claire et professionnelle

---

## Version 3.11.10 (2025-09-02)

### 🧪 Version de test
- **Test du système de mise à jour automatique** : Version créée spécialement pour tester la mise à jour à distance
- **Validation de la télémétrie** : Test de la remontée d'informations client
- **Vérification de l'indicateur** : Contrôle de l'affichage des notifications de mise à jour
- **Test de la distribution** : Validation du processus complet de déploiement

### 🔧 Améliorations techniques
- **Système de mise à jour** : Validation complète du cycle de vie des mises à jour
- **Interface utilisateur** : Test de l'indicateur en conditions réelles
- **Serveur de distribution** : Vérification de la robustesse du système

---

## Version 3.11.1 (2025-09-02)

### 🎨 Améliorations Interface Utilisateur
- **Onglets colorés** : Ajout de couleurs attrayantes aux onglets principaux
- **Design moderne** : Dégradés colorés pour chaque section de l'application
- **Couleurs par fonction** :
  - 🔵 Résumé - Bleu clair pour la vue d'ensemble
  - 🟣 Configurations - Violet clair pour les paramètres
  - 🟢 Pré-import - Vert clair pour la préparation
  - 🟠 Logs - Orange clair pour le monitoring
  - 🩷 Debug - Rose clair pour le débogage
  - 🟡 JSON/Excel - Couleurs spécialisées pour les données
- **Effets interactifs** : Survol et sélection avec animations fluides
- **Lisibilité améliorée** : Meilleur contraste et distinction visuelle

### 🔧 Améliorations Techniques
- **Méthodes utilitaires** : Fonctions pour éclaircir/assombrir les couleurs
- **Styles CSS avancés** : Utilisation de dégradés Qt modernes
- **Performance optimisée** : Application des styles sans impact sur les performances
- **Compatibilité** : Styles compatibles avec tous les thèmes système

### ✨ Expérience Utilisateur
- **Navigation intuitive** : Identification rapide des sections par couleur
- **Interface professionnelle** : Apparence moderne et soignée
- **Feedback visuel** : Réaction immédiate aux interactions utilisateur
- **Cohérence** : Palette de couleurs harmonieuse et cohérente

---

## Version 3.11.0 (2025-09-02)

### 🆕 Nouvelles fonctionnalités télémétrie
- **Système de télémétrie des postes clients** : Collecte automatique des informations des machines clientes
- **Interface d'administration avancée** : Gestion complète des postes connectés avec détails en temps réel
- **Monitoring en temps réel** : Suivi des connexions, versions, et activité des postes clients
- **Statistiques globales** : Répartition par OS, versions utilisées, clients actifs

### 🔧 Système de télémétrie
- **Collecte automatique** : Informations système, nom de poste, utilisateur, adresse IP
- **API détails client** : Endpoint `/api/v1/clients/{client_id}/details` pour informations complètes
- **Interface web dédiée** : Page `/admin/clients` pour visualiser tous les postes connectés
- **Filtres avancés** : Recherche par nom, statut (en ligne/hors ligne), version
- **Indicateurs visuels** : Statut de connexion avec code couleur (vert/rouge/orange)

### 🎨 Interface d'administration
- **Dashboard télémétrie** : Vue d'ensemble des postes clients avec statistiques
- **Cartes clients détaillées** : Affichage complet des informations par poste
- **Actions par client** : Boutons pour voir les détails et envoyer des pings
- **Actualisation automatique** : Rafraîchissement toutes les 30 secondes
- **Design moderne** : Interface Bootstrap responsive avec animations

### 📊 Données collectées
- **Informations système** : Nom de poste, utilisateur, plateforme OS
- **Version application** : Version actuelle installée sur chaque poste  
- **Connexion réseau** : Adresse IP, User-Agent, horodatage dernière connexion
- **Historique activité** : Première connexion, nombre de mises à jour effectuées
- **Téléchargements** : Log des téléchargements de mises à jour par poste

### 🔒 Sécurité et fiabilité
- **Authentification admin** : Protection de l'interface par login/mot de passe
- **Gestion des erreurs** : API robuste avec codes d'erreur appropriés
- **Stockage JSON** : Sauvegarde des données télémétrie dans des fichiers JSON
- **Nettoyage automatique** : Gestion de l'historique et suppression des données anciennes

### 🚀 Performance
- **Collecte non-intrusive** : Impact minimal sur les performances client
- **API optimisée** : Endpoints rapides et efficaces pour les données télémétrie
- **Stockage léger** : Fichiers JSON compacts avec données essentielles
- **Actualisation intelligente** : Mise à jour des données seulement si nécessaire

### 🧪 Tests et validation
- **Scripts de test complets** : Validation du système de télémétrie
- **Simulation clients** : Test avec données réalistes de postes clients
- **Vérification API** : Tests des endpoints de télémétrie et détails clients
- **Interface validée** : Tests de l'affichage et des fonctionnalités admin

---

## Version 3.10.2 (2025-09-02)

### 🆕 Nouvelles fonctionnalités majeures
- **Système de mise à jour automatique complet** : Détection, téléchargement et installation automatique des mises à jour
- **Interface de gestion des mises à jour** : Dialog moderne avec progression en temps réel et informations détaillées
- **Serveur de mises à jour intégré** : API RESTful pour distribuer les patches et mises à jour
- **Mise à jour automatique des versions** : Le fichier version.py est automatiquement mis à jour après installation
- **Redémarrage automatique** : L'application redémarre automatiquement après installation d'une mise à jour

### 🔧 Système de mise à jour
- **Détection intelligente** : Vérification automatique des nouvelles versions disponibles
- **Téléchargement sécurisé** : Téléchargement avec vérification d'intégrité et gestion des erreurs
- **Installation robuste** : Processus d'installation avec sauvegarde automatique des configurations
- **Préservation des données** : Les fichiers critiques (config, clés API) sont préservés lors des mises à jour
- **Gestion des conflits** : Résolution automatique des conflits de fichiers lors de l'installation

### 🐛 Corrections critiques
- **Bug de sauvegarde corrigé** : Correction du bug "[Errno 2] No such file or directory" lors du backup
- **Création automatique des répertoires** : Les répertoires parents sont maintenant créés automatiquement
- **Gestion robuste des chemins** : Amélioration de la gestion des chemins de fichiers multi-niveaux
- **Restauration sécurisée** : Processus de restauration des fichiers de configuration fiabilisé

### 🎨 Interface utilisateur améliorée
- **Dialog de mise à jour moderne** : Interface utilisateur intuitive avec informations complètes
- **Barre de progression intelligente** : Affichage du progrès de téléchargement en temps réel
- **Messages informatifs** : Descriptions détaillées des mises à jour avec changelog intégré
- **Boutons d'action clairs** : Options pour télécharger, reporter ou ignorer les mises à jour
- **Logs d'installation visibles** : Affichage en temps réel du processus d'installation

### 🔒 Sécurité et fiabilité
- **Sauvegarde automatique** : Création automatique de backups avant chaque mise à jour
- **Validation des téléchargements** : Vérification de l'intégrité des fichiers téléchargés
- **Rollback disponible** : Possibilité de restaurer la version précédente en cas de problème
- **Gestion des permissions** : Gestion correcte des permissions de fichiers lors des mises à jour
- **Isolation des processus** : Installation dans un environnement isolé pour éviter les conflits

### 🚀 Performance et optimisation
- **Téléchargement optimisé** : Téléchargement par chunks avec gestion de la bande passante
- **Installation rapide** : Processus d'installation optimisé avec extraction temporaire
- **Nettoyage automatique** : Suppression automatique des fichiers temporaires après installation
- **Gestion mémoire** : Optimisation de l'utilisation mémoire pendant les opérations
- **Timeouts configurables** : Timeouts adaptatifs selon la taille des fichiers

### 🧪 Tests et validation
- **Tests complets d'installation** : Suite de tests couvrant tous les cas d'usage
- **Tests de redémarrage** : Validation du processus de redémarrage automatique
- **Tests de récupération** : Validation des mécanismes de recovery en cas d'erreur
- **Simulation client/serveur** : Tests de bout en bout du processus de mise à jour
- **Tests de compatibilité** : Validation avec différentes configurations système

### 📚 Documentation technique
- **Guide d'administration** : Documentation complète du serveur de mises à jour
- **API de mise à jour** : Documentation des endpoints REST pour les mises à jour
- **Guide de déploiement** : Instructions pour configurer le serveur de mises à jour
- **Troubleshooting** : Guide de résolution des problèmes courants
- **Architecture système** : Documentation de l'architecture du système de mise à jour

### 🔧 Outils d'administration
- **Interface web d'administration** : Interface Bootstrap pour gérer les versions
- **Création automatique de versions** : Scripts pour automatiser la création de nouvelles versions
- **Statistiques de déploiement** : Suivi des téléchargements et installations
- **Gestion des manifests** : Outils pour gérer les métadonnées des versions
- **Scripts de test** : Outils pour valider le processus de mise à jour

---

## Version 3.9.0 (2025-07-17)

### 🎉 Nouveautés
- **Système d'alertes en temps réel** : Notifications instantanées et gestion proactive des événements
- **Interface utilisateur avancée** : Panneau d'alertes dédié avec animations fluides
- **Types d'alertes multiples** : INFO, WARNING, ERROR, SUCCESS, CRITICAL avec icônes et couleurs
- **Catégories d'alertes** : Système, Traitement, Validation, Réseau, Sécurité, Production
- **Notifications popup** : Dialogs pour alertes importantes avec auto-fermeture
- **Configuration complète** : Dialog de paramétrage des alertes par type
- **Intégration workflow** : Alertes automatiques dans le traitement des fichiers

### 🔧 Améliorations
- **Gestion automatique** : Auto-dismiss selon le type d'alerte (3s à 8s)
- **Compteur d'alertes** : Indicateur dans la barre de statut avec mise à jour en temps réel
- **Filtrage avancé** : Par type, catégorie, source avec méthodes utilitaires
- **Marquage intelligent** : Lu/non lu, fermé/actif avec statistiques
- **Limites et nettoyage** : Maximum 100 alertes, suppression automatique après 24h
- **Sérialisation** : Sauvegarde/restauration des alertes en JSON
- **Animations fluides** : Apparition/disparition avec QPropertyAnimation

### 🎨 Interface utilisateur
- **Panneau d'alertes** : Onglet dédié "🚨 Alertes" dans l'interface principale
- **Widgets d'alertes** : Design moderne avec icônes, couleurs et boutons de fermeture
- **Barre de statut** : Compteur d'alertes avec indicateur coloré (vert/rouge)
- **Menu configuration** : Réglages → 🚨 Configuration des alertes
- **Responsive design** : Adaptation automatique de la hauteur selon le nombre d'alertes

### 🧪 Tests et qualité
- **Tests unitaires complets** : 14 tests couvrant toutes les fonctionnalités
- **Test d'intégration** : Démonstration complète avec 5 types d'alertes
- **Validation robuste** : Gestion d'erreurs et fallbacks
- **Documentation détaillée** : Guide complet d'utilisation et d'intégration

### 🔧 Intégration technique
- **Signaux PyQt6** : Communication asynchrone entre composants
- **Thread-safe** : Compatible avec le traitement multi-thread existant
- **Méthodes utilitaires** : add_system_alert(), add_processing_alert(), etc.
- **Points d'intégration** : Début/fin de traitement, gestion d'erreurs
- **Compatibilité** : Aucune modification du code backend existant

### 📚 Documentation
- **Guide utilisateur** : Utilisation du panneau d'alertes et configuration
- **Guide développeur** : Intégration et API du système d'alertes
- **Architecture technique** : Classes, signaux, et workflow
- **Exemples d'utilisation** : Code d'intégration et cas d'usage
- **Dépannage** : Solutions aux problèmes courants

---

## Version 3.8.0 (2025-07-17)

### 🎉 Nouveautés
- **Système d'alertes de noyaux non détectés** : Détection automatique et correction interactive des noyaux "INCONNU"
- **Interface utilisateur dédiée** : Dialog NoyauAlertDialog avec liste déroulante pour corriger les noyaux
- **Gestion multi-fichiers** : Identification claire des alertes par nom de fichier
- **Workflow intégré** : Priorité des alertes avant les recommandations de production

### 🔧 Améliorations
- **Détection automatique** : Identification des noyaux non détectés pendant l'analyse LLM
- **Interface intuitive** : 
  - Tableau détaillé avec index, description, noyau détecté, correction
  - Liste déroulante avec 6 types de noyaux disponibles
  - Boutons d'action pour correction par fichier ou globale
- **Types de noyaux supportés** :
  - LATEX NATUREL
  - LATEX MIXTE 7 ZONES
  - MOUSSE RAINUREE 7 ZONES
  - LATEX RENFORCE
  - SELECT 43
  - MOUSSE VISCO
- **Intégration transparente** :
  - Aucune modification du code backend existant
  - Compatibilité totale avec les fonctionnalités actuelles
  - Gestion d'erreurs robuste avec fallbacks

### 🐛 Corrections
- Amélioration de la détection des noyaux non identifiés
- Correction de l'affichage des alertes par fichier
- Amélioration de la gestion des corrections utilisateur

### 📚 Documentation
- Documentation complète du système d'alertes de noyaux
- Guide d'utilisation de l'interface de correction
- Tests automatisés pour validation des fonctionnalités
- Scripts de test avec fichiers réels

### 🔒 Sécurité
- Validation des corrections utilisateur
- Gestion sécurisée des données de correction

---

## Version 3.7.0 (2025-07-17)

### 🎉 Nouveautés
- **Support complet OpenAI** : Intégration native du provider OpenAI avec gestion des clés API
- **Numérotation continue Excel** : Numérotation automatique des cas entre fichiers Excel pour la même semaine
- **Gestion intelligente des quantités** : Détection automatique des jumeaux et traitement des quantités
- **Parsing JSON robuste** : Gestion avancée des réponses LLM avec correction automatique

### 🔧 Améliorations
- **Provider OpenAI** : Support complet avec validation des clés API et gestion des erreurs
- **Numérotation Excel** : 
  - Numérotation continue entre fichiers (1-10, 11-20, etc.)
  - Fonctionne pour matelas et sommiers
  - Colonnes C2, E2, G2... W2 et D2, F2... X2
- **Gestion des quantités** :
  - Détection automatique du mot "jumeaux" dans les descriptions
  - Quantité 2 + jumeaux = 1 configuration
  - Quantité 2 sans jumeaux = 2 configurations séparées
- **Parsing JSON LLM** :
  - Extraction automatique du JSON entouré de backticks
  - Correction des chaînes non terminées
  - Suppression des virgules finales orphelines
  - Gestion des réponses tronquées
- **Limites et timeouts** :
  - Timeout configurable (30s → 60s)
  - Limite de tokens optimisée (8000 tokens)
  - Gestion des erreurs 400 Bad Request

### 🐛 Corrections
- Correction de la duplication des configurations matelas liée aux quantités
- Amélioration de la gestion des erreurs OpenAI (timeout, 400 Bad Request)
- Correction du parsing JSON pour les réponses malformées
- Sauvegarde correcte de l'ordre des noyaux dans l'interface
- Correction de l'import get_version dans app_gui.py

### 📚 Documentation
- Documentation de l'intégration OpenAI
- Guide d'utilisation de la numérotation continue Excel
- Tests de validation pour les nouvelles fonctionnalités
- Documentation du parsing JSON robuste

### 🔒 Sécurité
- Validation renforcée des clés API OpenAI
- Gestion sécurisée des timeouts et limites

---

## Version 3.2.1 (2025-07-17)

### 🔧 Améliorations
- **Numérotation continue des cas** dans les fichiers Excel matelas et sommiers :
  - Le premier fichier va de 1 à 10, le second de 11 à 20, etc.
  - Colonnes C2, E2, G2... W2 et D2, F2... X2
  - Fonctionne pour tous les exports multi-fichiers
- **Correction du mapping** pour supporter tuples et chaînes dans les mappings

### 🐛 Corrections
- Correction du mapping pour supporter à la fois les tuples et les chaînes dans les mappings par défaut et personnalisés

---

## Version 3.2.0 (2025-07-17)

### 🎉 Nouveautés
- Ajout de l'onglet Maintenance avec gestion des tests automatisés

### 🔧 Améliorations
- Mise à jour automatique de la version
- Amélioration du système de changelog

### 📚 Documentation
- Documentation des nouvelles fonctionnalités
- Tests de validation

---

## Version 3.1.0 (2025-07-17)

### 🔧 Améliorations
- **Prompt LLM amélioré** : Instructions explicites pour extraire la description complète des matelas
- **Détection FDL** : Ajout de la détection "Fermeture de Liaison" avec toutes ses variantes
- **Mapping FDL_C51** : Nouveau champ C51 pour la fermeture de liaison dans le pré-import
- **Prévention de troncature** : Le LLM ne tronque plus les descriptions de matelas

### 🐛 Corrections
- Correction de l'extraction incomplète des descriptions matelas par le LLM
- Amélioration de la détection de la matière housse TENCEL LUXE 3D
- Correction du calcul des dimensions housse pour les matelas RAINUREE
- Amélioration du système de mise à jour du changelog

### 📚 Documentation
- Documentation de la correction du prompt LLM
- Guide d'utilisation du nouveau champ FDL_C51
- Tests de validation pour la détection FDL

---

## Version 3.0.0 (2025-07-16)

### 🎉 Nouveautés
- **Système d'administration unifié** : Fusion du gestionnaire de mises à jour avec l'administration
- **Actions rapides de version** : Mise à jour patch/mineure/majeure en un clic
- **Interface simplifiée** : Un seul point d'entrée pour toutes les opérations d'administration
- **Liste des patches en temps réel** : Affichage dynamique des patches disponibles

### 🔧 Améliorations
- **Menu Réglages optimisé** : Suppression de la duplication, interface plus claire
- **Système de logging avancé** : Traçabilité complète des actions d'administration
- **Gestion des versions améliorée** : Incrémentation automatique intelligente
- **Interface utilisateur cohérente** : Design unifié et intuitif

### 🐛 Corrections
- Correction de l'erreur QLineEdit.getText() dans PyQt6
- Nettoyage du changelog et suppression des entrées dupliquées
- Amélioration de la lisibilité du changelog
- Correction des imports manquants

### 📚 Documentation
- Documentation complète de la fusion des systèmes
- Guide d'utilisation du nouveau système d'administration
- Tests automatisés pour validation

---

## Version 2.2.0 (2025-07-16)

### 🎉 Nouveautés
- **Système de version centralisé** avec fichier version.py
- **Affichage de la version** dans l'interface principale
- **Menu réorganisé** selon les standards (Réglages avant Aide)
- **Changelog intégré** accessible via le menu Aide
- **Gestionnaire de patches** pour les mises à jour

### 🔧 Améliorations
- **Interface utilisateur** : Version visible dans le titre et le panneau gauche
- **Menu Réglages** : Regroupement logique de toutes les options de configuration
- **Menu Aide** : Ajout du changelog et réorganisation
- **Cohérence** : Version identique partout dans l'application

### 🐛 Corrections
- Correction de l'ordre des menus selon les standards
- Amélioration de l'affichage de la version
- Correction des imports de version

### 📚 Documentation
- Documentation complète du système de version
- Guide de maintenance des versions
- Tests automatisés pour validation

---

## Version 2.1.0 (2025-07-16)

### 🔧 Améliorations
- **Versionning** : Système de gestion des versions
- **Changelog** : Amélioration de l'affichage du changelog
- **Patches** : Système de patches pour les mises à jour

---

## Version 1.0.0 (2025-01-27)

### 🎉 Nouveautés
- **Interface graphique complète** avec PyQt6
- **Traitement automatisé** des devis PDF
- **Support LLM** pour l'extraction de données
- **Calculs automatiques** des dimensions housse
- **Export Excel** avec pré-import
- **Gestion des clés API** sécurisée
- **Tests automatisés** complets
- **Système de logs** avancé

### 🔧 Fonctionnalités
- **Types de matelas supportés** :
  - Latex Mixte 7 Zones
  - Latex Naturel
  - Latex Renforcé
  - Mousse Viscoélastique
  - Mousse Rainurée 7 Zones
  - Select 43

- **Providers LLM supportés** :
  - OpenAI
  - Anthropic
  - Gemini
  - Mistral
  - OpenRouter
  - Ollama

- **Fonctionnalités avancées** :
  - Gestion des clés API sécurisée
  - Surveillance des coûts OpenRouter
  - Configuration des mappings Excel
  - Gestionnaire de mises à jour
  - Documentation de maintenance
  - Tests automatisés

### 🐛 Corrections
- Correction de la détection des poignées pour TENCEL LUXE 3D
- Amélioration de la coloration conditionnelle Excel
- Optimisation des calculs de dimensions housse
- Correction des problèmes d'encodage

### 📚 Documentation
- Guide d'aide complet intégré
- Documentation de maintenance
- Instructions d'installation
- Guide de configuration

### 🔒 Sécurité
- Stockage sécurisé des clés API
- Validation des données d'entrée
- Gestion des erreurs robuste

---

**Note** : Cette version représente la première version stable de l'application Matelas Processor.
"""

if __name__ == "__main__":
    print(f"Matelas Processor - Version {get_full_version()}")
    print(f"Build date: {BUILD_DATE}")
    print(f"Build number: {BUILD_NUMBER}") 