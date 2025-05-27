import { fetchData } from './dataService.js';

export class CardRenderer {
    constructor(containerId, cardTemplate, apiEndpoint, options = {}) {
        this.container = document.getElementById(containerId);
        this.cardTemplate = cardTemplate;
        this.apiEndpoint = apiEndpoint;
        this.cardClass = options.cardClass || 'card-item';
        this.emptyMessage = options.emptyMessage || 'Нет данных для отображения';
        this.errorMessage = options.errorMessage || 'Не удалось загрузить данные';
        this.currentPage = 1;
        this.itemsPerPage = options.itemsPerPage || 12;
    }

    async init() {
        try {
            const data = await this.fetchItems();
            this.renderCards(data);
        } catch (error) {
            console.error('Error initializing cards:', error);
            this.showError(this.errorMessage);
        }
    }

    async fetchItems() {
        return await fetchData(this.apiEndpoint);
    }

    renderCards(items) {
        this.container.innerHTML = '';

        if (!items || Object.keys(items).length === 0) {
            this.showEmptyState();
            return;
        }

        Object.entries(items).forEach(([id, itemData]) => {
            const card = this.createCard(id, itemData);
            this.container.appendChild(card);
        });
    }

    createCard(id, itemData) {
        const card = document.createElement('div');
        card.className = this.cardClass;
        card.innerHTML = this.cardTemplate(itemData);
        card.onclick = () => this.handleCardClick(id, itemData);
        return card;
    }

    handleCardClick(id, itemData) {
        console.log('Card clicked:', id, itemData);
    }

    showEmptyState() {
        this.container.innerHTML = `
            <div class="col-12 text-center py-5 text-muted">
                ${this.emptyMessage}
            </div>`;
    }

    showError(message) {
        this.container.innerHTML = `
            <div class="col-12 text-center py-5 text-danger">
                ${message}
            </div>`;
    }
}