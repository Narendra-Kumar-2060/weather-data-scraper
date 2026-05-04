import json
import csv
import folium
import os

DATA_FOLDER = "data_generated"
os.makedirs(DATA_FOLDER, exist_ok=True)


def decode_weather_code(weather_code):
    weather_codes = {
        0: ("Clear sky", "☀️", "sun-o"),
        1: ("Mainly clear", "🌤️", "sun-o"),
        2: ("Partly cloudy", "⛅", "cloud-sun"),
        3: ("Overcast", "☁️", "cloud"),
        45: ("Foggy", "🌫️", "smog"),
        48: ("Depositing rime fog", "🌫️", "smog"),
        51: ("Light drizzle", "🌦️", "cloud-rain"),
        53: ("Moderate drizzle", "🌦️", "cloud-rain"),
        55: ("Dense drizzle", "🌧️", "cloud-showers-heavy"),
        56: ("Light freezing drizzle", "🌨️", "cloud-snow"),
        57: ("Dense freezing drizzle", "🌨️", "cloud-snow"),
        61: ("Slight rain", "🌧️", "cloud-rain"),
        63: ("Moderate rain", "🌧️", "cloud-showers-heavy"),
        65: ("Heavy rain", "🌧️💧", "cloud-showers-heavy"),
        66: ("Light freezing rain", "🌨️", "cloud-snow"),
        67: ("Heavy freezing rain", "🌨️❄️", "cloud-snow"),
        71: ("Slight snow fall", "🌨️", "cloud-snow"),
        73: ("Moderate snow fall", "🌨️", "cloud-snow"),
        75: ("Heavy snow fall", "❄️🌨️", "cloud-snow"),
        77: ("Snow grains", "❄️", "cloud-snow"),
        80: ("Slight rain showers", "🌦️", "cloud-rain"),
        81: ("Moderate rain showers", "🌧️", "cloud-showers-heavy"),
        82: ("Violent rain showers", "⛈️", "cloud-rain"),
        85: ("Slight snow showers", "🌨️", "cloud-snow"),
        86: ("Heavy snow showers", "❄️🌨️", "cloud-snow"),
        95: ("Thunderstorm", "⛈️", "bolt"),
        96: ("Thunderstorm with slight hail", "⛈️🌨️", "bolt"),
        99: ("Thunderstorm with heavy hail", "⛈️❄️", "bolt"),
    }
    return weather_codes.get(int(weather_code), ("Unknown", "❓", "question"))


csv_path = os.path.join(DATA_FOLDER, "current_weather.csv")
cities = []
with open(csv_path, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cities.append(row)

with open("cities.json") as f:
    cities_data = json.load(f)

coords = {}
for city in cities_data:
    coords[city["name"]] = [city["lat"], city["lon"]]

m = folium.Map(location=[24.5, 86.5], zoom_start=7)

for city in cities:
    name = city["city"]
    if name in coords:
        temp = float(city["temperature_celsius"])
        humidity = float(city["humidity_percent"])
        wind = city["wind_speed_kmh"]
        weather_code = int(city.get("weather_code", 0))

        weather_desc, weather_emoji, weather_icon = decode_weather_code(weather_code)

        if temp < 10:
            m_color = "blue"
        elif 10 <= temp < 25:
            m_color = "green"
        elif 25 <= temp < 35:
            m_color = "orange"
        else:
            m_color = "red"

        if weather_code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
            m_icon = "cloud-rain"
            m_color = "cadetblue"
        elif weather_code in [71, 73, 75, 77, 85, 86]:
            m_icon = "cloud-snow"
            m_color = "lightgray"
        elif weather_code in [95, 96, 99]:
            m_icon = "bolt"
            m_color = "darkred"
        elif temp > 35:
            m_icon = "sun-o"
            m_color = "red"
        elif humidity > 80:
            m_icon = "tint"
            m_color = "blue"
        elif temp < 0:
            m_icon = "snowflake-o"
            m_color = "lightblue"
        else:
            m_icon = weather_icon

        popup_text = f"""
        <div style="width:180px; font-family: Arial, sans-serif;">
            <b style="font-size: 16px;">{name}</b><br>
            <hr style="margin: 5px 0;">
            {weather_emoji} <b>Conditions:</b> {weather_desc}<br>
            🌡️ <b>Temp:</b> {temp}°C<br>
            💧 <b>Humidity:</b> {humidity}%<br>
            💨 <b>Wind:</b> {wind} km/h<br>
            🧭 <b>Wind Direction:</b> {city.get('wind_direction_text', 'N/A')}<br>
            🕐 <b>Local Time:</b> {city.get('local_time', 'N/A')}
        </div>
        """

        folium.Marker(
            location=coords[name],
            tooltip=f"{weather_emoji} {name} - {temp}°C, {weather_desc}",
            popup=folium.Popup(popup_text, max_width=250),
            icon=folium.Icon(color=m_color, icon=m_icon, prefix="fa"),
        ).add_to(m)

title_html = """
<div style="position: fixed; top: 10px; left: 50%; transform: translateX(-50%);
            background-color: white; padding: 10px 20px; border-radius: 10px;
            border: 2px solid #333; box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            font-family: Arial, sans-serif; z-index: 1000;">
    <h2 style="margin: 0;">🌤️ Weather Map</h2>
    <p style="margin: 5px 0 0 0; font-size: 12px;">Click on markers for detailed weather info</p>
</div>
"""
m.get_root().html.add_child(folium.Element(title_html))
output_path = os.path.join(DATA_FOLDER, "weather_map.html")  # ADD THIS
m.save(output_path)  # CHANGE to output_path
print(f"✅ Successfully generated {output_path}")  # CHANGE THIS
print(f"   Open '{output_path}' in your web browser to view the interactive map!")
