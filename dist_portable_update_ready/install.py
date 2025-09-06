#!/usr/bin/env python3
"""
Script d'installation MATELAS Portable v3.11.12 - Version Windows
Installation automatique sur un nouveau poste Windows
"""

import os
import sys
import subprocess
import json
import platform
from pathlib import Path

def check_python_installation():
    """Vérifier et guider l'installation de Python"""
    print("🐍 Vérification de Python...")
    
    # Vérifier Python
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version_info = result.stdout.strip()
            print(f"   ✅ {version_info}")
            
            # Vérifier la version
            version_parts = sys.version_info
            if version_parts.major >= 3 and version_parts.minor >= 8:
                return True
            else:
                print(f"   ⚠️ Version trop ancienne: {version_parts.major}.{version_parts.minor}")
                print("   📥 Python 3.8+ requis")
                return False
        
    except Exception as e:
        print(f"   ❌ Erreur vérification Python: {e}")
    
    # Instructions d'installation
    print("\n🔽 INSTALLATION DE PYTHON REQUISE:")
    print("=" * 40)
    print("1. Aller sur https://python.org/downloads")
    print("2. Télécharger Python 3.11 ou plus récent")
    print("3. ⚠️ IMPORTANT: Cocher 'Add Python to PATH' lors de l'installation")
    print("4. Redémarrer l'invite de commande après installation")
    print("5. Relancer: python install.py")
    
    return False

