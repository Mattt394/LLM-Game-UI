arcane_adept = {
    "name": "Arcane Adept",
    "description": "The Arcane Adept is a basic magic user who specializes in fundamental magical skills. They are adept at casting spells to attack, heal, and boost the stats of themselves or their allies.",
    "skills": [
      {
        "name": "Blast",
        "level": 1,
        "experience": 0,
        "description": "The Arcane Adept launches a blast of arcane energy at an enemy.",
        "cost": {
          "resource": "mana",
          "amount": 8,
          "level_up_formula": "x*1.1"
        },
          "target_group": "enemies",
        "effects": [
          {
            "action": "damage",
            "value": 14,
            "dice": ["1d10"],
            "tags": {'tags':['magic', 'fire']},
            "level_up_formula": "x*(1+(0.04*(level-1)))",
              "target_group": "single_enemy"
          }
        ]
        },
        {
        "name": "Heal Pulse",
        "level": 1,
        "experience": 0,
        "description": "The Arcane Adept launches a healing pulse at their allies.",
        "cost": {
          "resource": "mana",
          "amount": 8,
          "level_up_formula": "x*1.1"
        },
          "target_group": "allies",
        "effects": [
          {
            "action": "heal",
            "value": 20,
            "dice": ["1d10"],
            "tags": {'tags':['magic']},
            "level_up_formula": "x*(1+(0.04*(level-1)))"
          }
        ]
        },
        {
        "name": "Hypnotise",
        "level": 1,
        "experience": 0,
        "description": "The Arcane Adept hypnotizes a target for a short time, causing them to lose their turn",
        "cost": {
          "resource": "mana",
          "amount": 8,
          "level_up_formula": "x*1.1"
        },
          "target_group": "single_target",
        "effects": [
          {
            "action": "stun",
            "duration": 1,
            "tags": {'tags':['magic']},
            "level_up_formula": "x*(1+(0.04*(level-1)))"
          }
        ]
        },
        {
        "name": "Cheer",
        "level": 1,
        "experience": 0,
        "description": "The Arcane Adept cheers for an ally, increasing their attack",
        "cost": {
          "resource": "stamina",
          "amount": 8,
          "level_up_formula": "x*1.1"
        },
          "target_group": "single_ally",
        "effects": [
          {
                "action": "boost",
                "value": 12,
                "stat_names": ["strength"],
                "duration": 5,
              "tags": {'tags':['magic']},
                "level_up_formula": "x*(1+(0.03*(level-1)))"
              }
        ]
        },
        {
        "name": "Drunken Cheer",
        "level": 1,
        "experience": 0,
        "description": "The Arcane Adept cheers for a random ally, increasing their strength",
        "cost": {
          "resource": "stamina",
          "amount": 8,
          "level_up_formula": "x*1.1"
        },
          "target_group": "random_ally",
        "effects": [
          {
                "action": "boost",
                "value": 12,
                "stat_names": ["strength"],
                "duration": 5,
              "tags": {'tags':['magic']},
                "level_up_formula": "x*(1+(0.03*(level-1)))"
              }
        ]
        },
        {
        "name": "Limit Break",
        "level": 1,
        "experience": 0,
        "description": "The Arcane Adept breaks his limits, increasing stats",
        "cost": {
          "resource": "mana",
          "amount": 30,
          "level_up_formula": "x*1.1"
        },
          "target_group": "self",
        "effects": [
          {
                "action": "boost",
                "boost_percentage": 1.1,
                "stat_names": ["strength", "endurance", "focus", "willpower"],
                "duration": 5,
              "tags": {'tags':['magic']},
                "level_up_formula": "x*(1+(0.03*(level-1)))"
              }
        ]
        },
        {
        "name": "Nova",
        "level": 1,
        "experience": 0,
        "description": "The Arcane Adept goes Nova",
        "cost": {
          "resource": "mana",
          "amount": 30,
          "level_up_formula": "x*1.1"
        },
          "target_group": "all",
        "effects": [
          {
            "action": "damage",
            "value": 50,
            "dice": ["1d10"],
            "tags": {'tags':['magic', 'fire', "light"]},
            "level_up_formula": "x*(1+(0.04*(level-1)))"
          }
        ]
        },
        {
        "name": "Leadership Aura",
        "level": 1,
        "experience": 0,
        "description": "The Arcane Adept has an aura of leadership",
      "is_passive": True,
        "cost": {
          "resource": "mana",
          "amount": 0,
          "level_up_formula": "x*1.1"
        },
          "target_group": "allies",
        "effects": [
          {
                "action": "boost",
                "boost_percentage": 1.0,
                "stat_names": ["strength", "endurance", "focus", "willpower"],
                "duration": 999,
              "tags": {'tags':['aura']},
                "level_up_formula": "x*(1+(0.03*(level-1)))"
              }
        ]
        }
    ]
  }



### REFERENCE CLASSES ONLY.
### DO NOT COMPLETE THIS FILE.
### THESE WILL NOT RUN AND ARE NOT FINISHED.
### They are only to understand what the backend classes might look like.
class Skill:
    def __init__(self, name, description, cost=None, effects=[], milestone_upgrades=None,
                 level=1, experience=0, base_exp=100, rarity='common', target_group:TargetGroup='all',
                 owner=None, tags=None, is_passive=False):
        #constants
        self.resource_to_action = {
            "mana": "decrease_mana",
            "stamina": "decrease_stamina",
            "health": "decrease_health"
            # Add more mappings as needed
        }

        self.action_to_resource = {
            "decrease_mana": "mana",
            "decrease_stamina": "stamina",
            "decrease_health": "health"
            # Add more mappings as needed
        }
        self.name = name
        self.level = level
        self.experience = experience
        self.description = description
        self.target_group = target_group
        self.is_passive = is_passive
        self.toggled_on = True # only for passive skills, only settable via ui
        self.cost = self.load_cost(cost)
        self.effects = [SkillEffect(**effect, owner=owner, name=name, source=self) for effect in effects]
        self.milestone_upgrades = milestone_upgrades
        self.base_exp = base_exp
        self.rarity = Rarity(rarity)
        self.level_requirements = self.precalculate_level_requirements()
        self.owner = owner
        self.tags = Tags(**tags) if tags else Tags()



class Class:
    def __init__(self, name, description, skills, rarity='common', tags=None, owner=None):
        self.name = name
        self.description = description
        self.skills = [Skill(owner=owner, **skill) for skill in skills]
        self.rarity = Rarity(rarity)
        self.tags = Tags(**tags) if tags is not None else Tags()
        self.owner = owner
    
    def use_skill(self, skill_name, base_exp, enemy_level, character_level, character_stats, enemy_stats):
        for skill in self.skills:
            if skill.name == skill_name:
                skill.gain_experience(base_exp, enemy_level, character_level, character_stats, enemy_stats)
                return skill
        return None
    
    def assign_owner(self, character):
        self.owner = character
        for skill in self.skills:
            skill.assign_owner(character)
