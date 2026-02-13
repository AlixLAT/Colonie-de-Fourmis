import threading
import random
import time

from PyQt6.QtWidgets import QApplication, QWidget
# from PyQt6.QtGui import QPainter, QPen, QBrush
from PyQt6.QtCore import Qt, QObject, pyqtSignal


WIDTH = 800
HEIGHT = 600

class Ant(threading.Thread, QObject):
    moved = pyqtSignal(int, int)

    def __init__(self):
        QObject.__init__(self)
        threading.Thread.__init__(self)

        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.vitesse = 8
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])

            if dx == 0 and dy == 0:
                continue

            self.x = max(0, min(WIDTH - 1, self.x + dx * self.vitesse))
            self.y = max(0, min(HEIGHT - 1, self.y + dy * self.vitesse))

            self.moved.emit(self.x, self.y)

            time.sleep(0.05)

    def stop(self):
        self.stop_event.set()

    def return_to_nest(self):
        return ""

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ant")
        self.setFixedSize(WIDTH, HEIGHT)

        self.path = []

        self.ant = Ant()
        self.ant.moved.connect(self.update_position)
        self.ant.start()

    def update_position(self, x, y):
        self.path.append((x, y))
        self.update()  # déclenche paintEvent

    def paintEvent(self, event):
        painter = QPainter(self)

        # dessiner le trajet
        painter.setPen(QPen(Qt.GlobalColor.black, 2))

        for i in range(1, len(self.path)):
            x1, y1 = self.path[i - 1]
            x2, y2 = self.path[i]
            painter.drawLine(x1, y1, x2, y2)

        # dessiner la fourmi
        if self.path:
            x, y = self.path[-1]
            painter.setPen(QPen(Qt.GlobalColor.red))
            painter.setBrush(Qt.GlobalColor.red)
            painter.drawEllipse(x - 6, y - 6, 12, 12)

    def closeEvent(self, event):
        self.ant.stop()
        self.ant.join()
        event.accept()
    
if __name__ == "__main__" :  
    ant = Ant()
    ant.start()
    time.sleep(10)
    ant.stop()
    ant.join()
    
    import sys
    
    # 1. Créer l'application PyQt
    app = QApplication(sys.argv)
    
    # 2. Créer et afficher la fenêtre
    # La classe Window s'occupe déjà de créer et lancer le thread 'Ant'
    win = Window()
    win.show()
    
    # 3. Lancer la boucle d'exécution de l'interface
    sys.exit(app.exec())