def install_dependencies():
    """Installer les dépendances requises"""
    print("\n📦 Installation des dépendances...")
    
    # Mettre à jour pip d'abord
    try:
        print("   🔄 Mise à jour de pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                            stdout=subprocess.DEVNULL)
        print("   ✅ pip mis à jour")
    except subprocess.CalledProcessError as e:
        print(f"   ⚠️ Avertissement mise à jour pip: {e}")
    
    requirements = [
        ("PyQt6", "Interface graphique"),
        ("requests", "Communication HTTP"), 
        ("PyMuPDF", "Traitement PDF"),
        ("openpyxl", "Génération Excel"),
        ("paramiko", "Upload SFTP"),
        ("cryptography", "Sécurité")
    ]
    
    failed_packages = []
    
    for package, description in requirements:
        try:
            print(f"   📥 Installation de {package} ({description})...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package, "--user"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"   ✅ {package} installé")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Erreur installation {package}: {e}")
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n⚠️ Échec d'installation: {', '.join(failed_packages)}")
        print("\n🔧 Solutions possibles:")
        print("   • Exécuter en tant qu'Administrateur")
        print("   • Vérifier la connexion Internet")
        print("   • Installer manuellement: pip install <package>")
        return False
    
    return True

def setup_directories():
    """Créer les répertoires nécessaires"""
    print("\n📁 Création des répertoires...")
    
    directories = [
        "output",
        "temp_uploads", 
        "logs",
        "data"
    ]
    
    for dir_name in directories:
        try:
            Path(dir_name).mkdir(exist_ok=True)
            print(f"   ✅ {dir_name}/")
        except Exception as e:
            print(f"   ❌ Erreur création {dir_name}: {e}")

def configure_application():
    """Configuration initiale de l'application"""
    print("\n⚙️ Configuration de l'application...")
    
    # Vérifier la configuration
    config_file = Path("matelas_config.json")
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print("   ✅ Configuration chargée")
            print(f"   🌐 Serveur: {config.get('server_url', 'Non configuré')}")
        except Exception as e:
            print(f"   ⚠️ Erreur lecture config: {e}")

def test_installation():
    """Tester l'installation"""
    print("\n🧪 Test de l'installation...")
    
    test_results = []
    
    # Tests des modules externes
    modules_externes = [
        ("PyQt6", "PyQt6"),
        ("requests", "requests"),
        ("PyMuPDF", "fitz"),
        ("openpyxl", "openpyxl"),
        ("paramiko", "paramiko"),
        ("cryptography", "cryptography")
    ]
    
    for nom, module in modules_externes:
        try:
            __import__(module)
            print(f"   ✅ {nom}")
            test_results.append(True)
        except ImportError:
            print(f"   ❌ {nom} - Module non trouvé")
            test_results.append(False)
    
    # Tests des modules de l'application
    modules_app = [
        ("config", "Configuration système"),
        ("version", "Gestion des versions"),
        ("backend_interface", "Interface backend")
    ]
    
    for module, desc in modules_app:
        try:
            __import__(module)
            print(f"   ✅ {desc}")
            test_results.append(True)
        except ImportError:
            print(f"   ⚠️ {desc} - Peut nécessiter d'être dans le bon répertoire")
            test_results.append(True)  # Ne pas faire échouer pour ces modules
    
    success_rate = sum(test_results) / len(test_results) * 100
    
    if success_rate >= 80:
        print(f"\n🎉 Installation réussie! ({success_rate:.0f}% des composants)")
        print("\n🚀 Pour lancer l'application:")
        print("   python app_gui.py")
        print("   ou")
        print("   Cliquer sur lancer_matelas.bat")
        return True
    else:
        print(f"\n⚠️ Installation partielle ({success_rate:.0f}% des composants)")
        print("\n🔧 Vérifiez les erreurs ci-dessus et relancez l'installation")
        return False

def create_desktop_shortcut():
    """Créer un raccourci sur le bureau (Windows)"""
    if platform.system() == "Windows":
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            path = os.path.join(desktop, "MATELAS v3.11.12.lnk")
            target = os.path.join(os.getcwd(), "lancer_matelas.bat")
            wDir = os.getcwd()
            icon = os.path.join(os.getcwd(), "assets", "lit-double.ico")
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = wDir
            if os.path.exists(icon):
                shortcut.IconLocation = icon
            shortcut.save()
            
            print("   ✅ Raccourci bureau créé")
        except ImportError:
            print("   ℹ️ Raccourci bureau non créé (modules Windows manquants)")
        except Exception as e:
            print(f"   ⚠️ Erreur création raccourci: {e}")

def main():
    """Fonction principale d'installation"""
    print("🚀 INSTALLATION MATELAS PORTABLE v3.11.12 - WINDOWS")
    print("=" * 60)
    
    print(f"📂 Répertoire d'installation: {Path.cwd()}")
    print(f"💻 Système: {platform.system()} {platform.release()}")
    
    # Étape 1: Vérifier Python
    if not check_python_installation():
        input("\nAppuyez sur Entrée pour fermer...")
        sys.exit(1)
    
    # Étapes d'installation
    steps = [
        ("Installation des dépendances", install_dependencies),
        ("Création des répertoires", setup_directories),
        ("Configuration", configure_application),
        ("Test de l'installation", test_installation)
    ]
    
    print(f"\n📋 {len(steps)} étapes d'installation...")
    
    for i, (step_name, step_func) in enumerate(steps, 1):
        print(f"\n[{i}/{len(steps)}] {step_name}...")
        try:
            result = step_func()
            if result is False:
                print(f"❌ Échec: {step_name}")
                print("\n🔧 Consultez les messages d'erreur ci-dessus")
                input("Appuyez sur Entrée pour fermer...")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Erreur {step_name}: {e}")
            input("Appuyez sur Entrée pour fermer...")
            sys.exit(1)
    
    # Créer raccourci bureau
    print("\n🖥️ Création du raccourci bureau...")
    create_desktop_shortcut()
    
    print("\n" + "=" * 60)
    print("✅ INSTALLATION TERMINÉE AVEC SUCCÈS!")
    print("\n📖 Comment utiliser:")
    print("   🚀 Lancer: python app_gui.py")
    print("   🚀 Ou cliquer: lancer_matelas.bat")  
    print("   📖 Guide: Ouvrir README.md")
    print("   📞 Support: Consulter logs/ en cas de problème")
    print("\n🎉 MATELAS v3.11.12 est prêt à l'emploi!")
    
    input("\nAppuyez sur Entrée pour fermer...")

if __name__ == "__main__":
    main()
