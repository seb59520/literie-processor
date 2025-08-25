#!/usr/bin/env python3
"""
Script pour vérifier et lister tous les modules manquants
"""

import sys
import os

def check_module(module_name):
    """Teste si un module peut être importé"""
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False

def find_missing_modules():
    """Trouve tous les modules manquants dans app_gui.py"""
    
    # Modules locaux à vérifier
    local_modules = [
        'backend_interface',
        'aide_generateur_preimport', 
        'config',
        'version',
        'liste_champs_pre_import',
        'workflow_manager_widget',
        'gui_enhancements'
    ]
    
    # Modules Python standards
    standard_modules = [
        'PyQt6.QtWidgets',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'requests',
        'pandas',
        'openpyxl',
        'psutil'
    ]
    
    missing_local = []
    missing_standard = []
    
    print("=" * 50)
    print("VÉRIFICATION DES DÉPENDANCES")
    print("=" * 50)
    
    # Vérifier modules locaux
    print("\nModules locaux:")
    for module in local_modules:
        if os.path.exists(f"{module}.py"):
            print(f"✅ {module}.py - PRÉSENT")
        else:
            print(f"❌ {module}.py - MANQUANT")
            missing_local.append(module)
    
    # Vérifier modules Python
    print("\nModules Python:")
    for module in standard_modules:
        if check_module(module):
            print(f"✅ {module} - INSTALLÉ")
        else:
            print(f"❌ {module} - MANQUANT")
            missing_standard.append(module)
    
    # Vérifier le dossier backend
    print("\nDossier backend:")
    if os.path.exists("backend"):
        backend_files = len([f for f in os.listdir("backend") if f.endswith('.py')])
        print(f"✅ backend/ - {backend_files} fichiers Python")
    else:
        print("❌ backend/ - MANQUANT")
    
    # Résumé
    print("\n" + "=" * 50)
    print("RÉSUMÉ")
    print("=" * 50)
    
    if missing_local:
        print(f"\n❌ Modules locaux manquants ({len(missing_local)}):")
        for module in missing_local:
            print(f"   - {module}.py")
    
    if missing_standard:
        print(f"\n❌ Modules Python manquants ({len(missing_standard)}):")
        for module in missing_standard:
            print(f"   - {module}")
    
    if not missing_local and not missing_standard:
        print("\n✅ TOUTES LES DÉPENDANCES SONT PRÉSENTES!")
        return True
    else:
        print(f"\n⚠️  {len(missing_local + missing_standard)} dépendances manquantes")
        return False

if __name__ == "__main__":
    success = find_missing_modules()
    
    if not success:
        print("\n" + "=" * 50)
        print("ACTIONS RECOMMANDÉES")
        print("=" * 50)
        print("\n1. Pour les modules Python manquants:")
        print("   pip install [nom_du_module]")
        print("\n2. Pour les modules locaux manquants:")
        print("   Copiez les fichiers .py depuis le projet principal")
        print("\n3. Relancez ce script pour vérifier")
    
    sys.exit(0 if success else 1)