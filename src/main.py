import sys
from PyQt6.QtWidgets import QApplication

from models import GameState
from ui import MainWindow
from utils import ThemeManager


class GameApp:
    """Main application class for the text adventure game UI."""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.theme_manager = ThemeManager()
        self.main_window = MainWindow()
        
        # Create demo game state
        self.game_state = GameState.create_demo_state()
        
        # Apply theme
        self.app.setStyleSheet(self.theme_manager.stylesheet)
        
        # Connect theme manager signals
        self.theme_manager.theme_changed.connect(self._on_theme_changed)
        
        # Connect main window signals
        self.main_window.story_message_sent.connect(self._on_story_message_sent)
        self.main_window.gm_message_sent.connect(self._on_gm_message_sent)
        self.main_window.theme_toggled.connect(self._on_theme_toggled)
        
        # Initialize UI with game state
        self._update_ui()
        
        # Override the main window's _show_character_window method to add debug output
        original_show_character_window = self.main_window._show_character_window
        
        def debug_show_character_window():
            result = original_show_character_window()
            self.main_window.update_character_window(
                self.game_state.character,
                self.game_state.current_location
            )
            return result
        
        self.main_window._show_character_window = debug_show_character_window
    
    def _on_theme_changed(self, theme):
        """Handle theme changes."""
        self.app.setStyleSheet(self.theme_manager.stylesheet)
    
    def _on_theme_toggled(self):
        """Handle theme toggle."""
        self.theme_manager.toggle_theme()
    
    def _on_story_message_sent(self, message):
        """Handle story messages sent by the player."""
        # In a real implementation, this would send the message to the backend
        # For now, we'll just add it to the game state
        self.game_state.add_story_message(message, sender="Player")
        self._update_ui()
    
    def _on_gm_message_sent(self, message):
        """Handle GM messages sent by the player."""
        # In a real implementation, this would send the message to the backend
        # For now, we'll just add it to the game state
        self.game_state.add_gm_message(message, sender="Player")
        self._update_ui()
    
    def _update_ui(self):
        """Update the UI with the current game state."""
        # Update main window
        self.main_window.update_story_log(self.game_state.story_log)
        self.main_window.update_gm_log(self.game_state.gm_log)
        self.main_window.update_inventory(self.game_state.character.inventory)
        self.main_window.update_status_bar(
            self.game_state.character.health,
            self.game_state.character.max_health,
            self.game_state.character.mana,
            self.game_state.character.max_mana,
            self.game_state.character.stamina,
            self.game_state.character.max_stamina,
            self.game_state.time_of_day
        )
        
        # Update character window if it exists
        self.main_window.update_character_window(
            self.game_state.character,
            self.game_state.current_location
        )
    
    def run(self):
        """Run the application."""
        self.main_window.show()
        return self.app.exec()


if __name__ == "__main__":
    app = GameApp()
    sys.exit(app.run()) 