"""
Exemple d'intégration du système de tracking des coûts dans votre application
Montre comment utiliser le cost_tracker et afficher les coûts aux utilisateurs
"""

import os
import sys
from pathlib import Path
from backend.cost_tracker import cost_tracker
from backend.llm_provider import llm_manager
from backend.secure_storage import secure_storage

def exemple_traitement_avec_couts(fichier_pdf: str):
    """
    Exemple de traitement d'un fichier PDF avec tracking des coûts
    """
    print(f"🔄 Traitement du fichier: {fichier_pdf}")
    
    # 1. Démarrer une session de tracking
    file_size = os.path.getsize(fichier_pdf) if os.path.exists(fichier_pdf) else 1024
    session_id = cost_tracker.start_session(
        file_name=os.path.basename(fichier_pdf),
        file_path=fichier_pdf,
        file_size=file_size
    )
    
    print(f"📊 Session démarrée: {session_id}")
    
    try:
        # 2. Configurer le LLM
        llm_manager.set_provider('openrouter')
        openrouter_key = secure_storage.load_api_key('openrouter')
        if openrouter_key:
            llm_manager.current_api_key = openrouter_key
        else:
            print("❌ Pas de clé OpenRouter disponible")
            return
        
        # 3. Faire des appels LLM avec tracking automatique
        prompt = "Analyse ce texte et extrait les informations de matelas : MATELAS MOUSSE MONOZONE HAUTE RÉSILIENCE ET HAUTE DENSITÉ (43kg/m3) - SELECT43 FERME - HOUSSE MATELASSÉE TENCEL AVEC POIGNÉES OREILLES LAVABLE A 40° - 119/198/18"
        
        print("🤖 Appel LLM en cours...")
        result = llm_manager.call_llm(
            prompt=prompt,
            file_name=os.path.basename(fichier_pdf),
            file_size=file_size,
            session_id=session_id,
            model="openai/gpt-4o-mini",
            max_tokens=500
        )
        
        if result.get('success'):
            print(f"✅ Appel réussi!")
            
            # Afficher les informations de coût
            if 'cost_info' in result:
                cost_info = result['cost_info']
                print(f"💰 Coût de cet appel: ${cost_info['total_cost']:.6f}")
                print(f"   - Prompt: {result['usage'].get('prompt_tokens', 0)} tokens (${cost_info['cost_prompt']:.6f})")
                print(f"   - Completion: {result['usage'].get('completion_tokens', 0)} tokens (${cost_info['cost_completion']:.6f})")
            
            # Simuler d'autres appels pour traitement complet
            for i in range(2):
                print(f"🤖 Appel LLM supplémentaire {i+1}...")
                result2 = llm_manager.call_llm(
                    prompt=f"Étape {i+1}: valide les dimensions et calcule les prix",
                    file_name=os.path.basename(fichier_pdf),
                    file_size=file_size,
                    session_id=session_id,
                    model="openai/gpt-4o-mini",
                    max_tokens=200
                )
                
                if result2.get('success') and 'cost_info' in result2:
                    print(f"   Coût étape {i+1}: ${result2['cost_info']['total_cost']:.6f}")
        
        # 4. Terminer la session avec succès
        cost_tracker.end_session(session_id, success=True)
        print("✅ Session terminée avec succès")
        
    except Exception as e:
        print(f"❌ Erreur durant le traitement: {e}")
        cost_tracker.end_session(session_id, success=False, error_message=str(e))
    
    # 5. Afficher le résumé de la session
    session_cost = cost_tracker.get_session_cost(session_id)
    print(f"\n📊 RÉSUMÉ DE LA SESSION")
    print(f"Coût total: ${session_cost:.6f}")
    
    return session_id

def afficher_statistiques_quotidiennes():
    """Affiche les statistiques du jour"""
    print("\n" + "="*50)
    print("📊 STATISTIQUES QUOTIDIENNES")
    print("="*50)
    
    stats = cost_tracker.get_daily_stats()
    
    print(f"Date: {stats['date']}")
    print(f"Appels API: {stats['total_calls']}")
    print(f"Coût total: ${stats['total_cost']:.4f}")
    print(f"Tokens: {stats['total_tokens']:,}")
    print(f"Sessions: {stats['total_sessions']}")
    print(f"Temps moyen: {stats['avg_processing_time']:.2f}s")
    
    if stats.get('providers'):
        print("\nPar provider:")
        for provider, provider_stats in stats['providers'].items():
            print(f"  {provider}: {provider_stats['calls']} appels, ${provider_stats['cost']:.4f}")

