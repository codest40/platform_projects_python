export interface City {
  name: string;
  zone: string;
}

export interface Country {
  code: string;
  name: string;
  emoji: string;
  timezone: string;
  cities: City[];
}

export const timezoneData: Country[] = [
  {
    code: "us",
    name: "United States",
    emoji: "🇺🇸",
    timezone: "America/New_York",
    cities: [
      { name: "New York", zone: "America/New_York" },
      { name: "Los Angeles", zone: "America/Los_Angeles" },
      { name: "Chicago", zone: "America/Chicago" },
      { name: "Phoenix", zone: "America/Phoenix" },
      { name: "Denver", zone: "America/Denver" }
    ]
  },
  {
    code: "gb",
    name: "United Kingdom",
    emoji: "🇬🇧",
    timezone: "Europe/London",
    cities: [
      { name: "London", zone: "Europe/London" },
      { name: "Manchester", zone: "Europe/London" },
      { name: "Edinburgh", zone: "Europe/London" }
    ]
  },
  {
    code: "jp",
    name: "Japan",
    emoji: "🇯🇵",
    timezone: "Asia/Tokyo",
    cities: [
      { name: "Tokyo", zone: "Asia/Tokyo" },
      { name: "Osaka", zone: "Asia/Tokyo" },
      { name: "Kyoto", zone: "Asia/Tokyo" }
    ]
  },
  {
    code: "au",
    name: "Australia",
    emoji: "🇦🇺",
    timezone: "Australia/Sydney",
    cities: [
      { name: "Sydney", zone: "Australia/Sydney" },
      { name: "Melbourne", zone: "Australia/Melbourne" },
      { name: "Perth", zone: "Australia/Perth" },
      { name: "Brisbane", zone: "Australia/Brisbane" }
    ]
  },
  {
    code: "ng",
    name: "Nigeria",
    emoji: "🇳🇬",
    timezone: "Africa/Lagos",
    cities: [
      { name: "Lagos", zone: "Africa/Lagos" },
      { name: "Abuja", zone: "Africa/Lagos" },
      { name: "Kano", zone: "Africa/Lagos" }
    ]
  },
  {
    code: "in",
    name: "India",
    emoji: "🇮🇳",
    timezone: "Asia/Kolkata",
    cities: [
      { name: "Mumbai", zone: "Asia/Kolkata" },
      { name: "Delhi", zone: "Asia/Kolkata" },
      { name: "Bangalore", zone: "Asia/Kolkata" },
      { name: "Chennai", zone: "Asia/Kolkata" }
    ]
  },
  {
    code: "br",
    name: "Brazil",
    emoji: "🇧🇷",
    timezone: "America/Sao_Paulo",
    cities: [
      { name: "São Paulo", zone: "America/Sao_Paulo" },
      { name: "Rio de Janeiro", zone: "America/Sao_Paulo" },
      { name: "Brasília", zone: "America/Sao_Paulo" }
    ]
  },
  {
    code: "ca",
    name: "Canada",
    emoji: "🇨🇦",
    timezone: "America/Toronto",
    cities: [
      { name: "Toronto", zone: "America/Toronto" },
      { name: "Vancouver", zone: "America/Vancouver" },
      { name: "Montreal", zone: "America/Toronto" },
      { name: "Calgary", zone: "America/Edmonton" }
    ]
  },
  {
    code: "de",
    name: "Germany",
    emoji: "🇩🇪",
    timezone: "Europe/Berlin",
    cities: [
      { name: "Berlin", zone: "Europe/Berlin" },
      { name: "Munich", zone: "Europe/Berlin" },
      { name: "Hamburg", zone: "Europe/Berlin" },
      { name: "Frankfurt", zone: "Europe/Berlin" }
    ]
  },
  {
    code: "fr",
    name: "France",
    emoji: "🇫🇷",
    timezone: "Europe/Paris",
    cities: [
      { name: "Paris", zone: "Europe/Paris" },
      { name: "Lyon", zone: "Europe/Paris" },
      { name: "Marseille", zone: "Europe/Paris" }
    ]
  },
  {
    code: "cn",
    name: "China",
    emoji: "🇨🇳",
    timezone: "Asia/Shanghai",
    cities: [
      { name: "Beijing", zone: "Asia/Shanghai" },
      { name: "Shanghai", zone: "Asia/Shanghai" },
      { name: "Guangzhou", zone: "Asia/Shanghai" },
      { name: "Shenzhen", zone: "Asia/Shanghai" }
    ]
  },
  {
    code: "ru",
    name: "Russia",
    emoji: "🇷🇺",
    timezone: "Europe/Moscow",
    cities: [
      { name: "Moscow", zone: "Europe/Moscow" },
      { name: "St. Petersburg", zone: "Europe/Moscow" },
      { name: "Novosibirsk", zone: "Asia/Novosibirsk" },
      { name: "Vladivostok", zone: "Asia/Vladivostok" }
    ]
  }
];

export const getAllCities = (): Array<City & { country: string; emoji: string }> => {
  return timezoneData.flatMap(country => 
    country.cities.map(city => ({
      ...city,
      country: country.name,
      emoji: country.emoji
    }))
  );
};