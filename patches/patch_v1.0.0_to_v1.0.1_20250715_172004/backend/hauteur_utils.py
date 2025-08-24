def calculer_hauteur_matelas(noyau):
    """
    Calcule la hauteur en fonction du type de noyau de matelas.
    Retourne la hauteur en centimètres.
    """
    hauteurs = {
        "LATEX NATUREL": 10,
        "LATEX MIXTE 7 ZONES": 9,
        "MOUSSE RAINUREE 7 ZONES": 9,
        "LATEX RENFORCE": 8,
        "SELECT 43": 8,
        "MOUSSE VISCO": 10
    }
    
    return hauteurs.get(noyau, 0)  # Retourne 0 si le noyau n'est pas reconnu

if __name__ == "__main__":
    # Tests
    test_noyaux = [
        "LATEX NATUREL",
        "LATEX MIXTE 7 ZONES", 
        "MOUSSE RAINUREE 7 ZONES",
        "LATEX RENFORCE",
        "SELECT 43",
        "MOUSSE VISCO",
        "INCONNU"
    ]
    
    for noyau in test_noyaux:
        hauteur = calculer_hauteur_matelas(noyau)
        print(f"{noyau} -> Hauteur = {hauteur}cm") 