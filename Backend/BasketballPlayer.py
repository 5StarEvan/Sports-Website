import Player

class BasketballPlayer(Player.Player):
    def __init__(self, name, age, team, sport, position, ppg, apg, rpg, spg, bpg, tpg, fpg, fgptc):
        super().__init__(name, age, team, "Basketball", position)
        self.ppg = ppg
        self.apg = apg
        self.rpg = rpg
        self.spg = spg
        self.bpg = bpg
        self.tpg = tpg
        self.fpg = fpg
        self.fgptc = fgptc
    
    def get_ppg(self):
        return self.ppg
    
    def get_apg(self):
        return self.apg
    
    def get_rpg(self):
        return self.rpg

    def get_spg(self):
        return self.spg
    
    def get_bpg(self):
        return self.bpg
    
    def get_tpg(self):
        return self.tpg
    
    def get_fpg(self):
        return self.fpg
    
    def get_fgptc(self):
        return self.fgptc
    
    def set_ppg(self, ppg):
        self.ppg = ppg
    
    def set_apg(self, apg):
        self.apg = apg
    
    def set_rpg(self, rpg):
        self.rpg = rpg
    
    def set_spg(self, spg): 
        self.spg = spg
    
    def set_bpg(self, bpg):
        self.bpg = bpg
    
    def set_tpg(self, tpg):
        self.tpg = tpg
    
    def set_fpg(self, fpg):
        self.fpg = fpg
    
    def set_fgptc(self, fgptc):
        self.fgptc = fgptc
    
    def __str__(self): 
        return f"{self.name} is {self.age} years old and plays for {self.team} as a {self.position} with {self.ppg} points per game, {self.apg} assists per game, {self.rpg} rebounds per game, {self.spg} steals per game, {self.bpg} blocks per game, {self.tpg} turnovers per game, {self.fpg} free throws per game, {self.fgptc} field goal %"
    
    def __repr__(self):
        return f"BasketballPlayer(name={self.name}, age={self.age}, team={self.team}, sport={self.sport}, position={self.position}, ppg={self.ppg}, apg={self.apg}, rpg={self.rpg}, spg={self.spg}, bpg={self.bpg}, tpg={self.tpg}, fpg={self.fpg}, fgptc={self.fgptc})"
