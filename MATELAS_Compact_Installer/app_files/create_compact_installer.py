#!/usr/bin/env python3
"""
Créateur d'installateur portable COMPACT pour MATELAS
Version optimisée pour éviter les erreurs Windows de taille de fichier
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def create_compact_installer():
    """Crée un installateur portable compact"""
    
    print("📦 CRÉATION INSTALLATEUR PORTABLE COMPACT MATELAS")
    print("=" * 60)
    
    version = "3.10.3"
    app_name = "MATELAS_Processor"
    
    # Créer le dossier d'installation
    installer_dir = Path("MATELAS_Compact_Installer")
    if installer_dir.exists():
        shutil.rmtree(installer_dir)
    installer_dir.mkdir()
    
    print(f"📁 Créer installateur: {installer_dir}")
    
    # 1. Copier les fichiers de l'application
    app_files_dir = installer_dir / "app_files"
    app_files_dir.mkdir()
    
    source_dir = Path.cwd()
    files_copied = 0
    files_skipped = 0
    
    # Fichiers et dossiers à exclure pour réduire la taille
    exclude_patterns = {
        '__pycache__', '.pyc', '.git', '.DS_Store', 
        'admin_update_storage', 'backup_*', 'temp_*', 
        'MATELAS_Portable_Installer', 'MATELAS_Compact_Installer',
        '*.backup', 'logs', 'output', 'temp_uploads',
        'shared_update_storage', 'demo_update_storage',
        'demo_packages', 'build', 'dist', 'dist_portable',
        'backups', 'patches', 'test_*', 'rapport_*',
        '*.log', '*.pkl'
    }
    
    # Extensions de fichiers à exclure
    exclude_extensions = {'.log', '.pkl', '.db', '.backup'}
    
    # Taille limite pour les fichiers individuels (50MB)
    max_file_size = 50 * 1024 * 1024
    
    print("📂 Copie des fichiers essentiels...")
    
    for root, dirs, files in os.walk(source_dir):
        # Filtrer les dossiers
        dirs[:] = [d for d in dirs if not any(pattern in d for pattern in exclude_patterns)]
        
        for file in files:
            # Vérifier les patterns d'exclusion
            if any(pattern in file for pattern in exclude_patterns):
                files_skipped += 1
                continue
            
            # Vérifier les extensions
            if any(file.endswith(ext) for ext in exclude_extensions):
                files_skipped += 1
                continue
                
            source_file = Path(root) / file
            
            # Vérifier la taille du fichier
            try:
                if source_file.stat().st_size > max_file_size:
                    print(f"   ⚠️ Fichier trop gros ignoré: {file} ({source_file.stat().st_size / (1024*1024):.1f} MB)")
                    files_skipped += 1
                    continue
            except:
                continue
            
            rel_path = source_file.relative_to(source_dir)
            target_file = app_files_dir / rel_path
            
            target_file.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                shutil.copy2(source_file, target_file)
                files_copied += 1
                if files_copied % 50 == 0:
                    print(f"   ✅ {files_copied} fichiers copiés...")
            except Exception as e:
                files_skipped += 1
                continue
    
    print(f"✅ {files_copied} fichiers copiés, {files_skipped} fichiers ignorés")
    
    # 2. Créer script d'installation simple
    install_script_content = create_install_script(version, app_name)
    (installer_dir / "install.py").write_text(install_script_content, encoding='utf-8')
    
    # 3. Créer README compact
    readme_content = create_compact_readme(version, app_name)
    (installer_dir / "README.txt").write_text(readme_content, encoding='utf-8')
    
    # 4. Créer lanceurs
    create_launchers(installer_dir, version)
    
    # 5. Créer archive ZIP avec compression maximum
    zip_name = f"MATELAS_Compact_v{version}.zip"
    print(f"📦 Création de {zip_name} avec compression maximum...")
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        for file_path in installer_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(installer_dir.parent)
                zipf.write(file_path, arcname)
                
    zip_size_mb = Path(zip_name).stat().st_size / (1024*1024)
    
    print(f"\n🎉 INSTALLATEUR COMPACT CRÉÉ AVEC SUCCÈS!")
    print(f"📁 Dossier: {installer_dir}")
    print(f"📦 Archive: {zip_name} ({zip_size_mb:.1f} MB)")
    print(f"📊 Statistiques: {files_copied} fichiers, {files_skipped} ignorés")
    
    # Si l'archive fait plus de 1GB, proposer de la diviser
    if zip_size_mb > 1000:
        print(f"⚠️ Archive toujours volumineuse ({zip_size_mb:.1f} MB)")
        create_split_installer(installer_dir, version)
    else:
        print(f"✅ Taille optimale pour Windows (<1GB)")
    
    show_compact_instructions(version, zip_size_mb)
    
    return True

def create_split_installer(installer_dir, version):
    """Crée un installateur divisé en plusieurs parties"""
    print(f"\n🔄 CRÉATION D'INSTALLATEUR DIVISÉ...")
    
    # Diviser l'installateur en parties de 500MB max
    part_size = 500 * 1024 * 1024  # 500MB
    part_num = 1
    
    base_name = f"MATELAS_Split_v{version}"
    
    with zipfile.ZipFile(f"{base_name}_part1.zip", 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        current_size = 0
        
        # Ajouter les fichiers essentiels d'abord
        essential_files = ['install.py', 'README.txt', 'INSTALL.bat', 'install.sh']
        
        for essential in essential_files:
            file_path = installer_dir / essential
            if file_path.exists():
                zipf.write(file_path, f"{installer_dir.name}/{essential}")
                current_size += file_path.stat().st_size
        
        # Ensuite ajouter app_files en vérifiant la taille
        for file_path in (installer_dir / "app_files").rglob('*'):
            if file_path.is_file():
                file_size = file_path.stat().st_size
                
                if current_size + file_size > part_size and part_num == 1:
                    # Créer la partie suivante
                    part_num += 1
                    zipf.close()
                    zipf = zipfile.ZipFile(f"{base_name}_part{part_num}.zip", 'w', zipfile.ZIP_DEFLATED, compresslevel=9)
                    current_size = 0
                
                arcname = file_path.relative_to(installer_dir.parent)
                zipf.write(file_path, arcname)
                current_size += file_size
    
    print(f"📦 Installateur divisé en {part_num} parties de <500MB")
    
    # Créer script de reconstruction
    merge_script = f'''#!/usr/bin/env python3
"""Script de fusion des parties d'installation"""
import zipfile
import os
from pathlib import Path

