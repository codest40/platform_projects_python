// Paginate.js - Handles pagination for reminders and other lists
export class Paginator {
    constructor() {
        this.itemsPerPage = 10;
        this.currentPage = 1;
        this.totalItems = 0;
        this.items = [];
        this.container = null;
        this.paginationContainer = null;
        this.onPageChange = null;
        this.onRender = null;
    }
    
    init(options = {}) {
        this.itemsPerPage = options.itemsPerPage || 10;
        this.container = document.getElementById(options.containerId);
        this.paginationContainer = document.getElementById(options.paginationId || 'pagination');
        this.onPageChange = options.onPageChange || null;
        this.onRender = options.onRender || null;
        
        if (!this.container) {
            console.warn('Pagination container not found');
            return;
        }
        
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Pagination click events
        if (this.paginationContainer) {
            this.paginationContainer.addEventListener('click', (e) => {
                const pageBtn = e.target.closest('.page-btn');
                if (pageBtn && !pageBtn.disabled) {
                    const action = pageBtn.getAttribute('data-action');
                    const page = pageBtn.getAttribute('data-page');
                    
                    if (action === 'prev') {
                        this.previousPage();
                    } else if (action === 'next') {
                        this.nextPage();
                    } else if (action === 'first') {
                        this.goToPage(1);
                    } else if (action === 'last') {
                        this.goToPage(this.getTotalPages());
                    } else if (page) {
                        this.goToPage(parseInt(page));
                    }
                }
            });
        }
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.target.closest('.pagination')) {
                this.handleKeyboardNavigation(e);
            }
        });
    }
    
    setItems(items) {
        this.items = items || [];
        this.totalItems = this.items.length;
        
        // Reset to first page if current page is out of range
        const totalPages = this.getTotalPages();
        if (this.currentPage > totalPages && totalPages > 0) {
            this.currentPage = totalPages;
        } else if (this.currentPage < 1) {
            this.currentPage = 1;
        }
        
        this.render();
        this.renderPagination();
        
        return this;
    }
    
    getCurrentPageItems() {
        const startIndex = (this.currentPage - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;
        return this.items.slice(startIndex, endIndex);
    }
    
    goToPage(page) {
        const totalPages = this.getTotalPages();
        
        if (page < 1 || page > totalPages || page === this.currentPage) {
            return this;
        }
        
        this.currentPage = page;
        this.render();
        this.renderPagination();
        
        if (this.onPageChange) {
            this.onPageChange({
                page: this.currentPage,
                items: this.getCurrentPageItems(),
                totalPages: totalPages,
                totalItems: this.totalItems
            });
        }
        
        return this;
    }
    
    nextPage() {
        return this.goToPage(this.currentPage + 1);
    }
    
    previousPage() {
        return this.goToPage(this.currentPage - 1);
    }
    
    firstPage() {
        return this.goToPage(1);
    }
    
    lastPage() {
        return this.goToPage(this.getTotalPages());
    }
    
    getTotalPages() {
        return Math.ceil(this.totalItems / this.itemsPerPage);
    }
    
    getCurrentPage() {
        return this.currentPage;
    }
    
    getPageInfo() {
        const totalPages = this.getTotalPages();
        const startItem = (this.currentPage - 1) * this.itemsPerPage + 1;
        const endItem = Math.min(this.currentPage * this.itemsPerPage, this.totalItems);
        
        return {
            currentPage: this.currentPage,
            totalPages,
            totalItems: this.totalItems,
            itemsPerPage: this.itemsPerPage,
            startItem,
            endItem,
            hasNextPage: this.currentPage < totalPages,
            hasPreviousPage: this.currentPage > 1
        };
    }
    
    setItemsPerPage(count) {
        this.itemsPerPage = Math.max(1, count);
        this.currentPage = 1; // Reset to first page
        this.render();
        this.renderPagination();
        return this;
    }
    
    render() {
        if (!this.container) return;
        
        const currentItems = this.getCurrentPageItems();
        
        if (this.onRender) {
            this.onRender(currentItems, this.getPageInfo());
        } else {
            // Default rendering
            this.container.innerHTML = '';
            currentItems.forEach(item => {
                const itemElement = this.createItemElement(item);
                this.container.appendChild(itemElement);
            });
        }
    }
    
    createItemElement(item) {
        // Default item renderer - should be overridden
        const element = document.createElement('div');
        element.className = 'paginated-item';
        element.textContent = JSON.stringify(item);
        return element;
    }
    
    renderPagination() {
        if (!this.paginationContainer) return;
        
        const pageInfo = this.getPageInfo();
        
        if (pageInfo.totalPages <= 1) {
            this.paginationContainer.innerHTML = '';
            return;
        }
        
        const paginationHTML = this.createPaginationHTML(pageInfo);
        this.paginationContainer.innerHTML = paginationHTML;
        
        // Update ARIA labels
        this.updateAccessibility();
    }
    
    createPaginationHTML(pageInfo) {
        const { currentPage, totalPages, hasNextPage, hasPreviousPage } = pageInfo;
        let html = '';
        
        // Previous button
        html += `
            <button class="page-btn prev-btn" data-action="prev" 
                    ${!hasPreviousPage ? 'disabled' : ''} 
                    title="Previous page">
                ← Previous
            </button>
        `;
        
        // Page numbers
        const pageNumbers = this.getPageNumbers(currentPage, totalPages);
        
        pageNumbers.forEach(pageNum => {
            if (pageNum === '...') {
                html += '<span class="page-ellipsis">...</span>';
            } else {
                const isActive = pageNum === currentPage;
                html += `
                    <button class="page-btn page-number ${isActive ? 'active' : ''}" 
                            data-page="${pageNum}" 
                            ${isActive ? 'disabled' : ''}
                            title="Go to page ${pageNum}">
                        ${pageNum}
                    </button>
                `;
            }
        });
        
        // Next button
        html += `
            <button class="page-btn next-btn" data-action="next" 
                    ${!hasNextPage ? 'disabled' : ''} 
                    title="Next page">
                Next →
            </button>
        `;
        
        // Page info
        html += `
            <div class="page-info">
                Showing ${pageInfo.startItem}-${pageInfo.endItem} of ${pageInfo.totalItems}
            </div>
        `;
        
        return html;
    }
    
    getPageNumbers(currentPage, totalPages) {
        const delta = 2; // Number of pages to show on each side of current page
        const range = [];
        const rangeWithDots = [];
        
        for (let i = Math.max(2, currentPage - delta); 
             i <= Math.min(totalPages - 1, currentPage + delta); 
             i++) {
            range.push(i);
        }
        
        if (currentPage - delta > 2) {
            rangeWithDots.push(1, '...');
        } else {
            rangeWithDots.push(1);
        }
        
        rangeWithDots.push(...range);
        
        if (currentPage + delta < totalPages - 1) {
            rangeWithDots.push('...', totalPages);
        } else if (totalPages > 1) {
            rangeWithDots.push(totalPages);
        }
        
        return rangeWithDots;
    }
    
    handleKeyboardNavigation(e) {
        switch (e.key) {
            case 'ArrowLeft':
                e.preventDefault();
                this.previousPage();
                break;
            case 'ArrowRight':
                e.preventDefault();
                this.nextPage();
                break;
            case 'Home':
                e.preventDefault();
                this.firstPage();
                break;
            case 'End':
                e.preventDefault();
                this.lastPage();
                break;
        }
    }
    
    updateAccessibility() {
        const pageButtons = this.paginationContainer.querySelectorAll('.page-btn');
        pageButtons.forEach(btn => {
            if (btn.disabled) {
                btn.setAttribute('aria-disabled', 'true');
            } else {
                btn.removeAttribute('aria-disabled');
            }
        });
        
        // Set ARIA label for pagination container
        this.paginationContainer.setAttribute('role', 'navigation');
        this.paginationContainer.setAttribute('aria-label', 'Pagination navigation');
    }
    
    // Search and filter integration
    setFilter(filterFn) {
        this.filterFunction = filterFn;
        this.applyFilter();
        return this;
    }
    
    applyFilter() {
        if (this.filterFunction && this.originalItems) {
            this.setItems(this.originalItems.filter(this.filterFunction));
        }
    }
    
    clearFilter() {
        this.filterFunction = null;
        if (this.originalItems) {
            this.setItems(this.originalItems);
        }
        return this;
    }
    
    // Save original items for filtering
    setOriginalItems(items) {
        this.originalItems = items;
        this.setItems(items);
        return this;
    }
    
    // Export pagination state
    getState() {
        return {
            currentPage: this.currentPage,
            itemsPerPage: this.itemsPerPage,
            totalItems: this.totalItems,
            totalPages: this.getTotalPages()
        };
    }
    
    // Restore pagination state
    setState(state) {
        this.currentPage = state.currentPage || 1;
        this.itemsPerPage = state.itemsPerPage || 10;
        this.render();
        this.renderPagination();
        return this;
    }
    
    // Jump to item by finding its page
    jumpToItem(itemId, idField = 'id') {
        const itemIndex = this.items.findIndex(item => item[idField] === itemId);
        if (itemIndex === -1) return false;
        
        const targetPage = Math.ceil((itemIndex + 1) / this.itemsPerPage);
        this.goToPage(targetPage);
        
        // Scroll to item if needed
        setTimeout(() => {
            const itemElement = this.container.querySelector(`[data-${idField}="${itemId}"]`);
            if (itemElement) {
                itemElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
                itemElement.classList.add('highlighted');
                setTimeout(() => itemElement.classList.remove('highlighted'), 2000);
            }
        }, 100);
        
        return true;
    }
    
    // Utility method to create page size selector
    createPageSizeSelector(sizes = [5, 10, 25, 50]) {
        const select = document.createElement('select');
        select.className = 'page-size-selector';
        select.setAttribute('aria-label', 'Items per page');
        
        sizes.forEach(size => {
            const option = document.createElement('option');
            option.value = size;
            option.textContent = `${size} per page`;
            option.selected = size === this.itemsPerPage;
            select.appendChild(option);
        });
        
        select.addEventListener('change', (e) => {
            this.setItemsPerPage(parseInt(e.target.value));
        });
        
        return select;
    }
}

