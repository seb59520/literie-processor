#!/usr/bin/env python3
"""
Tests automatisés pour la robustesse de l'application
"""

import unittest
import tempfile
import shutil
import os
import sys
import time
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from backend.advanced_logging import MatelasLogger, get_advanced_logger
    from backend.performance_monitor import PerformanceMonitor, get_performance_monitor
    from backend.auto_recovery import AutoRecoverySystem, RecoveryStrategy
    from backend.llm_cache import LLMCache
    from backend.file_validation import FileValidator, validate_pdf_file
except ImportError as e:
    print(f"Erreur d'import: {e}")
    sys.exit(1)

class TestAdvancedLogging(unittest.TestCase):
    """Tests pour le système de logging avancé"""
    
    def setUp(self):
        """Configuration des tests"""
        self.test_dir = tempfile.mkdtemp()
        self.logger = MatelasLogger(log_dir=self.test_dir)
    
    def tearDown(self):
        """Nettoyage après les tests"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_logger_creation(self):
        """Test la création des loggers"""
        self.assertIsNotNone(self.logger.app_logger)
        self.assertIsNotNone(self.logger.error_logger)
        self.assertIsNotNone(self.logger.perf_logger)
        self.assertIsNotNone(self.logger.llm_logger)
        self.assertIsNotNone(self.logger.processing_logger)
    
    def test_error_logging(self):
        """Test l'enregistrement des erreurs"""
        test_error = ValueError("Test error")
        context = {"file": "test.pdf", "user": "test_user"}
        
        self.logger.log_error(test_error, context)
        
        # Vérifier que le fichier d'erreur a été créé
        error_file = Path(self.test_dir) / "errors.log"
        self.assertTrue(error_file.exists())
        
        # Vérifier le contenu
        with open(error_file, 'r') as f:
            content = f.read()
            self.assertIn("ValueError", content)
            self.assertIn("Test error", content)
            self.assertIn("test.pdf", content)
    
    def test_performance_logging(self):
        """Test l'enregistrement des performances"""
        self.logger.log_performance("test_operation", 1.234, {"files": 3})
        
        perf_file = Path(self.test_dir) / "performance.log"
        self.assertTrue(perf_file.exists())
        
        with open(perf_file, 'r') as f:
            content = f.read()
            self.assertIn("test_operation", content)
            self.assertIn("1.234", content)
    
    def test_log_summary(self):
        """Test la génération de résumé des logs"""
        # Ajouter quelques logs
        self.logger.log_error(ValueError("Test 1"))
        self.logger.log_error(TypeError("Test 2"))
        
        summary = self.logger.get_log_summary()
        self.assertIn("period_hours", summary)
        self.assertIn("error_count", summary)

class TestPerformanceMonitor(unittest.TestCase):
    """Tests pour le moniteur de performance"""
    
    def setUp(self):
        """Configuration des tests"""
        self.test_file = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
        self.test_file.close()
        self.monitor = PerformanceMonitor(log_file=self.test_file.name)
    
    def tearDown(self):
        """Nettoyage après les tests"""
        os.unlink(self.test_file.name)
    
    def test_operation_monitoring(self):
        """Test le monitoring d'opération"""
        operation_id = "test_op_1"
        
        # Démarrer une opération
        self.monitor.start_operation(operation_id, "test_operation", {"test": "data"})
        self.assertIn(operation_id, self.monitor.active_operations)
        
        # Simuler du travail
        time.sleep(0.1)
        
        # Terminer l'opération
        self.monitor.end_operation(operation_id, success=True)
        self.assertNotIn(operation_id, self.monitor.active_operations)
        self.assertEqual(len(self.monitor.metrics_history), 1)
        
        # Vérifier les métriques
        metrics = self.monitor.metrics_history[0]
        self.assertEqual(metrics.operation, "test_operation")
        self.assertTrue(metrics.success)
        self.assertGreater(metrics.duration, 0.09)  # Au moins 0.1s
    
    def test_system_metrics(self):
        """Test les métriques système"""
        metrics = self.monitor.get_system_metrics()
        
        self.assertIn("timestamp", metrics)
        self.assertIn("cpu_percent", metrics)
        self.assertIn("memory_percent", metrics)
        self.assertIn("memory_used_mb", metrics)
    
    def test_operation_stats(self):
        """Test les statistiques d'opération"""
        # Ajouter plusieurs opérations
        for i in range(5):
            op_id = f"test_op_{i}"
            self.monitor.start_operation(op_id, "test_batch", {"batch": i})
            time.sleep(0.01)
            success = i < 4  # Une échec sur 5
            self.monitor.end_operation(op_id, success=success)
        
        stats = self.monitor.get_operation_stats("test_batch")
        
        self.assertEqual(stats["count"], 5)
        self.assertEqual(stats["success_rate"], 0.8)  # 4/5
        self.assertGreater(stats["avg_duration"], 0)

