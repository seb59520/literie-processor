#!/usr/bin/env python3
"""
Test simplifié du calcul de largeur de housse avec les tables de correspondance
"""

import re
import unicodedata
import json

def normalize_text(text: str) -> str:
    """Normalise un texte (supprime accents, minuscules)"""
    if not text:
        return ""
    # D'abord décoder les caractères Unicode
    text = decode_unicode_strings(text)
    # Puis normalisation Unicode et suppression des accents
    normalized = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('ascii')
    return normalized.lower()

def decode_unicode_strings(obj):
    """Décode récursivement tous les encodages unicode, même doubles, dans un objet."""
    if isinstance(obj, str):
        s = obj
        # Tentative de décodage multiple pour corriger l'encodage double
        for _ in range(5):  # Augmenté à 5 tentatives
            try:
                # D'abord, essayer de décoder les séquences unicode
                s_new = s.encode('latin-1').decode('utf-8')
                if s_new == s:
                    # Si pas de changement, essayer unicode_escape
                    s_new = s.encode('utf-8').decode('unicode_escape')
                    if s_new == s:
                        break
                s = s_new
            except Exception:
                try:
                    # Fallback: essayer directement unicode_escape
                    s_new = s.encode('utf-8').decode('unicode_escape')
                    if s_new == s:
                        break
                    s = s_new
                except Exception:
                    break
        return s
    elif isinstance(obj, dict):
        return {key: decode_unicode_strings(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [decode_unicode_strings(item) for item in obj]
    else:
        return obj

def apply_housse_tables(results: list) -> list:
    """Applique les tables de correspondance pour calculer dimension_housse_cm"""
    print("Application des tables de correspondance housse")
    
    # Création des 4 tables de correspondance (étendues pour gérer plus de cas)
    table1 = {"LUXE 3 D": {}, "TENCEL S": {}, "POLY S": {}}  # LATEX NATUREL
    table2 = {"LUXE 3 D": {}, "TENCEL S": {}, "POLY S": {}}  # LATEX MIXTE, PERFORE, RAINURE
    table3 = {"LUXE 3 D": {}, "TENCEL S": {}, "POLY S": {}}  # SELECT 43 / CENTRE RENFORCÉ
    table4 = {"LUXE 3 D": {}, "TENCEL S": {}, "POLY S": {}}  # VISCO / MÉMOIRE DE FORME
    
    # Remplissage des tables (étendu de 50 à 300 pour couvrir plus de cas)
    for i in range(50, 301):
        table1["LUXE 3 D"][i] = 74 + (i - 60) if i >= 60 else 74 - (60 - i)
        table1["TENCEL S"][i] = 80 + (i - 60) if i >= 60 else 80 - (60 - i)
        table1["POLY S"][i] = 152 + 2 * (i - 60) if i >= 60 else 152 - 2 * (60 - i)
        
        table2["LUXE 3 D"][i] = 72 + (i - 60) if i >= 60 else 72 - (60 - i)
        table2["TENCEL S"][i] = 78 + (i - 60) if i >= 60 else 78 - (60 - i)
        table2["POLY S"][i] = 149 + 2 * (i - 60) if i >= 60 else 149 - 2 * (60 - i)
        
        table3["LUXE 3 D"][i] = 70 + (i - 60) if i >= 60 else 70 - (60 - i)
        table3["TENCEL S"][i] = 76 + (i - 60) if i >= 60 else 76 - (60 - i)
        table3["POLY S"][i] = 145 + 2 * (i - 60) if i >= 60 else 145 - 2 * (60 - i)
        
        table4["LUXE 3 D"][i] = 70 + (i - 60) if i >= 60 else 70 - (60 - i)
        table4["TENCEL S"][i] = 76 + (i - 60) if i >= 60 else 76 - (60 - i)
        table4["POLY S"][i] = 145 + 2 * (i - 60) if i >= 60 else 145 - 2 * (60 - i)
    
    processed_results = []
    
    for item in results:
        t_noyau = normalize_text(item.get("type_noyau", "")).upper()
        matiere = normalize_text(item.get("matiere_housse", "")).upper()
        dim_str = item.get("dimension_housse", "") or ""
        largeur = None
        
        # Extraction de la largeur (accepte les valeurs décimales et formats avec slash)
        if dim_str:
            match = re.search(r'^(\d{2,4}(?:[.,]\d+)?)', str(dim_str))
            if match:
                largeur = round(float(match[1].replace(',', '.')))
                print(f"Largeur extraite: {largeur} depuis '{dim_str}'")
        
        # Sélection de la table selon le type de noyau
        table = None
        if t_noyau == "LATEX NATUREL":
            table = table1
        elif t_noyau in ["LATEX MIXTE", "RAINURE", "RAINURÉ", "PERFORE", "PERFORÉ"]:
            table = table2
        elif t_noyau in ["SELECT 43", "LATEX CENTRE RENFORCE", "LATEX CENTRE RENFORCÉ"]:
            table = table3
        elif t_noyau in ["VISCO", "VISCO ELASTIQUE", "MEMOIRE DE FORME", "MÉMOIRE DE FORME"]:
            table = table4
        
        # Sélection de la colonne selon la matière
        colonne = None
        if matiere == "TENCEL LUXE 3D":
            colonne = "LUXE 3 D"
        elif matiere == "TENCEL":
            colonne = "TENCEL S"
        elif matiere == "POLYESTER":
            colonne = "POLY S"
        
        # Calcul de dimension_housse_cm
        dimension_housse_cm = None
        alerte = item.get("alerte")
        
        if table and colonne and largeur and table[colonne].get(largeur):
            val = table[colonne][largeur]
            is_jumeaux = item.get("matelas_jumeaux", False)
            multiplicateur = 2 if matiere.startswith("TENCEL") else 1
            final_multiplier = multiplicateur * 2 if is_jumeaux else multiplicateur
            
            if final_multiplier > 1:
                dimension_housse_cm = f"{final_multiplier} X {val}"
            else:
                dimension_housse_cm = str(val)
                
            print(f"Dimension housse calculée: {dimension_housse_cm} (largeur: {largeur}, table: {t_noyau}, matière: {matiere})")
        else:
            if not alerte:
                alerte = "⚠️ Dimension housse non trouvée pour ce cas."
            else:
                alerte += " | ⚠️ Dimension housse non trouvée pour ce cas."
        
        # Mise à jour du résultat
        processed_item = item.copy()
        processed_item["dimension_housse_cm"] = dimension_housse_cm
        if alerte:
            processed_item["alerte"] = alerte
        
        processed_results.append(processed_item)
    
    return processed_results

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