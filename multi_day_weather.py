import requests
import csv
import json
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
            "hourly": "temperature_2m,relative_humidity_2m",
            "timezone": "auto",
            "forecast_days": 7,
        }

        try:
            response = requests.get(weather_api_url, params=request_params)

            if response.status_code == 200:
                weather_info = response.json()

                time_date = weather_info["hourly"]["time"]
                temperature = weather_info["hourly"]["temperature_2m"]
                humidity = weather_info["hourly"]["relative_humidity_2m"]

                city_weather = {
                    "city_name": city["name"],
                    "timezone": weather_info["timezone"],
                    "time_date": time_date,
                    "temperature": temperature,
                    "humidity": humidity,
                }

                all_weather_data.append(city_weather)
                print(f"  ✓ Got data for {city['name']}")

            else:
                print(f"  ✗ Failed to get data for {city['name']}")

        except Exception as error:
            print(f"  ✗ Error getting weather for {city['name']}: {error}")

    return all_weather_data


def show_weather_data(weather_data):
    print("\n" + "=" * 60)
    print("                WEATHER REPORT")
    print("=" * 60)

    for city in weather_data:
        print(f"\n📍 {city['city_name'].upper()}")

        for i in range(24):
            time = city["time_date"][i]
            temp = city["temperature"][i]
            hum = city["humidity"][i]
            print(f"{time} | {temp}°C | {hum}%")


def save_to_csv_file(weather_data, filename="7day_forecast.csv"):
    filepath = os.path.join(DATA_FOLDER, filename)
    with open(filepath, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["City", "Time", "Temperature_C", "Humidity_%"])

        for city in weather_data:
            for i in range(len(city["time_date"])):
                writer.writerow(
                    [
                        city["city_name"],
                        city["time_date"][i],
                        city["temperature"][i],
                        city["humidity"][i],
                    ]
                )

    print(f"✅ Saved to {filepath}")


def main():
    print("\n" + "=" * 60)
    print("     WELCOME TO THE WEATHER DATA SCRAPER")
    print("=" * 60)

    weather_info = get_weather_for_cities()

    if weather_info:
        show_weather_data(weather_info)
        save_to_csv_file(weather_info)
        print("\n✅ Weather data saved successfully!")
    else:
        print("\n❌ Sorry, couldn't get any weather data!")
        print("   Please check your internet connection and try again.")

    print("\nThanks for using the Weather Scraper!")


if __name__ == "__main__":
    main()
