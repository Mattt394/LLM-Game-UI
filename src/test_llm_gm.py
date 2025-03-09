#!/usr/bin/env python3
"""
Test script for the LLM-based GameMaster class.
This demonstrates how to use the LLM GameMaster with the UI.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
import src.ui.main_window as main_window_module
from src.models.llm_game_master import LLMGameMaster

def main():
    """Run the test application with the LLM GameMaster."""
    app = QApplication(sys.argv)
    
    # Create the main window
    window = main_window_module.MainWindow()
    
    # Replace the default GameMaster with the LLM-based one
    window.game_master.stop_conversation()  # Stop the default GM
    window.game_master = LLMGameMaster()    # Create a new LLM-based GM
    window.game_master.send_gm_message.connect(window._receive_gm_message)  # Reconnect signals
    window.game_master.start_conversation()  # Start the new GM
    
    # Show the window
    window.show()
    
    # Start the application event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 