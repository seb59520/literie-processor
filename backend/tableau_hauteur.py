"""
Tableau de référence pour les mesures de hauteur des matelas
Contient toutes les hauteurs standard par type de noyau et variantes
"""

# Tableau principal des hauteurs par type de noyau
TABLEAU_HAUTEUR_MATELAS = {
    # LATEX
    "LATEX NATUREL": {
        "hauteur_cm": 10,
        "description": "Matelas latex naturel 100%",
        "epaisseur_noyau": 8,
        "epaisseur_housse": 2,
        "total": 10
    },
    "LATEX MIXTE 7 ZONES": {
        "hauteur_cm": 9,
        "description": "Matelas latex mixte avec zones de confort",
        "epaisseur_noyau": 7,
        "epaisseur_housse": 2,
        "total": 9
    },
    "LATEX RENFORCE": {
        "hauteur_cm": 8,
        "description": "Matelas latex renforcé haute densité",
        "epaisseur_noyau": 6,
        "epaisseur_housse": 2,
        "total": 8
    },
    
    # MOUSSE
    "MOUSSE RAINUREE 7 ZONES": {
        "hauteur_cm": 9,
        "description": "Matelas mousse rainurée avec zones",
        "epaisseur_noyau": 7,
        "epaisseur_housse": 2,
        "total": 9
    },
    "MOUSSE RAINURÉE 7 ZONES": {
        "hauteur_cm": 9,
        "description": "Matelas mousse rainurée (accentué)",
        "epaisseur_noyau": 7,
        "epaisseur_housse": 2,
        "total": 9
    },
    "MOUSSE VISCO": {
        "hauteur_cm": 10,
        "description": "Matelas mousse viscoélastique",
        "epaisseur_noyau": 8,
        "epaisseur_housse": 2,
        "total": 10
    },
    
    # SELECT
    "SELECT 43": {
        "hauteur_cm": 8,
        "description": "Matelas Select 43 haute densité",
        "epaisseur_noyau": 6,
        "epaisseur_housse": 2,
        "total": 8
    },
    
    # Variantes et alternatives
    "LATEX MIXTE": {
        "hauteur_cm": 9,
        "description": "Matelas latex mixte (sans zones)",
        "epaisseur_noyau": 7,
        "epaisseur_housse": 2,
        "total": 9
    },
    "MOUSSE RAINUREE": {
        "hauteur_cm": 9,
        "description": "Matelas mousse rainurée (sans zones)",
        "epaisseur_noyau": 7,
        "epaisseur_housse": 2,
        "total": 9
    },
    "MOUSSE STANDARD": {
        "hauteur_cm": 8,
        "description": "Matelas mousse standard",
        "epaisseur_noyau": 6,
        "epaisseur_housse": 2,
        "total": 8
    }
}

# Tableau des hauteurs par catégorie
TABLEAU_HAUTEUR_PAR_CATEGORIE = {
    "LATEX": {
        "hauteur_min": 8,
        "hauteur_max": 10,
        "hauteur_moyenne": 9,
        "types": ["LATEX NATUREL", "LATEX MIXTE 7 ZONES", "LATEX RENFORCE", "LATEX MIXTE"]
    },
    "MOUSSE": {
        "hauteur_min": 8,
        "hauteur_max": 10,
        "hauteur_moyenne": 9,
        "types": ["MOUSSE RAINUREE 7 ZONES", "MOUSSE VISCO", "MOUSSE RAINUREE", "MOUSSE STANDARD"]
    },
    "SELECT": {
        "hauteur_min": 8,
        "hauteur_max": 8,
        "hauteur_moyenne": 8,
        "types": ["SELECT 43"]
    }
}

def obtenir_hauteur_matelas(noyau: str) -> dict:
    """
    Obtient les informations complètes de hauteur pour un type de noyau
    
    Args:
        noyau (str): Type de noyau du matelas
        
    Returns:
        dict: Dictionnaire avec toutes les informations de hauteur
    """
    return TABLEAU_HAUTEUR_MATELAS.get(noyau.upper(), {
        "hauteur_cm": 0,
        "description": "Type de noyau non reconnu",
        "epaisseur_noyau": 0,
        "epaisseur_housse": 0,
        "total": 0
    })

def calculer_hauteur_simple(noyau: str) -> int:
    """
    Calcule la hauteur simple en centimètres
    
    Args:
        noyau (str): Type de noyau du matelas
        
    Returns:
        int: Hauteur en centimètres
    """
    info = obtenir_hauteur_matelas(noyau)
    return info["hauteur_cm"]

