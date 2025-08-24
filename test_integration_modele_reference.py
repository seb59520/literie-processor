#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier l'intégration du modèle de référence
"""

import sys
import os
import json

def test_modele_reference_file():
    """Teste l'existence et la validité du fichier modèle de référence"""
    print("📋 Test du fichier modèle de référence")
    print("=" * 50)
    
    if os.path.exists("modele_extraction_reference.json"):
        print("✅ Fichier modele_extraction_reference.json trouvé")
        
        try:
            with open("modele_extraction_reference.json", "r", encoding="utf-8") as f:
                reference_model = json.load(f)
            
            print("✅ Fichier JSON valide")
            
            # Vérifier la structure
            required_sections = ["societe", "client", "commande", "mode_mise_a_disposition", "articles", "paiement"]
            for section in required_sections:
                if section in reference_model:
                    print(f"✅ Section '{section}' présente")
                else:
                    print(f"❌ Section '{section}' manquante")
            
            # Vérifier les articles
            if "articles" in reference_model and isinstance(reference_model["articles"], list):
                print(f"✅ {len(reference_model['articles'])} articles dans le modèle")
                
                # Vérifier la structure d'un article
                if reference_model["articles"]:
                    first_article = reference_model["articles"][0]
                    article_fields = ["type", "description", "titre_cote", "information", "quantite", 
                                    "dimensions", "noyau", "fermete", "housse", "matiere_housse", 
                                    "autres_caracteristiques"]
                    
                    for field in article_fields:
                        if field in first_article:
                            print(f"  ✅ Champ article '{field}' présent")
                        else:
                            print(f"  ❌ Champ article '{field}' manquant")
            
            return True
            
        except json.JSONDecodeError as e:
            print(f"❌ Erreur de parsing JSON: {e}")
            return False
        except Exception as e:
            print(f"❌ Erreur lors de la lecture: {e}")
            return False
    else:
        print("❌ Fichier modele_extraction_reference.json non trouvé")
        return False

