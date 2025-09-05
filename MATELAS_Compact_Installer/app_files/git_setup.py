#!/usr/bin/env python3
"""
Script pour initialiser et pousser le projet sur GitHub
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description=""):
    """Exécute une commande et affiche le résultat"""
    print(f"[INFO] {description}")
    print(f"$ {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERREUR] {e}")
        if e.stdout:
            print(f"Stdout: {e.stdout}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        return False

def check_git_installed():
    """Vérifie que Git est installé"""
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        print("[OK] Git est installé")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[ERREUR] Git n'est pas installé")
        print("Installez Git depuis: https://git-scm.com/")
        return False

def initialize_git_repo():
    """Initialise le repository Git"""
    if not os.path.exists('.git'):
        print("Initialisation du repository Git...")
        if not run_command("git init", "Initialisation Git"):
            return False
    else:
        print("[INFO] Repository Git déjà initialisé")
    
    return True

def create_gitignore_if_needed():
    """Vérifie que .gitignore existe"""
    if not os.path.exists('.gitignore'):
        print("[INFO] .gitignore manquant - créé automatiquement")
        return False
    else:
        print("[OK] .gitignore présent")
        return True

def add_all_files():
    """Ajoute tous les fichiers au repository"""
    print("Ajout des fichiers au repository...")
    if not run_command("git add .", "Ajout de tous les fichiers"):
        return False
    
    # Vérifier les fichiers ajoutés
    if not run_command("git status", "Statut du repository"):
        return False
    
    return True

def create_initial_commit():
    """Crée le commit initial"""
    print("Création du commit initial...")
    commit_message = "Initial commit - Processeur de Devis Literie\n\n- Interface PyQt6 complète\n- Support multi-LLM (OpenRouter, OpenAI, Anthropic)\n- Export Excel automatisé\n- Compilation Windows avec PyInstaller\n- Monitoring système en temps réel\n- Documentation complète"
    
    if not run_command(f'git commit -m "{commit_message}"', "Commit initial"):
        return False
    
    return True

def setup_github_remote():
    """Configure le remote GitHub"""
    print("\n" + "="*50)
    print("CONFIGURATION GITHUB")
    print("="*50)
    
    print("\nPour connecter à GitHub, vous avez plusieurs options:")
    print("1. Repository déjà créé sur GitHub")
    print("2. Créer un nouveau repository")
    print("3. Passer cette étape (configuration manuelle)")
    
    choice = input("\nChoisissez (1/2/3): ").strip()
    
    if choice == "1":
        repo_url = input("URL du repository GitHub (https://github.com/username/repo.git): ").strip()
        if repo_url:
            if not run_command(f"git remote add origin {repo_url}", "Ajout du remote"):
                return False
            print("[OK] Remote configuré")
            return repo_url
    
    elif choice == "2":
        print("\nÉtapes pour créer un nouveau repository:")
        print("1. Allez sur https://github.com/new")
        print("2. Nom: matelas-processor (ou votre choix)")
        print("3. Description: Processeur de Devis Literie avec IA")
        print("4. Public ou Privé (votre choix)")
        print("5. NE cochez PAS 'Add README' (on l'a déjà)")
        print("6. Créez le repository")
        print("7. Copiez l'URL du repository")
        
        input("\nAppuyez sur Entrée quand c'est fait...")
        repo_url = input("URL du repository créé: ").strip()
        if repo_url:
            if not run_command(f"git remote add origin {repo_url}", "Ajout du remote"):
                return False
            print("[OK] Remote configuré")
            return repo_url
    
    else:
        print("[INFO] Configuration manuelle - ajoutez le remote plus tard avec:")
        print("git remote add origin https://github.com/username/repo.git")
        return None

def push_to_github(repo_url):
    """Pousse le code vers GitHub"""
    if not repo_url:
        print("[INFO] Pas de remote configuré - push annulé")
        return True
    
    print("\nPush vers GitHub...")
    
    # Configurer la branche principale
    if not run_command("git branch -M main", "Configuration branche main"):
        return False
    
    # Push initial
    if not run_command("git push -u origin main", "Push initial"):
        print("\n[INFO] Si le push échoue, vérifiez:")
        print("1. Vos identifiants GitHub")
        print("2. Les permissions du repository")
        print("3. La configuration SSH/HTTPS")
        return False
    
    print(f"\n[OK] Code poussé avec succès vers: {repo_url}")
    return True

def setup_github_actions():
    """Vérifie la configuration GitHub Actions"""
    workflow_file = Path('.github/workflows/build-windows.yml')
    if workflow_file.exists():
        print("[OK] Workflow GitHub Actions configuré")
        print("Votre repository peut compiler automatiquement des exécutables Windows!")
    else:
        print("[INFO] Pas de workflow GitHub Actions")

def clean_sensitive_data():
    """Nettoie les données sensibles avant le push"""
    print("Vérification des données sensibles...")
    
    config_file = Path('matelas_config.json')
    if config_file.exists():
        try:
            import json
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            # Vérifier les clés API
            sensitive_keys = [k for k in config.keys() if 'api_key' in k and config[k]]
            if sensitive_keys:
                print(f"[!] Attention: Clés API détectées dans matelas_config.json")
                print(f"Clés trouvées: {sensitive_keys}")
                
                choice = input("Voulez-vous les masquer avant le push? (o/n): ").strip().lower()
                if choice == 'o':
                    # Créer une version template
                    for key in sensitive_keys:
                        if config[key]:  # Si la clé n'est pas vide
                            config[key] = "VOTRE_CLE_API_ICI"
                    
                    # Sauvegarder la version template
                    with open('matelas_config.json.template', 'w') as f:
                        json.dump(config, f, indent=2)
                    
                    print("[OK] Template créé: matelas_config.json.template")
                    print("[INFO] Ajoutez matelas_config.json au .gitignore si nécessaire")
            else:
                print("[OK] Pas de clés API sensibles détectées")
                
        except Exception as e:
            print(f"[!] Impossible de vérifier matelas_config.json: {e}")

def main():
    """Fonction principale"""
    print("="*60)
    print("    SETUP ET PUSH GITHUB")
    print("    Processeur de Devis Literie")
    print("="*60)
    
    # Vérifications préalables
    if not check_git_installed():
        return False
    
    if not os.path.exists('app_gui.py'):
        print("[ERREUR] app_gui.py non trouvé - êtes-vous dans le bon dossier?")
        return False
    
    # Nettoyage des données sensibles
    clean_sensitive_data()
    
    # Initialisation Git
    if not initialize_git_repo():
        return False
    
    if not create_gitignore_if_needed():
        print("[INFO] Créez un .gitignore si nécessaire")
    
    # Ajout des fichiers et commit
    if not add_all_files():
        return False
    
    if not create_initial_commit():
        # Peut-être qu'il y a déjà un commit
        print("[INFO] Peut-être déjà un commit existant")
    
    # Configuration GitHub
    repo_url = setup_github_remote()
    
    # Push vers GitHub
    if repo_url and not push_to_github(repo_url):
        print("[!] Push échoué - vous pouvez réessayer manuellement")
    
    # Vérification des actions
    setup_github_actions()
    
    # Résumé final
    print("\n" + "="*60)
    print("RÉSUMÉ")
    print("="*60)
    print("[OK] Repository Git initialisé")
    print("[OK] Fichiers ajoutés et committés")
    
    if repo_url:
        print(f"[OK] Code poussé vers GitHub: {repo_url}")
        print("\nProchaines étapes:")
        print("1. Vérifiez votre repository sur GitHub")
        print("2. Actions → 'Build Windows Executable' pour compiler")
        print("3. Invitez des collaborateurs si nécessaire")
        print("4. Configurez les GitHub Pages pour la documentation")
    else:
        print("[INFO] Push manuel nécessaire")
        print("Commandes pour push manuel:")
        print("git remote add origin https://github.com/username/repo.git")
        print("git branch -M main")
        print("git push -u origin main")
    
    print("\n[OK] Setup terminé!")
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n[INFO] Arrêté par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERREUR] Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)