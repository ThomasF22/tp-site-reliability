from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Optional, List
from database import get_db
from models import User, Post, Comment, PostLike
from schemas import (
    UserUpdate, User as UserSchema, UserProfile, UserProfileResponse,
    Post as PostSchema
)
from auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

def get_current_user_optional(session_id: Optional[str] = Cookie(None), db: Session = Depends(get_db)):
    """Récupère l'utilisateur actuel (optionnel)"""
    if session_id:
        return get_current_user(session_id, db)
    return None

def get_current_user_required(session_id: Optional[str] = Cookie(None), db: Session = Depends(get_db)):
    """Récupère l'utilisateur actuel (obligatoire)"""
    user = get_current_user(session_id, db)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user

@router.get("/", response_model=List[UserProfile])
def get_users(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Récupérer la liste des utilisateurs"""
    
    users = db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()
    
    # Enrichir avec les compteurs
    result = []
    for user in users:
        post_count = db.query(func.count(Post.id)).filter(Post.user_id == user.id).scalar() or 0
        
        user_profile = UserProfile.from_orm(user)
        user_profile.post_count = post_count
        user_profile.follower_count = 0  # Pour l'instant, pas de système de follow
        
        result.append(user_profile)
    
    return result

@router.get("/{username}", response_model=UserProfileResponse)
def get_user_profile(
    username: str,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Récupérer le profil d'un utilisateur avec ses posts"""
    
    user = db.query(User).filter(
        User.username == username,
        User.is_active == True
    ).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Récupérer les posts de l'utilisateur
    posts = db.query(Post).filter(Post.user_id == user.id).order_by(desc(Post.created_at)).all()
    
    # Enrichir les posts
    enriched_posts = []
    for post in posts:
        like_count = db.query(func.count(PostLike.id)).filter(PostLike.post_id == post.id).scalar() or 0
        comment_count = db.query(func.count(Comment.id)).filter(Comment.post_id == post.id).scalar() or 0
        
        is_liked = False
        if current_user:
            is_liked = db.query(PostLike).filter(
                PostLike.post_id == post.id,
                PostLike.user_id == current_user.id
            ).first() is not None
        
        post_data = PostSchema.from_orm(post)
        post_data.like_count = like_count
        post_data.comment_count = comment_count
        post_data.is_liked = is_liked
        
        enriched_posts.append(post_data)
    
    # Créer le profil utilisateur
    user_profile = UserProfileResponse.from_orm(user)
    user_profile.post_count = len(enriched_posts)
    user_profile.follower_count = 0
    user_profile.posts = enriched_posts
    
    return user_profile

@router.put("/me", response_model=UserSchema)
def update_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user_required),
    db: Session = Depends(get_db)
):
    """Mettre à jour son profil utilisateur"""
    
    # Mettre à jour les champs fournis
    update_data = user_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    return UserSchema.from_orm(current_user)

@router.get("/me/posts", response_model=List[PostSchema])
def get_my_posts(
    current_user: User = Depends(get_current_user_required),
    db: Session = Depends(get_db)
):
    """Récupérer ses propres posts"""
    
    posts = db.query(Post).filter(
        Post.user_id == current_user.id
    ).order_by(desc(Post.created_at)).all()
    
    # Enrichir les posts
    result = []
    for post in posts:
        like_count = db.query(func.count(PostLike.id)).filter(PostLike.post_id == post.id).scalar() or 0
        comment_count = db.query(func.count(Comment.id)).filter(Comment.post_id == post.id).scalar() or 0
        
        # L'utilisateur peut voir s'il a liké ses propres posts
        is_liked = db.query(PostLike).filter(
            PostLike.post_id == post.id,
            PostLike.user_id == current_user.id
        ).first() is not None
        
        post_data = PostSchema.from_orm(post)
        post_data.like_count = like_count
        post_data.comment_count = comment_count
        post_data.is_liked = is_liked
        
        result.append(post_data)
    
    return result