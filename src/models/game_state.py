from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from .character import Character


@dataclass
class Location:
    name: str
    description: str
    connections: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "connections": self.connections
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Location':
        return cls(
            name=data["name"],
            description=data["description"],
            connections=data.get("connections", [])
        )


@dataclass
class GameState:
    character: Character
    current_location: Location
    story_log: List[Dict[str, str]] = field(default_factory=list)
    gm_log: List[Dict[str, str]] = field(default_factory=list)
    time_of_day: str = "Morning"
    
    def add_story_message(self, message: str, sender: str = "GM") -> None:
        """Add a message to the story log."""
        self.story_log.append({
            "sender": sender,
            "message": message
        })
    
    def add_gm_message(self, message: str, sender: str = "Player") -> None:
        """Add a message to the GM log."""
        self.gm_log.append({
            "sender": sender,
            "message": message
        })
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "character": self.character.to_dict(),
            "current_location": self.current_location.to_dict(),
            "story_log": self.story_log,
            "gm_log": self.gm_log,
            "time_of_day": self.time_of_day
        }
    
    @classmethod
    def create_demo_state(cls) -> 'GameState':
        """Create a demo game state for UI testing."""
        from .character import CharacterClass, Skill, Character, CharacterEquipment
        from .item import Item, EquipmentItem, Effect
        
        # Create a demo character class
        arcane_adept_skills = [
            Skill(
                name="Blast",
                description="The Arcane Adept launches a blast of arcane energy at an enemy.",
                cost={"resource": "mana", "amount": 8},
                effects=[{
                    "action": "damage",
                    "value": 14,
                    "dice": ["1d10"],
                    "tags": {"tags": ["magic", "fire"]},
                    "target_group": "single_enemy"
                }]
            ),
            Skill(
                name="Heal Pulse",
                description="The Arcane Adept launches a healing pulse at their allies.",
                cost={"resource": "mana", "amount": 8},
                effects=[{
                    "action": "heal",
                    "value": 20,
                    "dice": ["1d10"],
                    "tags": {"tags": ["magic"]},
                }]
            ),
            Skill(
                name="Hypnotise",
                description="The Arcane Adept hypnotizes an enemy, causing them to fall asleep.",
                cost={"resource": "mana", "amount": 12},
                effects=[{
                    "action": "status",
                    "value": 2,
                    "status": "sleep",
                    "tags": {"tags": ["magic", "mind"]},
                    "target_group": "single_enemy"
                }]
            )
        ]
        
        arcane_adept = CharacterClass(
            name="Arcane Adept",
            description="The Arcane Adept is a basic magic user who specializes in fundamental magical skills. They are adept at casting spells to attack, heal, and boost the stats of themselves or their allies.",
            skills=arcane_adept_skills
        )
        
        # Create demo items
        health_potion = Item(
            name="Health Potion",
            item_type="consumable",
            description="A small vial filled with a red liquid. When consumed, it instantly restores 30 health points to an ally.",
            effects=[Effect(
                target_group="allies",
                action="heal",
                value=30
            )]
        )
        
        mana_potion = Item(
            name="Mana Potion",
            item_type="consumable",
            description="A small vial filled with a blue liquid. When consumed, it instantly restores 20 mana points to an ally.",
            effects=[Effect(
                target_group="allies",
                action="restore_mana",
                value=20
            )]
        )
        
        fire_sword = EquipmentItem(
            name="Fire Elemental Sword",
            item_type="weapon",
            description="A basic sword. But made of fire.",
            slot="main_hand",
            rarity="uncommon",
            level_requirement=1,
            physical_attack=0,
            physical_defense=0,
            magic_attack=0,
            magic_defense=0,
            attack_dice=["1d6"],
            tags={"tags": ["fire"]}
        )
        
        leather_armor = EquipmentItem(
            name="Leather Armor",
            item_type="armor",
            description="Basic leather armor that provides minimal protection.",
            slot="chest",
            rarity="common",
            level_requirement=1,
            physical_attack=0,
            physical_defense=2,
            magic_attack=0,
            magic_defense=1,
            tags={"tags": ["light"]}
        )
        
        wizard_hat = EquipmentItem(
            name="Wizard Hat",
            item_type="armor",
            description="A pointy hat that enhances magical abilities.",
            slot="head",
            rarity="common",
            level_requirement=1,
            physical_attack=0,
            physical_defense=0,
            magic_attack=2,
            magic_defense=1,
            tags={"tags": ["cloth", "magic"]}
        )
        
        # Create a demo character
        character = Character(
            name="Elyndra",
            character_class=arcane_adept,
            health=80,
            max_health=100,
            mana=40,
            max_mana=50,
            stamina=60,
            max_stamina=80,
            strength=8,
            endurance=10,
            focus=14,
            willpower=12,
            agility=10,
            luck=8,
            charisma=10
        )
        
        # Add items to inventory
        character.add_to_inventory(health_potion)
        character.add_to_inventory(mana_potion)
        character.add_to_inventory(fire_sword)
        character.add_to_inventory(leather_armor)
        character.add_to_inventory(wizard_hat)
        
        # Create a demo location
        forest_clearing = Location(
            name="Forest Clearing",
            description="A peaceful clearing in the middle of a dense forest. Sunlight filters through the canopy, illuminating a small pond in the center.",
            connections=["Forest Path", "Cave Entrance", "Mountain Trail"]
        )
        
        # Create demo story log
        story_log = [
            {"sender": "GM", "message": "You find yourself in a peaceful clearing in the middle of a dense forest. Sunlight filters through the canopy, illuminating a small pond in the center."},
            {"sender": "GM", "message": "The air is fresh and filled with the scent of pine and wildflowers. Birds chirp happily in the trees around you."},
            {"sender": "Player", "message": "I approach the pond and look at my reflection."},
            {"sender": "GM", "message": "As you approach the pond, you see your reflection in the clear water. You notice movement in the trees behind you."}
        ]
        
        # Create demo GM log
        gm_log = [
            {"sender": "Player", "message": "Is there anything special about this clearing?"},
            {"sender": "GM", "message": "This clearing is known as the 'Heart of the Forest' by locals. It's said to have magical properties, especially during the full moon."},
            {"sender": "Player", "message": "What's the movement I noticed in the trees?"},
            {"sender": "GM", "message": "Roll a perception check to find out."}
        ]
        
        # Create and return the game state
        return cls(
            character=character,
            current_location=forest_clearing,
            story_log=story_log,
            gm_log=gm_log,
            time_of_day="Dusk"
        ) 