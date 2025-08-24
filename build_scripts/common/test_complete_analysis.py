#!/usr/bin/env python3
"""
Script de test complet pour simuler l'analyse d'un fichier PDF
"""

import sys
import os
import tempfile
sys.path.append('.')

from app_gui import ProcessingThread
from datetime import datetime

def create_test_pdf():
    """Crée un fichier PDF de test temporaire"""
    try:
        import fitz  # PyMuPDF
        
        # Créer un document PDF temporaire
        doc = fitz.open()
        page = doc.new_page()
        
        # Ajouter du texte de test
        text = """
        COMMANDE MATELAS WESTELYNCK
        
        Client: Jean Dupont
        Date: 19/07/2025
        
        Articles commandés:
        - 1 Matelas latex naturel 160x200
        - 1 Sommier lattes bois massif 160x200
        - 2 Oreillers mémoire de forme
        
        Total: 850€
        """
        
        page.insert_text((50, 50), text)
        doc.save("test_commande.pdf")
        doc.close()
        
        return "test_commande.pdf"
        
    except ImportError:
        print("⚠️ PyMuPDF non disponible, création d'un fichier texte")
        with open("test_commande.txt", "w") as f:
            f.write("COMMANDE MATELAS WESTELYNCK\nMatelas latex + Sommier lattes")
        return "test_commande.txt"
    except Exception as e:
        print(f"❌ Erreur création fichier test: {e}")
        return None

def test_complete_analysis():
    """Test complet de l'analyse"""
    print("🧪 Test complet de l'analyse")
    print("=" * 50)
    
    # Créer un fichier de test
    test_file = create_test_pdf()
    if not test_file:
        print("❌ Impossible de créer le fichier de test")
        return
    
    print(f"📄 Fichier de test créé: {test_file}")
    
    try:
        # Créer une instance de ProcessingThread pour tester
        thread = ProcessingThread(
            files=[test_file],
            enrich_llm=False,  # Pas d'LLM pour ce test
            llm_provider="ollama",
            openrouter_api_key="",
            semaine_prod=datetime.now().isocalendar()[1],
            annee_prod=datetime.now().year,
            commande_client=["TEST001"]
        )
        
        # Simuler l'analyse préliminaire
        print("\n🔍 Début de l'analyse préliminaire...")
        
        # Analyser le contenu du fichier
        try:
            # Extraction du texte du PDF
            text = ""
            try:
                import fitz  # PyMuPDF
                doc = fitz.open(test_file)
                text = "\n".join(page.get_text() for page in doc)
                doc.close()
                print(f"✅ Texte extrait: {len(text)} caractères")
            except ImportError:
                print("⚠️ PyMuPDF non disponible, lecture du fichier texte")
                with open(test_file, "r") as f:
                    text = f.read()
            except Exception as e:
                print(f"⚠️ Erreur extraction PDF: {e}")
                text = "MATELAS SOMMIER"  # Texte par défaut
            
            # Analyse du contenu
            has_matelas, has_sommiers, matelas_count, sommier_count = thread.analyze_text_content(text)
            
            print(f"📊 Résultats de l'analyse:")
            print(f"   - Matelas détectés: {has_matelas} ({matelas_count} occurrences)")
            print(f"   - Sommiers détectés: {has_sommiers} ({sommier_count} occurrences)")
            
            # Calculer les recommandations
            try:
                from backend.date_utils import calculate_production_weeks
                semaine_actuelle = datetime.now().isocalendar()[1]
                annee_actuelle = datetime.now().year
                
                recommendations = calculate_production_weeks(
                    semaine_actuelle, annee_actuelle, has_matelas, has_sommiers
                )
                
                print(f"📅 Recommandations calculées:")
                print(f"   - Semaine matelas: {recommendations['matelas']['semaine']}/{recommendations['matelas']['annee']}")
                print(f"   - Semaine sommiers: {recommendations['sommiers']['semaine']}/{recommendations['sommiers']['annee']}")
                print(f"   - Recommandation: {recommendations['recommandation']}")
                
            except Exception as e:
                print(f"⚠️ Erreur calcul recommandations: {e}")
                # Valeurs par défaut
                semaine_actuelle = datetime.now().isocalendar()[1]
                annee_actuelle = datetime.now().year
                print(f"📅 Recommandations par défaut:")
                print(f"   - Semaine matelas: {semaine_actuelle + 1}/{annee_actuelle}")
                print(f"   - Semaine sommiers: {semaine_actuelle + 1}/{annee_actuelle}")
                print(f"   - Recommandation: Analyse réussie: {has_matelas} matelas, {has_sommiers} sommiers")
            
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse: {e}")
        
        print("\n✅ Test complet terminé")
        
    finally:
        # Nettoyer le fichier de test
        try:
            os.remove(test_file)
            print(f"🧹 Fichier de test supprimé: {test_file}")
        except:
            pass

if __name__ == "__main__":
    test_complete_analysis() 