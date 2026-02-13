class Nest:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.food_collected = 0

    def deposit_food(self):
        """ Une fourmi dépose de la nourriture """
        self.food_collected += 1