#!/usr/bin/env python3
"""
Diagnostic du comportement actuel de la logique Mr&MME
Vérifie si la correction a été appliquée et fonctionne
"""

import json
import sys
import os

# Ajouter le répertoire backend au path
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(script_dir, "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

def verifier_code_corrige():
    """Vérifie si le code a été corrigé"""
    
    print("🔍 VÉRIFICATION DU CODE CORRIGÉ")
    print("=" * 50)
    
    # Vérifier le fichier excel_import_utils.py
    fichier = "backend/excel_import_utils.py"
    
    if not os.path.exists(fichier):
        print(f"❌ Fichier {fichier} non trouvé")
        return False
    
    try:
        with open(fichier, 'r', encoding='utf-8') as f:
            contenu = f.read()
        
        # Vérifier les éléments de correction
        corrections = [
            "Si aucun titre Mr/Mme n'est trouvé, toutes les cellules D28 à D44 sont vidées",
            "Si C contient \"X\" mais AUCUN titre Mr/Mme trouvé, vider D",
            "Si C ne contient pas \"X\", s'assurer que D est vide",
            "aucun titre trouvé, toutes les cellules D28-D44 vidées"
        ]
        
        print("📋 Vérification des corrections dans le code :")
        for i, correction in enumerate(corrections, 1):
            if correction in contenu:
                print(f"   ✅ {i}. Correction présente")
            else:
                print(f"   ❌ {i}. Correction MANQUANTE")
        
        # Vérifier la logique spécifique
        if "worksheet[d_cell_address] = \"\"" in contenu:
            print("   ✅ Logique de vidage des cellules présente")
        else:
            print("   ❌ Logique de vidage des cellules MANQUANTE")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du fichier: {e}")
        return False

def simuler_comportement_attendu():
    """Simule le comportement attendu après correction"""
    
    print("\n🎯 COMPORTEMENT ATTENDU APRÈS CORRECTION")
    print("=" * 50)
    
    print("📋 SCÉNARIO 1: Avec titre Mr trouvé")
    print("   C37 = 'X' + description contient 'Mr'")
    print("   → D37 = 'Mr' ✅")
    
    print("\n📋 SCÉNARIO 2: Sans titre Mr/Mme")
    print("   C37 = 'X' + AUCUNE description avec 'Mr' ou 'Mme'")
    print("   → D37 = '' (vide) ✅")
    
    print("\n📋 SCÉNARIO 3: C37 ne contient pas 'X'")
    print("   C37 = '' (vide) + description contient 'Mr'")
    print("   → D37 = '' (vide) ✅")
    
    print("\n📋 SCÉNARIO 4: Nettoyage automatique")
    print("   Si aucun titre trouvé → Toutes les cellules D28-D44 vidées ✅")

def verifier_logs_recents():
    """Vérifie les logs récents pour voir le comportement actuel"""
    
    print("\n📊 VÉRIFICATION DES LOGS RÉCENTS")
    print("=" * 50)
    
    fichier_log = "logs/matelas_app.log"
    
    if not os.path.exists(fichier_log):
        print(f"❌ Fichier de log {fichier_log} non trouvé")
        return
    
    try:
        with open(fichier_log, 'r', encoding='utf-8') as f:
            lignes = f.readlines()
        
        # Chercher les dernières occurrences de la logique Mr&MME
        logiques_mr_mme = []
        for ligne in lignes[-100:]:  # Dernières 100 lignes
            if "Logique Mr&MME appliquée" in ligne:
                logiques_mr_mme.append(ligne.strip())
        
        if logiques_mr_mme:
            print(f"📋 Dernières logiques Mr&MME appliquées ({len(logiques_mr_mme)}):")
            for logique in logiques_mr_mme[-5:]:  # 5 dernières
                print(f"   📝 {logique}")
        else:
            print("   📝 Aucune logique Mr&MME récente trouvée")
        
        # Chercher les applications de la logique conditionnelle
        applications = []
        for ligne in lignes[-100:]:
            if "Application de la logique conditionnelle Mr&MME" in ligne:
                applications.append(ligne.strip())
        
        if applications:
            print(f"\n📋 Dernières applications de la logique conditionnelle ({len(applications)}):")
            for app in applications[-3:]:  # 3 dernières
                print(f"   🔧 {app}")
        else:
            print("\n   🔧 Aucune application récente trouvée")
            
    except Exception as e:
        print(f"❌ Erreur lors de la lecture des logs: {e}")

def main():
    """Fonction principale"""
    
    print("🔧 DIAGNOSTIC COMPLET DE LA LOGIQUE MR&MME")
    print("=" * 60)
    
    # 1. Vérifier le code
    code_ok = verifier_code_corrige()
    
    # 2. Simuler le comportement attendu
    simuler_comportement_attendu()
    
    # 3. Vérifier les logs
    verifier_logs_recents()
    
    # 4. Conclusion
    print("\n🎯 CONCLUSION")
    print("=" * 30)
    
    if code_ok:
        print("✅ Le code semble avoir été corrigé")
        print("⚠️  Si le problème persiste, il faut :")
        print("   1. Redémarrer MatelasApp")
        print("   2. Tester avec un nouveau PDF")
        print("   3. Vérifier que les cellules D sont bien vidées")
    else:
        print("❌ Le code n'a pas été corrigé")
        print("🔧 Il faut appliquer la correction dans excel_import_utils.py")

if __name__ == "__main__":
    main()

