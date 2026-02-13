class Resource:
    def __init__(self, x, y, quantity=100):
        self.x = x
        self.y = y
        self.quantity = quantity

    def take_food(self):
        """ Une fourmi prend de la nourriture """
        if self.quantity > 0:
            self.quantity -= 1
            return True
        return False