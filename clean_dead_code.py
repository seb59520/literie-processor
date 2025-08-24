#!/usr/bin/env python3
"""Script pour nettoyer le code mort dans app_gui.py"""

def clean_dead_code():
    """Supprime le code mort après la fonction create_right_panel"""
    
    with open('/Users/sebastien/MATELAS_FINAL/app_gui.py', 'r') as f:
        lines = f.readlines()
    
    # Trouver la fin réelle de create_right_panel
    in_function = False
    function_end = -1
    
    for i, line in enumerate(lines):
        if 'def create_right_panel(self):' in line:
            in_function = True
            continue
            
        if in_function and line.strip() == 'return right_widget':
            # Trouver la prochaine ligne non-commentaire/vide
            for j in range(i+1, len(lines)):
                next_line = lines[j].strip()
                if next_line and not next_line.startswith('#'):
                    if next_line.startswith('def ') or 'def filter_logs' in next_line:
                        function_end = j
                        break
                    elif next_line.startswith('# ') or next_line == '':
                        continue
                    else:
                        # Code mort trouvé
                        function_end = j
                        break
            break
    
    if function_end > 0:
        # Code mort entre fin de return et prochaine fonction
        dead_code_start = -1
        for i in range(function_end):
            if 'return right_widget' in lines[i]:
                dead_code_start = i + 1
                break
        
        if dead_code_start > 0:
            # Trouver la fin du code mort
            dead_code_end = function_end
            for i in range(dead_code_start, len(lines)):
                if 'def filter_logs' in lines[i]:
                    dead_code_end = i
                    break
            
            print(f"Code mort détecté lignes {dead_code_start+1} à {dead_code_end}")
            print(f"Environ {dead_code_end - dead_code_start} lignes à supprimer")
            
            # Sauvegarder et nettoyer
            new_lines = lines[:dead_code_start] + ['\n'] + lines[dead_code_end:]
            
            with open('/Users/sebastien/MATELAS_FINAL/app_gui.py', 'w') as f:
                f.writelines(new_lines)
            
            print("✅ Code mort supprimé")
        else:
            print("Pas de code mort détecté")

if __name__ == "__main__":
    clean_dead_code()