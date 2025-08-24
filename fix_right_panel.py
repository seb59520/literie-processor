#!/usr/bin/env python3
"""Fix pour le panneau de droite"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Test de la structure de create_right_panel
def test_right_panel_structure():
    """Teste la structure logique du panneau droit"""
    print("🔍 Analyse de create_right_panel...")
    
    with open('/Users/sebastien/MATELAS_FINAL/app_gui.py', 'r') as f:
        content = f.read()
    
    # Trouver la fonction create_right_panel
    lines = content.split('\n')
    in_function = False
    function_lines = []
    indent_level = 0
    
    for i, line in enumerate(lines):
        if 'def create_right_panel(self):' in line:
            in_function = True
            indent_level = len(line) - len(line.lstrip())
            print(f"✅ Fonction trouvée ligne {i+1}")
            function_lines.append((i+1, line))
            continue
            
        if in_function:
            current_indent = len(line) - len(line.lstrip()) if line.strip() else 0
            
            # Si on revient au niveau d'indentation de base et qu'on trouve une def, on sort
            if (line.strip().startswith('def ') and current_indent <= indent_level):
                print(f"✅ Fin de fonction ligne {i+1}")
                break
                
            function_lines.append((i+1, line))
    
    # Analyser les return statements
    return_count = 0
    for line_num, line in function_lines:
        if 'return' in line and 'right_widget' in line:
            return_count += 1
            print(f"📍 Return trouvé ligne {line_num}: {line.strip()}")
    
    print(f"📊 Total returns trouvés: {return_count}")
    
    # Vérifier les variables non définies
    right_widget_defined = False
    for line_num, line in function_lines:
        if 'right_widget = QWidget()' in line:
            right_widget_defined = True
            print(f"✅ right_widget définie ligne {line_num}")
            break
    
    if not right_widget_defined:
        print("❌ right_widget n'est pas définie!")
        
    print("✅ Analyse terminée")

if __name__ == "__main__":
    test_right_panel_structure()