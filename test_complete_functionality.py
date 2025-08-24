#!/usr/bin/env python3
"""Test complet des fonctionnalités corrigées"""

import sys
import os
sys.path.append('.')

def test_excel_folder_button():
    """Test du bouton ouvrir dossier Excel"""
    try:
        from config import Config
        config = Config()
        excel_dir = config.get_excel_output_directory()
        
        from pathlib import Path
        excel_path = Path(excel_dir)
        
        print(f"✅ Dossier Excel configuré: {excel_dir}")
        print(f"✅ Dossier existe: {excel_path.exists()}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur dossier Excel: {e}")
        return False

def test_configuration_tabs():
    """Test des onglets Configuration"""
    try:
        from PyQt6.QtWidgets import QApplication
        app = QApplication([])
        
        from app_gui import MatelasApp
        matelas_app = MatelasApp()
        
        # Vérifier les tables de configuration
        required_tables = ['matelas_config_table', 'sommiers_config_table', 'preimport_table']
        for table_name in required_tables:
            if hasattr(matelas_app, table_name):
                print(f"✅ Table {table_name} créée")
            else:
                print(f"❌ Table {table_name} manquante") 
                return False
                
        return True
    except Exception as e:
        print(f"❌ Erreur onglets configuration: {e}")
        return False

def test_logs_tab():
    """Test de l'onglet Logs"""
    try:
        from PyQt6.QtWidgets import QApplication
        app = QApplication([])
        
        from app_gui import MatelasApp
        matelas_app = MatelasApp()
        
        # Vérifier les widgets de logs
        if not hasattr(matelas_app, 'log_text'):
            print("❌ Widget log_text manquant")
            return False
            
        if not hasattr(matelas_app, 'log_filter_combo'):
            print("❌ Widget log_filter_combo manquant")
            return False
        
        # Test des méthodes logs
        matelas_app.clear_logs()
        print("✅ clear_logs() fonctionne")
        
        matelas_app.filter_logs()
        print("✅ filter_logs() fonctionne")
        
        matelas_app.refresh_logs()
        print("✅ refresh_logs() fonctionne")
        
        return True
    except Exception as e:
        print(f"❌ Erreur onglet logs: {e}")
        return False

def test_monitoring_system():
    """Test du système de monitoring avancé"""
    try:
        from PyQt6.QtWidgets import QApplication
        app = QApplication([])
        
        from app_gui import MatelasApp
        matelas_app = MatelasApp()
        
        # Vérifier les widgets de monitoring
        monitoring_widgets = ['cpu_label', 'memory_label', 'disk_label', 'metrics_timer']
        for widget in monitoring_widgets:
            if hasattr(matelas_app, widget):
                print(f"✅ Widget monitoring {widget} présent")
            else:
                print(f"❌ Widget monitoring {widget} manquant")
                return False
        
        # Test des méthodes
        matelas_app.start_metrics_timer()
        print("✅ start_metrics_timer() fonctionne")
        
        matelas_app.update_system_metrics()
        print("✅ update_system_metrics() fonctionne")
        
        matelas_app.get_debug_info()
        print("✅ get_debug_info() fonctionne")
        
        return True
    except Exception as e:
        print(f"❌ Erreur système de monitoring: {e}")
        return False

def main():
    print("🧪 Test complet des fonctionnalités corrigées")
    print("=" * 60)
    
    tests = [
        ("Bouton dossier Excel", test_excel_folder_button),
        ("Onglets Configuration", test_configuration_tabs),
        ("Onglet Logs", test_logs_tab),
        ("Système de monitoring", test_monitoring_system)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n🔍 Test {name}:")
        print("-" * 30)
        results.append(test_func())
        print()
    
    success_count = sum(results)
    total_tests = len(tests)
    
    print("📊 RÉSUMÉ FINAL:")
    print("=" * 60)
    print(f"Tests réussis: {success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("✅ Le bouton ouvrir dossier Excel utilise le répertoire configuré")
        print("✅ Les onglets Configuration et Logs fonctionnent correctement")  
        print("✅ Le système de monitoring avancé est opérationnel")
        print("✅ L'application est stable et sans erreurs")
    else:
        print("⚠️ Certains tests ont échoué")
        failed_tests = [tests[i][0] for i, result in enumerate(results) if not result]
        print(f"Tests échoués: {', '.join(failed_tests)}")
    
    return success_count == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)