from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os

# Import des routes
from routes_auth import router as auth_router
from routes_posts import router as posts_router
from routes_comments import router as comments_router
from routes_users import router as users_router

# Import de la base de données
from database import engine, Base
from auth import cleanup_expired_sessions, get_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestionnaire de cycle de vie de l'application"""
    # Démarrage : créer les tables si elles n'existent pas
    print("🚀 Starting Forum API...")
    
    # Créer les tables (si elles n'existent pas déjà)
    # En production, utilisez Alembic pour les migrations
    Base.metadata.create_all(bind=engine)
    
    # Nettoyer les sessions expirées au démarrage
    try:
        db = next(get_db())
        cleanup_expired_sessions(db)
        print("✅ Expired sessions cleaned")
    except Exception as e:
        print(f"⚠️ Could not clean expired sessions: {e}")
    
    yield
    
    # Arrêt de l'application
    print("👋 Shutting down Forum API...")

# Créer l'application FastAPI
app = FastAPI(
    title="Forum Twitter-like API",
    description="API REST pour un forum style Twitter avec authentification, posts, commentaires et likes",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Frontend Vue.js
        "http://127.0.0.1:3000",
        "http://localhost:8080",  # Alternative port Vue.js
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,  # Important pour les cookies de session
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes
app.include_router(auth_router)
app.include_router(posts_router)
app.include_router(comments_router)
app.include_router(users_router)

# Route de base pour vérifier que l'API fonctionne
@app.get("/")
def read_root():
    return {
        "message": "🚀 Forum Twitter-like API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

# Route de santé pour Docker
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "forum-api"}

# Point d'entrée pour le développement
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload en développement
        log_level="info"
    )