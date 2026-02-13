import threading
import random
import time
import math
from PyQt6.QtCore import QObject, pyqtSignal

class Ant(QObject, threading.Thread):
    """ Signal émis quand la fourmi bouge : envoie x y et si elle porte de la nourriture """
    moved = pyqtSignal(int, int, bool)
    
    def __init__(self, start_x, start_y, width_limit, height_limit, nest=None, pheromones_list=None):
        QObject.__init__(self)
        threading.Thread.__init__(self)
        
        # Position et limites 
        self.x = start_x
        self.y = start_y
        self.max_x = width_limit
        self.max_y = height_limit
        
        # Références vers le monde (nid phéromones)
        self.nest = nest
        self.pheromones = pheromones_list if pheromones_list is not None else []
        
        # État de la fourmi
        self.has_food = False # False = Cherche, True = Rentre au nid
        self.sensor_radius = 60
        self.speed = 0.05 # Temps de pause entre deux pas
        
        self.stop_event = threading.Event()


    def run(self):
        """ Boucle principale du thread de la fourmi """
        while not self.stop_event.is_set():
            dx, dy = 0, 0

            # COMPORTEMENT 1 : rentre au nid
            if self.has_food and self.nest:
                # Ignore les phéromones, rentre en ligne
                dx, dy = self.move_towards(self.nest.x, self.nest.y)

            # COMPORTEMENT 2 : suivre les phéromones
            else:
                target_pheromone = self.sense_pheromones()
                
                if target_pheromone:
                    # Si la fourmis sent une trace
                    dx, dy = self.move_towards(target_pheromone.x, target_pheromone.y)
                else:
                    # COMPORTEMENT 3 : exploration au hasard
                    dx = random.choice([-2, -1, 0, 1, 2])
                    dy = random.choice([-2, -1, 0, 1, 2])

            # Si le mouvement est nul, force le hasard
            if dx == 0 and dy == 0:
                 dx = random.choice([-1, 1])
                 dy = random.choice([-1, 1])

            # Calcul nouvelle position (avec vérif des bords)
            new_x = max(0, min(self.max_x, self.x + dx))
            new_y = max(0, min(self.max_y, self.y + dy))

            self.x = new_x
            self.y = new_y

            # Émission du signal pour prévenir l'interface graphique (et le controller)
            self.moved.emit(self.x, self.y, self.has_food)

            # Pause (vitesse de simulation)
            time.sleep(self.speed)
    
    
    def sense_pheromones(self):
        """ Cherche la phéromone la plus intense dans le rayon de détection """
        best_p = None
        max_intensity = -1
        
        # On copie la liste pour éviter une erreur si un élément est supprimé pendant la boucle
        current_pheromones = self.pheromones[:] 

        for p in current_pheromones:
            if not p.active:
                continue

            # Calcul de distance (Pythagore)
            dist = math.sqrt((self.x - p.x)**2 + (self.y - p.y)**2)
            
            if dist < self.sensor_radius and dist > 5: # >5 pour ne pas tourner en rond sur soi-même
                # Privilégie la phéromone la plus forte
                if p.intensity > max_intensity:
                    max_intensity = p.intensity
                    best_p = p
        
        return best_p


    def move_towards(self, target_x, target_y):
        """ Calcule dx, dy pour aller vers une cible """
        dx, dy = 0, 0
        
        if self.x < target_x: dx = 2
        elif self.x > target_x: dx = -2
        
        if self.y < target_y: dy = 2
        elif self.y > target_y: dy = -2
        
        # Ajout d'un petit bruit aléatoire
        if random.random() < 0.2: # 20% de chance de dévier un peu
            dx += random.choice([-1, 0, 1])
            dy += random.choice([-1, 0, 1])
            
        return dx, dy
            

    def stop(self):
        """ Arrête le thread """
        self.stop_event.set()


    def pick_up_food(self):
        """ Est appelé quand la fourmi trouve une ressource """
        self.has_food = True
        
        
    def drop_food(self):
        """ Est appelé quand la fourmi arrive au nid"""
        self.has_food = False