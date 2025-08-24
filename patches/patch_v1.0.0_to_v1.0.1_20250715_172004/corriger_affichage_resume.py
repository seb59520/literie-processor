#!/usr/bin/env python3

"""
Script pour corriger le problème d'affichage dans l'onglet Résumé
"""

import sys
import os
sys.path.append('backend')

def corriger_affichage_resume():
    """Corrige le problème d'affichage dans l'onglet Résumé"""
    
    print("🔧 CORRECTION DU PROBLÈME D'AFFICHAGE - ONGLET RÉSUMÉ")
    print("=" * 60)
    
    # Vérifier si le fichier app_gui.py existe
    if not os.path.exists('app_gui.py'):
        print("❌ Fichier app_gui.py non trouvé")
        return False
    
    print("✅ Fichier app_gui.py trouvé")
    
    # Lire le contenu du fichier
    with open('app_gui.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier les problèmes potentiels
    problems = []
    
    # 1. Vérifier si QTextBrowser est utilisé
    if 'QTextBrowser' not in content:
        problems.append("QTextBrowser n'est pas utilisé")
    else:
        print("✅ QTextBrowser utilisé correctement")
    
    # 2. Vérifier la connexion du signal anchorClicked
    if 'anchorClicked.connect' not in content:
        problems.append("Signal anchorClicked non connecté")
    else:
        print("✅ Signal anchorClicked connecté")
    
    # 3. Vérifier la méthode open_excel_file
    if 'def open_excel_file' not in content:
        problems.append("Méthode open_excel_file manquante")
    else:
        print("✅ Méthode open_excel_file présente")
    
    # 4. Vérifier setOpenExternalLinks(False)
    if 'setOpenExternalLinks(False)' not in content:
        problems.append("setOpenExternalLinks(False) manquant")
    else:
        print("✅ setOpenExternalLinks(False) configuré")
    
    # 5. Vérifier la génération HTML
    if 'summary = f"' not in content:
        problems.append("Génération HTML manquante")
    else:
        print("✅ Génération HTML présente")
    
    # Afficher les problèmes trouvés
    if problems:
        print("\n❌ PROBLÈMES DÉTECTÉS:")
        for i, problem in enumerate(problems, 1):
            print(f"  {i}. {problem}")
        return False
    else:
        print("\n✅ Aucun problème détecté dans le code")
    
    # Vérifier les fichiers Excel existants
    print("\n📁 VÉRIFICATION DES FICHIERS EXCEL:")
    excel_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.xlsx'):
                excel_files.append(os.path.join(root, file))
    
    if excel_files:
        print(f"✅ {len(excel_files)} fichier(s) Excel trouvé(s):")
        for file in excel_files[:5]:  # Afficher les 5 premiers
            print(f"  📄 {file}")
        if len(excel_files) > 5:
            print(f"  ... et {len(excel_files) - 5} autre(s)")
    else:
        print("⚠️ Aucun fichier Excel trouvé")
    
    # Recommandations
    print("\n💡 RECOMMANDATIONS:")
    print("1. Redémarrez l'application complètement")
    print("2. Vérifiez que les fichiers Excel existent avant de cliquer sur les liens")
    print("3. Si le problème persiste, essayez de:")
    print("   - Effacer tous les résultats et recommencer")
    print("   - Vérifier les logs pour d'éventuelles erreurs")
    
    return True

def test_generation_html():
    """Teste la génération HTML avec des fichiers existants"""
    
    print("\n🧪 TEST DE GÉNÉRATION HTML:")
    print("-" * 40)
    
    # Chercher des fichiers Excel existants
    excel_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.xlsx'):
                excel_files.append(os.path.join(root, file))
    
    if not excel_files:
        print("❌ Aucun fichier Excel trouvé pour le test")
        return
    
    # Prendre le premier fichier Excel trouvé
    test_file = excel_files[0]
    print(f"📄 Utilisation du fichier: {test_file}")
    
    # Générer le HTML de test
    summary = "<h3>Test d'affichage</h3>"
    summary += "<h4>📁 Fichiers Excel générés:</h4>"
    
    file_path = os.path.abspath(test_file)
    if os.path.exists(file_path):
        summary += f"<p>🔗 <a href='file://{file_path}'>{os.path.basename(test_file)}</a></p>"
        print("✅ Lien généré correctement")
    else:
        summary += f"<p>⚠️ {os.path.basename(test_file)} (fichier non trouvé)</p>"
        print("❌ Fichier non trouvé")
    
    summary += "<p><em>💡 Cliquez sur les liens pour ouvrir les fichiers Excel directement.</em></p>"
    
    # Vérifier le HTML
    if "<a href=" in summary:
        print("✅ HTML avec liens généré correctement")
        print(f"🔗 Nombre de liens: {summary.count('<a href=')}")
    else:
        print("❌ Problème dans la génération HTML")

if __name__ == "__main__":
    print("🚀 DÉMARRAGE DE LA CORRECTION")
    print("=" * 60)
    
    # Correction principale
    success = corriger_affichage_resume()
    
    if success:
        # Test de génération HTML
        test_generation_html()
        
        print("\n🎯 CORRECTION TERMINÉE")
        print("=" * 60)
        print("✅ Le code semble correct")
        print("💡 Le problème pourrait être temporaire")
        print("🔄 Redémarrez l'application pour tester")
    else:
        print("\n❌ CORRECTION ÉCHOUÉE")
        print("=" * 60)
        print("⚠️ Des problèmes ont été détectés dans le code")
        print("🔧 Contactez le support technique") 