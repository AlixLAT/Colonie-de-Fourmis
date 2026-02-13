import sys
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QBrush, QColor, QPen
from PyQt6.QtCore import Qt, pyqtSignal

class DisplayGUI(QWidget):
    obstacle_added = pyqtSignal(int, int)

    def __init__(self, width=800, height=600):
        super().__init__()
        self.setFixedSize(width, height)
        self.ants = []        
        self.resources = []   
        self.pheromones = []  
        self.obstacles = []   
        self.nest = None      
        self.background_color = QColor(240, 240, 240)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Fond
        painter.fillRect(self.rect(), self.background_color)

        # Phéromones (Rouge Progressif)
        painter.setPen(Qt.PenStyle.NoPen)
        for p in self.pheromones:
            if p.active:
                # Calcul progressif
                # Intensité 2.0 (départ) -> 2 * 20 = 40 (Très clair)
                # Intensité 12.0 (renforcé) -> 12 * 20 = 240 (Presque opaque)
                alpha = int(min(255, max(20, p.intensity * 20)))
                
                painter.setBrush(QColor(255, 0, 0, alpha))
                painter.drawEllipse(int(p.x) - 2, int(p.y) - 2, 5, 5)

        # Obstacles
        painter.setPen(Qt.PenStyle.SolidLine)
        painter.setBrush(QColor(80, 80, 80))
        for o in self.obstacles:
            painter.drawRect(o.x, o.y, o.w, o.h)

        # Nid
        if self.nest:
            painter.setBrush(QColor("blue"))
            painter.drawEllipse(self.nest.x - 15, self.nest.y - 15, 30, 30)

        # Ressources
        painter.setBrush(QColor("green"))
        for r in self.resources:
            if r.quantity > 0:
                size = 30 if r.quantity > 50 else 15
                painter.drawRect(r.x - size//2, r.y - size//2, size, size)

        # Fourmis
        for ant in self.ants:
            color = QColor("orange") if ant.has_food else QColor("black")
            painter.setBrush(color)
            painter.drawEllipse(int(ant.x) - 3, int(ant.y) - 3, 6, 6)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.obstacle_added.emit(event.pos().x(), event.pos().y())
    def mouseMoveEvent(self, event):
        self.obstacle_added.emit(event.pos().x(), event.pos().y())