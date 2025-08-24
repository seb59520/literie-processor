#!/usr/bin/env python3
"""
Script de test simple pour vérifier l'extraction de texte PDF
"""

import fitz  # PyMuPDF
import os

def test_extraction():
    """Test simple d'extraction de texte"""
    
    # Vérifier si le fichier de test existe
    test_file = "test_devis.pdf"
    if not os.path.exists(test_file):
        print(f"❌ Fichier de test {test_file} non trouvé")
        return False
    
    try:
        print(f"📖 Ouverture du fichier {test_file}")
        doc = fitz.open(test_file)
        
        # Récupérer le nombre de pages avant de fermer
        nb_pages = len(doc)
        
        # Extraire le texte de toutes les pages
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        
        print(f"✅ Extraction réussie")
        print(f"📊 Statistiques:")
        print(f"   - Caractères: {len(text)}")
        print(f"   - Mots: {len(text.split())}")
        print(f"   - Pages: {nb_pages}")
        
        # Aperçu du texte
        preview = text[:200] + "..." if len(text) > 200 else text
        print(f"📝 Aperçu du texte extrait:")
        print(f"   {preview}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'extraction: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Test d'extraction de texte PDF")
    print("=" * 40)
    
    success = test_extraction()
    
    if success:
        print("\n✅ Test réussi ! L'extraction de texte fonctionne correctement.")
    else:
        print("\n❌ Test échoué ! Il y a un problème avec l'extraction de texte.") 