#!/usr/bin/env python3

"""
Script pour lister tous les champs disponibles dans le pré-import
"""

def lister_champs_pre_import():
    """Liste tous les champs disponibles dans le pré-import"""
    
    print("📋 CHAMPS DISPONIBLES DANS LE PRÉ-IMPORT")
    print("=" * 60)
    
    # Champs client
    print("\n🏷️  CHAMPS CLIENT")
    print("-" * 30)
    champs_client = {
        "Client_D1": "Nom du client (ex: 'Mr LOUCHART FREDERIC')",
        "Adresse_D3": "Ville du client (ex: 'HAZEBROUCK')"
    }
    for champ, description in champs_client.items():
        print(f"  {champ:<20} : {description}")
    
    # Champs commande et dates
    print("\n📅 CHAMPS COMMANDE ET DATES")
    print("-" * 30)
    champs_commande = {
        "numero_D2": "Numéro de commande client (ex: 'LOUCHART')",
        "semaine_D5": "Semaine de production (ex: '25_2025')",
        "lundi_D6": "Date du lundi (ex: '2025-06-16')",
        "vendredi_D7": "Date du vendredi (ex: '2025-06-20')"
    }
    for champ, description in champs_commande.items():
        print(f"  {champ:<20} : {description}")
    
    # Champs matelas
    print("\n🛏️  CHAMPS MATELAS")
    print("-" * 30)
    champs_matelas = {
        "Hauteur_D22": "Hauteur du matelas (ex: 20)"
    }
    for champ, description in champs_matelas.items():
        print(f"  {champ:<20} : {description}")
    
    # Champs détection
    print("\n🔍 CHAMPS DÉTECTION")
    print("-" * 30)
    champs_detection = {
        "dosseret_tete_C8": "Détection DOSSERET/TETE ('X' si détecté, '' sinon)"
    }
    for champ, description in champs_detection.items():
        print(f"  {champ:<20} : {description}")
    
    # Champs quantité
    print("\n📦 CHAMPS QUANTITÉ")
    print("-" * 30)
    champs_quantite = {
        "jumeaux_C10": "Quantité = 2 ('X' si jumeaux, '' sinon)",
        "jumeaux_D10": "Dimensions pour jumeaux (ex: '89x198')",
        "1piece_C11": "Quantité = 1 ('X' si 1 pièce, '' sinon)",
        "1piece_D11": "Dimensions pour 1 pièce (ex: '89x198')"
    }
    for champ, description in champs_quantite.items():
        print(f"  {champ:<20} : {description}")
    
    # Champs housse simple
    print("\n🛏️  CHAMPS HOUSSE SIMPLE")
    print("-" * 30)
    champs_housse_simple = {
        "HSimple_polyester_C13": "Housse SIMPLE + POLYESTER ('X' si applicable)",
        "HSimple_polyester_D13": "Dimensions housse simple polyester",
        "HSimple_tencel_C14": "Housse SIMPLE + TENCEL ('X' si applicable)",
        "HSimple_tencel_D14": "Dimensions housse simple tencel",
        "HSimple_autre_C15": "Housse SIMPLE + AUTRE ('X' si applicable)",
        "HSimple_autre_D15": "Dimensions housse simple autre"
    }
    for champ, description in champs_housse_simple.items():
        print(f"  {champ:<20} : {description}")
    
    # Champs housse matelassée
    print("\n🛏️  CHAMPS HOUSSE MATELASSÉE")
    print("-" * 30)
    champs_housse_matelassee = {
        "Hmat_polyester_C17": "Housse MATELASSÉE + POLYESTER ('X' si applicable)",
        "Hmat_polyester_D17": "Dimensions housse matelassée polyester",
        "Hmat_tencel_C18": "Housse MATELASSÉE + TENCEL ('X' si applicable)",
        "Hmat_tencel_D18": "Dimensions housse matelassée tencel",
        "Hmat_luxe3D_C19": "Housse MATELASSÉE + TENCEL LUXE 3D ('X' si applicable)",
        "Hmat_luxe3D_D19": "Dimensions housse matelassée tencel luxe 3D"
    }
    for champ, description in champs_housse_matelassee.items():
        print(f"  {champ:<20} : {description}")
    
    # Champs poignées
    print("\n🔧 CHAMPS POIGNÉES")
    print("-" * 30)
    champs_poignees = {
        "poignees_C20": "Poignées ('X' si OUI, '' sinon)"
    }
    for champ, description in champs_poignees.items():
        print(f"  {champ:<20} : {description}")
    
    # Champs dimensions
    print("\n📏 CHAMPS DIMENSIONS")
    print("-" * 30)
    champs_dimensions = {
        "dimension_housse_D23": "Dimensions housse (ex: '89x198')",
        "longueur_D24": "Longueur housse (ex: '198')",
        "decoupe_noyau_D25": "Découpe noyau (ex: 'STANDARD')"
    }
    for champ, description in champs_dimensions.items():
        print(f"  {champ:<20} : {description}")
    
    # Champs noyau et fermeté
    print("\n🧱 CHAMPS NOYAU ET FERMETÉ")
    print("-" * 30)
    champs_noyau = {
        "LN_Ferme_C28": "LATEX NATUREL + FERME ('X' si applicable)",
        "LN_Medium_C29": "LATEX NATUREL + MEDIUM ('X' si applicable)",
        "LM7z_Ferme_C30": "LATEX MIXTE 7 ZONES + FERME ('X' si applicable)",
        "LM7z_Medium_C31": "LATEX MIXTE 7 ZONES + MEDIUM ('X' si applicable)",
        "LM3z_Ferme_C32": "LATEX MIXTE 3 ZONES + FERME ('X' si applicable)",
        "LM3z_Medium_C33": "LATEX MIXTE 3 ZONES + MEDIUM ('X' si applicable)",
        "MV_Ferme_C34": "MOUSSE VISCO + FERME ('X' si applicable)",
        "MV_Medium_C35": "MOUSSE VISCO + MEDIUM ('X' si applicable)",
        "MV_Confort_C36": "MOUSSE VISCO + CONFORT ('X' si applicable)",
        "MR_Ferme_C37": "MOUSSE RAINUREE + FERME ('X' si applicable)",
        "MR_Medium_C38": "MOUSSE RAINUREE + MEDIUM ('X' si applicable)",
        "MR_Confort_C39": "MOUSSE RAINUREE + CONFORT ('X' si applicable)",
        "SL43_Ferme_C40": "SELECT 43 + FERME ('X' si applicable)",
        "SL43_Medium_C41": "SELECT 43 + MEDIUM ('X' si applicable)"
    }
    for champ, description in champs_noyau.items():
        print(f"  {champ:<20} : {description}")
    
    # Champs surmatelas
    print("\n🛏️  CHAMPS SURMATELAS")
    print("-" * 30)
    champs_surmatelas = {
        "Surmatelas_C45": "Surmatelas ('X' si présent, '' sinon)"
    }
    for champ, description in champs_surmatelas.items():
        print(f"  {champ:<20} : {description}")
    
    # Champs opérations
    print("\n🚚 CHAMPS OPÉRATIONS")
    print("-" * 30)
    champs_operations = {
        "emporte_client_C57": "Enlèvement client ('X' si ENLEVEMENT détecté)",
        "fourgon_C58": "Livraison fourgon ('X' si LIVRAISON détecté)",
        "transporteur_C59": "Expédition transporteur ('X' si EXPEDITION détecté)"
    }
    for champ, description in champs_operations.items():
        print(f"  {champ:<20} : {description}")
    
    # Champs de référence
    print("\n📊 CHAMPS DE RÉFÉRENCE")
    print("-" * 30)
    champs_reference = {
        "matelas_index": "Index du matelas (pour référence)",
        "noyau": "Type de noyau (pour référence)",
        "quantite": "Quantité (pour référence)"
    }
    for champ, description in champs_reference.items():
        print(f"  {champ:<20} : {description}")
    
    # Résumé
    print("\n📈 RÉSUMÉ")
    print("-" * 30)
    total_champs = (
        len(champs_client) + len(champs_commande) + len(champs_matelas) + 
        len(champs_detection) + len(champs_quantite) + len(champs_housse_simple) + 
        len(champs_housse_matelassee) + len(champs_poignees) + len(champs_dimensions) + 
        len(champs_noyau) + len(champs_surmatelas) + len(champs_operations) + 
        len(champs_reference)
    )
    print(f"  Total des champs disponibles : {total_champs}")
    
    # Champs conditionnels
    print("\n⚠️  CHAMPS CONDITIONNELS")
    print("-" * 30)
    print("  Les champs D pour les housses (D13, D14, D15, D17, D18, D19)")
    print("  ne sont créés que si le champ C correspondant est 'X'")
    print("  Exemple: HSimple_polyester_D13 n'existe que si HSimple_polyester_C13 = 'X'")
    
    # Utilisation
    print("\n💡 UTILISATION")
    print("-" * 30)
    print("  Ces champs sont utilisés pour :")
    print("  - La validation des données de pré-import")
    print("  - L'affichage dans l'interface utilisateur")
    print("  - La préparation pour l'écriture Excel")
    print("  - Le mapping vers des cellules Excel spécifiques")

if __name__ == "__main__":
    lister_champs_pre_import() 