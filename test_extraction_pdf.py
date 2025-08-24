#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour l'extraction de texte PDF
"""

import sys
import os
import tempfile
import subprocess

def test_pdf_libraries():
    """Tester les bibliothèques PDF disponibles"""
    print("🔍 Test des bibliothèques PDF disponibles")
    print("=" * 50)
    
    libraries = {
        "PyMuPDF (fitz)": "import fitz",
        "PyPDF2": "import PyPDF2",
        "pdfplumber": "import pdfplumber"
    }
    
    available_libs = []
    
    for lib_name, import_cmd in libraries.items():
        try:
            exec(import_cmd)
            print(f"✅ {lib_name} - Disponible")
            available_libs.append(lib_name)
        except ImportError:
            print(f"❌ {lib_name} - Non disponible")
    
    return available_libs

def create_test_pdf():
    """Créer un PDF de test simple"""
    print("\n📄 Création d'un PDF de test")
    print("=" * 50)
    
    try:
        # Essayer d'utiliser reportlab pour créer un PDF
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        # Créer un fichier temporaire
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            pdf_path = tmp_file.name
        
        # Créer le PDF
        c = canvas.Canvas(pdf_path, pagesize=letter)
        
        # Ajouter du texte
        c.drawString(100, 750, "DEVIS LITERIE WESTELYNCK")
        c.drawString(100, 730, "SAS Literie Westelynck")
        c.drawString(100, 710, "525 RD 642 - 59190 BORRE")
        c.drawString(100, 690, "Tél : 03.28.48.04.19")
        c.drawString(100, 670, "Email : contact@lwest.fr")
        
        c.drawString(100, 620, "CLIENT :")
        c.drawString(100, 600, "Mr et Me DUPONT JEAN")
        c.drawString(100, 580, "15 AVENUE DE LA PAIX, 59000 LILLE")
        c.drawString(100, 560, "Code client : DUPOJEALIL")
        
        c.drawString(100, 520, "COMMANDE N° CM123456")
        c.drawString(100, 500, "Date : 22/07/2025")
        c.drawString(100, 480, "Commercial : P. ALINE")
        
        c.drawString(100, 440, "LITERIE 140/190/59 CM DOUBLE SUR PIEDS")
        
        c.drawString(100, 400, "1. SOMMIER DOUBLE RELAXATION MOTORISÉE")
        c.drawString(100, 380, "   Quantité : 1")
        
        c.drawString(100, 340, "2. MATELAS DOUBLE - MOUSSE VISCOÉLASTIQUE")
        c.drawString(100, 320, "   Quantité : 1")
        
        c.drawString(100, 280, "CONDITIONS DE PAIEMENT :")
        c.drawString(100, 260, "ACOMPTE DE 500 € EN CB LA COMMANDE")
        
        c.drawString(100, 220, "BASE HT : 2500,00€")
        c.drawString(100, 200, "TVA 20% : 500,00€")
        c.drawString(100, 180, "TOTAL TTC : 3000,00€")
        
        c.save()
        
        print(f"✅ PDF de test créé: {pdf_path}")
        return pdf_path
        
    except ImportError:
        print("❌ ReportLab non disponible, impossible de créer un PDF de test")
        return None
    except Exception as e:
        print(f"❌ Erreur lors de la création du PDF: {e}")
        return None

def test_pymupdf_extraction(pdf_path):
    """Tester l'extraction avec PyMuPDF"""
    print("\n🔧 Test d'extraction avec PyMuPDF")
    print("=" * 50)
    
    try:
        import fitz
        
        doc = fitz.open(pdf_path)
        text_parts = []
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            page_text = page.get_text()
            if page_text.strip():
                text_parts.append(f"--- PAGE {page_num + 1} ---\n{page_text}")
        
        doc.close()
        
        extracted_text = "\n\n".join(text_parts)
        
        if extracted_text.strip():
            print("✅ Extraction PyMuPDF réussie")
            print(f"📝 Texte extrait ({len(extracted_text)} caractères):")
            print("-" * 30)
            print(extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text)
            return extracted_text
        else:
            print("❌ Aucun texte extrait avec PyMuPDF")
            return None
            
    except ImportError:
        print("❌ PyMuPDF non disponible")
        return None
    except Exception as e:
        print(f"❌ Erreur PyMuPDF: {e}")
        return None

