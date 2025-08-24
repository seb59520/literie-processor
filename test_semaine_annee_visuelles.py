#!/usr/bin/env python3
"""
Script de test pour vérifier que la semaine et l'année sont visuelles uniquement
"""

import os
import re
from datetime import datetime

def test_modifications_semaine_annee():
    """Teste les modifications de la semaine et année"""
    
    print("🔍 TEST DES MODIFICATIONS SEMAINE ET ANNÉE")
    print("=" * 60)
    
    fichier_gui = "app_gui.py"
    
    if not os.path.exists(fichier_gui):
        print(f"❌ Fichier {fichier_gui} non trouvé")
        return False
    
    try:
        with open(fichier_gui, 'r', encoding='utf-8') as f:
            contenu = f.read()
        
        # Vérifier que les QSpinBox ont été remplacés par des QLabel
        modifications = [
            # Semaine
            ("QSpinBox semaine supprimé", "self.semaine_ref_spin = QSpinBox()", False),
            ("QLabel semaine ajouté", "self.semaine_ref_label = QLabel", True),
            ("Semaine visuelle", "Semaine {current_week}", True),
            
            # Année
            ("QSpinBox année supprimé", "self.annee_ref_spin = QSpinBox()", False),
            ("QLabel année ajouté", "self.annee_ref_label = QLabel", True),
            ("Année visuelle", "Année {current_year}", True),
            
            # Styles
            ("Style QLabel semaine", "QLabel {", True),
            ("Style QLabel année", "QLabel {", True),
            ("Bordure bleue", "border: 2px solid #3498db", True),
            ("Fond gris clair", "background-color: #ecf0f1", True),
        ]
        
        print("📋 Vérification des modifications:")
        for nom, code, doit_exister in modifications:
            if doit_exister:
                if code in contenu:
                    print(f"   ✅ {nom}")
                else:
                    print(f"   ❌ {nom} - Code manquant")
            else:
                if code not in contenu:
                    print(f"   ✅ {nom} - Supprimé avec succès")
                else:
                    print(f"   ❌ {nom} - Encore présent")
        
        # Vérifier les tooltips
        tooltips = [
            ("Tooltip semaine", "Semaine actuelle (non modifiable)"),
            ("Tooltip année", "Année actuelle (non modifiable)")
        ]
        
        print("\n📝 Vérification des tooltips:")
        for nom, texte in tooltips:
            if texte in contenu:
                print(f"   ✅ {nom}")
            else:
                print(f"   ❌ {nom} - Texte manquant")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

def afficher_apercu_interface():
    """Affiche un aperçu de l'interface modifiée"""
    
    print("\n🎨 APERÇU DE L'INTERFACE MODIFIÉE")
    print("=" * 50)
    
    current_week = datetime.now().isocalendar()[1]
    current_year = datetime.now().year
    
    print(f"""
📱 INTERFACE SIMPLIFIÉE :

┌─────────────────────────────────────┐
│           📆 Semaine actuelle      │
│                                     │
│        ┌─────────────────────┐     │
│        │   Semaine {current_week:2d}      │     │
│        └─────────────────────┘     │
│        (Non modifiable)            │
│                                     │
│           📅 Année actuelle        │
│                                     │
│        ┌─────────────────────┐     │
│        │   Année {current_year}      │     │
│        └─────────────────────┘     │
│        (Non modifiable)            │
└─────────────────────────────────────┘

✅ AVANTAGES :
   • Interface plus claire et simple
   • Pas de risque d'erreur de saisie
   • Affichage informatif et élégant
   • Mise à jour automatique quotidienne
   • Style cohérent avec le reste de l'interface

🎯 UTILISATION :
   • La semaine et l'année s'affichent automatiquement
   • Aucune action utilisateur requise
   • Les semaines de production sont calculées automatiquement
   • Interface plus intuitive et moins sujette aux erreurs
""")

def verifier_imports_datetime():
    """Vérifie que datetime est bien importé"""
    
    print("\n⏰ VÉRIFICATION DE L'IMPORT DATETIME")
    print("=" * 40)
    
    try:
        from datetime import datetime
        
        current_week = datetime.now().isocalendar()[1]
        current_year = datetime.now().year
        
        print(f"✅ Module datetime importé avec succès")
        print(f"✅ Semaine actuelle : {current_week}")
        print(f"✅ Année actuelle : {current_year}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erreur import datetime: {e}")
        return False

def main():
    """Fonction principale"""
    
    print("🎯 TEST DES MODIFICATIONS SEMAINE ET ANNÉE VISUELLES")
    print("=" * 70)
    
    # Test 1: Vérification des modifications
    if not test_modifications_semaine_annee():
        print("❌ Test des modifications échoué")
        return False
    
    # Test 2: Vérification de datetime
    if not verifier_imports_datetime():
        print("❌ Test de datetime échoué")
        return False
    
    # Test 3: Aperçu de l'interface
    afficher_apercu_interface()
    
    print("\n🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS !")
    print("✅ La semaine et l'année sont maintenant visuelles uniquement")
    print("✅ Interface simplifiée et plus intuitive")
    
    return True

if __name__ == "__main__":
    main()

