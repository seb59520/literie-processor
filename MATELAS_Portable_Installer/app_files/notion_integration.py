#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module d'intégration Notion pour Cursor et gestion de projets
Permet de synchroniser les projets, modifications, notices d'utilisation et liens externes
"""

import os
import json
import requests
import datetime
import hashlib
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class NotionConfig:
    """Configuration pour l'API Notion"""
    api_key: str
    database_id: str
    workspace_id: str
    base_url: str = "https://api.notion.com/v1"

@dataclass
class ProjectInfo:
    """Informations sur un projet"""
    name: str
    path: str
    description: str
    language: str
    framework: str
    last_modified: str
    git_status: str
    cursor_workspace: str

@dataclass
class ChangeLog:
    """Journal des modifications"""
    project_name: str
    file_path: str
    change_type: str  # 'modified', 'added', 'deleted'
    timestamp: str
    description: str
    author: str
    commit_hash: Optional[str] = None

@dataclass
class UserGuide:
    """Notice d'utilisation"""
    title: str
    project_name: str
    content: str
    category: str
    tags: List[str]
    created_date: str
    last_updated: str
    version: str

@dataclass
class ExternalLink:
    """Lien externe"""
    title: str
    url: str
    description: str
    category: str
    tags: List[str]
    project_name: str
    added_date: str

