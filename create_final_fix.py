#!/usr/bin/env python3
"""
Patch final pour corriger tous les problèmes de la version portable
"""

import shutil
from pathlib import Path

def create_final_portable_fix():
    """Créer tous les fichiers manquants pour la version portable"""
    
    print("🔧 PATCH FINAL POUR VERSION PORTABLE")
    print("=" * 50)
    
    base_path = Path.cwd()
    portable_path = base_path / "dist_portable_update_ready"
    
    # 1. Créer enhanced_processing_ui.py minimal
    enhanced_processing_ui_content = '''#!/usr/bin/env python3
"""
Enhanced Processing UI - Version minimale pour compatibilité
"""

from PyQt6.QtWidgets import QWidget

class EnhancedProcessingUI(QWidget):
    """Interface de traitement améliorée - Version minimale"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
    
    def apply_enhancements(self):
        """Appliquer les améliorations - Version minimale"""
        pass
    
    def setup_progress_display(self):
        """Configuration de l'affichage de progression - Version minimale"""
        pass

# Variables d'export pour compatibilité
ENHANCED_PROCESSING_AVAILABLE = False

def create_enhanced_processing_widget(parent=None):
    """Créer un widget de traitement amélioré"""
    return EnhancedProcessingUI(parent)

if __name__ == "__main__":
    print("Enhanced Processing UI - Version minimale")
'''
    
    enhanced_file = portable_path / "enhanced_processing_ui.py"
    with open(enhanced_file, 'w', encoding='utf-8') as f:
        f.write(enhanced_processing_ui_content)
    print("✅ enhanced_processing_ui.py créé")
    
    # 2. Créer une version simplifiée du système de logging avancé
    advanced_logging_simple = '''#!/usr/bin/env python3
"""
Système de logging avancé - Version simplifiée pour portable
"""

import logging
import sys
from pathlib import Path

def setup_advanced_logging(log_level=logging.INFO):
    """Configuration du logging avancé - Version simplifiée"""
    
    # Créer le répertoire logs
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Configuration basique
    logger = logging.getLogger("MATELAS")
    logger.setLevel(log_level)
    
    # Handler pour fichier
    try:
        file_handler = logging.FileHandler(logs_dir / "app.log", encoding='utf-8')
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Avertissement: Impossible de créer le fichier de log: {e}")
    
    # Handler pour console
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger

# Pour compatibilité
def get_advanced_logger():
    """Obtenir le logger avancé"""
    return logging.getLogger("MATELAS")

if __name__ == "__main__":
    logger = setup_advanced_logging()
    logger.info("Système de logging avancé initialisé")
'''
    
    # Ajouter le logging à app_gui.py directement
    app_gui_logging_fix = '''
# === AJOUT LOGGING POUR VERSION PORTABLE ===
import logging
from pathlib import Path

def setup_advanced_logging(log_level=logging.INFO):
    """Configuration du logging avancé - Version simplifiée portable"""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    logger = logging.getLogger("MATELAS")
    logger.setLevel(log_level)
    
    # Handler fichier
    try:
        file_handler = logging.FileHandler(logs_dir / "app.log", encoding='utf-8')
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except Exception:
        pass
    
    return logger
# === FIN AJOUT LOGGING ===

'''
    
    # 3. Patcher app_gui.py pour corriger les imports manquants
    app_gui_file = portable_path / "app_gui.py"
    
    if app_gui_file.exists():
        print("🔧 Correction de app_gui.py...")
        
        # Lire le contenu actuel
        with open(app_gui_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Corrections à appliquer
        fixes = [
            # 1. Ajouter la fonction de logging directement
            ("import logging", f"import logging{app_gui_logging_fix}"),
            
            # 2. Corriger l'import enhanced_processing_ui
            ("ENHANCED_PROCESSING_AVAILABLE = True", "ENHANCED_PROCESSING_AVAILABLE = False"),
            
            # 3. Gérer l'absence de modules optionnels
            ("from enhanced_processing_ui import", "# from enhanced_processing_ui import"),
        ]
        
        # Appliquer les corrections
        for old, new in fixes:
            if old in content:
                content = content.replace(old, new)
        
        # Écrire le fichier corrigé
        with open(app_gui_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ app_gui.py corrigé")
    
    # 4. Créer un fichier de dépendances minimales
    requirements_minimal = """# Dépendances minimales MATELAS v3.11.12 Portable
PyQt6>=6.5.0
requests>=2.25.0
PyMuPDF>=1.20.0
openpyxl>=3.0.0
paramiko>=2.7.0
cryptography>=3.0.0
"""
    
    req_file = portable_path / "requirements_minimal.txt"
    with open(req_file, 'w', encoding='utf-8') as f:
        f.write(requirements_minimal)
    print("✅ requirements_minimal.txt créé")
    
    # 5. Créer un script de lancement simplifié pour tests
    simple_launcher = '''#!/usr/bin/env python3
"""
Lanceur simplifié MATELAS - Pour tests et dépannage
"""

import sys
import os
from pathlib import Path

def main():
    print("🚀 MATELAS v3.11.12 - Lanceur Simplifié")
    print("=" * 40)
    
    # Vérifications de base
    print(f"📂 Répertoire: {Path.cwd()}")
    print(f"🐍 Python: {sys.version}")
    
    # Test des imports critiques
    try:
        print("🔍 Test des imports...")
        import PyQt6
        print("  ✅ PyQt6")
        
        import requests
        print("  ✅ requests")
        
        import config
        print("  ✅ config")
        
        import version
        print("  ✅ version")
        
    except ImportError as e:
        print(f"  ❌ Import manquant: {e}")
        print("\\n🔧 Exécutez: python install.py")
        input("Appuyez sur Entrée...")
        return False
    
    # Lancer l'application
    print("\\n🚀 Lancement de l'application...")
    
    try:
        # Import et lancement
        from PyQt6.QtWidgets import QApplication
        
        # Créer l'application Qt
        app = QApplication(sys.argv)
        
        # Import de l'interface principale
        import app_gui
        
        # Lancer l'interface
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Erreur de lancement: {e}")
        print("\\n📋 Informations de débogage:")
        print(f"   • Répertoire: {os.getcwd()}")
        print(f"   • Python: {sys.executable}")
        
        # Afficher la trace complète
        import traceback
        traceback.print_exc()
        
        input("\\nAppuyez sur Entrée pour fermer...")
        return False

if __name__ == "__main__":
    main()
'''
    
    launcher_file = portable_path / "launch_simple.py"
    with open(launcher_file, 'w', encoding='utf-8') as f:
        f.write(simple_launcher)
    print("✅ launch_simple.py créé")
    
    # 6. Mettre à jour le script d'installation pour être plus robuste
    robust_install = '''#!/usr/bin/env python3
"""
Installation robuste MATELAS v3.11.12 - Version finale
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_python():
    """Vérifier Python et pip"""
    print("🐍 Vérification Python...")
    
    try:
        version_info = sys.version_info
        if version_info.major >= 3 and version_info.minor >= 8:
            print(f"   ✅ Python {version_info.major}.{version_info.minor}.{version_info.micro}")
        else:
            print(f"   ❌ Python trop ancien: {version_info.major}.{version_info.minor}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur Python: {e}")
        return False
    
    # Vérifier pip
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"], 
                            stdout=subprocess.DEVNULL)
        print("   ✅ pip disponible")
        return True
    except subprocess.CalledProcessError:
        print("   ❌ pip non disponible")
        return False

def install_package(package_name, description=""):
    """Installer un package avec gestion d'erreurs"""
    try:
        print(f"   📥 {package_name} {description}...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", package_name, "--user", "--quiet"
        ])
        print(f"   ✅ {package_name}")
        return True
    except subprocess.CalledProcessError:
        try:
            # Essayer sans --user
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package_name, "--quiet"
            ])
            print(f"   ✅ {package_name} (global)")
            return True
        except subprocess.CalledProcessError as e:
            print(f"   ❌ {package_name}: {e}")
            return False

def main():
    print("🚀 INSTALLATION MATELAS v3.11.12 - ROBUSTE")
    print("=" * 50)
    
    # Vérifier Python
    if not check_python():
        print("\\n❌ Python non compatible")
        input("Appuyez sur Entrée...")
        return False
    
    # Créer répertoires
    print("\\n📁 Création répertoires...")
    for dir_name in ["logs", "output", "temp_uploads", "data"]:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"   ✅ {dir_name}/")
    
    # Installation packages
    print("\\n📦 Installation dépendances...")
    packages = [
        ("PyQt6", "Interface graphique"),
        ("requests", "HTTP"),
        ("PyMuPDF", "PDF"),
        ("openpyxl", "Excel"),
        ("paramiko", "SFTP"),
        ("cryptography", "Sécurité")
    ]
    
    failed = []
    for package, desc in packages:
        if not install_package(package, desc):
            failed.append(package)
    
    # Résultats
    print(f"\\n📊 Résultats: {len(packages)-len(failed)}/{len(packages)} installés")
    
    if failed:
        print(f"❌ Échecs: {', '.join(failed)}")
        print("\\n🔧 Essayez:")
        print("   • Exécuter en tant qu'Administrateur")
        print("   • pip install --upgrade pip")
        for pkg in failed:
            print(f"   • pip install {pkg}")
    else:
        print("✅ Toutes les dépendances installées!")
    
    # Test final
    print("\\n🧪 Tests...")
    try:
        import PyQt6
        import config
        import version
        print("✅ Tests réussis!")
        print("\\n🚀 Pour lancer:")
        print("   python app_gui.py")
        print("   python launch_simple.py  (version dépannage)")
        print("   lancer_matelas.bat")
    except ImportError as e:
        print(f"❌ Test échoué: {e}")
    
    input("\\nAppuyez sur Entrée...")
    return len(failed) == 0

if __name__ == "__main__":
    main()
'''
    
    robust_install_file = portable_path / "install_robust.py"
    with open(robust_install_file, 'w', encoding='utf-8') as f:
        f.write(robust_install)
    print("✅ install_robust.py créé")
    
    print("\n" + "=" * 50)
    print("✅ PATCH FINAL APPLIQUÉ!")
    print("📦 Fichiers ajoutés/corrigés:")
    print("   • enhanced_processing_ui.py (minimal)")
    print("   • app_gui.py (logging intégré)")
    print("   • requirements_minimal.txt")
    print("   • launch_simple.py (lanceur dépannage)")
    print("   • install_robust.py (installation robuste)")
    
    return True

if __name__ == "__main__":
    create_final_portable_fix()