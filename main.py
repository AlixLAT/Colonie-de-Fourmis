import sys
from PyQt6.QtCore import QCoreApplication, QTimer
from DATA.Ant import Ant
from DATA.Nest import Nest
from DATA.Resource import Resource
from DATA.Obstacle import Obstacle

# Dimensions de l'écran
WIDTH = 800
HEIGHT = 600

def test_simulation():
    print("--- Démarrage du test des classes DATA ---")

    # Création de l'application (pour les signaux PyQt)
    app = QCoreApplication(sys.argv)

    # Création des objets du modèle
    nest = Nest(100, 100)
    food = Resource(700, 500)
    wall = Obstacle(400, 300, 50, 100) 
    
    # Liste vide pour les phéromones (simule le partage de données)
    pheromones_list = [] 
    
    # Création de la fourmi avec les limites de la carte et ses propriétés
    ant = Ant(
        start_x=nest.x, 
        start_y=nest.y, 
        width_limit=WIDTH, 
        height_limit=HEIGHT,
        nest=nest,                    
        pheromones_list=pheromones_list 
    )

    # Fonction pour recevoir le signal (SLOT)
    def on_ant_moved(x, y, has_food):
        # Cette fonction est appelée quand la fourmi bouge
        status = "Rentre au nid" if has_food else "Cherche"
        print(f"Signal reçu -> Fourmi en : ({x}, {y}) | Nourriture : {has_food} ({status})")

    # Connexion du signal de la fourmi
    ant.moved.connect(on_ant_moved)

    # Lancement du thread de la fourmi
    print("Lancement de la fourmi...")
    ant.start()

    # Arrêt automatique après 5 secondes
    QTimer.singleShot(5000, lambda: (ant.stop(), ant.join(), app.quit()))


    # Lancement de la boucle d'événements
    sys.exit(app.exec())

if __name__ == "__main__":
    test_simulation()