class NotionIntegration:
    """Classe principale pour l'intégration avec Notion"""
    
    def __init__(self, config: NotionConfig):
        self.config = config
        self.headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
    def create_project_page(self, project: ProjectInfo) -> str:
        """Crée une page de projet dans Notion"""
        try:
            data = {
                "parent": {"database_id": self.config.database_id},
                "properties": {
                    "Nom": {"title": [{"text": {"content": project.name}}]},
                    "Chemin": {"rich_text": [{"text": {"content": project.path}}]},
                    "Description": {"rich_text": [{"text": {"content": project.description}}]},
                    "Langage": {"select": {"name": project.language}},
                    "Framework": {"rich_text": [{"text": {"content": project.framework}}]},
                    "Dernière modification": {"date": {"start": project.last_modified}},
                    "Statut Git": {"select": {"name": project.git_status}},
                    "Workspace Cursor": {"rich_text": [{"text": {"content": project.cursor_workspace}}]},
                    "Statut": {"select": {"name": "En cours"}},
                    "Date de création": {"date": {"start": datetime.datetime.now().isoformat()}}
                }
            }
            
            response = requests.post(
                f"{self.config.base_url}/pages",
                headers=self.headers,
                json=data
            )
            
            if response.status_code == 200:
                page_id = response.json()["id"]
                logger.info(f"Page de projet créée: {page_id}")
                return page_id
            else:
                logger.error(f"Erreur création page: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Erreur lors de la création de la page: {e}")
            return None
    
    def update_project_status(self, project_name: str, status: str) -> bool:
        """Met à jour le statut d'un projet"""
        try:
            # Rechercher la page du projet
            query = {
                "filter": {
                    "property": "Nom",
                    "title": {"equals": project_name}
                }
            }
            
            response = requests.post(
                f"{self.config.base_url}/databases/{self.config.database_id}/query",
                headers=self.headers,
                json=query
            )
            
            if response.status_code == 200:
                results = response.json()["results"]
                if results:
                    page_id = results[0]["id"]
                    
                    # Mettre à jour le statut
                    update_data = {
                        "properties": {
                            "Statut": {"select": {"name": status}}
                        }
                    }
                    
                    update_response = requests.patch(
                        f"{self.config.base_url}/pages/{page_id}",
                        headers=self.headers,
                        json=update_data
                    )
                    
                    return update_response.status_code == 200
                    
            return False
            
        except Exception as e:
            logger.error(f"Erreur mise à jour statut: {e}")
            return False
    
    def log_change(self, change: ChangeLog) -> bool:
        """Enregistre une modification dans Notion"""
        try:
            data = {
                "parent": {"database_id": self.config.database_id},
                "properties": {
                    "Projet": {"rich_text": [{"text": {"content": change.project_name}}]},
                    "Fichier": {"rich_text": [{"text": {"content": change.file_path}}]},
                    "Type de modification": {"select": {"name": change.change_type}},
                    "Description": {"rich_text": [{"text": {"content": change.description}}]},
                    "Auteur": {"rich_text": [{"text": {"content": change.author}}]},
                    "Date": {"date": {"start": change.timestamp}},
                    "Hash commit": {"rich_text": [{"text": {"content": change.commit_hash or ""}}]}
                }
            }
            
            response = requests.post(
                f"{self.config.base_url}/pages",
                headers=self.headers,
                json=data
            )
            
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"Erreur enregistrement modification: {e}")
            return False
    
    def create_user_guide(self, guide: UserGuide) -> str:
        """Crée une notice d'utilisation dans Notion"""
        try:
            data = {
                "parent": {"database_id": self.config.database_id},
                "properties": {
                    "Titre": {"title": [{"text": {"content": guide.title}}]},
                    "Projet": {"rich_text": [{"text": {"content": guide.project_name}}]},
                    "Catégorie": {"select": {"name": guide.category}},
                    "Tags": {"multi_select": [{"name": tag} for tag in guide.tags]},
                    "Version": {"rich_text": [{"text": {"content": guide.version}}]},
                    "Date création": {"date": {"start": guide.created_date}},
                    "Dernière mise à jour": {"date": {"start": guide.last_updated}}
                },
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": guide.content}}]
                        }
                    }
                ]
            }
            
            response = requests.post(
                f"{self.config.base_url}/pages",
                headers=self.headers,
                json=data
            )
            
            if response.status_code == 200:
                page_id = response.json()["id"]
                logger.info(f"Notice d'utilisation créée: {page_id}")
                return page_id
            else:
                logger.error(f"Erreur création notice: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Erreur lors de la création de la notice: {e}")
            return None
    
    def add_external_link(self, link: ExternalLink) -> bool:
        """Ajoute un lien externe dans Notion"""
        try:
            data = {
                "parent": {"database_id": self.config.database_id},
                "properties": {
                    "Titre": {"title": [{"text": {"content": link.title}}]},
                    "URL": {"url": link.url},
                    "Description": {"rich_text": [{"text": {"content": link.description}}]},
                    "Catégorie": {"select": {"name": link.category}},
                    "Tags": {"multi_select": [{"name": tag} for tag in link.tags]},
                    "Projet": {"rich_text": [{"text": {"content": link.project_name}}]},
                    "Date d'ajout": {"date": {"start": link.added_date}}
                }
            }
            
            response = requests.post(
                f"{self.config.base_url}/pages",
                headers=self.headers,
                json=data
            )
            
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"Erreur ajout lien externe: {e}")
            return False
    
    def search_projects(self, query: str) -> List[Dict]:
        """Recherche des projets dans Notion"""
        try:
            search_data = {
                "query": query,
                "filter": {
                    "property": "object",
                    "value": "page"
                }
            }
            
            response = requests.post(
                f"{self.config.base_url}/search",
                headers=self.headers,
                json=search_data
            )
            
            if response.status_code == 200:
                return response.json()["results"]
            else:
                logger.error(f"Erreur recherche: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Erreur lors de la recherche: {e}")
            return []

