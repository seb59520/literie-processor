#!/usr/bin/env python3
"""
Script de vérification du tri global des noyaux
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import config
from backend_interface import BackendInterface

def test_tri_global():
    """Test du tri global des noyaux"""
    
    print("🧪 Test de vérification du tri global des noyaux")
    print("=" * 60)
    
    # Vérifier l'ordre des noyaux configuré
    noyau_order = config.get_noyau_order()
    print(f"📋 Ordre des noyaux configuré ({len(noyau_order)} noyaux):")
    for i, noyau in enumerate(noyau_order, 1):
        print(f"  {i}. {noyau}")
    
    # Créer des données de test
    pre_import_test = [
        {
            'noyau': 'LATEX MIXTE 7 ZONES',
            'Client_D1': 'Client A',
            'type_article': 'matelas'
        },
        {
            'noyau': 'LATEX NATUREL',
            'Client_D1': 'Client B',
            'type_article': 'matelas'
        },
        {
            'noyau': 'MOUSSE VISCO',
            'Client_D1': 'Client C',
            'type_article': 'matelas'
        },
        {
            'noyau': 'SELECT 43',
            'Client_D1': 'Client D',
            'type_article': 'matelas'
        }
    ]
    
    print(f"\n📊 Données de test ({len(pre_import_test)} matelas):")
    for i, item in enumerate(pre_import_test, 1):
        print(f"  {i}. {item['noyau']} - {item['Client_D1']}")
    
    # Simuler le tri global
    backend = BackendInterface()
    
    # Séparer les matelas
    pre_import_matelas = [item for item in pre_import_test if item.get('type_article') != 'sommier']
    
    print(f"\n🔄 Application du tri global...")
    
    # Récupérer l'ordre des noyaux depuis la config
    noyau_order = config.get_noyau_order()
    print(f"Ordre des noyaux pour tri global: {noyau_order}")
    
    # Afficher les noyaux présents dans les pré-imports
    noyaux_presents = []
    for pre_import in pre_import_matelas:
        noyau = pre_import.get('noyau')
        if noyau:
            noyaux_presents.append(noyau)
    print(f"Noyaux présents dans les pré-imports: {noyaux_presents}")
    
    # Trier les pré-imports selon l'ordre des noyaux
    if noyau_order:
        def get_noyau_key(pre_import):
            noyau = pre_import.get('noyau', '')
            print(f"Tri global de la configuration avec noyau: {noyau}")
            try:
                return noyau_order.index(noyau)
            except ValueError:
                print(f"Noyau '{noyau}' non trouvé dans l'ordre, placé à la fin")
                return len(noyau_order) + 1  # Les noyaux non listés vont à la fin
        
        pre_import_matelas_tries = sorted(pre_import_matelas, key=get_noyau_key)
        print(f"Pré-imports matelas triés selon l'ordre global défini")
    else:
        pre_import_matelas_tries = pre_import_matelas
        print("Aucun ordre de noyaux configuré, pas de tri appliqué")
    
    print(f"\n✅ Résultat du tri:")
    for i, item in enumerate(pre_import_matelas_tries, 1):
        print(f"  {i}. {item['noyau']} - {item['Client_D1']}")
    
    # Vérifier si l'ordre est correct
    if noyau_order and len(pre_import_matelas_tries) > 1:
        premier_noyau = pre_import_matelas_tries[0]['noyau']
        if premier_noyau == noyau_order[0]:
            print(f"\n🎉 SUCCÈS : Le tri global fonctionne !")
            print(f"   Premier noyau après tri : {premier_noyau}")
            print(f"   Premier noyau dans l'ordre configuré : {noyau_order[0]}")
        else:
            print(f"\n❌ ERREUR : Le tri global ne fonctionne pas !")
            print(f"   Premier noyau après tri : {premier_noyau}")
            print(f"   Premier noyau dans l'ordre configuré : {noyau_order[0]}")
    else:
        print(f"\n⚠️  Impossible de vérifier le tri (pas assez de données ou pas d'ordre configuré)")
    
    print("\n" + "=" * 60)
    print("Test terminé !")

if __name__ == "__main__":
    test_tri_global() 