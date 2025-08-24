#!/usr/bin/env python3
"""
Test direct de la logique Mr&MME corrigée
Vérifie que la correction fonctionne sans l'application
"""

import sys
import os

# Ajouter le répertoire backend au path
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(script_dir, "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

def test_logique_mr_mme_corrigee():
    """Test direct de la logique corrigée"""
    
    print("🧪 TEST DIRECT DE LA LOGIQUE MR&MME CORRIGÉE")
    print("=" * 60)
    
    try:
        # Importer le module corrigé
        from excel_import_utils import ExcelMatelasImporter
        
        print("✅ Module excel_import_utils importé avec succès")
        
        # Créer une instance
        utils = ExcelMatelasImporter()
        print("✅ Instance ExcelMatelasImporter créée")
        
        # Simuler une configuration sans titre Mr/Mme
        config_sans_titre = {
            "description": "MATELAS 1 PIÈCE - MOUSSE RAINURÉE 7 ZONES",
            "Client_D1": "CLIENT SANS TITRE"
        }
        
        # Tester l'extraction
        resultat = utils._extract_mr_mme_from_matelas_description(config_sans_titre)
        print(f"📋 Test extraction sans titre: '{resultat}' (attendu: '')")
        
        if resultat == "":
            print("✅ Extraction sans titre fonctionne correctement")
        else:
            print("❌ Extraction sans titre ne fonctionne pas")
        
        # Simuler une configuration avec titre Mr
        config_avec_titre = {
            "description": "MATELAS POUR Mr DUPONT - MOUSSE RAINURÉE",
            "Client_D1": "Mr DUPONT"
        }
        
        resultat2 = utils._extract_mr_mme_from_matelas_description(config_avec_titre)
        print(f"📋 Test extraction avec titre: '{resultat2}' (attendu: 'Mr')")
        
        if resultat2 == "Mr":
            print("✅ Extraction avec titre fonctionne correctement")
        else:
            print("❌ Extraction avec titre ne fonctionne pas")
        
        print("\n🎯 CONCLUSION DU TEST DIRECT:")
        if resultat == "" and resultat2 == "Mr":
            print("✅ La logique corrigée fonctionne parfaitement !")
            print("🚀 Vous pouvez maintenant relancer MatelasApp")
        else:
            print("❌ Il y a encore un problème dans le code")
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_logique_mr_mme_corrigee()
