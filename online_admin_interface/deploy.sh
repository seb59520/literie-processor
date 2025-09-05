#!/bin/bash
# Script de déploiement automatique pour serveur

set -e

echo "🚀 DÉPLOIEMENT SERVEUR MATELAS UPDATE"
echo "===================================="

# Variables
SERVER_USER=${1:-"root"}
SERVER_HOST=${2:-"your-server.com"}
SERVER_PATH="/var/www/matelas-updates"

if [ "$SERVER_HOST" = "your-server.com" ]; then
    echo "❌ Usage: ./deploy.sh <user> <server-host>"
    echo "   Exemple: ./deploy.sh ubuntu updates.mondomaine.com"
    exit 1
fi

echo "📤 Envoi des fichiers vers $SERVER_USER@$SERVER_HOST..."

# Créer le répertoire sur le serveur
ssh $SERVER_USER@$SERVER_HOST "mkdir -p $SERVER_PATH"

# Copier les fichiers
rsync -avz --delete \
    --exclude=".git" \
    --exclude="*.pyc" \
    --exclude="__pycache__" \
    ./ $SERVER_USER@$SERVER_HOST:$SERVER_PATH/

echo "⚙️ Installation des dépendances sur le serveur..."

ssh $SERVER_USER@$SERVER_HOST << 'EOF'
cd /var/www/matelas-updates
pip3 install fastapi uvicorn jinja2 python-multipart
mkdir -p update_storage/{versions,metadata}
chmod 755 main.py
EOF

echo "🔧 Configuration du service systemd..."

ssh $SERVER_USER@$SERVER_HOST << 'EOF'
cat > /etc/systemd/system/matelas-updates.service << 'UNIT'
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
UNIT

systemctl daemon-reload
systemctl enable matelas-updates
systemctl restart matelas-updates
EOF

echo "✅ DÉPLOIEMENT TERMINÉ!"
echo ""
echo "🌐 Votre serveur est accessible à:"
echo "   http://$SERVER_HOST:8080/admin"
echo ""
echo "🔐 Identifiants par défaut:"
echo "   Utilisateur: admin"
echo "   Mot de passe: matelas2025"
echo ""
echo "⚠️  N'oubliez pas de:"
echo "   1. Configurer Nginx en reverse proxy"
echo "   2. Installer SSL avec certbot"
echo "   3. Changer le mot de passe admin"
