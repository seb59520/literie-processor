#!/usr/bin/env python3
"""
Générateur de documentation PDF professionnelle pour MatelasApp
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

def create_professional_documentation():
    """Crée la documentation PDF professionnelle"""
    
    # Configuration du document
    doc = SimpleDocTemplate(
        "Documentation_MatelasApp_Westelynck.pdf",
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
    story.append(Paragraph("Literie Processor", title_style))
    story.append(Paragraph("Application de Traitement Automatisé des Devis Matelas", subtitle_style))
    story.append(Paragraph("Documentation d'Installation et d'Utilisation", subtitle_style))
    story.append(Paragraph("Développé par SCINNOVA pour SAS Literie Westelynck", normal_style))
    
    story.append(Spacer(1, 2*cm))
    
    # Informations de version
    version_info = [
        ["Version", "3.8.0"],
        ["Date de création", datetime.now().strftime("%d/%m/%Y")],
        ["Éditeur", "SCINNOVA"],
        ["Support", "sebastien.confrere@scinnova.fr"]
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
        "1. Vue d'ensemble de l'application",
        "2. Installation et configuration",
        "3. Interface utilisateur",
        "4. Traitement des devis PDF",
        "5. Fonctionnalités principales",
        "   5.1 Noyaux de traitement spécialisés",
        "   5.2 Prompt LLM - Intelligence Artificielle",
        "   5.3 Extraction automatique",
        "6. Export et résultats",
        "   6.1 Formats d'export",
        "   6.2 Structure des fichiers Excel",
        "   6.3 Inscription Excel détaillée",
        "   6.4 Validation des résultats",
        "7. Dépannage et support",
        "8. Annexes techniques"
    ]
    
    for item in toc_items:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(PageBreak())
    
    # 1. Vue d'ensemble
    story.append(Paragraph("1. Vue d'ensemble de l'application", subtitle_style))
    
    story.append(Paragraph("""
        Literie Processor est une application professionnelle développée par SCINNOVA pour SAS Literie Westelynck 
        afin d'automatiser le traitement des devis de matelas. Cette solution innovante 
        combine intelligence artificielle et traitement automatisé pour optimiser 
        votre processus de production.
    """, normal_style))
    
    story.append(Paragraph("1.1 Objectifs de l'application", section_style))
    
    objectives = [
        "Automatiser l'extraction des données depuis les devis PDF",
        "Analyser intelligemment le contenu avec l'IA (LLM)",
        "Calculer automatiquement les dimensions et configurations",
        "Générer des fichiers Excel prêts pour la production",
        "Gérer les données clients et les informations de commande",
        "Réduire les erreurs manuelles et accélérer le traitement"
    ]
    
    for obj in objectives:
        story.append(Paragraph(f"• {obj}", list_style))
    
    story.append(Paragraph("1.2 Types de matelas supportés", section_style))
    
    matelas_types = [
        "Latex Mixte 7 Zones - Matelas latex avec zones de confort",
        "Latex Naturel - Matelas latex 100% naturel",
        "Latex Renforcé - Matelas latex avec renfort",
        "Mousse Viscoélastique - Matelas mousse mémoire",
        "Mousse Rainurée 7 Zones - Mousse avec zones de confort",
        "Select 43 - Matelas spécialisé"
    ]
    
    for matelas in matelas_types:
        story.append(Paragraph(f"• {matelas}", list_style))
    
    story.append(PageBreak())
    
    # 2. Installation et configuration
    story.append(Paragraph("2. Installation et configuration", subtitle_style))
    
    story.append(Paragraph("2.1 Prérequis système", section_style))
    
    prereqs = [
        "Système d'exploitation : Windows 10/11, macOS 10.15+, Linux",
        "Mémoire RAM : 4 GB minimum (8 GB recommandé)",
        "Espace disque : 500 MB pour l'application",
        "Connexion internet : Pour les mises à jour et l'IA cloud"
    ]
    
    for prereq in prereqs:
        story.append(Paragraph(f"• {prereq}", list_style))
    
    story.append(Paragraph("2.2 Installation Windows", section_style))
    
    story.append(Paragraph("""
        <b>Option 1 - Installation automatique (Recommandée) :</b>
    """, normal_style))
    
    story.append(Paragraph("""
        1. Téléchargez le fichier ZIP de l'application
        2. Extrayez le contenu dans un dossier
        3. Double-cliquez sur install_windows.bat
        4. L'application se lance automatiquement
    """, list_style))
    
    story.append(Paragraph("""
        <b>Option 2 - Installation manuelle :</b>
    """, normal_style))
    
    story.append(Paragraph("""
        1. Installez Python 3.8+ depuis python.org
        2. Ouvrez un terminal dans le dossier de l'application
        3. Exécutez : pip install -r requirements_gui.txt
        4. Lancez : python run_gui.py
    """, list_style))
    
    story.append(Paragraph("2.3 Configuration initiale", section_style))
    
    story.append(Paragraph("""
        Après le premier lancement, configurez les paramètres suivants :
    """, normal_style))
    
    config_items = [
        "Enrichissement LLM : Activé par défaut (recommandé)",
        "Provider : Ollama (gratuit) ou OpenRouter (payant)",
        "Clé API : Requise uniquement pour OpenRouter",
        "Semaine de production : Numéro de semaine (1-53)",
        "Année de production : Année courante",
        "Commande client : Nom du client"
    ]
    
    for item in config_items:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(PageBreak())
    
    # 3. Interface utilisateur
    story.append(Paragraph("3. Interface utilisateur", subtitle_style))
    
    story.append(Paragraph("""
        L'interface de Literie Processor est conçue pour être intuitive et efficace. 
        Elle se compose de deux panneaux principaux permettant une gestion 
        optimale du workflow de traitement des devis.
    """, normal_style))
    
    story.append(Paragraph("3.1 Panneau de configuration (Gauche)", section_style))
    
    story.append(Paragraph("""
        <b>Section Fichiers :</b>
    """, normal_style))
    
    file_section = [
        "Sélection PDF : Bouton pour choisir un ou plusieurs fichiers",
        "Liste des fichiers : Affichage des fichiers sélectionnés",
        "Suppression : Bouton pour retirer un fichier de la liste"
    ]
    
    for item in file_section:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(Paragraph("""
        <b>Section LLM :</b>
    """, normal_style))
    
    llm_section = [
        "Enrichissement LLM : Case à cocher pour activer l'IA",
        "Provider : Menu déroulant Ollama/OpenRouter",
        "Clé API : Champ texte pour la clé OpenRouter",
        "Statut : Indicateur de connexion au LLM"
    ]
    
    for item in llm_section:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(Paragraph("""
        <b>Section Production :</b>
    """, normal_style))
    
    prod_section = [
        "Semaine : Champ numérique (1-53)",
        "Année : Champ numérique (2024+)",
        "Commande client : Champ texte libre"
    ]
    
    for item in prod_section:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(Paragraph("3.2 Panneau de résultats (Droite)", section_style))
    
    story.append(Paragraph("""
        L'interface de résultats est organisée en onglets pour une navigation claire :
    """, normal_style))
    
    tabs = [
        "Onglet Résumé : Vue d'ensemble du traitement avec statistiques",
        "Onglet Configurations : Tableau des matelas détectés avec actions",
        "Onglet Pré-import : Données structurées prêtes pour Excel",
        "Onglet JSON : Données brutes au format JSON pour debug"
    ]
    
    for tab in tabs:
        story.append(Paragraph(f"• {tab}", list_style))
    
    story.append(PageBreak())
    
    # 4. Traitement des devis PDF
    story.append(Paragraph("4. Traitement des devis PDF", subtitle_style))
    
    story.append(Paragraph("4.1 Types de fichiers supportés", section_style))
    
    story.append(Paragraph("""
        Literie Processor prend en charge les formats suivants :
    """, normal_style))
    
    file_types = [
        "PDF de devis : Format PDF standard avec spécifications",
        "Taille maximale : 50 MB par fichier",
        "Encodage : UTF-8 recommandé",
        "Contenu : Devis de matelas avec dimensions et caractéristiques"
    ]
    
    for file_type in file_types:
        story.append(Paragraph(f"• {file_type}", list_style))
    
    story.append(Paragraph("4.2 Processus de traitement", section_style))
    
    story.append(Paragraph("""
        Le traitement suit un processus automatisé en plusieurs étapes :
    """, normal_style))
    
    process_steps = [
        "1. Validation des fichiers PDF sélectionnés",
        "2. Extraction du texte et analyse du contenu",
        "3. Enrichissement avec l'IA (si activé)",
        "4. Détection automatique des configurations matelas",
        "5. Calcul des dimensions et caractéristiques",
        "6. Génération des données structurées",
        "7. Préparation de l'export Excel"
    ]
    
    for step in process_steps:
        story.append(Paragraph(step, list_style))
    
    story.append(Paragraph("4.3 Intelligence artificielle", section_style))
    
    story.append(Paragraph("""
        L'IA améliore significativement la précision de l'extraction :
    """, normal_style))
    
    ai_benefits = [
        "Reconnaissance intelligente des types de matelas",
        "Extraction précise des dimensions et caractéristiques",
        "Détection automatique des housses et fermetés",
        "Gestion des cas particuliers et exceptions",
        "Amélioration continue de la précision"
    ]
    
    for benefit in ai_benefits:
        story.append(Paragraph(f"• {benefit}", list_style))
    
    story.append(PageBreak())
    
    # 5. Fonctionnalités principales
    story.append(Paragraph("5. Fonctionnalités principales", subtitle_style))
    
    story.append(Paragraph("5.1 Noyaux de traitement spécialisés", section_style))
    
    story.append(Paragraph("""
        <b>Literie Processor utilise des noyaux spécialisés pour chaque type de matelas :</b>
    """, normal_style))
    
    story.append(Paragraph("""
        <b>1. Latex Naturel (LN) :</b>
    """, normal_style))
    
    ln_features = [
        "Calcul automatique des longueurs de housse selon la matière",
        "Support des matières : LUXE 3D, TENCEL, POLYESTER",
        "Référentiel JSON avec correspondances longueur/matière",
        "Gestion des housses simples et matelassées",
        "Validation des dimensions et formats"
    ]
    
    for feature in ln_features:
        story.append(Paragraph(f"• {feature}", list_style))
    
    story.append(Paragraph("""
        <b>2. Latex Mixte 7 Zones (LM7z) :</b>
    """, normal_style))
    
    lm7z_features = [
        "Calcul des longueurs de housse pour latex mixte",
        "Support des 7 zones de confort",
        "Gestion des matières housse : LUXE 3D, TENCEL, POLYESTER",
        "Référentiel spécialisé 7 zones",
        "Validation des formats de housse"
    ]
    
    for feature in lm7z_features:
        story.append(Paragraph(f"• {feature}", list_style))
    
    story.append(Paragraph("""
        <b>3. Latex Mixte 3 Zones (LM3z) :</b>
    """, normal_style))
    
    lm3z_features = [
        "Calcul des longueurs de housse pour latex mixte 3 zones",
        "Support des 3 zones de confort",
        "Gestion des matières housse standard",
        "Référentiel spécialisé 3 zones",
        "Validation des formats de housse"
    ]
    
    for feature in lm3z_features:
        story.append(Paragraph(f"• {feature}", list_style))
    
    story.append(Paragraph("""
        <b>4. Mousse Viscoélastique (MV) :</b>
    """, normal_style))
    
    mv_features = [
        "Calcul automatique selon la largeur du matelas",
        "Support exclusif de la matière TENCEL",
        "Arrondi automatique de la largeur pour correspondance",
        "Préfixes automatiques : 2x (1 pièce), 4x (jumeaux)",
        "Référentiel spécialisé viscoélastique"
    ]
    
    for feature in mv_features:
        story.append(Paragraph(f"• {feature}", list_style))
    
    story.append(Paragraph("""
        <b>5. Mousse Rainurée 7 Zones (MR) :</b>
    """, normal_style))
    
    mr_features = [
        "Calcul des longueurs de housse pour mousse rainurée",
        "Support des 7 zones de confort",
        "Gestion des matières housse : LUXE 3D, TENCEL, POLYESTER",
        "Référentiel spécialisé rainuré 7 zones",
        "Validation des formats de housse"
    ]
    
    for feature in mr_features:
        story.append(Paragraph(f"• {feature}", list_style))
    
    story.append(Paragraph("""
        <b>6. Select 43 (SL43) :</b>
    """, normal_style))
    
    sl43_features = [
        "Calcul selon la largeur et matière housse",
        "Support des matières : LUXE 3D, TENCEL, POLYESTER",
        "Préfixes automatiques selon matière et quantité",
        "POLYESTER : pas de préfixe",
        "TENCEL/LUXE 3D : 2x (1 pièce), 4x (jumeaux)",
        "Référentiel spécialisé Select 43"
    ]
    
    for feature in sl43_features:
        story.append(Paragraph(f"• {feature}", list_style))
    
    story.append(Paragraph("5.2 Prompt LLM - Intelligence Artificielle", section_style))
    
    story.append(Paragraph("""
        <b>Le prompt LLM est le cœur intelligent de Literie Processor :</b>
    """, normal_style))
    
    story.append(Paragraph("""
        <b>Objectif principal :</b> Analyser le texte brut d'un devis et extraire 
        automatiquement toutes les informations pertinentes pour la production.
    """, normal_style))
    
    story.append(Paragraph("""
        <b>Instructions détaillées du prompt :</b>
    """, normal_style))
    
    prompt_instructions = [
        "0. Identification des dimensions du projet (format XXX/XXX)",
        "1. Extraction des matelas : description complète + quantité",
        "2. Extraction des housses : description complète + quantité",
        "3. Extraction des pieds : description complète + quantité",
        "4. Extraction des sommiers : description complète + quantité",
        "5. Extraction des informations client (nom, adresse, etc.)",
        "6. Regroupement des autres articles dans 'Autres'",
        "7. Détection des articles DOSSERET/TETE",
        "8. Identification jumeaux/1 pièce",
        "9. Transformation des dimensions (XX/XXX → XX x XXX)",
        "10. Gestion des modes de mise à disposition",
        "11. Exclusion des prix, montants, remises, délais"
    ]
    
    for instruction in prompt_instructions:
        story.append(Paragraph(f"• {instruction}", list_style))
    
    story.append(Paragraph("""
        <b>Format de sortie JSON structuré :</b>
    """, normal_style))
    
    json_structure = [
        "Matelas : description, quantité, jumeau/1 pièce, dosseret/tête, dimension_housse",
        "Housse : description, quantité",
        "Pieds : description, quantité",
        "Sommier : description, quantité",
        "Autres : description, quantité",
        "Client : nom, adresse, dimension projet"
    ]
    
    for structure in json_structure:
        story.append(Paragraph(f"• {structure}", list_style))
    
    story.append(Paragraph("""
        <b>Règles spéciales de traitement :</b>
    """, normal_style))
    
    special_rules = [
        "Gestion des quantités dans colonnes séparées",
        "Détection des formats de dimensions variés",
        "Préservation des lignes de livraison/enlèvement",
        "Exclusion des mentions administratives",
        "Validation des formats de sortie JSON"
    ]
    
    for rule in special_rules:
        story.append(Paragraph(f"• {rule}", list_style))
    
    story.append(Paragraph("5.3 Extraction automatique", section_style))
    
    extraction_features = [
        "Lecture automatique des devis PDF",
        "Extraction du texte avec préservation de la structure",
        "Reconnaissance des tableaux et listes",
        "Gestion des formats de devis variés",
        "Support multilingue (français principal)"
    ]
    
    for feature in extraction_features:
        story.append(Paragraph(f"• {feature}", list_style))
    
    story.append(Paragraph("5.2 Calculs automatiques", section_style))
    
    calc_features = [
        "Calcul automatique des dimensions housse",
        "Détermination de la fermeté selon le type",
        "Gestion des poignées et accessoires",
        "Calcul des quantités et configurations",
        "Validation des données extraites"
    ]
    
    for feature in calc_features:
        story.append(Paragraph(f"• {feature}", list_style))
    
    story.append(Paragraph("5.3 Gestion des clients", section_style))
    
    client_features = [
        "Extraction automatique des informations client",
        "Gestion des adresses et coordonnées",
        "Suivi des commandes par client",
        "Historique des traitements",
        "Export personnalisé par client"
    ]
    
    for feature in client_features:
        story.append(Paragraph(f"• {feature}", list_style))
    
    story.append(Paragraph("5.4 Pré-import Excel", section_style))
    
    excel_features = [
        "Formatage automatique pour import Excel",
        "Mapping des champs selon vos besoins",
        "Validation des données avant export",
        "Génération de fichiers prêts pour production",
        "Support des templates personnalisés"
    ]
    
    for feature in excel_features:
        story.append(Paragraph(f"• {feature}", list_style))
    
    story.append(PageBreak())
    
    # 6. Export et résultats
    story.append(Paragraph("6. Export et résultats", subtitle_style))
    
    story.append(Paragraph("6.1 Formats d'export", section_style))
    
    export_formats = [
        "Excel (.xlsx) : Format principal pour la production",
        "JSON : Données brutes pour intégration",
        "CSV : Format simple pour analyse",
        "PDF : Rapport de traitement"
    ]
    
    for format_type in export_formats:
        story.append(Paragraph(f"• {format_type}", list_style))
    
    story.append(Paragraph("6.2 Structure des fichiers Excel", section_style))
    
    story.append(Paragraph("""
        Les fichiers Excel générés contiennent :
    """, normal_style))
    
    excel_structure = [
        "Onglet Configurations : Toutes les matelas détectés",
        "Onglet Clients : Informations clients extraites",
        "Onglet Pré-import : Données formatées pour import",
        "Métadonnées : Informations de traitement et version"
    ]
    
    for item in excel_structure:
        story.append(Paragraph(f"• {item}", list_style))
    
    story.append(Paragraph("6.3 Inscription Excel détaillée", section_style))
    
    story.append(Paragraph("""
        <b>Structure des blocs de colonnes :</b>
    """, normal_style))
    
    story.append(Paragraph("""
        Chaque fichier Excel contient 10 cas de matelas répartis en blocs de colonnes :
    """, normal_style))
    
    blocks_info = [
        "Cas 1 : Colonnes C-D",
        "Cas 2 : Colonnes E-F", 
        "Cas 3 : Colonnes G-H",
        "Cas 4 : Colonnes I-J",
        "Cas 5 : Colonnes K-L",
        "Cas 6 : Colonnes O-P (M-N verrouillées)",
        "Cas 7 : Colonnes Q-R",
        "Cas 8 : Colonnes S-T",
        "Cas 9 : Colonnes U-V",
        "Cas 10 : Colonnes W-X"
    ]
    
    for block in blocks_info:
        story.append(Paragraph(f"• {block}", list_style))
    
    story.append(Paragraph("""
        <b>Champs disponibles pour les matelas :</b>
    """, normal_style))
    
    story.append(Paragraph("""
        <b>Informations client et commande :</b>
    """, normal_style))
    
    client_fields = [
        "Client_D1 : Nom du client (D1)",
        "Adresse_D3 : Adresse du client (D3)",
        "numero_D2 : Numéro de commande (D2)",
        "semaine_D5 : Semaine de production (D5)",
        "lundi_D6 : Date du lundi (D6)",
        "vendredi_D7 : Date du vendredi (D7)"
    ]
    
    for field in client_fields:
        story.append(Paragraph(f"• {field}", list_style))
    
    story.append(Paragraph("""
        <b>Dimensions et mesures :</b>
    """, normal_style))
    
    dimension_fields = [
        "Hauteur_D22 : Hauteur du matelas (D22)",
        "dimension_housse_D23 : Dimensions de la housse (D23)",
        "longueur_D24 : Longueur du matelas (D24)",
        "decoupe_noyau_D25 : Découpe du noyau (D25)"
    ]
    
    for field in dimension_fields:
        story.append(Paragraph(f"• {field}", list_style))
    
    story.append(Paragraph("""
        <b>Quantités et détection :</b>
    """, normal_style))
    
    quantity_fields = [
        "jumeaux_C10/D10 : Indication jumeaux (C10/D10)",
        "1piece_C11/D11 : Quantité 1 pièce (C11/D11)",
        "dosseret_tete_C8 : Détection dosseret/tête (C8)"
    ]
    
    for field in quantity_fields:
        story.append(Paragraph(f"• {field}", list_style))
    
    story.append(Paragraph("""
        <b>Housse et matière :</b>
    """, normal_style))
    
    housse_fields = [
        "HSimple_polyester_C13/D13 : Housse simple polyester (C13/D13)",
        "HSimple_tencel_C14/D14 : Housse simple tencel (C14/D14)",
        "HSimple_autre_C15/D15 : Housse simple autre (C15/D15)",
        "Hmat_polyester_C17/D17 : Housse matelassée polyester (C17/D17)",
        "Hmat_tencel_C18/D18 : Housse matelassée tencel (C18/D18)",
        "Hmat_luxe3D_C19/D19 : Housse matelassée luxe 3D (C19/D19)",
        "poignees_C20 : Poignées (C20)"
    ]
    
    for field in housse_fields:
        story.append(Paragraph(f"• {field}", list_style))
    
    story.append(Paragraph("""
        <b>Types de noyau et fermeté :</b>
    """, normal_style))
    
    noyau_fields = [
        "LN_Ferme_C28 : Latex Naturel Ferme (C28)",
        "LN_Medium_C29 : Latex Naturel Medium (C29)",
        "LM7z_Ferme_C30 : Latex Mixte 7 Zones Ferme (C30)",
        "LM7z_Medium_C31 : Latex Mixte 7 Zones Medium (C31)",
        "LM3z_Ferme_C32 : Latex Mixte 3 Zones Ferme (C32)",
        "LM3z_Medium_C33 : Latex Mixte 3 Zones Medium (C33)",
        "MV_Ferme_C34 : Mousse Viscoélastique Ferme (C34)",
        "MV_Medium_C35 : Mousse Viscoélastique Medium (C35)",
        "MV_Confort_C36 : Mousse Viscoélastique Confort (C36)",
        "MR_Ferme_C37 : Mousse Rainurée Ferme (C37)",
        "MR_Medium_C38 : Mousse Rainurée Medium (C38)",
        "MR_Confort_C39 : Mousse Rainurée Confort (C39)",
        "SL43_Ferme_C40 : Select 43 Ferme (C40)",
        "SL43_Medium_C41 : Select 43 Medium (C41)"
    ]
    
    for field in noyau_fields:
        story.append(Paragraph(f"• {field}", list_style))
    
    story.append(Paragraph("""
        <b>Options supplémentaires :</b>
    """, normal_style))
    
    options_fields = [
        "Surmatelas_C45 : Surmatelas (C45)",
        "emporte_client_C57 : Emporté client (C57)",
        "fourgon_C58 : Fourgon (C58)",
        "transporteur_C59 : Transporteur (C59)"
    ]
    
    for field in options_fields:
        story.append(Paragraph(f"• {field}", list_style))
    
    story.append(Paragraph("""
        <b>Fonctionnalités d'inscription :</b>
    """, normal_style))
    
    inscription_features = [
        "Alignement automatique : Toutes les cellules sont centrées",
        "Coloration conditionnelle : Activation selon les valeurs",
        "Numérotation continue : Cas 1-10, 11-20, etc. entre fichiers",
        "Validation des données : Vérification avant inscription",
        "Gestion des erreurs : Logs détaillés des opérations"
    ]
    
    for feature in inscription_features:
        story.append(Paragraph(f"• {feature}", list_style))
    
    story.append(Paragraph("6.4 Validation des résultats", section_style))
    
    validation_steps = [
        "Vérification automatique des données extraites",
        "Contrôle de cohérence des dimensions",
        "Validation des types de matelas",
        "Détection des anomalies et erreurs",
        "Rapport de qualité du traitement"
    ]
    
    for step in validation_steps:
        story.append(Paragraph(f"• {step}", list_style))
    
    story.append(PageBreak())
    
    # 7. Dépannage et support
    story.append(Paragraph("7. Dépannage et support", subtitle_style))
    
    story.append(Paragraph("7.1 Problèmes courants", section_style))
    
    common_issues = [
        "Erreur 'Module not found' : Réinstaller les dépendances",
        "Fichier PDF non lu : Vérifier le format et la taille",
        "LLM non connecté : Vérifier la clé API et la connexion",
        "Export échoué : Vérifier les permissions d'écriture",
        "Interface lente : Fermer les autres applications"
    ]
    
    for issue in common_issues:
        story.append(Paragraph(f"• {issue}", list_style))
    
    story.append(Paragraph("7.2 Logs et diagnostic", section_style))
    
    story.append(Paragraph("""
        L'application génère des logs détaillés pour le diagnostic :
    """, normal_style))
    
    log_files = [
        "matelas_app.log : Logs généraux de l'application",
        "matelas_errors.log : Erreurs détaillées",
        "admin_operations.log : Opérations d'administration"
    ]
    
    for log in log_files:
        story.append(Paragraph(f"• {log}", list_style))
    
    story.append(Paragraph("7.3 Support technique", section_style))
    
    support_info = [
        "Email : sebastien.confrere@scinnova.fr",
        "Téléphone : 06.66.05.72.47",
        "Éditeur : SCINNOVA",
        "Horaires : Lundi-Vendredi 9h-17h",
        "Réponse garantie : Sous 24h ouvrées"
    ]
    
    for info in support_info:
        story.append(Paragraph(f"• {info}", list_style))
    
    story.append(PageBreak())
    
    # 8. Annexes techniques
    story.append(Paragraph("8. Annexes techniques", subtitle_style))
    
    story.append(Paragraph("8.1 Configuration avancée", section_style))
    
    story.append(Paragraph("""
        Pour les utilisateurs avancés, l'application permet de :
    """, normal_style))
    
    advanced_config = [
        "Personnaliser les mappings Excel",
        "Configurer les providers LLM",
        "Ajuster les paramètres de traitement",
        "Créer des templates personnalisés",
        "Automatiser les exports"
    ]
    
    for config in advanced_config:
        story.append(Paragraph(f"• {config}", list_style))
    
    story.append(Paragraph("8.2 Sécurité", section_style))
    
    security_features = [
        "Stockage sécurisé des clés API",
        "Chiffrement des données sensibles",
        "Validation des entrées utilisateur",
        "Logs d'audit pour la traçabilité",
        "Conformité RGPD"
    ]
    
    for feature in security_features:
        story.append(Paragraph(f"• {feature}", list_style))
    
    story.append(Paragraph("8.3 Performance", section_style))
    
    performance_info = [
        "Traitement de 10-50 devis par heure",
        "Optimisation mémoire pour gros volumes",
        "Cache intelligent pour les calculs",
        "Parallélisation des traitements",
        "Monitoring des performances"
    ]
    
    for info in performance_info:
        story.append(Paragraph(f"• {info}", list_style))
    
    # Page de fin
    story.append(PageBreak())
    
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("Documentation Literie Processor", title_style))
    story.append(Paragraph("Développé par SCINNOVA", subtitle_style))
    story.append(Paragraph("Pour SAS Literie Westelynck", subtitle_style))
    story.append(Paragraph("Merci de votre confiance", normal_style))
    
    # Génération du PDF
    doc.build(story)
    print("✅ Documentation PDF générée avec succès : Documentation_MatelasApp_Westelynck.pdf")

if __name__ == "__main__":
    try:
        create_professional_documentation()
    except Exception as e:
        print(f"❌ Erreur lors de la génération du PDF : {e}")
        sys.exit(1) 