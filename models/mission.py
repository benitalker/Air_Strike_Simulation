from models.weather import Weather

def _cal_weather_score(weather: Weather) -> float:
    condition = weather.weather
    clouds = weather.clouds
    wind_speed = weather.wind_speed

    if condition == "Clear":
        score = 1.0
    elif condition == "Clouds":
        score = 0.7
    elif condition == "Rain":
        score = 0.4
    elif condition == "Stormy":
        score = 0.2
    else:
        score = 0

    score -= (clouds / 100) * 0.3
    score -= (wind_speed / 20) * 0.2

    return max(0, min(score, 1))

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
        distance_score = max(0, 100 - self.distance)
        aircraft_score = self.aircraft.calculate_total_score()
        pilot_score = self.pilot.skill
        weather_score1 = _cal_weather_score(self.weather_conditions)
        execution_time_score = 100

        # Weighted calculation
        score = (distance_score * 0.20 +
                 aircraft_score * 0.25 +
                 pilot_score * 0.25 +
                 weather_score1 * 0.20 +
                 execution_time_score * 0.10)
        return score

    def __str__(self) -> str:
        return (f"Target City: {self.target.city}, Priority: {self.target.priority}, "
                f"Assigned Pilot: {self.pilot.name}, Aircraft: {self.aircraft.type}, "
                f"Distance: {self.distance:.2f} km, Weather: {self.weather_conditions.weather}, "
                f"Pilot Skill: {self.pilot.skill}, Aircraft Speed: {self.aircraft.speed} km/h, "
                f"Fuel Capacity: {self.aircraft.fuel_capacity} L, Mission Fit Score: {self.score:.2f}, "
                f"Execution Time: {self.execution_time}")
