FROM node:18-alpine

# Répertoire de travail
WORKDIR /app

# Copier les fichiers de configuration
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier le code source
COPY . .

# Build de l'application
RUN npm run build

# Installer serve pour servir l'application en production
RUN npm install -g serve

# Exposer le port
EXPOSE 3000

# Variables d'environnement
ENV NODE_ENV=production

# Commande de démarrage
CMD ["serve", "-s", "dist", "-l", "3000"]