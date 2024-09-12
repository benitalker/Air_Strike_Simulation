from typing import Dict, List

import requests
import json

API_KEY = "2d49683fc3265165b6686e384969cf41"

def get_city_coordinates(city_name: str) -> Dict[str, float]:
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&appid={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data:
            city_info = data[0]
            lat = city_info.get('lat')
            lon = city_info.get('lon')
            return {"city": city_name, "lat": lat, "lon": lon}
        else:
            return {"city": city_name, "lat": None, "lon": None}  # Default values if city not found
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

def save_city_coordinates(cities: List[str], filename: str) -> None:
    city_coords = []
    for city in cities:
        coords = get_city_coordinates(city)
        city_coords.append(coords)

    with open(filename, 'w') as file:
        json.dump(city_coords, file, indent=4)

cities = ['Damascus', 'Beirut', 'Amman', 'Cairo', 'Baghdad', 'Tehran', 'Riyadh', 'Tripoli', 'Ankara', 'Khartoum', 'Gaza City', 'Sanaa', 'Manama', 'Kuwait City', 'Doha']
  
save_city_coordinates(cities, "../assets/city_coordinates.json")
