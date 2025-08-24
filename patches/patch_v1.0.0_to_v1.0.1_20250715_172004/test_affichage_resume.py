#!/usr/bin/env python3

"""
Script de test pour vérifier l'affichage de l'onglet Résumé
"""

import sys
import os
sys.path.append('backend')

def test_affichage_resume():
    """Teste l'affichage de l'onglet Résumé"""
    
    print("🧪 TEST D'AFFICHAGE DE L'ONGLET RÉSUMÉ")
    print("=" * 50)
    
    # Simuler des données de test
    all_results = [
        {
            'filename': 'test1.pdf',
            'status': 'Traité avec succès',
            'configurations_matelas': [{'noyau': 'LATEX NATUREL', 'quantite': 1}],
            'pre_import': [{'Client_D1': 'Test Client'}],
            'fichiers_excel': ['output/test1.xlsx']
        },
        {
            'filename': 'test2.pdf', 
            'status': 'Traité avec succès',
            'configurations_matelas': [{'noyau': 'MOUSSE VISCO', 'quantite': 2}],
            'pre_import': [{'Client_D1': 'Test Client 2'}],
            'fichiers_excel': ['output/test2.xlsx']
        }
    ]
    
    all_configurations = [
        {'noyau': 'LATEX NATUREL', 'quantite': 1, 'dimensions': {'largeur': 160, 'longueur': 200}},
        {'noyau': 'MOUSSE VISCO', 'quantite': 2, 'dimensions': {'largeur': 140, 'longueur': 190}}
    ]
    
    all_configurations_sommiers = [
        {'type_sommier': 'LATEX', 'quantite': 1, 'dimensions': {'largeur': 160, 'longueur': 200}}
    ]
    
    all_preimport = [
        {'Client_D1': 'Test Client', 'numero_D2': '12345', 'semaine_D5': 'S01'},
        {'Client_D1': 'Test Client 2', 'numero_D2': '67890', 'semaine_D5': 'S02'}
    ]
    
    all_excel_files = [
        'output/test1.xlsx',
        'output/test2.xlsx'
    ]
    
    # Générer le HTML comme dans update_display
    summary = f"<h3>Résultats globaux ({len(all_results)} fichier(s) traité(s))</h3>"
    
    total_configs_matelas = len(all_configurations)
    total_configs_sommiers = len(all_configurations_sommiers)
    total_preimport = len(all_preimport)
    total_excel = len(all_excel_files)
    
    summary += f"<p><strong>📊 Total configurations matelas:</strong> {total_configs_matelas}</p>"
    summary += f"<p><strong>🛏️ Total configurations sommiers:</strong> {total_configs_sommiers}</p>"
    summary += f"<p><strong>📋 Total éléments pré-import:</strong> {total_preimport}</p>"
    summary += f"<p><strong>📁 Total fichiers Excel générés:</strong> {total_excel}</p>"
    
    summary += "<h4>Détail par fichier:</h4>"
    for i, result in enumerate(all_results, 1):
        filename = result.get('filename', 'N/A')
        status = result.get('status', 'N/A')
        configs = len(result.get('configurations_matelas', []))
        preimport = len(result.get('pre_import', []))
        excel = len(result.get('fichiers_excel', []))
        
        summary += f"<p><strong>{i}. {filename}</strong><br>"
        summary += f"   Statut: {status}<br>"
        summary += f"   Configurations: {configs}<br>"
        summary += f"   Pré-import: {preimport}<br>"
        summary += f"   Excel: {excel}</p>"
    
    # Ajouter les liens hypertextes
    if all_excel_files:
        summary += "<h4>📁 Fichiers Excel générés:</h4>"
        for fichier in all_excel_files:
            file_path = os.path.abspath(fichier)
            if os.path.exists(file_path):
                summary += f"<p>🔗 <a href='file://{file_path}'>{os.path.basename(fichier)}</a></p>"
            else:
                summary += f"<p>⚠️ {os.path.basename(fichier)} (fichier non trouvé)</p>"
        summary += "<p><em>💡 Cliquez sur les liens pour ouvrir les fichiers Excel directement.</em></p>"
    
    print("📄 HTML généré:")
    print("-" * 30)
    print(summary)
    print("-" * 30)
    
    # Vérifier que le HTML est valide
    if "<h3>" in summary and "<a href=" in summary:
        print("✅ HTML généré correctement avec liens hypertextes")
    else:
        print("❌ Problème dans la génération HTML")
    
    # Vérifier les liens
    link_count = summary.count("<a href=")
    print(f"🔗 Nombre de liens détectés: {link_count}")
    
    return summary

if __name__ == "__main__":
    test_affichage_resume() 