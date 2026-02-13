from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                             QSlider, QGroupBox)
from PyQt6.QtCore import Qt, pyqtSignal

class SettingGUI(QWidget):
    speed_changed = pyqtSignal(int)
    evaporation_changed = pyqtSignal(int)
    pause_clicked = pyqtSignal()
    reset_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Groupe contrôles
        sim_group = QGroupBox("Simulation")
        sim_layout = QVBoxLayout()
        
        self.btn_pause = QPushButton("Pause")
        self.btn_pause.clicked.connect(self.toggle_pause_text)
        self.btn_pause.clicked.connect(self.pause_clicked.emit)
        sim_layout.addWidget(self.btn_pause)

        self.btn_reset = QPushButton("Réinitialiser")
        self.btn_reset.clicked.connect(self.reset_clicked.emit)
        sim_layout.addWidget(self.btn_reset)
        
        sim_group.setLayout(sim_layout)
        layout.addWidget(sim_group)

        # Groupe paramètres
        param_group = QGroupBox("Paramètres")
        param_layout = QVBoxLayout()

        self.lbl_speed = QLabel("Vitesse Simulation")
        param_layout.addWidget(self.lbl_speed)
        
        self.slider_speed = QSlider(Qt.Orientation.Horizontal)
        self.slider_speed.setRange(1, 100)
        self.slider_speed.setValue(50)
        self.slider_speed.valueChanged.connect(self.speed_changed.emit)
        param_layout.addWidget(self.slider_speed)

        self.lbl_evap = QLabel("Taux Évaporation")
        param_layout.addWidget(self.lbl_evap)

        self.slider_evap = QSlider(Qt.Orientation.Horizontal)
        self.slider_evap.setRange(1, 20)
        self.slider_evap.setValue(5)
        self.slider_evap.valueChanged.connect(self.evaporation_changed.emit)
        param_layout.addWidget(self.slider_evap)

        param_group.setLayout(param_layout)
        layout.addWidget(param_group)

        layout.addStretch()

    def toggle_pause_text(self):
        if self.btn_pause.text() == "Pause":
            self.btn_pause.setText("Reprendre")
        else:
            self.btn_pause.setText("Pause")