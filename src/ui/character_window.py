from PyQt6.QtWidgets import (QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QScrollArea, QFrame, QGridLayout, QListWidget, QListWidgetItem)
from PyQt6.QtCore import Qt, pyqtSignal
from .inventory_panel import InventoryPanel


class EquipmentSlot(QFrame):
    """A slot for equipped items."""
    
    item_clicked = pyqtSignal(object)
    
    def __init__(self, slot_name, parent=None):
        super().__init__(parent)
        self.setObjectName("equipmentSlot")
        self.slot_name = slot_name
        self.item = None
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(2)
        
        # Slot label
        slot_label = QLabel(self.slot_name.replace('_', ' ').title(), self)
        slot_label.setObjectName("slotLabel")
        slot_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Item label
        self.item_label = QLabel("Empty", self)
        self.item_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(slot_label)
        layout.addWidget(self.item_label)
        
        self.setLayout(layout)
        self.setProperty("occupied", "false")
        
        # Connect signals
        self.mousePressEvent = self._on_click
    
    def set_item(self, item):
        """Set the item in this slot."""
        self.item = item
        
        if item:
            self.item_label.setText(item.name)
            self.setProperty("occupied", "true")
            
            # Set rarity class if it's an equipment item
            if hasattr(item, 'rarity'):
                self.item_label.setProperty("class", item.rarity)
        else:
            self.item_label.setText("Empty")
            self.setProperty("occupied", "false")
            self.item_label.setProperty("class", "")
        
        # Force style update
        self.style().unpolish(self)
        self.style().polish(self)
    
    def _on_click(self, event):
        """Handle mouse click events."""
        if self.item:
            self.item_clicked.emit(self.item)


class EquipmentPanel(QWidget):
    """Panel displaying the character's equipped items."""
    
    item_unequipped = pyqtSignal(str, object)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("equipmentPanel")
        self.slots = {}
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components."""
        layout = QGridLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Create equipment slots
        self.slots['head'] = EquipmentSlot("head", self)
        self.slots['chest'] = EquipmentSlot("chest", self)
        self.slots['legs'] = EquipmentSlot("legs", self)
        self.slots['hands'] = EquipmentSlot("hands", self)
        self.slots['feet'] = EquipmentSlot("feet", self)
        self.slots['main_hand'] = EquipmentSlot("main_hand", self)
        self.slots['off_hand'] = EquipmentSlot("off_hand", self)
        self.slots['two_handed'] = EquipmentSlot("two_handed", self)
        
        # Add slots to layout
        layout.addWidget(self.slots['head'], 0, 1)
        layout.addWidget(self.slots['chest'], 1, 1)
        layout.addWidget(self.slots['legs'], 2, 1)
        layout.addWidget(self.slots['hands'], 1, 0)
        layout.addWidget(self.slots['feet'], 3, 1)
        layout.addWidget(self.slots['main_hand'], 1, 2)
        layout.addWidget(self.slots['off_hand'], 2, 2)
        layout.addWidget(self.slots['two_handed'], 3, 2)
        
        # Connect signals
        for slot_name, slot in self.slots.items():
            slot.item_clicked.connect(lambda item, slot=slot_name: self.item_unequipped.emit(slot, item))
        
        self.setLayout(layout)
    
    def update_equipment(self, equipment):
        """Update the equipment slots with new items."""
        for slot_name, item in equipment.items():
            if slot_name in self.slots:
                self.slots[slot_name].set_item(item)


class ClassPanel(QWidget):
    """Panel displaying the character's class information."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("classPanel")
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Class name and description
        self.class_name = QLabel(self)
        self.class_name.setObjectName("className")
        self.class_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.class_name.setWordWrap(True)
        
        self.class_description = QLabel(self)
        self.class_description.setObjectName("classDescription")
        self.class_description.setWordWrap(True)
        
        # Skills list
        skills_label = QLabel("Skills:", self)
        skills_label.setObjectName("skillsLabel")
        
        self.skills_list = QListWidget(self)
        self.skills_list.setObjectName("skillsList")
        
        # Add widgets to layout
        layout.addWidget(self.class_name)
        layout.addWidget(self.class_description)
        layout.addWidget(skills_label)
        layout.addWidget(self.skills_list)
        
        self.setLayout(layout)
    
    def update_class(self, character_class):
        """Update the class panel with new class information."""
        self.class_name.setText(character_class.name)
        self.class_description.setText(character_class.description)
        
        self.skills_list.clear()
        for skill in character_class.skills:
            item = QListWidgetItem(f"{skill.name} (Level {skill.level})")
            item.setToolTip(skill.description)
            self.skills_list.addItem(item)


