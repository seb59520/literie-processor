#!/usr/bin/env python3
"""
Script de correction spécifique pour Windows - Problème clé API OpenRouter
"""

import os
import json
import sys
from pathlib import Path

def corriger_cles_windows():
    """Corrige le problème de clés API sous Windows"""
    
    print("🔧 CORRECTION CLÉS API WINDOWS")
    print("=" * 50)
    
    # 1. Vérifier et corriger le fichier de configuration
    home_dir = Path.home()
    config_file = home_dir / ".matelas_config.json"
    
    print(f"📁 Fichier de configuration: {config_file}")
    
    # Créer ou mettre à jour le fichier de configuration
    config_data = {}
    
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            print("✅ Fichier de configuration existant chargé")
        except Exception as e:
            print(f"⚠️  Erreur lecture fichier existant: {e}")
            print("📝 Création d'un nouveau fichier de configuration")
    
    # Demander la clé API OpenRouter
    print("\n🔑 CONFIGURATION DE LA CLÉ API OPENROUTER")
    print("-" * 40)
    
    current_key = config_data.get('openrouter_api_key', '')
    if current_key:
        print(f"Clé actuelle: {current_key[:10]}...")
        response = input("Voulez-vous modifier la clé API ? (o/n): ").lower().strip()
        if response != 'o':
            print("✅ Clé API conservée")
            return
    else:
        print("Aucune clé API configurée")
    
    # Demander la nouvelle clé
    new_key = input("Entrez votre clé API OpenRouter (sk-or-v1-...): ").strip()
    
    if not new_key:
        print("❌ Aucune clé fournie")
        return
    
    if not new_key.startswith('sk-or-v1-'):
        print("⚠️  Attention: La clé ne semble pas être au bon format OpenRouter")
        response = input("Continuer quand même ? (o/n): ").lower().strip()
        if response != 'o':
            return
    
    # Mettre à jour la configuration
    config_data['openrouter_api_key'] = new_key
    config_data['provider'] = 'openrouter'  # S'assurer que le provider est défini
    
    # Sauvegarder le fichier
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        print("✅ Fichier de configuration mis à jour")
    except Exception as e:
        print(f"❌ Erreur sauvegarde: {e}")
        return
    
    # 2. Créer un script batch pour définir la variable d'environnement
    print(f"\n🌍 CRÉATION DU SCRIPT BATCH WINDOWS")
    print("-" * 40)
    
    batch_content = f"""@echo off
REM Script pour définir la variable d'environnement OpenRouter
REM Exécutez ce script en tant qu'administrateur pour une définition permanente

echo Configuration de la variable d'environnement OPENROUTER_API_KEY...

REM Définir la variable pour la session actuelle
set OPENROUTER_API_KEY={new_key}

REM Définir la variable de manière permanente (nécessite les droits admin)
setx OPENROUTER_API_KEY "{new_key}"

echo.
echo Variable d'environnement configurée !
echo Redémarrez l'application pour que les changements prennent effet.
echo.
pause
"""
    
    batch_file = Path("configurer_openrouter_windows.bat")
    try:
        with open(batch_file, 'w', encoding='utf-8') as f:
            f.write(batch_content)
        print(f"✅ Script batch créé: {batch_file}")
    except Exception as e:
        print(f"❌ Erreur création script batch: {e}")
    
    # 3. Créer un script PowerShell alternatif
    print(f"\n💻 CRÉATION DU SCRIPT POWERSHELL")
    print("-" * 40)
    
    ps_content = f"""# Script PowerShell pour configurer OpenRouter
# Exécutez ce script en tant qu'administrateur

Write-Host "Configuration de la variable d'environnement OPENROUTER_API_KEY..." -ForegroundColor Green

# Définir la variable pour la session actuelle
$env:OPENROUTER_API_KEY = "{new_key}"

# Définir la variable de manière permanente
[Environment]::SetEnvironmentVariable("OPENROUTER_API_KEY", "{new_key}", "User")

Write-Host "Variable d'environnement configurée !" -ForegroundColor Green
Write-Host "Redémarrez l'application pour que les changements prennent effet." -ForegroundColor Yellow
Read-Host "Appuyez sur Entrée pour continuer"
"""
    
    ps_file = Path("configurer_openrouter_windows.ps1")
    try:
        with open(ps_file, 'w', encoding='utf-8') as f:
            f.write(ps_content)
        print(f"✅ Script PowerShell créé: {ps_file}")
    except Exception as e:
        print(f"❌ Erreur création script PowerShell: {e}")
    
    # 4. Tester la configuration
    print(f"\n🧪 TEST DE LA CONFIGURATION")
    print("-" * 40)
    
    try:
        import config
        api_key = config.get_openrouter_api_key()
        if api_key:
            print(f"✅ Test réussi: Clé API récupérée ({api_key[:10]}...)")
        else:
            print("❌ Test échoué: Aucune clé API récupérée")
    except Exception as e:
        print(f"❌ Erreur test: {e}")
    
    # 5. Instructions finales
    print(f"\n📋 INSTRUCTIONS FINALES")
    print("-" * 40)
    print("1. ✅ Clé API configurée dans ~/.matelas_config.json")
    print("2. 📝 Scripts de configuration créés:")
    print(f"   - {batch_file} (Batch)")
    print(f"   - {ps_file} (PowerShell)")
    print("3. 🔄 Redémarrez l'application")
    print("4. 🧪 Testez avec un fichier PDF")
    print("\n💡 Si le problème persiste:")
    print("   - Exécutez le script batch en tant qu'administrateur")
    print("   - Ou définissez manuellement la variable d'environnement")
    print("   - Vérifiez que la clé API est valide sur OpenRouter")

if __name__ == "__main__":
    corriger_cles_windows() 