#!/usr/bin/env python3
"""
Script de validation finale - Test de tous les composants
"""

import sys
import os
from pathlib import Path

def test_python_syntax():
    """Tester la syntaxe Python de tous les fichiers"""
    print("🐍 Test syntaxe Python...")
    
    python_files = [
        "app_gui.py",
        "config.py", 
        "version.py",
        "package_builder.py",
        "auto_package_generator.py"
    ]
    
    for file_name in python_files:
        if Path(file_name).exists():
            try:
                # Test de compilation
                with open(file_name, 'r', encoding='utf-8') as f:
                    compile(f.read(), file_name, 'exec')
                print(f"   ✅ {file_name}")
            except SyntaxError as e:
                print(f"   ❌ {file_name}: {e}")
                return False
        else:
            print(f"   ⚠️ {file_name}: non trouvé")
    
    return True

def test_imports():
    """Tester les imports critiques"""
    print("\n📦 Test imports critiques...")
    
    tests = [
        ("config", "Configuration système"),
        ("version", "Gestion versions"),
        ("aide_generateur_preimport", "Générateur pré-import"),
        ("enhanced_processing_ui", "Interface améliorée"),
        ("gui_enhancements", "Améliorations GUI"),
        ("secure_storage", "Stockage sécurisé")
    ]
    
    success_count = 0
    for module, desc in tests:
        try:
            __import__(module)
            print(f"   ✅ {module} ({desc})")
            success_count += 1
        except ImportError as e:
            print(f"   ❌ {module}: {e}")
    
    print(f"\n📊 Résultat: {success_count}/{len(tests)} modules OK")
    return success_count >= len(tests) - 1  # Permettre 1 échec

def test_qt_availability():
    """Tester la disponibilité de PyQt6"""
    print("\n🖥️ Test PyQt6...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        print("   ✅ PyQt6 disponible")
        
        # Test de création d'application
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        print("   ✅ QApplication créée")
        
        return True
    except ImportError as e:
        print(f"   ❌ PyQt6: {e}")
        return False

def main():
    """Fonction principale de validation"""
    print("🧪 VALIDATION FINALE MATELAS v3.11.12")
    print("=" * 50)
    
    print(f"📂 Répertoire: {Path.cwd()}")
    print(f"🐍 Python: {sys.version}")
    
    # Tests
    tests = [
        ("Syntaxe Python", test_python_syntax),
        ("Imports modules", test_imports),
        ("PyQt6", test_qt_availability)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
            print(f"\n{'✅' if result else '❌'} {test_name}: {'RÉUSSI' if result else 'ÉCHEC'}")
        except Exception as e:
            print(f"\n❌ {test_name}: ERREUR - {e}")
            results.append(False)
    
    # Résultat final
    success_rate = sum(results) / len(results) * 100
    
    print("\n" + "=" * 50)
    if success_rate >= 80:
        print(f"✅ VALIDATION RÉUSSIE ({success_rate:.0f}%)")
        print("\n🚀 L'application peut être lancée:")
        print("   python app_gui.py")
    else:
        print(f"❌ VALIDATION ÉCHOUÉE ({success_rate:.0f}%)")
        print("\n🔧 Vérifiez les erreurs ci-dessus")
    
    input("\nAppuyez sur Entrée pour fermer...")
    return success_rate >= 80

if __name__ == "__main__":
    main()
