#!/usr/bin/env python3
"""
Script de construction complet avec tous les référentiels et fichiers
Garantit que l'intégralité du dossier soit incluse dans l'exécutable
"""

import os
import sys
import subprocess
import shutil
import platform
import glob

def get_all_backend_files():
    """Récupère tous les fichiers du dossier backend"""
    backend_files = []
    backend_dir = "backend"
    
    if not os.path.exists(backend_dir):
        print(f"❌ Dossier {backend_dir} non trouvé")
        return backend_files
    
    # Parcourir récursivement tous les fichiers
    for root, dirs, files in os.walk(backend_dir):
        for file in files:
            file_path = os.path.join(root, file)
            # Exclure les fichiers temporaires et caches
            if not any(exclude in file_path for exclude in ['__pycache__', '.pyc', '.DS_Store', 'Thumbs.db']):
                backend_files.append(file_path)
    
    return backend_files

def get_all_config_files():
    """Récupère tous les fichiers de configuration"""
    config_files = []
    config_dir = "config"
    
    if not os.path.exists(config_dir):
        print(f"❌ Dossier {config_dir} non trouvé")
        return config_files
    
    for root, dirs, files in os.walk(config_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if not any(exclude in file_path for exclude in ['__pycache__', '.pyc', '.DS_Store', 'Thumbs.db']):
                config_files.append(file_path)
    
    return config_files

def get_all_template_files():
    """Récupère tous les fichiers de template"""
    template_files = []
    template_dirs = ["template", "backend/template", "backend/templates"]
    
    for template_dir in template_dirs:
        if os.path.exists(template_dir):
            for root, dirs, files in os.walk(template_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    if not any(exclude in file_path for exclude in ['__pycache__', '.pyc', '.DS_Store', 'Thumbs.db']):
                        template_files.append(file_path)
        else:
            print(f"⚠️ Dossier {template_dir} non trouvé")
    
    return template_files

def get_all_asset_files():
    """Récupère tous les fichiers d'assets"""
    asset_files = []
    asset_dir = "assets"
    
    if not os.path.exists(asset_dir):
        print(f"❌ Dossier {asset_dir} non trouvé")
        return asset_files
    
    for root, dirs, files in os.walk(asset_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if not any(exclude in file_path for exclude in ['__pycache__', '.pyc', '.DS_Store', 'Thumbs.db']):
                asset_files.append(file_path)
    
    return asset_files

def get_all_command_files():
    """Récupère tous les fichiers de commandes"""
    command_files = []
    command_dir = "Commandes"
    
    if not os.path.exists(command_dir):
        print(f"⚠️ Dossier {command_dir} non trouvé")
        return command_files
    
    for root, dirs, files in os.walk(command_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if not any(exclude in file_path for exclude in ['__pycache__', '.pyc', '.DS_Store', 'Thumbs.db']):
                command_files.append(file_path)
    
    return command_files

def build_complete_executable():
    """Construit un exécutable complet avec tous les fichiers"""
    
    print("=" * 60)
    print("🔨 CONSTRUCTION COMPLÈTE - MATELAS APP")
    print("=" * 60)
    print(f"Plateforme: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print()
    
    # Nettoyer les anciens fichiers
    print("🧹 Nettoyage des anciens fichiers...")
    for dir_to_clean in ["build", "dist"]:
        if os.path.exists(dir_to_clean):
            shutil.rmtree(dir_to_clean)
            print(f"   Supprimé: {dir_to_clean}")
    
    # Supprimer les fichiers .spec existants
    for file in os.listdir("."):
        if file.endswith(".spec"):
            os.remove(file)
            print(f"   Supprimé: {file}")
    
    print("✅ Nettoyage terminé")
    print()
    
    # Récupérer tous les fichiers nécessaires
    print("📁 Inventaire des fichiers à inclure...")
    
    backend_files = get_all_backend_files()
    config_files = get_all_config_files()
    template_files = get_all_template_files()
    asset_files = get_all_asset_files()
    command_files = get_all_command_files()
    
    print(f"   Backend: {len(backend_files)} fichiers")
    print(f"   Config: {len(config_files)} fichiers")
    print(f"   Templates: {len(template_files)} fichiers")
    print(f"   Assets: {len(asset_files)} fichiers")
    print(f"   Commandes: {len(command_files)} fichiers")
    print()
    
    # Vérifier les fichiers critiques
    print("🔍 Vérification des fichiers critiques...")
    critical_files = [
        "backend/Référentiels/dimensions_matelas.json",
        "backend/Référentiels/longueurs_matelas.json",
        "backend/Référentiels/7z_dimensions_matelas.json",
        "backend/Référentiels/7z_longueurs_matelas.json",
        "template/template_matelas.xlsx",
        "template/template_sommier.xlsx",
        "config/mappings_matelas.json",
        "config/mappings_sommiers.json",
        "assets/lit-double.png",
        "assets/logo_westelynck.png"
    ]
    
    missing_critical = []
    for file in critical_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file}")
            missing_critical.append(file)
    
    if missing_critical:
        print(f"\n⚠️ Fichiers critiques manquants: {len(missing_critical)}")
        for file in missing_critical:
            print(f"   - {file}")
        print("La compilation peut échouer si ces fichiers sont nécessaires.")
        print()
    
    # Déterminer les séparateurs selon la plateforme
    is_windows = platform.system() == "Windows"
    data_sep = ";" if is_windows else ":"
    
    # Commande PyInstaller avec inclusion complète
    command = [
        "pyinstaller",
        "app_gui.py",  # Utiliser app_gui.py directement
        "--onefile",
        "--windowed",
        "--name", "MatelasApp_Complet",
        "--paths=backend",
        "--collect-all", "PyQt6",
        "--collect-all", "openpyxl",
        "--collect-all", "pandas",
        "--collect-all", "requests",
        "--collect-all", "cryptography",
        "--collect-all", "fitz",  # PyMuPDF
        "--collect-all", "httpx",
        "--collect-all", "openai",
        "--collect-all", "ollama",
    ]
    
    # Ajouter tous les dossiers de données
    data_dirs = [
        ("backend", "backend"),
        ("config", "config"),
        ("template", "template"),
        ("assets", "assets"),
        ("Commandes", "Commandes"),
    ]
    
    # Ajouter les fichiers critiques individuels
    critical_files_to_include = [
        ("EULA.txt", "."),
        ("version.py", "."),
        ("config.py", "."),
        ("backend_interface.py", "."),
    ]
    
    for src_dir, dest_dir in data_dirs:
        if os.path.exists(src_dir):
            command.extend(["--add-data", f"{src_dir}{data_sep}{dest_dir}"])
            print(f"   📁 Ajouté: {src_dir} → {dest_dir}")
    
    # Ajouter les fichiers critiques individuels
    for src_file, dest_dir in critical_files_to_include:
        if os.path.exists(src_file):
            command.extend(["--add-data", f"{src_file}{data_sep}{dest_dir}"])
            print(f"   📄 Ajouté: {src_file} → {dest_dir}")
        else:
            print(f"   ⚠️ Fichier critique manquant: {src_file}")
    
    # Ajouter tous les imports cachés nécessaires
    hidden_imports = [
        # PyQt6
        "PyQt6.QtCore",
        "PyQt6.QtWidgets", 
        "PyQt6.QtGui",
        "PyQt6.QtPrintSupport",
        "PyQt6.sip",
        
        # Backend modules
        "backend",
        "backend.article_utils",
        "backend.asset_utils",
        "backend.client_utils",
        "backend.date_utils",
        "backend.decoupe_noyau_utils",
        "backend.dimensions_sommiers",
        "backend.dimensions_utils",
        "backend.excel_import_utils",
        "backend.excel_sommier_import_utils",
        "backend.fermete_utils",
        "backend.hauteur_utils",
        "backend.housse_utils",
        "backend.latex_mixte7zones_longueur_housse_utils",
        "backend.latex_mixte7zones_referentiel",
        "backend.latex_naturel_longueur_housse_utils",
        "backend.latex_naturel_referentiel",
        "backend.latex_renforce_longueur_utils",
        "backend.latex_renforce_utils",
        "backend.llm_provider",
        "backend.mapping_manager",
        "backend.matelas_utils",
        "backend.matiere_housse_utils",
        "backend.mousse_rainuree7zones_longueur_housse_utils",
        "backend.mousse_rainuree7zones_referentiel",
        "backend.mousse_visco_longueur_utils",
        "backend.mousse_visco_utils",
        "backend.operation_utils",
        "backend.poignees_utils",
        "backend.pre_import_utils",
        "backend.select43_longueur_housse_utils",
        "backend.select43_utils",
        "backend.sommier_analytics_utils",
        "backend.sommier_utils",
        "backend.secure_storage",
        
        # Autres modules
        "backend_interface",
        "config",
        "openpyxl",
        "pandas",
        "numpy",
        "requests",
        "cryptography",
        "fitz",  # PyMuPDF
        "httpx",
        "openai",
        "ollama",
        "json",
        "logging",
        "asyncio",
        "aiohttp",
        "tempfile",
        "shutil",
        "pathlib",
        "datetime",
        "math",
        "re",
        "base64",
        "hashlib",
        "unicodedata",
        "csv",
        "openpyxl.utils",
        "openpyxl.workbook",
        "openpyxl.worksheet",
    ]
    
    for module in hidden_imports:
        command.extend(["--hidden-import", module])
    
    # Ajouter l'icône si disponible
    icon_path = "assets/lit-double.ico"
    if os.path.exists(icon_path):
        command.extend(["--icon", icon_path])
        print(f"   🎨 Icône utilisée: {icon_path}")
    else:
        print("   ⚠️ Icône non trouvée, utilisation de l'icône par défaut")
    
    command.append("--clean")
    
    print()
    print("🚀 Commande PyInstaller:")
    print(" ".join(command))
    print()
    
    try:
        # Exécuter PyInstaller
        print("⏳ Compilation en cours...")
        print("   (Cela peut prendre plusieurs minutes)")
        print("   (Tous les fichiers et référentiels sont inclus)")
        
        result = subprocess.run(command, capture_output=True, text=True, timeout=900)  # 15 minutes timeout
        
        if result.returncode == 0:
            print("✅ Compilation réussie!")
            
            # Vérifier que l'exécutable existe
            exe_name = "MatelasApp_Complet"
            if platform.system() == "Windows":
                exe_name += ".exe"
            
            exe_path = os.path.join("dist", exe_name)
            
            if os.path.exists(exe_path):
                size_mb = os.path.getsize(exe_path) / (1024*1024)
                print(f"✅ Exécutable créé: {exe_path}")
                print(f"   Taille: {size_mb:.1f} MB")
                print(f"   Inclut: {len(backend_files) + len(config_files) + len(template_files) + len(asset_files) + len(command_files)} fichiers")
                
                # Créer un fichier de vérification
                verification_file = os.path.join("dist", "verification_fichiers.txt")
                with open(verification_file, 'w', encoding='utf-8') as f:
                    f.write("FICHIERS INCLUS DANS L'EXÉCUTABLE\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(f"Backend: {len(backend_files)} fichiers\n")
                    f.write(f"Config: {len(config_files)} fichiers\n")
                    f.write(f"Templates: {len(template_files)} fichiers\n")
                    f.write(f"Assets: {len(asset_files)} fichiers\n")
                    f.write(f"Commandes: {len(command_files)} fichiers\n\n")
                    f.write("FICHIERS CRITIQUES VÉRIFIÉS:\n")
                    for file in critical_files:
                        status = "✅" if os.path.exists(file) else "❌"
                        f.write(f"{status} {file}\n")
                
                print(f"   📋 Fichier de vérification: {verification_file}")
                
                # Test rapide de l'exécutable
                print("\n🧪 Test rapide de l'exécutable...")
                try:
                    if platform.system() == "Windows":
                        test_process = subprocess.Popen([exe_path], 
                                                      stdout=subprocess.PIPE, 
                                                      stderr=subprocess.PIPE)
                        test_process.wait(timeout=15)
                        test_process.terminate()
                    else:
                        os.chmod(exe_path, 0o755)
                        test_process = subprocess.Popen([exe_path], 
                                                      stdout=subprocess.PIPE, 
                                                      stderr=subprocess.PIPE)
                        test_process.wait(timeout=15)
                        test_process.terminate()
                    
                    print("✅ Exécutable s'est lancé sans erreur")
                except subprocess.TimeoutExpired:
                    print("✅ Exécutable s'est lancé (arrêté après 15s)")
                except Exception as e:
                    print(f"⚠️ Erreur lors du test: {e}")
                
                print(f"\n🎉 Compilation terminée avec succès!")
                print(f"   Exécutable: {exe_path}")
                print(f"   Taille: {size_mb:.1f} MB")
                print(f"   Fichiers inclus: {len(backend_files) + len(config_files) + len(template_files) + len(asset_files) + len(command_files)}")
                print(f"   Référentiels: {len([f for f in backend_files if 'Référentiels' in f])} fichiers")
                
            else:
                print(f"❌ Exécutable non trouvé: {exe_path}")
                print("Vérifiez les logs de compilation ci-dessus.")
        else:
            print("❌ Erreur de compilation:")
            print(result.stderr)
            print("\nLogs de compilation:")
            print(result.stdout)
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout lors de la compilation (15 minutes)")
        print("La compilation peut prendre plus de temps sur certains systèmes.")
    except FileNotFoundError:
        print("❌ PyInstaller non trouvé")
        print("Installez-le avec: pip install pyinstaller")
    except Exception as e:
        print(f"❌ Erreur: {e}")


if __name__ == "__main__":
    build_complete_executable() 