import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication

from src.models import GameState
from src.ui.main_window import MainWindow
from src.utils.theme_manager import ThemeManager
from src.models.game_master import GameMaster, StorytellerGM, example_story
from src.models.llm_game_master import LLMGameMaster


class GameApp:
    """Main application class for the text adventure game UI."""
    
    def __init__(self, use_llm=True):
        self.app = QApplication(sys.argv)
        self.theme_manager = ThemeManager()
        self.main_window = MainWindow()
        
        # Create demo game state
        self.game_state = GameState.create_demo_state()
        
        # Create and initialize the game master
        if use_llm:
            self.game_master = LLMGameMaster()
        else:
            self.game_master = StorytellerGM(example_story)
        
        # Connect the game master to the main window
        self.game_master.send_gm_message.connect(self.main_window._receive_gm_message)
        
        # Apply theme
        self.app.setStyleSheet(self.theme_manager.stylesheet)
        
        # Connect theme manager signals
        self.theme_manager.theme_changed.connect(self._on_theme_changed)
        
        # Connect main window signals
        self.main_window.story_message_sent.connect(self._on_story_message_sent)
        self.main_window.gm_message_sent.connect(self._on_gm_message_sent)
        self.main_window.gm_message_received.connect(self._on_gm_message_received)
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
        
        # Store the game master in the main window for access in other methods
        self.main_window.game_master = self.game_master
    
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
        # Forward the message to the game master
        self.game_master.receive_player_message(message)
        
        # Add it to the game state
        self.game_state.add_gm_message(message, sender="Player")
        self._update_ui()
    
    def _on_gm_message_received(self, message):
        """Handle GM messages received from the game master."""
        # Add it to the game state
        self.game_state.add_gm_message(message, sender="GM")
        # Note: We don't call _update_ui() here because that would clear and rebuild the chat,
        # and the message is already displayed by _receive_gm_message
    
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
        
        # Start the game master conversation
        self.game_master.start_conversation()
        
        return self.app.exec()


if __name__ == "__main__":
    # Use the LLM-based game master
    app = GameApp(use_llm=True)
    sys.exit(app.run()) 