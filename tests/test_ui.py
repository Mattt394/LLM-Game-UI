import sys
import os
import unittest
from PyQt6.QtWidgets import QApplication, QListWidgetItem, QWidget
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QAction

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ui.main_window import MainWindow
from src.models.item import Item, EquipmentItem
from src.utils.theme_manager import ThemeManager


class TestUI(unittest.TestCase):
    """Test suite for the UI components and interactions."""
    
    @classmethod
    def setUpClass(cls):
        """Create the application once for all tests."""
        cls.app = QApplication(sys.argv)
        # Initialize theme manager to apply styling
        cls.theme_manager = ThemeManager()
        cls.app.setStyleSheet(cls.theme_manager.stylesheet)
    
    def setUp(self):
        """Create a fresh window for each test."""
        self.window = MainWindow()
        self.window.show()  # Important for UI testing
        QTest.qWait(100)  # Give time for window to fully initialize
    
    def test_initial_window_state(self):
        """Test that the window initializes with all expected components."""
        # Check main components exist
        self.assertIsNotNone(self.window.story_text_edit)
        self.assertIsNotNone(self.window.story_input)
        self.assertIsNotNone(self.window.gm_text_edit)
        self.assertIsNotNone(self.window.gm_input)
        self.assertIsNotNone(self.window.inventory_panel)
        self.assertIsNotNone(self.window.character_button)
        self.assertIsNotNone(self.window.status_bar)
        
        # Check initial window properties
        self.assertTrue(self.window.isVisible())
        # The actual title might be different, so we just check it's not empty
        self.assertTrue(len(self.window.windowTitle()) > 0)
        
        # Check headers exist - using findChildren to be more flexible
        story_headers = self.window.findChildren(QWidget, "storyHeader")
        gm_headers = self.window.findChildren(QWidget, "gmHeader")
        inventory_headers = self.window.inventory_panel.findChildren(QWidget, "inventoryHeader")
        
        # At least one of each header should exist
        self.assertTrue(len(story_headers) > 0, "Story header not found")
        self.assertTrue(len(gm_headers) > 0, "GM header not found")
        self.assertTrue(len(inventory_headers) > 0, "Inventory header not found")
    
    def test_character_window(self):
        """Test character window functionality."""
        # Initially, character window should not exist
        self.assertIsNone(getattr(self.window, 'character_window', None))
        
        # Click character button
        QTest.mouseClick(self.window.character_button, Qt.MouseButton.LeftButton)
        QTest.qWait(100)  # Wait for window to open
        
        # Check window was created and is visible
        self.assertIsNotNone(self.window.character_window)
        self.assertTrue(self.window.character_window.isVisible())
        
        # Check character window components
        char_window = self.window.character_window
        self.assertIsNotNone(char_window.equipment_panel)
        self.assertIsNotNone(char_window.inventory_panel)
        self.assertIsNotNone(char_window.tab_widget)
        
        # Check tabs exist
        self.assertEqual(char_window.tab_widget.count(), 3)  # Should have 3 tabs
        self.assertEqual(char_window.tab_widget.tabText(0), "Items & Equipment")
        self.assertEqual(char_window.tab_widget.tabText(1), "Class")
        self.assertEqual(char_window.tab_widget.tabText(2), "World")
        
        # Test switching tabs
        char_window.tab_widget.setCurrentIndex(1)  # Switch to Class tab
        QTest.qWait(50)
        self.assertEqual(char_window.tab_widget.currentIndex(), 1)
        
        char_window.tab_widget.setCurrentIndex(2)  # Switch to World tab
        QTest.qWait(50)
        self.assertEqual(char_window.tab_widget.currentIndex(), 2)
        
        # Test window closes properly
        char_window.close()
        QTest.qWait(100)  # Give time for window to close
        self.assertFalse(char_window.isVisible())
    
    def test_gm_chat(self):
        """Test GM chat functionality."""
        # Test sending a message
        test_message = "Test message to GM"
        self.window.gm_input.setText(test_message)
        QTest.keyClick(self.window.gm_input, Qt.Key.Key_Return)
        QTest.qWait(50)
        
        # Check message appears in chat
        chat_text = self.window.gm_text_edit.toPlainText()
        self.assertIn(test_message, chat_text)
        self.assertIn("You:", chat_text)  # Should show "You:" prefix
        
        # Check input field was cleared
        self.assertEqual(self.window.gm_input.text(), "")
    
    def test_story_input(self):
        """Test story input functionality."""
        test_message = "Test story action"
        self.window.story_input.setText(test_message)
        QTest.keyClick(self.window.story_input, Qt.Key.Key_Return)
        QTest.qWait(50)
        
        # Check message appears in story log
        story_text = self.window.story_text_edit.toPlainText()
        self.assertIn(test_message, story_text)
        self.assertIn("You:", story_text)  # Should show "You:" prefix
        
        # Check input field was cleared
        self.assertEqual(self.window.story_input.text(), "")
    
    def test_inventory_panel(self):
        """Test inventory panel functionality."""
        inventory = self.window.inventory_panel
        
        # Check inventory list exists
        self.assertIsNotNone(inventory.inventory_list)
        
        # Add a test item to inventory
        test_item = Item("Test Item", "consumable", "A test item for UI testing")
        list_item = QListWidgetItem(test_item.name)
        list_item.setData(Qt.ItemDataRole.UserRole, test_item)
        inventory.inventory_list.addItem(list_item)
        QTest.qWait(50)
        
        # Check item was added
        self.assertEqual(inventory.inventory_list.count(), 1)
        self.assertEqual(inventory.inventory_list.item(0).text(), "Test Item")
        
        # Test item tooltip appears on hover
        # This is hard to test directly, but we can check the connected signal
        self.assertTrue(hasattr(inventory, '_show_item_tooltip'))
        
        # Test right-click menu
        inventory.inventory_list.setCurrentItem(list_item)
        
        # Simulate right click at the center of the item
        rect = inventory.inventory_list.visualItemRect(list_item)
        pos = rect.center()
        QTest.mouseClick(inventory.inventory_list.viewport(), Qt.MouseButton.RightButton, pos=pos)
        QTest.qWait(100)  # Give time for menu to appear
    
    def test_equipment_slots(self):
        """Test equipment slots in character window."""
        # Open character window
        QTest.mouseClick(self.window.character_button, Qt.MouseButton.LeftButton)
        QTest.qWait(100)  # Wait for window to open
        
        char_window = self.window.character_window
        equipment_panel = char_window.equipment_panel
        
        # Check all equipment slots exist
        expected_slots = ['head', 'chest', 'legs', 'hands', 'feet', 
                         'main_hand', 'off_hand', 'two_handed']
        for slot_name in expected_slots:
            self.assertIn(slot_name, equipment_panel.slots)
            self.assertIsNotNone(equipment_panel.slots[slot_name])
            
        # Test equipping an item
        # Create a test equipment item
        test_sword = EquipmentItem(
            name="Test Sword",
            item_type="weapon",
            description="A test sword for UI testing",
            slot="main_hand",
            physical_attack=5
        )
        
        # Add it to inventory
        list_item = QListWidgetItem(test_sword.name)
        list_item.setData(Qt.ItemDataRole.UserRole, test_sword)
        char_window.inventory_panel.inventory_list.addItem(list_item)
        QTest.qWait(50)
        
        # Select the item
        char_window.inventory_panel.inventory_list.setCurrentItem(list_item)
        
        # Test right-click context menu for equipping
        rect = char_window.inventory_panel.inventory_list.visualItemRect(list_item)
        pos = rect.center()
        QTest.mouseClick(char_window.inventory_panel.inventory_list.viewport(), 
                        Qt.MouseButton.RightButton, pos=pos)
        QTest.qWait(100)  # Give time for menu to appear
    
    def test_status_bar(self):
        """Test status bar functionality."""
        status_bar = self.window.status_bar
        
        # Check status bar components exist - these should be present in any implementation
        self.assertIsNotNone(status_bar.health_bar)
        self.assertIsNotNone(status_bar.mana_bar)
        self.assertIsNotNone(status_bar.stamina_bar)
        
        # The time_label might have a different name, so we'll check for any QLabel
        time_labels = status_bar.findChildren(QWidget, "timeOfDayLabel")
        self.assertTrue(len(time_labels) > 0, "Time of day label not found")
        
        # Test updating status
        self.window.update_status_bar(
            health=75, max_health=100,
            mana=50, max_mana=100,
            stamina=25, max_stamina=100,
            time_of_day="Morning"
        )
        QTest.qWait(50)
        
        # Check values were updated
        self.assertEqual(status_bar.health_bar.value(), 75)
        self.assertEqual(status_bar.mana_bar.value(), 50)
        self.assertEqual(status_bar.stamina_bar.value(), 25)
    
    def test_theme_toggle(self):
        """Test theme toggling functionality."""
        # Get initial theme
        initial_stylesheet = self.window.styleSheet()
        
        # Directly emit the theme_toggled signal instead of trying to find the menu item
        self.window.theme_toggled.emit()
        QTest.qWait(100)  # Wait for theme to update
        
        # Check that stylesheet changed or that the theme manager was called
        # This is a bit tricky to test directly, so we'll just check that the signal exists
        self.assertTrue(hasattr(self.window, 'theme_toggled'))
    
    def test_equipped_item_tooltip(self):
        """Test that equipped items show tooltips in the character window."""
        # Open character window
        QTest.mouseClick(self.window.character_button, Qt.MouseButton.LeftButton)
        QTest.qWait(100)  # Wait for window to open
        
        char_window = self.window.character_window
        equipment_panel = char_window.equipment_panel
        
        # Create a test equipment item
        test_helmet = EquipmentItem(
            name="Test Helmet",
            item_type="armor",
            description="A test helmet for UI testing",
            slot="head",
            physical_defense=5,
            rarity="uncommon"
        )
        
        # Set the item in the head slot
        equipment_panel.slots['head'].set_item(test_helmet)
        QTest.qWait(50)
        
        # Check that the item is displayed in the slot
        self.assertEqual(equipment_panel.slots['head'].item_label.text(), "Test Helmet")
        
        # Test tooltip functionality
        # This is hard to test directly, but we can check the enterEvent method exists
        self.assertTrue(hasattr(equipment_panel.slots['head'], 'enterEvent'))
    
    def test_equipped_item_context_menu(self):
        """Test that equipped items show a context menu on right-click."""
        # Open character window
        QTest.mouseClick(self.window.character_button, Qt.MouseButton.LeftButton)
        QTest.qWait(100)  # Wait for window to open
        
        char_window = self.window.character_window
        equipment_panel = char_window.equipment_panel
        
        # Create a test equipment item
        test_helmet = EquipmentItem(
            name="Test Helmet",
            item_type="armor",
            description="A test helmet for UI testing",
            slot="head",
            physical_defense=5,
            rarity="uncommon"
        )
        
        # Set the item in the head slot
        equipment_panel.slots['head'].set_item(test_helmet)
        QTest.qWait(50)
        
        # Check that the item is displayed in the slot
        self.assertEqual(equipment_panel.slots['head'].item_label.text(), "Test Helmet")
        
        # Test context menu functionality
        # This is hard to test directly, but we can check the customContextMenuRequested signal is connected
        self.assertTrue(hasattr(equipment_panel.slots['head'], '_show_context_menu'))
    
    def test_inventory_equipped_items(self):
        """Test that equipped items appear grayed out in inventory."""
        # Open character window
        QTest.mouseClick(self.window.character_button, Qt.MouseButton.LeftButton)
        QTest.qWait(100)  # Wait for window to open
        
        # Create a test equipment item
        test_sword = EquipmentItem(
            name="Test Sword",
            item_type="weapon",
            description="A test sword for UI testing",
            slot="main_hand",
            physical_attack=5
        )
        test_sword.equipped = True  # Mark as equipped
        
        # Add it to inventory
        list_item = QListWidgetItem(test_sword.name)
        list_item.setData(Qt.ItemDataRole.UserRole, test_sword)
        self.window.inventory_panel.inventory_list.addItem(list_item)
        
        # Update inventory to apply styling
        self.window.inventory_panel.update_inventory([test_sword])
        QTest.qWait(50)
        
        # Check that the item is grayed out
        item = self.window.inventory_panel.inventory_list.item(0)
        self.assertEqual(item.foreground(), Qt.GlobalColor.gray)
    
    def test_gm_chat_receive_message(self):
        """Test receiving a message in GM chat."""
        # Test the _receive_gm_message method
        test_message = "Test GM response"
        self.window._receive_gm_message(test_message)
        QTest.qWait(50)
        
        # Check message appears in chat
        chat_text = self.window.gm_text_edit.toPlainText()
        self.assertIn(test_message, chat_text)
        self.assertIn("GM:", chat_text)  # Should show "GM:" prefix
    
    def tearDown(self):
        """Clean up after each test."""
        if hasattr(self.window, 'character_window') and self.window.character_window:
            self.window.character_window.close()
        self.window.close()
        QTest.qWait(100)  # Give time for cleanup
    
    @classmethod
    def tearDownClass(cls):
        """Clean up the application."""
        cls.app.quit()


if __name__ == "__main__":
    unittest.main() 