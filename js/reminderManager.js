// ReminderManager.js - Handles CRUD operations for reminders
export class ReminderManager {
    constructor() {
        this.storageKey = 'timzap-reminders';
        this.reminders = [];
        this.timezoneManager = null;
    }
    
    init(timezoneManager) {
        this.timezoneManager = timezoneManager;
        this.loadReminders();
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Listen for reminder form submissions
        document.addEventListener('reminderSubmit', (e) => {
            this.handleReminderSubmit(e.detail);
        });
        
        // Listen for reminder deletions
        document.addEventListener('reminderDelete', (e) => {
            this.deleteReminder(e.detail.id);
        });
        
        // Listen for reminder edits
        document.addEventListener('reminderEdit', (e) => {
            this.editReminder(e.detail);
        });
    }
    
    loadReminders() {
        try {
            const saved = localStorage.getItem(this.storageKey);
            this.reminders = saved ? JSON.parse(saved) : [];
            
            // Sort reminders by date and time
            this.sortReminders();
            
            console.log('Loaded', this.reminders.length, 'reminders');
        } catch (error) {
            console.error('Error loading reminders:', error);
            this.reminders = [];
        }
    }
    
    saveReminders() {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(this.reminders));
        } catch (error) {
            console.error('Error saving reminders:', error);
        }
    }
    
    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }
    
    createReminder(reminderData) {
        const reminder = {
            id: this.generateId(),
            text: reminderData.text.trim(),
            date: reminderData.date,
            time: reminderData.time,
            timezone: reminderData.timezone,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString()
        };
        
        // Validate reminder data
        if (!this.validateReminder(reminder)) {
            throw new Error('Invalid reminder data');
        }
        
        this.reminders.push(reminder);
        this.sortReminders();
        this.saveReminders();
        
        // Dispatch event
        document.dispatchEvent(new CustomEvent('reminderCreated', {
            detail: reminder
        }));
        
        return reminder;
    }
    
    updateReminder(id, updates) {
        const index = this.reminders.findIndex(r => r.id === id);
        if (index === -1) {
            throw new Error('Reminder not found');
        }
        
        const updatedReminder = {
            ...this.reminders[index],
            ...updates,
            updatedAt: new Date().toISOString()
        };
        
        // Validate updated reminder
        if (!this.validateReminder(updatedReminder)) {
            throw new Error('Invalid reminder data');
        }
        
        this.reminders[index] = updatedReminder;
        this.sortReminders();
        this.saveReminders();
        
        // Dispatch event
        document.dispatchEvent(new CustomEvent('reminderUpdated', {
            detail: updatedReminder
        }));
        
        return updatedReminder;
    }
    
    deleteReminder(id) {
        const index = this.reminders.findIndex(r => r.id === id);
        if (index === -1) {
            throw new Error('Reminder not found');
        }
        
        const deletedReminder = this.reminders.splice(index, 1)[0];
        this.saveReminders();
        
        // Dispatch event
        document.dispatchEvent(new CustomEvent('reminderDeleted', {
            detail: deletedReminder
        }));
        
        return deletedReminder;
    }
    
    getReminder(id) {
        return this.reminders.find(r => r.id === id);
    }
    
    getAllReminders() {
        return [...this.reminders];
    }
    
    getRemindersByDate(date) {
        return this.reminders.filter(r => r.date === date);
    }
    
    getUpcomingReminders(limit = 10) {
        const now = new Date();
        const currentDate = now.toISOString().split('T')[0];
        const currentTime = now.toTimeString().slice(0, 5);
        
        return this.reminders
            .filter(reminder => {
                // Include reminders for today that haven't passed yet
                if (reminder.date === currentDate) {
                    return reminder.time >= currentTime;
                }
                // Include all future reminders
                return reminder.date > currentDate;
            })
            .slice(0, limit);
    }
    
    getPastReminders(limit = 10) {
        const now = new Date();
        const currentDate = now.toISOString().split('T')[0];
        const currentTime = now.toTimeString().slice(0, 5);
        
        return this.reminders
            .filter(reminder => {
                // Include reminders for today that have passed
                if (reminder.date === currentDate) {
                    return reminder.time < currentTime;
                }
                // Include all past reminders
                return reminder.date < currentDate;
            })
            .reverse() // Show most recent first
            .slice(0, limit);
    }
    
    searchReminders(query) {
        const normalizedQuery = query.toLowerCase().trim();
        
        return this.reminders.filter(reminder =>
            reminder.text.toLowerCase().includes(normalizedQuery) ||
            reminder.date.includes(normalizedQuery) ||
            reminder.time.includes(normalizedQuery)
        );
    }
    
    sortReminders() {
        this.reminders.sort((a, b) => {
            // First sort by date
            const dateComparison = a.date.localeCompare(b.date);
            if (dateComparison !== 0) {
                return dateComparison;
            }
            
            // Then sort by time
            return a.time.localeCompare(b.time);
        });
    }
    
    validateReminder(reminder) {
        // Check required fields
        if (!reminder.text || !reminder.date || !reminder.time || !reminder.timezone) {
            return false;
        }
        
        // Validate date format (YYYY-MM-DD)
        const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
        if (!dateRegex.test(reminder.date)) {
            return false;
        }
        
        // Validate time format (HH:MM)
        const timeRegex = /^([01]?[0-9]|2[0-3]):[0-5][0-9]$/;
        if (!timeRegex.test(reminder.time)) {
            return false;
        }
        
        // Validate timezone
        if (this.timezoneManager && !this.timezoneManager.isValidTimezone(reminder.timezone)) {
            return false;
        }
        
        // Validate text length
        if (reminder.text.length > 500) {
            return false;
        }
        
        return true;
    }
    
    handleReminderSubmit(formData) {
        try {
            if (formData.id) {
                // Update existing reminder
                return this.updateReminder(formData.id, {
                    text: formData.text,
                    date: formData.date,
                    time: formData.time,
                    timezone: formData.timezone
                });
            } else {
                // Create new reminder
                return this.createReminder(formData);
            }
        } catch (error) {
            console.error('Error handling reminder submit:', error);
            throw error;
        }
    }
    
    editReminder(reminderData) {
        try {
            return this.updateReminder(reminderData.id, reminderData);
        } catch (error) {
            console.error('Error editing reminder:', error);
            throw error;
        }
    }
    
    // Get reminders grouped by date for calendar display
    getRemindersGroupedByDate() {
        const grouped = {};
        
        this.reminders.forEach(reminder => {
            if (!grouped[reminder.date]) {
                grouped[reminder.date] = [];
            }
            grouped[reminder.date].push(reminder);
        });
        
        return grouped;
    }
    
    // Convert reminder time to different timezone
    convertReminderTime(reminder, targetTimezone) {
        if (!this.timezoneManager) {
            return null;
        }
        
        try {
            const DateTime = luxon.DateTime;
            
            // Create datetime in original timezone
            const originalDateTime = DateTime.fromISO(
                `${reminder.date}T${reminder.time}:00`,
                { zone: reminder.timezone }
            );
            
            // Convert to target timezone
            const convertedDateTime = originalDateTime.setZone(targetTimezone);
            
            return {
                date: convertedDateTime.toISODate(),
                time: convertedDateTime.toFormat('HH:mm'),
                timezone: targetTimezone,
                originalTime: reminder.time,
                originalTimezone: reminder.timezone
            };
        } catch (error) {
            console.error('Error converting reminder time:', error);
            return null;
        }
    }
    
    // Get statistics about reminders
    getStatistics() {
        const now = new Date();
        const currentDate = now.toISOString().split('T')[0];
        
        const upcoming = this.getUpcomingReminders().length;
        const past = this.getPastReminders().length;
        const today = this.getRemindersByDate(currentDate).length;
        
        return {
            total: this.reminders.length,
            upcoming,
            past,
            today
        };
    }
    
    // Export reminders to JSON
    exportReminders() {
        return JSON.stringify(this.reminders, null, 2);
    }
    
    // Import reminders from JSON
    importReminders(jsonData) {
        try {
            const importedReminders = JSON.parse(jsonData);
            
            // Validate each reminder
            const validReminders = importedReminders.filter(r => this.validateReminder(r));
            
            // Add to existing reminders (with new IDs to avoid conflicts)
            validReminders.forEach(reminder => {
                const newReminder = {
                    ...reminder,
                    id: this.generateId(),
                    createdAt: new Date().toISOString(),
                    updatedAt: new Date().toISOString()
                };
                this.reminders.push(newReminder);
            });
            
            this.sortReminders();
            this.saveReminders();
            
            return {
                imported: validReminders.length,
                skipped: importedReminders.length - validReminders.length
            };
        } catch (error) {
            console.error('Error importing reminders:', error);
            throw new Error('Invalid JSON data');
        }
    }
    
    // Clear all reminders
    clearAllReminders() {
        const count = this.reminders.length;
        this.reminders = [];
        this.saveReminders();
        
        document.dispatchEvent(new CustomEvent('remindersCleared', {
            detail: { count }
        }));
        
        return count;
    }
}