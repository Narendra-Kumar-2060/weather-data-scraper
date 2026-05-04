import requests
import csv
import json
from datetime import datetime, timezone, timedelta
import os

DATA_FOLDER = "data_generated"
os.makedirs(DATA_FOLDER, exist_ok=True)


with open("cities.json") as f:
    cities = json.load(f)


def get_weather_for_cities():
    weather_api_url = "https://api.open-meteo.com/v1/forecast"
    all_weather_data = []

    for city in cities:
        print(f"Getting weather for {city['name']}...")

        request_params = {
            "latitude": city["lat"],
            "longitude": city["lon"],
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,wind_direction_10m,weather_code",
            "timezone": "auto",
        }

        try:
            response = requests.get(weather_api_url, params=request_params)

            if response.status_code == 200:
                weather_info = response.json()
                current_weather = weather_info["current"]
                city_timezone = weather_info.get("timezone", "Unknown")
                utc_offset_seconds = weather_info.get("utc_offset_seconds", 0)
                utc_now = datetime.now(timezone.utc)
                local_time = utc_now + timedelta(seconds=utc_offset_seconds)
                local_time_str = local_time.strftime("%Y-%m-%d %H:%M:%S")
                offset_hours = utc_offset_seconds / 3600

                city_weather = {
                    "city_name": city["name"],
                    "temperature": current_weather["temperature_2m"],
                    "humidity": current_weather["relative_humidity_2m"],
                    "feels_like": current_weather["apparent_temperature"],
                    "wind_speed": current_weather["wind_speed_10m"],
                    "wind_direction_degrees": current_weather["wind_direction_10m"],
                    "weather_code": current_weather["weather_code"],
                    "timezone": city_timezone,
                    "local_time": local_time_str,
                    "utc_offset_hours": offset_hours,
                }

                all_weather_data.append(city_weather)
                print(f"  ✓ Got data for {city['name']} (Local: {local_time_str})")

            else:
                print(f"  ✗ Failed to get data for {city['name']}")

        except Exception as error:
            print(f"  ✗ Error getting weather for {city['name']}: {error}")

    return all_weather_data


def convert_degrees_to_direction(degrees):
    degrees = degrees % 360

    if degrees < 22.5 or degrees >= 337.5:
        return "North"
    elif degrees < 67.5:
        return "Northeast"
    elif degrees < 112.5:
        return "East"
    elif degrees < 157.5:
        return "Southeast"
    elif degrees < 202.5:
        return "South"
    elif degrees < 247.5:
        return "Southwest"
    elif degrees < 292.5:
        return "West"
    else:
        return "Northwest"


def decode_weather_code(weather_code):
    weather_codes = {
        0: ("Clear sky", "☀️"),
        1: ("Mainly clear", "🌤️"),
        2: ("Partly cloudy", "⛅"),
        3: ("Overcast", "☁️"),
        45: ("Foggy", "🌫️"),
        48: ("Depositing rime fog", "🌫️"),
        51: ("Light drizzle", "🌦️"),
        53: ("Moderate drizzle", "🌦️"),
        55: ("Dense drizzle", "🌧️"),
        56: ("Light freezing drizzle", "🌨️"),
        57: ("Dense freezing drizzle", "🌨️"),
        61: ("Slight rain", "🌧️"),
        63: ("Moderate rain", "🌧️"),
        65: ("Heavy rain", "🌧️💧"),
        66: ("Light freezing rain", "🌨️"),
        67: ("Heavy freezing rain", "🌨️❄️"),
        71: ("Slight snow fall", "🌨️"),
        73: ("Moderate snow fall", "🌨️"),
        75: ("Heavy snow fall", "❄️🌨️"),
        77: ("Snow grains", "❄️"),
        80: ("Slight rain showers", "🌦️"),
        81: ("Moderate rain showers", "🌧️"),
        82: ("Violent rain showers", "⛈️"),
        85: ("Slight snow showers", "🌨️"),
        86: ("Heavy snow showers", "❄️🌨️"),
        95: ("Thunderstorm", "⛈️"),
        96: ("Thunderstorm with slight hail", "⛈️🌨️"),
        99: ("Thunderstorm with heavy hail", "⛈️❄️"),
    }
    return weather_codes.get(weather_code, ("Unknown", "❓"))


