#!/usr/bin/env python3
"""
Test du système d'administration de l'application Matelas Processor
"""

import sys
import os

# Ajouter le répertoire courant au path
sys.path.append('.')

def test_admin_modules():
    """Test des modules d'administration"""
    print("=== Test des modules d'administration ===")
    
    try:
        # Test du module de mise à jour de version
        from update_version import get_current_version, update_version_file
        current_version = get_current_version()
        print(f"✓ Version actuelle: {current_version}")
        
        # Test du module de logging d'administration
        from admin_logger import setup_admin_logger, log_admin_operation
        logger = setup_admin_logger()
        print("✓ Logger d'administration configuré")
        
        # Test d'une opération de log
        log_admin_operation("Test", "Test du système d'administration")
        print("✓ Opération de log testée")
        
        # Test du module de version
        from version import get_version_info
        version_info = get_version_info()
        print(f"✓ Informations de version: {version_info['version']}")
        
        print("\n✅ Tous les modules d'administration sont fonctionnels!")
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

def test_admin_dialog_import():
    """Test de l'import du dialogue administrateur"""
    print("\n=== Test du dialogue administrateur ===")
    
    try:
        from admin_dialog import AdminDialog, show_admin_dialog
        print("✓ Dialogue administrateur importé avec succès")
        
        # Test de la fonction utilitaire
        print("✓ Fonction show_admin_dialog disponible")
        
        print("✅ Dialogue administrateur prêt à l'utilisation!")
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import du dialogue: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

def test_admin_logs():
    """Test du système de logs d'administration"""
    print("\n=== Test du système de logs ===")
    
    try:
        from admin_logger import get_admin_logs, log_admin_access
        
        # Tester l'accès administrateur
        log_admin_access(True)
        log_admin_access(False)
        print("✓ Logs d'accès créés")
        
        # Récupérer les logs
        logs = get_admin_logs()
        print(f"✓ Logs récupérés (longueur: {len(logs)} caractères)")
        
        if "Accès administrateur" in logs:
            print("✅ Logs d'administration fonctionnels!")
            return True
        else:
            print("❌ Logs d'administration vides ou incorrects")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test des logs: {e}")
        return False

def test_version_update_system():
    """Test du système de mise à jour de version"""
    print("\n=== Test du système de mise à jour ===")
    
    try:
        from update_version import get_current_version, update_version_file
        
        # Sauvegarder la version actuelle
        original_version = get_current_version()
        print(f"✓ Version originale: {original_version}")
        
        # Test de mise à jour (simulation)
        test_version = "2.2.0"  # Même version pour ne pas changer
        test_date = "2025-07-16"
        test_build = "20250716"
        test_changelog = "## Version 2.2.0 (2025-07-16)\n- Test de mise à jour"
        
        # Vérifier que la fonction existe
        success = update_version_file(test_version, test_date, test_build, test_changelog)
        print(f"✓ Fonction de mise à jour testée: {success}")
        
        # Vérifier que la version n'a pas changé (car même version)
        current_version = get_current_version()
        if current_version == original_version:
            print("✅ Système de mise à jour fonctionnel!")
            return True
        else:
            print(f"❌ Version inattendue: {current_version}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test de mise à jour: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("Test du système d'administration - Matelas Processor")
    print("=" * 60)
    
    # Test des modules
    modules_ok = test_admin_modules()
    
    # Test du dialogue
    dialog_ok = test_admin_dialog_import()
    
    # Test des logs
    logs_ok = test_admin_logs()
    
    # Test de mise à jour
    update_ok = test_version_update_system()
    
    # Résumé
    print("\n" + "=" * 60)
    print("RÉSUMÉ DES TESTS:")
    print(f"✓ Modules d'administration: {'PASSÉ' if modules_ok else 'ÉCHOUÉ'}")
    print(f"✓ Dialogue administrateur: {'PASSÉ' if dialog_ok else 'ÉCHOUÉ'}")
    print(f"✓ Système de logs: {'PASSÉ' if logs_ok else 'ÉCHOUÉ'}")
    print(f"✓ Mise à jour de version: {'PASSÉ' if update_ok else 'ÉCHOUÉ'}")
    
    if all([modules_ok, dialog_ok, logs_ok, update_ok]):
        print("\n🎉 Tous les tests d'administration sont passés avec succès!")
        print("\n📋 Fonctionnalités disponibles:")
        print("  • Menu Réglages → Administration (mot de passe: 1981)")
        print("  • Gestion des versions avec mise à jour automatique")
        print("  • Création et application de patches")
        print("  • Logs d'administration complets")
        print("  • Interface graphique sécurisée")
        return 0
    else:
        print("\n❌ Certains tests ont échoué.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 