def merge_installer():
    print("🔄 Fusion des parties d'installation...")
    parts = [f"{base_name}_part{{i}}.zip" for i in range(1, {part_num + 1})]
    
    # Vérifier que toutes les parties sont présentes
    for part in parts:
        if not Path(part).exists():
            print(f"❌ Partie manquante: {{part}}")
            return False
    
    # Extraire toutes les parties
    for part in parts:
        print(f"📦 Extraction de {{part}}...")
        with zipfile.ZipFile(part, 'r') as zipf:
            zipf.extractall(".")
    
    print("✅ Installation prête! Exécutez:")
    print("   Windows: cd {installer_dir.name} && python install.py")
    print("   Linux/Mac: cd {installer_dir.name} && python3 install.py")
    return True

if __name__ == "__main__":
    merge_installer()
'''
    
    (Path.cwd() / f"merge_{base_name}.py").write_text(merge_script)
    print(f"📝 Script de fusion créé: merge_{base_name}.py")

def create_launchers(installer_dir, version):
    """Crée les lanceurs pour l'installation"""
    # Windows
    windows_bat = f'''@echo off
echo MATELAS Compact Installer v{version}
echo.
python install.py
pause
'''
    (installer_dir / "INSTALL.bat").write_text(windows_bat, encoding='utf-8')
    
    # Unix
    unix_sh = f'''#!/bin/bash
