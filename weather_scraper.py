import requests
import csv
from datetime import datetime

def get_weather_data():
    locations = [
        {"name": "Ranchi", "latitude": 23.3432, "longitude": 85.3094},
        {"name": "Ramgarh", "latitude": 23.6303, "longitude": 85.5216}
    ]

    api_url = "https://api.open-meteo.com/v1/forecast"
    result = []
    timezone_info = None

    for loc in locations:
        payload = {
            'latitude': loc["latitude"], 
            'longitude': loc["longitude"], 
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,wind_direction_10m",
            "timezone": "auto", 
            "forecast_days": 1
        }
        
        try:
            response = requests.get(api_url, params=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                timezone_info = data.get("timezone", "Unknown")
                result.append({
                    "city": loc["name"],
                    "temperature": data["current"]["temperature_2m"],
                    "humidity": data["current"]["relative_humidity_2m"],
                    "feels_like": data["current"]["apparent_temperature"],
                    "wind_speed": data["current"]["wind_speed_10m"],
                    "wind_direction": data["current"]["wind_direction_10m"],
                    "timezone": timezone_info
                })
            else:
                print(f"❌ Failed to get data for {loc['name']}: Status {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching data for {loc['name']}: {e}")
    
    if not result:
        print("❌ No weather data retrieved!")
        return [], "Unknown"
    
    return result, timezone_info

def wind_direction_8(degrees):
    degrees = degrees % 360
    if degrees < 22.5 or degrees >= 337.5:
        return "N"
    elif degrees < 67.5:
        return "NE"
    elif degrees < 112.5:
        return "E"
    elif degrees < 157.5:
        return "SE"
    elif degrees < 202.5:
        return "S"
    elif degrees < 247.5:
        return "SW"
    elif degrees < 292.5:
        return "W"
    else:
        return "NW"

def analyze_weather(weather_list, timezone):
    print(f"\n{'='*50}")
    print(f"📍 Timezone: {timezone}")
    print(f"🕐 Data as of: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")
    
    for city in weather_list:
        print(f"\n{city['city']}:")
        print(f"   Temperature: {city['temperature']}°C")
        print(f"   Humidity: {city['humidity']}%")
        print(f"   Feels like: {city['feels_like']}°C")
        print(f"   Wind speed: {city['wind_speed']} km/h")
        
        wind_dir = wind_direction_8(city['wind_direction'])
        print(f"   Wind direction: {wind_dir} ({city['wind_direction']}°)")
        
        if city['temperature'] > 30:
            print(f"   ⚠️  Hot!")
        elif city['temperature'] < 20:
            print(f"   🧥 Cool!")
        
        if city['wind_speed'] > 30:
            print(f"   💨 Windy!")
            
def get_csv(weather_list, filename="weather_data.csv"):
    csvfile = open(filename, 'w', newline='', encoding='utf-8')
    try:
        fieldnames = ['city', 'temperature', 'humidity', 'feels_like', 
                     'wind_speed', 'wind_direction', 'wind_cardinal', 'timezone']
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for city in weather_list:
            city['wind_cardinal'] = wind_direction_8(city['wind_direction'])
            writer.writerow(city)
        
        print(f"\n✅ Weather data saved to {filename}")
    finally:
        csvfile.close()

if __name__ == "__main__":
    weather_list, timezone = get_weather_data()
    analyze_weather(weather_list, timezone)
    get_csv(weather_list)