// TimezoneSelector.js - Custom dropdown for timezone selection
export class TimezoneSelector {
    constructor(element, timezoneManager) {
        this.element = element;
        this.timezoneManager = timezoneManager;
        this.isOpen = false;
        this.selectedTimezone = null;
        this.filteredOptions = [];
        this.highlightedIndex = -1;
        
        this.init();
    }
    
    init() {
        this.createSelector();
        this.loadTimezones();
        this.setupEventListeners();
    }
    
    createSelector() {
        this.element.innerHTML = '';
        this.element.className = 'timezone-selector';
        
        const selectorHTML = `
            <div class="selector-input-container">
                <input type="text" class="selector-input" placeholder="Select timezone..." readonly>
                <div class="selector-arrow">▼</div>
            </div>
            <div class="selector-dropdown">
                <div class="selector-search-container">
                    <input type="text" class="selector-search" placeholder="Search timezones...">
                </div>
                <div class="selector-options"></div>
            </div>
        `;
        
        this.element.innerHTML = selectorHTML;
        
        // Get references to elements
        this.input = this.element.querySelector('.selector-input');
        this.searchInput = this.element.querySelector('.selector-search');
        this.dropdown = this.element.querySelector('.selector-dropdown');
        this.optionsContainer = this.element.querySelector('.selector-options');
        this.arrow = this.element.querySelector('.selector-arrow');
    }
    
    loadTimezones() {
        this.timezones = this.timezoneManager.getAvailableTimezones();
        this.filteredOptions = [...this.timezones];
        this.renderOptions();
    }
    
    setupEventListeners() {
        // Toggle dropdown
        this.input.addEventListener('click', () => {
            this.toggle();
        });
        
        // Search functionality
        this.searchInput.addEventListener('input', (e) => {
            this.handleSearch(e.target.value);
        });
        
        // Keyboard navigation
        this.searchInput.addEventListener('keydown', (e) => {
            this.handleKeyDown(e);
        });
        
        // Click outside to close
        document.addEventListener('click', (e) => {
            if (!this.element.contains(e.target)) {
                this.close();
            }
        });
        
        // Option selection
        this.optionsContainer.addEventListener('click', (e) => {
            const option = e.target.closest('.selector-option');
            if (option) {
                const timezone = option.getAttribute('data-timezone');
                this.selectTimezone(timezone);
            }
        });
    }
    
    handleSearch(query) {
        const normalizedQuery = query.toLowerCase().trim();
        
        if (!normalizedQuery) {
            this.filteredOptions = [...this.timezones];
        } else {
            this.filteredOptions = this.timezones.filter(tz => 
                tz.display.toLowerCase().includes(normalizedQuery) ||
                tz.timezone.toLowerCase().includes(normalizedQuery)
            );
        }
        
        this.highlightedIndex = -1;
        this.renderOptions();
    }
    
    renderOptions() {
        this.optionsContainer.innerHTML = '';
        
        if (this.filteredOptions.length === 0) {
            const noResults = document.createElement('div');
            noResults.className = 'selector-no-results';
            noResults.textContent = 'No timezones found';
            this.optionsContainer.appendChild(noResults);
            return;
        }
        
        this.filteredOptions.forEach((timezone, index) => {
            const option = this.createOption(timezone, index);
            this.optionsContainer.appendChild(option);
        });
    }
    
    createOption(timezoneData, index) {
        const option = document.createElement('div');
        option.className = 'selector-option';
        option.setAttribute('data-timezone', timezoneData.timezone);
        
        // Get current time for this timezone
        const timeInfo = this.timezoneManager.getCurrentTime(timezoneData.timezone);
        
        option.innerHTML = `
            <div class="option-main">
                <div class="option-display">${timezoneData.display}</div>
                <div class="option-timezone">${timezoneData.timezone}</div>
            </div>
            <div class="option-time">
                <div class="option-current-time">${timeInfo.time}</div>
                <div class="option-offset">${timeInfo.offset}</div>
            </div>
        `;
        
        // Highlight if selected
        if (this.selectedTimezone === timezoneData.timezone) {
            option.classList.add('selected');
        }
        
        // Highlight if keyboard navigation
        if (index === this.highlightedIndex) {
            option.classList.add('highlighted');
        }
        
        return option;
    }
    
    selectTimezone(timezone) {
        this.selectedTimezone = timezone;
        const timezoneData = this.timezones.find(tz => tz.timezone === timezone);
        
        if (timezoneData) {
            this.input.value = timezoneData.display;
            this.input.setAttribute('data-timezone', timezone);
            
            // Dispatch change event
            const event = new CustomEvent('timezoneChange', {
                detail: { timezone, timezoneData }
            });
            this.element.dispatchEvent(event);
        }
        
        this.close();
    }
    
