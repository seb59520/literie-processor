"""
Utilitaires pour le tableau de hauteur des matelas
Charge et utilise les données depuis le fichier JSON de référence
"""

import json
import os
from typing import Dict, List, Optional, Any

# Chemin vers le fichier JSON de référence
TABLEAU_HAUTEUR_JSON = os.path.join(
    os.path.dirname(__file__), 
    "Référentiels", 
    "tableau_hauteur_matelas.json"
)

class TableauHauteurManager:
    """Gestionnaire du tableau de hauteur des matelas"""
    
    def __init__(self, json_path: str = None):
        """
        Initialise le gestionnaire de tableau de hauteur
        
        Args:
            json_path (str): Chemin vers le fichier JSON (optionnel)
        """
        self.json_path = json_path or TABLEAU_HAUTEUR_JSON
        self._data = None
        self._load_data()
    
    def _load_data(self):
        """Charge les données depuis le fichier JSON"""
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Fichier tableau hauteur non trouvé: {self.json_path}")
            self._data = self._get_default_data()
        except json.JSONDecodeError as e:
            print(f"❌ Erreur de décodage JSON: {e}")
            self._data = self._get_default_data()
    
    def _get_default_data(self) -> Dict[str, Any]:
        """Retourne des données par défaut si le fichier JSON n'est pas disponible"""
        return {
            "hauteurs_matelas": {
                "LATEX NATUREL": {"hauteur_cm": 10},
                "LATEX MIXTE 7 ZONES": {"hauteur_cm": 9},
                "MOUSSE RAINUREE 7 ZONES": {"hauteur_cm": 9},
                "MOUSSE VISCO": {"hauteur_cm": 10},
                "LATEX RENFORCE": {"hauteur_cm": 8},
                "SELECT 43": {"hauteur_cm": 8}
            }
        }
    
    def obtenir_hauteur(self, noyau: str) -> int:
        """
        Obtient la hauteur d'un type de noyau
        
        Args:
            noyau (str): Type de noyau du matelas
            
        Returns:
            int: Hauteur en centimètres
        """
        if not self._data:
            return 0
        
        hauteurs = self._data.get("hauteurs_matelas", {})
        info = hauteurs.get(noyau.upper(), {})
        return info.get("hauteur_cm", 0)
    
    def obtenir_info_complete(self, noyau: str) -> Dict[str, Any]:
        """
        Obtient toutes les informations d'un type de noyau
        
        Args:
            noyau (str): Type de noyau du matelas
            
        Returns:
            dict: Informations complètes du noyau
        """
        if not self._data:
            return {}
        
        hauteurs = self._data.get("hauteurs_matelas", {})
        return hauteurs.get(noyau.upper(), {})
    
    def lister_tous_noyaux(self) -> List[str]:
        """
        Liste tous les types de noyaux disponibles
        
        Returns:
            list: Liste des types de noyaux
        """
        if not self._data:
            return []
        
        hauteurs = self._data.get("hauteurs_matelas", {})
        return list(hauteurs.keys())
    
    def lister_noyaux_par_hauteur(self, hauteur_cm: int) -> List[str]:
        """
        Liste les noyaux ayant une hauteur spécifique
        
        Args:
            hauteur_cm (int): Hauteur en centimètres
            
        Returns:
            list: Liste des noyaux avec cette hauteur
        """
        if not self._data:
            return []
        
        hauteurs = self._data.get("hauteurs_matelas", {})
        noyaux = []
        
        for noyau, info in hauteurs.items():
            if info.get("hauteur_cm") == hauteur_cm:
                noyaux.append(noyau)
        
        return noyaux
    
    def obtenir_categories(self) -> Dict[str, Any]:
        """
        Obtient les informations des catégories
        
        Returns:
            dict: Informations des catégories
        """
        if not self._data:
            return {}
        
        return self._data.get("categories", {})
    
    def obtenir_statistiques_categorie(self, categorie: str) -> Dict[str, Any]:
        """
        Obtient les statistiques d'une catégorie
        
        Args:
            categorie (str): Nom de la catégorie
            
        Returns:
            dict: Statistiques de la catégorie
        """
        categories = self.obtenir_categories()
        return categories.get(categorie.upper(), {})
    
    def obtenir_categorie_noyau(self, noyau: str) -> str:
        """
        Détermine la catégorie d'un noyau
        
        Args:
            noyau (str): Type de noyau
            
        Returns:
            str: Catégorie du noyau
        """
        info = self.obtenir_info_complete(noyau)
        return info.get("categorie", "INCONNU")
    
    def afficher_tableau_complet(self):
        """Affiche le tableau complet des hauteurs"""
        if not self._data:
            print("❌ Aucune donnée disponible")
            return
        
        print("=" * 80)
        print("📏 TABLEAU COMPLET DES HAUTEURS DE MATELAS")
        print("=" * 80)
        
        hauteurs = self._data.get("hauteurs_matelas", {})
        for noyau, info in hauteurs.items():
            print(f"\n🔸 {noyau}")
            print(f"   📐 Hauteur: {info.get('hauteur_cm', 'N/A')} cm")
            print(f"   📋 Description: {info.get('description', 'N/A')}")
            print(f"   🏷️ Catégorie: {info.get('categorie', 'N/A')}")
            print(f"   🧱 Épaisseur noyau: {info.get('epaisseur_noyau', 'N/A')} cm")
            print(f"   🛏️ Épaisseur housse: {info.get('epaisseur_housse', 'N/A')} cm")
            print(f"   📊 Densité: {info.get('densite', 'N/A')}")
            print(f"   🎯 Zones: {'Oui' if info.get('zones') else 'Non'}")
        
        # Affichage des catégories
        categories = self.obtenir_categories()
        if categories:
            print("\n" + "=" * 80)
            print("📊 STATISTIQUES PAR CATÉGORIE")
            print("=" * 80)
            
            for categorie, stats in categories.items():
                print(f"\n🏷️ {categorie}")
                print(f"   📏 Hauteur min: {stats.get('hauteur_min', 'N/A')} cm")
                print(f"   📏 Hauteur max: {stats.get('hauteur_max', 'N/A')} cm")
                print(f"   📏 Hauteur moyenne: {stats.get('hauteur_moyenne', 'N/A')} cm")
                print(f"   📝 Types: {', '.join(stats.get('types', []))}")
                print(f"   📋 Description: {stats.get('description', 'N/A')}")
    
    def exporter_tableau_csv(self, output_path: str = "tableau_hauteur_matelas.csv"):
        """
        Exporte le tableau de hauteur en CSV
        
        Args:
            output_path (str): Chemin de sortie du fichier CSV
        """
        if not self._data:
            print("❌ Aucune donnée à exporter")
            return
        
        try:
            import csv
            
            hauteurs = self._data.get("hauteurs_matelas", {})
            
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'Noyau', 'Hauteur_cm', 'Description', 'Categorie', 
                    'Epaisseur_noyau', 'Epaisseur_housse', 'Densite', 'Zones'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for noyau, info in hauteurs.items():
                    writer.writerow({
                        'Noyau': noyau,
                        'Hauteur_cm': info.get('hauteur_cm', ''),
                        'Description': info.get('description', ''),
                        'Categorie': info.get('categorie', ''),
                        'Epaisseur_noyau': info.get('epaisseur_noyau', ''),
                        'Epaisseur_housse': info.get('epaisseur_housse', ''),
                        'Densite': info.get('densite', ''),
                        'Zones': 'Oui' if info.get('zones') else 'Non'
                    })
            
            print(f"✅ Tableau exporté vers: {output_path}")
            
        except ImportError:
            print("❌ Module csv non disponible")
        except Exception as e:
            print(f"❌ Erreur lors de l'export: {e}")

