# UI Tests for LLM Game UI

This directory contains UI tests for the LLM Game UI application. These tests focus on verifying that the UI components work correctly and interact properly with each other.

## Overview

The tests are designed to verify:
- Initial window state and component presence
- Character window functionality
- GM chat and story input functionality
- Inventory panel interactions
- Equipment slots and item interactions
- Status bar updates
- Theme toggling
- Tooltips and context menus for equipped items

## Running the Tests

### Using the Test Runner

The simplest way to run all tests is to use the provided test runner:

```bash
python tests/run_tests.py
```

### Using pytest

If you have pytest installed, you can run the tests with:

```bash
pytest
```

Or to run a specific test:

```bash
pytest tests/test_ui.py::TestUI::test_character_window
```

## Test Dependencies

To run the tests, you'll need:
- PyQt6
- pytest (optional, for running with pytest)
- pytest-qt (optional, for better Qt integration with pytest)

Install the development dependencies with:

```bash
pip install -r requirements-dev.txt
```

## Test Structure

- `test_ui.py`: Contains the main UI test suite
- `run_tests.py`: Simple test runner script
- `__init__.py`: Marks the directory as a Python package

## Adding New Tests

To add a new test:

1. Add a new test method to the `TestUI` class in `test_ui.py`
2. Follow the naming convention `test_*` for your test method
3. Use `self.window` to access the main window
4. Use `QTest` methods to simulate user interactions
5. Use `QTest.qWait()` to give time for UI updates
6. Clean up any resources in the `tearDown` method

Example:

```python
def test_new_feature(self):
    """Test a new feature."""
    # Setup
    self.window.some_button.click()
    QTest.qWait(100)  # Wait for UI to update
    
    # Test
    self.assertTrue(self.window.some_result)
    
    # Cleanup (if needed)
    self.window.close_button.click()
```

## Best Practices

1. **Keep tests independent**: Each test should be able to run on its own
2. **Clean up after tests**: Close any windows or dialogs you open
3. **Use appropriate wait times**: UI operations need time to complete
4. **Test behavior, not implementation**: Focus on what the user sees and does
5. **Be flexible with selectors**: Use `findChildren` instead of direct access when possible
6. **Handle styling differences**: Tests might run without the full styling from main.py

## Troubleshooting

- If tests fail with "QWidget: Cannot create a QWidget without QApplication", make sure `QApplication` is created in `setUpClass`
- If tests fail with timing issues, try increasing the `QTest.qWait()` duration
- If tests fail with "Object not found", check that you're using the correct object names and paths 