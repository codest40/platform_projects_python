// CalendarNavigation.js - Handles calendar navigation controls
export class CalendarNavigation {
    constructor() {
        this.calendarRender = null;
        this.reminderManager = null;
        this.modal = null;
        this.form = null;
        this.editingReminder = null;
    }
    
    init(calendarRender, reminderManager) {
        this.calendarRender = calendarRender;
        this.reminderManager = reminderManager;
        this.modal = document.getElementById('reminder-modal');
        this.form = document.getElementById('reminder-form');
        
        this.setupEventListeners();
        this.setupModal();
        this.populateTimezoneSelector();
    }
    
    setupEventListeners() {
        // Navigation buttons
        const prevBtn = document.getElementById('prev-month');
        const nextBtn = document.getElementById('next-month');
        const todayBtn = document.getElementById('today-btn');
        
        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                this.calendarRender.previousMonth();
            });
        }
        
        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                this.calendarRender.nextMonth();
            });
        }
        
        if (todayBtn) {
            todayBtn.addEventListener('click', () => {
                this.calendarRender.goToToday();
            });
        }
        
        // Add reminder button
        const addBtn = document.getElementById('add-reminder-btn');
        if (addBtn) {
            addBtn.addEventListener('click', () => {
                this.openReminderModal();
            });
        }
        
        // Calendar day selection
        document.addEventListener('calendarDaySelected', (e) => {
            this.handleDaySelected(e.detail);
        });
        
        // Listen for modal open requests
        document.addEventListener('openReminderModal', (e) => {
            if (e.detail.mode === 'edit') {
                this.openReminderModal(e.detail.reminder);
            } else {
                this.openReminderModal();
            }
        });
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (!this.modal.classList.contains('show')) {
                this.handleKeyboardNavigation(e);
            }
        });
    }
    
    setupModal() {
        if (!this.modal || !this.form) return;
        
        // Close modal buttons
        const closeBtn = document.getElementById('close-modal');
        const cancelBtn = document.getElementById('cancel-btn');
        
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                this.closeReminderModal();
            });
        }
        
        if (cancelBtn) {
            cancelBtn.addEventListener('click', () => {
                this.closeReminderModal();
            });
        }
        
        // Click outside to close
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.closeReminderModal();
            }
        });
        
        // Form submission
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleFormSubmit();
        });
        
        // Escape key to close
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.modal.classList.contains('show')) {
                this.closeReminderModal();
            }
        });
    }
    
    populateTimezoneSelector() {
        const timezoneSelect = document.getElementById('reminder-timezone');
        if (!timezoneSelect || !this.reminderManager.timezoneManager) return;
        
        const timezones = this.reminderManager.timezoneManager.getAvailableTimezones();
        
        timezoneSelect.innerHTML = '<option value="">Select timezone...</option>';
        
        timezones.forEach(tz => {
            const option = document.createElement('option');
            option.value = tz.timezone;
            option.textContent = tz.display;
            timezoneSelect.appendChild(option);
        });
        
        // Set default to user's timezone if available
        try {
            const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
            if (timezones.find(tz => tz.timezone === userTimezone)) {
                timezoneSelect.value = userTimezone;
            }
        } catch (error) {
            console.warn('Could not detect user timezone:', error);
        }
    }
    
    openReminderModal(reminder = null) {
        if (!this.modal || !this.form) return;
        
        this.editingReminder = reminder;
        
        // Reset form
        this.form.reset();
        
        // Populate form if editing
        if (reminder) {
            document.getElementById('reminder-text').value = reminder.text;
            document.getElementById('reminder-date').value = reminder.date;
            document.getElementById('reminder-time').value = reminder.time;
            document.getElementById('reminder-timezone').value = reminder.timezone;
            
            // Update modal title
            const modalTitle = this.modal.querySelector('.modal-title');
            if (modalTitle) {
                modalTitle.textContent = 'Edit Reminder';
            }
        } else {
            // Set default date to selected date or today
            const defaultDate = this.calendarRender.getSelectedDate() || 
                new Date().toISOString().split('T')[0];
            document.getElementById('reminder-date').value = defaultDate;
            
            // Set default time to next hour
            const now = new Date();
            now.setHours(now.getHours() + 1, 0, 0, 0);
            document.getElementById('reminder-time').value = 
                now.toTimeString().slice(0, 5);
            
            // Update modal title
            const modalTitle = this.modal.querySelector('.modal-title');
            if (modalTitle) {
                modalTitle.textContent = 'Add Reminder';
            }
        }
        
        // Show modal
        this.modal.classList.add('show');
        
        // Focus on text input
        setTimeout(() => {
            document.getElementById('reminder-text').focus();
        }, 100);
    }
    
    closeReminderModal() {
        if (!this.modal) return;
        
        this.modal.classList.remove('show');
        this.editingReminder = null;
        
        // Reset form
        if (this.form) {
            this.form.reset();
        }
    }
    
    handleFormSubmit() {
        const formData = new FormData(this.form);
        
        const reminderData = {
            text: formData.get('reminder-text').trim(),
            date: formData.get('reminder-date'),
            time: formData.get('reminder-time'),
            timezone: formData.get('reminder-timezone')
        };
        
        // Validate form data
        if (!this.validateFormData(reminderData)) {
            return;
        }
        
        try {
            if (this.editingReminder) {
                // Update existing reminder
                reminderData.id = this.editingReminder.id;
                this.reminderManager.updateReminder(this.editingReminder.id, reminderData);
                this.showMessage('Reminder updated successfully', 'success');
            } else {
                // Create new reminder
                this.reminderManager.createReminder(reminderData);
                this.showMessage('Reminder created successfully', 'success');
            }
            
            this.closeReminderModal();
        } catch (error) {
            console.error('Error saving reminder:', error);
            this.showMessage('Error saving reminder: ' + error.message, 'error');
        }
    }
    
    validateFormData(data) {
        if (!data.text) {
            this.showMessage('Please enter reminder text', 'error');
            return false;
        }
        
        if (!data.date) {
            this.showMessage('Please select a date', 'error');
            return false;
        }
        
        if (!data.time) {
            this.showMessage('Please select a time', 'error');
            return false;
        }
        
        if (!data.timezone) {
            this.showMessage('Please select a timezone', 'error');
            return false;
        }
        
        // Check if date is not too far in the past
        const reminderDate = new Date(data.date + 'T' + data.time);
        const now = new Date();
        const daysDiff = (reminderDate - now) / (1000 * 60 * 60 * 24);
        
        if (daysDiff < -7) {
            this.showMessage('Reminder date cannot be more than a week in the past', 'error');
            return false;
        }
        
        return true;
    }
    
    handleDaySelected(detail) {
        console.log('Day selected:', detail.date, 'Reminders:', detail.reminders.length);
        
        // Could open a day view or show reminders for the selected day
        if (detail.reminders.length > 0) {
            this.showDayReminders(detail.date, detail.reminders);
        }
    }
    
    showDayReminders(date, reminders) {
        // Create a simple popup showing reminders for the day
        const popup = document.createElement('div');
        popup.className = 'day-reminders-popup';
        popup.innerHTML = `
            <div class="popup-content">
                <div class="popup-header">
                    <h3>Reminders for ${this.formatDate(date)}</h3>
                    <button class="popup-close">×</button>
                </div>
                <div class="popup-body">
                    ${reminders.map(reminder => `
                        <div class="popup-reminder">
                            <div class="popup-reminder-text">${this.escapeHtml(reminder.text)}</div>
                            <div class="popup-reminder-time">${reminder.time} (${reminder.timezone})</div>
                        </div>
                    `).join('')}
                </div>
                <div class="popup-actions">
                    <button class="btn-primary" onclick="document.getElementById('add-reminder-btn').click()">
                        Add Reminder
                    </button>
                </div>
            </div>
        `;
        
        // Add to body
        document.body.appendChild(popup);
        
        // Close handlers
        const closeBtn = popup.querySelector('.popup-close');
        closeBtn.addEventListener('click', () => {
            popup.remove();
        });
        
        popup.addEventListener('click', (e) => {
            if (e.target === popup) {
                popup.remove();
            }
        });
        
        // Auto remove after 10 seconds
        setTimeout(() => {
            if (popup.parentNode) {
                popup.remove();
            }
        }, 10000);
    }
    
    handleKeyboardNavigation(e) {
        // Arrow key navigation for calendar
        if (!e.target.closest('.calendar-grid')) return;
        
        const selectedDate = this.calendarRender.getSelectedDate();
        if (!selectedDate) return;
        
        const [year, month, day] = selectedDate.split('-').map(Number);
        let newDate = new Date(year, month - 1, day);
        
        switch (e.key) {
            case 'ArrowLeft':
                e.preventDefault();
                newDate.setDate(newDate.getDate() - 1);
                break;
            case 'ArrowRight':
                e.preventDefault();
                newDate.setDate(newDate.getDate() + 1);
                break;
            case 'ArrowUp':
                e.preventDefault();
                newDate.setDate(newDate.getDate() - 7);
                break;
            case 'ArrowDown':
                e.preventDefault();
                newDate.setDate(newDate.getDate() + 7);
                break;
            case 'Enter':
                e.preventDefault();
                this.openReminderModal();
                return;
            default:
                return;
        }
        
        const newDateStr = this.calendarRender.formatDateString(
            newDate.getFullYear(),
            newDate.getMonth(),
            newDate.getDate()
        );
        
        this.calendarRender.selectDate(newDateStr);
    }
    
    formatDate(dateStr) {
        const date = new Date(dateStr + 'T00:00:00');
        return date.toLocaleDateString('en-US', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
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
            z-index: 1001;
            animation: slideIn 0.3s ease;
        `;
        
        if (type === 'error') {
            toast.style.borderColor = 'var(--color-danger)';
            toast.style.backgroundColor = 'var(--color-danger)';
            toast.style.color = 'white';
        } else if (type === 'success') {
            toast.style.borderColor = 'var(--color-success)';
            toast.style.backgroundColor = 'var(--color-success)';
            toast.style.color = 'white';
        }
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
    
    // Jump to specific month/year
    jumpToDate(year, month) {
        this.calendarRender.setCurrentDate(new Date(year, month, 1));
    }
    
    // Get current view info
    getCurrentView() {
        const currentDate = this.calendarRender.getCurrentDate();
        return {
            year: currentDate.getFullYear(),
            month: currentDate.getMonth(),
            selectedDate: this.calendarRender.getSelectedDate()
        };
    }
}

// Add CSS for day reminders popup
const style = document.createElement('style');
style.textContent = `
    .day-reminders-popup {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
        animation: fadeIn 0.3s ease;
    }
    
    .popup-content {
        background: var(--color-background);
        border-radius: var(--radius-xl);
        max-width: 400px;
        width: 90%;
        max-height: 80vh;
        overflow-y: auto;
        border: 1px solid var(--color-border);
        box-shadow: var(--glass-shadow);
    }
    
    .popup-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: var(--space-xl);
        border-bottom: 1px solid var(--color-border);
    }
    
    .popup-header h3 {
        margin: 0;
        color: var(--color-text-primary);
    }
    
    .popup-close {
        background: none;
        border: none;
        font-size: var(--font-size-xl);
        cursor: pointer;
        color: var(--color-text-muted);
        padding: var(--space-xs);
        border-radius: var(--radius-sm);
        transition: all var(--transition-fast);
    }
    
    .popup-close:hover {
        background: var(--color-surface);
        color: var(--color-text-primary);
    }
    
    .popup-body {
        padding: var(--space-xl);
    }
    
    .popup-reminder {
        padding: var(--space-md);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-md);
        margin-bottom: var(--space-md);
        background: var(--color-surface);
    }
    
    .popup-reminder:last-child {
        margin-bottom: 0;
    }
    
    .popup-reminder-text {
        font-weight: 600;
        color: var(--color-text-primary);
        margin-bottom: var(--space-xs);
    }
    
    .popup-reminder-time {
        font-size: var(--font-size-sm);
        color: var(--color-text-secondary);
    }
    
    .popup-actions {
        padding: var(--space-xl);
        border-top: 1px solid var(--color-border);
        text-align: center;
    }
`;
document.head.appendChild(style);