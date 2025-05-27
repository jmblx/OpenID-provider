import { fetchData } from '../api/dataService.js';

export class CardRenderer {
    constructor(containerId, cardTemplate, apiEndpoint) {
        this.container = document.getElementById(containerId);
        this.cardTemplate = cardTemplate;
        this.apiEndpoint = apiEndpoint;
        this.currentPage = 1;
        this.itemsPerPage = 12;
    }

    async init() {
        try {
            const data = await this.fetchItems();
            this.renderCards(data);
            // this.setupPagination(data.length); // Задел для пагинации
        } catch (error) {
            console.error('Error initializing cards:', error);
            this.showError('Не удалось загрузить данные');
        }
    }

    async fetchItems() {
        // TODO: Добавить параметры пагинации, когда API будет поддерживать
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
        card.className = 'card-item';
        card.innerHTML = this.cardTemplate(itemData);
        card.onclick = () => this.handleCardClick(id, itemData);
        return card;
    }

    handleCardClick(id, itemData) {
        // Базовый обработчик, можно переопределить
        console.log('Card clicked:', id, itemData);
    }

    showEmptyState() {
        this.container.innerHTML = '<div class="col-12 text-center py-5 text-muted">Нет данных для отображения</div>';
    }

    showError(message) {
        this.container.innerHTML = `<div class="col-12 text-center py-5 text-danger">${message}</div>`;
    }

    /* Задел для пагинации
    setupPagination(totalItems) {
        const totalPages = Math.ceil(totalItems / this.itemsPerPage);
        if (totalPages <= 1) return;

        // TODO: Реализовать создание элементов пагинации
    }
    */
}