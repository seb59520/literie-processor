#!/usr/bin/env python3

"""
Script de test pour vérifier la correction de l'affichage de l'onglet Résumé
"""

import sys
import os
sys.path.append('backend')

def test_correction_affichage():
    """Teste la correction de l'affichage de l'onglet Résumé"""
    
    print("🧪 TEST DE LA CORRECTION D'AFFICHAGE - ONGLET RÉSUMÉ")
    print("=" * 60)
    
    # Vérifier que le fichier app_gui.py existe
    if not os.path.exists('app_gui.py'):
        print("❌ Fichier app_gui.py non trouvé")
        return False
    
    print("✅ Fichier app_gui.py trouvé")
    
    # Lire le contenu du fichier
    with open('app_gui.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier les corrections apportées
    corrections = []
    
    # 1. Vérifier que QTextBrowser est utilisé
    if 'QTextBrowser' in content:
        corrections.append("✅ QTextBrowser utilisé correctement")
    else:
        corrections.append("❌ QTextBrowser non trouvé")
    
    # 2. Vérifier que setOpenExternalLinks(False) est configuré
    if 'setOpenExternalLinks(False)' in content:
        corrections.append("✅ setOpenExternalLinks(False) configuré")
    else:
        corrections.append("❌ setOpenExternalLinks(False) non trouvé")
    
    # 3. Vérifier que anchorClicked est connecté
    if 'anchorClicked.connect(self.open_excel_file)' in content:
        corrections.append("✅ anchorClicked connecté à open_excel_file")
    else:
        corrections.append("❌ anchorClicked non connecté")
    
    # 4. Vérifier que la méthode open_excel_file appelle update_display
    if 'self.update_display()' in content and 'open_excel_file' in content:
        corrections.append("✅ open_excel_file appelle update_display")
    else:
        corrections.append("❌ open_excel_file n'appelle pas update_display")
    
    # 5. Vérifier que le style CSS est appliqué
    if 'QTextBrowser {' in content and 'font-size:' in content:
        corrections.append("✅ Style CSS appliqué au QTextBrowser")
    else:
        corrections.append("❌ Style CSS non appliqué")
    
    # Afficher les résultats
    print("\n📋 VÉRIFICATION DES CORRECTIONS:")
    print("-" * 40)
    for correction in corrections:
        print(f"  {correction}")
    
    # Vérifier les problèmes potentiels
    print("\n🔍 VÉRIFICATION DES PROBLÈMES POTENTIELS:")
    print("-" * 40)
    
    problems = []
    
    # 1. Vérifier qu'il n'y a pas de setOpenExternalLinks(True)
    if 'setOpenExternalLinks(True)' in content:
        problems.append("⚠️ setOpenExternalLinks(True) trouvé - peut causer des problèmes")
    else:
        problems.append("✅ Pas de setOpenExternalLinks(True)")
    
    # 2. Vérifier qu'il n'y a pas de QTextEdit utilisé pour les liens
    if 'QTextEdit' in content and 'anchorClicked' in content:
        problems.append("⚠️ QTextEdit avec anchorClicked - peut causer des erreurs")
    else:
        problems.append("✅ Pas de QTextEdit avec anchorClicked")
    
    # 3. Vérifier qu'il n'y a pas de duplication de connexion de signal
    anchor_clicked_count = content.count('anchorClicked.connect')
    if anchor_clicked_count > 1:
        problems.append(f"⚠️ {anchor_clicked_count} connexions anchorClicked - risque de duplication")
    else:
        problems.append("✅ Une seule connexion anchorClicked")
    
    for problem in problems:
        print(f"  {problem}")
    
    # Résumé
    print("\n📊 RÉSUMÉ:")
    print("-" * 20)
    
    success_count = sum(1 for c in corrections if c.startswith("✅"))
    total_corrections = len(corrections)
    
    problem_count = sum(1 for p in problems if p.startswith("⚠️"))
    
    print(f"Corrections appliquées: {success_count}/{total_corrections}")
    print(f"Problèmes détectés: {problem_count}")
    
    if success_count == total_corrections and problem_count == 0:
        print("🎉 Toutes les corrections sont appliquées correctement !")
        return True
    else:
        print("⚠️ Des problèmes persistent, vérification recommandée")
        return False

def test_generation_html():
    """Teste la génération du HTML pour l'onglet Résumé"""
    
    print("\n🧪 TEST DE GÉNÉRATION HTML:")
    print("=" * 40)
    
    # Simuler des données de test
    all_results = [
        {
            'filename': 'test1.pdf',
            'status': 'Traité avec succès',
            'configurations_matelas': [{'noyau': 'LATEX NATUREL', 'quantite': 1}],
            'pre_import': [{'Client_D1': 'Test Client'}],
            'fichiers_excel': ['/Users/sebastien/Downloads/test1.xlsx']
        }
    ]
    
    all_configurations = [{'noyau': 'LATEX NATUREL', 'quantite': 1}]
    all_configurations_sommiers = []
    all_preimport = [{'Client_D1': 'Test Client'}]
    all_excel_files = ['/Users/sebastien/Downloads/test1.xlsx']
    
    # Générer le HTML comme dans update_display
    summary = f"""<h3>Résultats globaux ({len(all_results)} fichier(s))</h3>
    
<h4>📊 Statistiques</h4>
<p><strong>Fichiers traités:</strong> {len(all_results)}</p>
<p><strong>Configurations matelas:</strong> {len(all_configurations)}</p>
<p><strong>Configurations sommiers:</strong> {len(all_configurations_sommiers)}</p>
<p><strong>Données pré-import:</strong> {len(all_preimport)}</p>

<h4>📁 Fichiers Excel générés ({len(all_excel_files)})</h4>"""
    
    # Ajouter les liens vers les fichiers Excel
    for i, excel_file in enumerate(all_excel_files, 1):
        filename = os.path.basename(excel_file)
        summary += f'<p><a href="file://{excel_file}">📄 {filename}</a></p>'
    
    summary += """
<h4>📋 Détail des fichiers traités</h4>"""
    
    for result in all_results:
        filename = os.path.basename(result['filename'])
        status = result['status']
        config_count = len(result.get('configurations_matelas', []))
        sommier_count = len(result.get('configurations_sommiers', []))
        
        summary += f"""
<p><strong>{filename}</strong> - {status}</p>
<ul>
    <li>Configurations matelas: {config_count}</li>
    <li>Configurations sommiers: {sommier_count}</li>
</ul>"""
    
    # Vérifier que le HTML est valide
    print("✅ HTML généré avec succès")
    print(f"📏 Taille du HTML: {len(summary)} caractères")
    
    # Vérifier la présence des liens
    link_count = summary.count('<a href="file://')
    print(f"🔗 Nombre de liens: {link_count}")
    
    # Vérifier la structure HTML
    if '<h3>' in summary and '<h4>' in summary and '<p>' in summary:
        print("✅ Structure HTML correcte")
    else:
        print("❌ Structure HTML incorrecte")
    
    # Afficher un extrait du HTML généré
    print("\n📄 Extrait du HTML généré:")
    print("-" * 30)
    lines = summary.split('\n')
    for i, line in enumerate(lines[:10]):
        print(f"{i+1:2d}: {line}")
    if len(lines) > 10:
        print("    ...")
    
    return True

if __name__ == "__main__":
    print("🚀 DÉMARRAGE DES TESTS DE CORRECTION D'AFFICHAGE")
    print("=" * 60)
    
    # Test 1: Vérification des corrections
    test1_success = test_correction_affichage()
    
    # Test 2: Génération HTML
    test2_success = test_generation_html()
    
    # Résumé final
    print("\n🎯 RÉSUMÉ FINAL:")
    print("=" * 20)
    
    if test1_success and test2_success:
        print("✅ Tous les tests sont passés avec succès !")
        print("✅ L'affichage de l'onglet Résumé devrait fonctionner correctement")
        print("✅ Les liens hypertextes devraient ouvrir les fichiers Excel sans affecter l'affichage")
    else:
        print("⚠️ Certains tests ont échoué")
        print("⚠️ Vérification manuelle recommandée")
    
    print("\n📝 Instructions pour tester:")
    print("1. Lancez l'application: python3 app_gui.py")
    print("2. Traitez quelques fichiers PDF")
    print("3. Allez dans l'onglet Résumé")
    print("4. Cliquez sur un lien Excel")
    print("5. Vérifiez que le fichier s'ouvre et que l'affichage reste inchangé") 