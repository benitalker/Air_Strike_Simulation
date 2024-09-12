import math
from datetime import datetime, time
from typing import List, Tuple
from toolz import curry, pipe, compose, first, second, nth, pluck, get_in, assoc, partition
from toolz.curried import map, filter, take, reduce
from itertools import product

from models.aircraft import Aircraft
from models.mission import Mission
from models.pilot import Pilot
from models.target import Target
from models.weather import Weather
from repository.csv_repository import write_missions_to_csv
from repository.json_repository import load_weather_data


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
    city_data = get_in([target.city], weather_data, {})
    return Weather(
        weather=get_in(['weather'], city_data, 'No data'),
        clouds=get_in(['clouds'], city_data, 0),
        wind_speed=get_in(['wind_speed'], city_data, 0)
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
    if not all([_pilots, _aircraft, _targets]):
        return []

    weather_data = first(load_weather_data() or [{}])
    weather_func = get_weather_conditions(weather_data)

    def create_missions():
        used_resources = set()
        for target, aircraft, pilot in product(_targets, _aircraft, _pilots):
            resource_tuple = (target, aircraft, pilot)
            if any(r in used_resources for r in resource_tuple):
                continue

            distance = calculate_distance(target)
            if not has_sufficient_fuel(aircraft, distance):
                continue

            mission = create_mission(weather_func, target, aircraft, pilot)
            used_resources.update(resource_tuple)
            yield mission

    return pipe(
        create_missions(),
        list,
        lambda missions: sorted(missions, key=lambda m: m.score, reverse=True),
        take(7),
        list
    )


def get_top_pilots(n: int) -> List[Pilot]:
    return pipe(
        _pilots,
        lambda pilots: sorted(pilots, key=lambda p: p.experience, reverse=True),
        take(n),
        list
    )

def get_long_range_aircraft() -> List[Aircraft]:
    return pipe(
        _aircraft,
        filter(lambda a: a.fuel_capacity > 5000),
        list
    )

def get_high_priority_targets() -> List[Target]:
    return pipe(
        _targets,
        filter(lambda t: t.priority > 8),
        list
    )

def analyze_mission_distances() -> Tuple[float, float, float]:
    distances = pipe(
        get_recommendations(),
        map(lambda m: m.distance),
        list
    )
    return (
        reduce(min, distances),
        reduce(max, distances),
        sum(distances) / len(distances) if distances else 0
    )

def group_missions_by_aircraft_type() -> dict:
    return pipe(
        get_recommendations(),
        partition(2),
        map(lambda group: (first(group).aircraft.type, list(pluck('target', group)))),
        dict
    )