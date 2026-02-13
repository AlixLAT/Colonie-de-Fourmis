Colonie-de-Fourmis (branch: jade)
│
├── CONTROLER/  				# Fonctions du contrôleur (vitesse, évaporation, nombre, obstacle)                  
│   ├── DisplayControler.py		# Affichage de la partie graphique du contrôleur 
│   └── SettingControler.py		# Gestion des paramètres du contrôleur
│
├── DATA/                     	# Principales Classes
│   ├── Ant.py           			# Classe définissant le comportement d'une fourmi (run, stop, speed)
│   ├── Nest.py            		# Classe définissant le comportement d'un nid de Fourmi (food, isCollected)
│   ├── Obstacle.py            	# Classe définissant le comportement d'un obstacle (color, contains, location)
│   ├── Pheromone.py           	# Classe définissant le comportement d'un pheromone (evaporation, intensity)
│   └── Pesource.py            	# Classe définissant le comportement d'une ressource (quantite, location) 
│
├── GUI/                   		# Interface graphique (avec la lib PyQt) 
│   ├── DisplayGUI.py               # Affichage de la partie de la colonie (fourmilière)
│   └── SettingGUI.py            	 # Gestion des paramètres de l'affichage principal 
│
├── main.py                 	 # Point d'entrée du programme
└── README.md                	 # Documentation du projet (ce document)
