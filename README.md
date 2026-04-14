# Portfolio — 個人作品集網站

深色主題的全端個人作品集網站，具備前台展示與後台管理功能。

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat&logo=tailwind-css&logoColor=white)
![GSAP](https://img.shields.io/badge/GSAP-88CE02?style=flat&logo=greensock&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)

## 功能特色

### 前台（訪客端）
- **首頁** — Hero 動畫、打字機效果、精選作品展示
- **作品集** — 響應式卡片網格，展示專案資訊與技術標籤
- **關於我** — 個人簡介、技能專長、工作經歷時間軸、學歷
- **聯絡我** — 表單提交訊息，搭配即時驗證
- **登入** — 管理員 JWT 登入

### 後台（管理端）
- **儀表板** — 專案數量、訊息統計總覽
- **作品管理** — 新增 / 編輯 / 刪除專案（CRUD）
- **訊息管理** — 檢視 / 標記已讀 / 刪除訪客訊息
- **個人資料** — 編輯姓名、職稱、自我介紹

### 動畫與體驗
- GSAP + ScrollTrigger 進場動畫、視差捲動
- Glassmorphism 卡片風格（`backdrop-blur` + 半透明邊框）
- RWD 響應式設計（手機漢堡選單）
- `prefers-reduced-motion` 無障礙支援

## 技術架構

```
portfolio-2/
├── frontend/           # 前端靜態頁面
│   ├── index.html      # 首頁
│   ├── projects.html   # 作品集
│   ├── about.html      # 關於我
│   ├── contact.html    # 聯絡我
│   ├── login.html      # 登入頁
│   ├── css/            # 效能 CSS
│   └── admin/          # 後台管理頁面
│       ├── dashboard.html
│       ├── projects.html
│       ├── messages.html
│       ├── profile.html
│       └── js/auth.js  # 認證工具
├── backend/            # FastAPI 後端
│   ├── main.py         # 應用程式進入點
│   ├── database.py     # SQLite 資料庫初始化
│   ├── auth_utils.py   # JWT / bcrypt 認證
│   ├── models.py       # Pydantic 資料模型
│   ├── seed.py         # 測試資料填充
│   ├── requirements.txt
│   └── routers/        # API 路由模組
│       ├── auth.py     # 登入 / 初始化帳號
│       ├── projects.py # 專案 CRUD
│       ├── messages.py # 訊息 CRUD
│       └── profile.py  # 個人資料
└── LICENSE
```

## 快速開始

### 1. 後端

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python seed.py           # 填入測試資料
uvicorn main:app --reload --port 8000
```

### 2. 前端

```bash
cd frontend
python3 -m http.server 8080
```

開啟瀏覽器前往 `http://localhost:8080`

### 3. 管理後台

1. 前往 `http://localhost:8080/login.html`
2. 預設帳號：`admin` / 密碼：`admin123`
3. 登入後即可進入後台管理介面

## API 端點

| 方法 | 路徑 | 說明 | 權限 |
|------|------|------|------|
| `POST` | `/api/auth/init` | 初始化管理員帳號 | 公開 |
| `POST` | `/api/auth/login` | 登入取得 JWT | 公開 |
| `GET` | `/api/auth/me` | 取得當前使用者 | 需認證 |
| `GET` | `/api/projects` | 取得所有專案 | 公開 |
| `POST` | `/api/projects` | 新增專案 | 需認證 |
| `PUT` | `/api/projects/{id}` | 更新專案 | 需認證 |
| `DELETE` | `/api/projects/{id}` | 刪除專案 | 需認證 |
| `POST` | `/api/messages` | 訪客送出訊息 | 公開 |
| `GET` | `/api/messages` | 取得所有訊息 | 需認證 |
| `PUT` | `/api/messages/{id}` | 更新訊息狀態 | 需認證 |
| `DELETE` | `/api/messages/{id}` | 刪除訊息 | 需認證 |
| `GET` | `/api/profile` | 取得個人資料 | 公開 |
| `PUT` | `/api/profile` | 更新個人資料 | 需認證 |

## License

本專案採用 [MIT License](LICENSE) 授權。
