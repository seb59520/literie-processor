import unicodedata
import re

def normalize_str(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s or '')
        if unicodedata.category(c) != 'Mn'
    ).upper()

TYPES_SOMMIER = [
    "SOMMIER À LATTES",
    "SOMMIER TAPISSIER",
    "SOMMIER BOIS MASSIF",
    "SOMMIER MÉTALLIQUE",
    "SOMMIER À RESSORTS",
    "SOMMIER PLAT"
]

def detecter_type_sommier(sommier_articles):
    """
    Pour chaque sommier, retourne le type détecté (ou INCONNU).
    Retourne une liste de dicts {index, type_sommier}
    """
    result = []
    for idx, article in enumerate(sommier_articles, 1):
        desc = normalize_str(article.get('description', '')) + ' ' + normalize_str(article.get('nom', ''))
        type_sommier = "INCONNU"
        
        # Détection des types de sommier
        if "LATTES" in desc:
            type_sommier = "SOMMIER À LATTES"
        elif "TAPISSIER" in desc:
            type_sommier = "SOMMIER TAPISSIER"
        elif "BOIS MASSIF" in desc or "MASSIF" in desc:
            type_sommier = "SOMMIER BOIS MASSIF"
        elif "MÉTALLIQUE" in desc or "METALLIQUE" in desc:
            type_sommier = "SOMMIER MÉTALLIQUE"
        elif "RESSORTS" in desc:
            type_sommier = "SOMMIER À RESSORTS"
        elif "PLAT" in desc:
            type_sommier = "SOMMIER PLAT"
        else:
            # Détection standard
            for type_sommier_candidate in TYPES_SOMMIER:
                if type_sommier_candidate in desc:
                    type_sommier = type_sommier_candidate
                    break
        
        result.append({"index": idx, "type_sommier": type_sommier})
    return result

def calculer_hauteur_sommier(type_sommier):
    """
    Calcule la hauteur standard d'un sommier selon son type
    """
    hauteurs = {
        "SOMMIER À LATTES": 8,
        "SOMMIER TAPISSIER": 12,
        "SOMMIER BOIS MASSIF": 15,
        "SOMMIER MÉTALLIQUE": 10,
        "SOMMIER À RESSORTS": 14,
        "SOMMIER PLAT": 6,
        "INCONNU": 10
    }
    return hauteurs.get(type_sommier, 10)

def detecter_materiau_sommier(description):
    """
    Détecte le matériau principal du sommier
    """
    desc = normalize_str(description)
    
    if "BOIS" in desc or "MASSIF" in desc:
        return "BOIS"
    elif "MÉTAL" in desc or "METAL" in desc or "ACIER" in desc:
        return "MÉTAL"
    elif "TAPISSIER" in desc or "TISSU" in desc:
        return "TAPISSIER"
    elif "LATTES" in desc:
        return "LATTES"
    else:
        return "STANDARD"

def detecter_type_relaxation_sommier(description):
    """
    Détecte si le sommier est de type RELAXATION ou FIXE
    Retourne 'RELAXATION' si le mot 'relaxation' est trouvé (insensible à la casse),
    sinon retourne 'FIXE'
    """
    desc = normalize_str(description)
    
    # Recherche du mot 'relaxation' (insensible à la casse grâce à normalize_str)
    if "RELAXATION" in desc:
        return "RELAXATION"
    else:
        return "FIXE"

