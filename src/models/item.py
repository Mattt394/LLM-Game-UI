from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


@dataclass
class Effect:
    target_group: str
    action: str
    value: int = 0
    tags: Dict[str, List[str]] = field(default_factory=lambda: {"tags": []})


@dataclass
class Item:
    name: str
    item_type: str
    description: str
    effects: List[Effect] = field(default_factory=list)
    target_group: str = "single_ally"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "item_type": self.item_type,
            "description": self.description,
            "effects": [vars(effect) for effect in self.effects],
            "target_group": self.target_group
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Item':
        effects = [Effect(**effect) for effect in data.get("effects", [])]
        return cls(
            name=data["name"],
            item_type=data["item_type"],
            description=data["description"],
            effects=effects,
            target_group=data.get("target_group", "single_ally")
        )


@dataclass
class EquipmentItem(Item):
    slot: str = "main_hand"
    rarity: str = "common"
    level_requirement: int = 1
    physical_attack: int = 0
    physical_defense: int = 0
    magic_attack: int = 0
    magic_defense: int = 0
    attack_dice: List[str] = field(default_factory=list)
    tags: Dict[str, List[str]] = field(default_factory=lambda: {"tags": []})
    equipped: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        item_dict = super().to_dict()
        item_dict.update({
            "slot": self.slot,
            "rarity": self.rarity,
            "level_requirement": self.level_requirement,
            "physical_attack": self.physical_attack,
            "physical_defense": self.physical_defense,
            "magic_attack": self.magic_attack,
            "magic_defense": self.magic_defense,
            "attack_dice": self.attack_dice,
            "tags": self.tags,
            "equipped": self.equipped
        })
        return item_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EquipmentItem':
        item = super().from_dict(data)
        return cls(
            name=item.name,
            item_type=item.item_type,
            description=item.description,
            effects=item.effects,
            target_group=item.target_group,
            slot=data.get("slot", "main_hand"),
            rarity=data.get("rarity", "common"),
            level_requirement=data.get("level_requirement", 1),
            physical_attack=data.get("physical_attack", 0),
            physical_defense=data.get("physical_defense", 0),
            magic_attack=data.get("magic_attack", 0),
            magic_defense=data.get("magic_defense", 0),
            attack_dice=data.get("attack_dice", []),
            tags=data.get("tags", {"tags": []}),
            equipped=data.get("equipped", False)
        ) 