import { fetchWithAuth, loadUserAvatar, logoutClient } from './commonApi.js';

document.addEventListener('DOMContentLoaded', async () => {
    await renderUserPanel();
    await loadUserAvatar('user-panel-avatar');
});

async function renderUserPanel() {
    const meResp = await fetchWithAuth('/api/me');
    const me = await meResp.json();

    const availResp = await fetchWithAuth('/api/available-accounts');
    const { accounts, active_account_id } = await availResp.json();

    const panel = document.createElement('div');
    panel.className = 'admin-panel';

    if (me.is_admin) {
        const path = window.location.pathname;
        const pageName = path.substring(path.lastIndexOf('/') + 1).split('.')[0];
        const tabs = [
            { name: 'resourceServers', label: 'Resource Servers', href: '/pages/resourceServers.html' },
            { name: 'clients',         label: 'Clients',          href: '/pages/clients.html'         },
        ];
        const left = document.createElement('div');
        tabs.forEach(tab => {
            const a = document.createElement('a');
            a.href = tab.href;
            a.textContent = tab.label;
            if (tab.name === pageName) a.classList.add('active-tab');
            left.appendChild(a);
        });
        panel.appendChild(left);
    } else {
        panel.appendChild(document.createElement('div')); // чтобы правый блок был справа
    }

    const right = document.createElement('div');
    right.style.display = 'flex';
    right.style.alignItems = 'center';
    right.style.gap = '10px';

    const switcher = document.createElement('div');
    switcher.className = 'account-switcher';
    switcher.style.position = 'relative';

    const active = document.createElement('img');
    active.id = 'user-panel-avatar';
    active.src = accounts[active_account_id]?.avatar_url || '/icons/defaultAvatar.svg';
    active.alt = 'Avatar';
    active.style.width = '32px';
    active.style.height = '32px';
    active.style.borderRadius = '50%';
    active.style.cursor = 'pointer';

    switcher.appendChild(active);

    const menu = document.createElement('div');
    menu.className = 'account-menu';
    menu.style.position = 'absolute';
    menu.style.top = '100%';
    menu.style.right = '0';
    menu.style.background = '#fff';
    menu.style.boxShadow = '0 2px 8px rgba(0,0,0,0.2)';
    menu.style.borderRadius = '4px';
    menu.style.overflow = 'hidden';
    menu.style.display = 'none';
    menu.style.zIndex = '1001';

    Object.entries(accounts).forEach(([id, info]) => {
        const item = document.createElement('div');
        item.className = 'account-item d-flex align-items-center p-2';
        item.style.cursor = 'pointer';
        if (id === active_account_id) item.style.background = '#e9ecef';
        item.innerHTML = `
            <img src="${info.avatar_url}" width="24" height="24" class="rounded-circle me-2">
            <span>${info.email}</span>
        `;
        item.addEventListener('click', () => switchAccount(id));
        menu.appendChild(item);
    });
    const addBtn = document.createElement('div');
    addBtn.className = 'account-item d-flex align-items-center p-2';
    addBtn.style.cursor = 'pointer';
    addBtn.style.borderTop = '1px solid #e0e0e0';
    addBtn.innerHTML = `
        <span style="font-size: 20px; margin-right: 8px;">＋</span>
        <span>Добавить аккаунт</span>
    `;
    addBtn.addEventListener('click', async () => {
        try {
            const resp = await fetchWithAuth('/api/deactivate-current-account', {
                method: 'POST'
            });
            if (!resp.ok) throw new Error(`status ${resp.status}`);
            window.location.href = '/pages/login.html';
        } catch (e) {
            console.error('Не удалось деактивировать текущий аккаунт:', e);
            alert('Ошибка выхода для добавления аккаунта');
        }
    });
    menu.appendChild(addBtn);
    menu.appendChild(addBtn);

    switcher.appendChild(menu);
    right.appendChild(switcher);

    const logoutBtn = document.createElement('button');
    logoutBtn.id = 'logout-button';
    logoutBtn.className = 'logout-button';
    logoutBtn.title = 'Logout';
    logoutBtn.onclick = () => logoutClient();
    logoutBtn.innerHTML = `<img src="/icons/logout.svg" alt="Logout">`;
    right.appendChild(logoutBtn);

    panel.appendChild(right);
    document.body.prepend(panel);

    active.addEventListener('click', e => {
        menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
    });
    document.addEventListener('click', e => {
        if (!switcher.contains(e.target)) menu.style.display = 'none';
    });
}

async function switchAccount(newId) {
    try {
        const resp = await fetchWithAuth('/api/switch-account', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ new_active_user_id: newId })
        });
        if (!resp.ok) throw new Error(`status ${resp.status}`);
        // просто перезагружаем страницу, теперь запросы пойдут от лица нового аккаунта
        window.location.reload();
    } catch (e) {
        console.error('Switch account error:', e);
        alert('Не удалось сменить аккаунт');
    }
}
