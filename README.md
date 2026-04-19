# Weather Data Scraper
A simple Python script that fetches real-time weather data for Ranchi and Ramgarh cities using Open-Meteo API.

## Features
- Fetches temperature, humidity, feels-like temperature, wind speed, and wind direction
- Converts wind degrees to 8 cardinal directions (N, NE, E, SE, S, SW, W, NW)
- Displays weather alerts for hot temperatures (>30°C) and windy conditions (>30 km/h)
- Saves data to CSV file

## Requirements
- Python 3.x
- requests library

## Installation
1. Clone the repository
2. Install dependencies:
    ```bash
    pip install requests
    ```

## Usage
```bash
python weather_scraper.py
```

## Output
The script will:
- Display current weather data in the terminal
- Save data to weather_data.csv with timestamp

## File Structure
- weather_scraper.py - Main script
- weather_data.csv - Generated CSV output file

## Author
Narendra Kumar