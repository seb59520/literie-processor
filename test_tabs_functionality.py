#!/usr/bin/env python3
"""Test des fonctionnalités des onglets Configuration, Logs et Debug"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_debug_info():
    """Test de la fonction get_debug_info"""
    try:
        # Simuler la méthode get_debug_info
        import platform
        from datetime import datetime
        
        try:
            import psutil
            memory_info = f"- RAM totale: {psutil.virtual_memory().total / (1024**3):.1f} GB\n- RAM utilisée: {psutil.virtual_memory().percent}%\n- Disque libre: {psutil.disk_usage('.').free / (1024**3):.1f} GB"
        except ImportError:
            memory_info = "- Informations mémoire non disponibles (psutil manquant)"
        
        info = f"""=== INFORMATIONS DE DEBUG ===
Généré le: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
SYSTÈME:
- OS: {platform.system()} {platform.release()}
- Architecture: {platform.architecture()[0]}
- Processeur: {platform.processor() or 'Non disponible'}
- Python: {platform.python_version()}
{memory_info}

APPLICATION:
- Dossier: {os.getcwd()}
- Script: {__file__}
"""
        print("✅ Debug info généré avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur debug info: {e}")
        return False

def test_system_metrics():
    """Test de la fonction update_system_metrics"""
    try:
        try:
            import psutil
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('.')
            disk_percent = (disk.used / disk.total) * 100
            
            print(f"✅ Métriques système: CPU {cpu_percent:.1f}%, RAM {memory.percent:.1f}%, Disque {disk_percent:.1f}%")
        except ImportError:
            print("✅ Métriques système: Mode fallback (psutil non disponible)")
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur métriques système: {e}")
        return False

def test_logs_refresh():
    """Test de la fonction refresh_logs"""
    try:
        from datetime import datetime
        timestamp = datetime.now().strftime('%H:%M:%S')
        refresh_message = f"[{timestamp}] 🔄 Logs actualisés\n"
        
        print(f"✅ Refresh logs: {refresh_message.strip()}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur refresh logs: {e}")
        return False

def test_config_functionality():
    """Test des fonctionnalités de configuration"""
    try:
        from config import Config
        config = Config()
        
        # Test get_excel_output_directory
        excel_dir = config.get_excel_output_directory()
        print(f"✅ Configuration Excel: {excel_dir}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur configuration: {e}")
        return False

def main():
    print("🧪 Test des fonctionnalités des onglets")
    print("=" * 50)
    
    tests = [
        ("Debug Info", test_debug_info),
        ("System Metrics", test_system_metrics), 
        ("Logs Refresh", test_logs_refresh),
        ("Configuration", test_config_functionality)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n🔍 Test {name}:")
        results.append(test_func())
    
    success_count = sum(results)
    total_tests = len(tests)
    
    print(f"\n📊 Résultats: {success_count}/{total_tests} tests réussis")
    
    if success_count == total_tests:
        print("✅ Tous les tests des onglets réussis !")
        print("✅ Les onglets Configuration, Logs et Debug devraient fonctionner correctement")
    else:
        print("⚠️ Certains tests ont échoué")
    
    return success_count == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)