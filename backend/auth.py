import secrets
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models import User, UserSession
from database import get_db

# Configuration du hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Durée des sessions (7 jours)
SESSION_EXPIRE_DAYS = 7

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie si le mot de passe correspond au hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash un mot de passe"""
    # bcrypt a une limite de 72 caractères, on tronque si nécessaire
    if len(password.encode('utf-8')) > 72:
        password = password[:72]
    return pwd_context.hash(password)

def create_session(db: Session, user_id: int) -> str:
    """Crée une nouvelle session pour l'utilisateur"""
    session_id = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(days=SESSION_EXPIRE_DAYS)
    
    # Désactiver les anciennes sessions
    db.query(UserSession).filter(
        UserSession.user_id == user_id,
        UserSession.is_active == True
    ).update({"is_active": False})
    
    # Créer la nouvelle session
    db_session = UserSession(
        session_id=session_id,
        user_id=user_id,
        expires_at=expires_at,
        is_active=True
    )
    db.add(db_session)
    db.commit()
    
    return session_id

def get_current_user(session_id: str, db: Session) -> Optional[User]:
    """Récupère l'utilisateur à partir de la session"""
    if not session_id:
        return None
    
    # Chercher la session active et non expirée
    session = db.query(UserSession).filter(
        UserSession.session_id == session_id,
        UserSession.is_active == True,
        UserSession.expires_at > datetime.utcnow()
    ).first()
    
    if not session:
        return None
    
    # Retourner l'utilisateur associé
    return db.query(User).filter(
        User.id == session.user_id,
        User.is_active == True
    ).first()

def invalidate_session(session_id: str, db: Session) -> bool:
    """Invalide une session (logout)"""
    session = db.query(UserSession).filter(
        UserSession.session_id == session_id,
        UserSession.is_active == True
    ).first()
    
    if session:
        session.is_active = False
        db.commit()
        return True
    return False

def authenticate_user(username: str, password: str, db: Session) -> Optional[User]:
    """Authentifie un utilisateur"""
    user = db.query(User).filter(
        User.username == username,
        User.is_active == True
    ).first()
    
    if not user:
        return None
    
    if not verify_password(password, user.password_hash):
        return None
    
    return user

def cleanup_expired_sessions(db: Session):
    """Nettoie les sessions expirées"""
    db.query(UserSession).filter(
        UserSession.expires_at < datetime.utcnow()
    ).update({"is_active": False})
    db.commit()