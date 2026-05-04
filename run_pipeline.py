import subprocess
import os

DATA_FOLDER = "data_generated"
os.makedirs(DATA_FOLDER, exist_ok=True)

print(f"📁 Output folder: {DATA_FOLDER}/")
print("=" * 50)

scripts = [
    "weather_scraper.py",
    "multi_day_weather.py",
    "analyze_weather.py",
    "weather_visualizer.py",
]

for script in scripts:
    print(f"\n🚀 Running {script}...")
    result = subprocess.run(["python", script])
    if result.returncode != 0:
        print(f"❌ Failed at {script}")
        break
else:
    print("\n" + "=" * 50)
    print("✅ Pipeline complete!")
    print(f"📁 All files saved in '{DATA_FOLDER}/' folder")
    print(f"🗺️ Open '{DATA_FOLDER}/weather_map.html' in your browser")
