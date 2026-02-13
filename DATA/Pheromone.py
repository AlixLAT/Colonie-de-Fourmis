class Pheromone:
    def __init__(self, x, y, intensity=2.0):
        self.x = x
        self.y = y
        self.intensity = intensity
        self.active = True

    def evaporate(self, rate):
        self.intensity -= rate
        if self.intensity <= 0:
            self.intensity = 0
            self.active = False
        return self.active

    def reinforce(self, amount):
        """ La fourmi repasse dessus : on fonce la couleur """
        self.intensity += amount
        
        if self.intensity > 30.0:
            self.intensity = 30.0
        self.active = True