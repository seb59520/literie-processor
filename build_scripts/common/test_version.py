#!/usr/bin/env python3
"""
Test du système de version de l'application Matelas Processor
"""

import sys
import os

# Ajouter le répertoire courant au path
sys.path.append('.')

def test_version_system():
    """Test du système de version"""
    print("=== Test du système de version ===")
    
    try:
        from version import get_version, get_full_version, get_version_info, get_changelog
        
        # Test de la version simple
        version = get_version()
        print(f"✓ Version simple: {version}")
        assert version == "2.2.0", f"Version attendue: 2.2.0, obtenue: {version}"
        
        # Test de la version complète
        full_version = get_full_version()
        print(f"✓ Version complète: {full_version}")
        assert "2.2.0" in full_version, f"Version 2.2.0 non trouvée dans: {full_version}"
        
        # Test des informations de version
        version_info = get_version_info()
        print(f"✓ Informations de version: {version_info}")
        assert "version" in version_info, "Clé 'version' manquante"
        assert "build_date" in version_info, "Clé 'build_date' manquante"
        assert "build_number" in version_info, "Clé 'build_number' manquante"
        assert "full_version" in version_info, "Clé 'full_version' manquante"
        
        # Test du changelog
        changelog = get_changelog()
        print(f"✓ Changelog disponible (longueur: {len(changelog)} caractères)")
        assert len(changelog) > 100, "Changelog trop court"
        assert "Version 2.2.0" in changelog, "Version 2.2.0 non trouvée dans le changelog"
        
        print("\n✅ Tous les tests de version sont passés avec succès!")
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    except AssertionError as e:
        print(f"❌ Test échoué: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

def test_version_in_gui():
    """Test de l'intégration de la version dans l'interface GUI"""
    print("\n=== Test de l'intégration GUI ===")
    
    try:
        # Test d'import des modules GUI
        from app_gui import MatelasApp
        from PyQt6.QtWidgets import QApplication
        
        # Créer une application Qt pour les tests
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Créer l'application principale
        matelas_app = MatelasApp()
        
        # Vérifier que le titre contient la version
        window_title = matelas_app.windowTitle()
        print(f"✓ Titre de la fenêtre: {window_title}")
        assert "v2.2.0" in window_title, f"Version non trouvée dans le titre: {window_title}"
        
        # Fermer l'application
        matelas_app.close()
        
        print("✅ Test d'intégration GUI réussi!")
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import GUI: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test GUI: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("Test du système de version - Matelas Processor")
    print("=" * 50)
    
    # Test du système de version
    version_ok = test_version_system()
    
    # Test de l'intégration GUI
    gui_ok = test_version_in_gui()
    
    # Résumé
    print("\n" + "=" * 50)
    print("RÉSUMÉ DES TESTS:")
    print(f"✓ Système de version: {'PASSÉ' if version_ok else 'ÉCHOUÉ'}")
    print(f"✓ Intégration GUI: {'PASSÉ' if gui_ok else 'ÉCHOUÉ'}")
    
    if version_ok and gui_ok:
        print("\n🎉 Tous les tests sont passés avec succès!")
        return 0
    else:
        print("\n❌ Certains tests ont échoué.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 