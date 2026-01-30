import tkinter as tk
from tkinter import ttk
import random
import math

# --- PARAMÈTRES TECHNIQUES (Issus du PDF) ---
WIDTH, HEIGHT = 700, 500
CELL_SIZE = 5 
# Paramètres initiaux [cite: 416-432]
DEFAULTS = {
    "vitesse": 4.0,
    "evap": 0.95,
    "vision": 30,
    "quantite_phero": 15.0
}

class SimulationEngine:
    def __init__(self, root):
        self.root = root
        self.root.title("Ants Viewer v0.2 - Simulation OCF")
        self.root.configure(bg="#d9d9d9") # Gris industriel comme le cours 

        # 1. BARRE DE CONTRÔLE (TOP PANEL) [cite: 407, 485]
        self.top_panel = ttk.Frame(root, padding="5")
        self.top_panel.pack(side="top", fill="x")
        
        self.params = {}
        self._build_controls()

        # 2. ZONE DE SIMULATION (CANVAS)
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white", bd=2, relief="sunken")
        self.canvas.pack(padx=10, pady=5)
        
        # 3. ÉTAT DE L'ENVIRONNEMENT [cite: 134, 141]
        self.nest_pos = (80, 80)
        self.food_pos = (620, 420)
        self.grid = [[0.0 for _ in range(HEIGHT//CELL_SIZE + 1)] for _ in range(WIDTH//CELL_SIZE + 1)]
        self.obstacles = []
        
        self._init_world()
        
        # Agents [cite: 134, 444]
        self.ants = [AntAgent(self) for _ in range(25)]
        self.ant_ids = [self.canvas.create_oval(0,0,0,0, fill="black") for _ in self.ants]

        self.running = True
        self.update()

    def _build_controls(self):
        """Crée les widgets de contrôle mentionnés dans le cours [cite: 497-508]"""
        labels = [("Vitesse", "vitesse"), ("Évaporation", "evap"), ("Vision", "vision")]
        for i, (label, key) in enumerate(labels):
            ttk.Label(self.top_panel, text=label).grid(row=0, column=i*2, padx=5)
            var = tk.DoubleVar(value=DEFAULTS[key])
            scale = ttk.Scale(self.top_panel, from_=0.1 if key != "evap" else 0.8, 
                              to=10.0 if key != "evap" else 0.99, variable=var, orient="horizontal", length=80)
            scale.grid(row=0, column=i*2+1, padx=5)
            self.params[key] = var

        ttk.Button(self.top_panel, text="Stop/Run", command=self._toggle).grid(row=0, column=7, padx=20)

    def _init_world(self):
        # Dessin du Nid et de la Ressource [cite: 433, 434]
        self.canvas.create_oval(self.nest_pos[0]-15, self.nest_pos[1]-15, self.nest_pos[0]+15, self.nest_pos[1]+15, fill="#3366ff", outline="black")
        self.canvas.create_text(self.nest_pos[0], self.nest_pos[1]-25, text="NID", font=("Arial", 8, "bold"))
        
        self.canvas.create_rectangle(self.food_pos[0]-15, self.food_pos[1]-15, self.food_pos[0]+15, self.food_pos[1]+15, fill="#ff9933", outline="black")
        self.canvas.create_text(self.food_pos[0], self.food_pos[1]-25, text="RESSOURCE", font=("Arial", 8, "bold"))

        # Ajout d'obstacles (murs) [cite: 435, 521]
        wall = self.canvas.create_rectangle(250, 150, 270, 350, fill="black")
        self.obstacles.append((250, 150, 270, 350))

    def _toggle(self):
        self.running = not self.running

    def update(self):
        if self.running:
            # Évaporation (Rétroaction négative) [cite: 355, 369]
            evap = self.params["evap"].get()
            for x in range(len(self.grid)):
                for y in range(len(self.grid[0])):
                    self.grid[x][y] *= evap

            self.canvas.delete("phero")
            
            # Mise à jour agents [cite: 136, 185]
            for i, ant in enumerate(self.ants):
                ant.step()
                # Rendu visuel
                color = "#00ff00" if ant.has_food else "black"
                self.canvas.itemconfig(self.ant_ids[i], fill=color)
                self.canvas.coords(self.ant_ids[i], ant.x-2, ant.y-2, ant.x+2, ant.y+2)
                
                # Visualisation stigmergie (phéromones) [cite: 347, 512]
                if ant.has_food:
                    gx, gy = int(ant.x//CELL_SIZE), int(ant.y//CELL_SIZE)
                    if 0 <= gx < len(self.grid) and 0 <= gy < len(self.grid[0]):
                        self.grid[gx][gy] += 5.0
                        self.canvas.create_rectangle(gx*CELL_SIZE, gy*CELL_SIZE, (gx+1)*CELL_SIZE, (gy+1)*CELL_SIZE, 
                                                   fill="#ccd9ff", outline="", tags="phero")

        self.root.after(30, self.update)

class AntAgent:
    """Modèle d'agent avec perception de l'environnement [cite: 134, 136]"""
    def __init__(self, master):
        self.master = master
        self.x, self.y = master.nest_pos
        self.has_food = False
        self.angle = random.uniform(0, 2*math.pi)

    def step(self):
        speed = self.master.params["vitesse"].get()
        
        # Déplacement aléatoire + directionnelle [cite: 337]
        self.angle += random.uniform(-0.3, 0.3)
        
        new_x = self.x + math.cos(self.angle) * speed
        new_y = self.y + math.sin(self.angle) * speed

        # Collision Obstacles 
        hit_obstacle = False
        for obs in self.master.obstacles:
            if obs[0] <= new_x <= obs[2] and obs[1] <= new_y <= obs[3]:
                hit_obstacle = True
                break

        if not hit_obstacle and 0 < new_x < WIDTH and 0 < new_y < HEIGHT:
            self.x, self.y = new_x, new_y
        else:
            self.angle += math.pi # Rebond

        # Logique de récolte (Rationalité) [cite: 169, 185]
        if not self.has_food and math.hypot(self.x-self.master.food_pos[0], self.y-self.master.food_pos[1]) < 20:
            self.has_food = True
            self.angle += math.pi
        elif self.has_food and math.hypot(self.x-self.master.nest_pos[0], self.y-self.master.nest_pos[1]) < 20:
            self.has_food = False
            self.angle += math.pi

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationEngine(root)
    root.mainloop()