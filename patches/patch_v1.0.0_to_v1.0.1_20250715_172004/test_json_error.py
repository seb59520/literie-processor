#!/usr/bin/env python3

import json
import sys
sys.path.append('backend')

from main import clean_and_parse_json

# Tests de différents cas d'erreur JSON
test_cases = [
    "",  # Chaîne vide
    "   ",  # Espaces seulement
    "invalid json",  # JSON invalide
    '{"test": "value"}',  # JSON valide
    '{"test": "value"',  # JSON incomplet
    '{"test": "value",}',  # JSON avec virgule en trop
    '{"test": "value", "nested": {"key": "value"}}',  # JSON complexe valide
]

print("=== TEST GESTION ERREURS JSON ===")

for i, test_case in enumerate(test_cases):
    print(f"\n--- Test {i+1}: {repr(test_case)} ---")
    
    try:
        # Test de la fonction de nettoyage
        cleaned = clean_and_parse_json(test_case)
        print(f"Après nettoyage: {repr(cleaned)}")
        
        # Test du parsing JSON
        if cleaned.strip():
            try:
                parsed = json.loads(cleaned)
                print(f"✅ JSON valide: {type(parsed)} - {parsed}")
            except json.JSONDecodeError as e:
                print(f"❌ Erreur JSON: {e}")
        else:
            print("⚠️  Chaîne vide après nettoyage")
            
    except Exception as e:
        print(f"❌ Erreur générale: {e}")

print("\n✅ Tests terminés !") 