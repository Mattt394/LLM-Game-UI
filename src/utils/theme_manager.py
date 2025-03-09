import os
import darkdetect
from PyQt6.QtCore import QObject, pyqtSignal


class ThemeManager(QObject):
    """Manages the application theme (light/dark)."""
    
    theme_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        # Always use dark theme as default instead of detecting system theme
        self._theme = "dark"
        self._stylesheet = self._load_stylesheet(self._theme)
    
    def _detect_system_theme(self):
        """Detect the system theme (light/dark)."""
        return "dark" if darkdetect.isDark() else "light"
    
    def _load_stylesheet(self, theme):
        """Load the stylesheet for the given theme."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        stylesheet_path = os.path.join(base_dir, "assets", "styles", f"{theme}_theme.qss")
        
        try:
            with open(stylesheet_path, "r") as f:
                return f.read()
        except Exception as e:
            print(f"Error loading stylesheet: {e}")
            return ""
    
    @property
    def theme(self):
        """Get the current theme."""
        return self._theme
    
    @theme.setter
    def theme(self, value):
        """Set the theme."""
        if value in ["light", "dark"] and value != self._theme:
            self._theme = value
            self._stylesheet = self._load_stylesheet(value)
            self.theme_changed.emit(value)
    
    @property
    def stylesheet(self):
        """Get the current stylesheet."""
        return self._stylesheet
    
    def toggle_theme(self):
        """Toggle between light and dark themes."""
        self.theme = "light" if self._theme == "dark" else "dark" 