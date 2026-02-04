import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuration base de données
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+pymysql://forum_user:forum_password@localhost:3306/forum_db"
)

# Créer le moteur SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Vérifie la connexion avant utilisation
    pool_recycle=300,    # Renouvelle les connexions toutes les 5 minutes
    echo=True           # Affiche les requêtes SQL (pour le debug)
)

# Session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les models
Base = declarative_base()

# Dependency pour obtenir la session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()