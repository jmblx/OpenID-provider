import {loadUserAvatar} from "./commonApi";

async function renderAdminPanel() {
    const page = window.location.pathname.split("/").pop().split(".")[0]; // "clients", "profile" и т.п.

    const panel = document.createElement("div");
    panel.className = "admin-panel";

    const navLeft = document.createElement("div");

    const links = [
        { href: "/pages/resourceServers.html", label: "Resource Servers", key: "resourceServers" },
        { href: "/pages/clients.html", label: "Clients", key: "clients" },
    ];

    for (const { href, label, key } of links) {
        const link = document.createElement("a");
        link.href = href;
        link.textContent = label;
        if (key === page) {
            link.style.backgroundColor = "#495057";
        }
        navLeft.appendChild(link);
    }

    const navRight = document.createElement("div");
    navRight.style.display = "flex";
    navRight.style.alignItems = "center";
    navRight.style.gap = "10px";

    const profileLink = document.createElement("a");
    profileLink.href = "/pages/profile.html";

    const avatarImg = document.createElement("img");
    avatarImg.id = "user-avatar";
    avatarImg.style.width = "32px";
    avatarImg.style.height = "32px";
    avatarImg.style.borderRadius = "50%";
    avatarImg.alt = "Profile";
    profileLink.appendChild(avatarImg);

    const logoutBtn = document.createElement("button");
    logoutBtn.id = "logout-button";
    logoutBtn.className = "logout-button";
    logoutBtn.title = "Logout";
    logoutBtn.innerHTML = `<img src="/icons/logout.svg" alt="Logout">`;

    logoutBtn.onclick = () => {
        // Можно адаптировать
        localStorage.clear();
        window.location.href = "/login.html";
    };

    navRight.appendChild(profileLink);
    navRight.appendChild(logoutBtn);

    panel.appendChild(navLeft);
    panel.appendChild(navRight);

    document.body.prepend(panel);

    await loadUserAvatar("user-avatar");
}

document.addEventListener('DOMContentLoaded', async () => {
    renderAdminPanel()
});