class WorldPanel(QWidget):
    """Panel displaying the world information."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("worldPanel")
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Current location
        location_label = QLabel("Current Location:", self)
        location_label.setObjectName("locationLabel")
        
        self.location_name = QLabel(self)
        self.location_name.setObjectName("locationName")
        self.location_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.location_description = QLabel(self)
        self.location_description.setObjectName("locationDescription")
        self.location_description.setWordWrap(True)
        
        # Connections
        connections_label = QLabel("Connections:", self)
        connections_label.setObjectName("connectionsLabel")
        
        self.connections_list = QListWidget(self)
        self.connections_list.setObjectName("connectionsList")
        
        # Add widgets to layout
        layout.addWidget(location_label)
        layout.addWidget(self.location_name)
        layout.addWidget(self.location_description)
        layout.addWidget(connections_label)
        layout.addWidget(self.connections_list)
        
        self.setLayout(layout)
    
    def update_location(self, location):
        """Update the world panel with new location information."""
        self.location_name.setText(location.name)
        self.location_description.setText(location.description)
        
        self.connections_list.clear()
        for connection in location.connections:
            self.connections_list.addItem(connection)


class CharacterWindow(QWidget):
    """Window displaying character information."""
    
    item_unequipped = pyqtSignal(str, object)
    item_examined = pyqtSignal(object)
    item_used = pyqtSignal(object)
    item_dropped = pyqtSignal(object)
    item_equipped = pyqtSignal(object)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("characterWindow")
        self.setWindowTitle("Character")
        self.resize(800, 600)
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Character name
        self.character_name = QLabel(self)
        self.character_name.setObjectName("characterName")
        self.character_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.character_name)
        
        # Tab widget
        self.tab_widget = QTabWidget(self)
        
        # Equipment & Inventory tab
        equipment_inventory_tab = QWidget()
        equipment_inventory_layout = QHBoxLayout(equipment_inventory_tab)
        
        # Equipment panel
        self.equipment_panel = EquipmentPanel(equipment_inventory_tab)
        equipment_inventory_layout.addWidget(self.equipment_panel)
        
        # Inventory panel
        self.inventory_panel = InventoryPanel(equipment_inventory_tab)
        equipment_inventory_layout.addWidget(self.inventory_panel)
        
        # Class tab
        self.class_panel = ClassPanel()
        
        # World tab
        self.world_panel = WorldPanel()
        
        # Add tabs to tab widget
        self.tab_widget.addTab(equipment_inventory_tab, "Items & Equipment")
        self.tab_widget.addTab(self.class_panel, "Class")
        self.tab_widget.addTab(self.world_panel, "World")
        
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
        
        # Connect signals
        self.equipment_panel.item_unequipped.connect(self.item_unequipped)
        self.inventory_panel.item_examined.connect(self.item_examined)
        self.inventory_panel.item_used.connect(self.item_used)
        self.inventory_panel.item_dropped.connect(self.item_dropped)
        self.inventory_panel.item_equipped.connect(self.item_equipped)
    
    def update_character(self, character):
        """Update the character window with new character information."""
        self.character_name.setText(character.name)
        self.equipment_panel.update_equipment(character.equipment.equipment)
        self.inventory_panel.update_inventory(character.inventory)
        self.class_panel.update_class(character.character_class)
    
    def update_location(self, location):
        """Update the world panel with new location information."""
        self.world_panel.update_location(location) 