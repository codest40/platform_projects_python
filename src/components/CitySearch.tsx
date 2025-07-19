import React, { useState, useMemo } from 'react';
import { Search } from 'lucide-react';
import { Input } from './ui/input';
import { Button } from './ui/button';
import { getAllCities } from '../data/timezoneData';

interface City {
  name: string;
  zone: string;
  country: string;
  emoji: string;
}

interface CitySearchProps {
  onCitySelect: (city: City) => void;
}

export const CitySearch: React.FC<CitySearchProps> = ({ onCitySelect }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  
  const allCities = getAllCities();
  
  const filteredCities = useMemo(() => {
    if (!searchQuery.trim()) return [];
    
    return allCities
      .filter(city => 
        city.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        city.country.toLowerCase().includes(searchQuery.toLowerCase())
      )
      .slice(0, 8); // Limit results to 8 for better UX
  }, [searchQuery, allCities]);

  const handleCitySelect = (city: City) => {
    onCitySelect(city);
    setSearchQuery('');
    setIsOpen(false);
  };

  return (
    <div className="relative w-full max-w-md">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          type="text"
          placeholder="Search cities or countries..."
          value={searchQuery}
          onChange={(e) => {
            setSearchQuery(e.target.value);
            setIsOpen(true);
          }}
          onFocus={() => setIsOpen(true)}
          className="pl-10 glass-card border-primary/20"
        />
      </div>
      
      {isOpen && searchQuery && filteredCities.length > 0 && (
        <div className="absolute top-full left-0 right-0 mt-1 glass-card border border-primary/20 rounded-md shadow-lg z-50 max-h-64 overflow-y-auto">
          {filteredCities.map((city) => (
            <Button
              key={`${city.name}-${city.zone}`}
              variant="ghost"
              className="w-full justify-start p-3 h-auto"
              onClick={() => handleCitySelect(city)}
            >
              <div className="flex items-center space-x-3">
                <span className="text-lg">{city.emoji}</span>
                <div className="text-left">
                  <div className="font-medium">{city.name}</div>
                  <div className="text-sm text-muted-foreground">{city.country}</div>
                </div>
              </div>
            </Button>
          ))}
        </div>
      )}
      
      {isOpen && searchQuery && filteredCities.length === 0 && (
        <div className="absolute top-full left-0 right-0 mt-1 glass-card border border-primary/20 rounded-md shadow-lg z-50 p-3">
          <p className="text-sm text-muted-foreground text-center">
            No cities found for "{searchQuery}"
          </p>
        </div>
      )}
    </div>
  );
};