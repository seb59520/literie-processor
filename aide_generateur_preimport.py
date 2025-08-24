from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox, QApplication, QFormLayout, QTextEdit, QGroupBox
)
from PyQt6.QtCore import Qt
import json
import re
import unicodedata

# Imports backend pour les calculs
from backend.hauteur_utils import calculer_hauteur_matelas
from backend.decoupe_noyau_utils import calcul_decoupe_noyau
from backend.latex_naturel_longueur_housse_utils import get_latex_naturel_longueur_housse_value
from backend.latex_renforce_longueur_utils import get_latex_renforce_longueur_housse
from backend.mousse_visco_utils import get_mousse_visco_value
from backend.mousse_visco_longueur_utils import get_mousse_visco_longueur_value
from backend.mousse_rainuree7zones_referentiel import get_valeur_mousse_rainuree7zones
from backend.mousse_rainuree7zones_longueur_housse_utils import get_mousse_rainuree7zones_longueur_housse_value
from backend.latex_mixte7zones_referentiel import get_valeur_latex_mixte7zones
from backend.latex_mixte7zones_longueur_housse_utils import get_latex_mixte7zones_longueur_housse_value
from backend.select43_utils import get_select43_display_value
from backend.select43_longueur_housse_utils import get_select43_longueur_housse_value

# Dummy listes (à remplacer par les vraies listes du backend)
LISTE_NOYAUX = [
    "LATEX NATUREL", "LATEX MIXTE 7 ZONES", "MOUSSE RAINUREE 7 ZONES", "LATEX RENFORCE", "SELECT 43", "MOUSSE VISCO", "MÉMOIRE DE FORME HYBRIDE MOUSSE VISCOÉLASTIQUE"
]
LISTE_HOUSSES = [
    "TENCEL", "TENCEL LUXE3D", "EXTENSIBLE", "POLYESTER", "COUSSINETS", "LAVABLE", "COTON"
]

def normalize_str(txt):
    return unicodedata.normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII').upper()

def detecter_infos_depuis_texte(texte):
    # Extraction dimensions
    match = re.search(r'(\d{2,3})[\s/]+(\d{2,3})[\s/]+(\d{2,3})', texte)
    largeur, longueur, epaisseur = '', '', ''
    if match:
        largeur, longueur, epaisseur = match.groups()
    
    # Normalisation du texte pour la détection
    texte_norm = normalize_str(texte)
    
    # Détection du noyau (améliorée)
    noyau = ''
    if 'MOUSSE RAINUREE' in texte_norm:
        noyau = 'MOUSSE RAINURÉE 7 ZONES'
    elif 'LATEX NATUREL' in texte_norm:
        noyau = 'LATEX NATUREL'
    elif 'LATEX MIXTE' in texte_norm:
        noyau = 'LATEX MIXTE 7 ZONES'
    elif 'LATEX RENFORCE' in texte_norm:
        noyau = 'LATEX RENFORCE'
    elif 'SELECT 43' in texte_norm:
        noyau = 'SELECT 43'
    elif 'MOUSSE VISCO' in texte_norm:
        noyau = 'MOUSSE VISCO'
    
    # Détection de la housse
    housse = ''
    if 'TENCEL LUXE 3D' in texte_norm:
        housse = 'TENCEL LUXE 3D'
    elif 'TENCEL' in texte_norm:
        housse = 'TENCEL'
    elif 'POLYESTER' in texte_norm:
        housse = 'POLYESTER'
    
    # Détection de la fermeté (normalisée)
    fermete = ''
    # Vérifier d'abord dans le texte original (avec accents)
    for mot in ["FERME", "MÉDIUM", "CONFORT"]:
        if mot in texte.upper():
            fermete = mot
            break
    # Si pas trouvé, vérifier dans le texte normalisé
    if not fermete:
        for mot in ["FERME", "MEDIUM", "CONFORT"]:
            if mot in texte_norm:
                fermete = mot
                break
    # Si toujours pas trouvé, essayer une recherche plus flexible
    if not fermete:
        if "MÉDIUM" in texte or "MEDIUM" in texte_norm:
            fermete = "MÉDIUM"
        elif "FERME" in texte or "FERME" in texte_norm:
            fermete = "FERME"
        elif "CONFORT" in texte or "CONFORT" in texte_norm:
            fermete = "CONFORT"
    
    # Détection de la découpe noyau (regex)
    decoupe_noyau = ''
    match_decoupe = re.search(r'(\d+)\s*x\s*(\d+)', texte)
    if match_decoupe:
        decoupe_noyau = f"{match_decoupe.group(1)} x {match_decoupe.group(2)}"
    
    # Détection du type de literie (Jumeaux vs 1 pièce)
    type_literie = '1 PIÈCE'  # Par défaut
    if 'JUMEAUX' in texte_norm or '2 PIECES' in texte_norm or 'DEUX PIECES' in texte_norm:
        type_literie = 'JUMEAUX'
    elif '1 PIECE' in texte_norm or 'UNE PIECE' in texte_norm:
        type_literie = '1 PIÈCE'
    
    # Calculs de base
    hauteur = epaisseur if epaisseur else ''
    dimensions_housse = f"{largeur}x{longueur}" if largeur and longueur else ''
    longueur_housse = longueur if longueur else ''
    
    return largeur, longueur, epaisseur, hauteur, dimensions_housse, longueur_housse, decoupe_noyau, noyau, housse, type_literie, fermete

class GenerateurPreImportDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Générateur de Pré-import")
        self.setModal(True)
        self.resize(600, 700)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Groupe pour l'analyse de texte
        groupe_analyse = QGroupBox("Analyse de texte")
        layout_analyse = QVBoxLayout()
        
        # Zone de texte pour l'analyse
        self.input_texte = QTextEdit()
        self.input_texte.setPlaceholderText("Collez ici le texte à analyser...")
        self.input_texte.setMaximumHeight(100)
        layout_analyse.addWidget(QLabel("Texte à analyser:"))
        layout_analyse.addWidget(self.input_texte)
        
        # Bouton d'analyse
        btn_analyser = QPushButton("Analyser le texte")
        btn_analyser.clicked.connect(self.analyser_texte)
        layout_analyse.addWidget(btn_analyser)
        
        groupe_analyse.setLayout(layout_analyse)
        layout.addWidget(groupe_analyse)
        
        # Zone d'alertes
        self.zone_alertes = QLabel()
        self.zone_alertes.setStyleSheet("color: #e74c3c; font-weight: bold; background-color: #fdf2f2; padding: 10px; border: 1px solid #e74c3c; border-radius: 5px;")
        self.zone_alertes.setVisible(False)
        layout.addWidget(self.zone_alertes)
        
        # Groupe pour les données
        groupe_donnees = QGroupBox("Données du matelas")
        layout_donnees = QFormLayout()
        
        # Champs de saisie
        self.input_largeur = QLineEdit()
        self.input_longueur = QLineEdit()
        self.input_epaisseur = QLineEdit()
        self.input_hauteur = QLineEdit()
        
        # Combo box pour le noyau
        self.combo_noyau = QComboBox()
        self.combo_noyau.addItems([
            "(choisir)", "LATEX NATUREL", "LATEX MIXTE 7 ZONES", 
            "MOUSSE RAINURÉE 7 ZONES", "LATEX RENFORCE", "SELECT 43", "MOUSSE VISCO"
        ])
        
        # Combo box pour la housse
        self.combo_housse = QComboBox()
        self.combo_housse.addItems([
            "(choisir)", "TENCEL LUXE 3D", "TENCEL", "POLYESTER"
        ])
        
        # Combo box pour le type de literie
        self.combo_type_literie = QComboBox()
        self.combo_type_literie.addItems([
            "(choisir)", "1 PIÈCE", "JUMEAUX"
        ])
        
        self.input_dimensions_housse = QLineEdit()
        self.input_longueur_housse = QLineEdit()
        self.input_decoupe_noyau = QLineEdit()
        
        # Ajout des champs au formulaire
        layout_donnees.addRow("Largeur (cm):", self.input_largeur)
        layout_donnees.addRow("Longueur (cm):", self.input_longueur)
        layout_donnees.addRow("Épaisseur (cm):", self.input_epaisseur)
        layout_donnees.addRow("Hauteur (cm):", self.input_hauteur)
        layout_donnees.addRow("Type de noyau:", self.combo_noyau)
        layout_donnees.addRow("Type de housse:", self.combo_housse)
        layout_donnees.addRow("Type de literie:", self.combo_type_literie)
        layout_donnees.addRow("Dimensions housse (Lxl):", self.input_dimensions_housse)
        layout_donnees.addRow("Longueur housse (cm):", self.input_longueur_housse)
        layout_donnees.addRow("Découpe noyau:", self.input_decoupe_noyau)
        
        groupe_donnees.setLayout(layout_donnees)
        layout.addWidget(groupe_donnees)
        
        # Bouton de génération
        btn_generer = QPushButton("Générer le pré-import")
        btn_generer.clicked.connect(self.generer_preimport)
        layout.addWidget(btn_generer)
        
        # Zone de résultat
        layout.addWidget(QLabel("Résultat JSON:"))
        self.resultat = QTextEdit()
        self.resultat.setReadOnly(True)
        layout.addWidget(self.resultat)
        
        self.setLayout(layout)
    
    def afficher_alerte(self, message):
        """Affiche une alerte à l'utilisateur"""
        self.zone_alertes.setText(f"⚠️ {message}")
        self.zone_alertes.setVisible(True)
    
    def masquer_alerte(self):
        """Masque l'alerte"""
        self.zone_alertes.setVisible(False)
    
    def analyser_texte(self):
        texte = self.input_texte.toPlainText()
        largeur, longueur, epaisseur, hauteur, dimensions_housse, longueur_housse, decoupe_noyau, noyau, housse, type_literie, fermete = detecter_infos_depuis_texte(texte)
        
        # Masquer les alertes précédentes
        self.masquer_alerte()
        
        # Remplissage des champs
        self.input_largeur.setText(largeur)
        self.input_longueur.setText(longueur)
        self.input_epaisseur.setText(epaisseur)
        
        # Sélection du noyau
        if noyau:
            index = self.combo_noyau.findText(noyau)
            if index >= 0:
                self.combo_noyau.setCurrentIndex(index)
        
        # Sélection de la housse
        if housse:
            index = self.combo_housse.findText(housse)
            if index >= 0:
                self.combo_housse.setCurrentIndex(index)
        
        # Sélection du type de literie
        if type_literie:
            index = self.combo_type_literie.findText(type_literie)
            if index >= 0:
                self.combo_type_literie.setCurrentIndex(index)
        
        # Calculs automatiques via le backend
        alertes = []
        
        try:
            # Calcul de la hauteur (vraie logique métier)
            if noyau:
                hauteur_calc = calculer_hauteur_matelas(noyau)
                if hauteur_calc:
                    self.input_hauteur.setText(str(hauteur_calc))
                else:
                    alertes.append("Hauteur non calculée : type de noyau non reconnu")
                    self.input_hauteur.setText(hauteur)
            else:
                alertes.append("Hauteur non calculée : type de noyau non détecté")
                self.input_hauteur.setText(hauteur)
            
            # Calcul de la découpe noyau
            if noyau and fermete and largeur and longueur:
                try:
                    largeur_int = int(largeur)
                    longueur_int = int(longueur)
                    l_dec, L_dec = calcul_decoupe_noyau(noyau, fermete, largeur_int, longueur_int)
                    # Forcer l'utilisation du point décimal
                    l_str = str(l_dec).replace(',', '.')
                    L_str = str(L_dec).replace(',', '.')
                    self.input_decoupe_noyau.setText(f"{l_str} x {L_str}")
                except Exception as e:
                    alertes.append(f"Découpe noyau non calculée : {str(e)}")
                    self.input_decoupe_noyau.setText(decoupe_noyau)
            else:
                if not noyau:
                    alertes.append("Découpe noyau non calculée : type de noyau non détecté")
                if not fermete:
                    alertes.append(f"Découpe noyau non calculée : fermeté non détectée (FERME/MÉDIUM/CONFORT) - Texte: '{texte[:100]}...'")
                if not largeur or not longueur:
                    alertes.append("Découpe noyau non calculée : dimensions manquantes")
                self.input_decoupe_noyau.setText(decoupe_noyau)
            
            # Calculs des dimensions housse selon le type
            val_largeur = None
            val_longueur = None
            
            try:
                if "LATEX NATUREL" in noyau:
                    val_largeur = get_valeur_latex_naturel(int(largeur), housse) if largeur else None
                    val_longueur = get_latex_naturel_longueur_housse_value(int(longueur), housse) if longueur else None
                elif "LATEX MIXTE 7 ZONES" in noyau:
                    val_largeur = get_valeur_latex_mixte7zones(int(largeur), housse) if largeur else None
                    val_longueur = get_latex_mixte7zones_longueur_housse_value(int(longueur), housse) if longueur else None
                elif "MOUSSE RAINURÉE 7 ZONES" in noyau:
                    val_largeur = get_valeur_mousse_rainuree7zones(int(largeur), housse) if largeur else None
                    val_longueur = get_mousse_rainuree7zones_longueur_housse_value(int(longueur), housse) if longueur else None
                elif "LATEX RENFORCE" in noyau:
                    val_largeur = get_latex_renforce_display_value(int(largeur), housse) if largeur else None
                    val_longueur = get_latex_renforce_longueur_housse(int(longueur), housse) if longueur else None
                elif "SELECT 43" in noyau:
                    val_largeur = get_select43_display_value(int(largeur), housse) if largeur else None
                    val_longueur = get_select43_longueur_housse_value(int(longueur), housse) if longueur else None
                elif "MOUSSE VISCO" in noyau:
                    # Dimension housse (largeur) - utiliser le bon référentiel
                    val_largeur = get_mousse_visco_value(int(largeur), housse) if largeur else None
                    val_longueur = get_mousse_visco_longueur_value(int(longueur)) if longueur else None
            except Exception as e:
                alertes.append(f"Dimensions housse non calculées : {str(e)}")
            
            # Affichage des valeurs calculées
            if val_largeur:
                self.input_dimensions_housse.setText(str(val_largeur))
            else:
                if noyau and largeur:
                    alertes.append("Dimensions housse non calculées : référentiel non trouvé")
                self.input_dimensions_housse.setText(dimensions_housse)
            
            if val_longueur:
                self.input_longueur_housse.setText(str(val_longueur))
            else:
                if noyau and longueur:
                    alertes.append("Longueur housse non calculée : référentiel non trouvé")
                self.input_longueur_housse.setText(longueur_housse)
                
        except Exception as e:
            alertes.append(f"Erreur générale : {str(e)}")
            # En cas d'erreur, utiliser les valeurs détectées
            self.input_hauteur.setText(hauteur)
            self.input_decoupe_noyau.setText(decoupe_noyau)
            self.input_dimensions_housse.setText(dimensions_housse)
            self.input_longueur_housse.setText(longueur_housse)
        
        # Affichage des alertes
        if alertes:
            self.afficher_alerte(" | ".join(alertes))
    
    def generer_preimport(self):
        # Récupération des valeurs
        largeur = self.input_largeur.text().strip()
        longueur = self.input_longueur.text().strip()
        epaisseur = self.input_epaisseur.text().strip()
        hauteur = self.input_hauteur.text().strip()
        noyau = self.combo_noyau.currentText()
        housse = self.combo_housse.currentText()
        type_literie = self.combo_type_literie.currentText()
        dimensions_housse = self.input_dimensions_housse.text().strip()
        longueur_housse = self.input_longueur_housse.text().strip()
        decoupe_noyau = self.input_decoupe_noyau.text().strip()
        
        # Validation
        if noyau == "(choisir)" or housse == "(choisir)" or type_literie == "(choisir)":
            self.resultat.setPlainText("Erreur: Veuillez sélectionner le type de noyau, housse et literie.")
            return
        
        # Génération du JSON
        preimport = {
            "largeur": largeur,
            "longueur": longueur,
            "epaisseur": epaisseur,
            "hauteur": hauteur,
            "noyau": noyau,
            "housse": housse,
            "type_literie": type_literie,
            "dimensions_housse": dimensions_housse,
            "longueur_housse": longueur_housse,
            "decoupe_noyau": decoupe_noyau,
            "diagnostic": "OK"
        }
        
        self.resultat.setPlainText(json.dumps(preimport, indent=2, ensure_ascii=False))

# Pour test manuel
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dlg = GenerateurPreImportDialog()
    dlg.show()
    sys.exit(app.exec()) 