#!/usr/bin/env python3
"""Test progressif des imports pour identifier le crash"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🔍 Test des imports...")

try:
    print("1. Test imports PyQt6...")
    from PyQt6.QtWidgets import QApplication, QMainWindow
    from PyQt6.QtCore import QTimer
    from PyQt6.QtGui import QIcon
    print("✅ PyQt6 OK")
    
    print("2. Test imports backend...")
    try:
        from backend.advanced_logging import get_advanced_logger
        print("✅ advanced_logging OK")
    except Exception as e:
        print(f"❌ advanced_logging: {e}")
        
    try:
        from backend.workflow_engine import get_workflow_engine
        print("✅ workflow_engine OK")
    except Exception as e:
        print(f"❌ workflow_engine: {e}")
    
    print("3. Test imports principaux de app_gui...")
    # Test imports critique de app_gui sans l'exécuter
    exec("""
import logging
import json
import subprocess
from datetime import datetime
from pathlib import Path
""")
    print("✅ Imports standards OK")
    
    print("4. Test classe principale sans init...")
    # Importer juste la définition sans instancier
    with open('/Users/sebastien/MATELAS_FINAL/app_gui.py', 'r') as f:
        content = f.read()
    
    # Chercher les imports problématiques
    if "markdown" in content:
        try:
            import markdown
            print("✅ markdown disponible")
        except ImportError:
            print("⚠️ markdown manquant")
    
    print("✅ Tous les imports testés")
    
except Exception as e:
    print(f"❌ Erreur lors des tests: {e}")
    import traceback
    traceback.print_exc()