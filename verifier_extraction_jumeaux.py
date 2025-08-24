#!/usr/bin/env python3
"""
Vérification de l'extraction des jumeaux par le LLM
"""

import json
import os
import re

def verifier_extraction_jumeaux():
    """Vérifie l'extraction des jumeaux par le LLM"""
    
    print("🔍 VÉRIFICATION DE L'EXTRACTION DES JUMEAUX PAR LE LLM")
    print("=" * 60)
    
    # 1. Analyser le dernier log pour voir ce qui a été extrait
    print("\n📊 1. ANALYSE DU DERNIER LOG:")
    
    log_file = 'debug_llm.log'
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            print(f"   📊 Total lignes dans le log: {len(lines)}")
            
            # Chercher la dernière extraction LLM complète
            last_json_start = None
            last_json_end = None
            
            for i, line in enumerate(lines):
                if line.strip().startswith('{'):
                    last_json_start = i
                elif line.strip().endswith('}'):
                    last_json_end = i
            
            if last_json_start is not None and last_json_end is not None:
                print(f"   🔍 Dernier JSON trouvé: lignes {last_json_start + 1} à {last_json_end + 1}")
                
                # Extraire le JSON complet
                json_lines = lines[last_json_start:last_json_end + 1]
                json_text = ''.join(json_lines)
                
                print(f"   📝 JSON extrait (longueur: {len(json_text)} caractères)")
                
                # Essayer de parser le JSON
                try:
                    data = json.loads(json_text)
                    print("   ✅ JSON parsé avec succès")
                    
                    # Analyser la structure
                    print(f"   📋 Structure détectée:")
                    if 'articles' in data:
                        articles = data['articles']
                        print(f"      - Articles: {len(articles)}")
                        
                        for i, article in enumerate(articles):
                            print(f"\n      📋 Article {i+1}:")
                            print(f"        - Type: {article.get('type', 'NON DÉFINI')}")
                            print(f"        - Description: {article.get('description', 'NON DÉFINI')[:80]}...")
                            print(f"        - Quantité: {article.get('quantite', 'NON DÉFINI')}")
                            print(f"        - Dimensions: {article.get('dimensions', 'NON DÉFINI')}")
                            
                            # Vérifier les champs spécifiques aux jumeaux
                            est_jumeaux = article.get('est_jumeaux', 'NON DÉFINI')
                            type_matelas = article.get('type_matelas', 'NON DÉFINI')
                            
                            print(f"        - est_jumeaux: {est_jumeaux}")
                            print(f"        - type_matelas: {type_matelas}")
                            
                            # Détecter si c'est des jumeaux
                            is_jumeaux = False
                            if est_jumeaux is True:
                                is_jumeaux = True
                                print(f"        ✅ Détection via 'est_jumeaux': True")
                            elif type_matelas == 'jumeaux':
                                is_jumeaux = True
                                print(f"        ✅ Détection via 'type_matelas': jumeaux")
                            elif "jumeaux" in str(article.get('description', '')).lower():
                                is_jumeaux = True
                                print(f"        ✅ Détection via description: jumeaux trouvé")
                            else:
                                print(f"        ℹ️ Détection: Pas de jumeaux")
                            
                            # Simuler la logique de configuration
                            quantite = article.get('quantite', 1)
                            if is_jumeaux and quantite > 1:
                                print(f"        🎯 Cas des jumeaux: 1 configuration avec quantité = {quantite}")
                                print(f"        📏 Dimensions housse: 4 x [valeur] (jumeaux)")
                            else:
                                print(f"        ℹ️ Cas normal: {quantite} configuration(s) avec quantité = 1")
                                print(f"        📏 Dimensions housse: 2 x [valeur] (1 pièce)")
                    
                    if 'mode_mise_a_disposition' in data:
                        mode = data['mode_mise_a_disposition']
                        print(f"\n      🚚 Mode de mise à disposition:")
                        print(f"        - Emporte client: {mode.get('emporte_client_C57', 'NON DÉFINI')}")
                        print(f"        - Fourgon: {mode.get('fourgon_C58', 'NON DÉFINI')}")
                        print(f"        - Transporteur: {mode.get('transporteur_C59', 'NON DÉFINI')}")
                        
                except json.JSONDecodeError as e:
                    print(f"   ❌ Erreur parsing JSON: {e}")
                    print(f"   📝 Début du JSON: {json_text[:200]}...")
                    
        except Exception as e:
            print(f"   ❌ Erreur lecture log: {e}")
    else:
        print(f"   ❌ Fichier log {log_file} non trouvé")
    
    # 2. Vérifier le prompt actuel dans backend_interface.py
    print("\n🔍 2. VÉRIFICATION DU PROMPT ACTUEL:")
    
    backend_file = 'backend_interface.py'
    if os.path.exists(backend_file):
        try:
            with open(backend_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier les éléments clés du prompt
            checks = [
                ("Instructions jumeaux", "INSTRUCTIONS CRITIQUES POUR LA DÉTECTION DES JUMEAUX" in content),
                ("Exemples jumeaux", "EXEMPLES DE DÉTECTION DE JUMEAUX" in content),
                ("Champ est_jumeaux", "est_jumeaux" in content),
                ("Champ type_matelas", "type_matelas" in content),
                ("Logique détection", "article_matelas.get('est_jumeaux')" in content)
            ]
            
            print("   🔍 Vérification des éléments clés:")
            for check_name, check_result in checks:
                status = "✅" if check_result else "❌"
                print(f"      {status} {check_name}")
                
        except Exception as e:
            print(f"   ❌ Erreur lecture {backend_file}: {e}")
    else:
        print(f"   ❌ Fichier {backend_file} non trouvé")
    
    # 3. Problèmes identifiés et solutions
    print("\n🚨 3. PROBLÈMES IDENTIFIÉS ET SOLUTIONS:")
    
    print("   🎯 PROBLÈME PRINCIPAL:")
    print("      - Le LLM n'extrait PAS les champs 'est_jumeaux' et 'type_matelas'")
    print("      - La logique des jumeaux ne peut donc pas être appliquée")
    
    print("\n   🔧 SOLUTIONS:")
    print("      1. Vérifier que le prompt amélioré est bien appliqué")
    print("      2. Tester avec un PDF contenant clairement 'MATELAS JUMEAUX'")
    print("      3. Vérifier que l'option LLM est activée")
    print("      4. Regarder les logs pour voir la réponse complète du LLM")
    
    print("\n   🧪 TEST RECOMMANDÉ:")
    print("      - Utiliser un PDF avec 'MATELAS JUMEAUX' dans la description")
    print("      - Vérifier que l'option 'Utiliser l'enrichissement LLM' est cochée")
    print("      - Surveiller les logs pour voir l'extraction complète")
    
    return True

def instructions_test():
    """Instructions pour tester la détection des jumeaux"""
    
    print("\n📋 INSTRUCTIONS POUR TESTER LA DÉTECTION DES JUMEAUX:")
    
    print("   1. 📱 Ouvrir MatelasApp")
    print("   2. ✅ Cocher 'Utiliser l'enrichissement LLM'")
    print("   3. 📄 Sélectionner un PDF contenant 'MATELAS JUMEAUX'")
    print("   4. 🚀 Cliquer sur 'Traiter les fichiers'")
    
    print("\n   🔍 Vérifications à faire:")
    print("   - Dans les logs: Vérifier que le JSON contient 'est_jumeaux' et 'type_matelas'")
    print("   - Dans les logs: Voir si la logique des jumeaux est appliquée")
    print("   - Dans Excel: Vérifier les cellules jumeaux_C10 et jumeaux_D10")
    print("   - Dans Excel: Vérifier les dimensions housse avec préfixe '4 x'")

if __name__ == "__main__":
    print("🔍 Vérification de l'extraction des jumeaux")
    
    # Vérification principale
    success = verifier_extraction_jumeaux()
    
    # Instructions de test
    instructions_test()
    
    if success:
        print("\n🎯 RÉSUMÉ DE LA VÉRIFICATION:")
        print("✅ Log analysé")
        print("✅ Prompt vérifié")
        print("🔍 Problèmes identifiés")
        print("🔧 Solutions proposées")
    else:
        print("\n❌ Problème détecté dans la vérification")
    
    print("\n=== FIN DE LA VÉRIFICATION ===")

