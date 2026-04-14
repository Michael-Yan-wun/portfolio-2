from fastapi import APIRouter, Depends, HTTPException, status
from models import LoginRequest, TokenResponse
from auth_utils import hash_password, verify_password, create_token, get_current_user
from database import get_db

router = APIRouter(prefix="/api/auth", tags=["認證"])


@router.post("/login", response_model=dict)
def login(request: LoginRequest):
    """登入並取得 JWT token"""
    conn = get_db()
    try:
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (request.username,)
        ).fetchone()

        if not user or not verify_password(request.password, user["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="帳號或密碼錯誤",
            )

        token = create_token(user["username"])
        return {
            "success": True,
            "data": {"access_token": token, "token_type": "bearer"},
            "message": "登入成功",
        }
    finally:
        conn.close()


@router.post("/init", response_model=dict)
def init_admin():
    """建立預設管理員帳號（admin / admin123）"""
    conn = get_db()
    try:
        existing = conn.execute(
            "SELECT * FROM users WHERE username = ?", ("admin",)
        ).fetchone()

        if existing:
            return {
                "success": True,
                "data": None,
                "message": "管理員帳號已存在",
            }

        password_hash = hash_password("admin123")
        conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            ("admin", password_hash),
        )
        conn.commit()
        return {
            "success": True,
            "data": None,
            "message": "預設管理員帳號建立成功",
        }
    finally:
        conn.close()


@router.get("/me", response_model=dict)
def get_me(username: str = Depends(get_current_user)):
    """取得當前登入的使用者資訊"""
    conn = get_db()
    try:
        user = conn.execute(
            "SELECT id, username, created_at FROM users WHERE username = ?",
            (username,),
        ).fetchone()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="使用者不存在",
            )

        return {
            "success": True,
            "data": {
                "id": user["id"],
                "username": user["username"],
                "created_at": user["created_at"],
            },
            "message": "取得使用者資訊成功",
        }
    finally:
        conn.close()