def obtenir_categorie_noyau(noyau: str) -> str:
    """
    Détermine la catégorie d'un noyau
    
    Args:
        noyau (str): Type de noyau du matelas
        
    Returns:
        str: Catégorie (LATEX, MOUSSE, SELECT, INCONNU)
    """
    noyau_upper = noyau.upper()
    
    for categorie, info in TABLEAU_HAUTEUR_PAR_CATEGORIE.items():
        if noyau_upper in info["types"]:
            return categorie
    
    return "INCONNU"

def obtenir_statistiques_categorie(categorie: str) -> dict:
    """
    Obtient les statistiques de hauteur pour une catégorie
    
    Args:
        categorie (str): Catégorie de noyau
        
    Returns:
        dict: Statistiques de la catégorie
    """
    return TABLEAU_HAUTEUR_PAR_CATEGORIE.get(categorie.upper(), {
        "hauteur_min": 0,
        "hauteur_max": 0,
        "hauteur_moyenne": 0,
        "types": []
    })

def lister_tous_noyaux() -> list:
    """
    Liste tous les types de noyaux disponibles
    
    Returns:
        list: Liste de tous les types de noyaux
    """
    return list(TABLEAU_HAUTEUR_MATELAS.keys())

def lister_noyaux_par_hauteur(hauteur_cm: int) -> list:
    """
    Liste tous les noyaux ayant une hauteur spécifique
    
    Args:
        hauteur_cm (int): Hauteur en centimètres
        
    Returns:
        list: Liste des noyaux avec cette hauteur
    """
    noyaux = []
    for noyau, info in TABLEAU_HAUTEUR_MATELAS.items():
        if info["hauteur_cm"] == hauteur_cm:
            noyaux.append(noyau)
    return noyaux

def afficher_tableau_complet():
    """
    Affiche le tableau complet des hauteurs
    """
    print("=" * 80)
    print("📏 TABLEAU COMPLET DES HAUTEURS DE MATELAS")
    print("=" * 80)
    
    for noyau, info in TABLEAU_HAUTEUR_MATELAS.items():
        print(f"\n🔸 {noyau}")
        print(f"   📐 Hauteur totale: {info['hauteur_cm']} cm")
        print(f"   📋 Description: {info['description']}")
        print(f"   🧱 Épaisseur noyau: {info['epaisseur_noyau']} cm")
        print(f"   🛏️ Épaisseur housse: {info['epaisseur_housse']} cm")
        print(f"   ➕ Total: {info['total']} cm")
    
    print("\n" + "=" * 80)
    print("📊 STATISTIQUES PAR CATÉGORIE")
    print("=" * 80)
    
    for categorie, stats in TABLEAU_HAUTEUR_PAR_CATEGORIE.items():
        print(f"\n🏷️ {categorie}")
        print(f"   📏 Hauteur min: {stats['hauteur_min']} cm")
        print(f"   📏 Hauteur max: {stats['hauteur_max']} cm")
        print(f"   📏 Hauteur moyenne: {stats['hauteur_moyenne']} cm")
        print(f"   📝 Types: {', '.join(stats['types'])}")

if __name__ == "__main__":
    # Tests et démonstration
    print("🧪 TESTS DU TABLEAU DE HAUTEUR")
    print("=" * 50)
    
    # Test 1: Hauteur simple
    print(f"Hauteur LATEX NATUREL: {calculer_hauteur_simple('LATEX NATUREL')} cm")
    print(f"Hauteur MOUSSE VISCO: {calculer_hauteur_simple('MOUSSE VISCO')} cm")
    print(f"Hauteur INCONNU: {calculer_hauteur_simple('INCONNU')} cm")
    
    # Test 2: Informations complètes
    print(f"\nInfos LATEX MIXTE 7 ZONES: {obtenir_hauteur_matelas('LATEX MIXTE 7 ZONES')}")
    
    # Test 3: Catégorie
    print(f"\nCatégorie LATEX NATUREL: {obtenir_categorie_noyau('LATEX NATUREL')}")
    print(f"Catégorie MOUSSE VISCO: {obtenir_categorie_noyau('MOUSSE VISCO')}")
    
    # Test 4: Noyaux par hauteur
    print(f"\nNoyaux de 10cm: {lister_noyaux_par_hauteur(10)}")
    print(f"Noyaux de 9cm: {lister_noyaux_par_hauteur(9)}")
    
    # Affichage du tableau complet
    afficher_tableau_complet() 