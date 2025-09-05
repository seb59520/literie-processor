#!/usr/bin/env python3
"""
Plan de déploiement du serveur de mise à jour MATELAS sur Internet
"""

import os
from pathlib import Path
import json

def analyze_deployment_options():
    """Analyser les options de déploiement disponibles"""
    print("🌐 PLAN DE DÉPLOIEMENT INTERNET - SERVEUR MATELAS")
    print("=" * 60)
    
    print("\n🎯 OBJECTIFS:")
    print("• Rendre le serveur de mise à jour accessible depuis Internet")
    print("• Permettre aux clients distants de télécharger les mises à jour")
    print("• Maintenir l'interface d'administration sécurisée")
    print("• Collecter la télémétrie des postes clients distants")
    
    print("\n🏗️ OPTIONS DE DÉPLOIEMENT:")
    
    # Option 1: VPS/Serveur dédié
    print("\n1. 🖥️ SERVEUR VPS/DÉDIÉ (Recommandé)")
    print("   ✅ Avantages:")
    print("     • Contrôle total du serveur")
    print("     • IP publique fixe")
    print("     • Possibilité d'utiliser un nom de domaine")
    print("     • Sécurité maximale")
    print("   ⚠️ Inconvénients:")
    print("     • Coût mensuel (5-20€/mois)")
    print("     • Configuration système requise")
    print("   🔧 Providers suggérés:")
    print("     • OVH (France): VPS à partir de 3.99€/mois")
    print("     • Scaleway (France): DEV1-S à 2.99€/mois")
    print("     • Hetzner (Allemagne): CX11 à 3.29€/mois")
    print("     • DigitalOcean: Droplet à 5$/mois")
    
    # Option 2: Tunnel (gratuit mais limité)
    print("\n2. 🚇 TUNNEL (Solution temporaire)")
    print("   ✅ Avantages:")
    print("     • Gratuit")
    print("     • Configuration rapide")
    print("     • Pas besoin de serveur")
    print("   ⚠️ Inconvénients:")
    print("     • URLs changeantes")
    print("     • Limitations de bande passante")
    print("     • Moins fiable pour production")
    print("   🔧 Services disponibles:")
    print("     • ngrok (gratuit avec limitations)")
    print("     • Cloudflare Tunnel (gratuit)")
    print("     • serveo.net (gratuit)")
    
    # Option 3: Cloud (plus complexe)
    print("\n3. ☁️ CLOUD PLATFORM")
    print("   ✅ Avantages:")
    print("     • Scalabilité automatique")
    print("     • Haute disponibilité")
    print("     • Intégration avec CDN")
    print("   ⚠️ Inconvénients:")
    print("     • Configuration plus complexe")
    print("     • Coûts variables")
    print("   🔧 Plateformes:")
    print("     • Heroku (simple mais payant)")
    print("     • Railway (gratuit puis payant)")
    print("     • Fly.io (gratuit puis payant)")
    
    return True

def create_vps_deployment_guide():
    """Créer le guide de déploiement VPS"""
    print("\n📋 GUIDE DE DÉPLOIEMENT VPS (Recommandé)")
    print("=" * 45)
    
    # Configuration serveur recommandée
    print("\n⚙️ CONFIGURATION SERVEUR MINIMALE:")
    print("• CPU: 1 vCore")
    print("• RAM: 1 GB")
    print("• Stockage: 20 GB SSD")
    print("• OS: Ubuntu 22.04 LTS (recommandé)")
    print("• Bande passante: 1 TB/mois")
    
    print("\n🛠️ ÉTAPES DE DÉPLOIEMENT:")
    
    steps = [
        "1. Commander un VPS chez un fournisseur",
        "2. Configurer l'accès SSH et sécuriser le serveur",
        "3. Installer Python 3.11+ et les dépendances",
        "4. Transférer les fichiers du serveur MATELAS",
        "5. Configurer un reverse proxy (Nginx)",
        "6. Configurer HTTPS avec Let's Encrypt",
        "7. Configurer un nom de domaine (optionnel)",
        "8. Installer et configurer un service systemd",
        "9. Configurer le firewall et la sécurité",
        "10. Tester et valider le déploiement"
    ]
    
    for step in steps:
        print(f"   {step}")
    
    return True

