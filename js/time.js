// Time.js - Handles timezone operations using Luxon
export class TimezoneManager {
    constructor() {
        this.timezoneData = null;
        this.DateTime = luxon.DateTime;
    }
    
    async loadTimezoneData() {
        try {
            const response = await fetch('json/time_list.json');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            this.timezoneData = await response.json();
            console.log('Timezone data loaded:', this.timezoneData.length, 'countries');
        } catch (error) {
            console.error('Failed to load timezone data:', error);
            // Fallback to basic timezone data
            this.timezoneData = this.getFallbackTimezoneData();
        }
    }
    
    getFallbackTimezoneData() {
        return [
            {
                code: 'us',
                name: 'United States',
                emoji: '🇺🇸',
                cities: [
                    { name: 'New York', timezone: 'America/New_York' },
                    { name: 'Los Angeles', timezone: 'America/Los_Angeles' },
                    { name: 'Chicago', timezone: 'America/Chicago' },
                    { name: 'Denver', timezone: 'America/Denver' }
                ]
            },
            {
                code: 'gb',
                name: 'United Kingdom',
                emoji: '🇬🇧',
                cities: [
                    { name: 'London', timezone: 'Europe/London' },
                    { name: 'Edinburgh', timezone: 'Europe/London' },
                    { name: 'Cardiff', timezone: 'Europe/London' }
                ]
            },
            {
                code: 'jp',
                name: 'Japan',
                emoji: '🇯🇵',
                cities: [
                    { name: 'Tokyo', timezone: 'Asia/Tokyo' },
                    { name: 'Osaka', timezone: 'Asia/Tokyo' },
                    { name: 'Kyoto', timezone: 'Asia/Tokyo' }
                ]
            },
            {
                code: 'au',
                name: 'Australia',
                emoji: '🇦🇺',
                cities: [
                    { name: 'Sydney', timezone: 'Australia/Sydney' },
                    { name: 'Melbourne', timezone: 'Australia/Melbourne' },
                    { name: 'Perth', timezone: 'Australia/Perth' }
                ]
            },
            {
                code: 'de',
                name: 'Germany',
                emoji: '🇩🇪',
                cities: [
                    { name: 'Berlin', timezone: 'Europe/Berlin' },
                    { name: 'Munich', timezone: 'Europe/Berlin' },
                    { name: 'Hamburg', timezone: 'Europe/Berlin' }
                ]
            },
            {
                code: 'fr',
                name: 'France',
                emoji: '🇫🇷',
                cities: [
                    { name: 'Paris', timezone: 'Europe/Paris' },
                    { name: 'Lyon', timezone: 'Europe/Paris' },
                    { name: 'Marseille', timezone: 'Europe/Paris' }
                ]
            },
            {
                code: 'br',
                name: 'Brazil',
                emoji: '🇧🇷',
                cities: [
                    { name: 'São Paulo', timezone: 'America/Sao_Paulo' },
                    { name: 'Rio de Janeiro', timezone: 'America/Sao_Paulo' },
                    { name: 'Brasília', timezone: 'America/Sao_Paulo' }
                ]
            },
            {
                code: 'in',
                name: 'India',
                emoji: '🇮🇳',
                cities: [
                    { name: 'Mumbai', timezone: 'Asia/Kolkata' },
                    { name: 'Delhi', timezone: 'Asia/Kolkata' },
                    { name: 'Bangalore', timezone: 'Asia/Kolkata' }
                ]
            },
            {
                code: 'cn',
                name: 'China',
                emoji: '🇨🇳',
                cities: [
                    { name: 'Beijing', timezone: 'Asia/Shanghai' },
                    { name: 'Shanghai', timezone: 'Asia/Shanghai' },
                    { name: 'Guangzhou', timezone: 'Asia/Shanghai' }
                ]
            },
            {
                code: 'ru',
                name: 'Russia',
                emoji: '🇷🇺',
                cities: [
                    { name: 'Moscow', timezone: 'Europe/Moscow' },
                    { name: 'St. Petersburg', timezone: 'Europe/Moscow' },
                    { name: 'Novosibirsk', timezone: 'Asia/Novosibirsk' }
                ]
            }
        ];
    }
    
