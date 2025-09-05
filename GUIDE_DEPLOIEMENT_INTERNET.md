# 🌐 Guide de Déploiement Internet - Serveur MATELAS

## 🎯 Objectif
Mettre votre serveur de mise à jour MATELAS à disposition sur Internet pour permettre aux clients distants de télécharger les mises à jour automatiquement.

## 🚀 Option 1: Démarrage Rapide avec ngrok (GRATUIT)

### Étape 1: Installation et Configuration
```bash
# Démarrer le déploiement automatique
python3 deploy_internet_ngrok.py
```

Le script va:
1. Installer ngrok (si nécessaire)
2. Configurer l'authentification
3. Démarrer votre serveur local
4. Créer un tunnel Internet public
5. Tester l'accès distant

### Étape 2: Récupérer l'URL Publique
Une fois démarré, vous obtiendrez une URL comme:
```
🌐 URL publique: https://abc123.ngrok.io
```

### Étape 3: Configurer les Clients
```bash
# Configurer automatiquement les clients
python3 configure_clients_for_internet.py
```
Entrez votre URL ngrok quand demandé.

### ⚠️ Limitations ngrok Gratuit
- URL change à chaque redémarrage
- 20 connexions/minute maximum
- Session expire après 8 heures
- Pas de nom de domaine personnalisé

---

## 🖥️ Option 2: Déploiement VPS Production

### Prérequis
- VPS Ubuntu 22.04+ 
- 1 GB RAM minimum
- Nom de domaine (optionnel mais recommandé)

### Étape 1: Préparer le VPS
```bash
# Sur votre VPS
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip nginx certbot python3-certbot-nginx -y

# Créer un utilisateur pour l'application
sudo useradd -m -s /bin/bash matelas
sudo su - matelas
```

### Étape 2: Transférer les Fichiers
```bash
# Depuis votre machine locale
scp -r online_admin_interface/ matelas@VOTRE_IP:/home/matelas/
scp requirements_internet.txt matelas@VOTRE_IP:/home/matelas/
```

### Étape 3: Installation sur VPS
```bash
# Sur le VPS, en tant qu'utilisateur matelas
cd /home/matelas/online_admin_interface
pip3 install -r requirements_internet.txt

# Tester le serveur
python3 enhanced_admin_internet_ready.py
```

### Étape 4: Configuration Nginx
```nginx
# /etc/nginx/sites-available/matelas
server {
    listen 80;
    server_name votre-domaine.com;  # ou votre IP
    
    location / {
        proxy_pass http://127.0.0.1:8091;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Activer le site
sudo ln -s /etc/nginx/sites-available/matelas /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Étape 5: HTTPS avec Let's Encrypt
```bash
sudo certbot --nginx -d votre-domaine.com
```

### Étape 6: Service Systemd
```ini
# /etc/systemd/system/matelas.service
[Unit]
Description=MATELAS Update Server
After=network.target

[Service]
Type=simple
User=matelas
WorkingDirectory=/home/matelas/online_admin_interface
Environment=MATELAS_ADMIN_USER=votre_admin
Environment=MATELAS_ADMIN_PASS=votre_mot_de_passe_fort
ExecStart=/usr/bin/python3 enhanced_admin_internet_ready.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```bash
# Activer le service
sudo systemctl daemon-reload
sudo systemctl enable matelas
sudo systemctl start matelas
sudo systemctl status matelas
```

---

## 🔒 Sécurité Obligatoire

### Changement des Identifiants
```bash
# Définir de nouveaux identifiants
export MATELAS_ADMIN_USER=votre_admin
export MATELAS_ADMIN_PASS=VotreMotDePasseComplexe123!
```

### Firewall
```bash
# Configurer UFW
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw --force enable
```

### Surveillance
```bash
# Consulter les logs de sécurité
tail -f /home/matelas/online_admin_interface/update_storage/logs/security_*.log
```

---

## 💻 Configuration des Clients

### Automatique
```bash
python3 configure_clients_for_internet.py
```

### Manuelle
Modifiez ces fichiers pour remplacer `http://localhost:8091` par votre URL:
- `app_gui.py` (méthode `check_for_updates_async`)
- `backend/auto_updater.py` (toutes les occurrences)

---

## 🧪 Tests de Validation

### Test API Public
```bash
curl https://votre-serveur.com/api/v1/check-updates
```

### Test Interface Admin
Visitez: `https://votre-serveur.com/admin`

### Test Télémétrie
Visitez: `https://votre-serveur.com/admin/clients`

### Test Client
```bash
python3 test_complete_telemetry_update.py
```

---

## 📊 Monitoring et Maintenance

### URLs Importantes
- **Dashboard**: `https://votre-serveur.com/admin`
- **Clients**: `https://votre-serveur.com/admin/clients`
- **Sécurité**: `https://votre-serveur.com/admin/security`
- **API**: `https://votre-serveur.com/api/v1/check-updates`

### Logs à Surveiller
```bash
# Logs applicatifs
tail -f /home/matelas/online_admin_interface/update_storage/logs/*.log

# Logs système
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
sudo journalctl -u matelas -f
```

### Sauvegardes
```bash
# Créer une sauvegarde quotidienne
tar -czf backup_$(date +%Y%m%d).tar.gz /home/matelas/online_admin_interface/update_storage/
```

---

## 🆘 Dépannage

### Problèmes Courants

#### Serveur Non Accessible
```bash
# Vérifier le statut
sudo systemctl status matelas
sudo systemctl status nginx

# Redémarrer si nécessaire
sudo systemctl restart matelas
sudo systemctl restart nginx
```

#### Erreurs de Certificat SSL
```bash
# Renouveler Let's Encrypt
sudo certbot renew --dry-run
sudo certbot renew
```

#### Clients ne Se Connectent Pas
1. Vérifiez l'URL dans le code client
2. Testez l'API manuellement
3. Consultez les logs de sécurité
4. Vérifiez le firewall

---

## 💡 Bonnes Pratiques

### Sécurité
- ✅ Utilisez HTTPS en production
- ✅ Changez les identifiants par défaut
- ✅ Surveillez les logs régulièrement
- ✅ Mettez à jour le système régulièrement
- ✅ Limitez l'accès SSH (clés SSH uniquement)

### Performance
- ✅ Utilisez un CDN pour les gros fichiers
- ✅ Configurez la compression gzip
- ✅ Surveillez l'usage disque/CPU
- ✅ Nettoyez périodiquement les anciens logs

### Maintenance
- ✅ Sauvegardez quotidiennement
- ✅ Testez les restaurations
- ✅ Documentez vos configurations
- ✅ Préparez un plan de reprise d'activité

---

## 📞 Support

En cas de problème, consultez:
1. Les logs d'application dans `update_storage/logs/`
2. Les logs système avec `journalctl -u matelas`
3. Les logs Nginx dans `/var/log/nginx/`
4. L'interface de sécurité: `/admin/security`

---

**🎉 Votre serveur MATELAS est maintenant accessible depuis Internet !**

Les clients pourront désormais recevoir automatiquement les mises à jour, et vous pourrez suivre l'activité de tous les postes via l'interface de télémétrie.