// panelInit.js

import { fetchWithAuth, loadUserAvatar, logoutClient } from './commonApi.js';
import { initAccountSwitcher } from './accountSwitcher.js';

document.addEventListener('DOMContentLoaded', async () => {
    // 1. Сначала отрисуем панель (включая переключатель аккаунтов)
    await renderUserPanel();

    // 2. Загрузим аватар активного аккаунта (через общий loadUserAvatar)
    await loadUserAvatar('user-panel-avatar');
});

async function renderUserPanel() {
    // Получаем информацию о пользователе (is_admin и т.п.)
    const meResp = await fetchWithAuth('/api/me');
    const me = await meResp.json();

    // Контейнер панели
    const panel = document.createElement('div');
    panel.className = 'admin-panel';

    // Левая часть: вкладки, только если админ
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
        // Пустой див, чтобы правый блок был справа
        panel.appendChild(document.createElement('div'));
    }

    // Правая часть: переключатель аккаунтов + кнопка выхода
    const right = document.createElement('div');
    right.style.display = 'flex';
    right.style.alignItems = 'center';
    right.style.gap = '10px';

    // Переключатель аккаунтов (показывать кнопку "Добавить аккаунт")
    const switcherContainer = document.createElement('div');
    switcherContainer.dataset.context = 'panel';
    await initAccountSwitcher(switcherContainer, {
        allowAdd: true,
        onAdd: () => window.location.href = '/pages/login.html'
    });
    right.appendChild(switcherContainer);

    // Кнопка "Выход"
    const logoutBtn = document.createElement('button');
    logoutBtn.id = 'logout-button';
    logoutBtn.className = 'logout-button';
    logoutBtn.title = 'Logout';
    logoutBtn.onclick = logoutClient;
    logoutBtn.innerHTML = `<img src="/icons/logout.svg" alt="Logout">`;
    right.appendChild(logoutBtn);

    panel.appendChild(right);
    document.body.prepend(panel);
}
