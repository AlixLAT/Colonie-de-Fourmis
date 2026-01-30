import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPainter, QColor
from simulation import SimulationEngine

class SimulationCanvas(QWidget):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.setFixedSize(800, 600)

    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Dessiner Phéromones [cite: 512]
        painter.setPen(Qt.PenStyle.NoPen)
        for p in self.engine.pheromones:
            painter.setBrush(QColor(100, 100, 255, 100))
            painter.drawEllipse(int(p.x), int(p.y), 4, 4)

        # Dessiner Obstacles [cite: 435]
        painter.setBrush(QColor("gray"))
        for o in self.engine.obstacles:
            painter.drawRect(o.x, o.y, o.w, o.h)

        # Dessiner Nid et Ressources [cite: 411, 413]
        painter.setBrush(QColor("blue"))
        painter.drawEllipse(self.engine.nest.x-15, self.engine.nest.y-15, 30, 30)
        painter.setBrush(QColor("green"))
        for r in self.engine.resources:
            painter.drawRect(r.x-15, r.y-15, 30, 30)

        # Dessiner Fourmis [cite: 444]
        for ant in self.engine.ants:
            painter.setBrush(QColor("orange" if ant.has_food else "black"))
            painter.drawEllipse(int(ant.x-3), int(ant.y-3), 6, 6)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.engine = SimulationEngine(800, 600)
        self.canvas = SimulationCanvas(self.engine)
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        
        # Contrôles [cite: 416, 428]
        self.sld_speed = QSlider(Qt.Orientation.Horizontal)
        self.sld_speed.setRange(1, 10)
        layout.addWidget(QLabel("Vitesse"))
        layout.addWidget(self.sld_speed)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(30)

    def tick(self):
        self.engine.update(self.sld_speed.value(), 0.98)
        self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())