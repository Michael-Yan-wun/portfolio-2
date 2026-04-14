"""建立測試資料的腳本"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "portfolio.db")


def seed():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 新增 3 筆範例作品
    projects = [
        ("個人履歷網站", "使用 FastAPI + Tailwind CSS 打造的深色主題個人網站，具備前後台管理功能。", "FastAPI, Tailwind CSS, GSAP, SQLite", "", "https://example.com/demo1", "https://github.com/example/portfolio"),
        ("線上購物平台", "全端電商網站，支援商品瀏覽、購物車、結帳流程和後台訂單管理。", "React, Node.js, MongoDB, Stripe", "", "https://example.com/demo2", "https://github.com/example/shop"),
        ("即時聊天應用", "基於 WebSocket 的即時聊天室，支援多人對話、訊息歷史和表情符號。", "Vue.js, Socket.io, Express, Redis", "", "https://example.com/demo3", "https://github.com/example/chat"),
    ]
    cursor.executemany(
        "INSERT INTO projects (title, description, tech_stack, image_url, demo_url, github_url) VALUES (?, ?, ?, ?, ?, ?)",
        projects,
    )

    # 新增 2 筆範例留言
    messages_data = [
        ("張小明", "ming@example.com", "你好！我很喜歡你的作品集網站，設計得很棒。想請問你有接外包案件嗎？"),
        ("李美麗", "meili@example.com", "嗨，我是一名 HR，我們公司正在找前端工程師，對你的經歷很有興趣，方便聊聊嗎？"),
    ]
    cursor.executemany(
        "INSERT INTO messages (name, email, content) VALUES (?, ?, ?)",
        messages_data,
    )

    # 新增 1 筆個人資料
    cursor.execute(
        "INSERT INTO profile (name, title, bio, avatar_url, email, github, linkedin) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            "王大明",
            "全端開發者 / UI 設計愛好者",
            "我是一名熱愛技術的全端開發者，擅長使用 Python 和 JavaScript 建構現代化的網頁應用程式。喜歡探索新技術，對使用者體驗和介面設計有著高度的熱忱。",
            "",
            "contact@example.com",
            "https://github.com/example",
            "https://linkedin.com/in/example",
        ),
    )

    conn.commit()
    conn.close()
    print("測試資料建立成功！")
    print("- 3 筆作品")
    print("- 2 筆留言")
    print("- 1 筆個人資料")


if __name__ == "__main__":
    seed()
