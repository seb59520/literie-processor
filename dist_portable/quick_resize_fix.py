#!/usr/bin/env python3
"""
Script pour forcer les propriétés de redimensionnement dans l'application
"""

import sys
import os
from pathlib import Path

def apply_resize_fix():
    """Applique le fix de redimensionnement au fichier app_gui.py"""
    
    app_file = Path("app_gui.py")
    if not app_file.exists():
        print("[ERREUR] Fichier app_gui.py non trouvé")
        return False
    
    # Lire le contenu du fichier
    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix pour forcer le redimensionnement
    resize_fix = '''
        # FORCE RESIZE FIX - Ajouté par quick_resize_fix.py
        try:
            # Désactiver les restrictions de taille fixes
            self.setMinimumSize(800, 600)  # Taille minimale raisonnable
            self.setMaximumSize(16777215, 16777215)  # Taille maximale Qt
            
            # Permettre redimensionnement libre
            from PyQt6.QtWidgets import QSizePolicy
            self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
            
            # Activer le redimensionnement manuel
            self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, True)
            self.setWindowFlag(Qt.WindowType.WindowMinimizeButtonHint, True)
            
            print("✅ Fix de redimensionnement appliqué")
        except Exception as e:
            print(f"⚠️ Erreur fix redimensionnement: {e}")
'''
    
    # Insérer le fix après setup_responsive_window()
    if "def setup_responsive_window(self):" in content and "# FORCE RESIZE FIX" not in content:
        
        # Trouver la fin de la fonction setup_responsive_window
        lines = content.split('\n')
        insert_position = None
        
        for i, line in enumerate(lines):
            if "def setup_responsive_window(self):" in line:
                # Chercher la fin de cette fonction
                indent_level = len(line) - len(line.lstrip())
                for j in range(i + 1, len(lines)):
                    current_line = lines[j]
                    if current_line.strip() == "":
                        continue
                    current_indent = len(current_line) - len(current_line.lstrip())
                    if current_indent <= indent_level and current_line.strip().startswith('def '):
                        insert_position = j - 1
                        break
                break
        
        if insert_position:
            # Insérer le fix
            lines.insert(insert_position, resize_fix)
            modified_content = '\n'.join(lines)
            
            # Sauvegarder
            with open(app_file, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            
            print("✅ Fix de redimensionnement appliqué au fichier app_gui.py")
            return True
    else:
        print("⚠️ Fix déjà appliqué ou fonction non trouvée")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("FIX DE REDIMENSIONNEMENT WINDOWS")  
    print("=" * 50)
    
    if apply_resize_fix():
        print("\n✅ Fix appliqué avec succès!")
        print("Relancez l'application, vous devriez pouvoir redimensionner la fenêtre.")
    else:
        print("\n⚠️ Fix non appliqué")
        
    print("\nSi le problème persiste:")
    print("1. Essayez Alt+Espace puis 'Restaurer' ou 'Agrandir'") 
    print("2. Redémarrez l'application")
    print("3. Vérifiez que vous n'êtes pas en mode 'fenêtré sans bordures'")