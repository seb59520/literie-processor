# Notes de version - Literie Processor

## 2026-03-11 — Sommiers : corrections calculs jumeaux

- Détection du type FIXE améliorée (gestion du tiret dans "JUMEAUX - FIXE")
- Finition structure : distinction HÊTRE lattes vs HÊTRE structure, ajout type MULTIPLIS
- Détection PAREMENTÉ sans préfixe "STRUCTURE"
- Calcul dimensions jumeaux corrigé (déductions -10/-6 selon finition, 0 pour FIXE)
- Hauteur décimale formatée avec virgule (ex: 11,5)
- Détection TIROIR/NICHE pour chevets
- Détection pieds centraux
- Simplification nom client (suppression civilité)
- Types sommier : FIXE / TPR / TT embout TPR / TT embout sur TENON

---

## 2025-09-22 — Version 3.12.0

- Système de mise à jour automatique
- Améliorations et corrections générales

---

## 2025-09-02 — Version 3.11.x

- Correction erreur 500 téléchargement serveur distant
- Interface de mise à jour améliorée
- Télémétrie des postes clients
- Onglets colorés dans l'interface

---

## 2025-09-02 — Version 3.10.x

- Système de mise à jour automatique complet (détection, téléchargement, installation)
- Interface d'administration web pour les versions
- Correction bug sauvegarde backup

---

## 2025-07-17 — Version 3.7 à 3.9

- Support complet OpenAI
- Numérotation continue Excel entre fichiers
- Gestion intelligente des quantités jumeaux
- Parsing JSON LLM robuste
- Système d'alertes en temps réel
- Alertes noyaux non détectés avec correction interactive

---

## 2025-07-16 — Version 2.x à 3.0

- Système d'administration unifié
- Version centralisée (version.py)
- Changelog intégré dans le menu Aide
- Gestionnaire de patches

---

## 2025-01-27 — Version 1.0.0

- Interface graphique PyQt6
- Traitement automatisé des devis PDF via LLM
- Export Excel avec pré-import
- Support 6 types de matelas et 6 providers LLM
- Gestion sécurisée des clés API
