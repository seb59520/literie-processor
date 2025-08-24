#!/usr/bin/env python3
"""
Test de correction des dates de semaine
Vérifie que la fonction get_week_dates retourne les bonnes dates selon la norme ISO 8601
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from date_utils import get_week_dates
from datetime import datetime

def test_week_dates():
    """Test de la fonction get_week_dates avec différents cas"""
    
    print("🧪 Test de correction des dates de semaine")
    print("=" * 50)
    
    # Test cas problématique : semaine 29 de 2025
    print("\n📅 Test semaine 29 de 2025:")
    lundi, vendredi = get_week_dates(29, 2025)
    print(f"  Semaine 29_2025 : lundi = {lundi}, vendredi = {vendredi}")
    
    # Vérification que les dates correspondent bien à la semaine 29
    # Format français : DD-MM-YYYY
    lundi_date = datetime.strptime(lundi, "%d-%m-%Y")
    vendredi_date = datetime.strptime(vendredi, "%d-%m-%Y")
    
    # Calcul du numéro de semaine ISO pour vérification
    semaine_iso_lundi = lundi_date.isocalendar()[1]
    semaine_iso_vendredi = vendredi_date.isocalendar()[1]
    
    print(f"  Vérification ISO : lundi semaine {semaine_iso_lundi}, vendredi semaine {semaine_iso_vendredi}")
    
    if semaine_iso_lundi == 29 and semaine_iso_vendredi == 29:
        print("  ✅ CORRECTION RÉUSSIE : Les dates correspondent bien à la semaine 29")
    else:
        print("  ❌ ERREUR : Les dates ne correspondent pas à la semaine 29")
    
    # Test semaine 30 de 2025 (les dates qui étaient incorrectement attribuées à la semaine 29)
    print("\n📅 Test semaine 30 de 2025:")
    lundi, vendredi = get_week_dates(30, 2025)
    print(f"  Semaine 30_2025 : lundi = {lundi}, vendredi = {vendredi}")
    
    # Vérification que les dates correspondent bien à la semaine 30
    lundi_date = datetime.strptime(lundi, "%d-%m-%Y")
    vendredi_date = datetime.strptime(vendredi, "%d-%m-%Y")
    
    semaine_iso_lundi = lundi_date.isocalendar()[1]
    semaine_iso_vendredi = vendredi_date.isocalendar()[1]
    
    print(f"  Vérification ISO : lundi semaine {semaine_iso_lundi}, vendredi semaine {semaine_iso_vendredi}")
    
    if semaine_iso_lundi == 30 and semaine_iso_vendredi == 30:
        print("  ✅ CORRECTION RÉUSSIE : Les dates correspondent bien à la semaine 30")
    else:
        print("  ❌ ERREUR : Les dates ne correspondent pas à la semaine 30")
    
    # Test avec d'autres semaines pour vérifier la cohérence
    print("\n📅 Tests de cohérence avec d'autres semaines:")
    test_cases = [
        (1, 2025, "Semaine 1"),
        (25, 2025, "Semaine 25"),
        (52, 2025, "Semaine 52"),
        (1, 2024, "Semaine 1 2024"),
        (53, 2024, "Semaine 53 2024")
    ]
    
    for semaine, annee, description in test_cases:
        lundi, vendredi = get_week_dates(semaine, annee)
        lundi_date = datetime.strptime(lundi, "%d-%m-%Y")
        vendredi_date = datetime.strptime(vendredi, "%d-%m-%Y")
        
        semaine_iso_lundi = lundi_date.isocalendar()[1]
        semaine_iso_vendredi = vendredi_date.isocalendar()[1]
        
        print(f"  {description}: lundi = {lundi} (semaine {semaine_iso_lundi}), vendredi = {vendredi} (semaine {semaine_iso_vendredi})")
        
        if semaine_iso_lundi == semaine and semaine_iso_vendredi == semaine:
            print(f"    ✅ OK")
        else:
            print(f"    ❌ ERREUR")
    
    print("\n" + "=" * 50)
    print("🎉 Test terminé !")

if __name__ == "__main__":
    test_week_dates() 