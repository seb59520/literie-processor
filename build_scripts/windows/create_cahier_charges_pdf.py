#!/usr/bin/env python3
"""
Générateur de PDF du Cahier des Charges - Literie Processor
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

def create_cahier_charges_pdf():
    """Crée le PDF du cahier des charges professionnel"""
    
    # Configuration du document
    doc = SimpleDocTemplate(
        "Cahier_Charges_Literie_Processor.pdf",
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
    story.append(Paragraph("CAHIER DES CHARGES", title_style))
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
        "1. Présentation du projet",
        "   1.1 Contexte et objectifs",
        "   1.2 Problématique",
        "   1.3 Solution proposée",
        "2. Spécifications fonctionnelles",
        "   2.1 Fonctionnalités principales",
        "   2.2 Types de matelas supportés",
        "   2.3 Fonctionnalités avancées",
        "3. Spécifications techniques",
        "   3.1 Architecture générale",
        "   3.2 Technologies utilisées",
        "   3.3 Structure des données",
        "   3.4 Performance et scalabilité",
        "4. Contraintes et exigences",
        "   4.1 Contraintes techniques",
        "   4.2 Contraintes fonctionnelles",
        "   4.3 Contraintes organisationnelles",
        "5. Livrables",
        "6. Planning et phases",
        "7. Tests et validation",
        "8. Maintenance et évolution",
        "9. Risques et mitigation",
        "10. Conclusion"
    ]
    
    for item in toc_items:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(PageBreak())
    
    # 1. Présentation du projet
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
    
    problemes = [
        "Chronophage : Plusieurs heures par jour de traitement manuel",
        "Source d'erreurs humaines : 15-20% de corrections nécessaires",
        "Difficile à standardiser : Processus non uniforme",
        "Coûteux en ressources humaines : 2000-3000€/mois",
        "Délais de production : Retards dus au traitement manuel"
    ]
    
    for probleme in problemes:
        story.append(Paragraph(f"• {probleme}", list_style))
    
    story.append(Paragraph("1.3 Solution proposée", section_style))
    
    story.append(Paragraph("""
        Développement d'une application automatisée capable de :
    """, normal_style))
    
    solutions = [
        "Analyser automatiquement les devis PDF",
        "Extraire les informations structurées",
        "Générer des fichiers Excel prêts pour l'inscription",
        "Standardiser le processus de traitement",
        "Réduire drastiquement les erreurs et le temps de traitement"
    ]
    
    for solution in solutions:
        story.append(Paragraph(f"• {solution}", list_style))
    
    story.append(PageBreak())
    
    # 2. Spécifications fonctionnelles
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
    
    excel_features = [
        "Templates spécialisés : Modèles Excel adaptés aux différents types de matelas",
        "Remplissage automatique : Insertion des données dans les cellules appropriées",
        "Coloration conditionnelle : Mise en forme visuelle selon les caractéristiques",
        "Validation des données : Vérification de la cohérence avant export"
    ]
    
    for feature in excel_features:
        story.append(Paragraph(f"• {feature}", list_style))
    
    story.append(Paragraph("2.1.3 Interface utilisateur", section_style))
    
    ui_features = [
        "Interface graphique moderne : Application PyQt6 avec design professionnel",
        "Sélection de fichiers : Interface drag & drop et sélection multiple",
        "Suivi en temps réel : Barre de progression et logs détaillés",
        "Gestion des résultats : Affichage et export des fichiers générés"
    ]
    
    for feature in ui_features:
        story.append(Paragraph(f"• {feature}", list_style))
    
    story.append(Paragraph("2.2 Types de matelas supportés", section_style))
    
    story.append(Paragraph("2.2.1 Latex Naturel", section_style))
    
    latex_naturel = [
        "Caractéristiques : Densité, épaisseur, dimensions",
        "Calculs spécifiques : Prix selon référentiel JSON",
        "Options : Différentes fermetés et finitions"
    ]
    
    for item in latex_naturel:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(Paragraph("2.2.2 Latex Mixte 7 Zones", section_style))
    
    latex_mixte = [
        "Zones de confort : 7 zones différenciées",
        "Matériaux : Latex naturel + synthétique",
        "Calculs : Prix par zone et global"
    ]
    
    for item in latex_mixte:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(Paragraph("2.2.3 Latex Renforcé", section_style))
    
    latex_renforce = [
        "Renforcement : Structure renforcée",
        "Applications : Usage intensif",
        "Prix : Majoration selon référentiel"
    ]
    
    for item in latex_renforce:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(Paragraph("2.2.4 Mousse Viscoélastique", section_style))
    
    mousse_visco = [
        "Propriétés : Mémoire de forme",
        "Densités : Différentes options disponibles",
        "Calculs : Prix selon densité et épaisseur"
    ]
    
    for item in mousse_visco:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(Paragraph("2.2.5 Mousse Rainurée 7 Zones", section_style))
    
    mousse_rainuree = [
        "Rainures : Structure aérée",
        "Zones : 7 zones de confort",
        "Ventilation : Amélioration de l'aération"
    ]
    
    for item in mousse_rainuree:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(Paragraph("2.2.6 Select 43", section_style))
    
    select_43 = [
        "Matériau spécial : Mousse haute densité",
        "Applications : Usage professionnel",
        "Calculs : Prix spécifique"
    ]
    
    for item in select_43:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(PageBreak())
    
    # 3. Spécifications techniques
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
    
    story.append(Paragraph("3.1.3 Communication", section_style))
    
    comm_specs = [
        "Interface : backend_interface.py",
        "Sérialisation : JSON pour les échanges",
        "Gestion d'erreurs : Exceptions structurées"
    ]
    
    for spec in comm_specs:
        story.append(Paragraph(f"• {spec}", list_style))
    
    story.append(Paragraph("3.2 Technologies utilisées", section_style))
    
    story.append(Paragraph("3.2.1 Core Python", section_style))
    
    core_tech = [
        "PyPDF2 : Lecture des fichiers PDF",
        "openpyxl : Manipulation des fichiers Excel",
        "requests : Appels API HTTP",
        "json : Sérialisation des données"
    ]
    
    for tech in core_tech:
        story.append(Paragraph(f"• {tech}", list_style))
    
    story.append(Paragraph("3.2.2 Interface graphique", section_style))
    
    gui_tech = [
        "PyQt6 : Framework GUI principal",
        "Qt Designer : Conception des interfaces",
        "QThread : Traitement asynchrone",
        "QProgressBar : Indicateurs de progression"
    ]
    
    for tech in gui_tech:
        story.append(Paragraph(f"• {tech}", list_style))
    
    story.append(Paragraph("3.2.3 Intelligence artificielle", section_style))
    
    ai_tech = [
        "OpenAI API : GPT-4 pour l'analyse",
        "OpenRouter : Alternative multi-modèles",
        "Prompts spécialisés : Instructions détaillées pour l'extraction"
    ]
    
    for tech in ai_tech:
        story.append(Paragraph(f"• {tech}", list_style))
    
    story.append(Paragraph("3.2.4 Sécurité et stockage", section_style))
    
    security_tech = [
        "Cryptographie : Chiffrement des clés API",
        "Configuration : Fichiers JSON sécurisés",
        "Logs : Traçabilité complète"
    ]
    
    for tech in security_tech:
        story.append(Paragraph(f"• {tech}", list_style))
    
    story.append(PageBreak())
    
    # 4. Contraintes et exigences
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
    
    story.append(Paragraph("4.1.3 Performance", section_style))
    
    performance = [
        "Temps de réponse : < 2 secondes pour l'interface",
        "Traitement : < 30 secondes par devis",
        "Mémoire : Gestion optimisée des ressources"
    ]
    
    for item in performance:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(Paragraph("4.2 Contraintes fonctionnelles", section_style))
    
    story.append(Paragraph("4.2.1 Précision", section_style))
    
    precision = [
        "Taux de réussite : > 95% d'extraction correcte",
        "Validation : Vérification automatique des données",
        "Correction : Possibilité de correction manuelle"
    ]
    
    for item in precision:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(Paragraph("4.2.2 Fiabilité", section_style))
    
    fiabilite = [
        "Robustesse : Gestion des cas d'erreur",
        "Récupération : Sauvegarde automatique",
        "Logs : Traçabilité complète"
    ]
    
    for item in fiabilite:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(PageBreak())
    
    # 5. Livrables
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
    
    story.append(Paragraph("5.3 Fichiers de configuration", section_style))
    
    config_livrables = [
        "Templates Excel : Modèles pour chaque type",
        "Référentiels JSON : Données de prix et calculs",
        "Mappings : Correspondances personnalisables"
    ]
    
    for livrable in config_livrables:
        story.append(Paragraph(f"• {livrable}", list_style))
    
    story.append(Paragraph("5.4 Outils de maintenance", section_style))
    
    maintenance_livrables = [
        "Scripts de diagnostic : Outils de dépannage",
        "Système de logs : Traçabilité complète",
        "Utilitaires : Outils d'administration"
    ]
    
    for livrable in maintenance_livrables:
        story.append(Paragraph(f"• {livrable}", list_style))
    
    story.append(PageBreak())
    
    # 6. Planning et phases
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
    
    story.append(Paragraph("6.3 Phase 3 : Évolutions futures", section_style))
    
    phase3 = [
        "Nouveaux types : Support de nouveaux matelas",
        "API REST : Interface web",
        "Cloud : Version SaaS",
        "Mobile : Application mobile"
    ]
    
    for item in phase3:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(PageBreak())
    
    # 7. Tests et validation
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
    
    story.append(Paragraph("7.3 Tests de validation", section_style))
    
    tests_validation = [
        "Cas réels : Tests avec vrais devis",
        "Précision : Vérification des extractions",
        "Robustesse : Tests d'erreurs"
    ]
    
    for test in tests_validation:
        story.append(Paragraph(f"• {test}", list_style))
    
    story.append(PageBreak())
    
    # 8. Maintenance et évolution
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
    
    story.append(Paragraph("8.3 Évolutions", section_style))
    
    evolutions = [
        "Nouvelles fonctionnalités : Ajouts demandés",
        "Optimisations : Amélioration des performances",
        "Intégrations : Nouvelles APIs"
    ]
    
    for evolution in evolutions:
        story.append(Paragraph(f"• {evolution}", list_style))
    
    story.append(PageBreak())
    
    # 9. Risques et mitigation
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
    
    story.append(Paragraph("9.3 Risques organisationnels", section_style))
    
    risques_org = [
        "Formation → Documentation complète",
        "Support → Contact technique dédié",
        "Évolution → Roadmap claire"
    ]
    
    for risque in risques_org:
        story.append(Paragraph(f"• {risque}", list_style))
    
    story.append(PageBreak())
    
    # 10. Conclusion
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
    
    # Page de fin
    story.append(PageBreak())
    
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("Cahier des Charges", title_style))
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
    print("✅ Cahier des charges PDF généré avec succès : Cahier_Charges_Literie_Processor.pdf")

if __name__ == "__main__":
    try:
        create_cahier_charges_pdf()
    except Exception as e:
        print(f"❌ Erreur lors de la génération du PDF : {e}")
        sys.exit(1) 