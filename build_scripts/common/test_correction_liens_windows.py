#!/usr/bin/env python3
"""
Test de correction des liens hypertextes pour Windows et chemins réseau
"""

import sys
import os
import platform
import urllib.parse
from pathlib import Path

def test_chemin_windows():
    """Test de gestion des chemins Windows"""
    print("🧪 TEST DE CORRECTION DES LIENS WINDOWS")
    print("=" * 60)
    
    # Simuler différents types de chemins
    chemins_test = [
        # Chemin local Windows
        "C:\\Users\\Client\\Documents\\Matelas_S29_2025_1.xlsx",
        # Chemin réseau Windows
        "\\\\serveur\\partage\\Matelas_S29_2025_1.xlsx",
        # Chemin avec espaces
        "C:\\Users\\Client\\Mes Documents\\Matelas_S29_2025_1.xlsx",
        # Chemin avec caractères spéciaux
        "C:\\Users\\Client\\Documents\\Matelas_S29_2025_1.xlsx",
        # Chemin relatif
        "output\\Matelas_S29_2025_1.xlsx"
    ]
    
    print(f"🖥️  Système d'exploitation: {platform.system()}")
    print(f"📁 Répertoire courant: {os.getcwd()}")
    print()
    
    for i, chemin in enumerate(chemins_test, 1):
        print(f"Test {i}: {chemin}")
        
        # Simuler le traitement du chemin comme dans open_excel_file
        chemin_traite = traiter_chemin_windows(chemin)
        print(f"   → Traité: {chemin_traite}")
        
        # Vérifier si le fichier existe (simulation)
        existe = os.path.exists(chemin_traite) if os.path.isabs(chemin_traite) else False
        print(f"   → Existe: {'✅' if existe else '❌'}")
        print()

def traiter_chemin_windows(file_path):
    """Simule le traitement des chemins comme dans open_excel_file"""
    
    # Gestion des différents formats d'URL
    if file_path.startswith('file://'):
        # Enlever le préfixe 'file://' et gérer les caractères spéciaux
        file_path = file_path[7:]
        # Décoder les caractères spéciaux
        file_path = urllib.parse.unquote(file_path)
    elif file_path.startswith('file:///'):
        # Format Windows avec 3 slashes
        file_path = file_path[8:]
        file_path = urllib.parse.unquote(file_path)
    
    # Normaliser le chemin pour Windows
    if platform.system() == "Windows":
        # Convertir les slashes forward en backslashes si nécessaire
        file_path = file_path.replace('/', '\\')
        # Gérer les chemins réseau Windows (\\serveur\partage)
        if file_path.startswith('\\\\'):
            # C'est un chemin réseau Windows, le laisser tel quel
            pass
        elif file_path.startswith('\\'):
            # Chemin relatif avec backslash, le convertir en absolu
            file_path = os.path.abspath(file_path)
    
    return file_path

def test_generation_liens():
    """Test de génération des liens HTML"""
    print("🔗 TEST DE GÉNÉRATION DES LIENS HTML")
    print("=" * 60)
    
    # Simuler des fichiers Excel
    fichiers_excel = [
        "output/Matelas_S29_2025_1.xlsx",
        "C:/Users/Client/Documents/Matelas_S29_2025_1.xlsx",
        "\\\\serveur\\partage\\Matelas_S29_2025_1.xlsx"
    ]
    
    for fichier in fichiers_excel:
        # Simuler la génération de lien comme dans update_display
        file_path = os.path.abspath(fichier)
        if os.path.exists(file_path) or fichier.startswith('\\\\'):  # Simuler l'existence
            # Utiliser le chemin direct sans préfixe file://
            if platform.system() == "Windows":
                # Sur Windows, utiliser le chemin direct avec des backslashes
                link_path = file_path.replace('/', '\\')
            else:
                # Sur macOS/Linux, utiliser le chemin direct
                link_path = file_path
            
            lien_html = f"<p>🔗 <a href='{link_path}'>{os.path.basename(fichier)}</a></p>"
            print(f"Fichier: {fichier}")
            print(f"Lien généré: {lien_html}")
            print()

def test_ouverture_fichier():
    """Test de simulation d'ouverture de fichier"""
    print("📂 TEST DE SIMULATION D'OUVERTURE")
    print("=" * 60)
    
    # Créer un fichier de test temporaire
    fichier_test = "test_excel_temporaire.xlsx"
    try:
        with open(fichier_test, 'w') as f:
            f.write("Test")
        
        print(f"Fichier de test créé: {fichier_test}")
        
        # Simuler l'ouverture selon le système
        system = platform.system()
        if system == "Darwin":  # macOS
            print("Commande d'ouverture: open")
        elif system == "Windows":
            print("Commande d'ouverture: os.startfile ou start")
        else:  # Linux
            print("Commande d'ouverture: xdg-open")
        
        print("✅ Simulation d'ouverture réussie")
        
    except Exception as e:
        print(f"❌ Erreur lors de la simulation: {e}")
    finally:
        # Nettoyer le fichier de test
        if os.path.exists(fichier_test):
            os.remove(fichier_test)

def main():
    """Fonction principale de test"""
    print("🔧 CORRECTION DES LIENS HYPERTEXTES POUR WINDOWS")
    print("=" * 80)
    print()
    
    test_chemin_windows()
    test_generation_liens()
    test_ouverture_fichier()
    
    print("✅ Tests terminés")
    print()
    print("📋 RÉSUMÉ DES AMÉLIORATIONS:")
    print("• Gestion des chemins réseau Windows (\\\\serveur\\partage)")
    print("• Décodage des caractères spéciaux dans les URLs")
    print("• Normalisation des chemins avec backslashes sur Windows")
    print("• Fallback multiple pour l'ouverture de fichiers")
    print("• Messages d'erreur détaillés pour le débogage")
    print("• Suppression du préfixe file:// pour une meilleure compatibilité")

if __name__ == "__main__":
    main() 