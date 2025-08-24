#!/usr/bin/env python3
"""
Script de test pour vérifier l'analyse du contenu des fichiers PDF
"""

import sys
import os
sys.path.append('.')

from app_gui import ProcessingThread
from datetime import datetime

def test_analysis():
    """Test de l'analyse du contenu"""
    print("🧪 Test de l'analyse du contenu")
    print("=" * 50)
    
    # Créer une instance de ProcessingThread pour tester
    thread = ProcessingThread(
        files=[],  # Pas de fichiers pour ce test
        enrich_llm=False,  # Pas d'LLM pour ce test
        llm_provider="ollama",
        openrouter_api_key="",
        semaine_prod=datetime.now().isocalendar()[1],
        annee_prod=datetime.now().year,
        commande_client=[]
    )
    
    # Test 1: Texte avec matelas
    print("\n📋 Test 1: Texte avec matelas")
    text1 = "Commande de matelas latex 160x200"
    result1 = thread.analyze_text_content(text1)
    print(f"Texte: {text1}")
    print(f"Résultat: Matelas={result1[0]}, Sommiers={result1[1]}, Count={result1[2]}, {result1[3]}")
    
    # Test 2: Texte avec sommiers
    print("\n📋 Test 2: Texte avec sommiers")
    text2 = "Sommier lattes bois massif 160x200"
    result2 = thread.analyze_text_content(text2)
    print(f"Texte: {text2}")
    print(f"Résultat: Matelas={result2[0]}, Sommiers={result2[1]}, Count={result2[2]}, {result2[3]}")
    
    # Test 3: Texte avec les deux
    print("\n📋 Test 3: Texte avec matelas et sommiers")
    text3 = "Matelas memory foam + sommier lattes"
    result3 = thread.analyze_text_content(text3)
    print(f"Texte: {text3}")
    print(f"Résultat: Matelas={result3[0]}, Sommiers={result3[1]}, Count={result3[2]}, {result3[3]}")
    
    # Test 4: Texte sans mots-clés
    print("\n📋 Test 4: Texte sans mots-clés")
    text4 = "Commande de mobilier divers"
    result4 = thread.analyze_text_content(text4)
    print(f"Texte: {text4}")
    print(f"Résultat: Matelas={result4[0]}, Sommiers={result4[1]}, Count={result4[2]}, {result4[3]}")
    
    # Test 5: Texte vide
    print("\n📋 Test 5: Texte vide")
    text5 = ""
    result5 = thread.analyze_text_content(text5)
    print(f"Texte: (vide)")
    print(f"Résultat: Matelas={result5[0]}, Sommiers={result5[1]}, Count={result5[2]}, {result5[3]}")
    
    print("\n✅ Tests terminés")

if __name__ == "__main__":
    test_analysis() 