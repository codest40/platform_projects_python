// Search.js - Handles city search functionality
export class SearchManager {
    constructor() {
        this.searchInput = null;
        this.searchResults = null;
        this.timezoneManager = null;
        this.debounceTimer = null;
        this.debounceDelay = 300;
    }
    
    init(timezoneManager) {
        this.timezoneManager = timezoneManager;
        this.searchInput = document.getElementById('city-search');
        this.searchResults = document.getElementById('search-results');
        
        if (!this.searchInput || !this.searchResults) {
            console.warn('Search elements not found');
            return;
        }
        
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Handle input with debouncing
        this.searchInput.addEventListener('input', (e) => {
            this.handleSearch(e.target.value);
        });
        
        // Handle keyboard navigation
        this.searchInput.addEventListener('keydown', (e) => {
            this.handleKeyboardNavigation(e);
        });
        
        // Handle focus
        this.searchInput.addEventListener('focus', () => {
            if (this.searchInput.value.trim()) {
                this.showResults();
            }
        });
        
        // Handle clicks on results
        this.searchResults.addEventListener('click', (e) => {
            const resultElement = e.target.closest('.search-result');
            if (resultElement) {
                this.selectResult(resultElement);
            }
        });
    }
    
    handleSearch(query) {
        // Clear previous timer
        if (this.debounceTimer) {
            clearTimeout(this.debounceTimer);
        }
        
        // Debounce the search
        this.debounceTimer = setTimeout(() => {
            this.performSearch(query);
        }, this.debounceDelay);
    }
    
    performSearch(query) {
        const trimmedQuery = query.trim();
        
        if (trimmedQuery.length < 2) {
            this.hideResults();
            return;
        }
        
        const results = this.timezoneManager.searchCities(trimmedQuery);
        this.displayResults(results);
    }
    
    displayResults(results) {
        this.clearResults();
        
        if (results.length === 0) {
            this.showNoResults();
            return;
        }
        
        results.forEach((result, index) => {
            const resultElement = this.createResultElement(result, index === 0);
            this.searchResults.appendChild(resultElement);
        });
        
        this.showResults();
    }
    
    createResultElement(cityData, isFirst = false) {
        const resultDiv = document.createElement('div');
        resultDiv.className = `search-result ${isFirst ? 'highlighted' : ''}`;
        resultDiv.setAttribute('data-city', JSON.stringify(cityData));
        
        // Get current time for the city
        const timeInfo = this.timezoneManager.getCurrentTime(cityData.timezone);
        
        resultDiv.innerHTML = `
            <div class="result-main">
                <div class="result-city">${cityData.emoji} ${cityData.name}</div>
                <div class="result-country">${cityData.country}</div>
            </div>
            <div class="result-time">
                <div class="result-current-time">${timeInfo.time}</div>
                <div class="result-offset">${timeInfo.offset}</div>
            </div>
        `;
        
        // Add hover effect
        resultDiv.addEventListener('mouseenter', () => {
            this.highlightResult(resultDiv);
        });
        
        return resultDiv;
    }
    
    showNoResults() {
        const noResultsDiv = document.createElement('div');
        noResultsDiv.className = 'search-no-results';
        noResultsDiv.innerHTML = `
            <div style="padding: var(--space-lg); text-align: center; color: var(--color-text-muted);">
                No cities found. Try a different search term.
            </div>
        `;
        
        this.searchResults.appendChild(noResultsDiv);
        this.showResults();
    }
    
    showResults() {
        this.searchResults.classList.add('show');
    }
    
    hideResults() {
        this.searchResults.classList.remove('show');
    }
    
    clearResults() {
        this.searchResults.innerHTML = '';
    }
    
    highlightResult(resultElement) {
        // Remove highlight from all results
        this.searchResults.querySelectorAll('.search-result').forEach(el => {
            el.classList.remove('highlighted');
        });
        
        // Add highlight to current result
        resultElement.classList.add('highlighted');
    }
    
    getHighlightedResult() {
        return this.searchResults.querySelector('.search-result.highlighted');
    }
    
    selectResult(resultElement) {
        const cityDataStr = resultElement.getAttribute('data-city');
        if (!cityDataStr) return;
        
        try {
            const cityData = JSON.parse(cityDataStr);
            
            // Dispatch city selection event
            document.dispatchEvent(new CustomEvent('citySelected', {
                detail: cityData
            }));
            
            this.clearSearch();
        } catch (error) {
            console.error('Error selecting city:', error);
        }
    }
    
    handleKeyboardNavigation(e) {
        const results = this.searchResults.querySelectorAll('.search-result');
        const highlighted = this.getHighlightedResult();
        
        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                this.navigateDown(results, highlighted);
                break;
                
            case 'ArrowUp':
                e.preventDefault();
                this.navigateUp(results, highlighted);
                break;
                
            case 'Enter':
                e.preventDefault();
                if (highlighted) {
                    this.selectResult(highlighted);
                }
                break;
                
            case 'Escape':
                this.clearSearch();
                this.searchInput.blur();
                break;
        }
    }
    
    navigateDown(results, highlighted) {
        if (results.length === 0) return;
        
        if (!highlighted) {
            this.highlightResult(results[0]);
        } else {
            const currentIndex = Array.from(results).indexOf(highlighted);
            const nextIndex = Math.min(currentIndex + 1, results.length - 1);
            this.highlightResult(results[nextIndex]);
        }
    }
    
    navigateUp(results, highlighted) {
        if (results.length === 0) return;
        
        if (!highlighted) {
            this.highlightResult(results[results.length - 1]);
        } else {
            const currentIndex = Array.from(results).indexOf(highlighted);
            const prevIndex = Math.max(currentIndex - 1, 0);
            this.highlightResult(results[prevIndex]);
        }
    }
    
    clearSearch() {
        if (this.searchInput) {
            this.searchInput.value = '';
        }
        this.hideResults();
        this.clearResults();
    }
    
    setPlaceholder(text) {
        if (this.searchInput) {
            this.searchInput.placeholder = text;
        }
    }
    
    focus() {
        if (this.searchInput) {
            this.searchInput.focus();
        }
    }
}

// Add CSS for search result styling
const style = document.createElement('style');
style.textContent = `
    .search-result {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: var(--space-md);
        cursor: pointer;
        transition: all var(--transition-fast);
        border-bottom: 1px solid var(--color-border-light);
    }
    
    .search-result:hover,
    .search-result.highlighted {
        background: var(--color-surface);
        border-color: var(--color-primary);
    }
    
    .search-result:last-child {
        border-bottom: none;
    }
    
    .result-main {
        flex: 1;
    }
    
    .result-city {
        font-weight: 600;
        color: var(--color-text-primary);
        margin-bottom: var(--space-xs);
    }
    
    .result-country {
        font-size: var(--font-size-sm);
        color: var(--color-text-secondary);
    }
    
    .result-time {
        text-align: right;
        margin-left: var(--space-md);
    }
    
    .result-current-time {
        font-weight: 600;
        color: var(--color-primary);
        font-variant-numeric: tabular-nums;
    }
    
    .result-offset {
        font-size: var(--font-size-sm);
        color: var(--color-text-muted);
    }
    
    .search-no-results {
        padding: var(--space-lg);
        text-align: center;
        color: var(--color-text-muted);
    }
`;
document.head.appendChild(style);