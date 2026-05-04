# Weather Data Pipeline 🌍

A complete weather data pipeline that fetches real-time weather data from Open-Meteo API, stores it in SQLite, analyzes patterns, and generates interactive maps. Supports multiple cities with current conditions and 7-day forecasts.

## Features

### 🌐 Data Collection

- Fetches current weather data (temperature, humidity, wind, conditions)
- Retrieves 7-day hourly forecasts
- Supports multiple cities with custom coordinates
- Automatic timezone conversion to local time
- Real-time API integration

### 💾 Data Storage

- SQLite database for structured storage
- CSV exports for spreadsheet analysis
- Separate tables for current weather and forecasts
- Persistent data management with reset option

### 📊 Analysis

- Temperature extremes (hottest/coldest cities)
- Humidity analysis
- Wind speed tracking
- 7-day forecast averaging
- City-specific comparisons

### 🗺️ Visualization

- Interactive Folium maps with city markers
- Color-coded markers based on temperature/conditions
- Weather emoji indicators
- Popup windows with detailed weather info
- Custom icons for different weather types

## Tech Stack

- **Python 3.7+**
- **Requests** - API calls to Open-Meteo
- **SQLite3** - Local database storage
- **Folium** - Interactive map generation
- **CSV/JSON** - Data interchange formats
- **Datetime** - Timezone handling

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/weather-pipeline.git
cd weather-pipeline

# Install dependencies
pip install requests folium

# Run the complete pipeline
python weather_scraper.py    # Fetches current weather
python multi_day_weather.py   # Fetches 7-day forecast
python analyze_weather.py     # Analyzes data and creates DB
python weather_visualizer.py  # Generates interactive map
```

## Project Structure

```
weather-pipeline/
├── cities.json              # City coordinates configuration
├── weather_scraper.py       # Current weather fetcher
├── multi_day_weather.py     # 7-day forecast fetcher
├── analyze_weather.py       # Data analysis & DB storage
├── weather_visualizer.py    # Interactive map generator
├── current_weather.csv      # Current weather output
├── 7day_forecast.csv        # Forecast output
├── weather.db               # SQLite database
└── weather_map.html         # Interactive weather map
```

## Configuration

### cities.json Format

```json
[
  {
    "name": "Ranchi",
    "lat": 23.3432,
    "lon": 85.3094
  }
]
```

Add any city with its latitude and longitude coordinates.

## Usage

### 1. Fetch Current Weather

```bash
python weather_scraper.py
```

Output:

```
============================================================
     WELCOME TO THE WEATHER DATA SCRAPER
============================================================
Getting weather for Ranchi...
  ✓ Got data for Ranchi (Local: 2026-04-29 14:30:15)

============================================================
                WEATHER REPORT
============================================================

📍 Ranchi
   🕐 Local Time: 2026-04-29 14:30:15 (UTC+5.5)
   ☀️ Conditions: Clear sky
   🌡️  Temperature: 32°C
   💧 Humidity: 45%
   🤔 Feels like: 34°C
   💨 Wind speed: 12 km/h
   🧭 Wind direction: East (90°)
   ⚠️  HOT weather! Drink water!
```

### 2. Fetch 7-Day Forecast

```bash
python multi_day_weather.py
```

Fetches hourly weather data for the next 7 days and saves to 7day_forecast.csv.

### 3. Analyze and Store Data

```bash
python analyze_weather.py
```

Output:

```
=== CURRENT WEATHER SUMMARY ===
Hottest:  Siliguri (35.5°C)
Coldest:  Godda (28.2°C)
Most humid: Ranchi (78%)
Most windy:  Ramgarh (22 km/h)

=== 7-DAY FORECAST SUMMARY ===

📊 Average Temperature by City:
  Siliguri: 33.2°C
  Ranchi: 30.1°C
  Ramgarh: 29.8°C
  Godda: 28.5°C

🔥 Hottest Time by City:
  Siliguri: 36.0°C at 2026-04-30T14:00
  Ranchi: 33.5°C at 2026-05-01T13:00
```

### 4. Generate Interactive Map

```bash
python weather_visualizer.py
```

Creates weather_map.html - an interactive map with:

- Color-coded markers by temperature/conditions
- Clickable popups with detailed weather
- Weather icons and emojis
- City tooltips on hover

## Database Schema

### current_weather Table

| Column              | Type    |
| ------------------- | ------- |
| city                | TEXT    |
| temperature_celsius | REAL    |
| humidity_percent    | INTEGER |
| wind_speed_kmh      | REAL    |
| wind_direction_text | TEXT    |
| timezone            | TEXT    |
| local_time          | TEXT    |

### forecast_7day Table

| Column              | Type    |
| ------------------- | ------- |
| city                | TEXT    |
| time                | TEXT    |
| temperature_celsius | REAL    |
| humidity_percent    | INTEGER |

## Weather Categories

### Temperature Colors (Maps)

- 🔴 Red - Extreme heat (>35°C)
- 🟠 Orange - Hot (25-35°C)
- 🟢 Green - Moderate (10-25°C)
- 🔵 Blue - Cold (<10°C)

### Weather Codes

| Code  | Condition         |
| ----- | ----------------- |
| 0-3   | Clear to overcast |
| 45-48 | Fog               |
| 51-55 | Drizzle           |
| 61-65 | Rain              |
| 71-77 | Snow              |
| 80-82 | Rain showers      |
| 85-86 | Snow showers      |
| 95-99 | Thunderstorm      |

## Example Workflow

```bash
# One complete run
python weather_scraper.py && \
python multi_day_weather.py && \
python analyze_weather.py && \
python weather_visualizer.py

# Then open weather_map.html in your browser
```

## Future Improvements

- Automated scheduling with cron/Airflow
- Email/SMS alerts for extreme weather
- Historical data tracking
- Temperature trend graphs (matplotlib)
- Mobile-friendly web dashboard
- Docker containerization
- Weather prediction using ML

## API Reference

Uses Open-Meteo - Free weather API with no API key required.

## License

MIT

## Author

Narendra Kumar
