#!/usr/bin/env python3
"""
Script de diagnostic pour l'exécutable MatelasApp
Identifie les problèmes de lancement
"""

import os
import sys
import subprocess
import platform
import json

def check_executable():
    """Vérifie l'exécutable et ses dépendances"""
    
    print("=" * 50)
    print("DIAGNOSTIC EXÉCUTABLE MATELASAPP")
    print("=" * 50)
    print(f"Plateforme: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print()
    
    # Vérifier l'exécutable
    exe_name = "MatelasApp"
    if platform.system() == "Windows":
        exe_name += ".exe"
    
    exe_path = os.path.join("dist", exe_name)
    
    if not os.path.exists(exe_path):
        print(f"❌ Exécutable non trouvé: {exe_path}")
        print("Compilez d'abord l'application avec build_with_spec.py")
        return False
    
    print(f"✅ Exécutable trouvé: {exe_path}")
    size_mb = os.path.getsize(exe_path) / (1024*1024)
    print(f"   Taille: {size_mb:.1f} MB")
    print()
    
    # Test de lancement avec capture d'erreurs
    print("🧪 Test de lancement avec capture d'erreurs...")
    print()
    
    try:
        # Lancer l'exécutable et capturer la sortie
        if platform.system() == "Windows":
            # Windows - lancer avec console pour voir les erreurs
            test_command = [
                "cmd", "/c", 
                f'"{exe_path}" 2>&1'
            ]
        else:
            # macOS/Linux
            test_command = [exe_path]
        
        print(f"Commande de test: {' '.join(test_command)}")
        print()
        
        # Lancer avec timeout
        result = subprocess.run(
            test_command,
            capture_output=True,
            text=True,
            timeout=30,
            shell=True if platform.system() == "Windows" else False
        )
        
        print("📋 Sortie standard:")
        print(result.stdout)
        print()
        
        if result.stderr:
            print("❌ Erreurs détectées:")
            print(result.stderr)
            print()
        
        if result.returncode == 0:
            print("✅ Exécutable s'est lancé et terminé normalement")
        else:
            print(f"⚠️ Exécutable s'est terminé avec le code: {result.returncode}")
            
    except subprocess.TimeoutExpired:
        print("✅ Exécutable s'est lancé (arrêté après 30s)")
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        print()
        
        # Test alternatif pour Windows
        if platform.system() == "Windows":
            print("🔄 Test alternatif pour Windows...")
            try:
                # Lancer directement l'exécutable
                process = subprocess.Popen(
                    [exe_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # Attendre un peu
                import time
                time.sleep(5)
                
                # Vérifier si le processus existe encore
                if process.poll() is None:
                    print("✅ Exécutable semble fonctionner (processus actif)")
                    process.terminate()
                else:
                    stdout, stderr = process.communicate()
                    print(f"❌ Exécutable s'est arrêté")
                    if stdout:
                        print("Sortie:", stdout)
                    if stderr:
                        print("Erreurs:", stderr)
                        
            except Exception as e2:
                print(f"❌ Erreur lors du test alternatif: {e2}")
    
    print()
    print("🔍 Vérification des assets dans l'exécutable...")
    
    # Vérifier si les assets sont inclus
    try:
        if platform.system() == "Windows":
            # Sur Windows, on peut vérifier avec 7zip ou un outil similaire
            print("ℹ️ Sur Windows, vérifiez manuellement que les assets sont inclus")
        else:
            # Sur macOS/Linux, on peut extraire temporairement
            import tempfile
            import shutil
            
            with tempfile.TemporaryDirectory() as temp_dir:
                # Copier l'exécutable
                temp_exe = os.path.join(temp_dir, exe_name)
                shutil.copy2(exe_path, temp_exe)
                
                # Rendre exécutable
                os.chmod(temp_exe, 0o755)
                
                # Lancer avec variables d'environnement de debug
                env = os.environ.copy()
                env['PYTHONPATH'] = temp_dir
                
                result = subprocess.run(
                    [temp_exe],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    env=env
                )
                
                if result.stderr:
                    print("Erreurs détectées:")
                    print(result.stderr)
                    
    except Exception as e:
        print(f"⚠️ Impossible de vérifier les assets: {e}")
    
    print()
    print("💡 Solutions possibles:")
    print("1. Vérifiez que tous les assets existent avant compilation")
    print("2. Essayez de lancer l'exécutable depuis le dossier dist/")
    print("3. Vérifiez les permissions d'exécution")
    print("4. Sur Windows, essayez de lancer en tant qu'administrateur")
    print("5. Vérifiez que tous les modules backend sont correctement importés")
    
    return True

def check_assets():
    """Vérifie que tous les assets nécessaires existent"""
    
    print("=" * 50)
    print("VÉRIFICATION DES ASSETS")
    print("=" * 50)
    
    required_assets = [
        "assets/lit-double.png",
        "assets/logo_westelynck.png",
        "template/template_matelas.xlsx",
        "template/template_sommier.xlsx",
        "config/mappings_matelas.json",
        "config/mappings_sommiers.json",
        "backend/Référentiels"
    ]
    
    missing_assets = []
    for asset in required_assets:
        if os.path.exists(asset):
            print(f"✅ {asset}")
        else:
            print(f"❌ {asset}")
            missing_assets.append(asset)
    
    if missing_assets:
        print(f"\n⚠️ Assets manquants: {len(missing_assets)}")
        for asset in missing_assets:
            print(f"   - {asset}")
        print("\nCes assets manquants peuvent causer des problèmes de lancement.")
    else:
        print("\n✅ Tous les assets sont présents")
    
    return len(missing_assets) == 0

if __name__ == "__main__":
    print("🔍 Diagnostic de l'exécutable MatelasApp")
    print()
    
    # Vérifier les assets
    assets_ok = check_assets()
    print()
    
    # Vérifier l'exécutable
    if assets_ok:
        check_executable()
    else:
        print("❌ Corrigez d'abord les assets manquants avant de tester l'exécutable") 