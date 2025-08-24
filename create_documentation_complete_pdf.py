#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de génération de la documentation complète PDF
MatelasApp Westelynck - Documentation complète
"""

import os
import sys
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

def create_documentation_pdf():
    """Génère la documentation complète en PDF"""
    
    # Nom du fichier de sortie
    output_file = "Documentation_MatelasApp_Westelynck_Complete.pdf"
    
    # Création du document PDF
    doc = SimpleDocTemplate(
        output_file,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Styles personnalisés
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=20,
        spaceBefore=20,
        textColor=colors.darkblue
    )
    
    section_style = ParagraphStyle(
        'CustomSection',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=15,
        spaceBefore=15,
        textColor=colors.darkgreen
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_JUSTIFY
    )
    
    code_style = ParagraphStyle(
        'CustomCode',
        parent=styles['Code'],
        fontSize=9,
        spaceAfter=10,
        fontName='Courier',
        leftIndent=20,
        rightIndent=20,
        backColor=colors.lightgrey
    )
    
    # Contenu du document
    story = []
    
    # Page de titre
    story.append(Paragraph("DOCUMENTATION COMPLÈTE", title_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("MATELASAPP WESTELYNCK", title_style))
    story.append(Spacer(1, 40))
    story.append(Paragraph(f"Version 3.0.1 - {datetime.now().strftime('%d/%m/%Y')}", normal_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Système de traitement automatisé des commandes de literie", normal_style))
    story.append(PageBreak())
    
    # Table des matières
    story.append(Paragraph("TABLE DES MATIÈRES", subtitle_style))
    story.append(Spacer(1, 20))
    
    toc_items = [
        "1. Vue d'ensemble",
        "2. Système de dates et semaines", 
        "3. Système d'alertes en temps réel",
        "4. Modules de création et construction",
        "5. Scripts de build manuels",
        "6. Installation et configuration",
        "7. Utilisation",
        "8. Dépannage",
        "9. Maintenance"
    ]
    
    for item in toc_items:
        story.append(Paragraph(f"• {item}", normal_style))
    
    story.append(PageBreak())
    
    # 1. Vue d'ensemble
    story.append(Paragraph("1. VUE D'ENSEMBLE", subtitle_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph(
        "MatelasApp Westelynck est une application de traitement automatisé de commandes de literie "
        "développée pour Westelynck. Elle permet d'analyser des fichiers PDF de commandes, d'extraire "
        "les informations de matelas et sommiers, et de générer des fichiers Excel formatés pour la production.",
        normal_style
    ))
    
    story.append(Paragraph("Fonctionnalités principales :", section_style))
    features = [
        "• Analyse PDF : Extraction automatique des données de commandes",
        "• IA/LLM : Enrichissement des données via intelligence artificielle", 
        "• Génération Excel : Création de fichiers de production formatés",
        "• Coloration automatique : Mise en forme visuelle des données",
        "• Gestion des semaines : Organisation par semaines de production",
        "• Alertes temps réel : Notifications en temps réel",
        "• Build automatisé : Compilation et déploiement simplifiés"
    ]
    
    for feature in features:
        story.append(Paragraph(feature, normal_style))
    
    story.append(PageBreak())
    
    # 2. Système de dates et semaines
    story.append(Paragraph("2. SYSTÈME DE DATES ET SEMAINES", subtitle_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Format des semaines de production :", section_style))
    story.append(Paragraph("S{numéro_semaine}_{année}", code_style))
    story.append(Paragraph("Exemple: S31_2025 (Semaine 31 de 2025)", normal_style))
    
    story.append(Paragraph("Gestion automatique des dates :", section_style))
    date_features = [
        "• Détection automatique de la semaine courante",
        "• Calcul automatique de la semaine suivante", 
        "• Format standardisé : S{WW}_{YYYY}"
    ]
    
    for feature in date_features:
        story.append(Paragraph(feature, normal_style))
    
    story.append(Paragraph("Exemple de génération de nom de fichier :", section_style))
    story.append(Paragraph("nom_fichier = f\"Matelas_S{numero_semaine}_{annee}_{compteur}.xlsx\"", code_style))
    story.append(Paragraph("Résultat: Matelas_S31_2025_1.xlsx", normal_style))
    
    story.append(PageBreak())
    
    # 3. Système d'alertes en temps réel
    story.append(Paragraph("3. SYSTÈME D'ALERTES EN TEMPS RÉEL", subtitle_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Architecture des alertes :", section_style))
    alert_arch = [
        "AlertSystem",
        "├── AlertManager (Gestionnaire principal)",
        "├── AlertWidget (Interface utilisateur)", 
        "├── AlertTypes (Types d'alertes)",
        "└── AlertQueue (File d'attente)"
    ]
    
    for item in alert_arch:
        story.append(Paragraph(item, code_style))
    
    story.append(Paragraph("Types d'alertes disponibles :", section_style))
    alert_types = [
        "• Success : Opérations réussies",
        "• Warning : Avertissements",
        "• Error : Erreurs critiques",
        "• Info : Informations générales",
        "• Progress : Progression des opérations"
    ]
    
    for alert_type in alert_types:
        story.append(Paragraph(alert_type, normal_style))
    
    story.append(Paragraph("Caractéristiques des alertes :", section_style))
    alert_features = [
        "• Affichage automatique en temps réel",
        "• Fermeture automatique après délai configurable",
        "• Historique des alertes récentes",
        "• Actions utilisateur (fermer, effacer tout)",
        "• Intégration GUI avec PyQt6"
    ]
    
    for feature in alert_features:
        story.append(Paragraph(feature, normal_style))
    
    story.append(PageBreak())
    
    # 4. Modules de création et construction
    story.append(Paragraph("4. MODULES DE CRÉATION ET CONSTRUCTION", subtitle_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Architecture modulaire :", section_style))
    arch_items = [
        "MatelasApp/",
        "├── app_gui.py                 # Interface principale",
        "├── backend/                   # Modules backend",
        "│   ├── llm_provider.py       # Fournisseurs IA",
        "│   ├── excel_import_utils.py # Utilitaires Excel",
        "│   ├── pdf_utils.py          # Traitement PDF",
        "│   └── date_utils.py         # Gestion des dates",
        "├── build_scripts/            # Scripts de build",
        "│   └── windows/              # Scripts Windows",
        "└── assets/                   # Ressources"
    ]
    
    for item in arch_items:
        story.append(Paragraph(item, code_style))
    
    story.append(Paragraph("Modules principaux :", section_style))
    
    story.append(Paragraph("1. LLM Provider (backend/llm_provider.py)", section_style))
    llm_features = [
        "• Gestion multi-providers : OpenAI, OpenRouter, Ollama",
        "• Configuration centralisée des clés API",
        "• Fallback automatique en cas d'erreur",
        "• Cache intelligent des réponses"
    ]
    
    for feature in llm_features:
        story.append(Paragraph(feature, normal_style))
    
    story.append(Paragraph("2. Excel Import Utils (backend/excel_import_utils.py)", section_style))
    excel_features = [
        "• Génération Excel avec formatage avancé",
        "• Coloration automatique selon les données",
        "• Alignement intelligent des cellules",
        "• Gestion des templates matelas/sommiers"
    ]
    
    for feature in excel_features:
        story.append(Paragraph(feature, normal_style))
    
    story.append(PageBreak())
    
    # 5. Scripts de build manuels
    story.append(Paragraph("5. SCRIPTS DE BUILD MANUELS", subtitle_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Scripts ASCII Windows (Recommandés) :", section_style))
    
    story.append(Paragraph("1. Menu Principal (build_scripts/windows/menu_ascii.bat)", section_style))
    menu_code = [
        "@echo off",
        "chcp 65001 >nul",
        "",
        ":menu",
        "cls",
        "echo ========================================",
        "echo    MATELASAPP - MENU PRINCIPAL",
        "echo ========================================",
        "echo.",
        "echo Dossier: %CD%",
        "echo.",
        "echo Choisissez une option:",
        "echo.",
        "echo [1] Installation complete (recommandee)",
        "echo [2] Lancer l'application",
        "echo [3] Diagnostic complet",
        "echo [4] Nettoyer les builds",
        "echo [5] Informations",
        "echo [6] Quitter"
    ]
    
    for line in menu_code:
        story.append(Paragraph(line, code_style))
    
    story.append(Paragraph("Caractéristiques des scripts ASCII :", section_style))
    ascii_features = [
        "• Aucun caractère spécial (émojis, accents, symboles)",
        "• Format ASCII pur compatible Windows",
        "• Syntaxe batch standard sans caractères problématiques",
        "• Encodage UTF-8 avec chcp 65001",
        "• Début correct avec @echo off"
    ]
    
    for feature in ascii_features:
        story.append(Paragraph(feature, normal_style))
    
    story.append(PageBreak())
    
    # 6. Installation et configuration
    story.append(Paragraph("6. INSTALLATION ET CONFIGURATION", subtitle_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Prérequis système :", section_style))
    prereqs = [
        "• Python 3.8+ (recommandé 3.11+)",
        "• PyQt6 pour l'interface graphique",
        "• PyInstaller pour la compilation",
        "• Windows 10/11 (pour les scripts batch)"
    ]
    
    for prereq in prereqs:
        story.append(Paragraph(prereq, normal_style))
    
    story.append(Paragraph("Installation automatique :", section_style))
    story.append(Paragraph("# Double-cliquer sur", code_style))
    story.append(Paragraph("Lancer_MatelasApp_ASCII.bat", code_style))
    story.append(Paragraph("# Ou lancer directement", code_style))
    story.append(Paragraph("build_scripts\\windows\\menu_ascii.bat", code_style))
    
    story.append(Paragraph("Configuration des clés API :", section_style))
    api_config = [
        "{",
        '  "openrouter": {',
        '    "api_key": "votre_clé_api_ici",',
        '    "base_url": "https://openrouter.ai/api/v1"',
        '  },',
        '  "openai": {',
        '    "api_key": "votre_clé_api_ici",',
        '    "base_url": "https://api.openai.com/v1"',
        '  }',
        "}"
    ]
    
    for line in api_config:
        story.append(Paragraph(line, code_style))
    
    story.append(PageBreak())
    
    # 7. Utilisation
    story.append(Paragraph("7. UTILISATION", subtitle_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Lancement de l'application :", section_style))
    launch_steps = [
        "1. Double-cliquer sur Lancer_MatelasApp_ASCII.bat",
        "2. Choisir l'option 1 pour l'installation complète",
        "3. Attendre la compilation PyInstaller",
        "4. Lancer l'application via l'option 2"
    ]
    
    for step in launch_steps:
        story.append(Paragraph(step, normal_style))
    
    story.append(Paragraph("Interface utilisateur :", section_style))
    ui_parts = [
        "• Panneau gauche : Contrôles et configuration",
        "• Panneau central : Sélection de fichiers",
        "• Panneau droit : Résultats et prévisualisation",
        "• Barre de statut : Informations en temps réel"
    ]
    
    for part in ui_parts:
        story.append(Paragraph(part, normal_style))
    
    story.append(Paragraph("Traitement des commandes :", section_style))
    process_steps = [
        "1. Sélectionner les fichiers PDF de commandes",
        "2. Configurer le provider LLM (OpenRouter recommandé)",
        "3. Lancer le traitement",
        "4. Vérifier les résultats dans le panneau droit",
        "5. Ouvrir les fichiers Excel générés"
    ]
    
    for step in process_steps:
        story.append(Paragraph(step, normal_style))
    
    story.append(PageBreak())
    
    # 8. Dépannage
    story.append(Paragraph("8. DÉPANNAGE", subtitle_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Problèmes courants :", section_style))
    
    story.append(Paragraph("1. Erreurs d'encodage Windows", section_style))
    story.append(Paragraph("'ho' n'est pas reconnu en tant que commande interne", code_style))
    story.append(Paragraph("Solution : Utiliser les scripts ASCII (*_ascii.bat)", normal_style))
    
    story.append(Paragraph("2. Erreurs de clé API", section_style))
    story.append(Paragraph("401 Client Error: Unauthorized", code_style))
    story.append(Paragraph("Solution : Vérifier la clé API dans l'interface de gestion", normal_style))
    
    story.append(Paragraph("3. Erreurs PyQt6", section_style))
    story.append(Paragraph("ImportError: cannot import name 'QAction' from 'PyQt6.QtWidgets'", code_style))
    story.append(Paragraph("Solution : Réinstaller PyQt6 avec pip install --upgrade PyQt6", normal_style))
    
    story.append(Paragraph("Scripts de diagnostic :", section_style))
    diag_scripts = [
        "# Diagnostic complet",
        "build_scripts\\windows\\diagnostic_ascii.bat",
        "",
        "# Test rapide",
        "test_rapide_ascii.bat",
        "",
        "# Test détaillé",
        "test_scripts_ascii_windows.bat"
    ]
    
    for script in diag_scripts:
        story.append(Paragraph(script, code_style))
    
    story.append(PageBreak())
    
    # 9. Maintenance
    story.append(Paragraph("9. MAINTENANCE", subtitle_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Mise à jour de l'application :", section_style))
    update_steps = [
        "1. Sauvegarder les configurations importantes",
        "2. Télécharger la nouvelle version",
        "3. Remplacer les fichiers (sauf config/)",
        "4. Relancer l'installation"
    ]
    
    for step in update_steps:
        story.append(Paragraph(step, normal_style))
    
    story.append(Paragraph("Sauvegarde des données :", section_style))
    backup_items = [
        "• Configuration : config/ (clés API, mappings)",
        "• Référentiels : backend/Référentiels/",
        "• Templates : backend/template/",
        "• Logs : logs/"
    ]
    
    for item in backup_items:
        story.append(Paragraph(item, normal_style))
    
    story.append(Paragraph("Monitoring et performance :", section_style))
    monitoring_items = [
        "• Vérification des logs régulière",
        "• Nettoyage des fichiers temporaires",
        "• Mise à jour des dépendances",
        "• Sauvegarde des configurations"
    ]
    
    for item in monitoring_items:
        story.append(Paragraph(item, normal_style))
    
    story.append(PageBreak())
    
    # Support et contact
    story.append(Paragraph("SUPPORT ET CONTACT", subtitle_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("Documentation disponible :", section_style))
    docs = [
        "• GUIDE_INSTALLATION.md - Guide d'installation",
        "• GUIDE_TEST_SCRIPTS_ASCII.md - Test des scripts",
        "• RESUME_SCRIPTS_ASCII_FINAL.md - Résumé des scripts",
        "• CHANGELOG.md - Historique des versions"
    ]
    
    for doc in docs:
        story.append(Paragraph(doc, normal_style))
    
    story.append(Paragraph("En cas de problème :", section_style))
    support_steps = [
        "1. Consulter la documentation",
        "2. Exécuter les scripts de diagnostic",
        "3. Vérifier les logs d'erreur",
        "4. Contacter le support technique"
    ]
    
    for step in support_steps:
        story.append(Paragraph(step, normal_style))
    
    story.append(Paragraph("Informations système :", section_style))
    sys_info = [
        "• Version : 3.0.1",
        "• Dernière mise à jour : 19/07/2025",
        "• Compatibilité : Windows 10/11, macOS, Linux",
        "• Langage : Python 3.8+",
        "• Interface : PyQt6"
    ]
    
    for info in sys_info:
        story.append(Paragraph(info, normal_style))
    
    story.append(PageBreak())
    
    # Conclusion
    story.append(Paragraph("CONCLUSION", subtitle_style))
    story.append(Spacer(1, 20))
    
    story.append(Paragraph(
        "MatelasApp Westelynck est une solution complète et robuste pour le traitement automatisé "
        "des commandes de literie. Avec son système d'alertes en temps réel, sa gestion intelligente "
        "des dates et ses scripts de build optimisés, elle offre une expérience utilisateur fluide "
        "et professionnelle.",
        normal_style
    ))
    
    story.append(Spacer(1, 20))
    
    story.append(Paragraph(
        "Les scripts ASCII garantissent une compatibilité maximale avec Windows, éliminant les "
        "problèmes d'encodage courants. Le système modulaire permet une maintenance facile et "
        "des évolutions futures.",
        normal_style
    ))
    
    story.append(Spacer(1, 20))
    
    story.append(Paragraph(
        "Pour commencer : Double-cliquez sur Lancer_MatelasApp_ASCII.bat et suivez les instructions "
        "du menu principal.",
        normal_style
    ))
    
    # Génération du PDF
    try:
        doc.build(story)
        print(f"✅ Documentation PDF générée avec succès : {output_file}")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la génération du PDF : {e}")
        return False

if __name__ == "__main__":
    print("📄 Génération de la documentation complète PDF...")
    success = create_documentation_pdf()
    
    if success:
        print("🎉 Documentation complète générée avec succès !")
        print("📁 Fichier créé : Documentation_MatelasApp_Westelynck_Complete.pdf")
    else:
        print("💥 Échec de la génération de la documentation")
        sys.exit(1) 