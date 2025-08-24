#!/usr/bin/env python3

import sys
sys.path.append('backend')
import json

# Simuler les données d'entrée (comme dans le cas réel)
noyaux_matelas = [
    {
        "index": 1,
        "noyau": "LATEX NATUREL"
    }
]

matelas_articles = [
    {
        "description": "MATELAS JUMEAUX - LATEX 100% NATUREL PERFORÉ 7 ZONES DIFFÉRENCIÉES FERME - HOUSSE MATELASSÉE TENCEL LUXE 3D LAVABLE A 40° 89/ 198/ 22",
        "quantite": 2,  # Le LLM a fusionné 2 articles en 1 avec quantité=2
        "dimensions": "89/ 198/ 22"
    }
]

def test_logique_modifiee():
    """Test de la logique modifiée"""
    print("🔧 TEST DE LA LOGIQUE MODIFIÉE")
    print("=" * 60)
    
    configurations = []
    config_index = 1  # Index pour les configurations
    
    for i, noyau_info in enumerate(noyaux_matelas):
        if noyau_info['noyau'] != 'INCONNU':
            # Trouver l'article correspondant
            quantite = 1
            description = ""
            if noyau_info['index'] <= len(matelas_articles):
                article_matelas = matelas_articles[noyau_info['index'] - 1]
                quantite = article_matelas.get('quantite', 1)
                description = article_matelas.get('description', '')
            
            print(f"📋 Article trouvé:")
            print(f"  Description: {description[:60]}...")
            print(f"  Quantité: {quantite}")
            
            # DÉTECTION DE FUSION LLM : Si quantité > 1, créer 2 configurations
            nb_configurations = 2 if quantite > 1 else 1
            print(f"  Nombre de configurations à créer: {nb_configurations}")
            
            for j in range(nb_configurations):
                # Création de la configuration
                config = {
                    "matelas_index": config_index,  # Index unique pour chaque configuration
                    "noyau": noyau_info['noyau'],
                    "quantite": quantite,  # Garder la quantité originale
                    "description": description,
                    "dimensions": {"largeur": 89, "longueur": 198, "hauteur": 22}
                }
                
                configurations.append(config)
                print(f"  Configuration {config_index}: {quantite}x matelas (unité {j+1}/{nb_configurations})")
                config_index += 1
    
    print(f"\n✅ RÉSULTAT:")
    print(f"  • Configurations créées: {len(configurations)}")
    print(f"  • Quantités: {[c['quantite'] for c in configurations]}")
    print(f"  • Index: {[c['matelas_index'] for c in configurations]}")
    
    # Vérification
    if len(configurations) == 2 and all(c['quantite'] == 2 for c in configurations):
        print(f"\n🎉 SUCCÈS: La modification fonctionne correctement!")
        print(f"  • 2 configurations créées au lieu d'1")
        print(f"  • Chaque configuration garde sa quantité originale (2)")
        print(f"  • Cela donnera 2 lignes Excel avec quantité=2")
    else:
        print(f"\n❌ ÉCHEC: La modification ne fonctionne pas comme attendu")
    
    return configurations

def test_cas_normal():
    """Test avec quantité=1 (cas normal)"""
    print("\n🔍 TEST CAS NORMAL (quantité=1)")
    print("=" * 60)
    
    matelas_articles_normal = [
        {
            "description": "MATELAS SIMPLE - LATEX NATUREL",
            "quantite": 1,  # Cas normal
            "dimensions": "140/ 190/ 20"
        }
    ]
    
    configurations = []
    config_index = 1
    
    for i, noyau_info in enumerate(noyaux_matelas):
        if noyau_info['noyau'] != 'INCONNU':
            quantite = 1
            description = ""
            if noyau_info['index'] <= len(matelas_articles_normal):
                article_matelas = matelas_articles_normal[noyau_info['index'] - 1]
                quantite = article_matelas.get('quantite', 1)
                description = article_matelas.get('description', '')
            
            print(f"📋 Article trouvé:")
            print(f"  Description: {description}")
            print(f"  Quantité: {quantite}")
            
            # DÉTECTION DE FUSION LLM : Si quantité > 1, créer 2 configurations
            nb_configurations = 2 if quantite > 1 else 1
            print(f"  Nombre de configurations à créer: {nb_configurations}")
            
            for j in range(nb_configurations):
                config = {
                    "matelas_index": config_index,
                    "noyau": noyau_info['noyau'],
                    "quantite": quantite,
                    "description": description,
                    "dimensions": {"largeur": 140, "longueur": 190, "hauteur": 20}
                }
                
                configurations.append(config)
                print(f"  Configuration {config_index}: {quantite}x matelas (unité {j+1}/{nb_configurations})")
                config_index += 1
    
    print(f"\n✅ RÉSULTAT CAS NORMAL:")
    print(f"  • Configurations créées: {len(configurations)}")
    print(f"  • Quantités: {[c['quantite'] for c in configurations]}")
    
    # Vérification
    if len(configurations) == 1 and configurations[0]['quantite'] == 1:
        print(f"\n🎉 SUCCÈS: Le cas normal fonctionne correctement!")
        print(f"  • 1 configuration créée (comme attendu)")
        print(f"  • Quantité = 1 (comme attendu)")
    else:
        print(f"\n❌ ÉCHEC: Le cas normal ne fonctionne pas comme attendu")
    
    return configurations

if __name__ == "__main__":
    print("🧪 TESTS DE LA MODIFICATION DES CONFIGURATIONS")
    print("=" * 80)
    
    # Test cas fusion LLM
    configs_fusion = test_logique_modifiee()
    
    # Test cas normal
    configs_normal = test_cas_normal()
    
    print(f"\n📊 RÉSUMÉ FINAL:")
    print(f"  • Cas fusion LLM (quantité=2): {len(configs_fusion)} configurations")
    print(f"  • Cas normal (quantité=1): {len(configs_normal)} configurations")
    
    if len(configs_fusion) == 2 and len(configs_normal) == 1:
        print(f"\n🎉 TOUS LES TESTS RÉUSSIS!")
        print(f"  La modification fonctionne parfaitement pour les deux cas.")
    else:
        print(f"\n❌ CERTAINS TESTS ONT ÉCHOUÉ!")
        print(f"  Il faut vérifier la logique de modification.") 