#!/usr/bin/env python3
"""Test pour diagnostiquer l'affichage des boutons"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

class TestPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        print("🔄 Test création panneau avec boutons...")
        
        # Widget central
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Titre
        title = QLabel("Test Panneau")
        layout.addWidget(title)
        print("✅ Titre ajouté")
        
        # Boutons (comme dans app_gui.py)
        try:
            buttons_layout = QHBoxLayout()
            
            btn1 = QPushButton("📁 Bouton 1")
            btn1.clicked.connect(lambda: print("Bouton 1 cliqué"))
            buttons_layout.addWidget(btn1)
            print("✅ Bouton 1 créé")
            
            btn2 = QPushButton("📊 Bouton 2") 
            btn2.clicked.connect(lambda: print("Bouton 2 cliqué"))
            buttons_layout.addWidget(btn2)
            print("✅ Bouton 2 créé")
            
            btn3 = QPushButton("💾 Bouton 3")
            btn3.clicked.connect(lambda: print("Bouton 3 cliqué"))
            buttons_layout.addWidget(btn3)
            print("✅ Bouton 3 créé")
            
            layout.addLayout(buttons_layout)
            print("✅ Layout boutons ajouté")
            
        except Exception as e:
            print(f"❌ Erreur création boutons: {e}")
            import traceback
            traceback.print_exc()
        
        self.setWindowTitle("Test Boutons")
        self.resize(600, 400)
        print("✅ Test panel créé")

def main():
    app = QApplication(sys.argv)
    window = TestPanel()
    window.show()
    
    print("🎯 Fenêtre affichée - vérifiez si les boutons sont visibles")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()