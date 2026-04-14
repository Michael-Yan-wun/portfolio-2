from fastapi import APIRouter, Depends, HTTPException, status
from models import MessageCreate, MessageUpdate
from auth_utils import get_current_user
from database import get_db

router = APIRouter(prefix="/api/messages", tags=["留言"])


@router.get("/stats")
def get_message_stats(username: str = Depends(get_current_user)):
    """留言統計：總數 + 未讀數（需認證）"""
    conn = get_db()
    try:
        total = conn.execute("SELECT COUNT(*) as count FROM messages").fetchone()["count"]
        unread = conn.execute("SELECT COUNT(*) as count FROM messages WHERE is_read = 0").fetchone()["count"]
        return {
            "success": True,
            "data": {"total": total, "unread": unread},
            "message": "取得留言統計成功",
        }
    finally:
        conn.close()


@router.get("")
def get_messages(username: str = Depends(get_current_user)):
    """取得所有留言（需認證）"""
    conn = get_db()
    try:
        rows = conn.execute("SELECT * FROM messages ORDER BY created_at DESC").fetchall()
        messages = [dict(row) for row in rows]
        return {"success": True, "data": messages, "message": "取得留言列表成功"}
    finally:
        conn.close()


@router.get("/{message_id}")
def get_message(message_id: int, username: str = Depends(get_current_user)):
    """取得單筆留言（需認證）"""
    conn = get_db()
    try:
        row = conn.execute("SELECT * FROM messages WHERE id = ?", (message_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="留言不存在")
        return {"success": True, "data": dict(row), "message": "取得留言成功"}
    finally:
        conn.close()


@router.post("")
def create_message(message: MessageCreate):
    """新增留言（公開，給訪客用）"""
    conn = get_db()
    try:
        cursor = conn.execute(
            "INSERT INTO messages (name, email, content) VALUES (?, ?, ?)",
            (message.name, message.email, message.content),
        )
        conn.commit()
        new_id = cursor.lastrowid
        row = conn.execute("SELECT * FROM messages WHERE id = ?", (new_id,)).fetchone()
        return {"success": True, "data": dict(row), "message": "留言送出成功"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        conn.close()


@router.put("/{message_id}")
def update_message(message_id: int, message: MessageUpdate, username: str = Depends(get_current_user)):
    """更新留言狀態，如標記已讀（需認證）"""
    conn = get_db()
    try:
        existing = conn.execute("SELECT * FROM messages WHERE id = ?", (message_id,)).fetchone()
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="留言不存在")

        if message.is_read is not None:
            conn.execute("UPDATE messages SET is_read = ? WHERE id = ?", (message.is_read, message_id))
            conn.commit()

        row = conn.execute("SELECT * FROM messages WHERE id = ?", (message_id,)).fetchone()
        return {"success": True, "data": dict(row), "message": "留言更新成功"}
    finally:
        conn.close()


@router.delete("/{message_id}")
def delete_message(message_id: int, username: str = Depends(get_current_user)):
    """刪除留言（需認證）"""
    conn = get_db()
    try:
        existing = conn.execute("SELECT * FROM messages WHERE id = ?", (message_id,)).fetchone()
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="留言不存在")

        conn.execute("DELETE FROM messages WHERE id = ?", (message_id,))
        conn.commit()
        return {"success": True, "data": None, "message": "留言刪除成功"}
    finally:
        conn.close()
