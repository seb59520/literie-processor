#!/usr/bin/env python3
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

def create_test_pdf():
    """Crée un PDF de test avec des données de devis"""
    
    # Créer le document
    doc = SimpleDocTemplate("test_devis.pdf", pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Titre
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Centré
    )
    story.append(Paragraph("DEVIS LITERIE", title_style))
    story.append(Spacer(1, 20))
    
    # Informations client
    client_data = [
        ['Client:', 'Mr et Me YVOZ DAVID ET MARIE-PIERRE'],
        ['Adresse:', '1780 CHEMIN DE ZERMEZEELE, 59470 WORMHOUT'],
        ['Date:', '15/12/2024']
    ]
    
    client_table = Table(client_data, colWidths=[1.5*inch, 4*inch])
    client_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(client_table)
    story.append(Spacer(1, 20))
    
    # Articles
    articles_data = [
        ['Référence', 'Description', 'Quantité', 'Prix unitaire', 'Total'],
        ['', 'MATELAS LATEX 100% NATUREL - TENCEL LUXE 3D MATELASSEE 139/189', '1', '698,50 €', '698,50 €'],
        ['', 'HOUSSE TENCEL LUXE 3D MATELASSEE AVEC POIGNEES 139/189', '1', '245,00 €', '245,00 €'],
        ['', 'Livraison à domicile', '1', '45,00 €', '45,00 €'],
    ]
    
    articles_table = Table(articles_data, colWidths=[0.8*inch, 3.5*inch, 0.8*inch, 1.2*inch, 1.2*inch])
    articles_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(articles_table)
    story.append(Spacer(1, 20))
    
    # Total
    total_data = [
        ['Total HT:', '988,50 €'],
        ['TVA (20%):', '197,70 €'],
        ['Total TTC:', '1186,20 €']
    ]
    
    total_table = Table(total_data, colWidths=[1.5*inch, 1.5*inch])
    total_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(total_table)
    
    # Construire le PDF
    doc.build(story)
    print("✅ PDF de test créé : test_devis.pdf")

if __name__ == "__main__":
    create_test_pdf() 