    handleKeyDown(e) {
        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                this.navigateDown();
                break;
                
            case 'ArrowUp':
                e.preventDefault();
                this.navigateUp();
                break;
                
            case 'Enter':
                e.preventDefault();
                if (this.highlightedIndex >= 0 && this.filteredOptions[this.highlightedIndex]) {
                    this.selectTimezone(this.filteredOptions[this.highlightedIndex].timezone);
                }
                break;
                
            case 'Escape':
                this.close();
                break;
        }
    }
    
    navigateDown() {
        if (this.filteredOptions.length === 0) return;
        
        this.highlightedIndex = Math.min(
            this.highlightedIndex + 1,
            this.filteredOptions.length - 1
        );
        this.updateHighlight();
    }
    
    navigateUp() {
        if (this.filteredOptions.length === 0) return;
        
        this.highlightedIndex = Math.max(this.highlightedIndex - 1, 0);
        this.updateHighlight();
    }
    
    updateHighlight() {
        const options = this.optionsContainer.querySelectorAll('.selector-option');
        options.forEach((option, index) => {
            option.classList.toggle('highlighted', index === this.highlightedIndex);
        });
        
        // Scroll highlighted option into view
        if (this.highlightedIndex >= 0) {
            const highlightedOption = options[this.highlightedIndex];
            if (highlightedOption) {
                highlightedOption.scrollIntoView({
                    block: 'nearest'
                });
            }
        }
    }
    
    open() {
        if (this.isOpen) return;
        
        this.isOpen = true;
        this.dropdown.classList.add('open');
        this.arrow.style.transform = 'rotate(180deg)';
        this.searchInput.focus();
        this.searchInput.value = '';
        this.filteredOptions = [...this.timezones];
        this.highlightedIndex = -1;
        this.renderOptions();
    }
    
    close() {
        if (!this.isOpen) return;
        
        this.isOpen = false;
        this.dropdown.classList.remove('open');
        this.arrow.style.transform = 'rotate(0deg)';
        this.highlightedIndex = -1;
    }
    
    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }
    
    getValue() {
        return this.selectedTimezone;
    }
    
    setValue(timezone) {
        if (this.timezoneManager.isValidTimezone(timezone)) {
            this.selectTimezone(timezone);
        }
    }
    
    clear() {
        this.selectedTimezone = null;
        this.input.value = '';
        this.input.removeAttribute('data-timezone');
        this.close();
    }
}

// Add CSS for timezone selector
const style = document.createElement('style');
style.textContent = `
    .timezone-selector {
        position: relative;
        width: 100%;
    }
    
    .selector-input-container {
        position: relative;
        cursor: pointer;
    }
    
    .selector-input {
        width: 100%;
        padding: var(--space-md);
        padding-right: 40px;
        border: 1px solid var(--color-border);
        border-radius: var(--radius-md);
        background: var(--color-surface);
        color: var(--color-text-primary);
        cursor: pointer;
        transition: all var(--transition-fast);
    }
    
    .selector-input:focus {
        outline: none;
        border-color: var(--color-primary);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    .selector-arrow {
        position: absolute;
        top: 50%;
        right: var(--space-md);
        transform: translateY(-50%);
        transition: transform var(--transition-fast);
        pointer-events: none;
        color: var(--color-text-muted);
    }
    
    .selector-dropdown {
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: var(--color-surface-elevated);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-md);
        box-shadow: var(--glass-shadow);
        z-index: 100;
        max-height: 300px;
        overflow: hidden;
        opacity: 0;
        visibility: hidden;
        transform: translateY(-10px);
        transition: all var(--transition-fast);
    }
    
    .selector-dropdown.open {
        opacity: 1;
        visibility: visible;
        transform: translateY(0);
    }
    
    .selector-search-container {
        padding: var(--space-md);
        border-bottom: 1px solid var(--color-border);
    }
    
    .selector-search {
        width: 100%;
        padding: var(--space-sm) var(--space-md);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-sm);
        background: var(--color-background);
        color: var(--color-text-primary);
        font-size: var(--font-size-sm);
    }
    
    .selector-search:focus {
        outline: none;
        border-color: var(--color-primary);
    }
    
    .selector-options {
        max-height: 200px;
        overflow-y: auto;
    }
    
    .selector-option {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: var(--space-md);
        cursor: pointer;
        transition: all var(--transition-fast);
        border-bottom: 1px solid var(--color-border-light);
    }
    
    .selector-option:hover,
    .selector-option.highlighted {
        background: var(--color-surface);
    }
    
    .selector-option.selected {
        background: var(--color-primary);
        color: white;
    }
    
    .selector-option:last-child {
        border-bottom: none;
    }
    
    .option-main {
        flex: 1;
        min-width: 0;
    }
    
    .option-display {
        font-weight: 500;
        margin-bottom: var(--space-xs);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .option-timezone {
        font-size: var(--font-size-sm);
        color: var(--color-text-muted);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .selector-option.selected .option-timezone {
        color: rgba(255, 255, 255, 0.8);
    }
    
    .option-time {
        text-align: right;
        margin-left: var(--space-md);
        min-width: 80px;
    }
    
    .option-current-time {
        font-weight: 600;
        font-variant-numeric: tabular-nums;
    }
    
    .option-offset {
        font-size: var(--font-size-sm);
        color: var(--color-text-muted);
    }
    
    .selector-option.selected .option-offset {
        color: rgba(255, 255, 255, 0.8);
    }
    
    .selector-no-results {
        padding: var(--space-lg);
        text-align: center;
        color: var(--color-text-muted);
        font-style: italic;
    }
`;
document.head.appendChild(style);