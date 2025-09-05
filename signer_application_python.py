#!/usr/bin/env python3
"""
Script Python pour signer l'application MatelasApp Windows
Supporte les certificats commerciaux et auto-signés
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

def check_windows():
    """Vérifie que nous sommes sur Windows"""
    if platform.system() != "Windows":
        print("❌ Ce script ne fonctionne que sur Windows")
        return False
    return True

def check_executable():
    """Vérifie que l'exécutable existe"""
    exe_path = Path("dist/MatelasApp.exe")
    if not exe_path.exists():
        print("❌ Exécutable non trouvé: dist/MatelasApp.exe")
        print("\nCompilez d'abord l'application avec:")
        print("  python build_universal.py")
        print("  ou")
        print("  build_simple.bat")
        return False
    print(f"✅ Exécutable trouvé: {exe_path}")
    return True

def check_tools():
    """Vérifie que les outils de signature sont disponibles"""
    tools = {
        'signtool': 'signtool',
        'makecert': 'makecert',
        'pvk2pfx': 'pvk2pfx'
    }
    
    missing_tools = []
    for tool_name, tool_cmd in tools.items():
        try:
            subprocess.run([tool_cmd], capture_output=True, check=False)
            print(f"✅ {tool_name} disponible")
        except FileNotFoundError:
            missing_tools.append(tool_name)
            print(f"❌ {tool_name} non trouvé")
    
    if missing_tools:
        print(f"\n📥 Installez Windows SDK ou Visual Studio Build Tools:")
        print("   https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/")
        return False
    
    return True

def create_self_signed_certificate():
    """Crée un certificat auto-signé"""
    print("\n🔐 Création du certificat auto-signé...")
    
    # Créer le dossier certificats
    cert_dir = Path("certificats")
    cert_dir.mkdir(exist_ok=True)
    
    try:
        # 1. Créer l'autorité de certification
        print("1. Création de l'autorité de certification...")
        ca_cmd = [
            'makecert', '-r', '-pe', '-n', 'CN=SCINNOVA MatelasApp CA',
            '-ss', 'CA', '-sr', 'CurrentUser', '-a', 'sha256', '-cy', 'end',
            '-sky', 'signature', '-sv', str(cert_dir / 'CA.pvk'), str(cert_dir / 'CA.cer')
        ]
        subprocess.run(ca_cmd, check=True)
        print("✅ Autorité de certification créée")
        
        # 2. Créer le certificat de signature
        print("2. Création du certificat de signature...")
        cert_cmd = [
            'makecert', '-pe', '-n', 'CN=SCINNOVA MatelasApp',
            '-ss', 'MY', '-a', 'sha256', '-cy', 'end', '-sky', 'signature',
            '-ic', str(cert_dir / 'CA.cer'), '-iv', str(cert_dir / 'CA.pvk'),
            '-sv', str(cert_dir / 'MatelasApp.pvk'), str(cert_dir / 'MatelasApp.cer')
        ]
        subprocess.run(cert_cmd, check=True)
        print("✅ Certificat de signature créé")
        
        # 3. Convertir en PFX
        print("3. Conversion en format PFX...")
        pfx_cmd = [
            'pvk2pfx', '-pvk', str(cert_dir / 'MatelasApp.pvk'),
            '-spc', str(cert_dir / 'MatelasApp.cer'),
            '-pfx', str(cert_dir / 'MatelasApp.pfx')
        ]
        subprocess.run(pfx_cmd, check=True)
        print("✅ Certificat PFX créé")
        
        return str(cert_dir / 'MatelasApp.pfx')
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la création du certificat: {e}")
        return None

def sign_executable(cert_path, password=None):
    """Signe l'exécutable avec le certificat"""
    print(f"\n🔐 Signature de l'exécutable avec {cert_path}...")
    
    try:
        # Commande de signature avec horodatage
        sign_cmd = [
            'signtool', 'sign', '/f', cert_path,
            '/t', 'http://timestamp.digicert.com', '/v', 'dist/MatelasApp.exe'
        ]
        
        if password:
            sign_cmd.extend(['/p', password])
        
        subprocess.run(sign_cmd, check=True)
        print("✅ Signature réussie!")
        
        # Vérifier la signature
        print("\n🔍 Vérification de la signature:")
        verify_cmd = ['signtool', 'verify', '/pa', 'dist/MatelasApp.exe']
        subprocess.run(verify_cmd)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la signature: {e}")
        return False

