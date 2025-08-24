#!/usr/bin/env python3
import json
import re
import math
import unicodedata

def normalize_text(text: str) -> str:
    """Normalise un texte (supprime accents, minuscules)"""
    if not text:
        return ""
    # Normalisation Unicode et suppression des accents
    normalized = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('ascii')
    return normalized.lower()

def clean_dimension_housse(dim_str) -> str:
    """Nettoie et standardise le format des dimensions housse"""
    if not dim_str:
        return ""
    
    # Convertir en string si ce n'est pas déjà le cas
    dim_str = str(dim_str)
    
    # Supprime les espaces multiples et nettoie
    cleaned = re.sub(r'\s+', ' ', dim_str.strip())
    
    # Convertit les formats avec slash en format standard
    # "139/ 189/ 20" -> "139 x 189"
    match = re.search(r'(\d{2,4})\s*\/\s*(\d{2,4})', cleaned)
    if match:
        return f"{match[1]} x {match[2]}"
    
    return cleaned

def safe_int(value) -> int:
    """Convertit une valeur en entier de manière sécurisée"""
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        # Essayer de parser comme float d'abord, puis convertir en int
        try:
            return int(float(value.replace(',', '.')))
        except (ValueError, TypeError):
            return 0
    return 0

def apply_housse_tables(results: list) -> list:
    """Applique les tables de correspondance pour calculer dimension_housse_cm"""
    print("Application des tables de correspondance housse")
    
    # Création des 4 tables de correspondance (60 à 243)
    table1 = {"LUXE 3 D": {}, "TENCEL S": {}, "POLY S": {}}  # LATEX NATUREL
    table2 = {"LUXE 3 D": {}, "TENCEL S": {}, "POLY S": {}}  # LATEX MIXTE, PERFORE, RAINURE
    table3 = {"LUXE 3 D": {}, "TENCEL S": {}, "POLY S": {}}  # SELECT 43 / CENTRE RENFORCÉ
    table4 = {"LUXE 3 D": {}, "TENCEL S": {}, "POLY S": {}}  # VISCO / MÉMOIRE DE FORME
    
    # Remplissage des tables
    for i in range(60, 244):
        table1["LUXE 3 D"][i] = 74 + (i - 60)
        table1["TENCEL S"][i] = 80 + (i - 60)
        table1["POLY S"][i] = 152 + 2 * (i - 60)
        
        table2["LUXE 3 D"][i] = 72 + (i - 60)
        table2["TENCEL S"][i] = 78 + (i - 60)
        table2["POLY S"][i] = 149 + 2 * (i - 60)
        
        table3["LUXE 3 D"][i] = 70 + (i - 60)
        table3["TENCEL S"][i] = 76 + (i - 60)
        table3["POLY S"][i] = 145 + 2 * (i - 60)
        
        table4["LUXE 3 D"][i] = 70 + (i - 60)
        table4["TENCEL S"][i] = 76 + (i - 60)
        table4["POLY S"][i] = 145 + 2 * (i - 60)
    
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

