class Aircraft:
    def __init__(self,type,speed,fuel_capacity):
        self.type = type
        self.speed = speed
        self.fuel_capacity = fuel_capacity
        self.speed_score = self._calculate_speed_score()
        self.fuel_score = self._calculate_fuel_score()

    def _calculate_speed_score(self):
        max_speed = 2000
        min_speed = 300
        normalized_speed = (self.speed - min_speed) / (max_speed - min_speed)
        return min(max(normalized_speed, 0), 1)

    def _calculate_fuel_score(self):
        max_fuel_capacity = 6000
        min_fuel_capacity = 500
        normalized_fuel_capacity = (self.fuel_capacity - min_fuel_capacity) / (max_fuel_capacity - min_fuel_capacity)
        return min(max(normalized_fuel_capacity, 0), 1)

    def calculate_total_score(self):
        speed_weight = 0.6
        fuel_weight = 0.4
        return self.speed_score * speed_weight + self.fuel_score * fuel_weight

    def __repr__(self):
        return f"Type: {self.type}, Speed: {self.speed}, Fuel Capacity: {self.fuel_capacity}"
