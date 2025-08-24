#!/usr/bin/env python3
"""
Générateur de PDF Complet du Cahier des Charges - Literie Processor
Combinaison du cahier des charges, résumé exécutif et spécifications techniques
Avec logo Westelynck et mise en page professionnelle
"""

import os
import sys
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor, black, white, blue, darkblue, lightgrey
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors

def create_cahier_charges_complet_pdf():
    """Crée le PDF complet du cahier des charges professionnel"""
    
    # Configuration du document
    doc = SimpleDocTemplate(
        "Cahier_Charges_Complet_Literie_Processor.pdf",
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # Styles personnalisés
    styles = getSampleStyleSheet()
    
    # Style titre principal
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=HexColor('#1f4e79'),
        fontName='Helvetica-Bold'
    )
    
    # Style sous-titre
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=20,
        spaceBefore=20,
        textColor=HexColor('#2c5aa0'),
        fontName='Helvetica-Bold'
    )
    
    # Style section
    section_style = ParagraphStyle(
        'CustomSection',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=15,
        spaceBefore=15,
        textColor=HexColor('#1f4e79'),
        fontName='Helvetica-Bold'
    )
    
    # Style normal
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    )
    
    # Style liste
    list_style = ParagraphStyle(
        'CustomList',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=5,
        leftIndent=20,
        fontName='Helvetica'
    )
    
    # Style code
    code_style = ParagraphStyle(
        'CustomCode',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=8,
        leftIndent=20,
        fontName='Courier',
        backColor=HexColor('#f5f5f5'),
        borderWidth=1,
        borderColor=HexColor('#cccccc'),
        borderPadding=5
    )
    
    # Style highlight
    highlight_style = ParagraphStyle(
        'CustomHighlight',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        fontName='Helvetica-Bold',
        textColor=HexColor('#2c5aa0')
    )
    
    # Contenu du document
    story = []
    
    # Page de titre
    story.append(Spacer(1, 2*cm))
    
    # Logo Westelynck
    logo_path = "assets/logo_westelynck.png"
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=4*cm, height=2*cm)
        logo.hAlign = 'CENTER'
        story.append(logo)
        story.append(Spacer(1, 1*cm))
    
    # Titre principal
    story.append(Paragraph("CAHIER DES CHARGES COMPLET", title_style))
    story.append(Paragraph("Literie Processor", subtitle_style))
    story.append(Paragraph("Application de Traitement Automatisé des Devis Matelas", subtitle_style))
    story.append(Paragraph("Développé par SCINNOVA pour SAS Literie Westelynck", normal_style))
    
    story.append(Spacer(1, 2*cm))
    
    # Informations de version
    version_info = [
        ["Projet", "Literie Processor (anciennement MatelasApp)"],
        ["Client", "SAS Literie Westelynck"],
        ["Développeur", "SCINNOVA"],
        ["Version", "3.0.1"],
        ["Date", datetime.now().strftime("%d/%m/%Y")],
        ["Contact", "sebastien.confrere@scinnova.fr"]
    ]
    
    version_table = Table(version_info, colWidths=[3*cm, 8*cm])
    version_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#1f4e79')),
        ('TEXTCOLOR', (0, 0), (0, -1), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, black)
    ]))
    story.append(version_table)
    
    story.append(PageBreak())
    
    # Table des matières
    story.append(Paragraph("Table des Matières", title_style))
    story.append(Spacer(1, 1*cm))
    
    toc_items = [
        "PARTIE 1 : RÉSUMÉ EXÉCUTIF",
        "   1. Problématique et solution",
        "   2. Fonctionnalités clés",
        "   3. Avantages et ROI",
        "   4. Technologies et architecture",
        "   5. Planning et métriques",
        "",
        "PARTIE 2 : CAHIER DES CHARGES DÉTAILLÉ",
        "   1. Présentation du projet",
        "   2. Spécifications fonctionnelles",
        "   3. Spécifications techniques",
        "   4. Contraintes et exigences",
        "   5. Livrables",
        "   6. Planning et phases",
        "   7. Tests et validation",
        "   8. Maintenance et évolution",
        "   9. Risques et mitigation",
        "   10. Conclusion",
        "",
        "PARTIE 3 : SPÉCIFICATIONS TECHNIQUES",
        "   1. Architecture système",
        "   2. Modules détaillés",
        "   3. Structures de données",
        "   4. Performance et sécurité",
        "   5. Tests et déploiement"
    ]
    
    for item in toc_items:
        if item == "":
            story.append(Spacer(1, 0.5*cm))
        else:
            story.append(Paragraph(f"• {item}", list_style))
    
    story.append(PageBreak())
    
    # PARTIE 1 : RÉSUMÉ EXÉCUTIF
    story.append(Paragraph("PARTIE 1 : RÉSUMÉ EXÉCUTIF", title_style))
    story.append(PageBreak())
    
    # Problématique
    story.append(Paragraph("1. Problématique et solution", subtitle_style))
    
    story.append(Paragraph("""
        La SAS Literie Westelynck traite manuellement des centaines de devis PDF par mois, 
        ce qui représente un défi majeur pour la productivité et la qualité :
    """, normal_style))
    
    problemes = [
        "Temps perdu : 4-6 heures par jour de traitement manuel",
        "Erreurs humaines : 15-20% de corrections nécessaires",
        "Coût : 2000-3000€/mois en temps de traitement",
        "Délais : Retards dans la production",
        "Standardisation : Processus difficile à uniformiser"
    ]
    
    for probleme in problemes:
        story.append(Paragraph(f"• {probleme}", list_style))
    
    story.append(Paragraph("Solution proposée :", highlight_style))
    
    solutions = [
        "Application automatisée utilisant l'Intelligence Artificielle",
        "Analyse automatique des devis PDF avec GPT-4",
        "Génération de fichiers Excel prêts pour l'inscription",
        "Standardisation complète du processus"
    ]
    
    for solution in solutions:
        story.append(Paragraph(f"• {solution}", list_style))
    
    story.append(PageBreak())
    
    # Fonctionnalités clés
    story.append(Paragraph("2. Fonctionnalités clés", subtitle_style))
    
    story.append(Paragraph("✅ Traitement automatique", section_style))
    
    traitement_features = [
        "Lecture des PDF avec extraction de texte",
        "Analyse LLM (GPT-4) pour comprendre le contenu",
        "Extraction structurée des données (client, matelas, dimensions, prix)",
        "Validation automatique des informations"
    ]
    
    for feature in traitement_features:
        story.append(Paragraph(f"• {feature}", list_style))
    
    story.append(Paragraph("✅ Génération Excel", section_style))
    
    excel_features = [
        "Templates spécialisés par type de matelas",
        "Remplissage automatique des cellules",
        "Coloration conditionnelle selon les caractéristiques",
        "Support de 6 types de matelas différents"
    ]
    
    for feature in excel_features:
        story.append(Paragraph(f"• {feature}", list_style))
    
    story.append(Paragraph("✅ Interface utilisateur", section_style))
    
    ui_features = [
        "Interface moderne PyQt6 avec logo Westelynck",
        "Drag & drop des fichiers PDF",
        "Suivi en temps réel du traitement",
        "Gestion des erreurs et corrections"
    ]
    
    for feature in ui_features:
        story.append(Paragraph(f"• {feature}", list_style))
    
    story.append(PageBreak())
    
    # Avantages et ROI
    story.append(Paragraph("3. Avantages et ROI", subtitle_style))
    
    story.append(Paragraph("🚀 Gain de productivité", section_style))
    
    gains = [
        "Temps de traitement : 30 secondes vs 15 minutes manuellement",
        "Précision : 95%+ vs 80% manuellement",
        "Capacité : 10 devis simultanés vs 1 manuellement",
        "Standardisation : Processus uniforme"
    ]
    
    for gain in gains:
        story.append(Paragraph(f"• {gain}", list_style))
    
    story.append(Paragraph("💰 Retour sur investissement", section_style))
    
    roi = [
        "Économies : 2000-3000€/mois en temps de travail",
        "ROI : Amortissement en 3-6 mois",
        "Scalabilité : Pas de coût supplémentaire pour plus de volume",
        "Qualité : Réduction drastique des erreurs"
    ]
    
    for item in roi:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(PageBreak())
    
    # Technologies et architecture
    story.append(Paragraph("4. Technologies et architecture", subtitle_style))
    
    story.append(Paragraph("Technologies utilisées :", section_style))
    
    technologies = [
        "Python 3.8+ : Langage principal",
        "PyQt6 : Interface graphique moderne",
        "OpenAI GPT-4 : Intelligence artificielle",
        "PyPDF2 : Lecture des PDF",
        "openpyxl : Génération Excel",
        "Cryptographie : Sécurisation des clés API"
    ]
    
    for tech in technologies:
        story.append(Paragraph(f"• {tech}", list_style))
    
    story.append(Paragraph("Architecture :", section_style))
    
    story.append(Paragraph("""
        Frontend (PyQt6) ←→ Backend (Python) ←→ LLM APIs (OpenAI/OpenRouter)
    """, code_style))
    
    arch_features = [
        "Interface utilisateur PyQt6 moderne",
        "Modules backend spécialisés par type de matelas",
        "Intégration multi-providers LLM",
        "Système de sécurité et chiffrement"
    ]
    
    for feature in arch_features:
        story.append(Paragraph(f"• {feature}", list_style))
    
    story.append(PageBreak())
    
    # Planning et métriques
    story.append(Paragraph("5. Planning et métriques", subtitle_style))
    
    story.append(Paragraph("Planning :", section_style))
    
    story.append(Paragraph("✅ Phase 1 : Développement initial (TERMINÉE)", highlight_style))
    story.append(Paragraph("🔄 Phase 2 : Optimisation (EN COURS)", highlight_style))
    story.append(Paragraph("📋 Phase 3 : Évolutions futures", highlight_style))
    
    story.append(Paragraph("Métriques de succès :", section_style))
    
    metrics = [
        "Temps de traitement : < 30 secondes par devis",
        "Précision d'extraction : > 95%",
        "Taux d'adoption : 100% des utilisateurs formés",
        "ROI : Amortissement en 6 mois maximum",
        "Satisfaction utilisateur : > 90%"
    ]
    
    for metric in metrics:
        story.append(Paragraph(f"• {metric}", list_style))
    
    story.append(PageBreak())
    
    # PARTIE 2 : CAHIER DES CHARGES DÉTAILLÉ
    story.append(Paragraph("PARTIE 2 : CAHIER DES CHARGES DÉTAILLÉ", title_style))
    story.append(PageBreak())
    
    # Présentation du projet
    story.append(Paragraph("1. Présentation du projet", subtitle_style))
    
    story.append(Paragraph("1.1 Contexte et objectifs", section_style))
    
    story.append(Paragraph("""
        <b>Projet :</b> Literie Processor (anciennement MatelasApp)<br/>
        <b>Client :</b> SAS Literie Westelynck<br/>
        <b>Développeur :</b> SCINNOVA<br/>
        <b>Date de création :</b> 2025<br/>
        <b>Version actuelle :</b> 3.0.1
    """, normal_style))
    
    story.append(Paragraph("1.2 Problématique", section_style))
    
    story.append(Paragraph("""
        La SAS Literie Westelynck reçoit quotidiennement de nombreux devis de matelas au format PDF. 
        Le traitement manuel de ces devis présente plusieurs défis majeurs :
    """, normal_style))
    
    problemes_detailed = [
        "Chronophage : Plusieurs heures par jour de traitement manuel",
        "Source d'erreurs humaines : 15-20% de corrections nécessaires",
        "Difficile à standardiser : Processus non uniforme",
        "Coûteux en ressources humaines : 2000-3000€/mois",
        "Délais de production : Retards dus au traitement manuel"
    ]
    
    for probleme in problemes_detailed:
        story.append(Paragraph(f"• {probleme}", list_style))
    
    story.append(PageBreak())
    
    # Spécifications fonctionnelles
    story.append(Paragraph("2. Spécifications fonctionnelles", subtitle_style))
    
    story.append(Paragraph("2.1 Fonctionnalités principales", section_style))
    
    story.append(Paragraph("2.1.1 Traitement des devis PDF", section_style))
    
    pdf_features = [
        "Extraction de texte : Lecture et extraction du contenu textuel des fichiers PDF",
        "Analyse LLM : Utilisation d'intelligence artificielle pour comprendre et structurer les informations",
        "Validation : Vérification de la cohérence des données extraites",
        "Gestion d'erreurs : Traitement robuste des cas particuliers et des erreurs"
    ]
    
    for feature in pdf_features:
        story.append(Paragraph(f"• {feature}", list_style))
    
    story.append(Paragraph("2.1.2 Génération de fichiers Excel", section_style))
    
    excel_features_detailed = [
        "Templates spécialisés : Modèles Excel adaptés aux différents types de matelas",
        "Remplissage automatique : Insertion des données dans les cellules appropriées",
        "Coloration conditionnelle : Mise en forme visuelle selon les caractéristiques",
        "Validation des données : Vérification de la cohérence avant export"
    ]
    
    for feature in excel_features_detailed:
        story.append(Paragraph(f"• {feature}", list_style))
    
    story.append(PageBreak())
    
    # Types de matelas supportés
    story.append(Paragraph("2.2 Types de matelas supportés", section_style))
    
    matelas_types = [
        "Latex Naturel - Densité et épaisseur variables",
        "Latex Mixte 7 Zones - Zones de confort différenciées",
        "Latex Renforcé - Structure renforcée",
        "Mousse Viscoélastique - Mémoire de forme",
        "Mousse Rainurée 7 Zones - Structure aérée",
        "Select 43 - Mousse haute densité"
    ]
    
    for matelas in matelas_types:
        story.append(Paragraph(f"• {matelas}", list_style))
    
    story.append(PageBreak())
    
    # Spécifications techniques
    story.append(Paragraph("3. Spécifications techniques", subtitle_style))
    
    story.append(Paragraph("3.1 Architecture générale", section_style))
    
    story.append(Paragraph("3.1.1 Frontend (Interface utilisateur)", section_style))
    
    frontend_specs = [
        "Framework : PyQt6",
        "Design : Interface moderne et intuitive",
        "Responsive : Adaptation à différentes résolutions",
        "Thème : Intégration du logo Westelynck"
    ]
    
    for spec in frontend_specs:
        story.append(Paragraph(f"• {spec}", list_style))
    
    story.append(Paragraph("3.1.2 Backend (Traitement)", section_style))
    
    backend_specs = [
        "Langage : Python 3.8+",
        "Modules spécialisés : Un module par type de matelas",
        "API LLM : Intégration multi-providers",
        "Gestion des données : JSON et Excel"
    ]
    
    for spec in backend_specs:
        story.append(Paragraph(f"• {spec}", list_style))
    
    story.append(PageBreak())
    
    # Contraintes et exigences
    story.append(Paragraph("4. Contraintes et exigences", subtitle_style))
    
    story.append(Paragraph("4.1 Contraintes techniques", section_style))
    
    story.append(Paragraph("4.1.1 Compatibilité", section_style))
    
    compatibilite = [
        "Systèmes d'exploitation : Windows 10+, macOS 10.15+, Linux",
        "Python : Version 3.8 ou supérieure",
        "Mémoire : Minimum 4 GB RAM",
        "Espace disque : 500 MB pour l'installation"
    ]
    
    for item in compatibilite:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(Paragraph("4.1.2 Sécurité", section_style))
    
    securite = [
        "Chiffrement : AES-256 pour les clés API",
        "Validation : Vérification des entrées utilisateur",
        "Isolation : Pas d'accès réseau non autorisé"
    ]
    
    for item in securite:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(PageBreak())
    
    # Livrables
    story.append(Paragraph("5. Livrables", subtitle_style))
    
    story.append(Paragraph("5.1 Application principale", section_style))
    
    app_livrables = [
        "Exécutable standalone : Installation simple",
        "Interface graphique : PyQt6 moderne",
        "Documentation : Guide utilisateur complet"
    ]
    
    for livrable in app_livrables:
        story.append(Paragraph(f"• {livrable}", list_style))
    
    story.append(Paragraph("5.2 Documentation technique", section_style))
    
    doc_livrables = [
        "Cahier des charges : Ce document",
        "Documentation développeur : Guide technique",
        "API documentation : Référence des modules"
    ]
    
    for livrable in doc_livrables:
        story.append(Paragraph(f"• {livrable}", list_style))
    
    story.append(PageBreak())
    
    # Planning et phases
    story.append(Paragraph("6. Planning et phases", subtitle_style))
    
    story.append(Paragraph("6.1 Phase 1 : Développement initial (Terminée)", section_style))
    
    phase1 = [
        "Architecture : Structure modulaire",
        "Core modules : Modules de base",
        "Interface : GUI PyQt6",
        "Tests : Validation fonctionnelle"
    ]
    
    for item in phase1:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(Paragraph("6.2 Phase 2 : Optimisation (En cours)", section_style))
    
    phase2 = [
        "Performance : Optimisation des traitements",
        "Robustesse : Gestion d'erreurs avancée",
        "Documentation : Guides complets",
        "Packaging : Distribution standalone"
    ]
    
    for item in phase2:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(PageBreak())
    
    # Tests et validation
    story.append(Paragraph("7. Tests et validation", subtitle_style))
    
    story.append(Paragraph("7.1 Tests unitaires", section_style))
    
    tests_unitaires = [
        "Modules backend : Tests de chaque fonction",
        "Calculs : Validation des formules",
        "API : Tests des appels externes"
    ]
    
    for test in tests_unitaires:
        story.append(Paragraph(f"• {test}", list_style))
    
    story.append(Paragraph("7.2 Tests d'intégration", section_style))
    
    tests_integration = [
        "Workflow complet : PDF → Excel",
        "Interface : Tests utilisateur",
        "Performance : Tests de charge"
    ]
    
    for test in tests_integration:
        story.append(Paragraph(f"• {test}", list_style))
    
    story.append(PageBreak())
    
    # Maintenance et évolution
    story.append(Paragraph("8. Maintenance et évolution", subtitle_style))
    
    story.append(Paragraph("8.1 Maintenance préventive", section_style))
    
    maintenance_preventive = [
        "Monitoring : Surveillance des performances",
        "Logs : Analyse des erreurs",
        "Mises à jour : Corrections et améliorations"
    ]
    
    for item in maintenance_preventive:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(Paragraph("8.2 Maintenance corrective", section_style))
    
    maintenance_corrective = [
        "Bugs : Correction des erreurs",
        "Compatibilité : Adaptation aux évolutions",
        "Sécurité : Corrections de vulnérabilités"
    ]
    
    for item in maintenance_corrective:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(PageBreak())
    
    # Risques et mitigation
    story.append(Paragraph("9. Risques et mitigation", subtitle_style))
    
    story.append(Paragraph("9.1 Risques techniques", section_style))
    
    risques_tech = [
        "Évolution des APIs → Monitoring et adaptation",
        "Compatibilité → Tests réguliers",
        "Performance → Optimisation continue"
    ]
    
    for risque in risques_tech:
        story.append(Paragraph(f"• {risque}", list_style))
    
    story.append(Paragraph("9.2 Risques fonctionnels", section_style))
    
    risques_fonctionnels = [
        "Précision LLM → Amélioration des prompts",
        "Évolution des devis → Adaptation des modèles",
        "Formats → Support de nouveaux formats"
    ]
    
    for risque in risques_fonctionnels:
        story.append(Paragraph(f"• {risque}", list_style))
    
    story.append(PageBreak())
    
    # Conclusion
    story.append(Paragraph("10. Conclusion", subtitle_style))
    
    story.append(Paragraph("""
        Le projet Literie Processor répond parfaitement aux besoins de la SAS Literie Westelynck 
        en automatisant le traitement des devis PDF. L'application combine technologies modernes 
        (IA, interface graphique) et robustesse technique pour offrir une solution complète et évolutive.
    """, normal_style))
    
    story.append(Paragraph("Points forts :", highlight_style))
    
    points_forts = [
        "Automatisation complète du processus",
        "Précision élevée grâce à l'IA",
        "Interface utilisateur intuitive",
        "Architecture modulaire et évolutive",
        "Documentation complète"
    ]
    
    for point in points_forts:
        story.append(Paragraph(f"• {point}", list_style))
    
    story.append(Paragraph("Perspectives :", highlight_style))
    
    perspectives = [
        "Extension à d'autres types de documents",
        "Interface web pour accès distant",
        "Intégration avec les systèmes existants",
        "Développement d'une version SaaS"
    ]
    
    for perspective in perspectives:
        story.append(Paragraph(f"• {perspective}", list_style))
    
    story.append(PageBreak())
    
    # PARTIE 3 : SPÉCIFICATIONS TECHNIQUES
    story.append(Paragraph("PARTIE 3 : SPÉCIFICATIONS TECHNIQUES", title_style))
    story.append(PageBreak())
    
    # Architecture système
    story.append(Paragraph("1. Architecture système", subtitle_style))
    
    story.append(Paragraph("1.1 Vue d'ensemble", section_style))
    
    story.append(Paragraph("""
        L'application Literie Processor suit une architecture modulaire avec les composants suivants :
    """, normal_style))
    
    arch_components = [
        "Frontend PyQt6 : Interface utilisateur moderne",
        "Backend Python : Modules de traitement spécialisés",
        "APIs externes : OpenAI, OpenRouter pour l'IA",
        "Système de sécurité : Chiffrement des clés API",
        "Gestion des données : JSON et Excel"
    ]
    
    for component in arch_components:
        story.append(Paragraph(f"• {component}", list_style))
    
    story.append(Paragraph("1.2 Communication inter-modules", section_style))
    
    story.append(Paragraph("""
        La communication entre les modules s'effectue via :
    """, normal_style))
    
    communication = [
        "backend_interface.py : Interface principale",
        "JSON : Format de sérialisation des données",
        "Exceptions structurées : Gestion d'erreurs",
        "Logs détaillés : Traçabilité complète"
    ]
    
    for item in communication:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(PageBreak())
    
    # Modules détaillés
    story.append(Paragraph("2. Modules détaillés", subtitle_style))
    
    story.append(Paragraph("2.1 Module Interface (app_gui.py)", section_style))
    
    gui_features = [
        "Classe MatelasApp : Application principale PyQt6",
        "Widgets : QFileDialog, QProgressBar, QTextEdit, QTableWidget",
        "Événements : Drag & drop, sélection multiple, raccourcis clavier",
        "Threading : Traitement asynchrone avec QThread"
    ]
    
    for feature in gui_features:
        story.append(Paragraph(f"• {feature}", list_style))
    
    story.append(Paragraph("2.2 Module Backend Interface", section_style))
    
    backend_features = [
        "Workflow de traitement : Validation → Extraction → Analyse → Génération",
        "Gestion d'erreurs : Fichiers corrompus, APIs indisponibles, parsing échoué",
        "Validation : Vérification des données avant traitement",
        "Logs : Traçabilité complète des opérations"
    ]
    
    for feature in backend_features:
        story.append(Paragraph(f"• {feature}", list_style))
    
    story.append(PageBreak())
    
    # Structures de données
    story.append(Paragraph("3. Structures de données", subtitle_style))
    
    story.append(Paragraph("3.1 Format JSON d'entrée", section_style))
    
    story.append(Paragraph("""
        Le format JSON généré par l'IA contient :
    """, normal_style))
    
    json_structure = [
        "societe : Informations de la société",
        "client : Données client (nom, adresse, téléphone)",
        "configurations : Liste des matelas avec caractéristiques",
        "total_ht, tva, total_ttc : Calculs financiers"
    ]
    
    for structure in json_structure:
        story.append(Paragraph(f"• {structure}", list_style))
    
    story.append(Paragraph("3.2 Format de sortie Excel", section_style))
    
    excel_output = [
        "Feuille 1 : Données client et société",
        "Feuille 2 : Configurations matelas",
        "Feuille 3 : Configurations sommiers",
        "Feuille 4 : Résumé et totaux"
    ]
    
    for output in excel_output:
        story.append(Paragraph(f"• {output}", list_style))
    
    story.append(PageBreak())
    
    # Performance et sécurité
    story.append(Paragraph("4. Performance et sécurité", subtitle_style))
    
    story.append(Paragraph("4.1 Métriques de performance", section_style))
    
    performance_metrics = [
        "Temps de traitement : < 30 secondes par devis",
        "Mémoire utilisée : < 500 MB",
        "CPU : < 50% d'utilisation moyenne",
        "I/O : Optimisation des lectures/écritures"
    ]
    
    for metric in performance_metrics:
        story.append(Paragraph(f"• {metric}", list_style))
    
    story.append(Paragraph("4.2 Optimisations implémentées", section_style))
    
    optimizations = [
        "Threading : Traitement asynchrone",
        "Caching : Mise en cache des référentiels",
        "Lazy loading : Chargement à la demande",
        "Compression : Réduction de la taille des données"
    ]
    
    for optimization in optimizations:
        story.append(Paragraph(f"• {optimization}", list_style))
    
    story.append(Paragraph("4.3 Sécurité", section_style))
    
    security_features = [
        "Chiffrement AES-256 : Pour les clés API",
        "Validation : Sanitisation des entrées utilisateur",
        "Isolation : Contrôle des accès réseau",
        "Logs d'audit : Traçabilité complète"
    ]
    
    for feature in security_features:
        story.append(Paragraph(f"• {feature}", list_style))
    
    story.append(PageBreak())
    
    # Tests et déploiement
    story.append(Paragraph("5. Tests et déploiement", subtitle_style))
    
    story.append(Paragraph("5.1 Tests unitaires", section_style))
    
    unit_tests = [
        "Modules backend : Tests de chaque fonction",
        "Calculs : Validation des formules",
        "API : Tests des appels externes",
        "Interface : Tests des widgets"
    ]
    
    for test in unit_tests:
        story.append(Paragraph(f"• {test}", list_style))
    
    story.append(Paragraph("5.2 Tests d'intégration", section_style))
    
    integration_tests = [
        "Workflow complet : PDF → JSON → Excel",
        "APIs externes : Tests des providers LLM",
        "Interface : Tests utilisateur",
        "Performance : Tests de charge"
    ]
    
    for test in integration_tests:
        story.append(Paragraph(f"• {test}", list_style))
    
    story.append(Paragraph("5.3 Déploiement", section_style))
    
    deployment = [
        "PyInstaller : Création d'exécutables standalone",
        "Cross-platform : Windows, macOS, Linux",
        "Dépendances : Inclusion automatique",
        "Installation : Scripts d'installation"
    ]
    
    for item in deployment:
        story.append(Paragraph(f"• {item}", list_style))
    
    # Page de fin
    story.append(PageBreak())
    
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("Cahier des Charges Complet", title_style))
    story.append(Paragraph("Literie Processor", subtitle_style))
    story.append(Paragraph("Développé par SCINNOVA", subtitle_style))
    story.append(Paragraph("Pour SAS Literie Westelynck", subtitle_style))
    story.append(Paragraph("Merci de votre confiance", normal_style))
    
    # Informations de contact
    story.append(Spacer(1, 2*cm))
    
    contact_info = [
        ["Contact technique", "sebastien.confrere@scinnova.fr"],
        ["Téléphone", "06.66.05.72.47"],
        ["Éditeur", "SCINNOVA"],
        ["Client", "SAS Literie Westelynck"]
    ]
    
    contact_table = Table(contact_info, colWidths=[4*cm, 7*cm])
    contact_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#1f4e79')),
        ('TEXTCOLOR', (0, 0), (0, -1), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, black)
    ]))
    story.append(contact_table)
    
    # Génération du PDF
    doc.build(story)
    print("✅ Cahier des charges complet PDF généré avec succès : Cahier_Charges_Complet_Literie_Processor.pdf")

if __name__ == "__main__":
    try:
        create_cahier_charges_complet_pdf()
    except Exception as e:
        print(f"❌ Erreur lors de la génération du PDF : {e}")
        sys.exit(1) 