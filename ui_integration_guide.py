
# Intégration des optimisations UI
# Ajouter ces imports au début de app_gui.py

try:
    from ui_optimizations import UIOptimizationManager, SmartProgressBar
    from enhanced_processing_ui import OptimizedProcessingDialog
    from gui_enhancements import MatelasAppEnhancements, SmartFileSelector
    UI_ENHANCEMENTS_AVAILABLE = True
    print("✅ Améliorations UI chargées")
except ImportError as e:
    print(f"⚠️ Améliorations UI non disponibles: {e}")
    UI_ENHANCEMENTS_AVAILABLE = False

# Dans la classe MatelasApp.__init__(), ajouter:
if UI_ENHANCEMENTS_AVAILABLE:
    self.ui_enhancements = MatelasAppEnhancements(self)
    self.ui_enhancements.apply_all_enhancements()

# Pour remplacer les dialogues de progression existants:
def show_optimized_processing_dialog(self, files):
    if UI_ENHANCEMENTS_AVAILABLE:
        dialog = OptimizedProcessingDialog(files, self)
        return dialog.exec()
    else:
        # Utiliser le dialogue standard
        return self.show_standard_dialog(files)
