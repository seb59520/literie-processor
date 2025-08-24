#!/usr/bin/env python3
"""
Script de test pour analyser le fichier problématique
"""

import asyncio
import sys
import os

# Ajouter le répertoire backend au path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend_interface import BackendInterface

async def test_fichier_problematique():
    """Test du fichier problématique"""
    
    # Chemin vers le fichier problématique
    fichier_problematique = "Commandes/Commande SARL COUR DU DONJON 422.pdf"
    
    if not os.path.exists(fichier_problematique):
        print(f"Fichier non trouvé: {fichier_problematique}")
        return
    
    print(f"Test du fichier: {fichier_problematique}")
    
    # Créer l'interface backend
    backend = BackendInterface()
    
    # Paramètres de test
    enrich_llm = True
    llm_provider = "openai"
    openrouter_api_key = None  # Utilise la clé OpenAI configurée
    semaine_prod = 29
    annee_prod = 2025
    commande_client = ["422"]
    
    try:
        # Traiter le fichier
        result = await backend._process_single_file(
            {'file_path': fichier_problematique, 'filename': os.path.basename(fichier_problematique)},
            enrich_llm,
            llm_provider,
            openrouter_api_key,
            semaine_prod,
            annee_prod,
            commande_client
        )
        
        print(f"Résultat: {result}")
        
        if result.get('status') == 'success':
            print("✅ Traitement réussi")
            print(f"Configurations matelas: {len(result.get('configurations_matelas', []))}")
            print(f"Configurations sommiers: {len(result.get('configurations_sommiers', []))}")
        else:
            print(f"❌ Erreur: {result.get('error', 'Erreur inconnue')}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_fichier_problematique()) 