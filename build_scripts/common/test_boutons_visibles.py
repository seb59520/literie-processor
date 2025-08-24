#!/usr/bin/env python3
"""
Script de test pour vérifier que les boutons "X" et "?" sont bien visibles en blanc
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Import de l'application principale
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_boutons_visibles():
    """Test de la visibilité des boutons X et ?"""
    print("🧪 Test de la visibilité des boutons X et ?")
    
    app = QApplication(sys.argv)
    
    try:
        # Importer et créer l'application principale
        from app_gui import MatelasApp
        
        # Créer l'application
        main_app = MatelasApp()
        main_app.show()
        
        print("✅ Application lancée avec succès")
        print("📋 Instructions de test :")
        print("   1. Le bouton 'X' rouge doit être visible en haut à droite")
        print("   2. Le bouton '?' bleu doit être visible dans le groupe 'Enrichissement LLM'")
        print("   3. Les deux boutons doivent avoir un texte blanc bien visible")
        print("   4. Les boutons doivent être circulaires avec une bordure")
        print("   5. Les effets hover doivent fonctionner")
        
        # Timer pour afficher les informations après 2 secondes
        def afficher_info():
            try:
                # Informations sur le bouton X
                if hasattr(main_app, 'close_button'):
                    close_btn = main_app.close_button
                    print(f"\n🔴 Bouton X (fermeture) :")
                    print(f"   Position : {close_btn.pos()}")
                    print(f"   Taille : {close_btn.size()}")
                    print(f"   Style : {close_btn.styleSheet()[:100]}...")
                    print(f"   Texte : '{close_btn.text()}'")
                    print(f"   Couleur de fond : #e74c3c (rouge)")
                    print(f"   Couleur de texte : white")
                
                # Informations sur le bouton ?
                # Chercher le bouton d'aide dans le groupe Enrichissement LLM
                for child in main_app.findChildren(type(main_app)):
                    if hasattr(child, 'text') and child.text() == "?":
                        print(f"\n🔵 Bouton ? (aide) :")
                        print(f"   Position : {child.pos()}")
                        print(f"   Taille : {child.size()}")
                        print(f"   Style : {child.styleSheet()[:100]}...")
                        print(f"   Texte : '{child.text()}'")
                        print(f"   Couleur de fond : #3498db (bleu)")
                        print(f"   Couleur de texte : white")
                        break
                
                print(f"\n🎯 Test en cours...")
                print(f"   - Vérifiez que le 'X' rouge est visible en haut à droite")
                print(f"   - Vérifiez que le '?' bleu est visible dans 'Enrichissement LLM'")
                print(f"   - Les deux symboles doivent être blancs sur fond coloré")
                print(f"   - Testez les effets hover en passant la souris dessus")
                
            except Exception as e:
                print(f"❌ Erreur lors de l'affichage des informations : {e}")
        
        # Programmer l'affichage des informations après 2 secondes
        QTimer.singleShot(2000, afficher_info)
        
        # Lancer l'application
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement de l'application : {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_boutons_visibles() 