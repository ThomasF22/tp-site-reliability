FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Répertoire de travail
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Copier le script d'attente et le rendre exécutable
COPY wait-for-db.sh .
RUN chmod +x wait-for-db.sh

# Créer un utilisateur non-root
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# Exposer le port
EXPOSE 8000

# Commande par défaut avec attente de la DB
CMD ["./wait-for-db.sh"]