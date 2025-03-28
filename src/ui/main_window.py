from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
                             QLineEdit, QPushButton, QSplitter, QDialog, QSpacerItem, QSizePolicy, QListWidgetItem, QLabel, QMenu, QMenuBar,
                             QStatusBar, QApplication)
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QTimer
from PyQt6.QtGui import QAction, QIcon, QFont, QTextCursor

from src.ui.status_bar import StatusBar
from src.ui.inventory_panel import InventoryPanel
from src.ui.character_window import CharacterWindow
from src.models.character import Character, CharacterEquipment
from src.models.item import Item, EquipmentItem
from src.models.game_master import GameMaster, StorytellerGM, example_story
from src.utils.theme_manager import ThemeManager


class GMStatusIndicator(QWidget):
    """Widget that shows the current status of the GM (thinking, ready, etc.)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("gmStatusIndicator")
        self.setMinimumHeight(36)  # Slightly smaller height
        self.setMaximumWidth(150)  # Narrower width for a more subtle look
        
        # Initialize UI
        self._init_ui()
        
        # For the thinking animation
        self.thinking_timer = QTimer(self)
        self.thinking_timer.timeout.connect(self._update_thinking_animation)
        self.thinking_dots = 0
        self.is_thinking = False
    
    def _init_ui(self):
        """Initialize the UI components."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Status label - use fixed width and left alignment
        self.status_label = QLabel("GM: Ready", self)
        self.status_label.setObjectName("gmStatusLabel")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.status_label.setMinimumWidth(120)  # Set minimum width to accommodate text + dots
        
        # Make the font bold and slightly larger
        font = self.status_label.font()
        font.setBold(True)
        font.setPointSize(font.pointSize() + 1)
        self.status_label.setFont(font)
        
        # Set consistent light blue color
        self.status_label.setStyleSheet("color: #89b4fa;")  # Light blue color
        
        layout.addWidget(self.status_label)
        self.setLayout(layout)
    
    def start_thinking(self):
        """Start the 'GM is thinking...' animation."""
        self.is_thinking = True
        self.thinking_dots = 0
        self.status_label.setText("GM: Thinking    ")  # Add padding spaces for dots
        
        # Start the timer to update the animation
        self.thinking_timer.start(500)  # Update every 500ms
    
    def _update_thinking_animation(self):
        """Update the thinking animation dots."""
        if not self.is_thinking:
            return
            
        self.thinking_dots = (self.thinking_dots + 1) % 4
        dots = "." * self.thinking_dots
        padding = " " * (3 - self.thinking_dots)  # Add padding to keep width consistent
        self.status_label.setText(f"GM: Thinking{dots}{padding}")
    
    def stop_thinking(self):
        """Stop the thinking animation."""
        if not self.is_thinking:
            return
            
        self.is_thinking = False
        self.thinking_timer.stop()
        self.status_label.setText("GM: Ready")


