import React, { useState, useEffect } from 'react';
import { Plus, Clock, Globe, Zap } from 'lucide-react';
import { TimezoneCard } from '../components/TimezoneCard';
import { CitySearch } from '../components/CitySearch';
import { ThemeToggle } from '../components/ThemeToggle';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import cosmicHero from '../assets/cosmic-hero.jpg';

interface SelectedCity {
  name: string;
  zone: string;
  country: string;
  emoji: string;
}

const Index = () => {
  const [selectedCities, setSelectedCities] = useState<SelectedCity[]>([]);
  const [showSearch, setShowSearch] = useState(false);

  // Load saved cities from localStorage on mount
  useEffect(() => {
    const savedCities = localStorage.getItem('timzap-cities');
    if (savedCities) {
      try {
        setSelectedCities(JSON.parse(savedCities));
      } catch (error) {
        console.error('Error loading saved cities:', error);
      }
    } else {
      // Default cities for new users
      setSelectedCities([
        { name: 'New York', zone: 'America/New_York', country: 'United States', emoji: '🇺🇸' },
        { name: 'London', zone: 'Europe/London', country: 'United Kingdom', emoji: '🇬🇧' },
        { name: 'Tokyo', zone: 'Asia/Tokyo', country: 'Japan', emoji: '🇯🇵' }
      ]);
    }
  }, []);

  // Save cities to localStorage whenever selectedCities changes
  useEffect(() => {
    localStorage.setItem('timzap-cities', JSON.stringify(selectedCities));
  }, [selectedCities]);

  const handleCitySelect = (city: SelectedCity) => {
    // Check if city is already selected
    const isAlreadySelected = selectedCities.some(
      selected => selected.zone === city.zone && selected.name === city.name
    );
    
    if (!isAlreadySelected) {
      setSelectedCities(prev => [...prev, city]);
    }
    setShowSearch(false);
  };

  const handleRemoveCity = (cityToRemove: SelectedCity) => {
    setSelectedCities(prev => 
      prev.filter(city => !(city.zone === cityToRemove.zone && city.name === cityToRemove.name))
    );
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div 
        className="relative h-screen flex items-center justify-center bg-cover bg-center bg-no-repeat"
        style={{ backgroundImage: `url(${cosmicHero})` }}
      >
        <div className="absolute inset-0 bg-black/40"></div>
        
        {/* Header */}
        <div className="absolute top-6 left-6 right-6 flex justify-between items-center z-10">
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2">
              <Zap className="h-8 w-8 text-primary" />
              <h1 className="text-2xl font-bold text-white">Timzap</h1>
            </div>
          </div>
          <ThemeToggle />
        </div>

        <div className="relative z-10 text-center text-white max-w-4xl mx-auto px-6">
          <div className="space-y-6">
            <h2 className="text-5xl md:text-7xl font-bold leading-tight">
              Time Around
              <span className="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent"> The World</span>
            </h2>
            <p className="text-xl md:text-2xl text-white/80 max-w-2xl mx-auto">
              Stay synchronized with the world. Track time across continents with beautiful, real-time timezone cards.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-8">
              <CitySearch onCitySelect={handleCitySelect} />
              <Button
                variant="glow"
                size="lg"
                onClick={() => setShowSearch(!showSearch)}
                className="flex items-center gap-2"
              >
                <Plus className="h-5 w-5" />
                Add City
              </Button>
            </div>

            <div className="flex items-center justify-center space-x-8 pt-8 text-white/60">
              <div className="flex items-center space-x-2">
                <Clock className="h-5 w-5" />
                <span>Real-time</span>
              </div>
              <div className="flex items-center space-x-2">
                <Globe className="h-5 w-5" />
                <span>Global</span>
              </div>
              <div className="flex items-center space-x-2">
                <Zap className="h-5 w-5" />
                <span>Fast</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Timezone Cards Section */}
      <div className="py-16 px-6">
        <div className="max-w-7xl mx-auto">
          {selectedCities.length > 0 ? (
            <>
              <div className="text-center mb-12">
                <h3 className="text-3xl font-bold mb-4">Your Time Zones</h3>
                <p className="text-muted-foreground text-lg">
                  Keep track of time across {selectedCities.length} {selectedCities.length === 1 ? 'location' : 'locations'}
                </p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {selectedCities.map((city) => (
                  <TimezoneCard
                    key={`${city.name}-${city.zone}`}
                    cityName={city.name}
                    timezone={city.zone}
                    countryEmoji={city.emoji}
                    countryName={city.country}
                    onRemove={() => handleRemoveCity(city)}
                  />
                ))}
              </div>
            </>
          ) : (
            <div className="text-center py-16">
              <Card className="glass-card max-w-md mx-auto p-8">
                <Clock className="h-16 w-16 text-primary mx-auto mb-4" />
                <h3 className="text-2xl font-semibold mb-2">No Cities Selected</h3>
                <p className="text-muted-foreground mb-6">
                  Start by adding your first city to track its timezone
                </p>
                <CitySearch onCitySelect={handleCitySelect} />
              </Card>
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-primary/20 py-8">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <p className="text-muted-foreground">
            Built with ❤️ for global teams and world travelers
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