def detecter_type_telecommande_sommier(description):
    """
    Détecte le type de télécommande du sommier
    Retourne :
    - 'NON' si aucune télécommande n'est mentionnée ou si la description contient explicitement 'SANS TELECOMMANDE', 'PAS DE TELECOMMANDE', 'NON TELECOMMANDE'
    - 'TELECOMMANDE FILAIRE' si télécommande mais pas radio
    - 'TELECOMMANDE SANS FIL' si télécommande et radio
    """
    desc = normalize_str(description)
    
    # Cas explicite d'absence de télécommande
    if (
        "SANS TELECOMMANDE" in desc
        or "PAS DE TELECOMMANDE" in desc
        or "NON TELECOMMANDE" in desc
    ):
        return "NON"
    
    # Recherche des mots clés (après normalisation qui supprime les accents)
    has_telecommande = "TELECOMMANDE" in desc or "TELECOMMANDES" in desc
    
    # Recherche plus précise de "RADIO" pour éviter les faux positifs
    # On cherche "RADIO" mais pas dans des contextes comme "SANS RADIO"
    has_radio = False
    if "RADIO" in desc:
        # Vérifier que "RADIO" n'est pas précédé de "SANS" ou "PAS"
        words = desc.split()
        for i, word in enumerate(words):
            if word == "RADIO":
                # Vérifier le mot précédent
                if i > 0 and words[i-1] not in ["SANS", "PAS", "NON"]:
                    has_radio = True
                    break
                # Si c'est le premier mot, c'est OK
                elif i == 0:
                    has_radio = True
                    break
    
    if not has_telecommande:
        return "NON"
    elif has_telecommande and has_radio:
        return "TELECOMMANDE SANS FIL"
    else:  # has_telecommande and not has_radio
        return "TELECOMMANDE FILAIRE"

def detecter_soufflet_mousse_sommier(description):
    """
    Détecte si le sommier a un soufflet mousse
    Retourne 'OUI' si 'soufflet mousse' est trouvé (insensible à la casse),
    sinon retourne 'NON'
    """
    desc = normalize_str(description)
    
    # Recherche de 'soufflet mousse' (singulier ou pluriel)
    if "SOUFFLET MOUSSE" in desc or "SOUFFLETS MOUSSE" in desc:
        return "OUI"
    else:
        return "NON"

def detecter_facon_moderne_sommier(description):
    """
    Détecte si le sommier est de façon moderne
    Retourne 'OUI' si 'façon moderne' est trouvé (insensible à la casse),
    sinon retourne 'NON'
    """
    desc = normalize_str(description)
    
    # Recherche de 'façon moderne' (après normalisation qui supprime les accents)
    if "FACON MODERNE" in desc:
        return "OUI"
    else:
        return "NON"

def detecter_tapissier_a_lattes_sommier(description):
    """
    Détecte si le sommier est tapissier à lattes
    Retourne 'OUI' si 'tapissier à lattes' est trouvé (insensible à la casse),
    sinon retourne 'NON'
    """
    desc = normalize_str(description)
    
    # Recherche de 'tapissier à lattes' (après normalisation qui supprime les accents)
    if "TAPISSIER A LATTES" in desc:
        return "OUI"
    else:
        return "NON"

def detecter_lattes_francaises_sommier(description):
    """
    Détecte si le sommier a des lattes françaises
    Retourne 'OUI' si 'lattes françaises' est trouvé (insensible à la casse),
    sinon retourne 'NON'
    """
    desc = normalize_str(description)
    
    # Recherche de 'lattes françaises' (singulier ou pluriel, après normalisation qui supprime les accents)
    if "LATTES FRANCAISES" in desc or "LATTE FRANCAISE" in desc:
        return "OUI"
    else:
        return "NON"

def detecter_structure_renforcee_sommier(description):
    """
    Détecte si le sommier a une structure renforcée
    Retourne 'OUI' si 'structure renforcée' est trouvé (insensible à la casse et au pluriel),
    sinon retourne 'NON'
    """
    desc = normalize_str(description)
    
    # Recherche de 'structure renforcée' (singulier ou pluriel, après normalisation qui supprime les accents)
    if "STRUCTURE RENFORCEE" in desc or "STRUCTURES RENFORCEES" in desc:
        return "OUI"
    else:
        return "NON"

