from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from database import get_db
from models import User, Comment, CommentLike, Post
from schemas import (
    CommentCreate, CommentUpdate, Comment as CommentSchema,
    LikeResponse
)
from auth import get_current_user

router = APIRouter(prefix="/comments", tags=["comments"])

def get_current_user_required(session_id: Optional[str] = Cookie(None), db: Session = Depends(get_db)):
    """Récupère l'utilisateur actuel (obligatoire)"""
    user = get_current_user(session_id, db)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user

@router.post("/", response_model=CommentSchema)
def create_comment(
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user_required),
    db: Session = Depends(get_db)
):
    """Créer un nouveau commentaire"""
    
    # Vérifier que le post existe
    post = db.query(Post).filter(Post.id == comment_data.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db_comment = Comment(
        post_id=comment_data.post_id,
        user_id=current_user.id,
        content=comment_data.content
    )
    
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    
    # Charger le commentaire avec l'auteur
    comment_with_author = db.query(Comment).filter(Comment.id == db_comment.id).first()
    
    result = CommentSchema.from_orm(comment_with_author)
    result.like_count = 0
    result.is_liked = False
    
    return result

@router.get("/post/{post_id}", response_model=List[CommentSchema])
def get_post_comments(
    post_id: int,
    current_user: Optional[User] = Depends(lambda session_id: get_current_user(session_id, next(get_db())) if session_id else None),
    db: Session = Depends(get_db)
):
    """Récupérer tous les commentaires d'un post"""
    
    # Vérifier que le post existe
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    comments = db.query(Comment).join(User).filter(
        Comment.post_id == post_id,
        User.is_active == True
    ).order_by(Comment.created_at).all()
    
    # Enrichir les commentaires avec les likes
    result = []
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
        
        comment_data = CommentSchema.from_orm(comment)
        comment_data.like_count = like_count
        comment_data.is_liked = is_liked
        result.append(comment_data)
    
    return result

@router.put("/{comment_id}", response_model=CommentSchema)
def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    current_user: User = Depends(get_current_user_required),
    db: Session = Depends(get_db)
):
    """Modifier un commentaire (seulement par son auteur)"""
    
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this comment")
    
    # Mettre à jour les champs fournis
    update_data = comment_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(comment, field, value)
    
    db.commit()
    db.refresh(comment)
    
    result = CommentSchema.from_orm(comment)
    result.like_count = db.query(CommentLike).filter(CommentLike.comment_id == comment_id).count()
    result.is_liked = False
    
    return result

@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user_required),
    db: Session = Depends(get_db)
):
    """Supprimer un commentaire (seulement par son auteur)"""
    
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    
    db.delete(comment)
    db.commit()
    
    return {"message": "Comment deleted successfully"}

@router.post("/{comment_id}/like", response_model=LikeResponse)
def toggle_comment_like(
    comment_id: int,
    current_user: User = Depends(get_current_user_required),
    db: Session = Depends(get_db)
):
    """Liker/unliker un commentaire"""
    
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Vérifier si le like existe déjà
    existing_like = db.query(CommentLike).filter(
        CommentLike.comment_id == comment_id,
        CommentLike.user_id == current_user.id
    ).first()
    
    if existing_like:
        # Unliker
        db.delete(existing_like)
        db.commit()
        is_liked = False
        message = "Comment unliked"
    else:
        # Liker
        new_like = CommentLike(comment_id=comment_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()
        is_liked = True
        message = "Comment liked"
    
    # Compter les likes totaux
    like_count = db.query(CommentLike).filter(CommentLike.comment_id == comment_id).count()
    
    return LikeResponse(
        message=message,
        like_count=like_count,
        is_liked=is_liked
    )