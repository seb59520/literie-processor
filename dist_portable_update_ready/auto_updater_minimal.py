#!/usr/bin/env python3
"""
Auto Updater - Version minimale pour compatibilité
"""

class AutoUpdater:
    """Gestionnaire de mise à jour automatique - Version minimale"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.server_url = "http://72.60.47.183/"
    
    def start_background_check(self):
        """Démarrer la vérification en arrière-plan - Version minimale"""
        pass
    
    def check_for_updates(self):
        """Vérifier les mises à jour - Version minimale"""
        return None

# Pour compatibilité
AUTO_UPDATE_AVAILABLE = False

if __name__ == "__main__":
    print("Auto Updater - Version minimale")
