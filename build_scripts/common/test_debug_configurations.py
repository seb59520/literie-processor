#!/usr/bin/env python3
"""
Test de débogage pour comprendre pourquoi seulement 1 configuration est affichée
"""

import sys
import os
import json

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def test_configuration_display():
    """Test pour vérifier l'affichage des configurations"""
    
    print("🔍 Test de débogage des configurations")
    print("=" * 50)
    
    # Simuler les données comme elles seraient dans l'interface
    all_results = []
    all_configurations = []
    
    # Premier fichier (vanacker)
    result1 = {
        'filename': 'Commandes vanacker.pdf',
        'status': 'success',
        'configurations_matelas': [
            {
                'matelas_index': 1,
                'noyau': 'LATEX NATUREL',
                'quantite': 1,
                'dimensions': {'largeur': 89, 'longueur': 198},
                'housse': 'Simple',
                'matiere_housse': 'TENCEL',
                'hauteur': 18,
                'fermete': 'Moyenne'
            }
        ],
        'pre_import': [{'Client_D1': 'VANACKER', 'numero_D2': '2025', 'noyau': 'LATEX NATUREL'}],
        'fichiers_excel': ['output/Matelas_S35_2025_1.xlsx']
    }
    
    # Deuxième fichier (thullier)
    result2 = {
        'filename': 'Commandes thullier.pdf',
        'status': 'success',
        'configurations_matelas': [
            {
                'matelas_index': 1,
                'noyau': 'LATEX NATUREL',
                'quantite': 1,
                'dimensions': {'largeur': 89, 'longueur': 199},
                'housse': 'Simple',
                'matiere_housse': 'TENCEL',
                'hauteur': 18,
                'fermete': 'Moyenne'
            }
        ],
        'pre_import': [{'Client_D1': 'THULLIER', 'numero_D2': '2025', 'noyau': 'LATEX NATUREL'}],
        'fichiers_excel': ['output/Matelas_S35_2025_2.xlsx']
    }
    
    # Simuler l'accumulation comme dans l'interface
    all_results.append(result1)
    all_results.append(result2)
    
    all_configurations.extend(result1.get('configurations_matelas', []))
    all_configurations.extend(result2.get('configurations_matelas', []))
    
    print(f"📊 Nombre de résultats: {len(all_results)}")
    print(f"📊 Nombre de configurations: {len(all_configurations)}")
    print(f"📊 Nombre de fichiers Excel: {len(result1.get('fichiers_excel', [])) + len(result2.get('fichiers_excel', []))}")
    
    print("\n🔍 Détail des configurations:")
    for i, config in enumerate(all_configurations):
        print(f"  Configuration {i+1}:")
        print(f"    - Index: {config.get('matelas_index')}")
        print(f"    - Noyau: {config.get('noyau')}")
        print(f"    - Dimensions: {config.get('dimensions')}")
        print(f"    - Fichier source: {get_source_file(config, all_results)}")
    
    print("\n🔍 Test de la méthode display_configurations:")
    test_display_configurations(all_configurations, all_results)

def get_source_file(config, all_results):
    """Trouve le fichier source d'une configuration (comme dans l'interface)"""
    for result in all_results:
        if config in result.get('configurations_matelas', []):
            return os.path.basename(result.get('filename', 'N/A'))
    return "N/A"

def test_display_configurations(configurations, all_results):
    """Test de la méthode display_configurations"""
    if not configurations:
        print("  ❌ Aucune configuration à afficher")
        return
    
    print(f"  ✅ Affichage de {len(configurations)} configurations:")
    
    for i, config in enumerate(configurations):
        try:
            # Trouver le fichier source
            filename = "N/A"
            for result in all_results:
                if config in result.get('configurations_matelas', []):
                    filename = os.path.basename(result.get('filename', 'N/A'))
                    break
            
            print(f"    Ligne {i+1}: {filename} | {config.get('noyau')} | {config.get('dimensions')}")
            
        except Exception as e:
            print(f"    ❌ Erreur ligne {i+1}: {e}")

if __name__ == "__main__":
    test_configuration_display() 

#!/usr/bin/env python3

import sys
sys.path.append('backend')
import json

