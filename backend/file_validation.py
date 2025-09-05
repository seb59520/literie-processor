"""
Module de validation des fichiers pour l'application Matelas
"""

import os
import mimetypes
import logging
from typing import Optional, Dict, Any, List
from pathlib import Path
import fitz  # PyMuPDF
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class FileValidationResult:
    """Résultat de la validation d'un fichier"""
    is_valid: bool
    file_path: str
    file_size_mb: float
    mime_type: Optional[str] = None
    page_count: Optional[int] = None
    text_length: Optional[int] = None
    errors: List[str] = None
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []

class FileValidator:
    """Validateur de fichiers pour l'application"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._default_config()
        
    def _default_config(self) -> Dict[str, Any]:
        """Configuration par défaut pour la validation"""
        return {
            'max_file_size_mb': 50,
            'min_file_size_kb': 1,
            'allowed_mime_types': [
                'application/pdf',
                'application/x-pdf',
                'text/pdf'
            ],
            'max_pages': 100,
            'min_text_length': 10,
            'max_text_length': 1000000,  # 1M caractères
            'allowed_extensions': ['.pdf']
        }
    
    def validate_file_path(self, file_path: str) -> FileValidationResult:
        """
        Valide un fichier et retourne un résultat détaillé
        
        Args:
            file_path: Chemin vers le fichier à valider
            
        Returns:
            FileValidationResult avec les détails de validation
        """
        result = FileValidationResult(
            is_valid=False,
            file_path=file_path,
            file_size_mb=0.0
        )
        
        try:
            # Vérifier que le fichier existe
            if not os.path.exists(file_path):
                result.errors.append(f"Le fichier n'existe pas: {file_path}")
                return result
            
            # Vérifier que c'est bien un fichier
            if not os.path.isfile(file_path):
                result.errors.append(f"Le chemin ne pointe pas vers un fichier: {file_path}")
                return result
            
            # Vérifier la taille du fichier
            file_size_bytes = os.path.getsize(file_path)
            file_size_mb = file_size_bytes / (1024 * 1024)
            file_size_kb = file_size_bytes / 1024
            
            result.file_size_mb = file_size_mb
            
            if file_size_kb < self.config['min_file_size_kb']:
                result.errors.append(
                    f"Fichier trop petit: {file_size_kb:.1f} KB "
                    f"(minimum: {self.config['min_file_size_kb']} KB)"
                )
            
            if file_size_mb > self.config['max_file_size_mb']:
                result.errors.append(
                    f"Fichier trop volumineux: {file_size_mb:.1f} MB "
                    f"(maximum: {self.config['max_file_size_mb']} MB)"
                )
            
            # Vérifier l'extension
            file_extension = Path(file_path).suffix.lower()
            if file_extension not in self.config['allowed_extensions']:
                result.errors.append(
                    f"Extension non autorisée: {file_extension} "
                    f"(autorisées: {', '.join(self.config['allowed_extensions'])})"
                )
            
            # Vérifier le type MIME
            mime_type, _ = mimetypes.guess_type(file_path)
            result.mime_type = mime_type
            
            if mime_type not in self.config['allowed_mime_types']:
                result.warnings.append(
                    f"Type MIME non reconnu: {mime_type} "
                    f"(attendus: {', '.join(self.config['allowed_mime_types'])})"
                )
            
            # Validation spécifique PDF
            if file_extension == '.pdf':
                pdf_result = self._validate_pdf_content(file_path)
                result.page_count = pdf_result.get('page_count')
                result.text_length = pdf_result.get('text_length')
                
                if pdf_result.get('errors'):
                    result.errors.extend(pdf_result['errors'])
                if pdf_result.get('warnings'):
                    result.warnings.extend(pdf_result['warnings'])
            
            # Le fichier est valide s'il n'y a pas d'erreurs
            result.is_valid = len(result.errors) == 0
            
            if result.is_valid:
                logger.info(
                    f"Fichier validé avec succès: {file_path} "
                    f"({file_size_mb:.1f} MB, {result.page_count or 'N/A'} pages)"
                )
            else:
                logger.warning(
                    f"Validation échouée pour {file_path}: "
                    f"{'; '.join(result.errors)}"
                )
            
        except Exception as e:
            result.errors.append(f"Erreur lors de la validation: {str(e)}")
            logger.error(f"Erreur validation fichier {file_path}: {e}", exc_info=True)
        
        return result
    
    def _validate_pdf_content(self, file_path: str) -> Dict[str, Any]:
        """
        Valide le contenu spécifique d'un PDF
        
        Args:
            file_path: Chemin vers le fichier PDF
            
        Returns:
            Dictionnaire avec les résultats de validation
        """
        result = {
            'page_count': 0,
            'text_length': 0,
            'errors': [],
            'warnings': []
        }
        
        try:
            # Ouvrir le PDF avec PyMuPDF
            with fitz.open(file_path) as doc:
                page_count = len(doc)
                result['page_count'] = page_count
                
                # Vérifier le nombre de pages
                if page_count > self.config['max_pages']:
                    result['errors'].append(
                        f"PDF trop volumineux: {page_count} pages "
                        f"(maximum: {self.config['max_pages']})"
                    )
                
                # Extraire et valider le texte
                text_content = ""
                for page_num in range(min(page_count, 10)):  # Échantillon des 10 premières pages
                    page = doc[page_num]
                    text_content += page.get_text()
                
                text_length = len(text_content.strip())
                result['text_length'] = text_length
                
                if text_length < self.config['min_text_length']:
                    result['warnings'].append(
                        f"Peu de texte détecté: {text_length} caractères "
                        f"(minimum recommandé: {self.config['min_text_length']})"
                    )
                
                if text_length > self.config['max_text_length']:
                    result['warnings'].append(
                        f"Texte très volumineux: {text_length} caractères "
                        f"(traitement pourrait être lent)"
                    )
                
                # Vérifier si le PDF est chiffré
                if doc.needs_pass:
                    result['errors'].append("PDF protégé par mot de passe")
                
                # Vérifier s'il y a du texte extractible
                if text_length == 0:
                    result['warnings'].append(
                        "Aucun texte extractible détecté (PDF image ou scanné?)"
                    )
                
        except Exception as e:
            result['errors'].append(f"Erreur lors de l'analyse PDF: {str(e)}")
            logger.error(f"Erreur analyse PDF {file_path}: {e}")
        
        return result
    
    def validate_multiple_files(self, file_paths: List[str]) -> List[FileValidationResult]:
        """
        Valide plusieurs fichiers
        
        Args:
            file_paths: Liste des chemins de fichiers
            
        Returns:
            Liste des résultats de validation
        """
        results = []
        for file_path in file_paths:
            result = self.validate_file_path(file_path)
            results.append(result)
        
        return results
    
    def get_validation_summary(self, results: List[FileValidationResult]) -> Dict[str, Any]:
        """
        Génère un résumé des validations
        
        Args:
            results: Liste des résultats de validation
            
        Returns:
            Dictionnaire avec le résumé
        """
        total_files = len(results)
        valid_files = sum(1 for r in results if r.is_valid)
        invalid_files = total_files - valid_files
        
        total_size_mb = sum(r.file_size_mb for r in results)
        total_pages = sum(r.page_count or 0 for r in results if r.page_count)
        
        all_errors = []
        all_warnings = []
        for r in results:
            all_errors.extend(r.errors)
            all_warnings.extend(r.warnings)
        
        return {
            'total_files': total_files,
            'valid_files': valid_files,
            'invalid_files': invalid_files,
            'success_rate': valid_files / total_files if total_files > 0 else 0,
            'total_size_mb': total_size_mb,
            'total_pages': total_pages,
            'total_errors': len(all_errors),
            'total_warnings': len(all_warnings),
            'unique_errors': list(set(all_errors)),
            'unique_warnings': list(set(all_warnings))
        }

# Instance globale pour usage simple
default_validator = FileValidator()

def validate_pdf_file(file_path: str) -> FileValidationResult:
    """Fonction de convenance pour valider un fichier PDF"""
    return default_validator.validate_file_path(file_path)

def validate_file_size(file_path: str, max_size_mb: int = 50) -> bool:
    """Fonction rapide pour vérifier uniquement la taille"""
    try:
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        return size_mb <= max_size_mb
    except:
        return False