// Add CSS for pagination
const style = document.createElement('style');
style.textContent = `
    .pagination {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: var(--space-sm);
        margin: var(--space-lg) 0;
        flex-wrap: wrap;
    }
    
    .page-btn {
        background: var(--color-surface);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-md);
        padding: var(--space-sm) var(--space-md);
        cursor: pointer;
        transition: all var(--transition-fast);
        color: var(--color-text-primary);
        font-size: var(--font-size-sm);
        min-width: 40px;
        text-align: center;
    }
    
    .page-btn:hover:not(:disabled) {
        background: var(--color-surface-elevated);
        border-color: var(--color-primary);
        transform: translateY(-1px);
    }
    
    .page-btn.active {
        background: var(--color-primary);
        color: white;
        border-color: var(--color-primary);
    }
    
    .page-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
        transform: none;
    }
    
    .page-ellipsis {
        padding: var(--space-sm) var(--space-xs);
        color: var(--color-text-muted);
        font-size: var(--font-size-sm);
    }
    
    .page-info {
        font-size: var(--font-size-sm);
        color: var(--color-text-secondary);
        margin-left: var(--space-md);
        white-space: nowrap;
    }
    
    .page-size-selector {
        background: var(--color-surface);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-md);
        padding: var(--space-sm);
        color: var(--color-text-primary);
        font-size: var(--font-size-sm);
        cursor: pointer;
    }
    
    .page-size-selector:focus {
        outline: none;
        border-color: var(--color-primary);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    .paginated-item.highlighted {
        background: var(--color-primary);
        color: white;
        transition: all var(--transition-normal);
    }
    
    @media (max-width: 768px) {
        .pagination {
            flex-direction: column;
            gap: var(--space-md);
        }
        
        .page-info {
            margin-left: 0;
            order: -1;
        }
        
        .page-btn {
            min-width: 35px;
            padding: var(--space-xs) var(--space-sm);
        }
    }
`;
document.head.appendChild(style);