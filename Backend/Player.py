class Player:
    def __init__(self, name, age, team, sport, position):
        self.name = name
        self.age = age
        self.team = team
        self.sport = sport
        self.position = position

    def __str__(self):
        return f"{self.name} is {self.age} years old and plays for {self.team}"
    
    def __repr__(self):
        return f"Player(name={self.name}, age={self.age}, team={self.team})"
    
    def get_name(self):
        return self.name
    
    def get_age(self):
        return self.age
    
    def get_team(self):
        return self.team
    
    def get_sport(self):
        return self.sport
    
    def get_position(self):
        return self.position
    
    def set_name(self, name):
        self.name = name
    
    def set_age(self, age):
        self.age = age
    
    def set_team(self, team):
        self.team = team
    
