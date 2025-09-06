#!/usr/bin/env python3
"""
Stockage sécurisé - Version minimale pour compatibilité
"""

class SecureStorage:
    """Gestionnaire de stockage sécurisé - Version minimale"""
    
    def __init__(self, config_dir=None):
        self.config_dir = config_dir or "config"
    
    def store_key(self, key_name, key_value):
        """Stocker une clé - Version minimale"""
        print(f"Stockage clé {key_name} (version minimale)")
        return True
    
    def get_key(self, key_name):
        """Récupérer une clé - Version minimale"""
        return None
    
    def has_key(self, key_name):
        """Vérifier la présence d'une clé - Version minimale"""
        return False

# Pour compatibilité
def get_secure_storage():
    """Obtenir l'instance de stockage sécurisé"""
    return SecureStorage()

SECURE_STORAGE_AVAILABLE = False

if __name__ == "__main__":
    print("Secure Storage - Version minimale")