def create_tunnel_quick_start():
    """Créer le guide de démarrage rapide avec tunnel"""
    print("\n🚇 SOLUTION RAPIDE - TUNNEL NGROK")
    print("=" * 35)
    
    print("\n📦 PRÉREQUIS:")
    print("• Compte ngrok gratuit: https://ngrok.com")
    print("• Application ngrok installée")
    print("• Serveur MATELAS fonctionnel en local")
    
    print("\n⚡ DÉMARRAGE RAPIDE:")
    print("1. Installez ngrok:")
    print("   curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null")
    print("   echo 'deb https://ngrok-agent.s3.amazonaws.com buster main' | sudo tee /etc/apt/sources.list.d/ngrok.list")
    print("   sudo apt update && sudo apt install ngrok")
    
    print("\n2. Configurez votre token ngrok:")
    print("   ngrok config add-authtoken VOTRE_TOKEN")
    
    print("\n3. Démarrez le serveur MATELAS:")
    print("   cd online_admin_interface")
    print("   python3 enhanced_admin_with_telemetry.py")
    
    print("\n4. Dans un autre terminal, créez le tunnel:")
    print("   ngrok http 8091")
    
    print("\n5. Récupérez l'URL publique affichée (ex: https://abc123.ngrok.io)")
    
    print("\n⚠️ LIMITATIONS GRATUITES NGROK:")
    print("• URL change à chaque redémarrage")
    print("• Limite de 20 connexions/minute")
    print("• Timeout après 8 heures")
    print("• Pas de nom de domaine personnalisé")
    
    return True

def create_security_checklist():
    """Créer la checklist de sécurité"""
    print("\n🔒 CHECKLIST DE SÉCURITÉ")
    print("=" * 25)
    
    security_items = [
        "🔐 Changer les identifiants admin par défaut (admin/matelas2025)",
        "🛡️ Configurer HTTPS avec certificat SSL valide",
        "🚪 Limiter l'accès à l'interface d'admin (IP whitelisting)",
        "🔥 Configurer un firewall (ne pas exposer SSH sur port 22)",
        "📊 Monitorer les logs et accès suspects",
        "🔄 Sauvegardes automatiques des données",
        "⚡ Rate limiting pour éviter les attaques DDoS",
        "🕵️ Masquer les headers serveur (version Python/FastAPI)",
        "📝 Logs d'audit pour toutes les actions admin",
        "⏰ Sessions admin avec timeout automatique"
    ]
    
    for item in security_items:
        print(f"   {item}")
    
    print("\n⚠️ POINTS CRITIQUES:")
    print("• L'interface admin (/admin/*) doit être protégée")
    print("• L'API de mise à jour (/api/v1/*) peut être publique")
    print("• Changer immédiatement admin/matelas2025")
    print("• Utiliser HTTPS même avec un certificat auto-signé")
    
    return True

def create_client_configuration_guide():
    """Guide de configuration des clients"""
    print("\n💻 CONFIGURATION DES CLIENTS")
    print("=" * 30)
    
    print("\n📡 MODIFICATION DES CLIENTS:")
    print("Une fois le serveur déployé, vous devez modifier l'URL du serveur")
    print("dans le code client pour pointer vers votre serveur Internet.")
    
    print("\n🔧 FICHIERS À MODIFIER:")
    print("• backend/auto_updater.py")
    print("• app_gui.py (méthodes de vérification)")
    
    print("\n📝 CHANGEMENTS REQUIS:")
    print("Remplacer:")
    print('   "http://localhost:8091"')
    print("Par:")
    print('   "https://votre-serveur.com"  # ou votre URL')
    
    print("\n🎯 EXEMPLE AVEC NGROK:")
    print("Si votre tunnel ngrok donne: https://abc123.ngrok.io")
    print("Modifiez dans check_for_updates_async():")
    print('   update_info = check_for_updates_with_telemetry("https://abc123.ngrok.io")')
    
    print("\n🔄 DÉPLOIEMENT CLIENT:")
    print("1. Modifiez les URLs dans le code")
    print("2. Testez la connexion au serveur distant")
    print("3. Créez une nouvelle version avec les URLs mises à jour")
    print("4. Déployez cette version sur les postes clients")
    
    return True

if __name__ == "__main__":
    print("🚀 Analyse des options de déploiement Internet...")
    print()
    
    # Analyser les options
    analyze_deployment_options()
    
    # Guides détaillés
    create_vps_deployment_guide()
    create_tunnel_quick_start()
    create_security_checklist()
    create_client_configuration_guide()
    
    print("\n🎯 RECOMMANDATIONS:")
    print("=" * 20)
    print("• Pour TESTER rapidement: Utilisez ngrok (gratuit)")
    print("• Pour PRODUCTION: Utilisez un VPS avec nom de domaine")
    print("• Toujours activer HTTPS en production")
    print("• Changer les identifiants admin par défaut")
    print("• Sauvegarder régulièrement les données télémétrie")
    
    print("\n📞 PROCHAINES ÉTAPES:")
    print("1. Choisissez votre méthode de déploiement")
    print("2. Suivez le guide correspondant")
    print("3. Testez l'accès depuis un client externe")
    print("4. Mettez à jour les clients avec la nouvelle URL")
    print("5. Déployez progressivement sur les postes")
    
    print("\n💡 Voulez-vous que je crée les scripts de déploiement spécifiques ?")
    print("Indiquez votre choix:")
    print("• 'vps' pour un guide détaillé VPS")
    print("• 'ngrok' pour commencer rapidement avec ngrok")
    print("• 'docker' pour un déploiement containerisé")