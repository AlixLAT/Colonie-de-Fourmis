import threading
import random
import time
import math
from PyQt6.QtCore import QObject, pyqtSignal
from DATA.Pheromone import Pheromone

class Ant(QObject, threading.Thread):
    moved = pyqtSignal(int, int, bool)
    
    def __init__(self, start_x, start_y, width_limit, height_limit, nest=None, pheromones_list=None, obstacles_list=None):
        QObject.__init__(self)
        threading.Thread.__init__(self)
        
        self.x = start_x
        self.y = start_y
        self.max_x = width_limit
        self.max_y = height_limit
        self.nest = nest
        self.pheromones = pheromones_list if pheromones_list is not None else []
        self.obstacles = obstacles_list if obstacles_list is not None else []
        self.has_food = False 
        self.speed = 0.01 
        self.sensor_radius = 60
        self.dx = 0
        self.dy = 0
        self.escape_countdown = 0
        self.locked_dx = 0
        self.locked_dy = 0
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            
            # Cas A : RENTRER AU NID (Dépose la piste initiale)
            if self.has_food:
                # dépose une trace "Claire" (intensité défaut = 2.0)
                if random.random() < 0.4: 
                    self.pheromones.append(Pheromone(self.x, self.y))

                if self.escape_countdown > 0:
                    self.handle_escape()
                elif self.nest:
                    target_dx, target_dy = self.move_towards(self.nest.x, self.nest.y)
                    if self.is_not_blocked(self.x + target_dx, self.y + target_dy):
                        self.dx, self.dy = target_dx, target_dy
                    else:
                        self.start_contouring(target_dx, target_dy)

            # Cas B : CHERCHER (Suit et Renforce)
            else:
                target_pheromone = self.sense_pheromones()
                
                if target_pheromone and self.escape_countdown == 0:
                    # Si décide de suivre cette phéromone, la renforce
                    # la rends plus rouge pour les suivantes
                    target_pheromone.reinforce(1.5) # +1.5 d'intensité à chaque passage
                    
                    p_dx, p_dy = self.move_towards(target_pheromone.x, target_pheromone.y)
                    if self.is_not_blocked(self.x + p_dx, self.y + p_dy):
                        self.dx, self.dy = p_dx, p_dy
                    else:
                        self.start_contouring(p_dx, p_dy, duration=10)
                else:
                    if self.escape_countdown > 0: 
                        self.handle_escape()
                    else:
                        if random.random() < 0.1:
                            self.random_move()

            # Déplacement
            next_x = self.x + self.dx
            next_y = self.y + self.dy
            
            if not (0 <= next_x <= self.max_x):
                self.dx = -self.dx
                next_x = self.x 
                self.escape_countdown = 0
            if not (0 <= next_y <= self.max_y):
                self.dy = -self.dy
                next_y = self.y
                self.escape_countdown = 0

            if self.is_not_blocked(next_x, next_y):
                self.x = next_x
                self.y = next_y
            else:
                self.dx = -self.dx
                self.dy = -self.dy
                self.start_contouring()

            self.moved.emit(self.x, self.y, self.has_food)
            time.sleep(self.speed)

    def handle_escape(self):
        self.escape_countdown -= 1
        if self.is_not_blocked(self.x + self.locked_dx, self.y + self.locked_dy):
            self.dx, self.dy = self.locked_dx, self.locked_dy
        else:
            self.start_contouring()

    def sense_pheromones(self):
        best_p = None
        max_intensity = -1
        
        # Distance de la fourmi au nid
        my_dist_to_nest = math.sqrt((self.x - self.nest.x)**2 + (self.y - self.nest.y)**2)
        
        for p in self.pheromones:
            if not p.active: continue
            
            dist = math.sqrt((self.x - p.x)**2 + (self.y - p.y)**2)
            
            if 10 < dist < self.sensor_radius:
                # FILTRE : suit que celles qui éloignent du nid (vers ressource)
                p_dist_to_nest = math.sqrt((p.x - self.nest.x)**2 + (p.y - self.nest.y)**2)
                
                if p_dist_to_nest < my_dist_to_nest:
                    continue 

                if p.intensity > max_intensity:
                    max_intensity = p.intensity
                    best_p = p
        
        return best_p

    def start_contouring(self, blocked_dx=0, blocked_dy=0, duration=25):
        self.escape_countdown = duration
        candidates = []
        if blocked_dx != 0: candidates = [(0, 2), (0, -2)]
        elif blocked_dy != 0: candidates = [(2, 0), (-2, 0)]
        else: candidates = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(candidates)
        
        found = False
        for c_dx, c_dy in candidates:
            if self.is_not_blocked(self.x + c_dx, self.y + c_dy):
                self.locked_dx = c_dx
                self.locked_dy = c_dy
                found = True
                break
        
        if not found:
            self.locked_dx = -blocked_dx if blocked_dx != 0 else random.choice([-2, 2])
            self.locked_dy = -blocked_dy if blocked_dy != 0 else random.choice([-2, 2])
        
        self.dx = self.locked_dx
        self.dy = self.locked_dy

    def random_move(self):
        self.dx = random.choice([-2, -1, 0, 1, 2])
        self.dy = random.choice([-2, -1, 0, 1, 2])
        if self.dx == 0 and self.dy == 0: self.dx = 2

    def is_not_blocked(self, x, y):
        for obs in self.obstacles:
            if obs.contains(x, y):
                return False
        return True

    def move_towards(self, target_x, target_y):
        dx, dy = 0, 0
        if self.x < target_x: dx = 2
        elif self.x > target_x: dx = -2
        if self.y < target_y: dy = 2
        elif self.y > target_y: dy = -2
        if random.random() < 0.1:
            dx += random.choice([-1, 0, 1])
            dy += random.choice([-1, 0, 1])
        return dx, dy
    
    def stop(self): self.stop_event.set()
    def pick_up_food(self): self.has_food = True; self.dx = -self.dx; self.dy = -self.dy; self.escape_countdown = 0
    def drop_food(self): self.has_food = False; self.dx = -self.dx; self.dy = -self.dy; self.escape_countdown = 0