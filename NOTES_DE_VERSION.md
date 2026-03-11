# Notes de version - Literie Processor

## 2026-03-11 — Sommiers : pipeline PDF et corrections Excel

### Extraction PDF
- Split articles individuels (LITERIE, SOMMIER, DOSSERET, PIEDS, METRAGE, etc.) au lieu d'un bloc monolithique
- Extraction ville client corrigée (filtrage adresse société BORRE et codes APE)
- Suppression boilerplate page 2 des PDFs multi-pages
- Suppression préfixes prix/quantité des descriptions articles

### Détection et calculs
- Détection du type FIXE améliorée (gestion du tiret dans "JUMEAUX - FIXE")
- Finition structure : distinction HÊTRE lattes vs HÊTRE structure, ajout type MULTIPLIS
- Détection PAREMENTÉ/PAREMENT ÉE (espaces PDF)
- Calcul dimensions jumeaux corrigé (déductions -10/-6 selon finition, 0 pour FIXE)
- Hauteur row 7 : utilise hauteur SOMMIER structure (pas LITERIE)
- Dimensions jumeaux row 11 : utilise dimensions SOMMIER structure (pas LITERIE)
- Hauteur décimale formatée avec virgule (ex: 11,5)
- Types sommier : FIXE / TPR / TT embout TPR / TT embout sur TENON

### Excel
- DOSSERET : détection par startsWith uniquement (évite faux positifs "pour dosseret")
- DOSSERET texte : nettoyé (espaces, accents, coupé après "BASE SOMMIERS")
- METRAGE PVC/TISSU : texte nettoyé (tirets, parenthèses supprimés)
- PLATINE DE RÉUNION : détection pluriel "PLATINES"
- Détection TIROIR/NICHE pour chevets
- Détection pieds centraux
- Simplification nom client (suppression civilité)
- Numéros de commande en entier

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
