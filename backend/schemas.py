from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr

# Base schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    display_name: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class UserProfile(User):
    post_count: int = 0
    follower_count: int = 0

# Post schemas
class PostBase(BaseModel):
    content: str
    image_url: Optional[str] = None

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    content: Optional[str] = None
    image_url: Optional[str] = None

class Post(PostBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    author: User
    like_count: int = 0
    comment_count: int = 0
    is_liked: bool = False  # Si l'utilisateur actuel a liké
    
    class Config:
        from_attributes = True

# Comment schemas
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    post_id: int

class CommentUpdate(BaseModel):
    content: Optional[str] = None

class Comment(CommentBase):
    id: int
    post_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    author: User
    like_count: int = 0
    is_liked: bool = False  # Si l'utilisateur actuel a liké
    
    class Config:
        from_attributes = True

# Response schemas
class PostResponse(Post):
    comments: List[Comment] = []

class UserProfileResponse(UserProfile):
    posts: List[Post] = []

# Authentication schemas
class LoginResponse(BaseModel):
    message: str
    user: User

class LogoutResponse(BaseModel):
    message: str

# Like schemas
class LikeResponse(BaseModel):
    message: str
    like_count: int
    is_liked: bool

# Generic response
class MessageResponse(BaseModel):
    message: str