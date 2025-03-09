from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt


class StatusBar(QWidget):
    """Status bar displaying character stats and time of day."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("statusBar")
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        
        # Health bar
        health_label = QLabel("Health:", self)
        self.health_bar = QProgressBar(self)
        self.health_bar.setObjectName("healthBar")
        self.health_bar.setTextVisible(True)
        self.health_bar.setRange(0, 100)
        self.health_bar.setValue(80)
        self.health_bar.setFormat("%v/%m")
        
        # Mana bar
        mana_label = QLabel("Mana:", self)
        self.mana_bar = QProgressBar(self)
        self.mana_bar.setObjectName("manaBar")
        self.mana_bar.setTextVisible(True)
        self.mana_bar.setRange(0, 50)
        self.mana_bar.setValue(40)
        self.mana_bar.setFormat("%v/%m")
        
        # Stamina bar
        stamina_label = QLabel("Stamina:", self)
        self.stamina_bar = QProgressBar(self)
        self.stamina_bar.setObjectName("staminaBar")
        self.stamina_bar.setTextVisible(True)
        self.stamina_bar.setRange(0, 80)
        self.stamina_bar.setValue(60)
        self.stamina_bar.setFormat("%v/%m")
        
        # Time of day
        time_label = QLabel("Time:", self)
        self.time_of_day = QLabel("Dusk", self)
        self.time_of_day.setObjectName("timeOfDayLabel")
        
        # Add widgets to layout
        layout.addWidget(health_label)
        layout.addWidget(self.health_bar, 1)
        layout.addWidget(mana_label)
        layout.addWidget(self.mana_bar, 1)
        layout.addWidget(stamina_label)
        layout.addWidget(self.stamina_bar, 1)
        layout.addWidget(time_label)
        layout.addWidget(self.time_of_day)
        
        self.setLayout(layout)
    
    def update_stats(self, health, max_health, mana, max_mana, stamina, max_stamina, time_of_day):
        """Update the status bar with new stats."""
        self.health_bar.setRange(0, max_health)
        self.health_bar.setValue(health)
        
        self.mana_bar.setRange(0, max_mana)
        self.mana_bar.setValue(mana)
        
        self.stamina_bar.setRange(0, max_stamina)
        self.stamina_bar.setValue(stamina)
        
        self.time_of_day.setText(time_of_day) 