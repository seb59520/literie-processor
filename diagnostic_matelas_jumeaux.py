#!/usr/bin/env python3
"""
Diagnostic de la logique des matelas jumeaux
"""

import json
import os
import re

def diagnostic_matelas_jumeaux():
    """Diagnostic de la logique des matelas jumeaux"""
    
    print("🔍 DIAGNOSTIC DE LA LOGIQUE DES MATELAS JUMEAUX")
    print("=" * 60)
    
    # 1. Vérifier la configuration actuelle
    print("\n📁 1. CONFIGURATION ACTUELLE:")
    
    config_file = 'matelas_config.json'
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            print(f"   ✅ {config_file} trouvé")
            print(f"   🔧 Provider LLM: {config.get('llm_provider', 'NON CONFIGURÉ')}")
            
            if 'ollama' in config:
                ollama_config = config['ollama']
                print(f"   🎯 Modèle Ollama: {ollama_config.get('model', 'NON CONFIGURÉ')}")
                
        except Exception as e:
            print(f"   ❌ Erreur lecture configuration: {e}")
            config = {}
    else:
        print(f"   ❌ {config_file} non trouvé")
        config = {}
    
    # 2. Vérifier les logs récents pour voir l'extraction LLM
    print("\n🔍 2. ANALYSE DES LOGS RÉCENTS:")
    
    log_file = 'debug_llm.log'
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                last_lines = lines[-20:] if len(lines) > 20 else lines
            
            print(f"   📊 Dernières {len(last_lines)} lignes du log:")
            
            # Chercher les informations sur l'extraction LLM
            llm_extraction_found = False
            jumeaux_detected = False
            
            for line in last_lines:
                line = line.strip()
                if line:
                    # Chercher l'extraction LLM
                    if 'Appel LLM avec provider: ollama' in line:
                        print(f"      🔍 {line}")
                        llm_extraction_found = True
                    
                    # Chercher la détection des jumeaux
                    if 'jumeaux' in line.lower():
                        print(f"      🎯 {line}")
                        jumeaux_detected = True
                    
                    # Chercher les configurations créées
                    if 'Configuration' in line and 'écrite' in line:
                        print(f"      📝 {line}")
                    
                    # Chercher les erreurs
                    if 'ERROR' in line or 'WARNING' in line:
                        print(f"      ⚠️ {line}")
                        
        except Exception as e:
            print(f"   ❌ Erreur lecture log: {e}")
    else:
        print(f"   ❌ Fichier log {log_file} non trouvé")
    
    # 3. Vérifier la logique des matelas jumeaux dans le code
    print("\n🔍 3. VÉRIFICATION DE LA LOGIQUE DANS LE CODE:")
    
    # Lire le fichier backend_interface.py pour vérifier la logique
    backend_file = 'backend_interface.py'
    if os.path.exists(backend_file):
        try:
            with open(backend_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier la présence de la logique des jumeaux
            if 'is_jumeaux = "jumeaux" in description.lower()' in content:
                print("   ✅ Logique de détection des jumeaux trouvée")
            else:
                print("   ❌ Logique de détection des jumeaux NON trouvée")
            
            if 'if is_jumeaux and quantite_float > 1:' in content:
                print("   ✅ Logique conditionnelle des jumeaux trouvée")
            else:
                print("   ❌ Logique conditionnelle des jumeaux NON trouvée")
            
            if 'prefixe = "4 x " if quantite == 2 else ("2 x " if quantite == 1 else' in content:
                print("   ✅ Logique de calcul des dimensions housse jumeaux trouvée")
            else:
                print("   ❌ Logique de calcul des dimensions housse jumeaux NON trouvée")
                
        except Exception as e:
            print(f"   ❌ Erreur lecture {backend_file}: {e}")
    else:
        print(f"   ❌ Fichier {backend_file} non trouvé")
    
    # 4. Test de la logique des jumeaux
    print("\n🧪 4. TEST DE LA LOGIQUE DES JUMEAUX:")
    
    # Simuler la logique des jumeaux
    test_cases = [
        {
            "description": "MATELAS JUMEAUX - MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES FERME (50KG/ M3) - HOUSSE MATELASSÉE TENCEL LUXE 3D AVEC POIGNÉES INTÉGRÉES DÉHOUSSABLE SUR 3 CÔTÉS ET LAVABLE A 40° 139/ 189/ 20",
            "quantite": 2,
            "expected_jumeaux": True
        },
        {
            "description": "MATELAS 1 PIÈCE - MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES FERME (50KG/ M3) - HOUSSE MATELASSÉE TENCEL LUXE 3D AVEC POIGNÉES INTÉGRÉES DÉHOUSSABLE SUR 3 CÔTÉS ET LAVABLE A 40° 139/ 189/ 20",
            "quantite": 1,
            "expected_jumeaux": False
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\n   📋 Test {i+1}:")
        print(f"      Description: {test_case['description'][:80]}...")
        print(f"      Quantité: {test_case['quantite']}")
        
        # Simuler la détection des jumeaux
        is_jumeaux = "jumeaux" in test_case['description'].lower()
        print(f"      Détection jumeaux: {is_jumeaux}")
        
        # Simuler la logique conditionnelle
        if is_jumeaux and test_case['quantite'] > 1:
            print(f"      ✅ Cas des jumeaux: 1 configuration avec quantité = {test_case['quantite']}")
        else:
            print(f"      ℹ️ Cas normal: {test_case['quantite']} configuration(s) avec quantité = 1")
        
        # Simuler le calcul des dimensions housse
        if is_jumeaux and test_case['quantite'] == 2:
            print(f"      🎯 Dimensions housse jumeaux: 4 x [valeur]")
        elif test_case['quantite'] == 1:
            print(f"      🎯 Dimensions housse 1 pièce: 2 x [valeur]")
        else:
            print(f"      🎯 Dimensions housse: {test_case['quantite'] * 2} x [valeur]")
    
    # 5. Vérifier les fichiers Excel générés
    print("\n🔍 5. VÉRIFICATION DES FICHIERS EXCEL:")
    
    downloads_dir = os.path.expanduser("~/Downloads")
    if os.path.exists(downloads_dir):
        excel_files = [f for f in os.listdir(downloads_dir) if f.endswith('.xlsx') and 'Matelas_' in f]
        
        if excel_files:
            print(f"   ✅ Fichiers Excel trouvés: {len(excel_files)}")
            for file in sorted(excel_files, reverse=True)[:3]:  # 3 plus récents
                print(f"      📄 {file}")
        else:
            print("   ℹ️ Aucun fichier Excel Matelas trouvé dans Downloads")
    else:
        print("   ❌ Répertoire Downloads non trouvé")
    
    # 6. Solutions proposées
    print("\n🔧 6. SOLUTIONS PROPOSÉES:")
    
    if not llm_extraction_found:
        print("   🚨 PROBLÈME: Extraction LLM non détectée dans les logs")
        print("      Solution: Vérifier que l'option LLM est activée")
    
    if not jumeaux_detected:
        print("   🚨 PROBLÈME: Détection des jumeaux non trouvée dans les logs")
        print("      Solution: Vérifier que le prompt LLM inclut la détection des jumeaux")
    
    print("\n   🚀 Actions recommandées:")
    print("      1. Vérifier que l'option 'Utiliser l'enrichissement LLM' est cochée")
    print("      2. Vérifier que le prompt LLM inclut la détection des jumeaux")
    print("      3. Tester avec un PDF contenant clairement 'MATELAS JUMEAUX'")
    print("      4. Vérifier les logs pour voir l'extraction LLM")
    
    return True

def instructions_test_jumeaux():
    """Instructions pour tester la logique des jumeaux"""
    
    print("\n📋 INSTRUCTIONS POUR TESTER LA LOGIQUE DES JUMEAUX:")
    
    print("   1. 📱 Ouvrir MatelasApp")
    print("   2. ✅ Cocher 'Utiliser l'enrichissement LLM'")
    print("   3. 📄 Sélectionner un PDF contenant 'MATELAS JUMEAUX'")
    print("   4. 🚀 Cliquer sur 'Traiter les fichiers'")
    
    print("\n   🔍 Vérifications à faire:")
    print("   - Dans les logs: 'Appel LLM avec provider: ollama'")
    print("   - Dans les logs: Détection des jumeaux")
    print("   - Dans les logs: 'Cas des jumeaux: 1 configuration avec quantité = 2'")
    print("   - Dans Excel: Cellules jumeaux_C10 et jumeaux_D10 remplies")
    print("   - Dans Excel: Dimensions housse avec préfixe '4 x' pour jumeaux")

if __name__ == "__main__":
    print("🔍 Diagnostic de la logique des matelas jumeaux")
    
    # Diagnostic principal
    success = diagnostic_matelas_jumeaux()
    
    # Instructions de test
    instructions_test_jumeaux()
    
    if success:
        print("\n🎯 RÉSUMÉ DU DIAGNOSTIC:")
        print("✅ Configuration analysée")
        print("🔍 Logs examinés")
        print("🧪 Logique des jumeaux testée")
        print("🔧 Solutions proposées")
    else:
        print("\n❌ Problème détecté dans le diagnostic")
    
    print("\n=== FIN DU DIAGNOSTIC DES MATELAS JUMEAUX ===")

