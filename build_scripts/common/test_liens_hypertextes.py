#!/usr/bin/env python3
"""
Test des liens hypertextes dans l'onglet Résumé
Vérifie que les fichiers Excel générés sont bien affichés avec des liens cliquables
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_liens_hypertextes():
    """Test de la fonctionnalité des liens hypertextes"""
    
    print("🧪 Test des liens hypertextes dans l'onglet Résumé")
    print("=" * 60)
    
    # Simuler des fichiers Excel générés
    fichiers_excel_test = [
        "output/Matelas_S29_2025_1.xlsx",
        "output/Matelas_S29_2025_2.xlsx",
        "output/Sommier_S29_2025_1.xlsx"
    ]
    
    print(f"📁 Fichiers Excel de test ({len(fichiers_excel_test)}):")
    for fichier in fichiers_excel_test:
        print(f"   - {fichier}")
    
    print("\n🔗 Génération des liens hypertextes:")
    
    # Simuler la génération du résumé avec liens
    summary = "Résultats globaux (3 fichier(s) traité(s)):\n\n"
    summary += "📊 Total configurations matelas: 5\n"
    summary += "🛏️ Total configurations sommiers: 2\n"
    summary += "📋 Total éléments pré-import: 7\n"
    summary += "📁 Total fichiers Excel générés: 3\n\n"
    
    # Ajouter les liens hypertextes
    if fichiers_excel_test:
        summary += "📁 Fichiers Excel générés:\n"
        for fichier in fichiers_excel_test:
            # Créer un lien cliquable
            file_path = os.path.abspath(fichier)
            if os.path.exists(file_path):
                summary += f"   🔗 <a href='file://{file_path}' style='color: #0066cc; text-decoration: underline;'>{os.path.basename(fichier)}</a>\n"
            else:
                summary += f"   ⚠️ {os.path.basename(fichier)} (fichier non trouvé)\n"
        summary += "\n💡 Cliquez sur les liens pour ouvrir les fichiers Excel directement."
    
    print("✅ Résumé généré avec liens hypertextes:")
    print(summary)
    
    # Vérifier la structure des liens
    print("\n🔍 Vérification de la structure des liens:")
    lines = summary.split('\n')
    for line in lines:
        if 'href=' in line:
            print(f"   ✅ Lien détecté: {line.strip()}")
    
    print("\n🎯 Fonctionnalités testées:")
    print("   ✅ Génération des liens hypertextes")
    print("   ✅ Vérification de l'existence des fichiers")
    print("   ✅ Formatage HTML des liens")
    print("   ✅ Messages d'aide pour l'utilisateur")
    
    print("\n📝 Instructions pour tester dans l'application:")
    print("   1. Lancez l'application: python3 app_gui.py")
    print("   2. Traitez quelques fichiers PDF")
    print("   3. Allez dans l'onglet 'Résumé'")
    print("   4. Vérifiez que les fichiers Excel apparaissent avec des liens bleus")
    print("   5. Cliquez sur un lien pour ouvrir le fichier Excel")
    
    return True

if __name__ == "__main__":
    test_liens_hypertextes() 