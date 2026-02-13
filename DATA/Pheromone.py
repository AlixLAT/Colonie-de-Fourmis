class Pheromone:
    def __init__(self, x, y, intensity=10.0):
        self.x, self.y = x, y
        self.intensity = intensity

    def evaporate(self, rate):
        self.intensity *= rate
        return self.intensity > 0.1