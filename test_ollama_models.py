#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier la liste des modèles Ollama
"""

import sys
import os
import subprocess
import json
import time

def test_ollama_installation():
    """Teste si Ollama est installé et accessible"""
    print("🤖 Test de l'installation d'Ollama")
    print("=" * 50)
    
    try:
        # Test de la version
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print(f"✅ Ollama installé: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Erreur Ollama: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ Ollama non installé ou non trouvé dans le PATH")
        print("💡 Pour installer Ollama: https://ollama.ai")
        return False
    except subprocess.TimeoutExpired:
        print("⚠️ Timeout lors de la vérification d'Ollama")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de la vérification d'Ollama: {e}")
        return False

def test_ollama_service():
    """Teste si le service Ollama est en cours d'exécution"""
    print("\n🔧 Test du service Ollama")
    print("=" * 50)
    
    try:
        # Test de connexion au service
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ Service Ollama en cours d'exécution")
            return True
        else:
            print(f"❌ Service Ollama non accessible: {result.stderr}")
            print("💡 Démarrez Ollama avec: ollama serve")
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️ Timeout lors de la connexion au service Ollama")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test du service: {e}")
        return False

def test_ollama_models_list():
    """Teste la liste des modèles Ollama avec différents timeouts"""
    print("\n📋 Test de la liste des modèles Ollama")
    print("=" * 50)
    
    timeouts = [30, 60, 120]  # Test avec différents timeouts
    
    for timeout in timeouts:
        print(f"\n⏱️ Test avec timeout de {timeout} secondes:")
        
        try:
            start_time = time.time()
            
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            if result.returncode == 0:
                try:
                    # Parser la sortie textuelle d'ollama list
                    lines = result.stdout.strip().split('\n')
                    model_names = []
                    
                    # Ignorer la première ligne (en-tête)
                    for line in lines[1:]:  # Skip header line
                        if line.strip():
                            # Nettoyer la ligne et extraire le nom du modèle
                            # Format: NAME                                  ID              SIZE      MODIFIED
                            line = line.strip()
                            
                            # Chercher l'ID (12 caractères hexadécimaux)
                            import re
                            id_match = re.search(r'([a-f0-9]{12})', line)
                            if id_match:
                                # Prendre tout ce qui est avant l'ID
                                id_pos = id_match.start()
                                model_name = line[:id_pos].strip()
                                if model_name:
                                    model_names.append(model_name)
                    
                    print(f"✅ Succès en {duration:.2f}s")
                    print(f"📊 {len(model_names)} modèles trouvés:")
                    
                    for i, model in enumerate(model_names[:5]):  # Afficher les 5 premiers
                        print(f"   {i+1}. {model}")
                    
                    if len(model_names) > 5:
                        print(f"   ... et {len(model_names) - 5} autres")
                    
                    # Retourner les modèles trouvés
                    return model_names
                        
                except Exception as e:
                    print(f"❌ Erreur de parsing: {e}")
                    print(f"Réponse brute: {result.stdout[:200]}...")
                    
            else:
                print(f"❌ Erreur (code {result.returncode}): {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"❌ Timeout après {timeout}s")
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")
    
    print("\n❌ Impossible de récupérer la liste des modèles avec tous les timeouts")
    return []

def test_ollama_model_info():
    """Teste les informations détaillées d'un modèle"""
    print("\n🔍 Test des informations de modèle")
    print("=" * 50)
    
    try:
        # Essayer de récupérer les infos du premier modèle disponible
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            # Parser la sortie textuelle d'ollama list
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:  # Au moins l'en-tête + 1 modèle
                # Extraire le nom du premier modèle
                first_line = lines[1]
                first_line = first_line.strip()
                
                # Chercher l'ID (12 caractères hexadécimaux)
                import re
                id_match = re.search(r'([a-f0-9]{12})', first_line)
                if id_match:
                    # Prendre tout ce qui est avant l'ID
                    id_pos = id_match.start()
                    model_name = first_line[:id_pos].strip()
                
                if model_name:
                    print(f"📋 Informations pour le modèle: {model_name}")
                    
                    # Afficher les détails du modèle (format tabulaire)
                    print(f"   • Nom: {model_name}")
                    
                    # Extraire l'ID et autres informations
                    id_match = re.search(r'([a-f0-9]{12})', first_line)
                    if id_match:
                        id_value = id_match.group(1)
                        print(f"   • ID: {id_value}")
                        
                        # Extraire la taille et la date
                        remaining = first_line[id_match.end():].strip()
                        size_match = re.search(r'(\d+(?:\.\d+)?\s*GB)', remaining)
                        if size_match:
                            print(f"   • Taille: {size_match.group(1)}")
                            
                            # Le reste est la date
                            date_part = remaining[size_match.end():].strip()
                            if date_part:
                                print(f"   • Modifié: {date_part}")
                    
                    return True
                else:
                    print("❌ Aucun modèle trouvé")
                    return False
            else:
                print("❌ Aucun modèle disponible")
                return False
        else:
            print(f"❌ Erreur lors de la récupération des infos: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test des infos: {e}")
        return False

def test_ollama_pull():
    """Teste le téléchargement d'un petit modèle"""
    print("\n⬇️ Test de téléchargement de modèle")
    print("=" * 50)
    
    # Modèle de test (petit)
    test_model = "hello-world"
    
    try:
        print(f"📥 Téléchargement du modèle de test: {test_model}")
        
        result = subprocess.run(
            ["ollama", "pull", test_model],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes pour le téléchargement
        )
        
        if result.returncode == 0:
            print(f"✅ Modèle {test_model} téléchargé avec succès")
            
            # Vérifier qu'il apparaît dans la liste
            list_result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if list_result.returncode == 0:
                # Parser la sortie textuelle d'ollama list
                lines = list_result.stdout.strip().split('\n')
                model_names = []
                
                # Ignorer la première ligne (en-tête)
                for line in lines[1:]:  # Skip header line
                    if line.strip():
                        # Nettoyer la ligne et extraire le nom du modèle
                        # Format: NAME                                  ID              SIZE      MODIFIED
                        line = line.strip()
                        
                        # Chercher l'ID (12 caractères hexadécimaux)
                        import re
                        id_match = re.search(r'([a-f0-9]{12})', line)
                        if id_match:
                            # Prendre tout ce qui est avant l'ID
                            id_pos = id_match.start()
                            model_name = line[:id_pos].strip()
                            if model_name:
                                model_names.append(model_name)
                
                if test_model in model_names:
                    print(f"✅ Modèle {test_model} confirmé dans la liste")
                    return True
                else:
                    print(f"❌ Modèle {test_model} non trouvé dans la liste")
                    return False
            else:
                print("❌ Impossible de vérifier la liste après téléchargement")
                return False
        else:
            print(f"❌ Erreur lors du téléchargement: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ Timeout lors du téléchargement de {test_model}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue lors du téléchargement: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🤖 Test complet d'Ollama et de ses modèles")
    print("=" * 70)
    
    results = []
    
    # Test 1: Installation
    results.append(test_ollama_installation())
    
    # Test 2: Service
    if results[0]:  # Seulement si Ollama est installé
        results.append(test_ollama_service())
    else:
        results.append(False)
    
    # Test 3: Liste des modèles
    if results[1]:  # Seulement si le service fonctionne
        models = test_ollama_models_list()
        results.append(len(models) > 0)
    else:
        results.append(False)
    
    # Test 4: Informations de modèle
    if results[2]:  # Seulement si des modèles sont trouvés
        results.append(test_ollama_model_info())
    else:
        results.append(False)
    
    # Test 5: Téléchargement (optionnel)
    if results[1]:  # Seulement si le service fonctionne
        results.append(test_ollama_pull())
    else:
        results.append(False)
    
    print("\n🎉 Tests terminés !")
    print("=" * 70)
    
    test_names = [
        "Installation d'Ollama",
        "Service Ollama",
        "Liste des modèles",
        "Informations de modèle",
        "Téléchargement de modèle"
    ]
    
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    if all(results):
        print("\n🎉 TOUS LES TESTS RÉUSSIS")
        print("Ollama fonctionne parfaitement !")
    else:
        print("\n⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
        print("Vérifiez la configuration d'Ollama.")
    
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 