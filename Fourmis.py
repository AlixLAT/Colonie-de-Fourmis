import tkinter as tk
import random
import math

# --- CONFIGURATION (Inspirée du cahier des charges) ---
WIDTH, HEIGHT = 600, 500
CELL_SIZE = 10  # Grille pour la gestion des phéromones [cite: 207]
ANT_COUNT = 25
EVAP_RATE = 0.92 # Rétroaction négative [cite: 355]

class Environment:
    """Gère l'espace, les ressources et les traces chimiques [cite: 134, 199]"""
    def __init__(self):
        self.grid = [[0.0 for _ in range(HEIGHT//CELL_SIZE)] for _ in range(WIDTH//CELL_SIZE)]
        self.nest = (50, 50)
        self.food = (550, 450)

    def deposit(self, x, y, amount):
        gx, gy = int(x//CELL_SIZE), int(y//CELL_SIZE)
        if 0 <= gx < len(self.grid) and 0 <= gy < len(self.grid[0]):
            self.grid[gx][gy] += amount # Rétroaction positive [cite: 366]

    def evaporate(self):
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                self.grid[x][y] *= EVAP_RATE # Diminution graduelle [cite: 355]

class AntAgent:
    """Agent Rationnel : Perçoit, Décide, Agit [cite: 134, 185]"""
    def __init__(self, env):
        self.env = env
        self.x, self.y = env.nest
        self.has_food = False
        self.angle = random.uniform(0, 2*math.pi)

    def sense_and_act(self):
        # 1. PERCEPTION & DÉCISION [cite: 136, 184]
        if not self.has_food:
            self._explore()
        else:
            self._return_to_nest()
        
        # 2. ACTION : Mise à jour de la position [cite: 143]
        self.x += math.cos(self.angle) * 4
        self.y += math.sin(self.angle) * 4
        
        # Gestion des bords
        self.x = max(0, min(WIDTH-5, self.x))
        self.y = max(0, min(HEIGHT-5, self.y))

    def _explore(self):
        # Si proche nourriture : collecte [cite: 342]
        if math.hypot(self.x - self.env.food[0], self.y - self.env.food[1]) < 20:
            self.has_food = True
            self.angle += math.pi
        else:
            # Stigmergie : attirée par les phéromones existantes [cite: 343]
            self.angle += random.uniform(-0.4, 0.4)

    def _return_to_nest(self):
        # Si porte nourriture : dépose phéromone (Stigmergie) [cite: 340, 342]
        self.env.deposit(self.x, self.y, 10.0)
        
        # Direction vers le nid (Comportement rationnel) [cite: 169]
        dx, dy = self.env.nest[0] - self.x, self.env.nest[1] - self.y
        target_angle = math.atan2(dy, dx)
        self.angle = target_angle # Chemin direct [cite: 494]
        
        if math.hypot(dx, dy) < 20:
            self.has_food = False
            self.angle += math.pi

class SimulationEngine:
    def __init__(self, root):
        self.env = Environment()
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#f0f0f0")
        self.canvas.pack()
        
        # Dessin statique environnement [cite: 149]
        self.canvas.create_oval(self.env.nest[0]-15, self.env.nest[1]-15, 
                               self.env.nest[0]+15, self.env.nest[1]+15, fill="blue")
        self.canvas.create_rectangle(self.env.food[0]-15, self.env.food[1]-15, 
                                    self.env.food[0]+15, self.env.food[1]+15, fill="orange")

        self.agents = [AntAgent(self.env) for _ in range(ANT_COUNT)]
        self.agent_shapes = [self.canvas.create_oval(0,0,0,0, fill="black") for _ in self.agents]
        
        self.run()

    def run(self):
        self.env.evaporate() # Rétroaction négative [cite: 369]
        self.canvas.delete("phero_visual") # Rafraîchir l'affichage

        # Affichage des phéromones (Stigmergie visuelle) [cite: 512]
        for x in range(len(self.env.grid)):
            for y in range(len(self.env.grid[0])):
                val = self.env.grid[x][y]
                if val > 0.5:
                    alpha = min(int(val * 10), 255)
                    color = f'#{255-alpha:02x}ffff' # Bleu dégradé
                    self.canvas.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, 
                                               (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, 
                                               fill=color, outline="", tags="phero_visual")
        
        # Mise à jour des agents
        for i, agent in enumerate(self.agents):
            agent.sense_and_act()
            color = "green" if agent.has_food else "black"
            self.canvas.itemconfig(self.agent_shapes[i], fill=color)
            self.canvas.coords(self.agent_shapes[i], agent.x-2, agent.y-2, agent.x+2, agent.y+2)
            self.canvas.tag_raise(self.agent_shapes[i])

        self.canvas.after(40, self.run)

if __name__ == "__main__":
    root = tk.Tk()
    SimulationEngine(root)
    root.mainloop()