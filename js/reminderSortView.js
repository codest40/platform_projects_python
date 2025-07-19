// ReminderSortView.js - Handles reminder display and sorting
export class ReminderSortView {
    constructor() {
        this.reminderManager = null;
        this.container = null;
        this.sortBy = 'date'; // date, time, text, timezone
        this.sortOrder = 'asc'; // asc, desc
        this.filterBy = 'all'; // all, upcoming, past, today
        this.groupBy = 'date'; // date, timezone, none
        this.itemsPerPage = 10;
        this.currentPage = 1;
    }
    
    init(reminderManager, containerId = 'reminders-list') {
        this.reminderManager = reminderManager;
        this.container = document.getElementById(containerId);
        
        if (!this.container) {
            console.warn('Reminder container not found:', containerId);
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
        document.addEventListener('remindersCleared', () => this.render());
        
        // Filter controls
        document.addEventListener('change', (e) => {
            if (e.target.id === 'reminder-filter') {
                this.setFilter(e.target.value);
            } else if (e.target.id === 'reminder-sort') {
                this.setSortBy(e.target.value);
            } else if (e.target.id === 'reminder-group') {
                this.setGroupBy(e.target.value);
            }
        });
        
        // Sort order toggle
        document.addEventListener('click', (e) => {
            if (e.target.id === 'sort-order-toggle') {
                this.toggleSortOrder();
            }
        });
    }
    
    render() {
        if (!this.container || !this.reminderManager) return;
        
        const reminders = this.getFilteredReminders();
        const sortedReminders = this.sortReminders(reminders);
        const groupedReminders = this.groupReminders(sortedReminders);
        
        this.container.innerHTML = '';
        
        if (Object.keys(groupedReminders).length === 0) {
            this.renderEmptyState();
            return;
        }
        
        this.renderGroups(groupedReminders);
        this.renderPagination(sortedReminders.length);
    }
    
    renderGroups(groupedReminders) {
        Object.entries(groupedReminders).forEach(([groupKey, reminders]) => {
            if (this.groupBy !== 'none') {
                this.renderGroupHeader(groupKey);
            }
            
            reminders.forEach(reminder => {
                this.renderReminderItem(reminder);
            });
        });
    }
    
    renderGroupHeader(groupKey) {
        const header = document.createElement('div');
        header.className = 'reminder-group-header';
        
        let displayText = groupKey;
        
        if (this.groupBy === 'date') {
            const date = new Date(groupKey + 'T00:00:00');
            displayText = date.toLocaleDateString('en-US', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
            
            // Add relative date info
            const today = new Date().toISOString().split('T')[0];
            if (groupKey === today) {
                displayText += ' (Today)';
            } else {
                const diffTime = new Date(groupKey) - new Date(today);
                const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
                
                if (diffDays === 1) {
                    displayText += ' (Tomorrow)';
                } else if (diffDays === -1) {
                    displayText += ' (Yesterday)';
                } else if (diffDays > 0) {
                    displayText += ` (in ${diffDays} days)`;
                } else if (diffDays < 0) {
                    displayText += ` (${Math.abs(diffDays)} days ago)`;
                }
            }
        }
        
        header.innerHTML = `
            <h4 class="group-title">${displayText}</h4>
            <div class="group-count">${groupedReminders[groupKey].length} reminder${groupedReminders[groupKey].length === 1 ? '' : 's'}</div>
        `;
        
        this.container.appendChild(header);
    }
    
    renderReminderItem(reminder) {
        const item = document.createElement('div');
        item.className = 'reminder-item';
        item.setAttribute('data-reminder-id', reminder.id);
        
        // Format datetime display
        const dateTime = this.formatDateTime(reminder);
        const relativeTime = this.getRelativeTime(reminder);
        
        item.innerHTML = `
            <div class="reminder-content">
                <div class="reminder-header">
                    <div class="reminder-text">${this.escapeHtml(reminder.text)}</div>
                    <div class="reminder-actions">
                        <button class="edit-btn" data-id="${reminder.id}" title="Edit reminder">✏️</button>
                        <button class="delete-btn" data-id="${reminder.id}" title="Delete reminder">🗑️</button>
                    </div>
                </div>
                <div class="reminder-meta">
                    <div class="reminder-datetime">
                        <span class="date-time">${dateTime}</span>
                        <span class="relative-time">${relativeTime}</span>
                    </div>
                    <div class="reminder-timezone">${reminder.timezone}</div>
                </div>
            </div>
        `;
        
        // Add event listeners
        this.addReminderEventListeners(item, reminder);
        
        this.container.appendChild(item);
    }
    
    addReminderEventListeners(item, reminder) {
        // Edit button
        const editBtn = item.querySelector('.edit-btn');
        editBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.editReminder(reminder);
        });
        
        // Delete button
        const deleteBtn = item.querySelector('.delete-btn');
        deleteBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.deleteReminder(reminder);
        });
        
        // Click to view details
        item.addEventListener('click', () => {
            this.showReminderDetails(reminder);
        });
    }
    
    renderEmptyState() {
        const emptyState = document.createElement('div');
        emptyState.className = 'reminder-empty-state';
        
        let message = 'No reminders found.';
        
        switch (this.filterBy) {
            case 'upcoming':
                message = 'No upcoming reminders.';
                break;
            case 'past':
                message = 'No past reminders.';
                break;
            case 'today':
                message = 'No reminders for today.';
                break;
        }
        
        emptyState.innerHTML = `
            <div class="empty-state-content">
                <div class="empty-state-icon">📅</div>
                <div class="empty-state-message">${message}</div>
                <button class="btn-primary" onclick="document.getElementById('add-reminder-btn').click()">
                    Add your first reminder
                </button>
            </div>
        `;
        
        this.container.appendChild(emptyState);
    }
    
    getFilteredReminders() {
        let reminders = this.reminderManager.getAllReminders();
        
        switch (this.filterBy) {
            case 'upcoming':
                reminders = this.reminderManager.getUpcomingReminders(1000);
                break;
            case 'past':
                reminders = this.reminderManager.getPastReminders(1000);
                break;
            case 'today':
                const today = new Date().toISOString().split('T')[0];
                reminders = this.reminderManager.getRemindersByDate(today);
                break;
        }
        
        return reminders;
    }
    
    sortReminders(reminders) {
        return [...reminders].sort((a, b) => {
            let comparison = 0;
            
            switch (this.sortBy) {
                case 'date':
                    comparison = a.date.localeCompare(b.date) || a.time.localeCompare(b.time);
                    break;
                case 'time':
                    comparison = a.time.localeCompare(b.time);
                    break;
                case 'text':
                    comparison = a.text.localeCompare(b.text);
                    break;
                case 'timezone':
                    comparison = a.timezone.localeCompare(b.timezone);
                    break;
                case 'created':
                    comparison = new Date(a.createdAt) - new Date(b.createdAt);
                    break;
            }
            
            return this.sortOrder === 'desc' ? -comparison : comparison;
        });
    }
    
    groupReminders(reminders) {
        if (this.groupBy === 'none') {
            return { 'all': reminders };
        }
        
        const grouped = {};
        
        reminders.forEach(reminder => {
            let groupKey;
            
            switch (this.groupBy) {
                case 'date':
                    groupKey = reminder.date;
                    break;
                case 'timezone':
                    groupKey = reminder.timezone;
                    break;
                default:
                    groupKey = 'all';
            }
            
            if (!grouped[groupKey]) {
                grouped[groupKey] = [];
            }
            grouped[groupKey].push(reminder);
        });
        
        return grouped;
    }
    
    formatDateTime(reminder) {
        const date = new Date(reminder.date + 'T' + reminder.time + ':00');
        return date.toLocaleString('en-US', {
            weekday: 'short',
            month: 'short',
            day: 'numeric',
            hour: 'numeric',
            minute: '2-digit',
            hour12: true
        });
    }
    
    getRelativeTime(reminder) {
        const reminderDate = new Date(reminder.date + 'T' + reminder.time + ':00');
        const now = new Date();
        const diffMs = reminderDate - now;
        const diffMinutes = Math.round(diffMs / (1000 * 60));
        
        if (diffMs < 0) {
            const absDiffMinutes = Math.abs(diffMinutes);
            if (absDiffMinutes < 60) {
                return `${absDiffMinutes} min ago`;
            } else if (absDiffMinutes < 1440) {
                return `${Math.round(absDiffMinutes / 60)} hr ago`;
            } else {
                return `${Math.round(absDiffMinutes / 1440)} days ago`;
            }
        } else {
            if (diffMinutes < 60) {
                return `in ${diffMinutes} min`;
            } else if (diffMinutes < 1440) {
                return `in ${Math.round(diffMinutes / 60)} hr`;
            } else {
                return `in ${Math.round(diffMinutes / 1440)} days`;
            }
        }
    }
    
    setFilter(filter) {
        this.filterBy = filter;
        this.currentPage = 1;
        this.render();
    }
    
    setSortBy(sortBy) {
        this.sortBy = sortBy;
        this.render();
    }
    
    setGroupBy(groupBy) {
        this.groupBy = groupBy;
        this.render();
    }
    
    toggleSortOrder() {
        this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
        this.render();
    }
    
    editReminder(reminder) {
        document.dispatchEvent(new CustomEvent('openReminderModal', {
            detail: { mode: 'edit', reminder }
        }));
    }
    
    deleteReminder(reminder) {
        if (confirm(`Delete reminder: "${reminder.text}"?`)) {
            this.reminderManager.deleteReminder(reminder.id);
        }
    }
    
    showReminderDetails(reminder) {
        // Create a detailed view modal or expand the item
        console.log('Show reminder details:', reminder);
    }
    
    renderPagination(totalItems) {
        // Implementation would go here for pagination
        // For now, we'll show all items
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Add CSS for reminder sort view
const style = document.createElement('style');
style.textContent = `
    .reminder-group-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: var(--space-md) 0;
        margin: var(--space-lg) 0 var(--space-md) 0;
        border-bottom: 2px solid var(--color-border);
    }
    
    .group-title {
        font-size: var(--font-size-lg);
        font-weight: 600;
        color: var(--color-text-primary);
        margin: 0;
    }
    
    .group-count {
        font-size: var(--font-size-sm);
        color: var(--color-text-muted);
        background: var(--color-surface);
        padding: var(--space-xs) var(--space-sm);
        border-radius: var(--radius-sm);
    }
    
    .reminder-item {
        background: var(--color-surface);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-lg);
        padding: var(--space-lg);
        margin-bottom: var(--space-md);
        cursor: pointer;
        transition: all var(--transition-fast);
    }
    
    .reminder-item:hover {
        background: var(--color-surface-elevated);
        border-color: var(--color-primary);
        box-shadow: var(--glass-shadow);
    }
    
    .reminder-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: var(--space-sm);
    }
    
    .reminder-text {
        font-weight: 600;
        color: var(--color-text-primary);
        flex: 1;
        margin-right: var(--space-md);
        line-height: 1.4;
    }
    
    .reminder-actions {
        display: flex;
        gap: var(--space-sm);
    }
    
    .edit-btn,
    .delete-btn {
        background: none;
        border: none;
        cursor: pointer;
        padding: var(--space-xs);
        border-radius: var(--radius-sm);
        transition: all var(--transition-fast);
        font-size: var(--font-size-sm);
    }
    
    .edit-btn:hover {
        background: var(--color-primary);
    }
    
    .delete-btn:hover {
        background: var(--color-danger);
    }
    
    .reminder-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: var(--font-size-sm);
        color: var(--color-text-secondary);
    }
    
    .reminder-datetime {
        display: flex;
        flex-direction: column;
        gap: var(--space-xs);
    }
    
    .date-time {
        font-weight: 500;
    }
    
    .relative-time {
        color: var(--color-text-muted);
        font-size: var(--font-size-xs);
    }
    
    .reminder-timezone {
        background: var(--color-background);
        padding: var(--space-xs) var(--space-sm);
        border-radius: var(--radius-sm);
        font-weight: 500;
        font-size: var(--font-size-xs);
    }
    
    .reminder-empty-state {
        text-align: center;
        padding: var(--space-2xl);
    }
    
    .empty-state-content {
        max-width: 300px;
        margin: 0 auto;
    }
    
    .empty-state-icon {
        font-size: 3rem;
        margin-bottom: var(--space-lg);
    }
    
    .empty-state-message {
        font-size: var(--font-size-lg);
        color: var(--color-text-muted);
        margin-bottom: var(--space-xl);
    }
    
    @media (max-width: 768px) {
        .reminder-header {
            flex-direction: column;
            gap: var(--space-sm);
        }
        
        .reminder-meta {
            flex-direction: column;
            align-items: flex-start;
            gap: var(--space-sm);
        }
        
        .reminder-actions {
            align-self: flex-end;
        }
    }
`;
document.head.appendChild(style);