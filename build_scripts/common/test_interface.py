#!/usr/bin/env python3
import requests
import os

def test_interface():
    """Test simple de l'interface"""
    print("🧪 Test de l'interface...")
    
    # Test 1: Page d'accueil
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✅ Page d'accueil accessible")
            if "Analyse de Devis PDF" in response.text:
                print("✅ Interface moderne détectée")
            else:
                print("❌ Interface moderne non détectée")
        else:
            print(f"❌ Erreur page d'accueil: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return
    
    # Test 2: Upload sans LLM
    if os.path.exists("test_devis.pdf"):
        try:
            with open("test_devis.pdf", "rb") as f:
                files = {"file": ("test_devis.pdf", f, "application/pdf")}
                data = {"enrich_llm": "no"}
                
                print("📤 Test upload sans LLM...")
                response = requests.post("http://localhost:8000/upload", files=files, data=data)
                
                if response.status_code == 200:
                    print("✅ Upload réussi")
                    if "Étape 1 : Extraction du texte" in response.text:
                        print("✅ Étapes de traitement affichées")
                    else:
                        print("❌ Étapes de traitement non affichées")
                else:
                    print(f"❌ Erreur upload: {response.status_code}")
                    
        except Exception as e:
            print(f"❌ Erreur upload: {e}")
    else:
        print("⚠️ Fichier test_devis.pdf non trouvé")
    
    print("\n🎯 Test terminé!")
    print("\n📝 Pour tester manuellement:")
    print("1. Ouvrez http://localhost:8000 dans votre navigateur")
    print("2. Upload le fichier test_devis.pdf")
    print("3. Vérifiez que les étapes s'affichent")

if __name__ == "__main__":
    test_interface() 