class CursorNotionSync:
    """Synchronisation entre Cursor et Notion"""
    
    def __init__(self, notion_integration: NotionIntegration):
        self.notion = notion_integration
        
    def scan_cursor_workspace(self, workspace_path: str) -> List[ProjectInfo]:
        """Scanne un workspace Cursor pour détecter les projets"""
        projects = []
        workspace_path = Path(workspace_path)
        
        try:
            for item in workspace_path.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    # Vérifier si c'est un projet (présence de fichiers de configuration)
                    project_files = ['package.json', 'requirements.txt', 'pom.xml', 'build.gradle', 
                                   'Cargo.toml', 'go.mod', 'composer.json', '.git']
                    
                    if any((item / file).exists() for file in project_files):
                        project_info = ProjectInfo(
                            name=item.name,
                            path=str(item.absolute()),
                            description=self._detect_project_description(item),
                            language=self._detect_language(item),
                            framework=self._detect_framework(item),
                            last_modified=datetime.datetime.fromtimestamp(
                                item.stat().st_mtime
                            ).isoformat(),
                            git_status=self._get_git_status(item),
                            cursor_workspace=str(workspace_path.absolute())
                        )
                        projects.append(project_info)
                        
        except Exception as e:
            logger.error(f"Erreur scan workspace: {e}")
            
        return projects
    
    def _detect_project_description(self, project_path: Path) -> str:
        """Détecte la description du projet"""
        readme_files = ['README.md', 'README.txt', 'README.rst']
        
        for readme in readme_files:
            readme_path = project_path / readme
            if readme_path.exists():
                try:
                    content = readme_path.read_text(encoding='utf-8', errors='ignore')
                    # Extraire la première ligne non vide
                    lines = [line.strip() for line in content.split('\n') if line.strip()]
                    if lines:
                        return lines[0][:100]  # Limiter à 100 caractères
                except:
                    pass
        
        return f"Projet {project_path.name}"
    
    def _detect_language(self, project_path: Path) -> str:
        """Détecte le langage principal du projet"""
        language_files = {
            'Python': ['*.py', 'requirements.txt', 'setup.py'],
            'JavaScript': ['*.js', 'package.json', 'yarn.lock'],
            'Java': ['*.java', 'pom.xml', 'build.gradle'],
            'C++': ['*.cpp', '*.h', 'CMakeLists.txt'],
            'Go': ['*.go', 'go.mod'],
            'Rust': ['*.rs', 'Cargo.toml'],
            'PHP': ['*.php', 'composer.json']
        }
        
        for lang, patterns in language_files.items():
            for pattern in patterns:
                if list(project_path.glob(pattern)):
                    return lang
        
        return "Autre"
    
    def _detect_framework(self, project_path: Path) -> str:
        """Détecte le framework utilisé"""
        framework_indicators = {
            'Django': 'manage.py',
            'Flask': 'app.py',
            'React': 'package.json',
            'Vue.js': 'vue.config.js',
            'Angular': 'angular.json',
            'Spring': 'pom.xml',
            'Laravel': 'artisan',
            'Express': 'package.json'
        }
        
        for framework, indicator in framework_indicators.items():
            if (project_path / indicator).exists():
                return framework
        
        return "Standard"
    
    def _get_git_status(self, project_path: Path) -> str:
        """Obtient le statut Git du projet"""
        git_path = project_path / '.git'
        if git_path.exists():
            return "Git initialisé"
        return "Non versionné"
    
    def sync_workspace_to_notion(self, workspace_path: str) -> bool:
        """Synchronise le workspace Cursor avec Notion"""
        try:
            projects = self.scan_cursor_workspace(workspace_path)
            
            for project in projects:
                # Créer ou mettre à jour le projet dans Notion
                page_id = self.notion.create_project_page(project)
                if page_id:
                    logger.info(f"Projet synchronisé: {project.name}")
                else:
                    logger.warning(f"Échec synchronisation: {project.name}")
            
            return True
            
        except Exception as e:
            logger.error(f"Erreur synchronisation workspace: {e}")
            return False

def main():
    """Fonction principale pour tester l'intégration"""
    # Charger la configuration depuis un fichier
    config_path = Path("notion_config.json")
    
    if not config_path.exists():
        print("Création du fichier de configuration Notion...")
        create_config_template()
        return
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        config = NotionConfig(**config_data)
        notion = NotionIntegration(config)
        cursor_sync = CursorNotionSync(notion)
        
        # Synchroniser le workspace actuel
        current_workspace = os.getcwd()
        print(f"Synchronisation du workspace: {current_workspace}")
        
        success = cursor_sync.sync_workspace_to_notion(current_workspace)
        
        if success:
            print("✅ Synchronisation réussie avec Notion!")
        else:
            print("❌ Erreur lors de la synchronisation")
            
    except Exception as e:
        print(f"Erreur: {e}")

def create_config_template():
    """Crée un template de configuration Notion"""
    template = {
        "api_key": "VOTRE_CLE_API_NOTION_ICI",
        "database_id": "ID_DE_VOTRE_BASE_DE_DONNEES",
        "workspace_id": "ID_DE_VOTRE_WORKSPACE"
    }
    
    with open("notion_config.json", 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
    
    print("📝 Fichier de configuration créé: notion_config.json")
    print("⚠️  Veuillez configurer vos clés Notion dans ce fichier")

if __name__ == "__main__":
    main()


