import { CardRenderer } from './cardsCommon.js';

export class ResourceServersRenderer extends CardRenderer {
    constructor() {
        super(
            'clients-container',
            (server) => `<div class="card-title">${server.name}</div>`,
            '/api/client/ids_data'
        );
    }

    handleCardClick(id) {
        window.location.href = `/pages/client.html?rsId=${id}`;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const renderer = new ResourceServersRenderer();
    renderer.init();
});