# 🎨 Frontend Vue.js - Forum Twitter-like

## Vue d'ensemble
Interface utilisateur moderne avec Vue.js 3, Bootstrap 5 et Vue Router pour un forum style Twitter.

## 🏗️ Architecture

### Structure des fichiers
```
frontend/
├── src/
│   ├── components/          # Composants réutilisables
│   │   ├── NavBar.vue      # Barre de navigation
│   │   ├── PostCard.vue    # Carte d'affichage des posts
│   │   └── CreatePost.vue  # Formulaire de création
│   ├── views/              # Pages principales
│   │   ├── Home.vue        # Page d'accueil/timeline
│   │   ├── Login.vue       # Page de connexion
│   │   ├── Register.vue    # Page d'inscription
│   │   └── Profile.vue     # Profil utilisateur
│   ├── services/           # Services API
│   │   └── api.js          # Client API REST
│   ├── App.vue             # Composant racine
│   └── main.js             # Point d'entrée
├── package.json            # Dépendances
├── vite.config.js          # Configuration Vite
├── index.html              # Template HTML
├── Dockerfile              # Image Docker
└── README.md               # Cette documentation
```

## 🔧 Technologies utilisées
- **Vue.js 3** : Framework progressif
- **Vue Router** : Routage côté client
- **Vite** : Build tool moderne et rapide
- **Bootstrap 5** : Framework CSS
- **Axios** : Client HTTP pour l'API
- **Bootstrap Icons** : Icônes

## 🌐 Pages et fonctionnalités

### 🏠 **Page d'accueil (`/`)**
- Timeline des posts de tous les utilisateurs
- Formulaire de création de posts (si connecté)
- Sidebar avec statistiques et utilisateurs suggérés
- Pagination avec "Charger plus"

### 🔐 **Authentification**
- **Connexion (`/login`)** : Formulaire de connexion avec validation
- **Inscription (`/register`)** : Création de compte avec validation complète

### 👤 **Profil utilisateur (`/profile/:username`)**
- Affichage des informations utilisateur
- Liste des posts de l'utilisateur
- Statistiques (nombre de posts, date d'inscription)

## 🚀 Utilisation

### Développement local
```bash
# Installer les dépendances
npm install

# Lancer le serveur de développement
npm run dev

# Application accessible sur http://localhost:3000
```

### Build de production
```bash
# Build pour la production
npm run build

# Prévisualiser le build
npm run preview
```

### Docker
```bash
# Build de l'image
docker build -t forum-frontend .

# Lancement du conteneur
docker run -d \
  --name forum-ui \
  -p 3000:3000 \
  forum-frontend
```

## 🔗 Communication avec l'API
- **Base URL** : `http://localhost:8000`
- **Sessions** : Utilisation des cookies HTTP pour l'authentification
- **CORS** : Configuré pour accepter les requêtes cross-origin

### Principales fonctionnalités API
- ✅ Authentification (login/logout/register)
- ✅ CRUD des posts avec likes
- ✅ Système de commentaires
- ✅ Profils utilisateur
- ✅ Timeline publique

## 🎨 Interface utilisateur

### Design
- **Couleurs** : Palette inspirée de Twitter (bleu #1da1f2)
- **Responsive** : Compatible mobile/desktop
- **Icons** : Bootstrap Icons pour une cohérence visuelle
- **Animations** : Transitions CSS pour les interactions

### Composants principaux
- **NavBar** : Navigation adaptative avec menu utilisateur
- **PostCard** : Affichage des posts avec actions (like, commentaire)
- **CreatePost** : Formulaire de création avec prévisualisation
- **Forms** : Validation côté client avec feedback visuel

## ⚙️ Configuration

### Variables d'environnement
- L'URL de l'API est configurée dans `src/services/api.js`
- Modifier `API_BASE_URL` selon l'environnement

### Routing
- Routes publiques : `/`, `/login`, `/register`, `/profile/:username`
- Guard d'authentification prêt pour les routes privées
- Gestion automatique des redirections

## 🧪 Test de l'interface
1. **Inscription** : Créer un compte sur `/register`
2. **Connexion** : Se connecter sur `/login`  
3. **Posts** : Créer et liker des posts sur `/`
4. **Profil** : Consulter un profil sur `/profile/:username`
5. **Navigation** : Tester la barre de navigation et la déconnexion