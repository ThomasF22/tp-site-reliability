FROM mariadb:11.2

# Variables d'environnement
ENV MYSQL_DATABASE=forum_db
ENV MYSQL_USER=forum_user
ENV MYSQL_PASSWORD=forum_password
ENV MYSQL_ROOT_PASSWORD=root_password

# Copier le script d'initialisation
COPY init.sql /docker-entrypoint-initdb.d/

# Exposer le port standard MySQL/MariaDB
EXPOSE 3306

# Configuration pour optimiser la base
COPY my.cnf /etc/mysql/conf.d/

# Volume pour la persistance des données
VOLUME ["/var/lib/mysql"]