echo "MATELAS Compact Installer v{version}"
echo ""
python3 install.py
read -p "Appuyez sur Entree pour fermer..."
'''
    install_sh = installer_dir / "install.sh"
    install_sh.write_text(unix_sh, encoding='utf-8')
    
    try:
        install_sh.chmod(0o755)
    except:
        pass

def create_install_script(version, app_name):
    """Crée le script d'installation"""
    return '''#!/usr/bin/env python3
"""
Installateur portable MATELAS COMPACT v''' + version + '''
Installation autonome sans droits administrateur
"""

import os
import sys
import shutil
from pathlib import Path

def main():
    print("🚀 INSTALLATION PORTABLE MATELAS COMPACT v''' + version + '''")
    print("=" * 55)
    
    # Détecter l'OS
    import platform
    os_name = platform.system()
    print("💻 OS détecté: " + str(os_name))
    
    # Répertoire d'installation par défaut
    if os_name == "Windows":
        default_dir = Path.home() / "AppData" / "Local" / "''' + app_name + '''"
    elif os_name == "Darwin":
        default_dir = Path.home() / "Applications" / "''' + app_name + '''"
    else:
        default_dir = Path.home() / ".local" / "share" / "''' + app_name + '''"
    
    print("📁 Répertoire par défaut: " + str(default_dir))
    
    # Demander confirmation
    response = input("\\nInstaller dans " + str(default_dir) + "? [O/n]: ").strip().lower()
    
    if response in ['n', 'no', 'non']:
        custom_path = input("Entrez le chemin d'installation: ").strip()
        if custom_path:
            install_dir = Path(custom_path) / "''' + app_name + '''"
        else:
            install_dir = default_dir
    else:
        install_dir = default_dir
    
    print("\\n📦 Installation dans: " + str(install_dir))
    
    # Vérifier si le répertoire existe
    if install_dir.exists():
        response = input("⚠️ Le répertoire existe déjà. Continuer? [o/N]: ").strip().lower()
        if response not in ['o', 'oui', 'y', 'yes']:
            print("❌ Installation annulée")
            return
        try:
            shutil.rmtree(install_dir)
        except:
            pass
    
    # Créer le répertoire
    install_dir.mkdir(parents=True, exist_ok=True)
    
    # Copier les fichiers
    source_dir = Path(__file__).parent / "app_files"
    if not source_dir.exists():
        print("❌ Erreur: Fichiers d'installation non trouvés")
        return
    
    files_copied = 0
    print("\\n📂 Copie des fichiers...")
    
    try:
        for item in source_dir.rglob('*'):
            if item.is_file():
                rel_path = item.relative_to(source_dir)
                target_path = install_dir / rel_path
                
                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target_path)
                files_copied += 1
                
                if files_copied % 50 == 0:
                    print("   " + str(files_copied) + " fichiers copiés...")
        
        print("✅ " + str(files_copied) + " fichiers installés")
        
        # Créer lanceur
        create_launcher(install_dir, os_name)
        
        print("\\n🎉 INSTALLATION TERMINÉE!")
        print("📍 Application installée dans: " + str(install_dir))
        
        # Créer dossiers manquants si nécessaire
        (install_dir / "logs").mkdir(exist_ok=True)
        (install_dir / "output").mkdir(exist_ok=True)
        (install_dir / "temp_uploads").mkdir(exist_ok=True)
        
        print("📁 Dossiers de travail créés automatiquement")
        
        if os_name == "Windows":
            print("🚀 Pour démarrer: Double-cliquez sur " + str(install_dir / 'MATELAS.bat'))
        else:
            print("🚀 Pour démarrer: " + str(install_dir / 'start_matelas.sh'))
        
        print("\\n💡 Note: L'application créera automatiquement les fichiers")
        print("    de logs et de cache au premier démarrage.")
        
    except Exception as e:
        print("❌ Erreur d'installation: " + str(e))

