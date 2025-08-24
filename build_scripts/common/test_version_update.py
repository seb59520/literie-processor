#!/usr/bin/env python3
"""
Test de mise à jour de la version
"""

import sys
import os

def test_version_update():
    """Test que la version a été correctement mise à jour"""
    print("🧪 TEST MISE À JOUR VERSION")
    print("=" * 50)
    
    try:
        from version import get_version, get_full_version, get_version_info
        
        # Test de la version
        version = get_version()
        full_version = get_full_version()
        version_info = get_version_info()
        
        print(f"📋 Version: {version}")
        print(f"📋 Version complète: {full_version}")
        print(f"📋 Informations: {version_info}")
        
        # Vérifier que la version est 3.8.0
        expected_version = "3.8.0"
        if version == expected_version:
            print(f"✅ Version correcte: {version}")
        else:
            print(f"❌ Version incorrecte: {version} (attendu: {expected_version})")
            return False
        
        # Vérifier que la date de build est correcte
        expected_build_date = "2025-07-17"
        if version_info["build_date"] == expected_build_date:
            print(f"✅ Date de build correcte: {version_info['build_date']}")
        else:
            print(f"❌ Date de build incorrecte: {version_info['build_date']} (attendu: {expected_build_date})")
            return False
        
        # Test du changelog
        from version import get_changelog
        changelog = get_changelog()
        
        if "Version 3.8.0" in changelog:
            print("✅ Changelog contient la version 3.8.0")
        else:
            print("❌ Changelog ne contient pas la version 3.8.0")
            return False
        
        if "Système d'alertes de noyaux non détectés" in changelog:
            print("✅ Changelog contient les nouvelles fonctionnalités")
        else:
            print("❌ Changelog ne contient pas les nouvelles fonctionnalités")
            return False
        
        print("\n✅ Test de mise à jour de version réussi !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans test_version_update: {e}")
        return False

def test_changelog_file():
    """Test que le fichier CHANGELOG.md a été mis à jour"""
    print("\n🧪 TEST FICHIER CHANGELOG.MD")
    print("=" * 50)
    
    try:
        # Lire le fichier CHANGELOG.md
        with open("CHANGELOG.md", "r", encoding="utf-8") as f:
            changelog_content = f.read()
        
        # Vérifier que la version 3.8.0 est présente
        if "## Version 3.8.0 - 2025-07-17" in changelog_content:
            print("✅ Version 3.8.0 présente dans CHANGELOG.md")
        else:
            print("❌ Version 3.8.0 manquante dans CHANGELOG.md")
            return False
        
        # Vérifier que les nouvelles fonctionnalités sont documentées
        features_to_check = [
            "Système d'alertes de noyaux non détectés",
            "Interface utilisateur dédiée",
            "Gestion multi-fichiers",
            "Workflow intégré",
            "NoyauAlertDialog",
            "LATEX NATUREL",
            "LATEX MIXTE 7 ZONES",
            "MOUSSE RAINUREE 7 ZONES"
        ]
        
        missing_features = []
        for feature in features_to_check:
            if feature in changelog_content:
                print(f"✅ Fonctionnalité documentée: {feature}")
            else:
                missing_features.append(feature)
                print(f"❌ Fonctionnalité manquante: {feature}")
        
        if missing_features:
            print(f"\n⚠️ Fonctionnalités manquantes: {missing_features}")
            return False
        
        print("\n✅ Test du fichier CHANGELOG.md réussi !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans test_changelog_file: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 DÉBUT DES TESTS - MISE À JOUR VERSION")
    print("=" * 60)
    
    tests = [
        test_version_update,
        test_changelog_file
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Erreur dans le test {test.__name__}: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 RÉSULTATS: {passed}/{total} tests passent")
    
    if passed == total:
        print("🎉 TOUS LES TESTS PASSENT !")
        print("\n✅ La mise à jour de version est correcte !")
        print("\n📋 Éléments validés:")
        print("  • Version 3.8.0 correctement définie")
        print("  • Date de build mise à jour")
        print("  • Changelog complet avec nouvelles fonctionnalités")
        print("  • Documentation des alertes de noyaux")
        print("  • Cohérence entre version.py et CHANGELOG.md")
    else:
        print("⚠️  Certains tests ont échoué")
    
    return passed == total

if __name__ == "__main__":
    main() 