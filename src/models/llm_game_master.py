from src.models.game_master import GameMaster
import random
import time

class LLMGameMaster(GameMaster):
    """
    A GameMaster that uses an LLM for generating responses.
    This is a simulated version for demonstration purposes.
    In a real implementation, you would connect to an actual LLM API.
    """
    
    def __init__(self):
        super().__init__()
        self.context = []
        self.character_name = ""
        self.game_state = {
            "location": "village",
            "inventory": [],
            "quests": [],
            "npc_relationships": {}
        }
    
    def _simulate_llm_response(self, prompt):
        """
        Simulate an LLM response.
        In a real implementation, this would call an actual LLM API.
        """
        # Add a small delay to simulate API call
        time.sleep(1)
        
        # Simple response templates based on keywords
        responses = {
            "hello": [
                "Greetings, adventurer! How may I assist you today?",
                "Hello there! Ready for an adventure?",
                "Well met, traveler! What brings you to these parts?"
            ],
            "help": [
                "I can help you navigate this world. Try asking about locations, items, or quests.",
                "Need assistance? You can ask me about the world, your character, or available quests.",
                "I'm here to guide your adventure. What would you like to know?"
            ],
            "quest": [
                f"There are rumors of a dragon terrorizing the northern mountains. The village elder is offering a reward for anyone brave enough to investigate.",
                f"The local merchant guild is looking for someone to escort a valuable shipment to the next town. Interested?",
                f"I've heard whispers of an ancient artifact hidden in the ruins east of here. Many have sought it, none have returned."
            ],
            "village": [
                "The village is a small settlement with a few dozen buildings. There's an inn, a blacksmith, and a general store.",
                "This quaint village has stood for generations. The people are friendly but wary of strangers.",
                "The village is bustling with activity. Merchants hawk their wares, children play in the streets, and guards patrol the perimeter."
            ],
            "forest": [
                "The forest is dense and dark. Strange sounds echo through the trees, and you feel watched.",
                "Tall trees block out much of the sunlight. The forest floor is covered in moss and fallen leaves.",
                "The ancient forest is home to many creatures, both mundane and magical. Tread carefully."
            ],
            "mountain": [
                "The mountains loom large on the horizon. Their peaks are covered in snow year-round.",
                "The mountain path is treacherous and steep. Few travelers dare to make the journey.",
                "Legends speak of a dragon that makes its lair in these mountains. Some say it guards a vast treasure."
            ],
            "inn": [
                "The inn is warm and inviting. The innkeeper greets you with a smile.",
                "The smell of fresh bread and ale fills the air. The inn is crowded with travelers and locals alike.",
                "The inn is a two-story building with a thatched roof. A sign depicting a prancing pony hangs above the door."
            ]
        }
        
        # Check for keywords in the prompt
        for keyword, response_list in responses.items():
            if keyword in prompt.lower():
                return random.choice(response_list)
        
        # Default responses if no keywords match
        default_responses = [
            f"I understand. What would you like to do next?",
            f"Interesting. How would you like to proceed?",
            f"I see. What's your next move?",
            f"That's a unique approach. What else would you like to try?",
            f"Very well. Where would you like to go now?"
        ]
        
        return random.choice(default_responses)
    
    def _run_conversation(self):
        """Main conversation loop using the simulated LLM."""
        # Introduction
        self._send_message("Welcome, adventurer! I am your Game Master. What is your name?")
        self.character_name = self._wait_for_response()
        
        if not self.running:
            return
        
        # Add to context
        self.context.append(f"Player name: {self.character_name}")
        
        # Continue conversation
        self._send_message(f"Well met, {self.character_name}! You find yourself in a small village at the edge of a vast kingdom. What would you like to do?")
        
        # Main conversation loop
        while self.running:
            # Wait for player input
            player_message = self._wait_for_response()
            
            if not self.running or player_message == "CONVERSATION_TERMINATED":
                break
            
            # Add to context
            self.context.append(f"Player: {player_message}")
            
            # Generate response using simulated LLM
            response = self._simulate_llm_response(player_message)
            
            # Add to context
            self.context.append(f"GM: {response}")
            
            # Send response to player
            self._send_message(response)
            
            # Limit context size to prevent it from growing too large
            if len(self.context) > 20:
                self.context = self.context[-10:] 