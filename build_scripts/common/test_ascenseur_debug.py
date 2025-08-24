#!/usr/bin/env python3
"""
Script de test pour diagnostiquer le problème de l'ascenseur
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QScrollArea, QGroupBox
from PyQt6.QtCore import Qt

def test_ascenseur_simple():
    """Test simple de l'ascenseur pour diagnostiquer le problème"""
    print("🧪 Test de diagnostic de l'ascenseur")
    
    app = QApplication(sys.argv)
    
    # Créer une fenêtre de test
    window = QMainWindow()
    window.setWindowTitle("Test Ascenseur")
    window.setGeometry(100, 100, 400, 300)
    
    # Widget central
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    
    # Layout principal
    main_layout = QVBoxLayout(central_widget)
    
    # Groupe de test
    group = QGroupBox("Test Ascenseur")
    group_layout = QVBoxLayout(group)
    
    # Créer un widget scrollable
    scroll_widget = QWidget()
    scroll_layout = QVBoxLayout(scroll_widget)
    scroll_layout.setSpacing(5)
    
    # Créer plusieurs champs pour forcer l'ascenseur
    for i in range(10):
        hbox = QHBoxLayout()
        label = QLabel(f"Champ {i+1}:")
        lineedit = QLineEdit()
        lineedit.setPlaceholderText(f"Valeur {i+1}")
        hbox.addWidget(label)
        hbox.addWidget(lineedit)
        scroll_layout.addLayout(hbox)
    
    # Créer le QScrollArea
    scroll_area = QScrollArea()
    scroll_area.setWidget(scroll_widget)
    scroll_area.setWidgetResizable(True)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    
    # Limiter la hauteur pour forcer l'ascenseur
    max_height = 3 * 40  # 3 lignes * 40px
    scroll_area.setMaximumHeight(max_height)
    scroll_area.setMinimumHeight(120)
    
    # Ajouter au layout
    group_layout.addWidget(scroll_area)
    main_layout.addWidget(group)
    
    # Afficher la fenêtre
    window.show()
    
    print("✅ Fenêtre de test créée")
    print("📋 Instructions de test :")
    print("   1. Vous devriez voir 10 champs de saisie")
    print("   2. Seuls 3 champs devraient être visibles")
    print("   3. Un ascenseur vertical devrait apparaître")
    print("   4. Vous devriez pouvoir faire défiler pour voir les autres champs")
    print("")
    print("🎯 Test en cours...")
    print("   - Vérifiez que l'ascenseur apparaît")
    print("   - Testez le défilement")
    print("   - Vérifiez que tous les champs sont accessibles")
    
    # Lancer l'application
    sys.exit(app.exec())

if __name__ == "__main__":
    test_ascenseur_simple() 