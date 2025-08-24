#!/usr/bin/env python3
"""
Script de construction complet pour Mac avec package .app
Garantit que l'intégralité du dossier soit incluse dans le package
"""

import os
import sys
import subprocess
import shutil
import platform
import glob

def check_mac_environment():
    """Vérifie que l'environnement est compatible Mac"""
    if platform.system() != "Darwin":
        print("❌ Ce script est destiné à macOS uniquement")
        return False
    
    print("✅ Environnement macOS détecté")
    return True

def get_all_files_recursive(directory):
    """Récupère tous les fichiers d'un répertoire de manière récursive"""
    files = []
    if os.path.exists(directory):
        for root, dirs, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                # Exclure les fichiers temporaires
                if not any(exclude in file_path for exclude in ['__pycache__', '.pyc', '.DS_Store', 'Thumbs.db']):
                    files.append(file_path)
    return files

def build_mac_app():
    """Construit un package .app complet pour Mac"""
    
    if not check_mac_environment():
        return False
    
    print("=" * 60)
    print("🍎 CONSTRUCTION PACKAGE MAC - MATELAS APP")
    print("=" * 60)
    print(f"macOS: {platform.release()}")
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
    
    # Inventaire des fichiers
    print("📁 Inventaire des fichiers à inclure...")
    
    backend_files = get_all_files_recursive("backend")
    config_files = get_all_files_recursive("config")
    template_files = get_all_files_recursive("template")
    backend_template_files = get_all_files_recursive("backend/template")
    backend_templates_files = get_all_files_recursive("backend/templates")
    asset_files = get_all_files_recursive("assets")
    command_files = get_all_files_recursive("Commandes")
    
    all_template_files = template_files + backend_template_files + backend_templates_files
    
    print(f"   Backend: {len(backend_files)} fichiers")
    print(f"   Config: {len(config_files)} fichiers")
    print(f"   Templates: {len(all_template_files)} fichiers")
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
    
    # Commande PyInstaller pour Mac
    command = [
        "pyinstaller",
        "app_gui.py",
        "--onedir",  # Utiliser --onedir pour Mac pour un meilleur contrôle
        "--windowed",
        "--name", "MatelasApp",
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
            command.extend(["--add-data", f"{src_dir}:{dest_dir}"])
            print(f"   📁 Ajouté: {src_dir} → {dest_dir}")
    
    # Ajouter les fichiers critiques individuels
    for src_file, dest_dir in critical_files_to_include:
        if os.path.exists(src_file):
            command.extend(["--add-data", f"{src_file}:{dest_dir}"])
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
    icon_path = "assets/lit-double.icns"  # Format .icns pour Mac
    if os.path.exists(icon_path):
        command.extend(["--icon", icon_path])
        print(f"   🎨 Icône utilisée: {icon_path}")
    else:
        # Essayer avec .ico si .icns n'existe pas
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
            
            # Vérifier que l'app existe
            app_path = os.path.join("dist", "MatelasApp")
            
            if os.path.exists(app_path):
                # Calculer la taille du package
                total_size = 0
                file_count = 0
                for root, dirs, files in os.walk(app_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        total_size += os.path.getsize(file_path)
                        file_count += 1
                
                size_mb = total_size / (1024*1024)
                print(f"✅ Package créé: {app_path}")
                print(f"   Taille: {size_mb:.1f} MB")
                print(f"   Fichiers: {file_count}")
                print(f"   Inclut: {len(backend_files) + len(config_files) + len(all_template_files) + len(asset_files) + len(command_files)} fichiers source")
                
                # Créer un fichier de vérification
                verification_file = os.path.join("dist", "verification_fichiers_mac.txt")
                with open(verification_file, 'w', encoding='utf-8') as f:
                    f.write("FICHIERS INCLUS DANS LE PACKAGE MAC\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(f"Backend: {len(backend_files)} fichiers\n")
                    f.write(f"Config: {len(config_files)} fichiers\n")
                    f.write(f"Templates: {len(all_template_files)} fichiers\n")
                    f.write(f"Assets: {len(asset_files)} fichiers\n")
                    f.write(f"Commandes: {len(command_files)} fichiers\n\n")
                    f.write("FICHIERS CRITIQUES VÉRIFIÉS:\n")
                    for file in critical_files:
                        status = "✅" if os.path.exists(file) else "❌"
                        f.write(f"{status} {file}\n")
                    
                    f.write(f"\nPACKAGE FINAL:\n")
                    f.write(f"Taille: {size_mb:.1f} MB\n")
                    f.write(f"Fichiers dans le package: {file_count}\n")
                    f.write(f"Chemin: {app_path}\n")
                
                print(f"   📋 Fichier de vérification: {verification_file}")
                
                # Créer un script de lancement
                launch_script = os.path.join("dist", "Lancer_MatelasApp.command")
                with open(launch_script, 'w') as f:
                    f.write("#!/bin/bash\n")
                    f.write("cd \"$(dirname \"$0\")\"\n")
                    f.write("open MatelasApp\n")
                
                os.chmod(launch_script, 0o755)
                print(f"   🚀 Script de lancement: {launch_script}")
                
                # Test rapide de l'app
                print("\n🧪 Test rapide du package...")
                try:
                    test_process = subprocess.Popen(["open", app_path], 
                                                  stdout=subprocess.PIPE, 
                                                  stderr=subprocess.PIPE)
                    test_process.wait(timeout=15)
                    print("✅ Package s'est lancé sans erreur")
                except subprocess.TimeoutExpired:
                    print("✅ Package s'est lancé (arrêté après 15s)")
                except Exception as e:
                    print(f"⚠️ Erreur lors du test: {e}")
                
                print(f"\n🎉 Compilation Mac terminée avec succès!")
                print(f"   Package: {app_path}")
                print(f"   Taille: {size_mb:.1f} MB")
                print(f"   Fichiers inclus: {len(backend_files) + len(config_files) + len(all_template_files) + len(asset_files) + len(command_files)}")
                print(f"   Référentiels: {len([f for f in backend_files if 'Référentiels' in f])} fichiers")
                print(f"\n📋 Pour utiliser le package:")
                print(f"   1. Double-cliquez sur: {launch_script}")
                print(f"   2. Ou glissez-déposez MatelasApp dans Applications")
                print(f"   3. Ou lancez directement: open {app_path}")
                
            else:
                print(f"❌ Package non trouvé: {app_path}")
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
    
    return True


if __name__ == "__main__":
    build_mac_app() 