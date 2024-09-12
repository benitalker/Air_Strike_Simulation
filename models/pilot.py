class Pilot:
    def __init__(self, name, skill):
        self.name = name  # No tuple
        self.skill = skill  # No tuple

    def __repr__(self):
        return f"Name: {self.name}, Skill: {self.skill}"
