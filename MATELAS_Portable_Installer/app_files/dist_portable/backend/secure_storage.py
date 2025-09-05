"""
Module de stockage sécurisé pour les clés API
Utilise le chiffrement AES pour protéger les données sensibles
"""

import os
import json
import base64
import hashlib
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import logging

class SecureStorage:
    """Classe pour le stockage sécurisé des données sensibles"""
    
    def __init__(self, storage_file="config/secure_keys.dat", salt_file="config/salt.dat"):
        """
        Initialise le stockage sécurisé
        
        Args:
            storage_file (str): Chemin vers le fichier de stockage chiffré
            salt_file (str): Chemin vers le fichier contenant le salt
        """
        self.storage_file = Path(storage_file)
        self.salt_file = Path(salt_file)
        self.logger = logging.getLogger(__name__)
        
        # Créer les dossiers si nécessaire
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        self.salt_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialiser le salt
        self._init_salt()
    
    def _init_salt(self):
        """Initialise ou charge le salt pour le dérivé de clé"""
        if not self.salt_file.exists():
            # Générer un nouveau salt
            salt = os.urandom(16)
            with open(self.salt_file, 'wb') as f:
                f.write(salt)
            self.logger.info("Nouveau salt généré pour le stockage sécurisé")
        else:
            # Charger le salt existant
            with open(self.salt_file, 'rb') as f:
                salt = f.read()
        
        self.salt = salt
    
    def _derive_key(self, password):
        """
        Dérive une clé de chiffrement à partir du mot de passe
        
        Args:
            password (str): Mot de passe pour dériver la clé
            
        Returns:
            bytes: Clé de chiffrement
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def _get_master_password(self):
        """
        Récupère le mot de passe maître depuis les variables d'environnement
        ou utilise un mot de passe par défaut pour le développement
        
        Returns:
            str: Mot de passe maître
        """
        # Essayer de récupérer depuis les variables d'environnement
        master_password = os.getenv('MATELAS_MASTER_PASSWORD')
        
        if not master_password:
            # Mot de passe par défaut pour le développement
            # En production, il faudrait forcer l'utilisation d'une variable d'environnement
            master_password = "MatelasProcessor2024!Secure"
            self.logger.warning("Utilisation du mot de passe par défaut. En production, définissez MATELAS_MASTER_PASSWORD")
        
        return master_password
    
    def save_api_key(self, service_name, api_key, description=""):
        """
        Sauvegarde une clé API de manière sécurisée
        
        Args:
            service_name (str): Nom du service (ex: 'openrouter', 'ollama')
            api_key (str): Clé API à sauvegarder
            description (str): Description optionnelle
            
        Returns:
            bool: True si sauvegarde réussie, False sinon
        """
        try:
            # Charger les données existantes
            data = self.load_all_data()
            
            # Ajouter ou mettre à jour la clé
            data[service_name] = {
                'api_key': api_key,
                'description': description,
                'created_at': self._get_timestamp(),
                'updated_at': self._get_timestamp()
            }
            
            # Sauvegarder toutes les données
            return self._save_all_data(data)
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde de la clé API {service_name}: {str(e)}")
            return False
    
    def load_api_key(self, service_name):
        """
        Charge une clé API depuis le stockage sécurisé
        
        Args:
            service_name (str): Nom du service
            
        Returns:
            str: Clé API ou None si non trouvée
        """
        try:
            data = self.load_all_data()
            if service_name in data:
                return data[service_name]['api_key']
            return None
            
        except Exception as e:
            self.logger.error(f"Erreur lors du chargement de la clé API {service_name}: {str(e)}")
            return None
    
    def get_api_key_info(self, service_name):
        """
        Récupère les informations complètes d'une clé API
        
        Args:
            service_name (str): Nom du service
            
        Returns:
            dict: Informations de la clé ou None si non trouvée
        """
        try:
            data = self.load_all_data()
            return data.get(service_name)
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des infos de la clé API {service_name}: {str(e)}")
            return None
    
    def list_services(self):
        """
        Liste tous les services avec des clés API sauvegardées
        
        Returns:
            list: Liste des noms de services
        """
        try:
            data = self.load_all_data()
            return list(data.keys())
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la liste des services: {str(e)}")
            return []
    
    def delete_api_key(self, service_name):
        """
        Supprime une clé API du stockage
        
        Args:
            service_name (str): Nom du service à supprimer
            
        Returns:
            bool: True si suppression réussie, False sinon
        """
        try:
            data = self.load_all_data()
            
            if service_name in data:
                del data[service_name]
                return self._save_all_data(data)
            
            return True  # Service n'existait pas déjà
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la suppression de la clé API {service_name}: {str(e)}")
            return False
    
    def _save_all_data(self, data):
        """
        Sauvegarde toutes les données de manière chiffrée
        
        Args:
            data (dict): Données à sauvegarder
            
        Returns:
            bool: True si sauvegarde réussie, False sinon
        """
        try:
            # Convertir en JSON
            json_data = json.dumps(data, indent=2)
            
            # Chiffrer les données
            password = self._get_master_password()
            key = self._derive_key(password)
            fernet = Fernet(key)
            
            encrypted_data = fernet.encrypt(json_data.encode())
            
            # Sauvegarder
            with open(self.storage_file, 'wb') as f:
                f.write(encrypted_data)
            
            self.logger.info("Données sauvegardées de manière sécurisée")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde des données: {str(e)}")
            return False
    
    def load_all_data(self):
        """
        Charge toutes les données depuis le stockage chiffré
        
        Returns:
            dict: Données déchiffrées ou dict vide si erreur
        """
        try:
            if not self.storage_file.exists():
                return {}
            
            # Lire les données chiffrées
            with open(self.storage_file, 'rb') as f:
                encrypted_data = f.read()
            
            # Déchiffrer
            password = self._get_master_password()
            key = self._derive_key(password)
            fernet = Fernet(key)
            
            decrypted_data = fernet.decrypt(encrypted_data)
            data = json.loads(decrypted_data.decode())
            
            return data
            
        except Exception as e:
            self.logger.error(f"Erreur lors du chargement des données: {str(e)}")
            return {}
    
    def _get_timestamp(self):
        """Retourne un timestamp ISO"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def test_encryption(self):
        """
        Teste le système de chiffrement
        
        Returns:
            bool: True si le test réussit, False sinon
        """
        try:
            # Test de sauvegarde et chargement
            test_data = {
                'test_service': {
                    'api_key': 'test_key_12345',
                    'description': 'Test de chiffrement',
                    'created_at': self._get_timestamp(),
                    'updated_at': self._get_timestamp()
                }
            }
            
            # Sauvegarder
            if not self._save_all_data(test_data):
                return False
            
            # Charger
            loaded_data = self.load_all_data()
            
            # Vérifier
            if loaded_data.get('test_service', {}).get('api_key') == 'test_key_12345':
                # Nettoyer le test
                self._save_all_data({})
                self.logger.info("Test de chiffrement réussi")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Erreur lors du test de chiffrement: {str(e)}")
            return False


# Instance globale pour l'application
secure_storage = SecureStorage() 