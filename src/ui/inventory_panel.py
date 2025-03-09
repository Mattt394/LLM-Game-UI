from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
                             QMenu, QToolTip, QLabel, QFrame, QHBoxLayout)
from PyQt6.QtCore import Qt, pyqtSignal, QPoint


class ItemTooltip(QFrame):
    """Custom tooltip for inventory items."""
    
    def __init__(self, item, parent=None):
        super().__init__(parent)
        self.setObjectName("itemTooltip")
        self.setWindowFlags(Qt.WindowType.ToolTip)
        self.item = item
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(2)
        
        # Item name
        name_layout = QHBoxLayout()
        name = QLabel(self.item.name, self)
        name.setObjectName("itemName")
        name_layout.addWidget(name)
        
        # Item rarity (for equipment)
        if hasattr(self.item, 'rarity'):
            rarity = QLabel(self.item.rarity.capitalize(), self)
            rarity.setObjectName("itemRarity")
            rarity.setProperty("class", self.item.rarity)
            name_layout.addWidget(rarity)
        
        layout.addLayout(name_layout)
        
        # Item type
        type_label = QLabel(self.item.item_type.capitalize(), self)
        layout.addWidget(type_label)
        
        # Item description
        description = QLabel(self.item.description, self)
        description.setObjectName("itemDescription")
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Item stats (for equipment)
        if hasattr(self.item, 'physical_attack') and any([
            self.item.physical_attack, self.item.physical_defense,
            self.item.magic_attack, self.item.magic_defense
        ]):
            stats = QLabel(self)
            stats.setObjectName("itemStats")
            stats_text = ""
            
            if self.item.physical_attack:
                stats_text += f"Physical Attack: +{self.item.physical_attack}\n"
            if self.item.physical_defense:
                stats_text += f"Physical Defense: +{self.item.physical_defense}\n"
            if self.item.magic_attack:
                stats_text += f"Magic Attack: +{self.item.magic_attack}\n"
            if self.item.magic_defense:
                stats_text += f"Magic Defense: +{self.item.magic_defense}\n"
            
            stats.setText(stats_text.strip())
            layout.addWidget(stats)
        
        self.setLayout(layout)


class InventoryPanel(QWidget):
    """Panel displaying the character's inventory."""
    
    item_examined = pyqtSignal(object)
    item_used = pyqtSignal(object)
    item_dropped = pyqtSignal(object)
    item_equipped = pyqtSignal(object)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("inventoryPanel")
        self.tooltip = None
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Inventory list
        self.inventory_list = QListWidget(self)
        self.inventory_list.setObjectName("inventoryList")
        self.inventory_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.inventory_list.customContextMenuRequested.connect(self._show_context_menu)
        self.inventory_list.itemEntered.connect(self._show_item_tooltip)
        self.inventory_list.viewportEntered.connect(self._hide_tooltip)
        
        layout.addWidget(self.inventory_list)
        self.setLayout(layout)
    
    def update_inventory(self, items):
        """Update the inventory list with new items."""
        self.inventory_list.clear()
        
        for item in items:
            list_item = QListWidgetItem(item.name)
            list_item.setData(Qt.ItemDataRole.UserRole, item)
            self.inventory_list.addItem(list_item)
    
    def _show_context_menu(self, position):
        """Show the context menu for an item."""
        item = self.inventory_list.itemAt(position)
        if not item:
            return
        
        game_item = item.data(Qt.ItemDataRole.UserRole)
        
        menu = QMenu(self)
        menu.setObjectName("itemActionMenu")
        
        # Add actions
        examine_action = menu.addAction("Examine")
        use_action = menu.addAction("Use")
        drop_action = menu.addAction("Drop")
        
        # Add equip action if it's an equipment item
        equip_action = None
        if hasattr(game_item, 'slot'):
            equip_action = menu.addAction("Equip")
        
        # Show the menu and handle the selected action
        action = menu.exec(self.inventory_list.mapToGlobal(position))
        
        if action == examine_action:
            self.item_examined.emit(game_item)
        elif action == use_action:
            self.item_used.emit(game_item)
        elif action == drop_action:
            self.item_dropped.emit(game_item)
        elif equip_action and action == equip_action:
            self.item_equipped.emit(game_item)
    
    def _show_item_tooltip(self, item):
        """Show a tooltip for the item."""
        if not item:
            return
        
        game_item = item.data(Qt.ItemDataRole.UserRole)
        
        # Create and show the tooltip
        if self.tooltip:
            self.tooltip.deleteLater()
        
        self.tooltip = ItemTooltip(game_item)
        
        # Position the tooltip next to the item
        pos = self.inventory_list.mapToGlobal(self.inventory_list.visualItemRect(item).topRight())
        pos.setX(pos.x() + 10)  # Offset to the right
        
        self.tooltip.move(pos)
        self.tooltip.show()
    
    def _hide_tooltip(self):
        """Hide the tooltip."""
        if self.tooltip:
            self.tooltip.hide()
            self.tooltip.deleteLater()
            self.tooltip = None 