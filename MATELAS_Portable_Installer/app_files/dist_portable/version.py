#!/usr/bin/env python3
"""
Fichier de version centralisé pour l'application Matelas Processor
"""

# Version principale de l'application
VERSION = "3.9.0"

# Informations de build
BUILD_DATE = "2025-07-17"
BUILD_NUMBER = "20250717"

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
    """Retourne le changelog de l'application"""
    return """
# Changelog - Matelas Processor

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