import json

import requests

from models.aircraft import Aircraft
from typing import List, Dict, Any
from models.pilot import Pilot
from models.target import Target

def read_aircraft_from_json(filename: str) -> List[Aircraft]:
    data = _read_json(filename)
    return [convert_from_json_to_aircraft(aircraft) for aircraft in data]

def _read_json(path: str):
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return []

def convert_from_json_to_aircraft(aircraft_data: dict) -> Aircraft:
    return Aircraft(
        type=aircraft_data["type"],
        fuel_capacity=aircraft_data["fuel_capacity"],
        speed=aircraft_data["speed"]
    )

def read_pilots_from_json(filename: str) -> List[Pilot]:
    data = _read_json(filename)
    return [convert_from_json_to_pilot(pilot) for pilot in data]

def convert_from_json_to_pilot(pilot_data: dict) -> Pilot:
    return Pilot(
        name=pilot_data["name"],
        skill=pilot_data["skill"]
    )

def load_city_coordinates(filename: str) -> Dict[str, Dict[str, float]]:
    city_coords = _read_json(filename)
    return {item["city"]: {"lat": item["lat"], "lon": item["lon"]} for item in city_coords}

def convert_from_json_to_target(target_data: Dict[str, Any], geo_data: Dict[str, Dict[str, float]]) -> Target:
    city = target_data["city"]
    priority = target_data["priority"]
    location = geo_data.get(city, {"lat": 0.0, "lon": 0.0})
    return Target(
        city=city,
        priority=priority,
        lat=location["lat"],
        lon=location["lon"]
    )

def read_targets_from_json(filename1: str, coordinates_filename: str) -> List[Target]:
    data = _read_json(filename1)
    geo_data = load_city_coordinates(coordinates_filename)
    return [convert_from_json_to_target(target, geo_data) for target in data]

def load_weather_data():
    data = _read_json('./assets/weather_data.json')
    return data
