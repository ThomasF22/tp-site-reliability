from fastapi import APIRouter, Depends, HTTPException, Cookie, Response
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import User
from schemas import UserCreate, UserLogin, LoginResponse, LogoutResponse, User as UserSchema
from auth import (
    get_password_hash, 
    authenticate_user, 
    create_session, 
    get_current_user, 
    invalidate_session
)

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=LoginResponse)
def register(user_data: UserCreate, response: Response, db: Session = Depends(get_db)):
    """Inscription d'un nouvel utilisateur"""
    
    # Vérifier si l'utilisateur existe déjà
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    
    if existing_user:
        if existing_user.username == user_data.username:
            raise HTTPException(status_code=400, detail="Username already taken")
        else:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Créer le nouvel utilisateur
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        display_name=user_data.display_name,
        bio=user_data.bio,
        avatar_url=user_data.avatar_url
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Créer une session automatiquement
    session_id = create_session(db, db_user.id)
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=False,  # True en production avec HTTPS
        samesite="lax",
        max_age=7 * 24 * 60 * 60  # 7 jours
    )
    
    return LoginResponse(
        message="Registration successful",
        user=UserSchema.from_orm(db_user)
    )

@router.post("/login", response_model=LoginResponse)
def login(user_data: UserLogin, response: Response, db: Session = Depends(get_db)):
    """Connexion utilisateur"""
    
    # Authentifier l'utilisateur
    user = authenticate_user(user_data.username, user_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Créer une session
    session_id = create_session(db, user.id)
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=False,  # True en production
        samesite="lax",
        max_age=7 * 24 * 60 * 60  # 7 jours
    )
    
    return LoginResponse(
        message="Login successful",
        user=UserSchema.from_orm(user)
    )

@router.post("/logout", response_model=LogoutResponse)
def logout(response: Response, session_id: Optional[str] = Cookie(None), db: Session = Depends(get_db)):
    """Déconnexion utilisateur"""
    
    if session_id:
        invalidate_session(session_id, db)
    
    # Supprimer le cookie
    response.delete_cookie(key="session_id")
    
    return LogoutResponse(message="Logout successful")

@router.get("/me", response_model=UserSchema)
def get_current_user_info(session_id: Optional[str] = Cookie(None), db: Session = Depends(get_db)):
    """Récupérer les informations de l'utilisateur connecté"""
    
    user = get_current_user(session_id, db)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    return UserSchema.from_orm(user)