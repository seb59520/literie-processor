#!/usr/bin/env python3

import math

def test_dimension_literie():
    """Test du calcul de dimension literie avec arrondi largeur ET longueur"""
    
    # Cas de test
    test_cases = [
        {"largeur": 139, "longueur": 189, "quantite": 1, "expected": "140x190"},
        {"largeur": 89, "longueur": 198, "quantite": 2, "expected": "180x200"},
        {"largeur": 160, "longueur": 200, "quantite": 1, "expected": "160x200"},
        {"largeur": 180, "longueur": 200, "quantite": 1, "expected": "180x200"},
        {"largeur": 182, "longueur": 203, "quantite": 1, "expected": "190x210"},
    ]
    
    print("=== TEST DIMENSION LITERIE ===")
    
    for i, test_case in enumerate(test_cases, 1):
        largeur = test_case["largeur"]
        longueur = test_case["longueur"]
        quantite = test_case["quantite"]
        expected = test_case["expected"]
        
        # Calcul selon la logique corrigée
        largeur_arrondie = int(math.ceil(largeur / 10.0) * 10)
        longueur_arrondie = int(math.ceil(longueur / 10.0) * 10)
        
        if quantite == 2:
            largeur_literie = largeur_arrondie * 2
        else:
            largeur_literie = largeur_arrondie
            
        dimension_literie = f"{largeur_literie}x{longueur_arrondie}"
        
        # Vérification
        success = dimension_literie == expected
        status = "✅" if success else "❌"
        
        print(f"Test {i}: {largeur}x{longueur} (qte: {quantite}) -> {dimension_literie} {status}")
        if not success:
            print(f"  Attendu: {expected}")
            print(f"  Obtenu: {dimension_literie}")
    
    print("\n✅ Test terminé !")

if __name__ == "__main__":
    test_dimension_literie() 