def afficher_historique_fichiers():
    """Affiche l'historique des 10 derniers fichiers"""
    print("\n" + "="*50)
    print("📁 HISTORIQUE DES FICHIERS")
    print("="*50)
    
    history = cost_tracker.get_file_history(10)
    
    if not history:
        print("Aucun fichier traité")
        return
    
    print(f"{'Fichier':<25} {'Date':<16} {'Appels':<7} {'Coût':<12} {'Statut'}")
    print("-" * 70)
    
    for session in history:
        file_name = session['file_name'][:24]
        timestamp = session['timestamp'][:16]
        calls = session['total_api_calls']
        cost = session['total_cost']
        status = "✅" if session['success'] else "❌"
        
        print(f"{file_name:<25} {timestamp:<16} {calls:<7} ${cost:<11.4f} {status}")

def generer_rapport_detaille():
    """Génère un rapport détaillé des 7 derniers jours"""
    print("\n" + "="*50)
    print("📋 RAPPORT DÉTAILLÉ (7 derniers jours)")
    print("="*50)
    
    from datetime import datetime, timedelta
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    stats = cost_tracker.export_statistics(start_date, end_date)
    
    global_stats = stats.get('global_stats', {})
    print(f"Période: {start_date} au {end_date}")
    print(f"Appels totaux: {global_stats.get('total_calls', 0):,}")
    print(f"Coût total: ${global_stats.get('total_cost', 0.0):.4f}")
    print(f"Tokens: {global_stats.get('total_tokens', 0):,}")
    print(f"Fichiers: {global_stats.get('total_files', 0)}")
    
    if stats.get('top_models'):
        print(f"\nTop 5 modèles:")
        for i, model in enumerate(stats['top_models'][:5], 1):
            print(f"  {i}. {model['provider']}/{model['model']}")
            print(f"     {model['calls']} appels, ${model['cost']:.4f}")

def tester_calcul_couts():
    """Teste les calculs de coûts pour différents providers"""
    print("\n" + "="*50)
    print("🧮 TEST DES CALCULS DE COÛTS")
    print("="*50)
    
    # Simulation d'usage
    usage_example = {
        'prompt_tokens': 1000,
        'completion_tokens': 500,
        'total_tokens': 1500
    }
    
    providers_models = [
        ('openrouter', 'openai/gpt-4o'),
        ('openrouter', 'openai/gpt-4o-mini'),
        ('openrouter', 'anthropic/claude-3-5-sonnet'),
        ('openai', 'gpt-4o'),
        ('anthropic', 'claude-3-5-sonnet-20241022'),
        ('ollama', 'default')
    ]
    
    print(f"Usage test: {usage_example['prompt_tokens']} prompt + {usage_example['completion_tokens']} completion tokens")
    print()
    
    for provider, model in providers_models:
        costs = cost_tracker.calculate_cost(provider, model, usage_example)
        print(f"{provider}/{model}:")
        print(f"  Coût total: ${costs['total_cost']:.6f}")
        print(f"  Prompt: ${costs['cost_prompt']:.6f} | Completion: ${costs['cost_completion']:.6f}")
        print()

def main():
    """Fonction principale de démonstration"""
    print("🚀 DÉMO DU SYSTÈME DE TRACKING DES COÛTS API")
    print("=" * 60)
    
    # 1. Tester les calculs de coûts
    tester_calcul_couts()
    
    # 2. Simuler le traitement d'un fichier
    fichier_test = "test_commande.pdf"
    exemple_traitement_avec_couts(fichier_test)
    
    # 3. Afficher les statistiques
    afficher_statistiques_quotidiennes()
    
    # 4. Afficher l'historique
    afficher_historique_fichiers()
    
    # 5. Générer un rapport détaillé
    generer_rapport_detaille()
    
    print("\n✅ Démonstration terminée!")
    print("\n💡 Pour intégrer dans votre app:")
    print("1. Utilisez cost_tracker.start_session() au début du traitement")
    print("2. Passez session_id aux appels llm_manager.call_llm()")
    print("3. Utilisez cost_tracker.end_session() à la fin")
    print("4. Affichez les coûts avec cost_display_widget.py")

if __name__ == "__main__":
    main()