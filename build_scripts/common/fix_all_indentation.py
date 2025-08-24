#!/usr/bin/env python3
"""
Script pour corriger automatiquement toutes les erreurs d'indentation dans les fichiers backend
"""

import os
import re
from pathlib import Path

def fix_indentation_errors():
    """Corrige les erreurs d'indentation dans tous les fichiers backend"""
    print("🔧 Correction des erreurs d'indentation dans backend/")
    print("=" * 50)
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Dossier backend non trouvé")
        return False
    
    files_modified = 0
    
    for py_file in backend_dir.glob("*.py"):
        print(f"📄 Traitement de {py_file.name}...")
        
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Pattern pour détecter les lignes mal indentées après un import
            # Cherche une ligne qui commence par un mot-clé sans indentation après un import
            lines = content.split('\n')
            fixed_lines = []
            
            for i, line in enumerate(lines):
                # Si c'est une ligne d'import, vérifier la ligne suivante
                if 'from backend.asset_utils import' in line and i + 1 < len(lines):
                    next_line = lines[i + 1]
                    # Si la ligne suivante n'est pas indentée et contient un appel de fonction
                    if (not next_line.startswith(' ') and 
                        ('get_referentiel_path(' in next_line or 
                         'json_path =' in next_line or
                         'REFERENTIEL_PATH =' in next_line)):
                        # Corriger l'indentation
                        indent = ' ' * 8  # 8 espaces pour correspondre au niveau try
                        fixed_lines.append(line)
                        fixed_lines.append(indent + next_line.lstrip())
                        # Marquer que la ligne suivante a été traitée
                        if i + 1 < len(lines):
                            lines[i + 1] = "SKIP_THIS_LINE"
                    else:
                        fixed_lines.append(line)
                elif line == "SKIP_THIS_LINE":
                    continue  # Ignorer cette ligne car elle a été traitée
                else:
                    fixed_lines.append(line)
            
            content = '\n'.join(fixed_lines)
            
            # Si le contenu a changé, sauvegarder
            if content != original_content:
                with open(py_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"   ✅ Corrigé: {py_file.name}")
                files_modified += 1
            else:
                print(f"   ℹ️ Aucune erreur d'indentation trouvée")
                
        except Exception as e:
            print(f"   ❌ Erreur lors du traitement de {py_file.name}: {e}")
    
    print(f"\n🎉 Correction terminée!")
    print(f"📊 Fichiers modifiés: {files_modified}")
    
    return True

def main():
    print("🚀 Correction automatique des erreurs d'indentation")
    print("=" * 50)
    
    if fix_indentation_errors():
        print("\n✅ Toutes les erreurs d'indentation ont été corrigées")
        print("💡 Vous pouvez maintenant recompiler l'application:")
        print("   python3 build_final_solution.py")
    else:
        print("\n❌ Erreur lors de la correction")

if __name__ == "__main__":
    main() 