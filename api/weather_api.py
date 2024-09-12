import json
import requests
from typing import List, Dict

API_KEY = "2d49683fc3265165b6686e384969cf41"


def fetch_and_save_weather_data(cities: List[str], filename: str):
    weather_data = {}

    for city in cities:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            target_datetime = "2024-09-13 00:00:00"

            for entry in data['list']:
                if entry['dt_txt'] == target_datetime:
                    weather_main = entry['weather'][0]['main']
                    clouds_all = entry['clouds']['all']
                    wind_speed = entry['wind']['speed']
                    weather_data[city] = {
                        "weather": weather_main,
                        "clouds": clouds_all,
                        "wind_speed": wind_speed
                    }
                    break
        else:
            weather_data[city] = {
                "weather": f"Error {response.status_code}",
                "clouds": 0,
                "wind_speed": 0
            }

    with open(filename, 'w') as file:
        json.dump(weather_data, file, indent=4)



cities = ["Damascus", "Beirut", "Amman", "Cairo", "Baghdad", "Tehran", "Riyadh", "Tripoli", "Ankara", "Khartoum",
          "Gaza City", "Sanaa", "Manama", "Kuwait City", "Doha"]
fetch_and_save_weather_data(cities, '../assets/weather_data.json')
