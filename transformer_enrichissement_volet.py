#!/usr/bin/env python3
"""
Script pour transformer la zone Enrichissement LLM en volet déroulant
"""

import re
import os

def analyser_zone_enrichissement():
    """Analyse la zone Enrichissement LLM actuelle"""
    
    print("🔍 ANALYSE DE LA ZONE ENRICHISSEMENT LLM")
    print("=" * 60)
    
    fichier_gui = "app_gui.py"
    
    if not os.path.exists(fichier_gui):
        print(f"❌ Fichier {fichier_gui} non trouvé")
        return False
    
    try:
        with open(fichier_gui, 'r', encoding='utf-8') as f:
            contenu = f.read()
        
        # Chercher la zone Enrichissement LLM
        if "Enrichissement LLM" in contenu:
            print("✅ Zone 'Enrichissement LLM' trouvée")
        else:
            print("❌ Zone 'Enrichissement LLM' non trouvée")
        
        # Chercher le groupe LLM
        if "llm_group = QGroupBox" in contenu:
            print("✅ Groupe LLM trouvé")
        else:
            print("❌ Groupe LLM non trouvé")
        
        # Chercher les éléments de la zone
        elements = [
            "llm_provider_combo",
            "api_key_group", 
            "enrichissement_checkbox",
            "llm_layout"
        ]
        
        print("\n📋 Éléments trouvés dans la zone LLM :")
        for element in elements:
            if element in contenu:
                print(f"   ✅ {element}")
            else:
                print(f"   ❌ {element}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")
        return False

def afficher_plan_modification():
    """Affiche le plan de modification"""
    
    print("\n🎯 PLAN DE MODIFICATION")
    print("=" * 40)
    
    print("""
🔧 MODIFICATIONS À EFFECTUER :

1. 🎨 TRANSFORMATION EN VOLET DÉROULANT :
   - Remplacer QGroupBox statique par QGroupBox checkable
   - Ajouter propriété checkable=True
   - Connecter signal toggled pour ouvrir/fermer

2. 📏 GESTION DE L'ESPACE :
   - Masquer les widgets enfants quand fermé
   - Ajuster la taille du volet selon l'état
   - Sauvegarder l'état dans la configuration

3. 🎨 STYLISATION :
   - Ajouter icône pour indiquer l'état
   - Style visuel pour le volet fermé/ouvert
   - Animation fluide (optionnel)

4. 💾 PERSISTANCE :
   - Sauvegarder l'état ouvert/fermé
   - Restaurer l'état au redémarrage
   - Configuration utilisateur personnalisable

📋 CODE À MODIFIER :
```python
# AVANT (statique)
llm_group = QGroupBox("Enrichissement LLM")

# APRÈS (déroulant)
llm_group = QGroupBox("🔽 Enrichissement LLM")
llm_group.setCheckable(True)
llm_group.setChecked(True)  # Ouvert par défaut
llm_group.toggled.connect(self.on_llm_group_toggled)
```
""")

def afficher_implementation_complete():
    """Affiche l'implémentation complète"""
    
    print("\n📝 IMPLÉMENTATION COMPLÈTE")
    print("=" * 40)
    
    print("""
🔧 FONCTION DE GESTION DU VOLET :

```python
def on_llm_group_toggled(self, checked):
    \"\"\"Gère l'ouverture/fermeture du volet Enrichissement LLM\"\"\"
    try:
        # Afficher/masquer les widgets enfants
        for i in range(self.llm_layout.count()):
            widget = self.llm_layout.itemAt(i).widget()
            if widget:
                widget.setVisible(checked)
        
        # Changer l'icône du titre
        if checked:
            self.llm_group.setTitle("🔽 Enrichissement LLM")
            if hasattr(self, 'app_logger'):
                self.app_logger.info("Volet Enrichissement LLM ouvert")
        else:
            self.llm_group.setTitle("▶️ Enrichissement LLM")
            if hasattr(self, 'app_logger'):
                self.app_logger.info("Volet Enrichissement LLM fermé")
        
        # Sauvegarder l'état
        self.save_llm_panel_state(checked)
        
    except Exception as e:
        if hasattr(self, 'app_logger'):
            self.app_logger.error(f"Erreur lors du basculement du volet LLM: {e}")
```

🔧 FONCTION DE SAUVEGARDE :

```python
def save_llm_panel_state(self, is_open):
    \"\"\"Sauvegarde l'état du volet Enrichissement LLM\"\"\"
    try:
        config = config_manager.get_config()
        config['llm_panel_open'] = is_open
        config_manager.save_config(config)
    except Exception as e:
        if hasattr(self, 'app_logger'):
            self.app_logger.error(f"Erreur lors de la sauvegarde de l'état du volet: {e}")
```

🔧 RESTAURATION AU DÉMARRAGE :

```python
def restore_llm_panel_state(self):
    \"\"\"Restaure l'état du volet Enrichissement LLM\"\"\"
    try:
        config = config_manager.get_config()
        is_open = config.get('llm_panel_open', True)  # Ouvert par défaut
        
        self.llm_group.setChecked(is_open)
        self.on_llm_group_toggled(is_open)
        
    except Exception as e:
        if hasattr(self, 'app_logger'):
            self.app_logger.error(f"Erreur lors de la restauration de l'état du volet: {e}")
```
""")

def main():
    """Fonction principale"""
    
    print("🎯 TRANSFORMATEUR DE ZONE ENRICHISSEMENT LLM")
    print("=" * 70)
    
    # 1. Analyser la zone actuelle
    if analyser_zone_enrichissement():
        print("✅ Analyse terminée avec succès")
        
        # 2. Afficher le plan de modification
        afficher_plan_modification()
        
        # 3. Afficher l'implémentation complète
        afficher_implementation_complete()
        
        print("\n🎯 PROCHAINES ÉTAPES :")
        print("1. Voulez-vous que j'applique ces modifications ?")
        print("2. Ou préférez-vous les faire manuellement ?")
        print("3. Souhaitez-vous d'abord voir le code actuel ?")
        
    else:
        print("❌ Impossible d'analyser la zone")

if __name__ == "__main__":
    main()