# JSON LLM fourni par l'utilisateur
llm_result = """{
  "societe": {
    "nom": "SAS Literie Westelynck",
    "capital": "23 100 Euros",
    "adresse": "525 RD 642 - 59190 BORRE",
    "telephone": "03.28.48.04.19",
    "fax": "03.28.41.02.74",
    "email": "contact@lwest.fr",
    "siret": "429 352 891 00015",
    "APE": "3103Z",
    "CEE": "FR50 429 352 891",
    "banque": "Crédit Agricole d'Hazebrouck",
    "IBAN": "FR76 1670 6050 1650 4613 2602 341"
  },
  "client": {
    "nom": "SCI LA BORDERIE",
    "adresse": "1009 CHEMIN VERT 59670 WINNEZEELE",
    "code_client": "LABORDWIN"
  },
  "commande": {
    "numero": "CM00009544",
    "date": "04/07/2025",
    "date_validite": null,
    "commercial": "P. ALINE",
    "origine": "www.literie-westelynck.fr"
  },
  "articles": [
    {
      "quantite": 1,
      "description": "SOMMIERS JUMEAUX RELAXATION MOTORISÉE 5 PLIS TÉLESCOPIQUE",
      "dimensions": "179/199/19",
      "pu_ttc": 2138.15,
      "eco_part": 13.15,
      "pu_ht": 2125.00
    },
    {
      "quantite": 1,
      "description": "TÉLÉCOMMANDE NOIRE RADIO FRÉQUENCE (x2) + ÉCLAIRAGE TORCHE",
      "montant": 120.00
    },
    {
      "quantite": 1,
      "description": "LOT DE 2 RAMPES 3 PLOTS",
      "montant": 12.00
    },
    {
      "quantite": 2,
      "description": "MATELAS JUMEAUX - LATEX 100% NATUREL PERFORÉ 7 ZONES DIFFÉRENCIÉES FERME - HOUSSE MATELASSÉE TENCEL LUXE 3D LAVABLE A 40°",
      "dimensions": "89/198/22",
      "pu_ttc": 1733.00,
      "eco_part": 5.50,
      "pu_ht": 861.00
    },
    {
      "quantite": 1,
      "description": "JEU DE 8 PIEDS CUBIQUE TEINTÉ WENGÉ 20 CM + PLATINES DE RÉUNION + PATINS FEUTRES (en retrait)",
      "dimensions": null,
      "pu_ttc": 185.44,
      "eco_part": 1.44,
      "pu_ht": 184.00
    },
    {
      "quantite": 1,
      "description": "SOMMIERS JUMEAUX FIXE - DOUBLES LATTES (HÊTRE MULTIPLIS) - STRUCTURE PAREMENTÉE - LATTES A FLEUR 3 COTES",
      "dimensions": "179/199/19",
      "pu_ttc": 694.66,
      "eco_part": 9.66,
      "pu_ht": 685.00
    },
    {
      "quantite": 2.5,
      "description": "MÉTRAGE TISSU CASAL 84015 CANOAS col. 13 COTON",
      "montant": 195.00
    },
    {
      "quantite": 1,
      "description": "BUTÉES LATÉRALES & PIEDS FIXE",
      "montant": 69.00
    },
    {
      "quantite": 1,
      "description": "REMISE : 5% ENLÈVEMENT PAR VOS SOINS (emballage renforcé pour déménagement)",
      "montant": -350.90
    }
  ],
  "paiement": {
    "conditions": "VIREMENT",
    "port_ht": 0.00,
    "base_ht": 5555.90,
    "taux_tva": 20.00,
    "total_ttc": 6714.79,
    "acompte": 1714.79,
    "net_a_payer": 6714.79
  }
}"""

def analyser_probleme_configurations():
    """Analyse pourquoi il n'y a qu'une seule configuration au lieu de deux"""
    
    print("=== ANALYSE DU PROBLÈME DE CONFIGURATIONS ===")
    print()
    
    # Parser le JSON
    try:
        llm_data = json.loads(llm_result)
        articles_llm = llm_data.get('articles', [])
    except Exception as e:
        print(f"❌ Erreur parsing JSON: {e}")
        return
    
    print(f"📊 STATISTIQUES:")
    print(f"   - Articles totaux dans le LLM: {len(articles_llm)}")
    
    # Analyser les articles matelas
    matelas_articles = []
    for i, article in enumerate(articles_llm):
        description = article.get('description', '').upper()
        if 'MATELAS' in description:
            matelas_articles.append(article)
            print(f"   - Article {i+1}: {description[:80]}...")
            print(f"     Quantité: {article.get('quantite', 1)}")
    
    print(f"   - Articles matelas détectés: {len(matelas_articles)}")
    print()
    
    # Simuler la détection des noyaux
    from matelas_utils import detecter_noyau_matelas
    noyaux_matelas = detecter_noyau_matelas(matelas_articles)
    print(f"🔍 DÉTECTION DES NOYAUX:")
    for i, noyau_info in enumerate(noyaux_matelas):
        print(f"   - Noyau {i+1}: {noyau_info['noyau']} (index: {noyau_info['index']})")
    print()
    
    # Simuler la création des configurations
    print(f"⚙️  CRÉATION DES CONFIGURATIONS:")
    configurations = []
    
    for i, noyau_info in enumerate(noyaux_matelas):
        if noyau_info['noyau'] != 'INCONNU':
            # Trouver l'article correspondant
            quantite = 1
            description = ""
            if noyau_info['index'] <= len(matelas_articles):
                article_matelas = matelas_articles[noyau_info['index'] - 1]
                quantite = article_matelas.get('quantite', 1)
                description = article_matelas.get('description', '')
            
            print(f"   - Configuration {len(configurations)+1}:")
            print(f"     Index: {noyau_info['index']}")
            print(f"     Noyau: {noyau_info['noyau']}")
            print(f"     Quantité: {quantite}")
            print(f"     Description: {description[:60]}...")
            
            config = {
                "matelas_index": noyau_info['index'],
                "noyau": noyau_info['noyau'],
                "quantite": quantite,
                "description": description
            }
            configurations.append(config)
    
    print(f"\n📋 RÉSULTAT FINAL:")
    print(f"   - Configurations créées: {len(configurations)}")
    
    if len(configurations) == 1 and configurations[0]['quantite'] == 2:
        print(f"\n⚠️  PROBLÈME IDENTIFIÉ:")
        print(f"   Le LLM a fusionné 2 articles identiques en un seul avec quantité=2")
        print(f"   au lieu de les garder séparés comme demandé dans le prompt.")
        print(f"   Cela explique pourquoi il n'y a qu'une seule configuration.")
        
        print(f"\n💡 SOLUTIONS POSSIBLES:")
        print(f"   1. Améliorer le prompt pour forcer la séparation des articles identiques")
        print(f"   2. Modifier la logique pour créer 2 configurations quand quantité=2")
        print(f"   3. Analyser le texte original pour détecter les doublons")
    
    return configurations

if __name__ == "__main__":
    analyser_probleme_configurations() 