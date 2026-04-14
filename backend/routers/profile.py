from fastapi import APIRouter, Depends
from models import ProfileUpdate
from auth_utils import get_current_user
from database import get_db

router = APIRouter(prefix="/api/profile", tags=["個人資料"])


@router.get("")
def get_profile():
    """取得個人資料（公開）"""
    conn = get_db()
    try:
        row = conn.execute("SELECT * FROM profile ORDER BY id DESC LIMIT 1").fetchone()
        if not row:
            return {"success": True, "data": None, "message": "尚無個人資料"}
        return {"success": True, "data": dict(row), "message": "取得個人資料成功"}
    finally:
        conn.close()


@router.put("")
def update_profile(profile: ProfileUpdate, username: str = Depends(get_current_user)):
    """更新個人資料（需認證）"""
    conn = get_db()
    try:
        existing = conn.execute("SELECT * FROM profile ORDER BY id DESC LIMIT 1").fetchone()

        if existing:
            conn.execute(
                "UPDATE profile SET name=?, title=?, bio=?, avatar_url=?, email=?, github=?, linkedin=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
                (profile.name, profile.title, profile.bio, profile.avatar_url, profile.email, profile.github, profile.linkedin, existing["id"]),
            )
        else:
            conn.execute(
                "INSERT INTO profile (name, title, bio, avatar_url, email, github, linkedin) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (profile.name, profile.title, profile.bio, profile.avatar_url, profile.email, profile.github, profile.linkedin),
            )

        conn.commit()
        row = conn.execute("SELECT * FROM profile ORDER BY id DESC LIMIT 1").fetchone()
        return {"success": True, "data": dict(row), "message": "個人資料更新成功"}
    finally:
        conn.close()
