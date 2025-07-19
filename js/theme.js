// Theme.js - Handles theme switching and persistence
export class ThemeManager {
    constructor() {
        this.currentTheme = 'auto';
        this.systemTheme = 'light';
        this.storageKey = 'timzap-theme';
        
        this.mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    }
    
    async init() {
        // Detect system theme
        this.systemTheme = this.mediaQuery.matches ? 'dark' : 'light';
        
        // Listen for system theme changes
        this.mediaQuery.addEventListener('change', (e) => {
            this.systemTheme = e.matches ? 'dark' : 'light';
            if (this.currentTheme === 'auto') {
                this.applyTheme();
            }
        });
        
        // Load saved theme
        this.loadTheme();
        
        // Apply theme
        this.applyTheme();
        
        // Update toggle button
        this.updateThemeToggle();
    }
    
    loadTheme() {
        try {
            const savedTheme = localStorage.getItem(this.storageKey);
            if (savedTheme && ['light', 'dark', 'auto'].includes(savedTheme)) {
                this.currentTheme = savedTheme;
            }
        } catch (error) {
            console.error('Error loading theme:', error);
            this.currentTheme = 'auto';
        }
    }
    
    saveTheme() {
        try {
            localStorage.setItem(this.storageKey, this.currentTheme);
        } catch (error) {
            console.error('Error saving theme:', error);
        }
    }
    
    getEffectiveTheme() {
        if (this.currentTheme === 'auto') {
            return this.systemTheme;
        }
        return this.currentTheme;
    }
    
    applyTheme() {
        const effectiveTheme = this.getEffectiveTheme();
        const html = document.documentElement;
        
        // Remove existing theme classes
        html.removeAttribute('data-theme');
        
        // Apply new theme
        if (effectiveTheme === 'dark') {
            html.setAttribute('data-theme', 'dark');
        } else {
            html.setAttribute('data-theme', 'light');
        }
        
        // Dispatch theme change event
        document.dispatchEvent(new CustomEvent('themeChanged', {
            detail: {
                theme: this.currentTheme,
                effectiveTheme: effectiveTheme
            }
        }));
    }
    
    setTheme(theme) {
        if (!['light', 'dark', 'auto'].includes(theme)) {
            console.warn('Invalid theme:', theme);
            return;
        }
        
        this.currentTheme = theme;
        this.saveTheme();
        this.applyTheme();
        this.updateThemeToggle();
    }
    
    toggleTheme() {
        const themes = ['light', 'dark', 'auto'];
        const currentIndex = themes.indexOf(this.currentTheme);
        const nextIndex = (currentIndex + 1) % themes.length;
        this.setTheme(themes[nextIndex]);
    }
    
    updateThemeToggle() {
        const toggleButton = document.getElementById('theme-toggle');
        if (!toggleButton) return;
        
        const icons = {
            light: '☀️',
            dark: '🌙',
            auto: '🌓'
        };
        
        const labels = {
            light: 'Light theme',
            dark: 'Dark theme',
            auto: 'Auto theme (follows system)'
        };
        
        toggleButton.textContent = icons[this.currentTheme];
        toggleButton.setAttribute('title', labels[this.currentTheme]);
        toggleButton.setAttribute('aria-label', labels[this.currentTheme]);
    }
    
    getCurrentTheme() {
        return this.currentTheme;
    }
    
    getEffectiveThemeName() {
        return this.getEffectiveTheme();
    }
    
    isDarkMode() {
        return this.getEffectiveTheme() === 'dark';
    }
    
    isLightMode() {
        return this.getEffectiveTheme() === 'light';
    }
    
    isAutoMode() {
        return this.currentTheme === 'auto';
    }
    
    getSystemTheme() {
        return this.systemTheme;
    }
    
    // Utility method to get theme-appropriate colors
    getThemeColor(colorName) {
        const computedStyle = getComputedStyle(document.documentElement);
        return computedStyle.getPropertyValue(`--color-${colorName}`).trim();
    }
    
    // Method to temporarily override theme for specific elements
    applyThemeToElement(element, theme) {
        if (!element) return;
        
        element.setAttribute('data-theme-override', theme);
        
        // Return cleanup function
        return () => {
            element.removeAttribute('data-theme-override');
        };
    }
    
    // Add custom CSS properties for theme transitions
    addThemeTransitions() {
        const style = document.createElement('style');
        style.textContent = `
            :root {
                transition: 
                    color 0.3s ease,
                    background-color 0.3s ease,
                    border-color 0.3s ease;
            }
            
            * {
                transition: 
                    color 0.3s ease,
                    background-color 0.3s ease,
                    border-color 0.3s ease,
                    box-shadow 0.3s ease;
            }
            
            /* Preserve important animations */
            .fade-in,
            .loading,
            [class*="animate-"] {
                transition: none !important;
                animation-duration: inherit !important;
            }
        `;
        
        document.head.appendChild(style);
    }
    
    // Event listener helpers
    onThemeChange(callback) {
        document.addEventListener('themeChanged', callback);
        
        // Return cleanup function
        return () => {
            document.removeEventListener('themeChanged', callback);
        };
    }
    
    // Method to detect if user prefers reduced motion
    prefersReducedMotion() {
        return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    }
    
    // Method to get contrast ratio preference
    getContrastPreference() {
        if (window.matchMedia('(prefers-contrast: high)').matches) {
            return 'high';
        } else if (window.matchMedia('(prefers-contrast: low)').matches) {
            return 'low';
        }
        return 'normal';
    }
}

// Add theme-related CSS custom properties
const themeStyle = document.createElement('style');
themeStyle.textContent = `
    /* Theme transition styles */
    [data-theme-override="dark"] {
        --color-background: #0f172a;
        --color-surface: #1e293b;
        --color-surface-elevated: #334155;
        --color-text-primary: #f1f5f9;
        --color-text-secondary: #cbd5e1;
        --color-text-muted: #64748b;
        --color-border: #334155;
        --color-border-light: #475569;
        --glass-bg: rgba(15, 23, 42, 0.25);
        --glass-border: rgba(148, 163, 184, 0.18);
        --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        --cosmic-glow: 0 0 20px rgba(102, 126, 234, 0.5);
    }
    
    [data-theme-override="light"] {
        --color-background: #ffffff;
        --color-surface: #f8fafc;
        --color-surface-elevated: #ffffff;
        --color-text-primary: #1e293b;
        --color-text-secondary: #64748b;
        --color-text-muted: #94a3b8;
        --color-border: #e2e8f0;
        --color-border-light: #f1f5f9;
        --glass-bg: rgba(255, 255, 255, 0.25);
        --glass-border: rgba(255, 255, 255, 0.18);
        --glass-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        --cosmic-glow: 0 0 20px rgba(102, 126, 234, 0.3);
    }
`;
document.head.appendChild(themeStyle);