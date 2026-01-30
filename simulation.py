from models import Ant, Nest, Resource, Obstacle, Pheromone
import math

class SimulationEngine:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.nest = Nest(100, 100)
        self.ants = [Ant(self.nest) for _ in range(30)]
        self.resources = [Resource(700, 500)]
        self.obstacles = [Obstacle(350, 250, 100, 100)] # Obstacle central [cite: 435]
        self.pheromones = []

    def update(self, speed_mult, evap_rate):
        for ant in self.ants:
            ant.speed = speed_mult
            ant.move(self.obstacles, self.width, self.height)

            # Logique de récolte [cite: 342]
            for res in self.resources:
                if not ant.has_food and math.hypot(ant.x - res.x, ant.y - res.y) < 20:
                    ant.has_food = True
                    ant.angle += math.pi
            
            # Retour au nid [cite: 494]
            if ant.has_food and math.hypot(ant.x - self.nest.x, ant.y - self.nest.y) < 20:
                ant.has_food = False
                self.nest.food_collected += 1
                ant.angle += math.pi
            
            # Dépôt de phéromones [cite: 340]
            if ant.has_food:
                self.pheromones.append(Pheromone(ant.x, ant.y))

        # Évaporation [cite: 355, 499]
        self.pheromones = [p for p in self.pheromones if p.evaporate(evap_rate)]