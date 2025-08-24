#!/usr/bin/env python3
"""Test spécifique pour AlertPanel"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout

def test_alert_panel():
    """Test d'import et création d'AlertPanel"""
    print("🔍 Test AlertPanel...")
    
    try:
        # Test import backend
        from backend.real_time_alerts import RealTimeAlertSystem, AlertPanel
        print("✅ Import AlertPanel réussi")
        
        # Test création QApplication
        app = QApplication(sys.argv)
        
        # Test création système d'alertes
        print("🔄 Création RealTimeAlertSystem...")
        alert_system = RealTimeAlertSystem(None)
        print("✅ RealTimeAlertSystem créé")
        
        # Test création AlertPanel
        print("🔄 Création AlertPanel...")
        alert_panel = AlertPanel(alert_system)
        print("✅ AlertPanel créé")
        
        # Test configuration
        alert_panel.setMaximumHeight(200)
        alert_panel.setMinimumHeight(100)
        print("✅ Configuration AlertPanel OK")
        
        print("✅ Test AlertPanel réussi !")
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur création AlertPanel: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_alert_panel()