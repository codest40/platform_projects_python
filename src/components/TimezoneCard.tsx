import React, { useState, useEffect } from 'react';
import { DateTime } from 'luxon';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { X, MapPin } from 'lucide-react';

interface TimezoneCardProps {
  cityName: string;
  timezone: string;
  countryEmoji: string;
  countryName: string;
  onRemove: () => void;
}

export const TimezoneCard: React.FC<TimezoneCardProps> = ({
  cityName,
  timezone,
  countryEmoji,
  countryName,
  onRemove
}) => {
  const [currentTime, setCurrentTime] = useState<DateTime>(DateTime.now().setZone(timezone));

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(DateTime.now().setZone(timezone));
    }, 1000);

    return () => clearInterval(interval);
  }, [timezone]);

  const formatTime = (dt: DateTime) => {
    return dt.toLocaleString(DateTime.TIME_WITH_SECONDS);
  };

  const formatDate = (dt: DateTime) => {
    return dt.toLocaleString(DateTime.DATE_MED);
  };

  const getTimeStatus = () => {
    const hour = currentTime.hour;
    if (hour >= 6 && hour < 12) return { emoji: '🌅', status: 'Morning' };
    if (hour >= 12 && hour < 17) return { emoji: '☀️', status: 'Afternoon' };
    if (hour >= 17 && hour < 21) return { emoji: '🌇', status: 'Evening' };
    return { emoji: '🌙', status: 'Night' };
  };

  const timeStatus = getTimeStatus();
  const offset = currentTime.toFormat('ZZZ');
  const abbr = currentTime.toFormat('ZZZZ');

  return (
    <Card className="glass-card p-6 hover:scale-105 transform transition-smooth relative group">
      <Button
        variant="ghost"
        size="icon"
        className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-smooth h-8 w-8"
        onClick={onRemove}
      >
        <X className="h-4 w-4" />
      </Button>
      
      <div className="space-y-4">
        <div className="flex items-center space-x-3">
          <span className="text-2xl">{countryEmoji}</span>
          <div>
            <h3 className="font-semibold text-lg flex items-center gap-2">
              <MapPin className="h-4 w-4 text-primary" />
              {cityName}
            </h3>
            <p className="text-sm text-muted-foreground">{countryName}</p>
          </div>
        </div>
        
        <div className="space-y-2">
          <div className="text-3xl font-mono font-bold clock-glow">
            {formatTime(currentTime)}
          </div>
          <div className="flex items-center justify-between text-sm text-muted-foreground">
            <span>{formatDate(currentTime)}</span>
            <span className="flex items-center gap-1">
              {timeStatus.emoji} {timeStatus.status}
            </span>
          </div>
          <div className="text-xs text-muted-foreground">
            {abbr} ({offset})
          </div>
        </div>
      </div>
    </Card>
  );
};