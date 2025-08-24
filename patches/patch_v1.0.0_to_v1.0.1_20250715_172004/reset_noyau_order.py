#!/usr/bin/env python3
"""
Script pour réinitialiser l'ordre des noyaux avec tous les 6 noyaux par défaut
"""

from config import config

def reset_noyau_order():
    """Réinitialise l'ordre des noyaux avec tous les 6 noyaux par défaut"""
    
    print("🔄 Réinitialisation de l'ordre des noyaux...")
    
    # Ordre par défaut complet avec tous les 6 noyaux
    noyaux_complets = [
        "MOUSSE VISCO",
        "LATEX NATUREL",
        "LATEX MIXTE 7 ZONES",
        "MOUSSE RAINUREE 7 ZONES",
        "LATEX RENFORCÉ",
        "SELECT 43"
    ]
    
    # Afficher l'ordre actuel
    ordre_actuel = config.get_noyau_order()
    print(f"📋 Ordre actuel ({len(ordre_actuel)} noyaux): {ordre_actuel}")
    
    # Appliquer le nouvel ordre
    config.set_noyau_order(noyaux_complets)
    
    # Vérifier que le changement a été appliqué
    nouvel_ordre = config.get_noyau_order()
    print(f"✅ Nouvel ordre ({len(nouvel_ordre)} noyaux): {nouvel_ordre}")
    
    print("\n🎉 Réinitialisation terminée !")
    print("Vous pouvez maintenant relancer l'application et aller dans")
    print("Configuration → Classement des noyaux pour voir tous les 6 noyaux.")

if __name__ == "__main__":
    reset_noyau_order() 