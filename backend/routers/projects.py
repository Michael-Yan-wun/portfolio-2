from fastapi import APIRouter, Depends, HTTPException, status
from models import ProjectCreate
from auth_utils import get_current_user
from database import get_db

router = APIRouter(prefix="/api/projects", tags=["作品集"])


@router.get("")
def get_projects():
    """取得所有作品（公開）"""
    conn = get_db()
    try:
        rows = conn.execute("SELECT * FROM projects ORDER BY created_at DESC").fetchall()
        projects = [dict(row) for row in rows]
        return {"success": True, "data": projects, "message": "取得作品列表成功"}
    finally:
        conn.close()


@router.get("/{project_id}")
def get_project(project_id: int):
    """取得單筆作品（公開）"""
    conn = get_db()
    try:
        row = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="作品不存在")
        return {"success": True, "data": dict(row), "message": "取得作品成功"}
    finally:
        conn.close()


@router.post("")
def create_project(project: ProjectCreate, username: str = Depends(get_current_user)):
    """新增作品（需認證）"""
    conn = get_db()
    try:
        cursor = conn.execute(
            "INSERT INTO projects (title, description, tech_stack, image_url, demo_url, github_url) VALUES (?, ?, ?, ?, ?, ?)",
            (project.title, project.description, project.tech_stack, project.image_url, project.demo_url, project.github_url),
        )
        conn.commit()
        new_id = cursor.lastrowid
        row = conn.execute("SELECT * FROM projects WHERE id = ?", (new_id,)).fetchone()
        return {"success": True, "data": dict(row), "message": "作品新增成功"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        conn.close()


@router.put("/{project_id}")
def update_project(project_id: int, project: ProjectCreate, username: str = Depends(get_current_user)):
    """更新作品（需認證）"""
    conn = get_db()
    try:
        existing = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="作品不存在")

        conn.execute(
            "UPDATE projects SET title=?, description=?, tech_stack=?, image_url=?, demo_url=?, github_url=? WHERE id=?",
            (project.title, project.description, project.tech_stack, project.image_url, project.demo_url, project.github_url, project_id),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
        return {"success": True, "data": dict(row), "message": "作品更新成功"}
    finally:
        conn.close()


@router.delete("/{project_id}")
def delete_project(project_id: int, username: str = Depends(get_current_user)):
    """刪除作品（需認證）"""
    conn = get_db()
    try:
        existing = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="作品不存在")

        conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
        return {"success": True, "data": None, "message": "作品刪除成功"}
    finally:
        conn.close()
