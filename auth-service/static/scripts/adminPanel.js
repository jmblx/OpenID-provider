import {fetchWithAuth, loadUserAvatar, loadUserData, logoutClient} from "./commonApi.js";

document.addEventListener('DOMContentLoaded', async () => {
    const userData = await loadUserData();
    if (userData.is_admin) {
        await renderAdminPanel();
        await loadUserAvatar('admin-panel-user-avatar');
    }
});

async function renderAdminPanel() {
    const response = await fetchWithAuth('/api/me');
    const userData = await response.json();
    const path = window.location.pathname;
    const filename = path.substring(path.lastIndexOf('/') + 1);
    const pageName = filename.split('.')[0];

    // Список вкладок: name совпадает с pageName
    const tabs = [
        { name: 'resourceServers', label: 'Resource Servers', href: '/pages/resourceServers.html' },
        { name: 'clients',         label: 'Clients',          href: '/pages/clients.html'         },
    ];

    const panel = document.createElement('div');
    panel.className = 'admin-panel';

    // Левая часть: ссылки-вкладки
    const leftDiv = document.createElement('div');
    tabs.forEach(tab => {
        const a = document.createElement('a');
        a.href = tab.href;
        a.textContent = tab.label;
        if (tab.name === pageName) {
            a.classList.add('active-tab');
        }
        leftDiv.appendChild(a);
    });
    panel.appendChild(leftDiv);

    // Правая часть: ссылка на профиль (аватар) и кнопка logout
    const rightDiv = document.createElement('div');
    rightDiv.style.display = 'flex';
    rightDiv.style.alignItems = 'center';
    rightDiv.style.gap = '10px';

    const profileLink = document.createElement('a');
    profileLink.href = '/pages/profile.html';

    const avatarImg = document.createElement('img');
    avatarImg.id = 'admin-panel-user-avatar';
    avatarImg.alt = 'User Avatar';
    avatarImg.style.width = '32px';
    avatarImg.style.height = '32px';
    avatarImg.style.borderRadius = '50%';
    avatarImg.src = '/icons/defaultAvatar.svg'; // временно — пока loadUserAvatar не загрузит

    profileLink.appendChild(avatarImg);
    rightDiv.appendChild(profileLink);

    const logoutBtn = document.createElement('button');
    logoutBtn.id = 'logout-button';
    logoutBtn.className = 'logout-button';
    logoutBtn.title = 'Logout';
    logoutBtn.onclick = () => {
        logoutClient();
    };

    const logoutImg = document.createElement('img');
    logoutImg.src = '/icons/logout.svg';
    logoutImg.alt = 'Logout';
    logoutBtn.appendChild(logoutImg);

    rightDiv.appendChild(logoutBtn);

    panel.appendChild(rightDiv);

    document.body.prepend(panel);
}