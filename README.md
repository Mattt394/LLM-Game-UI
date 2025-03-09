# AI-Driven Text Adventure Game UI

A modern, responsive UI for a text-based adventure game where an AI acts as the Game Master (GM).

## Features

- Text-based adventure game interface
- Main story window with input field for roleplaying actions
- GM & Log chatbox for game responses and OOC conversations
- Inventory panel with item interactions
- Character window with equipment, class, and world information
- Status bar showing health, mana, stamina, and time of day

## Technical Stack

- Python 3.8+
- PyQt6 for the UI framework
- Dark mode support with darkdetect

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python src/main.py
   ```

## Project Structure

```
.
├── specs/                  # Game specifications
├── src/
│   ├── assets/             # Static assets
│   │   └── styles/         # CSS stylesheets
│   ├── models/             # Data models
│   ├── ui/                 # UI components
│   ├── utils/              # Utility functions
│   └── main.py             # Application entry point
└── requirements.txt        # Python dependencies
```

## Development

This UI is designed to be independent from backend logic, serving as a frontend to be hooked up later. It provides a modern, responsive interface for text-based adventure games with structured gameplay mechanics. 