def create_launcher(install_dir, os_name):
    """Crée les lanceurs selon l'OS"""
    if os_name == "Windows":
        bat_content = '@echo off\\ncd /d "' + str(install_dir) + '"\\npython app_gui.py\\npause'
        (install_dir / "MATELAS.bat").write_text(bat_content)
        
        # Tentative de raccourci bureau
        try:
            desktop = Path.home() / "Desktop"
            if desktop.exists():
                (desktop / "MATELAS.bat").write_text(bat_content)
                print("🖥️ Raccourci bureau créé")
        except:
            pass
    
    else:
        shell_content = '#!/bin/bash\\ncd "' + str(install_dir) + '"\\npython3 app_gui.py'
        shell_script = install_dir / "start_matelas.sh"
        shell_script.write_text(shell_content)
        try:
            shell_script.chmod(0o755)
        except:
            pass

if __name__ == "__main__":
    try:
        main()
        input("\\nAppuyez sur Entrée pour fermer...")
    except KeyboardInterrupt:
        print("\\n❌ Installation interrompue")
    except Exception as e:
        print("\\n❌ Erreur: " + str(e))
        input("Appuyez sur Entrée pour fermer...")
'''

def create_compact_readme(version, app_name):
    """Crée un README compact"""
    return f'''MATELAS Compact Installer v{version}
======================================

INSTALLATION AUTONOME OPTIMISÉE POUR WINDOWS

Instructions d'installation:
---------------------------

1. Windows:
   - Double-cliquez sur INSTALL.bat
   
2. Mac/Linux:
   - Terminal: ./install.sh ou python3 install.py

3. Suivez les instructions à l'écran

Optimisations appliquées:
------------------------
✓ Fichiers de logs exclus (créés au runtime)
✓ Fichiers de cache exclus (générés automatiquement)  
✓ Dossiers de backup temporaires exclus
✓ Fichiers de test exclus
✓ Compression maximum appliquée

Répertoires d'installation:
--------------------------
- Windows: %LOCALAPPDATA%\\{app_name}
- macOS: ~/Applications/{app_name}
- Linux: ~/.local/share/{app_name}

Fonctionnalités:
---------------
✓ Installation portable (aucun droit admin)
✓ Système de mise à jour automatique intégré
✓ Interface PyQt6 moderne
✓ Traitement LLM automatique
✓ Export Excel intégré
✓ Compatible Windows/Mac/Linux
✓ Dossiers de travail créés automatiquement

Support:
--------
- Nécessite Python 3.8 ou supérieur
- Environ 500 MB d'espace disque
- Aucune connexion Internet requise pour l'installation
- Les logs et caches sont générés au premier démarrage

Version: {version}
Type: Installation portable compacte
Créé: {datetime.now().strftime("%Y-%m-%d")}
Optimisé pour: Windows (évite erreur 0x80070DF)
'''

def show_compact_instructions(version, zip_size_mb):
    """Affiche les instructions d'utilisation compactes"""
    print(f"\n📋 SOLUTION POUR L'ERREUR WINDOWS 0x80070DF:")
    print("=" * 50)
    print(f"✅ Archive compacte créée: {zip_size_mb:.1f} MB")
    print("✅ Compression maximum appliquée")
    print("✅ Fichiers non-essentiels exclus")
    print()
    print("🚀 DÉPLOIEMENT:")
    print(f"1. Copiez MATELAS_Compact_v{version}.zip")
    print("2. Décompressez sur le poste cible")
    print("3. Exécutez INSTALL.bat (Windows)")
    print("4. L'application créera automatiquement:")
    print("   • Dossier logs/")
    print("   • Dossier output/") 
    print("   • Dossier temp_uploads/")
    print("   • Cache LLM au premier usage")
    print()
    print("💡 AVANTAGES:")
    print("• Taille optimisée pour Windows")
    print("• Installation ultra-rapide")
    print("• Aucun fichier temporaire inclus")
    print("• Génération automatique des dossiers manquants")

if __name__ == "__main__":
    success = create_compact_installer()
    
    if success:
        print(f"\n✅ Installateur compact prêt pour Windows!")
    else:
        print(f"\n❌ Erreur de création")
        sys.exit(1)