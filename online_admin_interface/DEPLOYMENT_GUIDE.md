# 🚀 GUIDE DE DÉPLOIEMENT SERVEUR EN LIGNE

## 📋 ÉTAPES DE DÉPLOIEMENT

### 1. Préparation du serveur
```bash
# Sur votre serveur Linux (Ubuntu/Debian)
sudo apt update
sudo apt install python3 python3-pip nginx certbot

# Installer les dépendances Python
pip3 install fastapi uvicorn jinja2 python-multipart
```

### 2. Configuration du serveur
```bash
# Copier les fichiers sur le serveur
scp -r online_admin_interface/* user@your-server.com:/var/www/matelas-updates/

# Créer le service systemd
sudo nano /etc/systemd/system/matelas-updates.service
```

Contenu du service:
```ini
[Unit]
Description=MATELAS Update Server
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/matelas-updates
Environment=PATH=/usr/local/bin:/usr/bin:/bin
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### 3. Configuration Nginx
```nginx
server {
    listen 80;
    server_name updates.votre-domaine.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Augmenter la taille max pour les uploads
    client_max_body_size 500M;
}
```

### 4. SSL avec Let's Encrypt
```bash
sudo certbot --nginx -d updates.votre-domaine.com
```

### 5. Démarrage des services
```bash
sudo systemctl enable matelas-updates
sudo systemctl start matelas-updates
sudo systemctl enable nginx
sudo systemctl restart nginx
```

## 🌐 URLS D'ACCÈS

- **Interface Admin**: https://updates.votre-domaine.com/admin
- **API Clients**: https://updates.votre-domaine.com/api/v1/check-updates
- **Identifiants par défaut**: admin / matelas2025

## 🔧 CONFIGURATION PRODUCTION

### Sécurité
1. Changez le mot de passe admin dans main.py (ligne 42)
2. Configurez un reverse proxy Nginx
3. Activez HTTPS avec certbot
4. Limitez les IPs d'administration (optionnel)

### Performance
1. Configurez les logs rotatifs
2. Monitorer l'espace disque (dossier versions/)
3. Backup automatique quotidien
4. Configuration firewall (ports 80, 443, 22)

### Backup
```bash
# Script de backup quotidien
#!/bin/bash
tar -czf backup-$(date +%Y%m%d).tar.gz /var/www/matelas-updates/update_storage/
```

## 📱 UTILISATION DEPUIS VOTRE POSTE

1. **Via navigateur**: https://updates.votre-domaine.com/admin
2. **Upload direct**: Glisser-déposer vos fichiers ZIP
3. **Gestion visuelle**: Aucune ligne de code à toucher
4. **Statistiques temps réel**: Voir les téléchargements
