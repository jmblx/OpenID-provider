import { CardRenderer } from './cardsCommon.js';

export class ClientsRenderer extends CardRenderer {
    constructor() {
        super(
            'clients-container',
            (client) => `
                <div class="card-title">${client.name}</div>
                <div class="card-meta">ID: ${client.client_id}</div>
            `,
            '/api/client/ids_data'
        );
    }

    handleCardClick(id) {
        window.location.href = `/pages/client.html?clientId=${id}`;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const renderer = new ClientsRenderer();
    renderer.init();
});