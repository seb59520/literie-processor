#!/usr/bin/env python3
"""
Script de test pour vérifier la correction de la barre de progression
et de l'alerte "Traitement terminé" lors de l'affichage de la popup de confirmation
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, QProgressBar
from PyQt6.QtCore import QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QFont

# Import de l'application principale
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestProcessingThread(QThread):
    """Thread de test pour simuler le traitement"""
    progress_updated = pyqtSignal(int)
    recommendations_ready = pyqtSignal(dict)
    
    def run(self):
        """Simule le traitement avec analyse préliminaire"""
        print("🧪 Début du test de traitement")
        
        # Simulation de l'analyse préliminaire
        for i in range(5, 31, 5):
            self.progress_updated.emit(i)
            import time
            time.sleep(0.2)
        
        print("📊 Analyse préliminaire terminée - envoi des recommandations")
        
        # Simuler les recommandations de production
        recommendations = {
            "test_file.pdf": {
                'has_matelas': True,
                'has_sommiers': False,
                'matelas_count': 2,
                'sommier_count': 0,
                'semaine_actuelle': 31,
                'annee_actuelle': 2025,
                'recommendation': "Seulement matelas détectés - production S+1",
                'semaine_matelas': 32,
                'annee_matelas': 2025,
                'semaine_sommiers': 32,
                'annee_sommiers': 2025
            }
        }
        
        # Envoyer les recommandations (ce qui déclenche la popup)
        self.recommendations_ready.emit(recommendations)
        
        print("✅ Recommandations envoyées - thread se termine")

def test_correction_progression_popup():
    """Test de la correction de la barre de progression"""
    print("🧪 Test de correction de la barre de progression")
    
    app = QApplication(sys.argv)
    
    try:
        # Importer et créer l'application principale
        from app_gui import MatelasApp
        
        # Créer l'application
        main_app = MatelasApp()
        main_app.show()
        
        print("✅ Application créée avec succès")
        
        # Vérifier que la barre de progression est initialement masquée
        progress_bar = main_app.progress_bar
        progress_status_label = main_app.progress_status_label
        
        print(f"   - Barre de progression visible: {progress_bar.isVisible()}")
        print(f"   - Label de statut visible: {progress_status_label.isVisible()}")
        
        # Simuler la sélection de fichiers
        main_app.selected_files = ["test_file.pdf"]
        
        # Créer et lancer le thread de test
        test_thread = TestProcessingThread()
        
        # Connecter les signaux
        test_thread.progress_updated.connect(main_app.on_progress_updated)
        test_thread.recommendations_ready.connect(main_app.show_production_recommendations)
        test_thread.finished.connect(lambda: print("✅ Thread de test terminé"))
        
        # Lancer le test
        print("🚀 Lancement du test de traitement...")
        test_thread.start()
        
        # Vérifier que la barre de progression devient visible
        def check_progress_visible():
            print(f"📊 Vérification barre de progression:")
            print(f"   - Visible: {progress_bar.isVisible()}")
            print(f"   - Valeur: {progress_bar.value()}%")
            print(f"   - Label visible: {progress_status_label.isVisible()}")
            print(f"   - Texte label: {progress_status_label.text()}")
            
            # Vérifier que la barre est visible pendant l'analyse
            if progress_bar.isVisible():
                print("✅ Barre de progression visible pendant l'analyse")
            else:
                print("❌ Barre de progression masquée pendant l'analyse")
        
        # Vérifier après 2 secondes
        QTimer.singleShot(2000, check_progress_visible)
        
        # Vérifier après 4 secondes (quand la popup devrait apparaître)
        def check_during_popup():
            print(f"📋 Vérification pendant la popup:")
            print(f"   - Barre visible: {progress_bar.isVisible()}")
            print(f"   - Valeur: {progress_bar.value()}%")
            
            # La barre devrait rester visible pendant la popup
            if progress_bar.isVisible():
                print("✅ Barre de progression reste visible pendant la popup")
            else:
                print("❌ Barre de progression masquée pendant la popup")
        
        QTimer.singleShot(4000, check_during_popup)
        
        # Fermer l'application après 15 secondes
        QTimer.singleShot(15000, app.quit)
        
        print("\n🎯 Test en cours...")
        print("   - La barre de progression devrait devenir visible")
        print("   - La popup de recommandations devrait apparaître")
        print("   - La barre de progression devrait rester visible pendant la popup")
        print("   - L'alerte 'Traitement terminé' ne devrait PAS apparaître prématurément")
        
        return app.exec()
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return 1

if __name__ == "__main__":
    test_correction_progression_popup() 