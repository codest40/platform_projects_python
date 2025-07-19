// CalendarRender.js - Handles calendar grid rendering
export class CalendarRender {
    constructor() {
        this.currentDate = new Date();
        this.selectedDate = null;
        this.reminderManager = null;
        this.container = null;
        this.monthDisplay = null;
    }
    
    init(reminderManager, containerId = 'calendar-grid') {
        this.reminderManager = reminderManager;
        this.container = document.getElementById(containerId);
        this.monthDisplay = document.getElementById('current-month');
        
        if (!this.container) {
            console.warn('Calendar container not found:', containerId);
            return;
        }
        
        this.setupEventListeners();
        this.render();
    }
    
    setupEventListeners() {
        // Listen for reminder changes
        document.addEventListener('reminderCreated', () => this.render());
        document.addEventListener('reminderUpdated', () => this.render());
        document.addEventListener('reminderDeleted', () => this.render());
        
        // Listen for date selection
        document.addEventListener('dateSelected', (e) => {
            this.selectDate(e.detail.date);
        });
        
        // Calendar day clicks
        this.container.addEventListener('click', (e) => {
            const dayElement = e.target.closest('.calendar-day');
            if (dayElement) {
                const date = dayElement.getAttribute('data-date');
                if (date) {
                    this.handleDayClick(date, dayElement);
                }
            }
        });
    }
    
    render() {
        if (!this.container) return;
        
        this.container.innerHTML = '';
        this.updateMonthDisplay();
        
        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth();
        
        // Get first day of month and how many days
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const daysInMonth = lastDay.getDate();
        const startingDayOfWeek = firstDay.getDay();
        
        // Get previous month's last days
        const prevMonth = new Date(year, month, 0);
        const daysInPrevMonth = prevMonth.getDate();
        
        // Create calendar grid
        let dayCount = 1;
        let nextMonthDay = 1;
        
        // 6 rows × 7 days = 42 cells
        for (let week = 0; week < 6; week++) {
            for (let day = 0; day < 7; day++) {
                const cellIndex = week * 7 + day;
                let dayElement;
                
                if (cellIndex < startingDayOfWeek) {
                    // Previous month days
                    const prevMonthDate = daysInPrevMonth - (startingDayOfWeek - cellIndex - 1);
                    dayElement = this.createDayElement(
                        prevMonthDate, 
                        year, 
                        month - 1,
                        true // other month
                    );
                } else if (dayCount <= daysInMonth) {
                    // Current month days
                    dayElement = this.createDayElement(
                        dayCount,
                        year,
                        month,
                        false
                    );
                    dayCount++;
                } else {
                    // Next month days
                    dayElement = this.createDayElement(
                        nextMonthDay,
                        year,
                        month + 1,
                        true // other month
                    );
                    nextMonthDay++;
                }
                
                this.container.appendChild(dayElement);
            }
            
            // Don't render more weeks if we've finished the month and next month start
            if (dayCount > daysInMonth && nextMonthDay > 7) {
                break;
            }
        }
    }
    
    createDayElement(day, year, month, isOtherMonth = false) {
        const dayElement = document.createElement('div');
        dayElement.className = 'calendar-day';
        
        // Handle month overflow/underflow
        let actualYear = year;
        let actualMonth = month;
        
        if (month < 0) {
            actualMonth = 11;
            actualYear = year - 1;
        } else if (month > 11) {
            actualMonth = 0;
            actualYear = year + 1;
        }
        
        const dateStr = this.formatDateString(actualYear, actualMonth, day);
        dayElement.setAttribute('data-date', dateStr);
        
        if (isOtherMonth) {
            dayElement.classList.add('other-month');
        }
        
        // Check if it's today
        const today = new Date();
        if (actualYear === today.getFullYear() && 
            actualMonth === today.getMonth() && 
            day === today.getDate()) {
            dayElement.classList.add('today');
        }
        
        // Check if it's selected
        if (this.selectedDate === dateStr) {
            dayElement.classList.add('selected');
        }
        
        // Get reminders for this date
        const reminders = this.reminderManager ? 
            this.reminderManager.getRemindersByDate(dateStr) : [];
        
        // Create day content
        dayElement.innerHTML = `
            <div class="day-number">${day}</div>
            <div class="day-reminders">
                ${reminders.slice(0, 3).map(reminder => `
                    <div class="reminder-dot" title="${this.escapeHtml(reminder.text)} at ${reminder.time}">
                        ${reminder.text.substring(0, 15)}${reminder.text.length > 15 ? '...' : ''}
                    </div>
                `).join('')}
                ${reminders.length > 3 ? `
                    <div class="reminder-dot more-reminders" title="${reminders.length - 3} more reminders">
                        +${reminders.length - 3} more
                    </div>
                ` : ''}
            </div>
        `;
        
        return dayElement;
    }
    
