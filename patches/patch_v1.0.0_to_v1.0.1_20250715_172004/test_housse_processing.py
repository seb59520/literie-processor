#!/usr/bin/env python3
"""
Test du calcul de largeur de housse avec les tables de correspondance
"""

import sys
import os
import json
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from main import apply_housse_tables, normalize_text, decode_unicode_strings

def test_housse_calculation():
    """Test du calcul de largeur de housse"""
    
    # Charger les données de test
    with open('test_housse.json', 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    # Décoder les caractères Unicode
    test_data = decode_unicode_strings(test_data)
    
    print("=== Test du calcul de largeur de housse ===")
    print(f"Données de test chargées: {len(test_data.get('Matelas', []))} matelas")
    
    # Simuler le processus de traitement
    matelas = test_data.get("Matelas", [])
    if not matelas:
        print("❌ Aucun matelas trouvé dans les données de test")
        return
    
    # Créer des articles structurés comme dans le système
    articles = []
    for idx, matelas_data in enumerate(matelas):
        article = {
            "categorie": "Matelas",
            "description": matelas_data.get("description", ""),
            "quantité": matelas_data.get("quantité", 1),
            "dimension_housse": matelas_data.get("dimension_housse", ""),
            "nom_client": test_data.get("Client", {}).get("nom", ""),
            "adresse_client": test_data.get("Client", {}).get("adresse", ""),
            "type_noyau": "INCONNU",  # Sera détecté par le système
            "matiere_housse": "TENCEL LUXE 3D",  # Extrait de la description
            "matelas_jumeaux": False,
            "alerte": ""
        }
        articles.append(article)
    
    print(f"Articles créés: {len(articles)}")
    
    # Détecter le type de noyau et la matière
    for article in articles:
        desc = normalize_text(article["description"])
        
        # Détection du type de noyau
        if "rainure" in desc or "rainurée" in desc or "rainuré" in desc:
            article["type_noyau"] = "RAINURÉ"
        elif "latex" in desc:
            if "naturel" in desc:
                article["type_noyau"] = "LATEX NATUREL"
            else:
                article["type_noyau"] = "LATEX MIXTE"
        elif "visco" in desc:
            article["type_noyau"] = "VISCO"
        
        # Détection de la matière housse
        if "tencel luxe 3d" in desc:
            article["matiere_housse"] = "TENCEL LUXE 3D"
        elif "tencel" in desc:
            article["matiere_housse"] = "TENCEL"
        elif "polyester" in desc:
            article["matiere_housse"] = "POLYESTER"
        
        print(f"Article: {article['description'][:50]}...")
        print(f"  - Type noyau: {article['type_noyau']}")
        print(f"  - Matière housse: {article['matiere_housse']}")
        print(f"  - Dimension housse: {article['dimension_housse']}")
    
    # Appliquer les tables de correspondance
    print("\n=== Application des tables de correspondance ===")
    results = apply_housse_tables(articles)
    
    # Afficher les résultats
    print("\n=== Résultats ===")
    for i, result in enumerate(results, 1):
        print(f"\nMatelas {i}:")
        print(f"  - Description: {result['description'][:60]}...")
        print(f"  - Type noyau: {result['type_noyau']}")
        print(f"  - Matière housse: {result['matiere_housse']}")
        print(f"  - Dimension housse: {result['dimension_housse']}")
        print(f"  - Dimension housse calculée: {result.get('dimension_housse_cm', 'N/A')}")
        if result.get('alerte'):
            print(f"  - Alerte: {result['alerte']}")
    
    print("\n=== Test terminé ===")

if __name__ == "__main__":
    test_housse_calculation() 