def process_ensemble_1(articles: list) -> list:
    """Traitement spécifique pour l'ensemble 1 (SuperCategorie1 + SuperCategorie1_&_2)"""
    print(f"Traitement ensemble 1: {len(articles)} articles")
    
    if not articles:
        print("Aucun article dans l'ensemble 1")
        return []
    
    # Séparation des articles par catégorie
    matelas = [a for a in articles if normalize_text(a.get("categorie", "")) == "matelas"]
    housses = [a for a in articles if normalize_text(a.get("categorie", "")) == "housse"]
    autres = [a for a in articles if normalize_text(a.get("categorie", "")) == "autres"]
    
    print(f"Matelas trouvés: {len(matelas)}, Housses trouvées: {len(housses)}, Autres trouvés: {len(autres)}")
    
    # Infos client (depuis le premier article)
    client_nom = articles[0].get("nom_client") if articles else None
    client_adresse = articles[0].get("adresse_client") if articles else None
    
    # Mode de mise à disposition
    mode_mise_dispo = matelas[0].get("mode_mise_a_disposition") if matelas else None
    
    # Vérification du mode dans les articles "Autres"
    for item in autres:
        desc = normalize_text(item.get("description", ""))
        if "livraison" in desc:
            mode_mise_dispo = "LIVRAISON"
            break
        elif "enlevement" in desc or "enlèvement" in desc:
            mode_mise_dispo = "ENLÈVEMENT"
            break
        elif "envoi" in desc or "expedition" in desc:
            mode_mise_dispo = "EXPÉDITION"
            break
    
    # Présence d'un surmatelas
    has_surmatelas = any("surmatelas" in normalize_text(item.get("description", "")) for item in autres)
    
    # Tête ou Dosseret
    tete_dosseret = "N/A"
    tete_description = "N/A"
    dosseret_description = "N/A"
    
    for item in autres:
        desc = normalize_text(item.get("description", ""))
        if "tete" in desc:
            tete_dosseret = "TÊTE"
            tete_description = item.get("description", "")
        if "dosseret" in desc:
            tete_dosseret = "DOSSERET"
            dosseret_description = item.get("description", "")
    
    results = []
    index = 1
    
    # Traitement des matelas
    for item in matelas:
        desc = normalize_text(item.get("description", ""))
        qty = item.get("quantité", 1)
        alertes = []
        
        # Utiliser dimension_projet_cm du matelas si existant
        dimension = item.get("dimension_projet_cm")
        
        if not dimension:
            # Extraction des dimensions depuis dimension_housse (format: "139/ 189/ 20" ou "139 x 189")
            dim_housse = item.get("dimension_housse", "") or ""
            if dim_housse:
                dim_match = re.search(r'(\d{2,3})\s*[\/xX]\s*(\d{2,3})', str(dim_housse))
                if dim_match:
                    largeur = round(int(dim_match[1]) / 10) * 10
                    longueur = round(int(dim_match[2]) / 10) * 10
                    dimension = f"{largeur} x {longueur}"
                    print(f"Dimensions extraites: {largeur} x {longueur} depuis '{dim_housse}'")
                else:
                    alertes.append("⚠️ Dimensions non trouvées dans dimension_housse ou description.")
                    continue
            else:
                alertes.append("⚠️ Dimension housse manquante.")
                continue
        
        # Type de noyau
        type_noyau = "INCONNU"
        if "select 43" in desc or "select43" in desc:
            type_noyau = "SELECT 43"
        elif "rainure" in desc:
            type_noyau = "RAINURÉ"
        elif "latex" in desc:
            if "naturel" in desc:
                type_noyau = "LATEX NATUREL"
            elif any(x in desc for x in ["latex 100", "100 latex", "100% latex", "perfore", "perforé", "7 zones"]):
                type_noyau = "LATEX MIXTE 7 ZONES"
            else:
                type_noyau = "LATEX MIXTE"
        elif "visco" in desc:
            type_noyau = "VISCO"
        elif "bebe mousse" in desc:
            type_noyau = "BÉBÉ MOUSSE"
        elif "bebe latex" in desc:
            type_noyau = "BÉBÉ LATEX"
        else:
            alertes.append("⚠️ Type de noyau non identifié.")
        
        # Fermeté
        fermete = "INCONNUE"
        if "ferme" in desc:
            fermete = "FERME"
        elif "medium" in desc:
            fermete = "MEDIUM"
        elif "confort" in desc:
            fermete = "CONFORT"
        else:
            alertes.append("⚠️ Fermeté non identifiée.")
        
        # Hauteur
        hauteur_cm = None
        if type_noyau == "VISCO" or type_noyau == "LATEX NATUREL":
            hauteur_cm = 10
        elif type_noyau in ["RAINURÉ", "MIXTE", "LATEX MIXTE 7 ZONES"]:
            hauteur_cm = 9
        elif type_noyau == "SELECT 43" or "latex 3 zones" in desc:
            hauteur_cm = 8
        else:
            alertes.append("⚠️ Hauteur non identifiable depuis la description.")
        
        # Type de housse
        type_housse = "INCONNU"
        matiere_housse = "INCONNUE"
        housse_poignees = False
        
        if "matelassee" in desc:
            type_housse = "MATELASSEE"
        elif "housse" in desc:
            type_housse = "SIMPLE"
        else:
            alertes.append("⚠️ Type de housse non détecté dans la description.")
        
        if "poignee" in desc or "poignees" in desc:
            housse_poignees = True
        
        if "tencel luxe 3d" in desc:
            matiere_housse = "TENCEL LUXE 3D"
        elif "tencel" in desc:
            matiere_housse = "TENCEL"
        elif "polyester" in desc:
            matiere_housse = "POLYESTER"
        else:
            alertes.append("⚠️ Matière de la housse non détectée.")
        
        # Jumeaux ou 1 pièce
        matelas_jumeaux = "matelas jumeaux" in desc
        jumeau_one = "Jumeaux" if matelas_jumeaux else "1 pièce"
        
        # Conversion sécurisée de la quantité
        qty_int = safe_int(qty)
        should_split = not (matelas_jumeaux and qty_int == 2)
        loops = qty_int if should_split else 1
        
        # Détection Commande Spéciale
        special_pattern = r'matelas\s*en\s*forme|en\s*forme|1\s*\/\s*2\s*corbeille'
        is_commande_speciale = any(
            re.search(special_pattern, normalize_text(m.get("description", "")), re.IGNORECASE)
            for m in matelas
        )
        
        # Extraction des dimensions jumeaux
        dim_jumeaux = None
        dim_source = item.get("dimension_projet") or item.get("dimension_brute")
        if dim_source:
            match = re.search(r'(\d{2,4})\s*[xX/]\s*(\d{2,4})', dim_source)
            if match:
                val1 = math.ceil(int(match[1]) / 10) * 10
                val2 = math.ceil(int(match[2]) / 10) * 10
                dim_jumeaux = f"{val1} x {val2}"
        
        # Création des résultats
        for i in range(loops):
            # Nettoyage de la dimension housse
            dimension_housse_clean = clean_dimension_housse(item.get("dimension_housse", ""))
            
            result = {
                "Configuration": f"Configuration matelas {index}",
                "dimensions_cm": dimension,
                "dimension_housse": dimension_housse_clean,
                "dimension_projet_cm": dimension,
                "dimension_jumeaux_cm": dim_jumeaux,
                "dimension_1piece_cm": dim_jumeaux,
                "quantité": qty_int,
                "poignees": housse_poignees,
                "type_housse": type_housse,
                "matiere_housse": matiere_housse,
                "type_noyau": type_noyau,
                "fermete": fermete,
                "hauteur_cm": hauteur_cm,
                "surmatelas": has_surmatelas,
                "mode_mise_a_disposition": mode_mise_dispo,
                "nom_client": client_nom,
                "adresse_client": client_adresse,
                "TETE_DOSSERET": tete_dosseret,
                "TETE_DESCRIPTION": tete_description,
                "DOSSERET_DESCRIPTION": dosseret_description,
                "jumeau_One": jumeau_one,
                "alerte": " | ".join(alertes) if alertes else None,
                "matelas_jumeaux": matelas_jumeaux,
                "dimension_housse_cm": None  # Sera calculé par apply_housse_tables
            }
            
            results.append(result)
            index += 1
    
    # Traitement des housses séparées
    for item in housses:
        desc = normalize_text(item.get("description", ""))
        qty = item.get("quantité", 1)
        alertes = []
        
        # Type de housse
        type_housse = "INCONNU"
        if "matelassee" in desc:
            type_housse = "MATELASSEE"
        elif "housse" in desc:
            type_housse = "SIMPLE"
        else:
            alertes.append("⚠️ Type de housse non détecté dans la description.")
        
        # Matière de housse
        matiere_housse = "INCONNUE"
        if "tencel luxe 3d" in desc:
            matiere_housse = "TENCEL LUXE 3D"
        elif "tencel" in desc:
            matiere_housse = "TENCEL"
        elif "polyester" in desc:
            matiere_housse = "POLYESTER"
        else:
            alertes.append("⚠️ Matière de la housse non détectée.")
        
        # Poignées
        housse_poignees = "poignee" in desc or "poignees" in desc
        
        # Extraction des dimensions housse
        dimension_housse = item.get("dimension_housse", "")
        if not dimension_housse:
            # Essayer d'extraire depuis la description
            dim_match = re.search(r'(\d{2,3})\s*[\/xX]\s*(\d{2,3})', desc)
            if dim_match:
                dimension_housse = f"{dim_match[1]} x {dim_match[2]}"
                print(f"Dimension housse extraite depuis description: {dimension_housse}")
            else:
                alertes.append("⚠️ Dimension housse non trouvée.")
        
        # Nettoyage de la dimension housse
        dimension_housse_clean = clean_dimension_housse(dimension_housse)
        
        # Conversion sécurisée de la quantité
        qty_int = safe_int(qty)
        
        result = {
            "Configuration": f"Configuration housse {index}",
            "dimensions_cm": None,  # Pas de dimension projet pour les housses
            "dimension_housse": dimension_housse_clean,
            "dimension_projet_cm": None,
            "dimension_jumeaux_cm": None,
            "dimension_1piece_cm": None,
            "quantité": qty_int,
            "poignees": housse_poignees,
            "type_housse": type_housse,
            "matiere_housse": matiere_housse,
            "type_noyau": "N/A",  # Pas de noyau pour les housses
            "fermete": "N/A",     # Pas de fermeté pour les housses
            "hauteur_cm": None,   # Pas de hauteur pour les housses
            "surmatelas": has_surmatelas,
            "mode_mise_a_disposition": mode_mise_dispo,
            "nom_client": client_nom,
            "adresse_client": client_adresse,
            "TETE_DOSSERET": tete_dosseret,
            "TETE_DESCRIPTION": tete_description,
            "DOSSERET_DESCRIPTION": dosseret_description,
            "jumeau_One": "N/A",  # Pas de jumeaux pour les housses
            "alerte": " | ".join(alertes) if alertes else None,
            "matelas_jumeaux": False,  # Pas de jumeaux pour les housses
            "dimension_housse_cm": None  # Sera calculé par apply_housse_tables
        }
        
        results.append(result)
        index += 1
    
    print(f"Traitement ensemble 1 terminé: {len(results)} résultats")
    
    # Application des tables de correspondance pour dimension_housse_cm
    results = apply_housse_tables(results)
    
    return results

