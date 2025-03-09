# AI-Driven Text Adventure Game UI

A modern, responsive UI for a text-based adventure game where an AI acts as the Game Master (GM).

## Features

### Completed Features
- Text-based adventure game interface with dark/light theme support
- Main story window with input field for roleplaying actions
- GM chat panel for out-of-character conversations
- Inventory system with:
  - Item examination via tooltips
  - Equipment system with visual slot layout
  - Context menu for item actions (equip/unequip, examine, use, drop)
  - Visual feedback for equipped items (grayed out in inventory)
- Character window with:
  - Equipment management with visual slot layout
  - Class information and skills display
  - World information and location tracking
  - Inventory management
- Status bar showing health, mana, stamina, and time of day
- Clean, modern UI with consistent styling
- Proper state management between panels

### Planned Features
- Backend integration for actual gameplay
- Save/load game functionality
- Character creation system
- Combat system UI
- Quest tracking system
- NPC interaction dialogs
- Party system for multiplayer support
- Sound effects and background music
- Customizable UI themes
- Accessibility features

## Technical Stack

- Python 3.8+
- PyQt6 for the UI framework
- Dark/Light mode theme support

## Installation

1. Clone this repository
```bash
git clone [repository-url]
cd [repository-name]
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python src/main.py
```

## Project Structure

```
.
├── specs/                  # Game specifications
├── src/
│   ├── assets/            # Static assets
│   │   └── styles/        # CSS stylesheets
│   ├── models/            # Data models
│   ├── ui/                # UI components
│   ├── utils/             # Utility functions
│   └── main.py           # Application entry point
├── requirements.txt       # Python dependencies
├── LICENSE               # MIT License
└── README.md            # This file
```

## Development

This UI is designed to be independent from backend logic, serving as a frontend to be hooked up later. It provides a modern, responsive interface for text-based adventure games with structured gameplay mechanics.

### Current State
The project currently implements a fully functional UI with:
- Complete inventory and equipment management
- Character class and skills display
- World information panel
- Theme support (dark/light)
- Proper state management between different panels

### Next Steps
To make this a complete game, the following would be needed:
1. Backend game engine integration
2. Game state management system
3. Save/load functionality
4. Combat system implementation
5. Quest system
6. NPC interaction system
7. Multiplayer support (optional)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 