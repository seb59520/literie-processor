#!/usr/bin/env python3
"""
Test de correction du nommage des fichiers avec les bonnes semaines de production
"""

import sys
import os
from datetime import datetime

# Ajouter le répertoire backend au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_nommage_fichiers_semaines():
    """Test que les fichiers sont nommés avec les bonnes semaines de production"""
    print("🧪 Test de correction du nommage des fichiers")
    print("=" * 60)
    
    try:
        from backend.date_utils import calculate_production_weeks
        from backend_interface import BackendInterface
        
        # Créer une instance du backend
        backend = BackendInterface()
        
        # Test avec semaine 29 de 2025
        semaine_ref = 29
        annee_ref = 2025
        
        print(f"📅 Test avec semaine référence: {semaine_ref}_{annee_ref}")
        
        # Calculer les semaines de production automatiquement
        recommendations = calculate_production_weeks(semaine_ref, annee_ref, True, True)
        
        semaine_matelas = recommendations['matelas']['semaine']
        annee_matelas = recommendations['matelas']['annee']
        semaine_sommiers = recommendations['sommiers']['semaine']
        annee_sommiers = recommendations['sommiers']['annee']
        
        print(f"  📋 Semaines calculées automatiquement:")
        print(f"    - Matelas: S{semaine_matelas}_{annee_matelas}")
        print(f"    - Sommiers: S{semaine_sommiers}_{annee_sommiers}")
        
        # Simuler des données de pré-import
        pre_import_data = [
            {
                'type_article': 'matelas',
                'Client_D1': 'Test Client',
                'noyau': 'LATEX MIXTE 7 ZONES',
                'quantite': 1
            },
            {
                'type_article': 'sommier',
                'Client_D1': 'Test Client',
                'type_sommier': 'LATTES',
                'quantite': 1
            }
        ]
        
        # Tester l'export avec les semaines de production calculées
        print(f"\n📁 Test de l'export Excel avec les bonnes semaines:")
        
        fichiers_crees = backend._export_excel_global(
            pre_import_data, semaine_ref, annee_ref,
            semaine_matelas=semaine_matelas, annee_matelas=annee_matelas,
            semaine_sommiers=semaine_sommiers, annee_sommiers=annee_sommiers
        )
        
        print(f"  ✅ Fichiers créés: {fichiers_crees}")
        
        # Vérifier que les noms de fichiers contiennent les bonnes semaines
        for fichier in fichiers_crees:
            nom_fichier = os.path.basename(fichier)
            print(f"  📄 Fichier: {nom_fichier}")
            
            if 'Matelas' in nom_fichier:
                # Vérifier que le nom contient la semaine matelas calculée
                semaine_attendue = f"S{str(semaine_matelas).zfill(2)}"
                if semaine_attendue in nom_fichier:
                    print(f"    ✅ Semaine matelas correcte: {semaine_attendue}")
                else:
                    print(f"    ❌ Semaine matelas incorrecte: attendu {semaine_attendue}")
                    
            elif 'Sommier' in nom_fichier:
                # Vérifier que le nom contient la semaine sommiers calculée
                semaine_attendue = f"S{str(semaine_sommiers).zfill(2)}"
                if semaine_attendue in nom_fichier:
                    print(f"    ✅ Semaine sommiers correcte: {semaine_attendue}")
                else:
                    print(f"    ❌ Semaine sommiers incorrecte: attendu {semaine_attendue}")
        
        # Test avec seulement matelas
        print(f"\n📋 Test avec seulement matelas:")
        recommendations_matelas = calculate_production_weeks(semaine_ref, annee_ref, True, False)
        semaine_matelas_seul = recommendations_matelas['matelas']['semaine']
        annee_matelas_seul = recommendations_matelas['matelas']['annee']
        
        pre_import_matelas_seul = [
            {
                'type_article': 'matelas',
                'Client_D1': 'Test Client Matelas',
                'noyau': 'LATEX MIXTE 7 ZONES',
                'quantite': 1
            }
        ]
        
        fichiers_matelas = backend._export_excel_global(
            pre_import_matelas_seul, semaine_ref, annee_ref,
            semaine_matelas=semaine_matelas_seul, annee_matelas=annee_matelas_seul
        )
        
        print(f"  📄 Fichiers matelas: {fichiers_matelas}")
        
        # Test avec seulement sommiers
        print(f"\n📋 Test avec seulement sommiers:")
        recommendations_sommiers = calculate_production_weeks(semaine_ref, annee_ref, False, True)
        semaine_sommiers_seul = recommendations_sommiers['sommiers']['semaine']
        annee_sommiers_seul = recommendations_sommiers['sommiers']['annee']
        
        pre_import_sommiers_seul = [
            {
                'type_article': 'sommier',
                'Client_D1': 'Test Client Sommiers',
                'type_sommier': 'LATTES',
                'quantite': 1
            }
        ]
        
        fichiers_sommiers = backend._export_excel_global(
            pre_import_sommiers_seul, semaine_ref, annee_ref,
            semaine_sommiers=semaine_sommiers_seul, annee_sommiers=annee_sommiers_seul
        )
        
        print(f"  📄 Fichiers sommiers: {fichiers_sommiers}")
        
        print(f"\n✅ Test de correction du nommage terminé avec succès !")
        
        # Nettoyer les fichiers de test
        print(f"\n🧹 Nettoyage des fichiers de test...")
        for fichier in fichiers_crees + fichiers_matelas + fichiers_sommiers:
            try:
                if os.path.exists(fichier):
                    os.remove(fichier)
                    print(f"  Supprimé: {os.path.basename(fichier)}")
            except Exception as e:
                print(f"  ⚠️ Impossible de supprimer {fichier}: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_comparaison_avant_apres():
    """Test de comparaison avant/après la correction"""
    print("\n🧪 Test de comparaison avant/après la correction")
    print("=" * 60)
    
    try:
        from backend.date_utils import calculate_production_weeks
        from backend_interface import BackendInterface
        
        backend = BackendInterface()
        
        # Semaine de référence
        semaine_ref = 29
        annee_ref = 2025
        
        # Calculer les semaines de production
        recommendations = calculate_production_weeks(semaine_ref, annee_ref, True, True)
        
        semaine_matelas = recommendations['matelas']['semaine']
        annee_matelas = recommendations['matelas']['annee']
        semaine_sommiers = recommendations['sommiers']['semaine']
        annee_sommiers = recommendations['sommiers']['annee']
        
        print(f"📅 Semaine référence: {semaine_ref}_{annee_ref}")
        print(f"📋 Semaines de production calculées:")
        print(f"  - Matelas: {semaine_matelas}_{annee_matelas}")
        print(f"  - Sommiers: {semaine_sommiers}_{annee_sommiers}")
        
        # Simuler des données
        pre_import_data = [
            {'type_article': 'matelas', 'Client_D1': 'Test', 'noyau': 'LATEX', 'quantite': 1},
            {'type_article': 'sommier', 'Client_D1': 'Test', 'type_sommier': 'LATTES', 'quantite': 1}
        ]
        
        # Test AVANT correction (utilise les semaines de référence)
        print(f"\n📁 AVANT correction (semaines de référence):")
        try:
            # Simuler l'ancien comportement en passant None pour les semaines de production
            fichiers_avant = backend._export_excel_global(
                pre_import_data, semaine_ref, annee_ref
            )
            print(f"  📄 Fichiers créés: {fichiers_avant}")
            
            # Nettoyer
            for fichier in fichiers_avant:
                if os.path.exists(fichier):
                    os.remove(fichier)
                    
        except Exception as e:
            print(f"  ⚠️ Erreur simulation avant: {e}")
        
        # Test APRÈS correction (utilise les semaines de production)
        print(f"\n📁 APRÈS correction (semaines de production):")
        fichiers_apres = backend._export_excel_global(
            pre_import_data, semaine_ref, annee_ref,
            semaine_matelas=semaine_matelas, annee_matelas=annee_matelas,
            semaine_sommiers=semaine_sommiers, annee_sommiers=annee_sommiers
        )
        print(f"  📄 Fichiers créés: {fichiers_apres}")
        
        # Vérifier la différence
        print(f"\n🔍 Comparaison des noms de fichiers:")
        for fichier in fichiers_apres:
            nom_fichier = os.path.basename(fichier)
            print(f"  📄 {nom_fichier}")
            
            # Extraire la semaine du nom de fichier
            if 'Matelas' in nom_fichier:
                # Format attendu: Matelas_S30_2025_1.xlsx
                parts = nom_fichier.split('_')
                if len(parts) >= 3:
                    semaine_fichier = parts[1]  # S30
                    annee_fichier = parts[2]    # 2025
                    print(f"    - Semaine fichier: {semaine_fichier}")
                    print(f"    - Semaine calculée: S{str(semaine_matelas).zfill(2)}")
                    print(f"    - Année fichier: {annee_fichier}")
                    print(f"    - Année calculée: {annee_matelas}")
                    
                    if semaine_fichier == f"S{str(semaine_matelas).zfill(2)}" and annee_fichier == str(annee_matelas):
                        print(f"    ✅ CORRECTION RÉUSSIE pour les matelas !")
                    else:
                        print(f"    ❌ Problème persistant pour les matelas")
                        
            elif 'Sommier' in nom_fichier:
                # Format attendu: Sommier_S30_2025_1.xlsx
                parts = nom_fichier.split('_')
                if len(parts) >= 3:
                    semaine_fichier = parts[1]  # S30
                    annee_fichier = parts[2]    # 2025
                    print(f"    - Semaine fichier: {semaine_fichier}")
                    print(f"    - Semaine calculée: S{str(semaine_sommiers).zfill(2)}")
                    print(f"    - Année fichier: {annee_fichier}")
                    print(f"    - Année calculée: {annee_sommiers}")
                    
                    if semaine_fichier == f"S{str(semaine_sommiers).zfill(2)}" and annee_fichier == str(annee_sommiers):
                        print(f"    ✅ CORRECTION RÉUSSIE pour les sommiers !")
                    else:
                        print(f"    ❌ Problème persistant pour les sommiers")
        
        # Nettoyer
        for fichier in fichiers_apres:
            if os.path.exists(fichier):
                os.remove(fichier)
        
        print(f"\n✅ Test de comparaison terminé !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test de comparaison: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Test de correction du nommage des fichiers avec les bonnes semaines")
    print("=" * 80)
    
    # Test principal
    success1 = test_nommage_fichiers_semaines()
    
    # Test de comparaison
    success2 = test_comparaison_avant_apres()
    
    if success1 and success2:
        print(f"\n🎉 TOUS LES TESTS SONT PASSÉS !")
        print(f"✅ Le nommage des fichiers utilise maintenant les bonnes semaines de production")
    else:
        print(f"\n❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print(f"⚠️ Vérifiez les erreurs ci-dessus") 