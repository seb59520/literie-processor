#!/usr/bin/env python3
"""
Générateur automatique de packages correctifs MATELAS
Détecte les modifications et propose automatiquement des packages adaptés
"""

import os
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

from package_builder import PackageBuilder


class ChangeType(Enum):
    """Types de changements détectés"""
    INTERFACE = "interface"
    REFERENTIEL = "referentiel"
    BACKEND = "backend"
    CONFIG = "config"
    TEMPLATE = "template"
    SCRIPT = "script"
    DOC = "documentation"


@dataclass
class FileChange:
    """Information sur un fichier modifié"""
    file_path: str
    change_type: ChangeType
    old_hash: str
    new_hash: str
    size: int
    modified_time: float
    description: str = ""


@dataclass
class ChangeGroup:
    """Groupe de changements logiques"""
    group_type: ChangeType
    files: List[FileChange]
    suggested_description: str
    suggested_changelog: str
    priority: int  # 1=critique, 2=important, 3=normal
    package_name_suffix: str = ""


class AutoPackageGenerator:
    """Générateur automatique de packages basé sur les modifications"""
    
    def __init__(self):
        self.base_path = Path.cwd()
        self.state_file = self.base_path / ".package_generator_state.json"
        self.builder = PackageBuilder()
        
        # Configuration des fichiers à surveiller par catégorie
        self.file_categories = {
            ChangeType.INTERFACE: {
                "patterns": ["app_gui*.py", "*_gui*.py", "ui_*.py", "gui_*.py", "*_dialog*.py"],
                "paths": [".", "backend"],
                "keywords": ["interface", "ui", "gui", "dialog", "widget", "window"]
            },
            ChangeType.REFERENTIEL: {
                "patterns": ["*referentiel*.py", "*_utils.py"],
                "paths": ["backend", "backend/Référentiels"],
                "keywords": ["referentiel", "utils", "dimensions", "hauteur", "latex", "mousse", "select"]
            },
            ChangeType.BACKEND: {
                "patterns": ["backend/*.py", "backend_*.py", "*_provider.py", "*_cache.py"],
                "paths": ["backend"],
                "keywords": ["backend", "provider", "cache", "llm", "api", "server"]
            },
            ChangeType.CONFIG: {
                "patterns": ["config*.py", "*config*.json", "matelas_config*", "*.json"],
                "paths": ["."],
                "keywords": ["config", "settings", "parameters"]
            },
            ChangeType.TEMPLATE: {
                "patterns": ["template*.xlsx", "*.xlsx"],
                "paths": ["template", "backend/template"],
                "keywords": ["template", "excel", "xlsx"]
            },
            ChangeType.SCRIPT: {
                "patterns": ["*.py"],
                "paths": ["."],
                "keywords": ["script", "tool", "utility", "helper"]
            }
        }
        
        # État précédent des fichiers
        self.previous_state = self.load_state()
        
    def load_state(self) -> Dict:
        """Charger l'état précédent des fichiers"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erreur lecture état précédent: {e}")
        
        return {"files": {}, "last_scan": 0}
    
    def save_state(self, current_state: Dict):
        """Sauvegarder l'état actuel des fichiers"""
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(current_state, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur sauvegarde état: {e}")
    
    def calculate_file_hash(self, file_path: str) -> str:
        """Calculer le hash d'un fichier"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception:
            return ""
    
    def detect_file_category(self, file_path: str) -> ChangeType:
        """Détecter la catégorie d'un fichier modifié"""
        file_path_lower = file_path.lower()
        file_name = os.path.basename(file_path_lower)
        
        # Vérification par patterns et mots-clés
        for category, config in self.file_categories.items():
            # Vérifier les patterns
            for pattern in config["patterns"]:
                if self._match_pattern(file_name, pattern.lower()):
                    return category
            
            # Vérifier les mots-clés dans le nom
            for keyword in config["keywords"]:
                if keyword in file_path_lower:
                    return category
        
        # Catégorie par défaut
        return ChangeType.SCRIPT
    
    def _match_pattern(self, filename: str, pattern: str) -> bool:
        """Vérifier si un nom de fichier correspond à un pattern simple"""
        if '*' not in pattern:
            return filename == pattern
        
        # Support basique des wildcards
        import fnmatch
        return fnmatch.fnmatch(filename, pattern)
    
    def scan_for_changes(self, since_hours: int = 24) -> List[FileChange]:
        """Scanner les fichiers modifiés depuis X heures"""
        changes = []
        cutoff_time = datetime.now().timestamp() - (since_hours * 3600)
        
        # Scanner tous les fichiers Python et de config
        extensions = ['.py', '.json', '.xlsx', '.md', '.txt']
        exclude_dirs = {'.git', '__pycache__', 'venv', 'node_modules', 'backup', 'dist'}
        
        for root, dirs, files in os.walk('.'):
            # Filtrer les dossiers à exclure
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                file_path = os.path.join(root, file)
                file_path = file_path[2:] if file_path.startswith('./') else file_path  # Enlever ./
                
                # Filtrer par extension
                if not any(file.lower().endswith(ext) for ext in extensions):
                    continue
                
                try:
                    stat = os.stat(file_path)
                    
                    # Vérifier si modifié récemment
                    if stat.st_mtime < cutoff_time:
                        continue
                    
                    # Calculer le hash actuel
                    current_hash = self.calculate_file_hash(file_path)
                    previous_hash = self.previous_state["files"].get(file_path, {}).get("hash", "")
                    
                    # Détecter les changements
                    if current_hash != previous_hash and current_hash:
                        change_type = self.detect_file_category(file_path)
                        
                        change = FileChange(
                            file_path=file_path,
                            change_type=change_type,
                            old_hash=previous_hash,
                            new_hash=current_hash,
                            size=stat.st_size,
                            modified_time=stat.st_mtime,
                            description=self._generate_change_description(file_path, change_type)
                        )
                        
                        changes.append(change)
                
                except Exception as e:
                    print(f"Erreur scan {file_path}: {e}")
                    continue
        
        return changes
    
    def _generate_change_description(self, file_path: str, change_type: ChangeType) -> str:
        """Générer une description du changement"""
        filename = os.path.basename(file_path)
        
        descriptions = {
            ChangeType.INTERFACE: f"Modification interface utilisateur ({filename})",
            ChangeType.REFERENTIEL: f"Mise à jour référentiel ({filename})",
            ChangeType.BACKEND: f"Modification backend ({filename})",
            ChangeType.CONFIG: f"Changement configuration ({filename})",
            ChangeType.TEMPLATE: f"Mise à jour template Excel ({filename})",
            ChangeType.SCRIPT: f"Modification script ({filename})"
        }
        
        return descriptions.get(change_type, f"Modification fichier ({filename})")
    
    def group_changes_by_type(self, changes: List[FileChange]) -> List[ChangeGroup]:
        """Grouper les changements par type logique"""
        groups_dict = {}
        
        for change in changes:
            change_type = change.change_type
            
            if change_type not in groups_dict:
                groups_dict[change_type] = []
            
            groups_dict[change_type].append(change)
        
        # Créer les groupes avec descriptions et priorités
        groups = []
        for change_type, file_changes in groups_dict.items():
            group = self._create_change_group(change_type, file_changes)
            groups.append(group)
        
        # Trier par priorité (plus urgent en premier)
        groups.sort(key=lambda g: g.priority)
        
        return groups
    
    def _create_change_group(self, change_type: ChangeType, changes: List[FileChange]) -> ChangeGroup:
        """Créer un groupe de changements avec métadonnées"""
        file_count = len(changes)
        file_names = [os.path.basename(c.file_path) for c in changes]
        
        # Génération des descriptions et priorités selon le type
        templates = {
            ChangeType.INTERFACE: {
                "description": f"Mise à jour interface utilisateur ({file_count} fichier{'s' if file_count > 1 else ''})",
                "changelog": f"🎨 Interface utilisateur:\n" + 
                           "\n".join([f"- {c.description}" for c in changes]),
                "priority": 1,  # Critique - impacte l'utilisateur
                "suffix": "interface"
            },
            ChangeType.REFERENTIEL: {
                "description": f"Mise à jour référentiels métier ({file_count} fichier{'s' if file_count > 1 else ''})",
                "changelog": f"📊 Référentiels métier:\n" + 
                           "\n".join([f"- {c.description}" for c in changes]),
                "priority": 1,  # Critique - impacte les calculs
                "suffix": "referentiels"
            },
            ChangeType.BACKEND: {
                "description": f"Améliorations backend ({file_count} fichier{'s' if file_count > 1 else ''})",
                "changelog": f"⚙️ Backend:\n" + 
                           "\n".join([f"- {c.description}" for c in changes]),
                "priority": 2,  # Important
                "suffix": "backend"
            },
            ChangeType.CONFIG: {
                "description": f"Changements configuration ({file_count} fichier{'s' if file_count > 1 else ''})",
                "changelog": f"🔧 Configuration:\n" + 
                           "\n".join([f"- {c.description}" for c in changes]),
                "priority": 2,  # Important
                "suffix": "config"
            },
            ChangeType.TEMPLATE: {
                "description": f"Mise à jour templates Excel ({file_count} fichier{'s' if file_count > 1 else ''})",
                "changelog": f"📄 Templates Excel:\n" + 
                           "\n".join([f"- {c.description}" for c in changes]),
                "priority": 1,  # Critique - impacte les exports
                "suffix": "templates"
            },
            ChangeType.SCRIPT: {
                "description": f"Scripts et outils ({file_count} fichier{'s' if file_count > 1 else ''})",
                "changelog": f"🛠️ Scripts et outils:\n" + 
                           "\n".join([f"- {c.description}" for c in changes]),
                "priority": 3,  # Normal
                "suffix": "scripts"
            }
        }
        
        template = templates.get(change_type, templates[ChangeType.SCRIPT])
        
        return ChangeGroup(
            group_type=change_type,
            files=changes,
            suggested_description=template["description"],
            suggested_changelog=template["changelog"],
            priority=template["priority"],
            package_name_suffix=template["suffix"]
        )
    
    def suggest_packages(self, since_hours: int = 24) -> List[ChangeGroup]:
        """Analyser et suggérer des packages basés sur les modifications récentes"""
        print(f"🔍 Analyse des modifications des dernières {since_hours} heures...")
        
        # Scanner les changements
        changes = self.scan_for_changes(since_hours)
        
        if not changes:
            print("ℹ️ Aucune modification détectée")
            return []
        
        print(f"📝 {len(changes)} modification(s) détectée(s)")
        
        # Grouper par type
        groups = self.group_changes_by_type(changes)
        
        print(f"📋 {len(groups)} groupe(s) de changements identifié(s)")
        
        return groups
    
    def create_package_for_group(self, group: ChangeGroup, auto_version: bool = True) -> Dict:
        """Créer un package pour un groupe de changements"""
        files_to_include = [change.file_path for change in group.files]
        
        # Version personnalisée avec suffixe
        if auto_version:
            base_version = self.builder.get_next_version()
            # Ajouter un suffixe pour identifier le type de package
            custom_version = f"{base_version}-{group.package_name_suffix}"
        else:
            custom_version = None
        
        return self.builder.create_correction_package(
            description=group.suggested_description,
            files_to_include=files_to_include,
            changelog=group.suggested_changelog,
            custom_version=custom_version
        )
    
    def update_state_after_scan(self):
        """Mettre à jour l'état après un scan"""
        current_state = {
            "files": {},
            "last_scan": datetime.now().timestamp()
        }
        
        # Scanner tous les fichiers pour mettre à jour les hashes
        extensions = ['.py', '.json', '.xlsx', '.md', '.txt']
        exclude_dirs = {'.git', '__pycache__', 'venv', 'node_modules', 'backup', 'dist'}
        
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    file_path = file_path[2:] if file_path.startswith('./') else file_path
                    
                    try:
                        stat = os.stat(file_path)
                        current_hash = self.calculate_file_hash(file_path)
                        
                        current_state["files"][file_path] = {
                            "hash": current_hash,
                            "size": stat.st_size,
                            "modified": stat.st_mtime
                        }
                    except Exception:
                        continue
        
        self.save_state(current_state)
        self.previous_state = current_state


def analyze_recent_changes(hours: int = 24) -> List[ChangeGroup]:
    """Fonction utilitaire pour analyser les changements récents"""
    generator = AutoPackageGenerator()
    return generator.suggest_packages(since_hours=hours)


def create_auto_packages(hours: int = 24, interactive: bool = True) -> List[Dict]:
    """Créer automatiquement des packages pour les changements récents"""
    generator = AutoPackageGenerator()
    suggested_groups = generator.suggest_packages(since_hours=hours)
    
    if not suggested_groups:
        print("ℹ️ Aucun package à créer")
        return []
    
    created_packages = []
    
    for i, group in enumerate(suggested_groups, 1):
        print(f"\n📦 Groupe {i}/{len(suggested_groups)} - {group.group_type.value.upper()}")
        print(f"📋 Description: {group.suggested_description}")
        print(f"📁 Fichiers ({len(group.files)}):")
        for change in group.files:
            print(f"   • {change.file_path}")
        print(f"⭐ Priorité: {'🔴 Critique' if group.priority == 1 else '🟡 Important' if group.priority == 2 else '🟢 Normal'}")
        
        if interactive:
            response = input(f"\nCréer ce package? (O/n/s=sauter tous): ").lower()
            if response == 's':
                break
            elif response == 'n':
                continue
        
        print("🚀 Création du package...")
        result = generator.create_package_for_group(group)
        
        if result["success"]:
            print(f"✅ Package créé: {result['package_name']}")
            created_packages.append(result)
        else:
            print(f"❌ Erreur: {result.get('error')}")
    
    # Mettre à jour l'état après création des packages
    generator.update_state_after_scan()
    
    return created_packages


if __name__ == "__main__":
    print("🤖 Générateur Automatique de Packages MATELAS")
    print("=" * 50)
    
    # Test de détection
    suggested = analyze_recent_changes(hours=48)  # 48h pour test
    
    if suggested:
        print(f"\n📊 {len(suggested)} groupe(s) de changements suggéré(s):")
        for i, group in enumerate(suggested, 1):
            print(f"\n{i}. {group.suggested_description}")
            print(f"   📁 {len(group.files)} fichier(s)")
            print(f"   ⭐ Priorité: {group.priority}")
    else:
        print("\nℹ️ Aucune modification récente détectée")
    
    # Proposer création automatique
    if suggested:
        response = input("\n🚀 Créer automatiquement les packages suggérés? (o/N): ")
        if response.lower() in ['o', 'oui', 'y', 'yes']:
            created = create_auto_packages(hours=48, interactive=True)
            print(f"\n✅ {len(created)} package(s) créé(s) avec succès!")