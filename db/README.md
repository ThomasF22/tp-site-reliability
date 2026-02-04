# 🗃️ Base de données - Forum Twitter-like

## Vue d'ensemble
Base de données MariaDB avec schéma complet pour un forum style Twitter.

## 📋 Structure des tables

### `users` - Utilisateurs
- Authentification et profils
- Champs : username, email, password_hash, display_name, bio, avatar_url

### `posts` - Messages principaux  
- Posts des utilisateurs avec contenu texte/image
- Référence vers l'auteur (user_id)

### `comments` - Commentaires
- Réponses aux posts
- Référence vers le post et l'auteur

### `post_likes` & `comment_likes` - Système de likes
- Likes sur posts et commentaires
- Contrainte unique pour éviter les doublons

### `user_sessions` - Sessions d'authentification
- Gestion des sessions utilisateur
- Expiration automatique

## 🚀 Utilisation

### Build de l'image
```bash
cd tp/db
docker build -t forum-db .
```

### Lancement du conteneur
```bash
docker run -d \
  --name forum-database \
  -e MYSQL_ROOT_PASSWORD=root_password \
  -e MYSQL_DATABASE=forum_db \
  -e MYSQL_USER=forum_user \
  -e MYSQL_PASSWORD=forum_password \
  -p 3306:3306 \
  -v forum_data:/var/lib/mysql \
  forum-db
```

### Connexion à la base
```bash
docker exec -it forum-database mariadb -u forum_user -p forum_password
```

## 📊 Données de test
Le script `init.sql` inclut :
- 3 utilisateurs de test
- 4 posts d'exemple  
- Commentaires et likes de démonstration

## 🔧 Configuration
- Encodage UTF8MB4 pour les emojis
- Optimisations pour le développement
- Logs des requêtes lentes activés