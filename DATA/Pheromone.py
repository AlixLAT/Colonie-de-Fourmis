class Pheromone:
    def __init__(self, x, y, intensity=10.0):
        self.x = x
        self.y = y
        self.intensity = intensity
        self.active = True

    def evaporate(self, rate):
        """ Réduit l'intensité, retourne False si la phéromone a disparu"""
        self.intensity -= rate
        if self.intensity <= 0.1:
            self.intensity = 0
            self.active = False
        return self.active