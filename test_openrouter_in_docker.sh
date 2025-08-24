#!/bin/bash

# Script pour tester l'intégration OpenRouter dans l'environnement Docker

echo "🧪 Test d'intégration OpenRouter dans Docker"
echo "=============================================="

# Vérifier si la clé API est définie
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "❌ Erreur: Variable OPENROUTER_API_KEY non définie"
    echo ""
    echo "Pour définir la clé API, utilisez:"
    echo "export OPENROUTER_API_KEY='sk-or-votre-cle-api-ici'"
    echo ""
    echo "Ou ajoutez-la au fichier .env:"
    echo "echo 'OPENROUTER_API_KEY=sk-or-votre-cle-api-ici' >> .env"
    exit 1
fi

# Vérifier le format de la clé
if [[ ! "$OPENROUTER_API_KEY" =~ ^sk-or- ]]; then
    echo "❌ Erreur: Format de clé API invalide"
    echo "La clé API OpenRouter doit commencer par 'sk-or-'"
    exit 1
fi

echo "✅ Clé API détectée: ${OPENROUTER_API_KEY:0:10}..."

# Vérifier si Docker est en cours d'exécution
if ! docker info > /dev/null 2>&1; then
    echo "❌ Erreur: Docker n'est pas en cours d'exécution"
    exit 1
fi

echo "✅ Docker est en cours d'exécution"

# Vérifier si le conteneur backend existe
if ! docker ps -a --format "table {{.Names}}" | grep -q "matelas_final-backend-1"; then
    echo "❌ Erreur: Conteneur backend non trouvé"
    echo "Lancez d'abord l'application avec: docker-compose up -d"
    exit 1
fi

echo "✅ Conteneur backend trouvé"

# Copier le script de test dans le conteneur
echo "📋 Copie du script de test dans le conteneur..."
docker cp test_openrouter_docker.py matelas_final-backend-1:/app/test_openrouter_docker.py

# Exécuter le test dans le conteneur
echo "🚀 Exécution du test dans le conteneur..."
docker exec -e OPENROUTER_API_KEY="$OPENROUTER_API_KEY" matelas_final-backend-1 python test_openrouter_docker.py

# Nettoyer
echo "🧹 Nettoyage..."
docker exec matelas_final-backend-1 rm -f /app/test_openrouter_docker.py

echo ""
echo "✅ Test terminé!" 