class MainWindow(QMainWindow):
    """Main window for the text adventure game UI."""
    
    story_message_sent = pyqtSignal(str)
    gm_message_sent = pyqtSignal(str)
    gm_message_received = pyqtSignal(str)
    theme_toggled = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI-Driven Text Adventure Game")
        self.resize(1200, 800)
        self.character_window = None
        
        # Initialize theme manager
        self.theme_manager = ThemeManager()
        
        # Create a dummy character for testing
        self._character = Character("Test Character", "Human", "Arcane Adept")
        
        # Initialize the game master
        self.game_master = StorytellerGM(example_story)
        
        # Connect the game master's signal to our method
        self.game_master.send_gm_message.connect(self._receive_gm_message)
        
        self._init_ui()
        
        # Start the game master conversation
        QTimer.singleShot(1000, self.game_master.start_conversation)
    
    def _init_ui(self):
        """Initialize the UI components."""
        # Create central widget and main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setCentralWidget(central_widget)
        
        # Create splitter for main panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel (story)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(15, 15, 15, 15)
        left_layout.setSpacing(10)
        
        # Story header
        story_header = QLabel("Story", left_panel)
        story_header.setObjectName("storyHeader")
        story_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = story_header.font()
        font.setBold(True)
        font.setPointSize(font.pointSize() + 1)
        story_header.setFont(font)
        left_layout.addWidget(story_header)
        
        # Story text area
        self.story_text_edit = QTextEdit()
        self.story_text_edit.setObjectName("mainStoryTextEdit")
        self.story_text_edit.setReadOnly(True)
        left_layout.addWidget(self.story_text_edit)
        
        # Story input area
        story_input_layout = QHBoxLayout()
        
        self.story_input = QLineEdit()
        self.story_input.setPlaceholderText("Enter your action...")
        self.story_input.returnPressed.connect(self._send_story_message)
        
        self.story_send_button = QPushButton("Send")
        self.story_send_button.clicked.connect(self._send_story_message)
        
        story_input_layout.addWidget(self.story_input)
        story_input_layout.addWidget(self.story_send_button)
        
        left_layout.addLayout(story_input_layout)
        
        # Right panel (GM chat and inventory)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(15, 15, 15, 15)
        right_layout.setSpacing(10)
        
        # GM header
        gm_header = QLabel("GM Chat", right_panel)
        gm_header.setObjectName("gmHeader")
        gm_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = gm_header.font()
        font.setBold(True)
        font.setPointSize(font.pointSize() + 1)
        gm_header.setFont(font)
        right_layout.addWidget(gm_header)
        
        # GM chat area
        self.gm_text_edit = QTextEdit()
        self.gm_text_edit.setObjectName("gmLogTextEdit")
        self.gm_text_edit.setReadOnly(True)
        
        # GM input area
        gm_input_layout = QHBoxLayout()
        
        self.gm_input = QLineEdit()
        self.gm_input.setPlaceholderText("Chat with GM...")
        self.gm_input.returnPressed.connect(self._send_gm_message)
        
        self.gm_send_button = QPushButton("Send")
        self.gm_send_button.clicked.connect(self._send_gm_message)
        
        gm_input_layout.addWidget(self.gm_input)
        gm_input_layout.addWidget(self.gm_send_button)
        
        # Inventory panel
        self.inventory_panel = InventoryPanel()
        
        # Connect inventory panel signals
        self.inventory_panel.item_examined.connect(self._handle_item_examined)
        self.inventory_panel.item_used.connect(self._handle_item_used)
        self.inventory_panel.item_dropped.connect(self._handle_item_dropped)
        self.inventory_panel.item_equipped.connect(self._handle_item_equipped)
        self.inventory_panel.item_unequipped.connect(self._handle_item_unequipped_from_inventory)
        
        right_layout.addWidget(self.gm_text_edit, 2)
        right_layout.addLayout(gm_input_layout)
        right_layout.addWidget(self.inventory_panel, 1)
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([700, 500])  # Initial sizes
        
        # Add spacer for padding
        main_layout.addWidget(splitter, 10)  # Give the splitter a larger stretch factor
        
        # Character button layout
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(15, 15, 15, 15)  # Add more padding
        
        # Character button (only takes up about 1/5 of the width)
        self.character_button = QPushButton("Character Sheet")
        self.character_button.setObjectName("characterButton")
        self.character_button.setMinimumHeight(40)
        self.character_button.setMaximumWidth(200)  # Limit width to about 1/5 of screen
        font = self.character_button.font()
        font.setBold(True)
        font.setPointSize(font.pointSize() + 1)
        self.character_button.setFont(font)
        self.character_button.clicked.connect(self._show_character_window)
        
        # GM Status Indicator (on the right side)
        self.gm_status = GMStatusIndicator()
        
        # Add button and status indicator to layout with spacer in between
        button_layout.addWidget(self.character_button)
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        button_layout.addWidget(self.gm_status)
        
        # Status bar
        self.status_bar = StatusBar()
        
        # Add widgets to main layout
        main_layout.addLayout(button_layout)
        
        # Add spacer for additional padding before status bar
        main_layout.addItem(QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        
        main_layout.addWidget(self.status_bar)
        
        # Add spacer for additional padding after status bar
        main_layout.addItem(QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        
        # Create menu bar
        self._create_menu_bar()
    
    def _create_menu_bar(self):
        """Create the menu bar."""
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("File")
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Character menu
        character_menu = menu_bar.addMenu("Character")
        
        character_action = QAction("Character Sheet", self)
        character_action.triggered.connect(self._show_character_window)
        character_menu.addAction(character_action)
        
        # View menu
        view_menu = menu_bar.addMenu("View")
        
        theme_action = QAction("Toggle Theme", self)
        theme_action.triggered.connect(self._toggle_theme)
        view_menu.addAction(theme_action)
    
    def _send_story_message(self):
        """Send a message to the story log."""
        message = self.story_input.text().strip()
        if message:
            self.story_text_edit.append(f"<span style='color:#a6e3a1;'>You:</span> {message}")
            self.story_input.clear()
            self.story_message_sent.emit(message)
    
    def _send_gm_message(self):
        """Send a message to the GM chat."""
        message = self.gm_input.text()
        if message:
            self.gm_text_edit.append(f"<span style='color:#a6e3a1;'>You:</span> {message}")
            self.gm_input.clear()
            
            # Show the GM is thinking
            self.gm_status.start_thinking()
            
            self.gm_message_sent.emit(message)
    
    def _receive_gm_message(self, message):
        """Receive a message from the game master and display it in the GM chat."""
        # Stop the thinking animation
        self.gm_status.stop_thinking()
        
        # Display the actual message
        self.gm_text_edit.append(f"<span style='color:#89b4fa;'>GM:</span> {message}")
        
        # Ensure the message is visible by scrolling to the bottom
        self.gm_text_edit.moveCursor(QTextCursor.MoveOperation.End)
        
        # Emit a signal that can be caught by the GameApp to add this to the game state
        # We don't emit gm_message_sent because that's for player messages
        if hasattr(self, 'gm_message_received'):
            self.gm_message_received.emit(message)
    
    def _show_character_window(self):
        """Show the character window."""
        if not self.character_window:
            self.character_window = CharacterWindow()
            
            # Connect signals
            self.character_window.item_examined.connect(self._handle_item_examined)
            self.character_window.item_used.connect(self._handle_item_used)
            self.character_window.item_dropped.connect(self._handle_item_dropped)
            self.character_window.item_equipped.connect(self._handle_item_equipped)
            self.character_window.item_unequipped.connect(self._handle_item_unequipped)
            
            # Connect the inventory panel signals
            self.character_window.inventory_panel.item_examined.connect(self._handle_item_examined)
            self.character_window.inventory_panel.item_used.connect(self._handle_item_used)
            self.character_window.inventory_panel.item_dropped.connect(self._handle_item_dropped)
            self.character_window.inventory_panel.item_equipped.connect(self._handle_item_equipped)
            self.character_window.inventory_panel.item_unequipped.connect(self._handle_item_unequipped_from_inventory)
        
        # Always update the character window with current inventory before showing it
        if hasattr(self, 'inventory_panel') and self.inventory_panel:
            items = []
            for i in range(self.inventory_panel.inventory_list.count()):
                item = self.inventory_panel.inventory_list.item(i)
                if item:
                    items.append(item.data(Qt.ItemDataRole.UserRole))
            self.character_window.inventory_panel.update_inventory(items)
        
        # Show the window and make sure it's in front
        self.character_window.show()
        self.character_window.raise_()  # Bring window to front
        self.character_window.activateWindow()  # Give it focus
        
        # Force an update of the character window if it's already created
        # This ensures the character class and location information is displayed
        if hasattr(self, '_character') and hasattr(self, '_location'):
            self.character_window.update_character(self._character)
            self.character_window.update_location(self._location)
    
    def _toggle_theme(self):
        """Toggle between light and dark themes."""
        self.theme_toggled.emit()
    
    def update_story_log(self, messages):
        """Update the story log with new messages."""
        self.story_text_edit.clear()
        for message in messages:
            sender = message["sender"]
            text = message["message"]
            
            if sender == "GM":
                self.story_text_edit.append(f"<span style='color:#89b4fa;'>GM:</span> {text}")
            else:
                self.story_text_edit.append(f"<span style='color:#a6e3a1;'>You:</span> {text}")
    
    def update_gm_log(self, messages):
        """Update the GM log with new messages."""
        self.gm_text_edit.clear()
        for message in messages:
            sender = message["sender"]
            text = message["message"]
            
            if sender == "GM":
                self.gm_text_edit.append(f"<span style='color:#89b4fa;'>GM:</span> {text}")
            else:
                self.gm_text_edit.append(f"<span style='color:#a6e3a1;'>You:</span> {text}")
    
    def update_inventory(self, items):
        """Update the inventory panel with new items."""
        self.inventory_panel.update_inventory(items)
        
        # Also update character window inventory if it exists
        if self.character_window:
            self.character_window.inventory_panel.update_inventory(items)
    
    def update_status_bar(self, health, max_health, mana, max_mana, stamina, max_stamina, time_of_day):
        """Update the status bar with new stats."""
        self.status_bar.update_stats(health, max_health, mana, max_mana, stamina, max_stamina, time_of_day)
    
    def update_character_window(self, character, location):
        """Update the character window with new character and location information."""
        # Store character and location for later use
        self._character = character
        self._location = location
        
        # Update character window if it exists
        if self.character_window:
            self.character_window.update_character(character)
            self.character_window.update_location(location)
            
            # Ensure inventory is synced
            if hasattr(self, 'inventory_panel') and self.inventory_panel:
                items = []
                for i in range(self.inventory_panel.inventory_list.count()):
                    item = self.inventory_panel.inventory_list.item(i)
                    if item:
                        items.append(item.data(Qt.ItemDataRole.UserRole))
                self.character_window.inventory_panel.update_inventory(items)
    
    def _handle_item_examined(self, item):
        """Handle item examination."""
        # This would typically send a message to the backend
        self.gm_text_edit.append(f"<span style='color:#a6e3a1;'>You:</span> I examine the {item.name}.")
        self.gm_text_edit.append(f"<span style='color:#89b4fa;'>GM:</span> {item.description}")
    
    def _handle_item_used(self, item):
        """Handle item usage."""
        # This would typically send a message to the backend
        self.story_text_edit.append(f"<span style='color:#a6e3a1;'>You:</span> I use the {item.name}.")
    
    def _handle_item_dropped(self, item):
        """Handle item dropping."""
        # This would typically send a message to the backend
        self.story_text_edit.append(f"<span style='color:#a6e3a1;'>You:</span> I drop the {item.name}.")
    
    def _handle_item_equipped(self, item):
        """Handle item equipping."""
        # This would typically send a message to the backend
        self.story_text_edit.append(f"<span style='color:#a6e3a1;'>You:</span> I equip the {item.name}.")
        
        # Actually equip the item in the character's equipment
        if hasattr(self, '_character'):
            # Mark the item as equipped first
            item.equipped = True
            
            # Add to equipment
            if item.slot == 'two_handed':
                # Unequip main_hand and off_hand if equipping a two-handed weapon
                if self._character.equipment.equipment['main_hand']:
                    self._character.equipment.equipment['main_hand'].equipped = False
                if self._character.equipment.equipment['off_hand']:
                    self._character.equipment.equipment['off_hand'].equipped = False
                self._character.equipment.equipment['main_hand'] = None
                self._character.equipment.equipment['off_hand'] = None
                self._character.equipment.equipment['two_handed'] = item
            elif item.slot in ['main_hand', 'off_hand']:
                # Unequip two_handed if equipping a one-handed weapon
                if self._character.equipment.equipment['two_handed']:
                    self._character.equipment.equipment['two_handed'].equipped = False
                self._character.equipment.equipment['two_handed'] = None
                if self._character.equipment.equipment[item.slot]:
                    self._character.equipment.equipment[item.slot].equipped = False
                self._character.equipment.equipment[item.slot] = item
            elif item.slot == 'accessories':
                # Add to accessories list
                if 'accessories' not in self._character.equipment.equipment:
                    self._character.equipment.equipment['accessories'] = []
                if len(self._character.equipment.equipment['accessories']) < self._character.equipment.MAX_ACCESSORIES:
                    self._character.equipment.equipment['accessories'].append(item)
            else:
                # Regular equipment slot
                if self._character.equipment.equipment[item.slot]:
                    self._character.equipment.equipment[item.slot].equipped = False
                self._character.equipment.equipment[item.slot] = item
            
            # Update both inventory panels with the current inventory
            current_inventory = self._get_inventory_items()
            self.inventory_panel.update_inventory(current_inventory)
            
            # Update character window if it exists
            if self.character_window:
                self.character_window.equipment_panel.update_equipment(self._character.equipment.equipment)
                self.character_window.inventory_panel.update_inventory(current_inventory)
    
    def _handle_item_unequipped_from_inventory(self, item):
        """Handle item unequipping from the inventory panel."""
        # This would typically send a message to the backend
        self.story_text_edit.append(f"<span style='color:#a6e3a1;'>You:</span> I unequip the {item.name}.")
        
        # Actually unequip the item from the character's equipment
        if hasattr(self, '_character'):
            # Find the slot that contains this item
            slot = None
            for slot_name, equipped_item in self._character.equipment.equipment.items():
                if equipped_item == item:
                    slot = slot_name
                    break
            
            if slot:
                # Remove from equipment
                if slot == 'accessories':
                    if 'accessories' in self._character.equipment.equipment:
                        if item in self._character.equipment.equipment['accessories']:
                            self._character.equipment.equipment['accessories'].remove(item)
                            item.equipped = False
                else:
                    self._character.equipment.equipment[slot] = None
                    item.equipped = False
                
                # Update both inventory panels with the current inventory
                current_inventory = self._get_inventory_items()
                self.inventory_panel.update_inventory(current_inventory)
                
                # Update character window if it exists
                if self.character_window:
                    self.character_window.equipment_panel.update_equipment(self._character.equipment.equipment)
                    self.character_window.inventory_panel.update_inventory(current_inventory)
    
    def _handle_item_unequipped(self, slot, item):
        """Handle item unequipping from equipment slots."""
        # This would typically send a message to the backend
        self.story_text_edit.append(f"<span style='color:#a6e3a1;'>You:</span> I unequip the {item.name}.")
        
        # Actually unequip the item from the character's equipment
        if hasattr(self, '_character'):
            # Remove from equipment
            if slot == 'accessories':
                if 'accessories' in self._character.equipment.equipment:
                    if item in self._character.equipment.equipment['accessories']:
                        self._character.equipment.equipment['accessories'].remove(item)
                        item.equipped = False
            else:
                self._character.equipment.equipment[slot] = None
                item.equipped = False
            
            # Update both inventory panels with the current inventory
            # Note: We don't need to add the item back to inventory manually
            # because it's already in the character's inventory list, just marked as equipped
            current_inventory = self._get_inventory_items()
            self.inventory_panel.update_inventory(current_inventory)
            
            # Update character window if it exists
            if self.character_window:
                self.character_window.equipment_panel.update_equipment(self._character.equipment.equipment)
                self.character_window.inventory_panel.update_inventory(current_inventory)
    
    def _create_inventory_item(self, item):
        """Create a QListWidgetItem for an inventory item."""
        list_item = QListWidgetItem(item.name)
        list_item.setData(Qt.ItemDataRole.UserRole, item)
        return list_item
    
    def _get_inventory_items(self):
        """Get all items from the inventory panel."""
        items = []
        for i in range(self.inventory_panel.inventory_list.count()):
            item = self.inventory_panel.inventory_list.item(i)
            if item:
                items.append(item.data(Qt.ItemDataRole.UserRole))
        return items
    
    def closeEvent(self, event):
        """Handle the window close event."""
        # Stop the game master conversation
        self.game_master.stop_conversation()
        
        # Accept the event to close the window
        event.accept() 