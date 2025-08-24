#!/usr/bin/env python3
"""
Générateur de PDF du Résumé Exécutif - Literie Processor
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

def create_resume_executif_pdf():
    """Crée le PDF du résumé exécutif professionnel"""
    
    # Configuration du document
    doc = SimpleDocTemplate(
        "Resume_Executif_Literie_Processor.pdf",
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
    
    # Style metrics
    metrics_style = ParagraphStyle(
        'CustomMetrics',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        textColor=HexColor('#1f4e79'),
        backColor=HexColor('#f0f8ff'),
        borderWidth=1,
        borderColor=HexColor('#1f4e79'),
        borderPadding=10
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
    story.append(Paragraph("RÉSUMÉ EXÉCUTIF", title_style))
    story.append(Paragraph("Literie Processor", subtitle_style))
    story.append(Paragraph("Application de Traitement Automatisé des Devis Matelas", subtitle_style))
    story.append(Paragraph("Développé par SCINNOVA pour SAS Literie Westelynck", normal_style))
    
    story.append(Spacer(1, 2*cm))
    
    # Informations de version
    version_info = [
        ["Projet", "Literie Processor"],
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
    
    # PROBLÉMATIQUE
    story.append(Paragraph("PROBLÉMATIQUE", subtitle_style))
    
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
    
    story.append(Spacer(1, 1*cm))
    
    # SOLUTION
    story.append(Paragraph("SOLUTION", subtitle_style))
    
    story.append(Paragraph("""
        Application automatisée utilisant l'Intelligence Artificielle pour :
    """, normal_style))
    
    solutions = [
        "Analyser les devis PDF automatiquement",
        "Extraire les informations structurées",
        "Générer des fichiers Excel prêts pour l'inscription",
        "Standardiser le processus de traitement"
    ]
    
    for solution in solutions:
        story.append(Paragraph(f"• {solution}", list_style))
    
    story.append(PageBreak())
    
    # FONCTIONNALITÉS CLÉS
    story.append(Paragraph("FONCTIONNALITÉS CLÉS", subtitle_style))
    
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
    
    # TYPES DE MATELAS SUPPORTÉS
    story.append(Paragraph("TYPES DE MATELAS SUPPORTÉS", subtitle_style))
    
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
    
    # AVANTAGES
    story.append(Paragraph("AVANTAGES", subtitle_style))
    
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
    
    story.append(Paragraph("🎯 Qualité", section_style))
    
    qualite = [
        "Standardisation : Processus uniforme",
        "Traçabilité : Logs complets de toutes les opérations",
        "Fiabilité : Gestion robuste des erreurs"
    ]
    
    for item in qualite:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(PageBreak())
    
    # TECHNOLOGIES UTILISÉES
    story.append(Paragraph("TECHNOLOGIES UTILISÉES", subtitle_style))
    
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
    
    story.append(Spacer(1, 1*cm))
    
    # ARCHITECTURE
    story.append(Paragraph("ARCHITECTURE", section_style))
    
    story.append(Paragraph("""
        Frontend (PyQt6) ←→ Backend (Python) ←→ LLM APIs (OpenAI/OpenRouter)
    """, normal_style))
    
    story.append(Paragraph("""
        L'application suit une architecture modulaire avec :
    """, normal_style))
    
    arch_features = [
        "Interface utilisateur PyQt6 moderne",
        "Modules backend spécialisés par type de matelas",
        "Intégration multi-providers LLM",
        "Système de sécurité et chiffrement"
    ]
    
    for feature in arch_features:
        story.append(Paragraph(f"• {feature}", list_style))
    
    story.append(PageBreak())
    
    # LIVRABLES
    story.append(Paragraph("LIVRABLES", subtitle_style))
    
    livrables = [
        "Application standalone : Exécutable Windows/macOS/Linux",
        "Documentation complète : Guide utilisateur et technique",
        "Templates Excel : Modèles pour chaque type de matelas",
        "Outils de maintenance : Diagnostic et réparation",
        "Formation : 2 heures pour les utilisateurs"
    ]
    
    for livrable in livrables:
        story.append(Paragraph(f"• {livrable}", list_style))
    
    story.append(Spacer(1, 1*cm))
    
    # PLANNING
    story.append(Paragraph("PLANNING", section_style))
    
    story.append(Paragraph("✅ Phase 1 : Développement initial (TERMINÉE)", highlight_style))
    
    phase1 = [
        "Architecture modulaire",
        "Modules de base",
        "Interface graphique",
        "Tests fonctionnels"
    ]
    
    for item in phase1:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(Paragraph("🔄 Phase 2 : Optimisation (EN COURS)", highlight_style))
    
    phase2 = [
        "Performance et robustesse",
        "Documentation complète",
        "Packaging standalone",
        "Tests de validation"
    ]
    
    for item in phase2:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(Paragraph("📋 Phase 3 : Évolutions futures", highlight_style))
    
    phase3 = [
        "Nouveaux types de matelas",
        "Interface web",
        "Version SaaS",
        "Application mobile"
    ]
    
    for item in phase3:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(PageBreak())
    
    # MÉTRIQUES DE SUCCÈS
    story.append(Paragraph("MÉTRIQUES DE SUCCÈS", subtitle_style))
    
    story.append(Paragraph("""
        Les objectifs de performance et de qualité définis pour le projet :
    """, normal_style))
    
    metrics = [
        "Temps de traitement : < 30 secondes par devis",
        "Précision d'extraction : > 95%",
        "Taux d'adoption : 100% des utilisateurs formés",
        "ROI : Amortissement en 6 mois maximum",
        "Satisfaction utilisateur : > 90%"
    ]
    
    for metric in metrics:
        story.append(Paragraph(f"• {metric}", list_style))
    
    story.append(Spacer(1, 1*cm))
    
    # RISQUES ET MITIGATION
    story.append(Paragraph("RISQUES ET MITIGATION", section_style))
    
    story.append(Paragraph("⚠️ Risques techniques", highlight_style))
    
    risques_tech = [
        "Évolution des APIs → Monitoring et adaptation",
        "Compatibilité → Tests réguliers",
        "Performance → Optimisation continue"
    ]
    
    for risque in risques_tech:
        story.append(Paragraph(f"• {risque}", list_style))
    
    story.append(Paragraph("⚠️ Risques fonctionnels", highlight_style))
    
    risques_fonctionnels = [
        "Précision LLM → Amélioration des prompts",
        "Évolution des devis → Adaptation des modèles",
        "Formats → Support de nouveaux formats"
    ]
    
    for risque in risques_fonctionnels:
        story.append(Paragraph(f"• {risque}", list_style))
    
    story.append(PageBreak())
    
    # CONCLUSION
    story.append(Paragraph("CONCLUSION", subtitle_style))
    
    story.append(Paragraph("""
        Le projet Literie Processor transforme radicalement le processus de traitement 
        des devis de la SAS Literie Westelynck en :
    """, normal_style))
    
    impacts = [
        "Automatisant 95% du travail manuel",
        "Réduisant les erreurs de 80% à 5%",
        "Accélérant le traitement par 30x",
        "Standardisant le processus de production"
    ]
    
    for impact in impacts:
        story.append(Paragraph(f"• {impact}", list_style))
    
    story.append(Spacer(1, 1*cm))
    
    story.append(Paragraph("""
        L'investissement est rapidement amorti et l'application offre une base solide 
        pour les évolutions futures.
    """, normal_style))
    
    # Page de fin
    story.append(PageBreak())
    
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("Résumé Exécutif", title_style))
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
    print("✅ Résumé exécutif PDF généré avec succès : Resume_Executif_Literie_Processor.pdf")

if __name__ == "__main__":
    try:
        create_resume_executif_pdf()
    except Exception as e:
        print(f"❌ Erreur lors de la génération du PDF : {e}")
        sys.exit(1) 