def test_pypdf2_extraction(pdf_path):
    """Tester l'extraction avec PyPDF2"""
    print("\n🔧 Test d'extraction avec PyPDF2")
    print("=" * 50)
    
    try:
        import PyPDF2
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text_parts = []
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                if page_text.strip():
                    text_parts.append(f"--- PAGE {page_num + 1} ---\n{page_text}")
            
            extracted_text = "\n\n".join(text_parts)
            
            if extracted_text.strip():
                print("✅ Extraction PyPDF2 réussie")
                print(f"📝 Texte extrait ({len(extracted_text)} caractères):")
                print("-" * 30)
                print(extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text)
                return extracted_text
            else:
                print("❌ Aucun texte extrait avec PyPDF2")
                return None
                
    except ImportError:
        print("❌ PyPDF2 non disponible")
        return None
    except Exception as e:
        print(f"❌ Erreur PyPDF2: {e}")
        return None

def clean_extracted_text(text):
    """Nettoyer le texte extrait"""
    if not text:
        return text
    
    import re
    
    # Remplacer les sauts de ligne multiples par des sauts simples
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    
    # Supprimer les espaces en début et fin de ligne
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        cleaned_line = line.strip()
        if cleaned_line and not re.match(r'^[\s\-_=*#]+$', cleaned_line):
            cleaned_lines.append(cleaned_line)
    
    cleaned_text = '\n'.join(cleaned_lines)
    return cleaned_text.strip()

def test_text_cleaning(extracted_text):
    """Tester le nettoyage du texte"""
    print("\n🧹 Test de nettoyage du texte")
    print("=" * 50)
    
    if not extracted_text:
        print("❌ Aucun texte à nettoyer")
        return None
    
    cleaned_text = clean_extracted_text(extracted_text)
    
    print(f"📊 Avant nettoyage: {len(extracted_text)} caractères")
    print(f"📊 Après nettoyage: {len(cleaned_text)} caractères")
    
    if cleaned_text != extracted_text:
        print("✅ Texte nettoyé avec succès")
        print("📝 Texte nettoyé:")
        print("-" * 30)
        print(cleaned_text[:500] + "..." if len(cleaned_text) > 500 else cleaned_text)
    else:
        print("ℹ️ Aucun nettoyage nécessaire")
    
    return cleaned_text

def main():
    """Fonction principale"""
    print("📄 Test d'extraction de texte PDF")
    print("=" * 60)
    
    try:
        # 1. Tester les bibliothèques disponibles
        available_libs = test_pdf_libraries()
        
        if not available_libs:
            print("\n❌ Aucune bibliothèque PDF disponible")
            print("💡 Installez une bibliothèque avec:")
            print("   pip install PyMuPDF")
            print("   pip install PyPDF2")
            return False
        
        # 2. Créer un PDF de test
        pdf_path = create_test_pdf()
        if not pdf_path:
            print("\n❌ Impossible de créer un PDF de test")
            return False
        
        # 3. Tester l'extraction avec les bibliothèques disponibles
        extracted_text = None
        
        if "PyMuPDF (fitz)" in available_libs:
            extracted_text = test_pymupdf_extraction(pdf_path)
        
        if not extracted_text and "PyPDF2" in available_libs:
            extracted_text = test_pypdf2_extraction(pdf_path)
        
        if not extracted_text:
            print("\n❌ Aucune extraction réussie")
            return False
        
        # 4. Tester le nettoyage du texte
        cleaned_text = test_text_cleaning(extracted_text)
        
        # 5. Nettoyer le fichier temporaire
        try:
            os.unlink(pdf_path)
            print(f"\n🗑️ Fichier temporaire supprimé: {pdf_path}")
        except:
            pass
        
        # 6. Résumé
        print("\n🎉 Test terminé avec succès !")
        print("=" * 60)
        print("✅ Extraction PDF fonctionnelle")
        print("✅ Nettoyage de texte opérationnel")
        print("✅ Prêt pour l'utilisation dans l'application")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 