def show_weather_report(weather_data):
    utc_now = datetime.now(timezone.utc)

    print("\n" + "=" * 60)
    print("                WEATHER REPORT")
    print("=" * 60)
    print(f"🕐 UTC Time: {utc_now.strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("=" * 60)

    for city in weather_data:
        weather_description, weather_emoji = decode_weather_code(city["weather_code"])
        print(f"\n📍 {city['city_name']}")
        print(
            f"   🕐 Local Time: {city['local_time']} (UTC{city['utc_offset_hours']:+g})"
        )
        print(f"   {weather_emoji} Conditions: {weather_description}")
        print(f"   🌡️  Temperature: {city['temperature']}°C")
        print(f"   💧 Humidity: {city['humidity']}%")
        print(f"   🤔 Feels like: {city['feels_like']}°C")
        print(f"   💨 Wind speed: {city['wind_speed']} km/h")

        wind_direction_text = convert_degrees_to_direction(
            city["wind_direction_degrees"]
        )
        print(
            f"   🧭 Wind direction: {wind_direction_text} ({city['wind_direction_degrees']}°)"
        )

        temp = city["temperature"]

        if temp > 35:
            print("   🔥 EXTREME HEAT! Stay hydrated!")
        elif temp > 30:
            print("   ⚠️  HOT weather! Drink water!")
        elif temp > 25:
            print("   🌤️  Warm and pleasant")
        elif temp > 20:
            print("   👍 Comfortable weather")
        elif temp > 15:
            print("   🧥 A bit cool, take a jacket")
        else:
            print("   ❄️  COLD! Wear warm clothes!")

        wind = city["wind_speed"]
        if wind > 30:
            print("   💨 VERY WINDY! Be careful!")
        elif wind > 20:
            print("   🍃 Breezy outside")

    print("\n" + "=" * 60)


def save_to_csv_file(weather_data, filename="current_weather.csv"):
    filepath = os.path.join(DATA_FOLDER, filename)
    with open(filepath, "w", newline="", encoding="utf-8") as csv_file:  # CHANGE THIS
        column_names = [
            "city",
            "temperature_celsius",
            "humidity_percent",
            "feels_like_celsius",
            "wind_speed_kmh",
            "wind_direction_degrees",
            "wind_direction_text",
            "weather_code",
            "weather_description",
            "timezone",
            "local_time",
            "utc_offset_hours",
        ]

        writer = csv.DictWriter(csv_file, fieldnames=column_names)
        writer.writeheader()

        for city in weather_data:
            city["wind_direction_text"] = convert_degrees_to_direction(
                city["wind_direction_degrees"]
            )

            weather_desc, weather_emoji = decode_weather_code(city["weather_code"])

            row_data = {
                "city": city["city_name"],
                "temperature_celsius": city["temperature"],
                "humidity_percent": city["humidity"],
                "feels_like_celsius": city["feels_like"],
                "wind_speed_kmh": city["wind_speed"],
                "wind_direction_degrees": city["wind_direction_degrees"],
                "wind_direction_text": city["wind_direction_text"],
                "weather_code": city["weather_code"],
                "weather_description": weather_desc,
                "timezone": city["timezone"],
                "local_time": city["local_time"],
                "utc_offset_hours": city["utc_offset_hours"],
            }

            writer.writerow(row_data)

    print(f"\n✅ Weather data saved to {filepath}")  # CHANGE THIS
    print("   You can open this file with Excel or any text editor")


def main():
    print("\n" + "=" * 60)
    print("     WELCOME TO THE WEATHER DATA SCRAPER")
    print("=" * 60)

    weather_info = get_weather_for_cities()

    if len(weather_info) > 0:
        show_weather_report(weather_info)
        save_to_csv_file(weather_info)
    else:
        print("\n❌ Sorry, couldn't get any weather data!")
        print("   Please check your internet connection and try again.")

    print("\nThanks for using the Weather Scraper!")


if __name__ == "__main__":
    main()
