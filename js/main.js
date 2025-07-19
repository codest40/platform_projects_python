// Main.js - Application initialization and coordination
import { ThemeManager } from './theme.js';
import { TimezoneManager } from './time.js';
import { SearchManager } from './search.js';
import { ClockManager } from './clock.js';

class TimzapApp {
    constructor() {
        this.themeManager = new ThemeManager();
        this.timezoneManager = new TimezoneManager();
        this.searchManager = new SearchManager();
        this.clockManager = new ClockManager();
        
        this.init();
    }
    
    async init() {
        try {
            // Initialize theme first
            await this.themeManager.init();
            
            // Load timezone data
            await this.timezoneManager.loadTimezoneData();
            
            // Initialize search
            this.searchManager.init(this.timezoneManager);
            
            // Initialize clocks
            this.clockManager.init(this.timezoneManager);
            
            // Set up event listeners
            this.setupEventListeners();
            
            // Load saved cities and display them
            this.loadSavedCities();
            
            console.log('Timzap app initialized successfully');
        } catch (error) {
            console.error('Failed to initialize Timzap app:', error);
            this.showError('Failed to load application. Please refresh the page.');
        }
    }
    
    setupEventListeners() {
        // Theme toggle
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                this.themeManager.toggleTheme();
            });
        }
        
        // Search functionality
        const searchInput = document.getElementById('city-search');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.searchManager.handleSearch(e.target.value);
            });
            
            // Clear search when clicking outside
            document.addEventListener('click', (e) => {
                if (!e.target.closest('.search-container')) {
                    this.searchManager.hideResults();
                }
            });
        }
        
        // Listen for city selection
        document.addEventListener('citySelected', (e) => {
            this.addCity(e.detail);
        });
        
        // Listen for city removal
        document.addEventListener('cityRemoved', (e) => {
            this.removeCity(e.detail.timezone);
        });
    }
    
    loadSavedCities() {
        const savedCities = this.getSavedCities();
        
        // If no saved cities, add default ones
        if (savedCities.length === 0) {
            const defaultCities = [
                { name: 'New York', country: 'United States', timezone: 'America/New_York', emoji: '🇺🇸' },
                { name: 'London', country: 'United Kingdom', timezone: 'Europe/London', emoji: '🇬🇧' },
                { name: 'Tokyo', country: 'Japan', timezone: 'Asia/Tokyo', emoji: '🇯🇵' }
            ];
            
            defaultCities.forEach(city => {
                this.addCity(city, false); // Don't save to storage yet
            });
            
            // Save all default cities at once
            this.saveCities(defaultCities);
        } else {
            // Load saved cities
            savedCities.forEach(city => {
                this.addCity(city, false); // Don't save again
            });
        }
        
        // Start the clocks
        this.clockManager.startAll();
    }
    
    addCity(cityData, saveToStorage = true) {
        const container = document.getElementById('timezone-cards');
        if (!container) return;
        
        // Check if city already exists
        if (container.querySelector(`[data-timezone="${cityData.timezone}"]`)) {
            this.showMessage('City already added', 'warning');
            return;
        }
        
        // Create timezone card
        const card = this.createTimezoneCard(cityData);
        container.appendChild(card);
        
        // Add fade-in animation
        card.classList.add('fade-in');
        
        // Save to localStorage if requested
        if (saveToStorage) {
            const savedCities = this.getSavedCities();
            savedCities.push(cityData);
            this.saveCities(savedCities);
        }
        
        // Register with clock manager
        this.clockManager.addClock(cityData.timezone);
        
        // Clear search
        this.searchManager.clearSearch();
    }
    
    removeCity(timezone) {
        const card = document.querySelector(`[data-timezone="${timezone}"]`);
        if (card) {
            card.remove();
            
            // Remove from saved cities
            const savedCities = this.getSavedCities().filter(city => city.timezone !== timezone);
            this.saveCities(savedCities);
            
            // Unregister from clock manager
            this.clockManager.removeClock(timezone);
        }
    }
    
    createTimezoneCard(cityData) {
        const card = document.createElement('div');
        card.className = 'timezone-card';
        card.setAttribute('data-timezone', cityData.timezone);
        
        card.innerHTML = `
            <div class="card-header">
                <div class="city-info">
                    <h3>${cityData.emoji} ${cityData.name}</h3>
                    <p>${cityData.country}</p>
                </div>
                <button class="remove-btn" data-timezone="${cityData.timezone}">×</button>
            </div>
            <div class="time-display">
                <div class="current-time" data-timezone="${cityData.timezone}">--:--:--</div>
            </div>
            <div class="timezone-info">
                <span class="timezone-offset" data-timezone="${cityData.timezone}">--</span>
                <span class="timezone-abbr" data-timezone="${cityData.timezone}">--</span>
            </div>
        `;
        
        // Add remove event listener
        const removeBtn = card.querySelector('.remove-btn');
        removeBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const timezone = e.target.getAttribute('data-timezone');
            document.dispatchEvent(new CustomEvent('cityRemoved', { detail: { timezone } }));
        });
        
        return card;
    }
    
    getSavedCities() {
        try {
            const saved = localStorage.getItem('timzap-cities');
            return saved ? JSON.parse(saved) : [];
        } catch (error) {
            console.error('Error loading saved cities:', error);
            return [];
        }
    }
    
    saveCities(cities) {
        try {
            localStorage.setItem('timzap-cities', JSON.stringify(cities));
        } catch (error) {
            console.error('Error saving cities:', error);
        }
    }
    
    showMessage(message, type = 'info') {
        // Simple toast notification
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--color-surface-elevated);
            color: var(--color-text-primary);
            padding: var(--space-md) var(--space-lg);
            border-radius: var(--radius-md);
            border: 1px solid var(--color-border);
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
    
    showError(message) {
        this.showMessage(message, 'error');
    }
}

// Initialize app when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new TimzapApp();
    });
} else {
    new TimzapApp();
}

// Add toast animations to head
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);