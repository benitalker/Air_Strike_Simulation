import math
from datetime import datetime, time
from typing import List, Tuple
from toolz import curry, pipe, compose
from toolz.curried import map, filter, take
from itertools import product

from models.aircraft import Aircraft
from models.mission import Mission
from models.pilot import Pilot
from models.target import Target
from models.weather import Weather
from repository.csv_repository import write_missions_to_csv
from repository.json_repository import load_weather_data

# Global variables for data
_pilots: List[Pilot] = []
_aircraft: List[Aircraft] = []
_targets: List[Target] = []


def load_data(pilots: List[Pilot], aircraft: List[Aircraft], targets: List[Target]):
    global _pilots, _aircraft, _targets
    _pilots, _aircraft, _targets = pilots, aircraft, targets

def save_recommendations_to_csv(filename: str):
    return write_missions_to_csv(get_recommendations(), filename)

@curry
def get_weather_conditions(weather_data: dict, target: Target) -> Weather:
    city_data = weather_data.get(target.city, {})
    return Weather(
        weather=city_data.get('weather', 'No data'),
        clouds=city_data.get('clouds', 0),
        wind_speed=city_data.get('wind_speed', 0)
    )

def calculate_distance(target: Target) -> float:
    return haversine_distance(target.lat, target.lon, 32.081669, 34.841011)

def haversine_distance(lat1, lon1, lat2, lon2):
    r = 6371.0
    lat1_rad, lon1_rad = map(math.radians, (float(lat1), float(lon1)))
    lat2_rad, lon2_rad = map(math.radians, (lat2, lon2))
    dlat, dlon = lat2_rad - lat1_rad, lon2_rad - lon1_rad
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c

def get_execution_time() -> str:
    return datetime.combine(datetime.today(), time(0, 0, 0)).strftime('%Y-%m-%d %H:%M:%S')

@curry
def create_mission(weather_func, target: Target, aircraft: Aircraft, pilot: Pilot) -> Mission:
    return Mission(
        target,
        aircraft,
        pilot,
        weather_func(target),
        calculate_distance(target),
        get_execution_time()
    )

@curry
def has_sufficient_fuel(aircraft: Aircraft, distance: float) -> bool:
    return aircraft.fuel_capacity >= (distance * 2) / aircraft.fuel_capacity
def get_recommendations() -> List[Mission]:
    if not (_pilots and _aircraft and _targets):
        return []

    weather_data = load_weather_data()
    if isinstance(weather_data, list) and weather_data:
        weather_data = weather_data[0]

    weather_func = get_weather_conditions(weather_data)

    def create_missions():
        used_pilots = set()
        used_aircraft = set()
        used_targets = set()  # Keep track of used targets

        for target, aircraft, pilot in product(_targets, _aircraft, _pilots):
            if pilot in used_pilots or aircraft in used_aircraft or target in used_targets:
                continue

            distance = calculate_distance(target)
            if not has_sufficient_fuel(aircraft, distance):
                continue

            mission = create_mission(weather_func, target, aircraft, pilot)
            used_pilots.add(pilot)
            used_aircraft.add(aircraft)
            used_targets.add(target)  # Mark the target as used
            yield mission

    # Convert generator to list before sorting
    missions = list(create_missions())

    return pipe(
        sorted(missions, key=lambda m: m.score, reverse=True),  # Sort based on score
        take(7),  # Take top 7 missions
        list  # Convert back to list
    )
