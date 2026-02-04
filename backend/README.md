# 🚀 Backend FastAPI - Forum Twitter-like

## Vue d'ensemble
API REST complète avec authentification par sessions, gestion des posts, commentaires et likes.

## 🏗️ Architecture

### Structure des fichiers
```
backend/
├── main.py              # Point d'entrée FastAPI
├── database.py          # Configuration SQLAlchemy
├── models.py            # Models ORM
├── schemas.py           # Schémas Pydantic
├── auth.py              # Système d'authentification
├── routes_auth.py       # Endpoints d'authentification
├── routes_posts.py      # Endpoints des posts
├── routes_comments.py   # Endpoints des commentaires
├── routes_users.py      # Endpoints des utilisateurs
├── requirements.txt     # Dépendances Python
├── Dockerfile          # Image Docker
├── .env.example        # Variables d'environnement
└── README.md           # Cette documentation
```

## 🔧 Technologies utilisées
- **FastAPI** : Framework web moderne et rapide
- **SQLAlchemy** : ORM pour la base de données
- **Pydantic** : Validation et sérialisation des données
- **Passlib** : Hachage des mots de passe (bcrypt)
- **PyMySQL** : Driver MySQL/MariaDB

## 🌐 API Endpoints

### Authentification (`/auth`)
- `POST /auth/register` - Inscription
- `POST /auth/login` - Connexion  
- `POST /auth/logout` - Déconnexion
- `GET /auth/me` - Informations utilisateur connecté

### Posts (`/posts`)
- `GET /posts/` - Liste des posts (timeline)
- `GET /posts/{id}` - Post spécifique avec commentaires
- `POST /posts/` - Créer un post
- `PUT /posts/{id}` - Modifier son post
- `DELETE /posts/{id}` - Supprimer son post
- `POST /posts/{id}/like` - Liker/unliker un post

### Commentaires (`/comments`)
- `POST /comments/` - Créer un commentaire
- `GET /comments/post/{post_id}` - Commentaires d'un post
- `PUT /comments/{id}` - Modifier son commentaire
- `DELETE /comments/{id}` - Supprimer son commentaire
- `POST /comments/{id}/like` - Liker/unliker un commentaire

### Utilisateurs (`/users`)
- `GET /users/` - Liste des utilisateurs
- `GET /users/{username}` - Profil utilisateur
- `PUT /users/me` - Modifier son profil
- `GET /users/me/posts` - Ses propres posts

## 🚀 Utilisation

### Développement local
```bash
# Installer les dépendances
pip install -r requirements.txt

# Configurer la base de données (voir .env.example)
cp .env.example .env

# Lancer le serveur de développement
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Docker
```bash
# Build de l'image
docker build -t forum-backend .

# Lancement du conteneur
docker run -d \
  --name forum-api \
  -p 8000:8000 \
  -e DATABASE_URL=mysql+pymysql://forum_user:forum_password@db:3306/forum_db \
  forum-backend
```

## 🔐 Authentification
- **Sessions HTTP** avec cookies sécurisés
- **Hachage bcrypt** pour les mots de passe
- **Expiration automatique** des sessions (7 jours)
- **Nettoyage automatique** des sessions expirées

## 📝 Documentation API
Une fois l'API lancée :
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## 🧪 Tests
```bash
# Vérifier la santé de l'API
curl http://localhost:8000/health

# Tester l'inscription
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"test123","display_name":"Test User"}'
```

## ⚙️ Configuration
Variables d'environnement importantes :
- `DATABASE_URL` : URL de connexion à la base
- `ENVIRONMENT` : development/production  
- `SESSION_EXPIRE_DAYS` : Durée des sessions
- `ALLOWED_ORIGINS` : Domaines autorisés (CORS)