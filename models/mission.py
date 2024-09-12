from models.weather import Weather
from toolz import curry, compose
from toolz.curried import get

weather_scores = {
    "Clear": 1.0,
    "Clouds": 0.7,
    "Rain": 0.4,
    "Stormy": 0.2
}

@curry
def adjust_score(factor, max_value, value, score):
    return score - (value / max_value) * factor

cloud_adjustment = adjust_score(0.3, 100)
wind_adjustment = adjust_score(0.2, 20)

def _cal_weather_score(weather: Weather) -> float:
    return compose(
        lambda x: max(0, min(x, 1)),
        wind_adjustment(weather.wind_speed),
        cloud_adjustment(weather.clouds),
        get(weather.weather, default=0)
    )(weather_scores)

class Mission:
    def __init__(self, target, aircraft, pilot, weather_conditions, distance, execution_time):
        self.target = target
        self.aircraft = aircraft
        self.pilot = pilot
        self.weather_conditions = weather_conditions
        self.distance = distance
        self.execution_time = execution_time
        self.score = self.calculate_score()

    def calculate_score(self) -> float:
        scores = {
            'distance': max(0, 100 - self.distance),
            'aircraft': self.aircraft.calculate_total_score(),
            'pilot': self.pilot.skill,
            'weather': _cal_weather_score(self.weather_conditions),
            'execution_time': 100
        }
        weights = {
            'distance': 0.20,
            'aircraft': 0.25,
            'pilot': 0.25,
            'weather': 0.20,
            'execution_time': 0.10
        }
        return sum(scores[key] * weights[key] for key in scores)

    def __str__(self) -> str:
        return (f"Target City: {self.target.city}, Priority: {self.target.priority}, "
                f"Assigned Pilot: {self.pilot.name}, Aircraft: {self.aircraft.type}, "
                f"Distance: {self.distance:.2f} km, Weather: {self.weather_conditions.weather}, "
                f"Pilot Skill: {self.pilot.skill}, Aircraft Speed: {self.aircraft.speed} km/h, "
                f"Fuel Capacity: {self.aircraft.fuel_capacity} L, Mission Fit Score: {self.score:.2f}, "
                f"Execution Time: {self.execution_time}")