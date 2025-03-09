from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from .item import Item, EquipmentItem


@dataclass
class Skill:
    name: str
    description: str
    level: int = 1
    experience: int = 0
    cost: Dict[str, Any] = field(default_factory=dict)
    effects: List[Dict[str, Any]] = field(default_factory=list)
    target_group: str = "enemies"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "level": self.level,
            "experience": self.experience,
            "cost": self.cost,
            "effects": self.effects,
            "target_group": self.target_group
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Skill':
        return cls(
            name=data["name"],
            description=data["description"],
            level=data.get("level", 1),
            experience=data.get("experience", 0),
            cost=data.get("cost", {}),
            effects=data.get("effects", []),
            target_group=data.get("target_group", "enemies")
        )


@dataclass
class CharacterClass:
    name: str
    description: str
    skills: List[Skill] = field(default_factory=list)
    rarity: str = "common"
    tags: Dict[str, List[str]] = field(default_factory=lambda: {"tags": []})
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "skills": [skill.to_dict() for skill in self.skills],
            "rarity": self.rarity,
            "tags": self.tags
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CharacterClass':
        skills = [Skill.from_dict(skill) for skill in data.get("skills", [])]
        return cls(
            name=data["name"],
            description=data["description"],
            skills=skills,
            rarity=data.get("rarity", "common"),
            tags=data.get("tags", {"tags": []})
        )


@dataclass
class CharacterEquipment:
    DEFAULT_SLOTS = {
        'head': None,
        'chest': None,
        'legs': None,
        'hands': None,
        'feet': None,
        'main_hand': None,
        'off_hand': None,
        'two_handed': None,
        'accessories': []
    }
    MAX_ACCESSORIES = 5
    
    equipment: Dict[str, Any] = field(default_factory=lambda: {
        slot: None for slot in CharacterEquipment.DEFAULT_SLOTS
    })
    
    def __post_init__(self):
        if 'accessories' not in self.equipment:
            self.equipment['accessories'] = []
    
    def equip(self, item: EquipmentItem) -> bool:
        slot = item.slot
        
        # Check if the slot exists
        if slot not in self.equipment and slot != 'accessories':
            return False
        
        # Handle two-handed weapons
        if slot == 'two_handed':
            self.unequip('main_hand')
            self.unequip('off_hand')
            self.equipment['two_handed'] = item
        elif slot == 'main_hand' or slot == 'off_hand':
            if self.equipment.get('two_handed'):
                return False  # Cannot equip one-handed weapons if a two-handed weapon is equipped
            self.unequip(slot)
            self.equipment[slot] = item
        elif slot == 'accessories':
            if len(self.equipment['accessories']) >= self.MAX_ACCESSORIES:
                return False
            self.equipment['accessories'].append(item)
        else:
            self.unequip(slot)
            self.equipment[slot] = item
        
        return True
    
    def unequip(self, slot: str) -> bool:
        if slot not in self.equipment:
            return False
        
        if slot == 'accessories':
            return False  # Need to specify which accessory to unequip
        
        self.equipment[slot] = None
        return True
    
    def unequip_accessory(self, item: EquipmentItem) -> bool:
        if item in self.equipment['accessories']:
            self.equipment['accessories'].remove(item)
            return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for slot, item in self.equipment.items():
            if slot == 'accessories':
                result[slot] = [item.to_dict() if item else None for item in self.equipment['accessories']]
            else:
                result[slot] = item.to_dict() if item else None
        return result


@dataclass
class Character:
    name: str
    character_class: CharacterClass
    level: int = 1
    experience: int = 0
    experience_to_next_level: int = 100
    health: int = 100
    max_health: int = 100
    mana: int = 50
    max_mana: int = 50
    stamina: int = 100
    max_stamina: int = 100
    strength: int = 10
    endurance: int = 10
    focus: int = 10
    willpower: int = 10
    agility: int = 10
    luck: int = 10
    charisma: int = 10
    equipment: CharacterEquipment = field(default_factory=CharacterEquipment)
    inventory: List[Item] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "character_class": self.character_class.to_dict(),
            "level": self.level,
            "experience": self.experience,
            "experience_to_next_level": self.experience_to_next_level,
            "health": self.health,
            "max_health": self.max_health,
            "mana": self.mana,
            "max_mana": self.max_mana,
            "stamina": self.stamina,
            "max_stamina": self.max_stamina,
            "strength": self.strength,
            "endurance": self.endurance,
            "focus": self.focus,
            "willpower": self.willpower,
            "agility": self.agility,
            "luck": self.luck,
            "charisma": self.charisma,
            "equipment": self.equipment.to_dict(),
            "inventory": [item.to_dict() for item in self.inventory]
        }
    
    @property
    def skills(self) -> List[Skill]:
        return self.character_class.skills
    
    def add_to_inventory(self, item: Item) -> bool:
        self.inventory.append(item)
        return True
    
    def remove_from_inventory(self, item: Item) -> bool:
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False
    
    def equip_item(self, item: EquipmentItem) -> bool:
        if item not in self.inventory:
            return False
        
        if self.equipment.equip(item):
            self.remove_from_inventory(item)
            return True
        
        return False
    
    def unequip_item(self, slot: str) -> bool:
        if slot not in self.equipment.equipment:
            return False
        
        item = self.equipment.equipment[slot]
        if item:
            self.equipment.unequip(slot)
            self.add_to_inventory(item)
            return True
        
        return False
    
    def unequip_accessory(self, item: EquipmentItem) -> bool:
        if self.equipment.unequip_accessory(item):
            self.add_to_inventory(item)
            return True
        return False 