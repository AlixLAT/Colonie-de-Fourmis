import math
import random

class Pheromone:
    def __init__(self, x, y, intensity=10.0):
        self.x, self.y = x, y
        self.intensity = intensity

    def evaporate(self, rate):
        self.intensity *= rate
        return self.intensity > 0.1

class Resource:
    def __init__(self, x, y, quantity=100):
        self.x, self.y = x, y
        self.quantity = quantity

class Obstacle:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    def contains(self, px, py):
        return self.x <= px <= self.x + self.w and self.y <= py <= self.y + self.h

class Nest:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.food_collected = 0

class Ant:
    def __init__(self, nest):
        self.nest = nest
        self.x, self.y = nest.x, nest.y
        self.has_food = False
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = 2.0

    def move(self, obstacles, width, height):
        # Mouvement aléatoire (Exploration) [cite: 337]
        self.angle += random.uniform(-0.5, 0.5)
        nx = self.x + math.cos(self.angle) * self.speed
        ny = self.y + math.sin(self.angle) * self.speed

        # Collision murs et obstacles [cite: 521, 522]
        collision = any(o.contains(nx, ny) for o in obstacles)
        if 0 <= nx <= width and 0 <= ny <= height and not collision:
            self.x, self.y = nx, ny
        else:
            self.angle += math.pi # Rebond
        
    def return_to_nest(self):
        if self.mode_soleil:
            # Calcul de l'angle direct vers les coordonnées du nid
            self.angle = math.atan2(self.nest.y - self.y, self.nest.x - self.x)
        else:
            # Logique de détection des phéromones environnantes pour choisir la direction
            self.angle = self.detect_strongest_pheromone()