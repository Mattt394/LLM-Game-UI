from PyQt6.QtWidgets import (QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QScrollArea, QFrame, QGridLayout, QListWidget, QListWidgetItem,
                             QProgressBar, QMenu, QApplication)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from .inventory_panel import InventoryPanel


class EquipmentSlot(QFrame):
    """A slot for equipped items."""
    
    item_unequipped = pyqtSignal(str, object)
    
    def __init__(self, slot_name, parent=None):
        super().__init__(parent)
        self.setObjectName("equipmentSlot")
        self.slot_name = slot_name
        self.item = None
        self.tooltip = None
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
        
        # Enable mouse tracking for hover events
        self.setMouseTracking(True)
        
        # Set context menu policy
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
    
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
    
    def enterEvent(self, event):
        """Handle mouse enter events to show tooltip."""
        if self.item:
            from .inventory_panel import ItemTooltip
            
            # Create and show the tooltip
            if self.tooltip:
                self.tooltip.hide()
                self.tooltip.deleteLater()
            
            self.tooltip = ItemTooltip(self.item)
            
            # Calculate tooltip size before showing it
            self.tooltip.adjustSize()
            tooltip_width = self.tooltip.width()
            tooltip_height = self.tooltip.height()
            
            # Get global position for the tooltip
            global_pos = self.mapToGlobal(self.rect().topRight())
            
            # Get screen geometry to ensure tooltip stays within screen
            screen_rect = QApplication.primaryScreen().availableGeometry()
            
            # Adjust position if tooltip would go off-screen
            if global_pos.x() + tooltip_width > screen_rect.right():
                # If tooltip would go off right edge, show it to the left of the slot
                global_pos.setX(global_pos.x() - tooltip_width - self.width() - 10)
            else:
                # Otherwise, show it to the right with a small offset
                global_pos.setX(global_pos.x() + 10)
            
            # Check if tooltip would go off bottom of screen
            if global_pos.y() + tooltip_height > screen_rect.bottom():
                # Move it up so it fits
                global_pos.setY(screen_rect.bottom() - tooltip_height)
            
            self.tooltip.move(global_pos)
            self.tooltip.show()
        
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Handle mouse leave events to hide tooltip."""
        if self.tooltip:
            self.tooltip.hide()
            self.tooltip.deleteLater()
            self.tooltip = None
        
        super().leaveEvent(event)
    
    def _show_context_menu(self, position):
        """Show the context menu for an equipped item."""
        if not self.item:
            return
        
        menu = QMenu(self)
        menu.setObjectName("itemActionMenu")
        
        # Add actions
        examine_action = menu.addAction("Examine")
        unequip_action = menu.addAction("Unequip")
        
        # Show the menu and handle the selected action
        action = menu.exec(self.mapToGlobal(position))
        
        if action == examine_action:
            # For now, we'll just show the tooltip
            # In the future, you might want to emit a signal for examination
            pass
        elif action == unequip_action:
            self.item_unequipped.emit(self.slot_name, self.item)


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
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Add header
        header = QLabel("Equipment", self)
        header.setObjectName("equipmentHeader")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = header.font()
        font.setBold(True)
        font.setPointSize(font.pointSize() + 1)
        header.setFont(font)
        layout.addWidget(header)
        
        # Equipment grid
        equipment_layout = QGridLayout()
        equipment_layout.setSpacing(10)
        
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
        equipment_layout.addWidget(self.slots['head'], 0, 1)
        equipment_layout.addWidget(self.slots['chest'], 1, 1)
        equipment_layout.addWidget(self.slots['legs'], 2, 1)
        equipment_layout.addWidget(self.slots['hands'], 1, 0)
        equipment_layout.addWidget(self.slots['feet'], 3, 1)
        equipment_layout.addWidget(self.slots['main_hand'], 1, 2)
        equipment_layout.addWidget(self.slots['off_hand'], 2, 2)
        equipment_layout.addWidget(self.slots['two_handed'], 3, 2)
        
        layout.addLayout(equipment_layout)
        
        # Connect signals
        for slot_name, slot in self.slots.items():
            slot.item_unequipped.connect(lambda slot_name, item, slot=slot_name: self.item_unequipped.emit(slot, item))
        
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
        
        # Add header
        header = QLabel("Character Class", self)
        header.setObjectName("classHeader")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = header.font()
        font.setBold(True)
        font.setPointSize(font.pointSize() + 1)
        header.setFont(font)
        layout.addWidget(header)
        
        # Class name and description
        self.class_name = QLabel(self)
        self.class_name.setObjectName("className")
        self.class_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.class_name.setWordWrap(True)
        font = self.class_name.font()
        font.setBold(True)
        font.setPointSize(font.pointSize() + 1)
        self.class_name.setFont(font)
        
        self.class_description = QLabel(self)
        self.class_description.setObjectName("classDescription")
        self.class_description.setWordWrap(True)
        
        # Level and Experience
        level_exp_layout = QHBoxLayout()
        
        self.level_label = QLabel("Level: 1", self)
        self.level_label.setObjectName("levelLabel")
        font = self.level_label.font()
        font.setBold(True)
        self.level_label.setFont(font)
        
        level_exp_layout.addWidget(self.level_label)
        level_exp_layout.addStretch()
        
        # Experience bar
        exp_layout = QVBoxLayout()
        
        exp_header_layout = QHBoxLayout()
        exp_label = QLabel("Experience:", self)
        exp_label.setObjectName("expLabel")
        self.exp_value_label = QLabel("0/100", self)
        self.exp_value_label.setObjectName("expValueLabel")
        exp_header_layout.addWidget(exp_label)
        exp_header_layout.addStretch()
        exp_header_layout.addWidget(self.exp_value_label)
        
        self.exp_bar = QProgressBar(self)
        self.exp_bar.setObjectName("expBar")
        self.exp_bar.setTextVisible(False)
        self.exp_bar.setRange(0, 100)
        self.exp_bar.setValue(0)
        
        exp_layout.addLayout(exp_header_layout)
        exp_layout.addWidget(self.exp_bar)
        
        # Skills list
        skills_label = QLabel("Skills:", self)
        skills_label.setObjectName("skillsLabel")
        font = skills_label.font()
        font.setBold(True)
        skills_label.setFont(font)
        
        self.skills_list = QListWidget(self)
        self.skills_list.setObjectName("skillsList")
        self.skills_list.setMouseTracking(True)  # Enable mouse tracking for hover events
        self.skills_list.setToolTipDuration(5000)  # Set tooltip duration to 5 seconds
        
        # Add widgets to layout
        layout.addWidget(self.class_name)
        layout.addWidget(self.class_description)
        layout.addLayout(level_exp_layout)
        layout.addLayout(exp_layout)
        layout.addWidget(skills_label)
        layout.addWidget(self.skills_list)
        
        self.setLayout(layout)
    
    def update_class(self, character_class):
        """Update the class panel with new class information."""
        # Set text with explicit styling to ensure visibility
        self.class_name.setText(f"<h2>{character_class.name}</h2>")
        self.class_description.setText(f"<p>{character_class.description}</p>")
        
        self.skills_list.clear()
        for skill in character_class.skills:
            item = QListWidgetItem(f"{skill.name} (Level {skill.level})")
            
            # Create detailed tooltip with HTML formatting
            tooltip = f"""
            <h3>{skill.name}</h3>
            <p><b>Level:</b> {skill.level}</p>
            <p><b>Description:</b> {skill.description}</p>
            """
            
            # Add cost information if available
            if skill.cost:
                cost_text = f"<p><b>Cost:</b> {skill.cost.get('amount', 0)} {skill.cost.get('resource', 'mana')}</p>"
                tooltip += cost_text
            
            # Add effects information if available
            if skill.effects:
                effects_text = "<p><b>Effects:</b></p><ul>"
                for effect in skill.effects:
                    action = effect.get("action", "")
                    value = effect.get("value", 0)
                    target = effect.get("target_group", "")
                    effects_text += f"<li>{action.capitalize()} {value} to {target}</li>"
                effects_text += "</ul>"
                tooltip += effects_text
            
            item.setToolTip(tooltip)
            self.skills_list.addItem(item)
    
    def update_experience(self, level, experience, experience_to_next_level):
        """Update the experience bar with new experience information."""
        self.level_label.setText(f"Level: {level}")
        self.exp_value_label.setText(f"{experience}/{experience_to_next_level}")
        self.exp_bar.setRange(0, experience_to_next_level)
        self.exp_bar.setValue(experience)


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
        
        # Add header
        header = QLabel("World Map", self)
        header.setObjectName("worldHeader")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = header.font()
        font.setBold(True)
        font.setPointSize(font.pointSize() + 1)
        header.setFont(font)
        layout.addWidget(header)
        
        # Current location
        location_label = QLabel("Current Location:", self)
        location_label.setObjectName("locationLabel")
        font = location_label.font()
        font.setBold(True)
        location_label.setFont(font)
        
        self.location_name = QLabel(self)
        self.location_name.setObjectName("locationName")
        self.location_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.location_name.font()
        font.setBold(True)
        self.location_name.setFont(font)
        
        self.location_description = QLabel(self)
        self.location_description.setObjectName("locationDescription")
        self.location_description.setWordWrap(True)
        
        # Connections
        connections_label = QLabel("Connections:", self)
        connections_label.setObjectName("connectionsLabel")
        font = connections_label.font()
        font.setBold(True)
        connections_label.setFont(font)
        
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
        # Set location name and description with explicit styling
        self.location_name.setText(f"<h3>{location.name}</h3>")
        self.location_description.setText(f"<p>{location.description}</p>")
        
        # Update connections list
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
        self.setWindowTitle("Character Sheet")
        self.resize(800, 600)
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Character name
        self.character_name = QLabel(self)
        self.character_name.setObjectName("characterName")
        self.character_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.character_name.font()
        font.setBold(True)
        font.setPointSize(font.pointSize() + 2)
        self.character_name.setFont(font)
        layout.addWidget(self.character_name)
        
        # Tab widget
        self.tab_widget = QTabWidget(self)
        
        # Equipment & Inventory tab
        equipment_inventory_tab = QWidget()
        equipment_inventory_layout = QHBoxLayout(equipment_inventory_tab)
        equipment_inventory_layout.setContentsMargins(5, 5, 5, 5)
        equipment_inventory_layout.setSpacing(10)
        
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
        # Set character name with explicit styling
        self.character_name.setText(f"<h1>{character.name}</h1>")
        
        # Update equipment and inventory
        self.equipment_panel.update_equipment(character.equipment.equipment)
        self.inventory_panel.update_inventory(character.inventory)
        
        # Update class panel with class and experience information
        self.class_panel.update_class(character.character_class)
        self.class_panel.update_experience(
            character.level,
            character.experience,
            character.experience_to_next_level
        )
    
    def update_location(self, location):
        """Update the world panel with new location information."""
        self.world_panel.update_location(location) 