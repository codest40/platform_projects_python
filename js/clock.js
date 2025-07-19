// Clock.js - Manages real-time clock updates
export class ClockManager {
    constructor() {
        this.clocks = new Map();
        this.intervalId = null;
        this.updateInterval = 1000; // 1 second
        this.timezoneManager = null;
        this.isRunning = false;
    }
    
    init(timezoneManager) {
        this.timezoneManager = timezoneManager;
    }
    
    addClock(timezone) {
        if (!this.timezoneManager) {
            console.error('TimezoneManager not initialized');
            return;
        }
        
        if (this.clocks.has(timezone)) {
            return; // Clock already exists
        }
        
        // Find all elements for this timezone
        const timeElements = document.querySelectorAll(`[data-timezone="${timezone}"]`);
        
        if (timeElements.length === 0) {
            console.warn('No elements found for timezone:', timezone);
            return;
        }
        
        this.clocks.set(timezone, {
            timezone,
            elements: Array.from(timeElements),
            lastUpdate: null
        });
        
        // Update immediately
        this.updateClock(timezone);
        
        // Start the interval if not already running
        if (!this.isRunning) {
            this.start();
        }
    }
    
    removeClock(timezone) {
        this.clocks.delete(timezone);
        
        // Stop the interval if no clocks remain
        if (this.clocks.size === 0 && this.isRunning) {
            this.stop();
        }
    }
    
    updateClock(timezone) {
        const clock = this.clocks.get(timezone);
        if (!clock) return;
        
        try {
            const timeInfo = this.timezoneManager.getCurrentTime(timezone);
            
            if (!timeInfo.isValid) {
                console.error('Invalid time for timezone:', timezone);
                return;
            }
            
            clock.elements.forEach(element => {
                this.updateElement(element, timeInfo);
            });
            
            clock.lastUpdate = Date.now();
            
        } catch (error) {
            console.error('Error updating clock for timezone:', timezone, error);
        }
    }
    
    updateElement(element, timeInfo) {
        const className = element.className;
        
        if (className.includes('current-time')) {
            element.textContent = timeInfo.time;
        } else if (className.includes('timezone-offset')) {
            const offsetHours = timeInfo.offsetHours;
            const offsetText = offsetHours >= 0 ? `UTC+${offsetHours}` : `UTC${offsetHours}`;
            element.textContent = offsetText;
        } else if (className.includes('timezone-abbr')) {
            element.textContent = timeInfo.abbreviation;
        } else if (className.includes('result-current-time')) {
            element.textContent = timeInfo.time;
        } else if (className.includes('result-offset')) {
            element.textContent = timeInfo.offset;
        } else if (className.includes('option-current-time')) {
            element.textContent = timeInfo.time;
        } else if (className.includes('option-offset')) {
            element.textContent = timeInfo.offset;
        }
    }
    
    updateAllClocks() {
        this.clocks.forEach((clock, timezone) => {
            this.updateClock(timezone);
        });
    }
    
    start() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        this.intervalId = setInterval(() => {
            this.updateAllClocks();
        }, this.updateInterval);
        
        console.log('Clock manager started');
    }
    
    stop() {
        if (!this.isRunning) return;
        
        this.isRunning = false;
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
        
        console.log('Clock manager stopped');
    }
    
    startAll() {
        // Update all clocks immediately
        this.updateAllClocks();
        
        // Start the update interval
        this.start();
    }
    
    refreshElements() {
        // Re-scan for elements in case new ones were added
        this.clocks.forEach((clock, timezone) => {
            const timeElements = document.querySelectorAll(`[data-timezone="${timezone}"]`);
            clock.elements = Array.from(timeElements);
        });
    }
    
    setUpdateInterval(milliseconds) {
        if (milliseconds < 100) {
            console.warn('Update interval too low, minimum is 100ms');
            return;
        }
        
        this.updateInterval = milliseconds;
        
        // Restart with new interval if currently running
        if (this.isRunning) {
            this.stop();
            this.start();
        }
    }
    
    getClockInfo(timezone) {
        return this.clocks.get(timezone);
    }
    
    getAllClocks() {
        return Array.from(this.clocks.keys());
    }
    
    getRunningState() {
        return {
            isRunning: this.isRunning,
            clockCount: this.clocks.size,
            updateInterval: this.updateInterval,
            intervalId: this.intervalId
        };
    }
    
    // Pause/resume functionality for performance optimization
    pause() {
        if (this.isRunning) {
            this.stop();
            this._wasPaused = true;
        }
    }
    
    resume() {
        if (this._wasPaused && this.clocks.size > 0) {
            this.start();
            this._wasPaused = false;
        }
    }
    
    // Performance optimization: pause when page is not visible
    setupVisibilityHandling() {
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.pause();
            } else {
                this.resume();
                // Update immediately when page becomes visible
                this.updateAllClocks();
            }
        });
    }
    
    // Handle timezone changes dynamically
    handleTimezoneElementsChange() {
        // Use MutationObserver to detect when timezone elements are added/removed
        const observer = new MutationObserver((mutations) => {
            let needsRefresh = false;
            
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        const timezoneElements = node.querySelectorAll('[data-timezone]');
                        if (timezoneElements.length > 0) {
                            needsRefresh = true;
                        }
                    }
                });
                
                mutation.removedNodes.forEach((node) => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        const timezoneElements = node.querySelectorAll('[data-timezone]');
                        if (timezoneElements.length > 0) {
                            needsRefresh = true;
                        }
                    }
                });
            });
            
            if (needsRefresh) {
                this.refreshElements();
            }
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
        
        return observer;
    }
    
    // Format time for different display purposes
    formatTime(timezone, format = 'HH:mm:ss') {
        if (!this.timezoneManager) {
            return '--:--:--';
        }
        
        return this.timezoneManager.formatTimeForDisplay(timezone, format);
    }
    
    // Get detailed time information for a timezone
    getDetailedTimeInfo(timezone) {
        if (!this.timezoneManager) {
            return null;
        }
        
        return this.timezoneManager.getTimezoneInfo(timezone);
    }
    
    // Cleanup method
    destroy() {
        this.stop();
        this.clocks.clear();
        this.timezoneManager = null;
    }
}