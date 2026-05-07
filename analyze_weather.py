import csv
import sqlite3
import os

DATA_FOLDER = "data_generated"
os.makedirs(DATA_FOLDER, exist_ok=True)


def create_weather_db(dbname="weather.db"):
    db_path = os.path.join(DATA_FOLDER, dbname)
    sqlite3.connect(db_path).close()


def create_current_weather_table(dbname="weather.db", csvfile="current_weather.csv"):
    csv_path = os.path.join(DATA_FOLDER, csvfile)
    db_path = os.path.join(DATA_FOLDER, dbname)
    if not os.path.exists(csv_path):
        print(f"Warning: {csv_path} not found. Skipping...")
        return
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS current_weather(city text not null, temperature_celsius real not null, humidity_percent int not null, wind_speed_kmh real not null, wind_direction_text text not null, timezone text not null, local_time text not null)"
    )
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for data in reader:
            cur.execute(
                "INSERT INTO current_weather(city, temperature_celsius, humidity_percent, wind_speed_kmh, wind_direction_text, timezone, local_time) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    data["city"],
                    data["temperature_celsius"],
                    data["humidity_percent"],
                    data["wind_speed_kmh"],
                    data["wind_direction_text"],
                    data["timezone"],
                    data["local_time"],
                ),
            )

    con.commit()
    con.close()


def create_7day_forecast_table(dbname="weather.db", csvfile="7day_forecast.csv"):
    csv_path = os.path.join(DATA_FOLDER, csvfile)
    db_path = os.path.join(DATA_FOLDER, dbname)

    if not os.path.exists(csv_path):
        print(f"Warning: {csv_path} not found. Skipping...")
        return
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS forecast_7day(city text not null, time text not null, temperature_celsius real not null, humidity_percent int not null)"
    )

    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        next(reader)
        for data in reader:
            cur.execute(
                "INSERT INTO forecast_7day(city, time, temperature_celsius, humidity_percent) VALUES (?, ?, ?, ?)",
                (data[0], data[1], data[2], data[3]),
            )

    con.commit()
    con.close()


def current_data(dbname="weather.db"):
    db_path = os.path.join(DATA_FOLDER, dbname)
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute(
        "SELECT city, temperature_celsius FROM current_weather WHERE temperature_celsius = (SELECT MAX(temperature_celsius) FROM current_weather)"
    )
    hot = cur.fetchone()

    cur.execute(
        "SELECT city, temperature_celsius FROM current_weather WHERE temperature_celsius = (SELECT MIN(temperature_celsius) FROM current_weather)"
    )
    cold = cur.fetchone()

    cur.execute(
        "SELECT city, humidity_percent FROM current_weather WHERE humidity_percent = (SELECT MAX(humidity_percent) FROM current_weather)"
    )
    humid = cur.fetchone()

    cur.execute(
        "SELECT city, wind_speed_kmh FROM current_weather WHERE wind_speed_kmh = (SELECT MAX(wind_speed_kmh) FROM current_weather)"
    )
    windy = cur.fetchone()

    print("=== CURRENT WEATHER SUMMARY ===")

    if hot:
        print(f"Hottest:  {hot[0]} ({hot[1]}°C)")

    if cold:
        print(f"Coldest:  {cold[0]} ({cold[1]}°C)")

    if humid:
        print(f"Most humid: {humid[0]} ({humid[1]}%)")

    if windy:
        print(f"Most windy:  {windy[0]} ({windy[1]} km/h)")

    con.close()


def forecast_analysis(dbname="weather.db"):
    db_path = os.path.join(DATA_FOLDER, dbname)

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute(
        "SELECT city, AVG(temperature_celsius) FROM forecast_7day GROUP BY city ORDER BY AVG(temperature_celsius) DESC"
    )
    avg_temps = cur.fetchall()

    cur.execute(
        "SELECT city, time, MAX(temperature_celsius) FROM forecast_7day GROUP BY city"
    )
    hottest_times = cur.fetchall()

    cur.execute(
        "SELECT city, time, MIN(temperature_celsius) FROM forecast_7day GROUP BY city"
    )
    coldest_times = cur.fetchall()

    print("\n=== 7-DAY FORECAST SUMMARY ===")

    print("\n📊 Average Temperature by City:")
    for city, avg_temp in avg_temps:
        print(f"  {city}: {avg_temp:.1f}°C")

    print("\n🔥 Hottest Time by City:")
    for city, time, max_temp in hottest_times:
        print(f"  {city}: {max_temp:.1f}°C at {time}")

    print("\n❄️ Coldest Time by City:")
    for city, time, min_temp in coldest_times:
        print(f"  {city}: {min_temp:.1f}°C at {time}")

    con.close()


def reset_database(dbname="weather.db"):
    db_path = os.path.join(DATA_FOLDER, dbname)

    if os.path.exists(db_path):
        os.remove(db_path)


def main():
    reset_database()
    create_weather_db()
    create_current_weather_table()
    create_7day_forecast_table()
    current_data()
    forecast_analysis()


if __name__ == "__main__":
    main()