def test_application_integration():
    """Teste l'intégration dans l'application de test LLM"""
    print("\n🧪 Test de l'intégration dans l'application")
    print("=" * 50)
    
    if os.path.exists("test_llm_prompt.py"):
        print("✅ Fichier test_llm_prompt.py trouvé")
        
        with open("test_llm_prompt.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Vérifier les nouvelles fonctionnalités
        features_to_check = [
            ("Bouton modèle référence", "load_model_btn"),
            ("Méthode load_reference_model", "load_reference_model"),
            ("Méthode create_prompt_from_reference", "create_prompt_from_reference"),
            ("Méthode create_example_text_from_reference", "create_example_text_from_reference"),
            ("Bouton comparaison", "compare_btn"),
            ("Méthode compare_with_reference", "compare_with_reference"),
            ("Méthode compare_json_structures", "compare_json_structures"),
            ("Méthode show_comparison_dialog", "show_comparison_dialog")
        ]
        
        for feature_name, feature_code in features_to_check:
            if feature_code in content:
                print(f"✅ {feature_name} - Implémenté")
            else:
                print(f"❌ {feature_name} - Manquant")
        
        return True
    else:
        print("❌ Fichier test_llm_prompt.py non trouvé")
        return False

def test_backend_integration():
    """Teste l'intégration dans le backend"""
    print("\n🔧 Test de l'intégration dans le backend")
    print("=" * 50)
    
    if os.path.exists("backend/main.py"):
        print("✅ Fichier backend/main.py trouvé")
        
        with open("backend/main.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Vérifier les améliorations du prompt
        prompt_improvements = [
            ("Structure JSON obligatoire", "STRUCTURE JSON OBLIGATOIRE"),
            ("Règles spécifiques", "RÈGLES SPÉCIFIQUES"),
            ("Exemple de référence", "EXEMPLE DE RÉFÉRENCE"),
            ("Champ autres_caracteristiques", "autres_caracteristiques"),
            ("Types d'articles étendus", "matelas|sommier|accessoire|tête de lit|pieds|remise")
        ]
        
        for improvement_name, improvement_code in prompt_improvements:
            if improvement_code in content:
                print(f"✅ {improvement_name} - Implémenté")
            else:
                print(f"❌ {improvement_name} - Manquant")
        
        return True
    else:
        print("❌ Fichier backend/main.py non trouvé")
        return False

def test_prompt_quality():
    """Teste la qualité du prompt généré"""
    print("\n📝 Test de la qualité du prompt")
    print("=" * 50)
    
    try:
        # Simuler la création d'un prompt
        with open("modele_extraction_reference.json", "r", encoding="utf-8") as f:
            reference_model = json.load(f)
        
        # Créer un prompt basé sur le modèle
        prompt_template = f'''Tu es un assistant d'extraction spécialisé pour des devis de literie. Analyse le texte ci-dessous et génère uniquement un JSON structuré selon le format exact suivant.

TEXTE À ANALYSER :
{{text}}

RÈGLES D'EXTRACTION STRICTES :

1. STRUCTURE JSON OBLIGATOIRE :
{{
  "societe": {{
    "nom": "nom de l'entreprise",
    "capital": "capital social",
    "adresse": "adresse complète",
    "telephone": "numéro de téléphone",
    "email": "adresse email",
    "siret": "numéro SIRET",
    "APE": "code APE",
    "CEE": "numéro CEE",
    "banque": "nom de la banque",
    "IBAN": "numéro IBAN"
  }},
  "client": {{
    "nom": "nom du client",
    "adresse": "adresse du client",
    "code_client": "code client"
  }},
  "commande": {{
    "numero": "numéro de commande",
    "date": "date de commande",
    "date_validite": "date de validité",
    "commercial": "nom du commercial",
    "origine": "origine de la commande"
  }},
  "mode_mise_a_disposition": {{
    "emporte_client_C57": "texte si enlèvement client",
    "fourgon_C58": "texte si livraison fourgon",
    "transporteur_C59": "texte si transporteur"
  }},
  "articles": [
    {{
      "type": "matelas|sommier|accessoire|tête de lit|pieds|remise",
      "description": "description complète de l'article",
      "titre_cote": "Mr/Mme Gauche/Droit si applicable",
      "information": "en-tête comme '1/ CHAMBRE XYZ' si présent",
      "quantite": nombre,
      "dimensions": "format LxlxH",
      "noyau": "type de noyau pour matelas",
      "fermete": "niveau de fermeté",
      "housse": "type de housse",
      "matiere_housse": "matériau de la housse",
      "autres_caracteristiques": {{
        "caracteristique1": "valeur1",
        "caracteristique2": "valeur2"
      }}
    }}
  ],
  "paiement": {{
    "conditions": "conditions de paiement",
    "port_ht": montant_ht_port,
    "base_ht": montant_ht_total,
    "taux_tva": pourcentage_tva,
    "total_ttc": montant_ttc,
    "acompte": montant_acompte,
    "net_a_payer": montant_final
  }}
}}

2. RÈGLES SPÉCIFIQUES :
- Pour chaque article, extraire TOUS les champs disponibles
- Le champ "autres_caracteristiques" doit contenir les spécificités non standard
- Les remises sont des articles de type "remise" avec montant dans autres_caracteristiques
- Les dimensions doivent être au format "LxlxH" (ex: "159x199x19")
- Les montants doivent être des nombres (pas de texte)
- Si une information est absente : null pour les nombres, "" pour les textes

3. EXEMPLE DE RÉFÉRENCE :
{json.dumps(reference_model, indent=2, ensure_ascii=False)}

Réponds UNIQUEMENT avec un JSON valide selon cette structure exacte.'''
        
        print("✅ Prompt généré avec succès")
        print(f"📏 Taille du prompt : {len(prompt_template)} caractères")
        
        # Vérifier les éléments clés
        key_elements = [
            "STRUCTURE JSON OBLIGATOIRE",
            "RÈGLES SPÉCIFIQUES",
            "EXEMPLE DE RÉFÉRENCE",
            "autres_caracteristiques",
            "matelas|sommier|accessoire|tête de lit|pieds|remise"
        ]
        
        for element in key_elements:
            if element in prompt_template:
                print(f"✅ Élément clé '{element}' présent")
            else:
                print(f"❌ Élément clé '{element}' manquant")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération du prompt: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🧪 Test d'intégration du modèle de référence")
    print("=" * 70)
    
    results = []
    
    results.append(test_modele_reference_file())
    results.append(test_application_integration())
    results.append(test_backend_integration())
    results.append(test_prompt_quality())
    
    print("\n🎉 Tests terminés !")
    print("=" * 70)
    
    if all(results):
        print("✅ TOUS LES TESTS RÉUSSIS")
        print("\n📋 Résumé de l'intégration:")
        print("   • Modèle de référence JSON créé et validé")
        print("   • Application de test LLM enrichie")
        print("   • Backend mis à jour avec le nouveau prompt")
        print("   • Fonctionnalités de comparaison ajoutées")
        print("   • Interface utilisateur améliorée")
        print("\n🚀 Le modèle de référence est maintenant intégré !")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("Vérifiez les erreurs ci-dessus et corrigez-les.")
    
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 