# Instance globale pour utilisation facile
tableau_hauteur = TableauHauteurManager()

# Fonctions de compatibilité avec l'ancien système
def calculer_hauteur_matelas(noyau: str) -> int:
    """
    Calcule la hauteur d'un matelas (compatibilité avec l'ancien système)
    
    Args:
        noyau (str): Type de noyau du matelas
        
    Returns:
        int: Hauteur en centimètres
    """
    return tableau_hauteur.obtenir_hauteur(noyau)

def obtenir_hauteur_matelas(noyau: str) -> Dict[str, Any]:
    """
    Obtient les informations complètes de hauteur (compatibilité)
    
    Args:
        noyau (str): Type de noyau du matelas
        
    Returns:
        dict: Informations complètes
    """
    return tableau_hauteur.obtenir_info_complete(noyau)

if __name__ == "__main__":
    # Tests et démonstration
    print("🧪 TESTS DU TABLEAU DE HAUTEUR (JSON)")
    print("=" * 50)
    
    # Test 1: Hauteur simple
    print(f"Hauteur LATEX NATUREL: {calculer_hauteur_matelas('LATEX NATUREL')} cm")
    print(f"Hauteur MOUSSE VISCO: {calculer_hauteur_matelas('MOUSSE VISCO')} cm")
    print(f"Hauteur INCONNU: {calculer_hauteur_matelas('INCONNU')} cm")
    
    # Test 2: Informations complètes
    print(f"\nInfos LATEX MIXTE 7 ZONES: {obtenir_hauteur_matelas('LATEX MIXTE 7 ZONES')}")
    
    # Test 3: Catégorie
    print(f"\nCatégorie LATEX NATUREL: {tableau_hauteur.obtenir_categorie_noyau('LATEX NATUREL')}")
    print(f"Catégorie MOUSSE VISCO: {tableau_hauteur.obtenir_categorie_noyau('MOUSSE VISCO')}")
    
    # Test 4: Noyaux par hauteur
    print(f"\nNoyaux de 10cm: {tableau_hauteur.lister_noyaux_par_hauteur(10)}")
    print(f"Noyaux de 9cm: {tableau_hauteur.lister_noyaux_par_hauteur(9)}")
    
    # Test 5: Tous les noyaux
    print(f"\nTous les noyaux: {tableau_hauteur.lister_tous_noyaux()}")
    
    # Affichage du tableau complet
    tableau_hauteur.afficher_tableau_complet()
    
    # Export CSV (optionnel)
    # tableau_hauteur.exporter_tableau_csv() 