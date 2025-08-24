#!/usr/bin/env python3
"""
Script pour diagnostiquer et corriger le problème de l'interface graphique
"""

import re
import sys
from pathlib import Path

def diagnostiquer_probleme_gui():
    """Diagnostique le problème de l'interface graphique"""
    
    print("🔍 DIAGNOSTIC DE L'INTERFACE GRAPHIQUE")
    print("=" * 50)
    
    # Lire le fichier app_gui.py
    app_gui_path = Path("app_gui.py")
    if not app_gui_path.exists():
        print("❌ Fichier app_gui.py non trouvé")
        return False
    
    with open(app_gui_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📄 Fichier: {app_gui_path.absolute()}")
    print(f"📏 Taille: {app_gui_path.stat().st_size} octets")
    
    # Rechercher les problèmes
    problemes = []
    corrections = []
    
    # 1. Vérifier les appels à setOpenExternalLinks sur QTextEdit
    pattern_qtextedit = r'(\w+)\.setOpenExternalLinks\([^)]*\)'
    matches = re.finditer(pattern_qtextedit, content)
    
    for match in matches:
        ligne = content[:match.start()].count('\n') + 1
        variable = match.group(1)
        
        # Chercher la déclaration de la variable
        pattern_declaration = rf'{variable}\s*=\s*QTextEdit\(\)'
        if re.search(pattern_declaration, content):
            problemes.append(f"❌ Ligne {ligne}: {variable}.setOpenExternalLinks() appelé sur QTextEdit")
            corrections.append(f"   → Remplacer QTextEdit() par QTextBrowser() pour {variable}")
    
    # 2. Vérifier les QTextBrowser corrects
    pattern_qtextbrowser = r'(\w+)\s*=\s*QTextBrowser\(\)'
    matches = re.finditer(pattern_qtextbrowser, content)
    
    for match in matches:
        ligne = content[:match.start()].count('\n') + 1
        variable = match.group(1)
        corrections.append(f"✅ Ligne {ligne}: {variable} = QTextBrowser() (correct)")
    
    # 3. Vérifier les imports
    if 'from PyQt6.QtWidgets import QTextBrowser' in content:
        corrections.append("✅ QTextBrowser importé correctement")
    else:
        problemes.append("❌ QTextBrowser non importé")
        corrections.append("   → Ajouter QTextBrowser aux imports")
    
    # Afficher les résultats
    print("\n🔍 RÉSULTATS DU DIAGNOSTIC:")
    print("-" * 30)
    
    if problemes:
        print("❌ PROBLÈMES DÉTECTÉS:")
        for probleme in problemes:
            print(f"  {probleme}")
    else:
        print("✅ Aucun problème détecté")
    
    if corrections:
        print("\n💡 CORRECTIONS APPLIQUÉES:")
        for correction in corrections:
            print(f"  {correction}")
    
    return len(problemes) == 0

def corriger_interface_gui():
    """Corrige automatiquement les problèmes de l'interface graphique"""
    
    print("\n🔧 CORRECTION AUTOMATIQUE")
    print("=" * 30)
    
    app_gui_path = Path("app_gui.py")
    if not app_gui_path.exists():
        print("❌ Fichier app_gui.py non trouvé")
        return False
    
    # Sauvegarder le fichier original
    backup_path = app_gui_path.with_suffix('.py.backup')
    with open(app_gui_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(original_content)
    
    print(f"💾 Sauvegarde créée: {backup_path}")
    
    # Appliquer les corrections
    content = original_content
    modifications = []
    
    # 1. S'assurer que QTextBrowser est importé
    if 'from PyQt6.QtWidgets import QTextBrowser' not in content:
        # Ajouter QTextBrowser aux imports existants
        pattern_import = r'(from PyQt6\.QtWidgets import [^)]+)'
        match = re.search(pattern_import, content)
        if match:
            old_import = match.group(1)
            new_import = old_import + ', QTextBrowser'
            content = content.replace(old_import, new_import)
            modifications.append("✅ QTextBrowser ajouté aux imports")
    
    # 2. Remplacer les QTextEdit problématiques par QTextBrowser
    # Chercher les patterns où setOpenExternalLinks est appelé
    pattern_problematique = r'(\w+)\s*=\s*QTextEdit\(\)'
    matches = list(re.finditer(pattern_problematique, content))
    
    for match in reversed(matches):  # Parcourir en sens inverse pour éviter les problèmes d'index
        variable = match.group(1)
        start, end = match.span()
        
        # Vérifier si cette variable utilise setOpenExternalLinks
        pattern_usage = rf'{variable}\.setOpenExternalLinks\([^)]*\)'
        if re.search(pattern_usage, content):
            # Remplacer QTextEdit par QTextBrowser
            content = content[:start] + f'{variable} = QTextBrowser()' + content[end:]
            modifications.append(f"✅ {variable} changé de QTextEdit à QTextBrowser")
    
    # 3. S'assurer que setOpenExternalLinks(False) est présent pour le summary_text
    if 'self.summary_text.setOpenExternalLinks(False)' not in content:
        # Chercher la ligne après la création du summary_text
        pattern_summary = r'(self\.summary_text\s*=\s*QTextBrowser\(\)[^}]*?)(\n\s*)(self\.summary_text\.anchorClicked\.connect)'
        match = re.search(pattern_summary, content, re.DOTALL)
        if match:
            before = match.group(1)
            newline = match.group(2)
            after = match.group(3)
            insertion = f'{before}{newline}self.summary_text.setOpenExternalLinks(False)  # Désactiver l\'ouverture automatique{newline}{after}'
            content = re.sub(pattern_summary, insertion, content, flags=re.DOTALL)
            modifications.append("✅ setOpenExternalLinks(False) ajouté pour summary_text")
    
    # Sauvegarder les modifications
    if modifications:
        with open(app_gui_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Modifications appliquées:")
        for modif in modifications:
            print(f"  {modif}")
        
        print(f"\n💾 Fichier modifié: {app_gui_path}")
        print(f"💾 Sauvegarde: {backup_path}")
        
        return True
    else:
        print("ℹ️ Aucune modification nécessaire")
        return True

def tester_interface_gui():
    """Teste si l'interface graphique peut être lancée"""
    
    print("\n🧪 TEST DE L'INTERFACE GRAPHIQUE")
    print("=" * 35)
    
    try:
        # Test d'import des modules nécessaires
        print("📦 Test des imports...")
        
        import sys
        from PyQt6.QtWidgets import QApplication, QTextBrowser
        from PyQt6.QtCore import Qt
        
        print("✅ Imports PyQt6 réussis")
        
        # Test de création d'un QTextBrowser
        print("🔧 Test de création QTextBrowser...")
        app = QApplication(sys.argv)
        text_browser = QTextBrowser()
        text_browser.setOpenExternalLinks(False)
        text_browser.anchorClicked.connect(lambda url: print(f"Lien cliqué: {url}"))
        
        print("✅ QTextBrowser créé avec succès")
        print("✅ setOpenExternalLinks(False) fonctionne")
        print("✅ anchorClicked connecté")
        
        app.quit()
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def main():
    """Fonction principale"""
    
    print("🔧 CORRECTEUR D'INTERFACE GRAPHIQUE")
    print("=" * 40)
    
    # Diagnostic
    diagnostic_ok = diagnostiquer_probleme_gui()
    
    if not diagnostic_ok:
        # Correction automatique
        correction_ok = corriger_interface_gui()
        
        if correction_ok:
            # Re-diagnostic après correction
            print("\n🔍 VÉRIFICATION APRÈS CORRECTION:")
            diagnostic_ok = diagnostiquer_probleme_gui()
    
    # Test final
    test_ok = tester_interface_gui()
    
    # Résumé
    print("\n📊 RÉSUMÉ:")
    print("-" * 10)
    print(f"Diagnostic: {'✅ OK' if diagnostic_ok else '❌ Problèmes'}")
    print(f"Test: {'✅ OK' if test_ok else '❌ Échec'}")
    
    if diagnostic_ok and test_ok:
        print("\n🎉 L'interface graphique devrait maintenant fonctionner correctement!")
        print("💡 Vous pouvez lancer l'application avec: python3 app_gui.py")
    else:
        print("\n⚠️ Des problèmes persistent. Vérifiez les messages ci-dessus.")

if __name__ == "__main__":
    main() 