def detecter_options_sommier(description):
    """
    Détecte la présence de chaque option dans la description du sommier.
    Retourne un dict {option: 'OUI'/'NON'} pour chaque terme de la liste.
    """
    termes = [
        ("butees_laterales", ["butées latérales", "butees laterales"]),
        ("butees_pieds", ["butées pieds", "butees pieds"]),
        ("solidarisation", ["solidarisation"]),
        ("demi_corbeille", ["1/2 corbeille", "demi corbeille"]),
        ("profile", ["profilé", "profile"]),
        ("renforces", ["renforcés", "renforces"]),
        ("genou_moins", ["genou moins"]),
        ("tronc_plus", ["tronc plus"]),
        ("calles", ["calles"]),
        ("rampes", ["rampes"]),
        ("autre", ["autre"]),
        ("platine_reunion", ["platine reunion"]),
        ("pieds_centraux", ["pieds centraux"]),
        ("patins_feutre", ["patins feutre", "patin feutre"]),
        ("patins_carrelage", ["patins carrelage", "patin carrelage"]),
        ("patins_teflon", ["patins teflon", "patin teflon"]),
        ("finition_multiplis", ["multiplis"]),
        ("finition_90mm", ["90mm", "90 mm"]),
        ("finition_paremente", ["paremente"]),
        ("finition_multiplis_tv", ["multiplis tv"]),
        ("finition_multiplis_l", ["multiplis l"]),
        ("finition_chene", ["chene", "chêne"]),
        ("finition_frene_tv", ["frene tv", "frêne tv"]),
        ("finition_frene_l", ["frene l", "frêne l"])
    ]
    desc = description.lower()
    result = {}
    for key, patterns in termes:
        found = any(pat in desc for pat in patterns)
        result[key] = "OUI" if found else "NON"
    return result

def segmenter_pieds_sommier(description, quantite_article=1):
    """
    Segmente une description de pieds de sommier pour extraire un objet fusionné :
    - quantité totale (quantité d'article x nombre de pieds par lot)
    - nombre de lots (quantité d'article)
    - type, hauteur, finition, patin, etc.
    Retourne un seul dict fusionné par article.
    """
    TYPES_PIEDS = [
        "ANGLE DROIT", "ANGLE GALBE", "ANGLE", "CUBIQUE", "CYLINDRE", "DROIT", "GALBE", "PLATINE REUNION", "CENTRAUX",
        "PIEDS CENTRAUX", "AUTRE"
    ]
    TYPES_PATINS = ["FEUTRE", "CARRELAGE", "TEFLON"]

    def normalize(txt):
        return unicodedata.normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII').upper()

    desc = normalize(description)
    result = {}

    # Nombre de pieds par lot (par défaut 1)
    nb_par_lot = 1
    m = re.search(r"(\d+) ?PIED", desc)
    if m:
        nb_par_lot = int(m.group(1))
    # Quantité totale
    result["quantite"] = quantite_article * nb_par_lot
    # Nombre de lots
    result["nb_lots"] = quantite_article

    # Type de pied (privilégier les types composés)
    for t in sorted(TYPES_PIEDS, key=lambda x: -len(x)):
        if t in desc:
            result["type_pied"] = t
            break
    # Hauteur
    m = re.search(r"(\d{1,3}) ?CM", desc)
    if m:
        result["hauteur_cm"] = int(m.group(1))
    # Finition/couleur
    m = re.search(r"(LAQUE|NOIR|SATINE|BLANC|GRIS|BOIS|NATUREL|CHENE|WENGE|METAL|ALU|ARGENTE|DORE|BRONZE|VERNI|BRUT|PEINT|VARNISH|SATIN)", desc)
    if m:
        result["finition"] = m.group(1)
    # Patins
    if "PATIN" in desc:
        for p in TYPES_PATINS:
            if p in desc:
                result["patin"] = p
                break
        result["type_accessoire"] = "PATINS"
    return result