class TestAutoRecovery(unittest.TestCase):
    """Tests pour le système de récupération automatique"""
    
    def setUp(self):
        """Configuration des tests"""
        self.test_file = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
        self.test_file.close()
        self.recovery = AutoRecoverySystem(log_file=self.test_file.name)
    
    def tearDown(self):
        """Nettoyage après les tests"""
        os.unlink(self.test_file.name)
    
    def test_successful_recovery(self):
        """Test une récupération réussie"""
        call_count = 0
        
        def failing_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ConnectionError("Test connection error")
            return "success"
        
        # Tenter la récupération
        result = self.recovery.attempt_recovery("test_op", ConnectionError("Test error"), failing_function)
        
        self.assertEqual(result, "success")
        self.assertEqual(call_count, 3)  # 1 échec + 2 retry
    
    def test_recovery_failure(self):
        """Test une récupération qui échoue"""
        def always_failing_function():
            raise ConnectionError("Persistent error")
        
        # Doit lever l'erreur après épuisement des tentatives
        with self.assertRaises(ConnectionError):
            self.recovery.attempt_recovery("test_op", ConnectionError("Test error"), always_failing_function)
    
    def test_recovery_stats(self):
        """Test les statistiques de récupération"""
        # Simuler quelques tentatives
        try:
            self.recovery.attempt_recovery("test_1", ValueError("Test"), lambda: exec('raise ValueError()'))
        except:
            pass
        
        stats = self.recovery.get_recovery_stats()
        self.assertIn("total_attempts", stats)
        self.assertIn("success_rate", stats)

class TestIntegration(unittest.TestCase):
    """Tests d'intégration des systèmes de robustesse"""
    
    def setUp(self):
        """Configuration des tests"""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Nettoyage après les tests"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_llm_cache_robustness(self):
        """Test la robustesse du cache LLM"""
        cache = LLMCache(max_size=10, ttl_seconds=3600)
        
        # Test avec clé None
        result = cache.get(None)
        self.assertIsNone(result)
        
        # Test avec valeur None
        cache.set("test_key", None)
        result = cache.get("test_key")
        self.assertIsNone(result)
        
        # Test normal
        cache.set("valid_key", "valid_value")
        result = cache.get("valid_key")
        self.assertEqual(result, "valid_value")
    
    def test_file_validation_robustness(self):
        """Test la robustesse de la validation de fichiers"""
        validator = FileValidator({
            'max_file_size_mb': 10,
            'min_file_size_kb': 1,
            'max_pages': 50,
            'allowed_extensions': ['.pdf']
        })
        
        # Test avec fichier inexistant
        result = validate_pdf_file("/non/existent/file.pdf")
        self.assertFalse(result.is_valid)
        self.assertIn("n'existe pas", result.error_message)
        
        # Test avec chemin None
        result = validate_pdf_file(None)
        self.assertFalse(result.is_valid)

def run_robustness_tests():
    """Lance tous les tests de robustesse"""
    
    print("🧪 Lancement des tests de robustesse...")
    print("=" * 60)
    
    # Découvrir et lancer tous les tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    print("📊 Résultats des tests:")
    print(f"   Tests lancés: {result.testsRun}")
    print(f"   Succès: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"   Échecs: {len(result.failures)}")
    print(f"   Erreurs: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ Échecs:")
        for test, trace in result.failures:
            print(f"   - {test}: {trace.split('\\n')[-2] if trace else 'N/A'}")
    
    if result.errors:
        print("\n💥 Erreurs:")
        for test, trace in result.errors:
            print(f"   - {test}: {trace.split('\\n')[-2] if trace else 'N/A'}")
    
    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
    print(f"\n🎯 Taux de réussite: {success_rate:.1f}%")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_robustness_tests()
    sys.exit(0 if success else 1)