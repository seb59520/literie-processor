#!/usr/bin/env python3
"""
Test spécifique pour la détection de télécommande
"""

import sys
import os

# Ajouter le répertoire backend au path
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(script_dir, "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from sommier_utils import detecter_type_telecommande_sommier, normalize_str

def test_telecommande_specifique():
    """Test avec l'exemple spécifique"""
    description = "TÉLÉCOMMANDE NOIRE RADIO FRÉQUENCE (x2) + ÉCLAIRAGE TORCHE"
    
    print(f"Description originale: {description}")
    
    # Test de normalisation
    desc_normalized = normalize_str(description)
    print(f"Description normalisée: {desc_normalized}")
    
    # Test de détection
    resultat = detecter_type_telecommande_sommier(description)
    print(f"Résultat détection: {resultat}")
    
    # Vérification manuelle
    has_telecommande = "TELECOMMANDE" in desc_normalized or "TELECOMMANDES" in desc_normalized
    has_radio = "RADIO" in desc_normalized
    
    print(f"Contient 'TELECOMMANDE': {has_telecommande}")
    print(f"Contient 'RADIO': {has_radio}")
    
    if has_telecommande and has_radio:
        print("✅ Devrait détecter: TELECOMMANDE SANS FIL")
    elif has_telecommande:
        print("✅ Devrait détecter: TELECOMMANDE FILAIRE")
    else:
        print("✅ Devrait détecter: NON")

def test_variations_telecommande():
    """Test avec différentes variations"""
    cas_tests = [
        "TÉLÉCOMMANDE NOIRE RADIO FRÉQUENCE (x2) + ÉCLAIRAGE TORCHE",
        "TELECOMMANDE NOIRE RADIO FREQUENCE (x2) + ECLAIRAGE TORCHE",
        "TÉLÉCOMMANDE RADIO",
        "TELECOMMANDE RADIO",
        "TÉLÉCOMMANDE SANS RADIO",
        "RADIO SANS TÉLÉCOMMANDE",
        "TÉLÉCOMMANDE FILAIRE",
        "TELECOMMANDE FILAIRE",
    ]
    
    print("\n=== TESTS VARIATIONS TÉLÉCOMMANDE ===")
    for i, desc in enumerate(cas_tests, 1):
        resultat = detecter_type_telecommande_sommier(desc)
        print(f"Test {i}: '{desc}' -> {resultat}")

if __name__ == "__main__":
    test_telecommande_specifique()
    test_variations_telecommande() 