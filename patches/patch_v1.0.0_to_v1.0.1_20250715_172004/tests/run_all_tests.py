#!/usr/bin/env python3
"""
Script pour exécuter tous les tests de l'application Matelas
Utilisation: python tests/run_all_tests.py [options]
"""

import sys
import os
import subprocess
import argparse
import time
import json
from datetime import datetime
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuration des chemins
TESTS_DIR = Path(__file__).parent
PROJECT_ROOT = TESTS_DIR.parent
REPORTS_DIR = PROJECT_ROOT / "test_reports"

# Créer le répertoire de rapports s'il n'existe pas
REPORTS_DIR.mkdir(exist_ok=True)


def run_command(command, description=""):
    """Exécute une commande et retourne le résultat"""
    print(f"\n{'='*60}")
    print(f"Exécution: {description}")
    print(f"Commande: {' '.join(command)}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"Durée: {duration:.2f} secondes")
        print(f"Code de retour: {result.returncode}")
        
        if result.stdout:
            print("Sortie standard:")
            print(result.stdout)
        
        if result.stderr:
            print("Erreurs:")
            print(result.stderr)
        
        return {
            'success': result.returncode == 0,
            'duration': duration,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
        
    except Exception as e:
        print(f"Erreur lors de l'exécution: {e}")
        return {
            'success': False,
            'duration': 0,
            'stdout': '',
            'stderr': str(e),
            'returncode': -1
        }


def run_unit_tests(verbose=False, coverage=False):
    """Exécute les tests unitaires"""
    command = ["python3", "-m", "pytest", "tests/test_unitaires.py"]
    
    if verbose:
        command.append("-v")
    
    if coverage:
        command.extend([
            "--cov=backend",
            "--cov=config",
            "--cov-report=html:test_reports/coverage_html",
            "--cov-report=xml:test_reports/coverage.xml",
            "--cov-report=term-missing"
        ])
    
    return run_command(command, "Tests unitaires")


def run_integration_tests(verbose=False):
    """Exécute les tests d'intégration"""
    command = ["python3", "-m", "pytest", "tests/test_integration.py"]
    
    if verbose:
        command.append("-v")
    
    return run_command(command, "Tests d'intégration")


def run_performance_tests(verbose=False):
    """Exécute les tests de performance"""
    command = ["python3", "-m", "pytest", "tests/test_performance.py"]
    
    if verbose:
        command.append("-v")
    
    return run_command(command, "Tests de performance")


def run_regression_tests(verbose=False):
    """Exécute les tests de régression"""
    command = ["python3", "-m", "pytest", "tests/test_regression.py"]
    
    if verbose:
        command.append("-v")
    
    return run_command(command, "Tests de régression")


def run_all_tests(verbose=False, coverage=False):
    """Exécute tous les tests"""
    command = ["python3", "-m", "pytest", "tests/"]
    
    if verbose:
        command.append("-v")
    
    if coverage:
        command.extend([
            "--cov=backend",
            "--cov=config",
            "--cov-report=html:test_reports/coverage_html",
            "--cov-report=xml:test_reports/coverage.xml",
            "--cov-report=term-missing"
        ])
    
    return run_command(command, "Tous les tests")


def run_benchmark_performance():
    """Exécute le benchmark de performance"""
    command = ["python3", "tests/test_performance.py"]
    return run_command(command, "Benchmark de performance")


def run_regression_suite():
    """Exécute la suite de tests de régression"""
    command = ["python3", "tests/test_regression.py"]
    return run_command(command, "Suite de tests de régression")


def generate_test_report(results, output_file):
    """Génère un rapport de tests"""
    report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total_tests': len(results),
            'passed': sum(1 for r in results.values() if r['success']),
            'failed': sum(1 for r in results.values() if not r['success']),
            'total_duration': sum(r['duration'] for r in results.values())
        },
        'results': results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\nRapport généré: {output_file}")
    
    # Afficher le résumé
    print(f"\n{'='*60}")
    print("RÉSUMÉ DES TESTS")
    print(f"{'='*60}")
    print(f"Total des tests: {report['summary']['total_tests']}")
    print(f"Réussis: {report['summary']['passed']}")
    print(f"Échoués: {report['summary']['failed']}")
    print(f"Durée totale: {report['summary']['total_duration']:.2f} secondes")
    
    # Afficher les détails
    for test_name, result in results.items():
        status = "✅ RÉUSSI" if result['success'] else "❌ ÉCHOUÉ"
        print(f"{test_name}: {status} ({result['duration']:.2f}s)")


def install_test_dependencies():
    """Installe les dépendances nécessaires pour les tests"""
    print("Installation des dépendances de test...")
    
    dependencies = [
        "pytest",
        "pytest-asyncio",
        "pytest-cov",
        "pytest-html",
        "pytest-xdist"
    ]
    
    for dep in dependencies:
        command = ["pip", "install", dep]
        result = run_command(command, f"Installation de {dep}")
        if not result['success']:
            print(f"⚠️  Échec de l'installation de {dep}")


def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(
        description="Exécute les tests de l'application Matelas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python3 tests/run_all_tests.py --all                    # Tous les tests
  python3 tests/run_all_tests.py --unit --verbose         # Tests unitaires avec détails
  python3 tests/run_all_tests.py --performance            # Tests de performance
  python3 tests/run_all_tests.py --regression             # Tests de régression
  python3 tests/run_all_tests.py --coverage               # Avec couverture de code
  python3 tests/run_all_tests.py --install-deps           # Installer les dépendances
        """
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='Exécute tous les tests'
    )
    
    parser.add_argument(
        '--unit',
        action='store_true',
        help='Exécute les tests unitaires'
    )
    
    parser.add_argument(
        '--integration',
        action='store_true',
        help='Exécute les tests d\'intégration'
    )
    
    parser.add_argument(
        '--performance',
        action='store_true',
        help='Exécute les tests de performance'
    )
    
    parser.add_argument(
        '--regression',
        action='store_true',
        help='Exécute les tests de régression'
    )
    
    parser.add_argument(
        '--benchmark',
        action='store_true',
        help='Exécute le benchmark de performance'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Mode verbeux'
    )
    
    parser.add_argument(
        '--coverage',
        action='store_true',
        help='Génère un rapport de couverture de code'
    )
    
    parser.add_argument(
        '--install-deps',
        action='store_true',
        help='Installe les dépendances de test'
    )
    
    parser.add_argument(
        '--report',
        action='store_true',
        help='Génère un rapport JSON des résultats'
    )
    
    args = parser.parse_args()
    
    # Installation des dépendances si demandé
    if args.install_deps:
        install_test_dependencies()
        return
    
    # Si aucun argument spécifique, exécuter tous les tests
    if not any([args.all, args.unit, args.integration, args.performance, 
                args.regression, args.benchmark]):
        args.all = True
    
    print("🧪 TESTS DE L'APPLICATION MATELAS")
    print("=" * 60)
    
    results = {}
    start_time = time.time()
    
    try:
        # Tests unitaires
        if args.unit or args.all:
            results['Tests unitaires'] = run_unit_tests(args.verbose, args.coverage)
        
        # Tests d'intégration
        if args.integration or args.all:
            results['Tests d\'intégration'] = run_integration_tests(args.verbose)
        
        # Tests de performance
        if args.performance or args.all:
            results['Tests de performance'] = run_performance_tests(args.verbose)
        
        # Tests de régression
        if args.regression or args.all:
            results['Tests de régression'] = run_regression_tests(args.verbose)
        
        # Benchmark de performance
        if args.benchmark:
            results['Benchmark de performance'] = run_benchmark_performance()
        
        # Tous les tests (si demandé explicitement)
        if args.all and not any([args.unit, args.integration, args.performance, args.regression]):
            results['Tous les tests'] = run_all_tests(args.verbose, args.coverage)
        
        total_time = time.time() - start_time
        
        # Génération du rapport
        if args.report or args.coverage:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = REPORTS_DIR / f"test_report_{timestamp}.json"
            generate_test_report(results, report_file)
        
        # Résumé final
        print(f"\n{'='*60}")
        print("RÉSUMÉ FINAL")
        print(f"{'='*60}")
        print(f"Durée totale: {total_time:.2f} secondes")
        
        passed = sum(1 for r in results.values() if r['success'])
        failed = sum(1 for r in results.values() if not r['success'])
        
        if failed == 0:
            print("🎉 TOUS LES TESTS ONT RÉUSSI!")
        else:
            print(f"⚠️  {failed} test(s) ont échoué sur {len(results)}")
        
        # Code de retour approprié
        sys.exit(1 if failed > 0 else 0)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrompus par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erreur lors de l'exécution des tests: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 