# 🚀 Guide de Déploiement - Forum Twitter-like

## 📋 Prérequis

Avant de commencer, assure-toi d'avoir :
- **Docker** installé ([Docker Desktop](https://www.docker.com/products/docker-desktop/))
- **Docker Compose** (inclus avec Docker Desktop)
- **Ports libres** : 3000, 8000, 3306

## 🎯 Option 1: Lancement rapide (Images Docker Hub)

### Télécharge uniquement le docker-compose.yml

```bash
# Crée un dossier pour le projet
mkdir forum-project
cd forum-project

# Télécharge le fichier docker-compose.yml
curl -o docker-compose.yml https://raw.githubusercontent.com/YOUR_REPO/main/docker-compose.yml
```

### Lance tous les services
```bash
# Démarrage des services (télécharge automatiquement les images)
docker-compose up -d

# Vérification que tout fonctionne
docker-compose ps
```

### ✅ C'est prêt !
- **Frontend** : http://localhost:3000
- **API** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs

## 🎯 Option 2: Développement complet (Code source)

### Clone le projet
```bash
# Clone le repository
git clone <URL_DU_REPO>
cd tp

# Lance tous les services
docker-compose up -d
```

### Build des images locales (optionnel)
```bash
# Si tu veux rebuilder les images localement
docker-compose build --no-cache
docker-compose up -d
```

## 🎯 Option 3: Lancement manuel (étape par étape)

### 1. Base de données
```bash
docker run -d \
  --name forum-database \
  -p 3306:3306 \
  -e MYSQL_DATABASE=forum_db \
  -e MYSQL_USER=forum_user \
  -e MYSQL_PASSWORD=forum_password \
  -e MYSQL_ROOT_PASSWORD=root_password \
  thomasf22/forum-database:latest
```

### 2. Backend API
```bash
docker run -d \
  --name forum-backend \
  -p 8000:8000 \
  -e DATABASE_URL="mysql+pymysql://forum_user:forum_password@forum-database:3306/forum_db" \
  --link forum-database \
  thomasf22/forum-backend:latest
```

### 3. Frontend
```bash
docker run -d \
  --name forum-frontend \
  -p 3000:3000 \
  thomasf22/forum-frontend:latest
```

## 🧪 Test de l'installation

### 1. Vérification des services
```bash
# Vérifie que tous les conteneurs tournent
docker ps

# Ou avec docker-compose
docker-compose ps
```

### 2. Test manuel
- **Frontend** : Ouvre http://localhost:3000
- **API Health** : Ouvre http://localhost:8000/health
- **Documentation** : Ouvre http://localhost:8000/docs

### 3. Test complet
```bash
# Test de création d'utilisateur
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "password123", "display_name": "Test User"}'

# Test de récupération des posts
curl http://localhost:8000/posts/
```

## 🛠️ Commandes utiles

### Gestion des services
```bash
# Démarrer
docker-compose up -d

# Arrêter
docker-compose down

# Redémarrer
docker-compose restart

# Voir les logs
docker-compose logs -f

# Voir les logs d'un service spécifique
docker-compose logs -f backend
```

### Maintenance
```bash
# Reconstruction complète
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Nettoyage (supprime tout)
docker-compose down -v
docker system prune -f
```

## 🔧 Variables d'environnement personnalisables

Crée un fichier `.env` pour personnaliser :

```bash
# .env
MYSQL_ROOT_PASSWORD=your_secure_password
MYSQL_PASSWORD=your_db_password
SECRET_KEY=your_super_secret_key_here
API_PORT=8000
FRONTEND_PORT=3000
DB_PORT=3306
```

Puis lance avec :
```bash
docker-compose --env-file .env up -d
```

## 🆘 Résolution de problèmes

### Port déjà utilisé
```bash
# Trouve ce qui utilise le port
netstat -tulpn | grep :3000
# Ou
lsof -i :3000

# Change le port dans docker-compose.yml
ports:
  - "3001:3000"  # Au lieu de 3000:3000
```

### Services qui ne démarrent pas
```bash
# Vérifie les logs
docker-compose logs database
docker-compose logs backend
docker-compose logs frontend

# Redémarre un service spécifique
docker-compose restart backend
```

### Base de données corrompue
```bash
# Recrée la base de données
docker-compose down -v
docker-compose up -d
```

## 📚 Fonctionnalités disponibles

Une fois lancé, tu peux :
- ✅ **S'inscrire** et se connecter
- ✅ **Créer des posts** avec texte
- ✅ **Liker/Unliker** les posts
- ✅ **Commenter** les publications
- ✅ **Voir les profils** utilisateurs
- ✅ **Timeline** en temps réel

## 🎓 Pour les étudiants

Ce projet démontre :
- **Conteneurisation** avec Docker
- **Orchestration** avec Docker Compose
- **Architecture microservices**
- **API REST** avec FastAPI
- **Frontend moderne** avec Vue.js
- **Base de données relationnelle** avec MariaDB
- **Authentification** par sessions

---

**🎉 Bon test !** 

Si tu rencontres des problèmes, vérifie les logs avec `docker-compose logs` !