    handleDayClick(date, dayElement) {
        // Remove previous selection
        this.container.querySelectorAll('.calendar-day.selected').forEach(el => {
            el.classList.remove('selected');
        });
        
        // Add selection to clicked day
        dayElement.classList.add('selected');
        this.selectedDate = date;
        
        // Dispatch event
        document.dispatchEvent(new CustomEvent('calendarDaySelected', {
            detail: { 
                date, 
                reminders: this.reminderManager ? 
                    this.reminderManager.getRemindersByDate(date) : [] 
            }
        }));
    }
    
    updateMonthDisplay() {
        if (!this.monthDisplay) return;
        
        const monthNames = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ];
        
        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth();
        
        this.monthDisplay.textContent = `${monthNames[month]} ${year}`;
    }
    
    formatDateString(year, month, day) {
        return `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    }
    
    setCurrentDate(date) {
        this.currentDate = new Date(date);
        this.render();
    }
    
    getCurrentDate() {
        return new Date(this.currentDate);
    }
    
    nextMonth() {
        this.currentDate.setMonth(this.currentDate.getMonth() + 1);
        this.render();
    }
    
    previousMonth() {
        this.currentDate.setMonth(this.currentDate.getMonth() - 1);
        this.render();
    }
    
    goToToday() {
        this.currentDate = new Date();
        this.selectedDate = this.formatDateString(
            this.currentDate.getFullYear(),
            this.currentDate.getMonth(),
            this.currentDate.getDate()
        );
        this.render();
    }
    
    goToDate(year, month, day) {
        this.currentDate = new Date(year, month, day);
        this.selectedDate = this.formatDateString(year, month, day);
        this.render();
    }
    
    selectDate(dateStr) {
        this.selectedDate = dateStr;
        
        // Parse date and navigate to that month if needed
        const [year, month, day] = dateStr.split('-').map(Number);
        const targetDate = new Date(year, month - 1, day);
        
        if (targetDate.getFullYear() !== this.currentDate.getFullYear() ||
            targetDate.getMonth() !== this.currentDate.getMonth()) {
            this.setCurrentDate(targetDate);
        } else {
            this.render();
        }
    }
    
    getSelectedDate() {
        return this.selectedDate;
    }
    
    clearSelection() {
        this.selectedDate = null;
        this.container.querySelectorAll('.calendar-day.selected').forEach(el => {
            el.classList.remove('selected');
        });
    }
    
    highlightDates(dates) {
        // Add special highlighting for specific dates
        dates.forEach(date => {
            const dayElement = this.container.querySelector(`[data-date="${date}"]`);
            if (dayElement) {
                dayElement.classList.add('highlighted');
            }
        });
    }
    
    removeHighlights() {
        this.container.querySelectorAll('.calendar-day.highlighted').forEach(el => {
            el.classList.remove('highlighted');
        });
    }
    
    getDatesWithReminders() {
        if (!this.reminderManager) return [];
        
        const remindersGrouped = this.reminderManager.getRemindersGroupedByDate();
        return Object.keys(remindersGrouped);
    }
    
    getMonthDateRange() {
        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth();
        
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        
        return {
            start: this.formatDateString(year, month, 1),
            end: this.formatDateString(year, month, lastDay.getDate()),
            firstDay: firstDay.getDay(),
            daysInMonth: lastDay.getDate()
        };
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // Export calendar data
    exportCalendarData() {
        const dateRange = this.getMonthDateRange();
        const remindersInMonth = [];
        
        if (this.reminderManager) {
            const allReminders = this.reminderManager.getAllReminders();
            remindersInMonth.push(...allReminders.filter(reminder => 
                reminder.date >= dateRange.start && reminder.date <= dateRange.end
            ));
        }
        
        return {
            month: this.currentDate.getMonth(),
            year: this.currentDate.getFullYear(),
            selectedDate: this.selectedDate,
            reminders: remindersInMonth,
            dateRange
        };
    }
}

// Add CSS for calendar rendering
const style = document.createElement('style');
style.textContent = `
    .calendar-day.highlighted {
        background: var(--color-accent) !important;
        color: white;
    }
    
    .calendar-day.highlighted .day-reminders {
        opacity: 0.9;
    }
    
    .reminder-dot.more-reminders {
        background: var(--color-warning);
        color: white;
        font-size: var(--font-size-xs);
        padding: 2px var(--space-xs);
        border-radius: var(--radius-sm);
        text-align: center;
    }
    
    .calendar-day:hover .reminder-dot {
        opacity: 1;
        transform: scale(1.05);
    }
    
    .calendar-day.today {
        position: relative;
    }
    
    .calendar-day.today::before {
        content: '';
        position: absolute;
        top: 2px;
        right: 2px;
        width: 8px;
        height: 8px;
        background: var(--color-success);
        border-radius: 50%;
        z-index: 1;
    }
`;
document.head.appendChild(style);