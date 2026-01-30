import sys
import random
import math
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QSlider, QLabel, QPushButton, QFrame)
from PyQt6.QtCore import QTimer, Qt, QRectF
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen

# --- CONFIGURATION (PDF) ---
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10 
NEST_POS = (100, 100) # [cite: 149]
FOOD_POS = (700, 500) # [cite: 149]

class AntAgent:
    """Agent Rationnel : Perçoit et Agit [cite: 134, 185]"""
    def __init__(self):
        self.x, self.y = NEST_POS
        self.has_food = False
        self.angle = random.uniform(0, 2 * math.pi)

    def step(self, speed, obstacles):
        # Mouvement aléatoire (Exploration) [cite: 337]
        self.angle += random.uniform(-0.5, 0.5)
        
        new_x = self.x + math.cos(self.angle) * speed
        new_y = self.y + math.sin(self.angle) * speed

        # Gestion des collisions et bordures [cite: 522]
        if 0 < new_x < WIDTH and 0 < new_y < HEIGHT:
            self.x, self.y = new_x, new_y
        else:
            self.angle += math.pi

        # Logique de récolte (Stigmergie) [cite: 342, 343]
        dist_food = math.hypot(self.x - FOOD_POS[0], self.y - FOOD_POS[1])
        if not self.has_food and dist_food < 30:
            self.has_food = True
            self.angle += math.pi # Demi-tour

        dist_nest = math.hypot(self.x - NEST_POS[0], self.y - NEST_POS[1])
        if self.has_food and dist_nest < 30:
            self.has_food = False
            self.angle += math.pi

class SimulationCanvas(QFrame):
    """Zone de rendu graphique [cite: 401]"""
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(WIDTH, HEIGHT)
        self.setStyleSheet("background-color: white; border: 1px solid #999;")
        
        self.parent = parent
        self.ants = [AntAgent() for _ in range(30)]
        self.grid = [[0.0 for _ in range(HEIGHT//CELL_SIZE + 1)] for _ in range(WIDTH//CELL_SIZE + 1)]

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 1. Dessiner les Phéromones (Stigmergie) [cite: 347, 512]
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                val = self.grid[x][y]
                if val > 0.1:
                    color_val = min(int(val * 15), 255)
                    painter.fillRect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE, 
                                   QColor(200, 220, 255, color_val))

        # 2. Dessiner le Nid et la Nourriture [cite: 411, 413]
        painter.setBrush(QColor("blue"))
        painter.drawEllipse(NEST_POS[0]-15, NEST_POS[1]-15, 30, 30)
        
        painter.setBrush(QColor("orange"))
        painter.drawRect(FOOD_POS[0]-15, FOOD_POS[1]-15, 30, 30)

        # 3. Dessiner les Fourmis (Agents) [cite: 444]
        for ant in self.ants:
            color = QColor("green") if ant.has_food else QColor("black")
            painter.setBrush(color)
            painter.drawEllipse(int(ant.x-3), int(ant.y-3), 6, 6)

class MainWindow(QMainWindow):
    """Interface principale type 'Ants Viewer' """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ants Viewer v0.3 - PyQt Edition")
        
        main_layout = QHBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Simulation
        self.canvas = SimulationCanvas(self)
        main_layout.addWidget(self.canvas)

        # Panneau de contrôle (Design Ingé) [cite: 410-432]
        ctrl_panel = QVBoxLayout()
        main_layout.addLayout(ctrl_panel)

        self.speed_slider = self._add_control(ctrl_panel, "Vitesse", 1, 10, 4)
        self.evap_slider = self._add_control(ctrl_panel, "Évaporation (%)", 80, 99, 95)
        
        self.btn_run = QPushButton("Start / Pause")
        self.btn_run.clicked.connect(self.toggle_sim)
        ctrl_panel.addWidget(self.btn_run)
        ctrl_panel.addStretch()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_sim)
        self.is_running = False

    def _add_control(self, layout, name, min_v, max_v, def_v):
        layout.addWidget(QLabel(name))
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(min_v, max_v)
        slider.setValue(def_v)
        layout.addWidget(slider)
        return slider

    def toggle_sim(self):
        self.is_running = not self.is_running
        if self.is_running: self.timer.start(30)
        else: self.timer.stop()

    def update_sim(self):
        speed = self.speed_slider.value()
        evap = self.evap_slider.value() / 100.0

        # Évaporation [cite: 355]
        for x in range(len(self.canvas.grid)):
            for y in range(len(self.canvas.grid[0])):
                self.canvas.grid[x][y] *= evap

        # Mise à jour agents
        for ant in self.canvas.ants:
            ant.step(speed, [])
            if ant.has_food:
                gx, gy = int(ant.x//CELL_SIZE), int(ant.y//CELL_SIZE)
                if 0 <= gx < len(self.canvas.grid) and 0 <= gy < len(self.canvas.grid[0]):
                    self.canvas.grid[gx][gy] += 5.0 # Dépôt [cite: 340]

        self.canvas.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())