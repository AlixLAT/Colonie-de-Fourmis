import sys
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QWidget
from PyQt6.QtCore import QTimer
from GUI.DisplayGUI import DisplayGUI
from GUI.SettingGUI import SettingGUI
from DATA.Ant import Ant
from DATA.Nest import Nest
from DATA.Resource import Resource
from DATA.Obstacle import Obstacle

def main():
    app = QApplication(sys.argv)
    
    main_window = QWidget()
    main_window.setWindowTitle("Test : Contournement d'Obstacle")
    layout = QHBoxLayout()
    main_window.setLayout(layout)

    display = DisplayGUI()
    settings = SettingGUI()

    layout.addWidget(display)
    layout.addWidget(settings)

    # SETUP SCÉNARIO
    nest = Nest(100, 300) # A gauche
    display.nest = nest
    
    display.resources = [Resource(700, 300, quantity=5000)] # A droite
    
    # Obstacle au centre
    obs_list = [Obstacle(350, 100, 50, 400)] 
    display.obstacles = obs_list
    
    display.pheromones = [] 
    
    ants = []
    for _ in range(50): # Nombre de fourmis 
        ant = Ant(
            start_x=nest.x, 
            start_y=nest.y, 
            width_limit=800, 
            height_limit=600, 
            nest=nest, 
            pheromones_list=display.pheromones, 
            obstacles_list=obs_list             
        )
        ants.append(ant)
    
    display.ants = ants

    def update_simulation():
        # Gestion Nourriture & Nid
        for ant in ants:
            # Interaction Ressource
            for res in display.resources:
                if not ant.has_food and res.quantity > 0:
                    if abs(ant.x - res.x) < 15 and abs(ant.y - res.y) < 15:
                        ant.pick_up_food()
                        res.take_food()
                        
        evap_rate = 0.01
            
        for p in display.pheromones:
            p.evaporate(evap_rate) 
        
        # Itère sur une copie [:] pour pouvoir supprimer dans l'original
        for p in display.pheromones[:]:
            if not p.active:
                display.pheromones.remove(p)

        display.update()

    print("Lancement des threads...")
    for ant in ants:
        ant.start()

    timer = QTimer()
    timer.timeout.connect(update_simulation)
    timer.start(16)

    main_window.show()
    exit_code = app.exec()
    
    for ant in ants:
        ant.stop()
        ant.join()
        
    sys.exit(exit_code)

if __name__ == "__main__":
    main()