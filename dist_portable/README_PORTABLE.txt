===============================================
    PROCESSEUR DE DEVIS LITERIE - VERSION PORTABLE
===============================================

INSTRUCTIONS D'INSTALLATION ET D'UTILISATION:

1. PREREQUIS:
   - Windows 10/11
   - Python 3.8 ou superieur installe
   - Connexion internet (pour premiere installation)

2. INSTALLATION:
   - Copiez ce dossier complet sur votre machine Windows
   - Aucune installation supplementaire requise

3. LANCEMENT:
   - Double-cliquez sur "Lancer_Matelas.bat"
   - Les dependances seront installees automatiquement
   - L'application se lancera

4. CONFIGURATION:
   - Editez "matelas_config.json" pour configurer vos cles API
   - Remplacez "VOTRE_CLE_API_ICI" par votre vraie cle
   - Pour saisir la cle API facilement: redimensionnez la fenetre!

5. PROBLEMES COURANTS:

   A. FENETRE NON REDIMENSIONNABLE:
      - Executez "Test_Resize.bat" pour appliquer le fix
      - Ou utilisez Alt+Espace puis "Agrandir" 
      - Ou double-cliquez sur la barre de titre
      - Ou faites glisser les bords de la fenetre avec la souris

   B. IMAGES NON AFFICHEES:
      - Verifiez que le dossier "assets/" est present
      - Contient: logo_westelynck.png, lit-double.png, etc.
      - Si manquant: recopiez depuis le projet principal

   C. MODULES MANQUANTS:
      - Executez "python check_dependencies.py" pour diagnostic
      - Ou relancez "Lancer_Matelas.bat" pour installation auto

6. FICHIERS INCLUS:
   - Lancer_Matelas.bat       -> Lanceur principal
   - check_dependencies.py    -> Verification des modules
   - quick_resize_fix.py      -> Fix redimensionnement
   - Test_Resize.bat         -> Test interface
   - assets/                 -> Images et icones
   - backend/                -> Modules metier
   - utilities/              -> Outils supplementaires

7. AVANTAGES VERSION PORTABLE:
   - Pas de probleme de taille de fichier
   - Installation rapide et simple
   - Facile a distribuer
   - Pas de permissions administrateur requises
   - Toutes les images incluses
   - Scripts de diagnostic integres

8. SUPPORT:
   - Probleme redimensionnement: Test_Resize.bat
   - Diagnostic complet: python check_dependencies.py
   - En cas de probleme, verifiez que Python est bien installe
   - Installez Python depuis https://python.org si necessaire

9. SAISIE CLE API:
   - Si vous ne pouvez pas voir le champ de saisie:
     1. Redimensionnez la fenetre en tirant les bords
     2. Ou utilisez Alt+Espace puis Agrandir
     3. Ou double-cliquez la barre de titre
     4. Le champ API Key apparaitra dans Configuration

===============================================
Developpe avec Python et PyQt6
Version Portable - Resolution problemes Windows
===============================================