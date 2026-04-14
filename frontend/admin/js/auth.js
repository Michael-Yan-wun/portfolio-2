const API_BASE = 'http://localhost:8000';

/**
 * 檢查登入狀態，未登入跳轉到登入頁
 */
function checkAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '../login.html';
    }
}

/**
 * 登出：清除 token 並跳轉
 */
function logout() {
    localStorage.removeItem('token');
    window.location.href = '../login.html';
}

/**
 * 帶 JWT token 的 fetch 封裝
 */
async function authFetch(url, options = {}) {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '../login.html';
        return;
    }

    const defaultHeaders = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
    };

    options.headers = { ...defaultHeaders, ...options.headers };

    try {
        const response = await fetch(url, options);

        if (response.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '../login.html';
            return;
        }

        return await response.json();
    } catch (error) {
        showToast('伺服器連線失敗', 'error');
        throw error;
    }
}

/**
 * Toast 通知：成功（綠色）/ 失敗（紅色），3 秒後消失
 */
function showToast(message, type = 'success') {
    const existing = document.querySelector('.toast-notification');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = `toast-notification fixed top-6 right-6 z-50 px-6 py-3 rounded-lg text-white font-medium shadow-lg transition-all duration-300 transform translate-x-0`;

    if (type === 'success') {
        toast.classList.add('bg-emerald-500');
    } else {
        toast.classList.add('bg-red-500');
    }

    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100px)';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
