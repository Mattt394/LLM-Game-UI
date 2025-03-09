from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
                             QLineEdit, QPushButton, QSplitter, QDialog)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QIcon

from .status_bar import StatusBar
from .inventory_panel import InventoryPanel
from .character_window import CharacterWindow


class MainWindow(QMainWindow):
    """Main window for the text adventure game UI."""
    
    story_message_sent = pyqtSignal(str)
    gm_message_sent = pyqtSignal(str)
    theme_toggled = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI-Driven Text Adventure Game")
        self.resize(1200, 800)
        self.character_window = None
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI components."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create splitter for main content
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel (Story)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(10, 10, 10, 10)
        
        # Story text edit
        self.story_text_edit = QTextEdit()
        self.story_text_edit.setObjectName("mainStoryTextEdit")
        self.story_text_edit.setReadOnly(True)
        
        # Story input
        story_input_layout = QHBoxLayout()
        self.story_input = QLineEdit()
        self.story_input.setPlaceholderText("Enter your action...")
        self.story_input.returnPressed.connect(self._send_story_message)
        
        self.story_send_button = QPushButton("Send")
        self.story_send_button.clicked.connect(self._send_story_message)
        
        story_input_layout.addWidget(self.story_input)
        story_input_layout.addWidget(self.story_send_button)
        
        left_layout.addWidget(self.story_text_edit)
        left_layout.addLayout(story_input_layout)
        
        # Right panel (GM Chat & Inventory)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)
        
        # GM chat text edit
        self.gm_text_edit = QTextEdit()
        self.gm_text_edit.setObjectName("gmLogTextEdit")
        self.gm_text_edit.setReadOnly(True)
        
        # GM chat input
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
        
        right_layout.addWidget(self.gm_text_edit, 2)
        right_layout.addLayout(gm_input_layout)
        right_layout.addWidget(self.inventory_panel, 1)
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([700, 500])  # Initial sizes
        
        # Status bar
        self.status_bar = StatusBar()
        
        # Add widgets to main layout
        main_layout.addWidget(splitter)
        main_layout.addWidget(self.status_bar)
        
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
        """Send a message to the GM log."""
        message = self.gm_input.text().strip()
        if message:
            self.gm_text_edit.append(f"<span style='color:#a6e3a1;'>You:</span> {message}")
            self.gm_input.clear()
            self.gm_message_sent.emit(message)
    
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
        
        self.character_window.show()
    
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
    
    def update_status_bar(self, health, max_health, mana, max_mana, stamina, max_stamina, time_of_day):
        """Update the status bar with new stats."""
        self.status_bar.update_stats(health, max_health, mana, max_mana, stamina, max_stamina, time_of_day)
    
    def update_character_window(self, character, location):
        """Update the character window with new character and location information."""
        if self.character_window:
            self.character_window.update_character(character)
            self.character_window.update_location(location)
    
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
    
    def _handle_item_unequipped(self, slot, item):
        """Handle item unequipping."""
        # This would typically send a message to the backend
        self.story_text_edit.append(f"<span style='color:#a6e3a1;'>You:</span> I unequip the {item.name}.") 