class Obstacle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, px, py):
        """ Vérifi si une coordonnée (px, py) est dans l'obstacle """
        return self.x <= px <= self.x + self.w and self.y <= py <= self.y + self.h