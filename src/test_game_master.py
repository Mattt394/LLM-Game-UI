#!/usr/bin/env python3
"""
Test script for the GameMaster class.
This demonstrates how to use the GameMaster with the UI.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
import src.ui.main_window as main_window_module

def main():
    """Run the test application."""
    app = QApplication(sys.argv)
    
    # Create and show the main window
    window = main_window_module.MainWindow()
    window.show()
    
    # Start the application event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 