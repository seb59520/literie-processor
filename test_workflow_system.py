#!/usr/bin/env python3
"""
Test simple du système de workflow
"""

import time
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_workflow_engine():
    """Test le moteur de workflow"""
    print("🧪 Test du moteur de workflow...")
    
    try:
        from backend.workflow_engine import get_workflow_engine, Workflow, WorkflowTask
        
        # Créer le moteur
        engine = get_workflow_engine()
        print("✅ Moteur de workflow créé")
        
        # Démarrer le moteur
        engine.start()
        print("✅ Moteur démarré")
        
        # Créer une tâche simple
        def simple_task(message):
            print(f"Exécution tâche: {message}")
            time.sleep(1)
            return f"Résultat: {message}"
        
        # Créer un workflow de test
        workflow = Workflow(
            id="test_workflow",
            name="Test Simple",
            description="Test basique du système"
        )
        
        # Ajouter des tâches
        task1 = WorkflowTask(
            id="task1",
            name="Première tâche",
            function=simple_task,
            args=("Hello World",)
        )
        
        task2 = WorkflowTask(
            id="task2", 
            name="Deuxième tâche",
            function=simple_task,
            args=("Task 2",),
            depends_on=["task1"]
        )
        
        workflow.tasks.extend([task1, task2])
        
        # Soumettre le workflow
        workflow_id = engine.submit_workflow(workflow)
        print(f"✅ Workflow soumis: {workflow_id}")
        
        # Attendre la completion
        max_wait = 10
        waited = 0
        
        while waited < max_wait:
            status = engine.get_workflow_status(workflow_id)
            if status and status["status"] in ["completed", "failed"]:
                break
            time.sleep(1)
            waited += 1
            print(f"⏳ Attente... ({waited}s)")
        
        # Vérifier le résultat final
        final_status = engine.get_workflow_status(workflow_id)
        if final_status:
            print(f"📊 Statut final: {final_status['status']}")
            print(f"📊 Progression: {final_status['progress']:.1f}%")
        
        engine.stop()
        print("✅ Test workflow terminé")
        return True
        
    except Exception as e:
        print(f"❌ Erreur test workflow: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_batch_processor():
    """Test le processeur de lots"""
    print("\n🧪 Test du processeur de lots...")
    
    try:
        from backend.batch_processor import get_batch_processor
        
        # Créer le processeur
        processor = get_batch_processor()
        print("✅ Processeur de lots créé")
        
        # Créer des fichiers de test (simulation)
        test_files = [
            "/path/to/test1.pdf",
            "/path/to/test2.pdf", 
            "/path/to/test3.pdf"
        ]
        
        config = {
            "auto_retry": True,
            "priority": 5
        }
        
        # Créer un lot
        workflow_id = processor.create_pdf_processing_batch(
            test_files, 
            config, 
            "Lot de test",
            priority=5
        )
        
        print(f"✅ Lot créé: {workflow_id}")
        
        # Vérifier le statut
        time.sleep(2)
        batch_status = processor.get_batch_status("batch_" + workflow_id.split("_", 1)[1])
        
        if batch_status:
            print(f"📊 Statut du lot: {batch_status.get('workflow_status', {}).get('status', 'unknown')}")
        
        print("✅ Test batch processor terminé")
        return True
        
    except Exception as e:
        print(f"❌ Erreur test batch: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_monitoring():
    """Test le système de monitoring"""
    print("\n🧪 Test du système de monitoring...")
    
    try:
        from backend.workflow_monitor import get_workflow_monitor
        from backend.workflow_engine import get_workflow_engine
        
        engine = get_workflow_engine()
        monitor = get_workflow_monitor(engine)
        
        print("✅ Moniteur créé")
        
        # Démarrer le monitoring
        monitor.start_monitoring()
        print("✅ Monitoring démarré")
        
        # Obtenir les données dashboard
        dashboard_data = monitor.get_dashboard_data()
        print(f"📊 Workflows actifs: {dashboard_data['active_workflows']}")
        print(f"📊 Workflows aujourd'hui: {dashboard_data['workflows_today']}")
        
        monitor.stop_monitoring()
        print("✅ Test monitoring terminé")
        return True
        
    except Exception as e:
        print(f"❌ Erreur test monitoring: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Lance tous les tests"""
    print("🚀 Test du Système de Workflow Automatisé")
    print("=" * 60)
    
    results = []
    
    # Test 1: Moteur de workflow
    results.append(test_workflow_engine())
    
    # Test 2: Processeur de lots
    results.append(test_batch_processor())
    
    # Test 3: Système de monitoring
    results.append(test_monitoring())
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 Résultats des Tests:")
    
    success_count = sum(results)
    total_tests = len(results)
    
    print(f"   ✅ Succès: {success_count}/{total_tests}")
    print(f"   ❌ Échecs: {total_tests - success_count}/{total_tests}")
    print(f"   📈 Taux de réussite: {success_count/total_tests:.1%}")
    
    if success_count == total_tests:
        print("\n🎉 Tous les tests sont passés! Le système de workflow est opérationnel.")
        return True
    else:
        print(f"\n⚠️ {total_tests - success_count} test(s) ont échoué. Vérifiez les erreurs ci-dessus.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)