if __name__ == "__main__":
    # Tests des types de sommiers
    print("=== TESTS TYPES SOMMIERS ===")
    sommiers = [
        {"description": "Sommier à lattes bois massif"},
        {"description": "Sommier tapissier 160x200"},
        {"description": "Sommier métallique à ressorts"},
        {"description": "Sommier plat standard"}
    ]
    print(detecter_type_sommier(sommiers))
    
    # Tests du type relaxation
    print("\n=== TESTS TYPE RELAXATION ===")
    descriptions_relaxation = [
        "SOMMIER RELAXATION MOTORISÉE 5 PLIS TÉLESCOPIQUE",
        "SOMMIER relaxation motorisée",
        "SOMMIER RELAXATIONS MOTORISÉES",
        "SOMMIER À LATTES FIXE",
        "SOMMIER TAPISSIER STANDARD",
        "SOMMIER RÉLAXATION",  # Avec accent
        "SOMMIER Relaxation",  # Mixte
    ]
    
    for i, desc in enumerate(descriptions_relaxation, 1):
        type_relaxation = detecter_type_relaxation_sommier(desc)
        print(f"Test {i}: '{desc}' -> {type_relaxation}")
    
    # Tests du type télécommande
    print("\n=== TESTS TYPE TÉLÉCOMMANDE ===")
    descriptions_telecommande = [
        "SOMMIER RELAXATION MOTORISÉE",  # Sans télécommande
        "SOMMIER AVEC TELECOMMANDE",  # Télécommande filaire
        "SOMMIER TELECOMMANDE RADIO",  # Télécommande sans fil
        "SOMMIER TÉLÉCOMMANDE",  # Avec accent
        "SOMMIER telecommande",  # Minuscules
        "SOMMIER TELECOMMANDES",  # Pluriel
        "SOMMIER RADIO SEUL",  # Radio seul
    ]
    
    for i, desc in enumerate(descriptions_telecommande, 1):
        type_telecommande = detecter_type_telecommande_sommier(desc)
        print(f"Test {i}: '{desc}' -> {type_telecommande}")
    
    # Tests des nouvelles caractéristiques
    print("\n=== TESTS NOUVELLES CARACTÉRISTIQUES ===")
    descriptions_nouvelles = [
        "SOMMIER SOUFFLET MOUSSE",  # Soufflet mousse
        "SOMMIER SOUFFLETS MOUSSE",  # Pluriel
        "SOMMIER FAÇON MODERNE",  # Façon moderne
        "SOMMIER FACON MODERNE",  # Sans accent
        "SOMMIER TAPISSIER À LATTES",  # Tapissier à lattes
        "SOMMIER TAPISSIER A LATTES",  # Sans accent
        "SOMMIER LATTES FRANÇAISES",  # Lattes françaises
        "SOMMIER LATTES FRANCAISES",  # Sans accent
        "SOMMIER LATTE FRANÇAISE",  # Singulier
        "SOMMIER STANDARD",  # Aucune caractéristique
    ]
    
    for i, desc in enumerate(descriptions_nouvelles, 1):
        soufflet = detecter_soufflet_mousse_sommier(desc)
        facon = detecter_facon_moderne_sommier(desc)
        tapissier = detecter_tapissier_a_lattes_sommier(desc)
        lattes_fr = detecter_lattes_francaises_sommier(desc)
        print(f"Test {i}: '{desc}' -> Soufflet: {soufflet}, Façon: {facon}, Tapissier: {tapissier}, Lattes FR: {lattes_fr}")
    
    # Tests structure renforcée
    print("\n=== TESTS STRUCTURE RENFORCÉE ===")
    descriptions_structure = [
        "SOMMIER STRUCTURE RENFORCÉE",  # Avec accent
        "SOMMIER STRUCTURE RENFORCEE",  # Sans accent
        "SOMMIER STRUCTURES RENFORCÉES",  # Pluriel avec accent
        "SOMMIER STRUCTURES RENFORCEES",  # Pluriel sans accent
        "SOMMIER structure renforcée",  # Minuscules
        "SOMMIER Structure Renforcée",  # Mixte
        "SOMMIER STANDARD",  # Sans structure renforcée
    ]
    
    for i, desc in enumerate(descriptions_structure, 1):
        structure_renforcee = detecter_structure_renforcee_sommier(desc)
        print(f"Test {i}: '{desc}' -> Structure renforcée: {structure_renforcee}") 