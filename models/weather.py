class Weather:
    def __init__(self, weather, clouds, wind_speed):

        self.weather = weather
        self.clouds = clouds
        self.wind_speed = wind_speed

    def __repr__(self):
        return f"weather: {self.weather}, clouds: {self.clouds}, wind_speed: {self.wind_speed}"
