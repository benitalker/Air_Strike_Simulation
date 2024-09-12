class Target:
    def __init__(self, city, priority, lat, lon):
        self.city = city
        self.priority = priority
        self.lat = lat
        self.lon = lon


    def __repr__(self):
        return f"City: {self.city}, Priority: {self.priority}, Lat: {self.lat}, Lon: {self.lon}"