def test_housse_processing():
    """Test du traitement des housses"""
    print("🧪 Test du traitement des housses...")
    
    # Créer des données de test directement
    test_articles = [
        {
            "categorie": "Matelas",
            "description": "MATELAS LATEX 100% NATUREL - TENCEL LUXE 3D MATELASSEE",
            "quantité": 1,
            "dimension_housse": "139 x 189",
            "nom_client": "Mr et Me YVOZ DAVID ET MARIE-PIERRE",
            "adresse_client": "1780 CHEMIN DE ZERMEZEELE, 59470 WORMHOUT"
        },
        {
            "categorie": "Housse",
            "description": "HOUSSE TENCEL LUXE 3D MATELASSEE AVEC POIGNEES 139/189",
            "quantité": 1,
            "nom_client": "Mr et Me YVOZ DAVID ET MARIE-PIERRE",
            "adresse_client": "1780 CHEMIN DE ZERMEZEELE, 59470 WORMHOUT"
        },
        {
            "categorie": "Autres",
            "description": "Livraison à domicile",
            "quantité": 1,
            "nom_client": "Mr et Me YVOZ DAVID ET MARIE-PIERRE",
            "adresse_client": "1780 CHEMIN DE ZERMEZEELE, 59470 WORMHOUT"
        }
    ]
    
    print("📋 Données de test créées:")
    print(f"  - Articles: {len(test_articles)}")
    
    # Traitement direct
    print("\n⚙️ Traitement des articles...")
    results = process_ensemble_1(test_articles)
    
    print(f"\n📊 Résultats ({len(results)} articles):")
    
    for i, result in enumerate(results, 1):
        print(f"\n  Article {i}:")
        print(f"    Configuration: {result.get('Configuration', 'N/A')}")
        print(f"    Type housse: {result.get('type_housse', 'N/A')}")
        print(f"    Matière housse: {result.get('matiere_housse', 'N/A')}")
        print(f"    Poignées: {result.get('poignees', 'N/A')}")
        print(f"    Dimension housse: {result.get('dimension_housse', 'N/A')}")
        print(f"    Dimension housse cm: {result.get('dimension_housse_cm', 'N/A')}")
        print(f"    Dimension jumeaux cm: {result.get('dimension_jumeaux_cm', 'N/A')}")
        print(f"    Dimension 1 piece cm: {result.get('dimension_1piece_cm', 'N/A')}")
        print(f"    Alerte: {result.get('alerte', 'Aucune')}")
    
    # Vérifications spécifiques
    print("\n✅ Vérifications:")
    
    # Vérifier qu'on a bien traité les housses
    housses_traitees = [r for r in results if 'housse' in r.get('Configuration', '').lower()]
    print(f"  - Housses traitées: {len(housses_traitees)}")
    
    # Vérifier les caractéristiques des housses
    for housse in housses_traitees:
        if housse.get('type_housse') != 'INCONNU':
            print(f"  ✅ Type de housse détecté: {housse['type_housse']}")
        else:
            print(f"  ❌ Type de housse non détecté")
            
        if housse.get('matiere_housse') != 'INCONNUE':
            print(f"  ✅ Matière de housse détectée: {housse['matiere_housse']}")
        else:
            print(f"  ❌ Matière de housse non détectée")
            
        if housse.get('dimension_housse_cm'):
            print(f"  ✅ Dimension housse calculée: {housse['dimension_housse_cm']}")
        else:
            print(f"  ❌ Dimension housse non calculée")
    
    print("\n🎯 Test terminé!")

if __name__ == "__main__":
    test_housse_processing() 