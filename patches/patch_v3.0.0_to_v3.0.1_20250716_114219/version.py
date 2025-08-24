#!/usr/bin/env python3
"""
Fichier de version centralisé pour l'application Matelas Processor
"""

# Version principale de l'application
VERSION = "3.0.0"

# Informations de build
BUILD_DATE = "2025-07-16"
BUILD_NUMBER = "20250716"

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