import { CardRenderer } from './cardsCommon.js';

export class ResourceServersRenderer extends CardRenderer {
    constructor() {
        super(
            'rs-container',
            (server) => `<div class="card-title">${server.name}</div>`,
            '/api/rs/ids_data'
        );
    }

    handleCardClick(id) {
        window.location.href = `/pages/resourceServer.html?rsId=${id}`;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const renderer = new ResourceServersRenderer();
    renderer.init();
});