def commercial_certificate():
    """Gère la signature avec un certificat commercial"""
    print("\n🔐 Signature avec certificat commercial")
    print("=" * 50)
    
    cert_path = input("Chemin vers le certificat (.pfx): ").strip()
    if not cert_path:
        print("❌ Chemin du certificat requis")
        return False
    
    if not Path(cert_path).exists():
        print(f"❌ Fichier certificat non trouvé: {cert_path}")
        return False
    
    password = input("Mot de passe du certificat: ").strip()
    
    return sign_executable(cert_path, password)

def self_signed_certificate():
    """Gère la signature avec un certificat auto-signé"""
    print("\n🔐 Signature avec certificat auto-signé")
    print("=" * 50)
    
    cert_path = create_self_signed_certificate()
    if not cert_path:
        return False
    
    return sign_executable(cert_path)

def verify_signature():
    """Vérifie la signature de l'exécutable"""
    print("\n🔍 Vérification de la signature")
    print("=" * 50)
    
    try:
        # Vérification basique
        print("Vérification basique:")
        subprocess.run(['signtool', 'verify', '/pa', 'dist/MatelasApp.exe'])
        
        print("\nVérification détaillée:")
        subprocess.run(['signtool', 'verify', '/v', '/pa', 'dist/MatelasApp.exe'])
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la vérification: {e}")

def create_installer_script():
    """Crée un script d'installation du certificat"""
    print("\n📁 Création du script d'installation...")
    
    installer_content = '''@echo off
chcp 65001 >nul
echo ========================================
echo    INSTALLATION CERTIFICAT AUTO-SIGNÉ
echo    MatelasApp - SCINNOVA
echo ========================================
echo.

if not exist "MatelasApp.cer" (
    echo ❌ Certificat non trouvé: MatelasApp.cer
    echo Copiez ce script dans le dossier 'certificats'
    pause
    exit /b 1
)

echo ✅ Certificat trouvé: MatelasApp.cer
echo.

echo 🔐 Installation du certificat...
certmgr.exe -add -c "MatelasApp.cer" -s -r localMachine root

if %errorlevel% equ 0 (
    echo ✅ Certificat installé avec succès!
    echo L'application peut maintenant être exécutée sans alertes.
) else (
    echo ❌ Erreur lors de l'installation
    echo Exécutez en tant qu'administrateur.
)

pause
'''
    
    installer_path = Path("certificats/installer_certificat.bat")
    installer_path.parent.mkdir(exist_ok=True)
    
    with open(installer_path, 'w', encoding='utf-8') as f:
        f.write(installer_content)
    
    print(f"✅ Script créé: {installer_path}")

def main():
    """Fonction principale"""
    print("🔐 SIGNATURE APPLICATION WINDOWS - MATELASAPP")
    print("=" * 60)
    
    # Vérifications préalables
    if not check_windows():
        return
    
    if not check_executable():
        return
    
    if not check_tools():
        return
    
    # Menu principal
    while True:
        print("\n" + "=" * 50)
        print("MENU DE SIGNATURE")
        print("=" * 50)
        print("1. Certificat commercial")
        print("2. Certificat auto-signé")
        print("3. Vérifier la signature")
        print("4. Créer script d'installation")
        print("5. Quitter")
        print("=" * 50)
        
        choice = input("\nVotre choix (1-5): ").strip()
        
        if choice == '1':
            commercial_certificate()
        elif choice == '2':
            self_signed_certificate()
        elif choice == '3':
            verify_signature()
        elif choice == '4':
            create_installer_script()
        elif choice == '5':
            print("\n👋 Au revoir!")
            break
        else:
            print("❌ Choix invalide")
        
        input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main() 