    getCurrentTime(timezone) {
        try {
            const now = this.DateTime.now().setZone(timezone);
            
            return {
                time: now.toFormat('HH:mm:ss'),
                date: now.toFormat('yyyy-MM-dd'),
                offset: now.toFormat('ZZ'),
                offsetHours: now.offset / 60,
                abbreviation: now.toFormat('ZZZZ'),
                isValid: now.isValid
            };
        } catch (error) {
            console.error('Error getting current time for timezone:', timezone, error);
            return {
                time: '--:--:--',
                date: '--',
                offset: '--',
                offsetHours: 0,
                abbreviation: '--',
                isValid: false
            };
        }
    }
    
    getTimezoneInfo(timezone) {
        try {
            const now = this.DateTime.now().setZone(timezone);
            const utc = this.DateTime.utc();
            
            return {
                timezone,
                currentTime: now.toFormat('HH:mm:ss'),
                currentDate: now.toFormat('cccc, LLLL d, yyyy'),
                offset: now.toFormat('ZZ'),
                offsetHours: now.offset / 60,
                abbreviation: now.toFormat('ZZZZ'),
                isDST: now.isInDST,
                isValid: now.isValid,
                utcTime: utc.toFormat('HH:mm:ss'),
                localTime: this.DateTime.local().toFormat('HH:mm:ss')
            };
        } catch (error) {
            console.error('Error getting timezone info:', timezone, error);
            return null;
        }
    }
    
    searchCities(query) {
        if (!this.timezoneData || !query) {
            return [];
        }
        
        const normalizedQuery = query.toLowerCase().trim();
        const results = [];
        
        this.timezoneData.forEach(country => {
            if (country.cities) {
                country.cities.forEach(city => {
                    if (city.name.toLowerCase().includes(normalizedQuery) ||
                        country.name.toLowerCase().includes(normalizedQuery)) {
                        results.push({
                            name: city.name,
                            country: country.name,
                            timezone: city.timezone,
                            emoji: country.emoji,
                            countryCode: country.code
                        });
                    }
                });
            }
        });
        
        // Sort results: exact matches first, then partial matches
        results.sort((a, b) => {
            const aExact = a.name.toLowerCase() === normalizedQuery;
            const bExact = b.name.toLowerCase() === normalizedQuery;
            
            if (aExact && !bExact) return -1;
            if (!aExact && bExact) return 1;
            
            const aStarts = a.name.toLowerCase().startsWith(normalizedQuery);
            const bStarts = b.name.toLowerCase().startsWith(normalizedQuery);
            
            if (aStarts && !bStarts) return -1;
            if (!aStarts && bStarts) return 1;
            
            return a.name.localeCompare(b.name);
        });
        
        return results.slice(0, 10); // Limit to 10 results
    }
    
    convertTime(fromTimezone, toTimezone, timeString) {
        try {
            const [hours, minutes] = timeString.split(':').map(Number);
            const fromTime = this.DateTime.now()
                .setZone(fromTimezone)
                .set({ hour: hours, minute: minutes, second: 0 });
            
            const toTime = fromTime.setZone(toTimezone);
            
            return {
                time: toTime.toFormat('HH:mm:ss'),
                date: toTime.toFormat('yyyy-MM-dd'),
                isNextDay: toTime.day !== fromTime.day,
                isPrevDay: toTime.day < fromTime.day
            };
        } catch (error) {
            console.error('Error converting time:', error);
            return null;
        }
    }
    
    getTimezoneOffset(timezone) {
        try {
            const now = this.DateTime.now().setZone(timezone);
            return now.offset; // offset in minutes
        } catch (error) {
            console.error('Error getting timezone offset:', timezone, error);
            return 0;
        }
    }
    
    isValidTimezone(timezone) {
        try {
            const dt = this.DateTime.now().setZone(timezone);
            return dt.isValid;
        } catch (error) {
            return false;
        }
    }
    
    getAvailableTimezones() {
        if (!this.timezoneData) {
            return [];
        }
        
        const timezones = [];
        this.timezoneData.forEach(country => {
            if (country.cities) {
                country.cities.forEach(city => {
                    if (!timezones.find(tz => tz.timezone === city.timezone)) {
                        timezones.push({
                            timezone: city.timezone,
                            display: `${city.name}, ${country.name}`,
                            country: country.name,
                            city: city.name
                        });
                    }
                });
            }
        });
        
        return timezones.sort((a, b) => a.display.localeCompare(b.display));
    }
    
    formatTimeForDisplay(timezone, format = 'HH:mm:ss') {
        try {
            return this.DateTime.now().setZone(timezone).toFormat(format);
        } catch (error) {
            console.error('Error formatting time:', timezone, error);
            return '--:--:--';
        }
    }
}