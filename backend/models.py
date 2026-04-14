from pydantic import BaseModel
from typing import Optional


# === 認證相關 ===
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# === 使用者 ===
class UserResponse(BaseModel):
    id: int
    username: str
    created_at: str


# === 作品集 ===
class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    tech_stack: Optional[str] = ""
    image_url: Optional[str] = ""
    demo_url: Optional[str] = ""
    github_url: Optional[str] = ""


class ProjectResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    tech_stack: Optional[str]
    image_url: Optional[str]
    demo_url: Optional[str]
    github_url: Optional[str]
    created_at: str


# === 訪客留言 ===
class MessageCreate(BaseModel):
    name: str
    email: str
    content: str


class MessageUpdate(BaseModel):
    is_read: Optional[int] = None


class MessageResponse(BaseModel):
    id: int
    name: str
    email: str
    content: str
    is_read: int
    created_at: str


# === 個人資料 ===
class ProfileUpdate(BaseModel):
    name: Optional[str] = ""
    title: Optional[str] = ""
    bio: Optional[str] = ""
    avatar_url: Optional[str] = ""
    email: Optional[str] = ""
    github: Optional[str] = ""
    linkedin: Optional[str] = ""


class ProfileResponse(BaseModel):
    id: int
    name: Optional[str]
    title: Optional[str]
    bio: Optional[str]
    avatar_url: Optional[str]
    email: Optional[str]
    github: Optional[str]
    linkedin: Optional[str]
    updated_at: str
