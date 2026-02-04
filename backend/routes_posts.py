from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import Optional, List
from database import get_db
from models import User, Post, PostLike, Comment
from schemas import (
    PostCreate, PostUpdate, PostResponse, Post as PostSchema,
    LikeResponse
)
from auth import get_current_user

router = APIRouter(prefix="/posts", tags=["posts"])

def get_current_user_optional(session_id: Optional[str] = Cookie(None), db: Session = Depends(get_db)):
    """Récupère l'utilisateur actuel (optionnel pour les vues publiques)"""
    if session_id:
        return get_current_user(session_id, db)
    return None

def get_current_user_required(session_id: Optional[str] = Cookie(None), db: Session = Depends(get_db)):
    """Récupère l'utilisateur actuel (obligatoire)"""
    user = get_current_user(session_id, db)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user

@router.get("/", response_model=List[PostSchema])
def get_posts(
    skip: int = 0, 
    limit: int = 20,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Récupérer la liste des posts (timeline publique)"""
    
    # Requête de base pour les posts avec leurs auteurs
    query = db.query(Post).join(User).filter(User.is_active == True)
    
    # Récupérer les posts triés par date
    posts = query.order_by(desc(Post.created_at)).offset(skip).limit(limit).all()
    
    # Enrichir avec les données de comptage et likes
    result = []
    for post in posts:
        # Compter les likes et commentaires
        like_count = db.query(PostLike).filter(PostLike.post_id == post.id).count()
        comment_count = db.query(Comment).filter(Comment.post_id == post.id).count()
        
        # Vérifier si l'utilisateur actuel a liké
        is_liked = False
        if current_user:
            is_liked = db.query(PostLike).filter(
                PostLike.post_id == post.id,
                PostLike.user_id == current_user.id
            ).first() is not None
        
        # Créer l'objet post enrichi
        post_data = PostSchema.from_orm(post)
        post_data.like_count = like_count
        post_data.comment_count = comment_count
        post_data.is_liked = is_liked
        
        result.append(post_data)
    
    return result

@router.get("/{post_id}", response_model=PostResponse)
def get_post(
    post_id: int,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Récupérer un post spécifique avec ses commentaires"""
    
    post = db.query(Post).join(User).filter(
        Post.id == post_id,
        User.is_active == True
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Récupérer les commentaires
    comments = db.query(Comment).join(User).filter(
        Comment.post_id == post_id,
        User.is_active == True
    ).order_by(Comment.created_at).all()
    
    # Enrichir les commentaires
    enriched_comments = []
    for comment in comments:
        like_count = db.query(func.count(CommentLike.id)).filter(
            CommentLike.comment_id == comment.id
        ).scalar() or 0
        
        is_liked = False
        if current_user:
            is_liked = db.query(CommentLike).filter(
                CommentLike.comment_id == comment.id,
                CommentLike.user_id == current_user.id
            ).first() is not None
        
        comment_data = Comment.from_orm(comment)
        comment_data.like_count = like_count
        comment_data.is_liked = is_liked
        enriched_comments.append(comment_data)
    
    # Enrichir le post
    like_count = db.query(func.count(PostLike.id)).filter(PostLike.post_id == post_id).scalar() or 0
    is_liked = False
    if current_user:
        is_liked = db.query(PostLike).filter(
            PostLike.post_id == post_id,
            PostLike.user_id == current_user.id
        ).first() is not None
    
    post_data = PostResponse.from_orm(post)
    post_data.like_count = like_count
    post_data.comment_count = len(enriched_comments)
    post_data.is_liked = is_liked
    post_data.comments = enriched_comments
    
    return post_data

@router.post("/", response_model=PostSchema)
def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user_required),
    db: Session = Depends(get_db)
):
    """Créer un nouveau post"""
    
    db_post = Post(
        user_id=current_user.id,
        content=post_data.content,
        image_url=post_data.image_url
    )
    
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    # Charger le post avec l'auteur
    post_with_author = db.query(Post).filter(Post.id == db_post.id).first()
    
    result = PostSchema.from_orm(post_with_author)
    result.like_count = 0
    result.comment_count = 0
    result.is_liked = False
    
    return result

@router.put("/{post_id}", response_model=PostSchema)
def update_post(
    post_id: int,
    post_data: PostUpdate,
    current_user: User = Depends(get_current_user_required),
    db: Session = Depends(get_db)
):
    """Modifier un post (seulement par son auteur)"""
    
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this post")
    
    # Mettre à jour les champs fournis
    update_data = post_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(post, field, value)
    
    db.commit()
    db.refresh(post)
    
    result = PostSchema.from_orm(post)
    result.like_count = db.query(PostLike).filter(PostLike.post_id == post_id).count()
    result.comment_count = db.query(Comment).filter(Comment.post_id == post_id).count()
    result.is_liked = False  # L'auteur n'a pas forcément liké son propre post
    
    return result

@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user_required),
    db: Session = Depends(get_db)
):
    """Supprimer un post (seulement par son auteur)"""
    
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
    db.delete(post)
    db.commit()
    
    return {"message": "Post deleted successfully"}

@router.post("/{post_id}/like", response_model=LikeResponse)
def toggle_post_like(
    post_id: int,
    current_user: User = Depends(get_current_user_required),
    db: Session = Depends(get_db)
):
    """Liker/unliker un post"""
    
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Vérifier si le like existe déjà
    existing_like = db.query(PostLike).filter(
        PostLike.post_id == post_id,
        PostLike.user_id == current_user.id
    ).first()
    
    if existing_like:
        # Unliker
        db.delete(existing_like)
        db.commit()
        is_liked = False
        message = "Post unliked"
    else:
        # Liker
        new_like = PostLike(post_id=post_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()
        is_liked = True
        message = "Post liked"
    
    # Compter les likes totaux
    like_count = db.query(PostLike).filter(PostLike.post_id == post_id).count()
    
    return LikeResponse(
        message=message,
        like_count=like_count,
        is_liked=is_liked
    )