# 🐦 Forum Twitter-like - Site Reliability Project

Un forum de type Twitter développé pour tester l'utilisation de Docker avec une architecture microservices.

## 🏗️ Architecture

### Services
- **Database** : MariaDB 11.2 avec schéma complet (utilisateurs, posts, commentaires, likes)
- **Backend** : FastAPI avec SQLAlchemy, authentification par sessions, bcrypt
- **Frontend** : Vue.js 3 + Vite + Bootstrap 5, interface responsive

### Technologies
- 🐳 **Docker & Docker Compose** pour l'orchestration
- 🗄️ **MariaDB** pour la persistance des données
- ⚡ **FastAPI** pour l'API REST
- 🎨 **Vue.js 3** pour l'interface utilisateur
- 🔐 **Sessions HTTP** pour l'authentification

## 🐳 Images Docker Hub

Les images sont disponibles sur Docker Hub sous le namespace `thomasf22` :

| Service | Image Docker Hub | Description |
|---------|------------------|-------------|
| Database | [`thomasf22/forum-database:latest`](https://hub.docker.com/r/thomasf22/forum-database) | MariaDB avec schéma forum pré-configuré |
| Backend | [`thomasf22/forum-backend:latest`](https://hub.docker.com/r/thomasf22/forum-backend) | API FastAPI avec authentification |
| Frontend | [`thomasf22/forum-frontend:latest`](https://hub.docker.com/r/thomasf22/forum-frontend) | Interface Vue.js optimisée pour production |

## 🚀 Démarrage rapide

### Prérequis
- Docker et Docker Compose installés
- Ports 3000, 8000 et 3306 disponibles

## 🚀 Démarrage rapide

### Prérequis
- Docker et Docker Compose installés
- Ports 3000, 8000 et 3306 disponibles

### Option 1: Avec le code source
```bash
# Clone du projet
git clone <your-repo-url>
cd tp

# Démarrage avec Docker Compose
docker-compose up -d
```

### Option 2: Images Docker Hub uniquement
```bash
# Télécharge uniquement le docker-compose.yml
curl -o docker-compose.yml https://raw.githubusercontent.com/YOUR_REPO/main/docker-compose.yml

# Lance tous les services
docker-compose up -d
```

### ✅ Services disponibles
- **Frontend** : http://localhost:3000
- **API Backend** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs
- **Base de données** : localhost:3306

📖 **Guide complet** : Voir [INSTALL.md](INSTALL.md) pour instructions détaillées

### Lancer tous les services
```bash
# Clone du projet
git clone <your-repo-url>
cd tp

# Démarrage avec Docker Compose
docker-compose up -d

# Vérification des services
docker-compose ps
```

### Accès aux services
- **Frontend** : http://localhost:3000
- **API Backend** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs
- **Base de données** : localhost:3306

## 📋 Fonctionnalités

### ✅ Authentification
- Inscription utilisateur avec validation
- Connexion par sessions HTTP sécurisées
- Gestion des profils utilisateur

### ✅ Posts & Interactions
- Création et suppression de posts
- Système de likes/unlikes temps réel
- Commentaires sur les posts
- Timeline personnalisée

### ✅ Interface moderne
- Design Bootstrap 5 responsive
- Icônes Bootstrap Icons
- Navigation intuitive
- Gestion d'état en temps réel

## 🔧 Développement

### Structure du projet
```
tp/
├── db/                 # Configuration MariaDB
│   ├── Dockerfile
│   ├── init.sql        # Schéma de base
│   └── my.cnf          # Configuration MySQL
├── backend/            # API FastAPI
│   ├── Dockerfile
│   ├── main.py
│   ├── models.py       # Modèles SQLAlchemy
│   ├── routes_*.py     # Endpoints API
│   └── requirements.txt
├── frontend/           # Application Vue.js
│   ├── Dockerfile
│   ├── src/
│   │   ├── views/      # Pages
│   │   ├── components/ # Composants réutilisables
│   │   └── services/   # API client
│   └── package.json
└── docker-compose.yml  # Orchestration
```

### Variables d'environnement

#### Base de données
- `MYSQL_DATABASE=forum_db`
- `MYSQL_USER=forum_user`
- `MYSQL_PASSWORD=forum_password`
- `MYSQL_ROOT_PASSWORD=root_password`

#### Backend
- `DATABASE_URL=mysql+pymysql://forum_user:forum_password@database:3306/forum_db`
- `SECRET_KEY=your-super-secret-key-change-in-production`
- `DEBUG=False`

#### Frontend
- `VITE_API_BASE_URL=http://localhost:8000`

## 🐳 Build & Push des images

Pour construire et pousser les images sur Docker Hub :

```powershell
# Windows PowerShell
.\build-and-push.ps1

# Ou manuellement
docker build -t thomasf22/forum-database:latest ./db
docker build -t thomasf22/forum-backend:latest ./backend
docker build -t thomasf22/forum-frontend:latest ./frontend

docker push thomasf22/forum-database:latest
docker push thomasf22/forum-backend:latest
docker push thomasf22/forum-frontend:latest
```

## 🔧 Commandes utiles

```bash
# Démarrer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter tous les services
docker-compose down

# Reconstruire les images
docker-compose build --no-cache

# Vérifier la santé des services
docker-compose ps
```

## 📊 Monitoring

Chaque service inclut des healthchecks :
- **Database** : `mysqladmin ping`
- **Backend** : `curl http://localhost:8000/health`
- **Frontend** : `curl http://localhost:3000`

## 🎯 Objectifs pédagogiques

Ce projet démontre :
- 📦 **Conteneurisation** avec Docker
- 🔗 **Orchestration** avec Docker Compose
- 🌐 **Architecture microservices**
- 🗄️ **Persistance des données** avec volumes
- 🔒 **Sécurité** avec authentification par sessions
- 🚀 **Déploiement** avec images Docker Hub

## 👤 Auteur

**Thomas F.** - Projet Site Reliability M1 S2 2026

---
*Projet réalisé dans le cadre du module Site Reliability - M1 S2 2026*