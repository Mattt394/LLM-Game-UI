from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from queue import Queue
from threading import Thread, Event
import time

class GameMaster(QObject):
    """
    Backend class that manages the game's narrative flow and interactions.
    This class is separate from the UI but can communicate with it.
    """
    
    # Signals to communicate with the UI
    send_gm_message = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.response_queue = Queue()
        self.waiting_for_response = Event()
        self.running = False
        self.conversation_thread = None
    
    def start_conversation(self):
        """Start the conversation in a separate thread."""
        if self.conversation_thread and self.conversation_thread.is_alive():
            return  # Already running
        
        self.running = True
        self.conversation_thread = Thread(target=self._run_conversation)
        self.conversation_thread.daemon = True  # Thread will exit when main program exits
        self.conversation_thread.start()
    
    def stop_conversation(self):
        """Stop the conversation thread."""
        self.running = False
        if self.waiting_for_response.is_set():
            self.waiting_for_response.clear()
            self.response_queue.put("CONVERSATION_TERMINATED")
    
    def receive_player_message(self, message):
        """Called by the UI when the player sends a message."""
        if self.waiting_for_response.is_set():
            self.response_queue.put(message)
            self.waiting_for_response.clear()
    
    def _send_message(self, message):
        """Send a message to the GM chat in the UI."""
        # We use emit to send the message to the UI
        self.send_gm_message.emit(message)
    
    def _wait_for_response(self, timeout=None):
        """Wait for the player to respond."""
        self.waiting_for_response.set()
        
        # Wait for a response
        start_time = time.time()
        while self.waiting_for_response.is_set() and self.running:
            if timeout and time.time() - start_time > timeout:
                self.waiting_for_response.clear()
                return None
            time.sleep(0.1)
        
        # Get the response from the queue
        if not self.response_queue.empty():
            return self.response_queue.get()
        return None
    
    def _run_conversation(self):
        """Main conversation loop. Override this in subclasses."""
        self._send_message("Hello! I'm your Game Master. What's your name?")
        name = self._wait_for_response()
        
        if not self.running:
            return
        
        self._send_message(f"Nice to meet you, {name}! What kind of adventure are you looking for today?")
        adventure_type = self._wait_for_response()
        
        if not self.running:
            return
        
        # Example of altering and sending back a message
        modified_response = f"Ah, so you want {adventure_type.lower()}? " \
                          f"That's quite ambitious! Let me think about that..."
        self._send_message(modified_response)
        
        # More conversation can continue here...
        self._send_message("I've prepared a special adventure for you. Are you ready to begin?")
        ready = self._wait_for_response()
        
        if not self.running:
            return
        
        if "yes" in ready.lower():
            self._send_message("Excellent! Let's begin your journey...")
            # Start the actual game here
        else:
            self._send_message("No rush. Let me know when you're ready.")


class StorytellerGM(GameMaster):
    """
    A GameMaster that tells a pre-written story with branching paths.
    This is just an example of how you could extend the GameMaster class.
    """
    
    def __init__(self, story_data=None):
        super().__init__()
        self.story_data = story_data or {}
        self.current_node = "start"
        self.player_state = {
            "name": "",
            "choices": []
        }
    
    def _run_conversation(self):
        """Run through the story nodes."""
        while self.running and self.current_node in self.story_data:
            node = self.story_data[self.current_node]
            
            # Send the node text
            self._send_message(node["text"])
            
            # If this is an end node, exit
            if "choices" not in node:
                break
                
            # Wait for player response
            response = self._wait_for_response()
            if not self.running:
                break
                
            # Process the response and determine the next node
            self.player_state["choices"].append(response)
            
            # Simple choice matching (in a real implementation, you'd want more sophisticated matching)
            next_node = None
            for choice in node["choices"]:
                if choice["keywords"] and any(keyword.lower() in response.lower() for keyword in choice["keywords"]):
                    next_node = choice["next"]
                    break
            
            # Default to the first choice if no match
            if not next_node and node["choices"]:
                next_node = node["choices"][0]["next"]
                
            self.current_node = next_node


# Example story data structure
example_story = {
    "start": {
        "text": "You find yourself standing at the entrance of a dark cave. A cool breeze flows from within. What do you do?",
        "choices": [
            {"keywords": ["enter", "go in", "inside"], "next": "cave_entrance"},
            {"keywords": ["leave", "go back", "return"], "next": "forest_path"}
        ]
    },
    "cave_entrance": {
        "text": "As you step into the cave, your eyes adjust to the darkness. You see two tunnels ahead. One seems to slope downward, the other curves to the right. Which way do you go?",
        "choices": [
            {"keywords": ["down", "downward", "slope"], "next": "lower_cavern"},
            {"keywords": ["right", "curve", "curved"], "next": "crystal_chamber"}
        ]
    },
    "forest_path": {
        "text": "You decide not to enter the cave and instead follow a path through the forest. After walking for a while, you come across a small village. Do you approach it?",
        "choices": [
            {"keywords": ["yes", "approach", "enter"], "next": "village"},
            {"keywords": ["no", "continue", "forest"], "next": "deep_forest"}
        ]
    },
    # More nodes would be defined here...
} 