### This file is for reference only.
# It's not complete and will not run, but is useful for understanding what properties the different classes may have.
# Don't try and finish this file, it's just a reference.

class CharacterEquipment:
    DEFAULT_SLOTS = {
        'head': None,
        'chest': None,
        'legs': None,
        'hands': None,
        'feet': None,
        'main_hand': None,
        'off_hand': None,
        'two_handed': None
    }
    MAX_ACCESSORIES = 5

    def __init__(self, character):
        self.character = character
        self.equipment = {slot: None for slot in self.DEFAULT_SLOTS}
        self.equipment['accessories'] = []

    def equip(self, item: Equipment) -> bool:
        slot = item.slot

        # Check if the slot exists
        if slot not in self.equipment:
            return False

        # Check level requirement
        if self.character.level < item.level_requirement:
            return False

        # Handle two-handed weapons
        if slot == 'two_handed':
            self.unequip(self.equipment['main_hand'], 'main_hand')
            self.unequip(self.equipment['off_hand'], 'off_hand')
            self.equipment['two_handed'] = item
        elif slot == 'main_hand' or slot == 'off_hand':
            if self.equipment['two_handed']:
                return False  # Cannot equip one-handed weapons if a two-handed weapon is equipped
            self.unequip(self.equipment[slot], slot)
            self.equipment[slot] = item
        elif slot == 'accessories':
            if len(self.equipment['accessories']) >= self.MAX_ACCESSORIES:
                return False
            self.equipment['accessories'].append(item)
        else:
            self.unequip(self.equipment[slot], slot)
            self.equipment[slot] = item

        if item in self.character.inventory:
            self.character.inventory.remove(item)

        item.assign_owner(self.character)

        return True
    
    # def get_weapon_tags(self):
    #     # Handle two-handed weapons
    #     if self.equipment['two_handed']:
    #         return self.equipment['two_handed'].tags
    #     if self.equipment['main_hand']:
    #         tags = self.equipment['main_hand'].tags
    #         if self.equipment['off_hand']:
    #             tags = 
    #         return 
    #         if self.equipment['two_handed']:
    #             return False  # Cannot equip one-handed weapons if a two-handed weapon is equipped
    #         self.unequip(self.equipment[slot], slot)
    #         self.equipment[slot] = item

    def get_weapon(self):
        if self.equipment['two_handed'] is not None:
            return self.equipment['two_handed']
        if self.equipment['main_hand'] is not None:
            return self.equipment['main_hand']
        if self.equipment['off_hand'] is not None:
            if 'shield' not in self.equipment['off_hand'].tags.tags:
                return self.equipment['off_hand']
        return None

    def unequip(self, item: Optional[Equipment], slot: str) -> bool:
        if item and self.equipment[slot] == item:
            if slot == 'accessories':
                self.equipment[slot].remove(item)
            else:
                self.equipment[slot] = None
            item.remove_owner(self.character)
            self.character.add_to_inventory(item)
            return True
        return False

class Character:
    def __init__(self, name, strength, endurance, focus, willpower, agility, luck=0, charisma=0,
                stamina_recovery_rate=0.1, mana_recovery_rate=0.1, health_recovery_rate=0.05, level=1,
                default_basic_attack_type='physical', 
                default_basic_attack_dice=['1d6'], #dice are 1d6 like (1,6)
                alignment='Ally',
                rewarded_exp=None,
                tags=None,
                default_basic_attack_target='random_enemy'):
        self.name = name
        
        self.level = level

        self.default_basic_attack_type = default_basic_attack_type
        self.default_basic_attack_dice = default_basic_attack_dice
        self.default_basic_attack_target = default_basic_attack_target
        self.alignment = alignment

        self.base_stamina_recovery_rate = stamina_recovery_rate
        self.base_mana_recovery_rate = mana_recovery_rate
        self.base_health_recovery_rate = health_recovery_rate

        self.tags = Tags(**tags) if tags else Tags()

        self.stats = {
                'strength': strength,
                'endurance': endurance,
                'focus': focus,
                'willpower': willpower,
                'agility': agility,
                'luck': luck,
                'charisma': charisma,
                'stamina_recovery_rate': stamina_recovery_rate,
                'mana_recovery_rate': mana_recovery_rate,
                'health_recovery_rate': health_recovery_rate
            }
        
        self.equipment = items.CharacterEquipment(self)

        self.boostable_stats = { f'boostable_{stat}':self.stats[stat] for stat in self.stats.keys() }

        

        self.physical_barrier = 0
        self.magic_barrier = 0
        self.barrier = 0

        #flags
        self.incapacitated = False # ready or fainted
        self.fled_combat = False

        self.actions = ["fight", "flee", "use_item", "freeform action"]
        self.inventory = []
        
        self.status_effects = []
        self.banished_passive_status_effects = []
        self.character_class = None

        self.rewarded_exp = self.calculate_rewarded_exp(rewarded_exp)

        # Current pools
        self.current_health = self.max_health
        self.current_mana = self.max_mana
        self.current_stamina = self.max_stamina

    
    
    def _calc_stat_modifier(self, stat_name:str):
        max_modifier = 0
        for effect in self.status_effects:
            if isinstance(effect, StatBoostOverTime) and (stat_name == effect.stat_names or stat_name in effect.stat_names):
                modifier = effect._get_stat_modifier(self, stat_name)
                if modifier > max_modifier:
                    max_modifier = modifier
        return max_modifier
    
    # Properties for calculated max values
    @property
    def max_health(self):
        return (self.strength + self.endurance) * 5
    @property
    def max_mana(self):
        return (self.focus + self.willpower) * 5
    @property
    def max_stamina(self):
        return self.endurance * 10
    @property
    def speed(self):
        return max(self.agility, (self.strength/2)) / 2 + 5
    @property
    def physical_defense(self):
        return self.endurance * 0.1 + self.equipment.total_physical_defense
    @property
    def magic_defense(self):
        return self.willpower * 0.1 + self.equipment.total_magic_defense
    @property
    def physical_attack(self):
        return self.strength * 2 + self.equipment.total_physical_attack
    @property
    def magic_attack(self):
        return self.focus * 2 + self.equipment.total_magic_attack
    
    @property
    def basic_attack_type(self):
        return self.default_basic_attack_type
    @property
    def basic_attack_dice(self):
        return self.default_basic_attack_dice + self.equipment.get_attack_dice()
    
    @property
    def defense_dice(self):
        return self.equipment.get_defense_dice()
    
    @property
    def skills(self):
        if self.character_class is None:
            return []
        return [skill.name for skill in self.character_class.skills]
    
    def get_dodge_chance(self, opponent):
        speed_difference = self.speed - opponent.speed
        scaling_factor = 20  # Adjust to make the curve less steep
        bias = -1.75  # Adjust to shift the curve downwards
        dodge_chance = 1 / (1 + math.exp(-(speed_difference / scaling_factor + bias)))
        return min(max(dodge_chance, 0), 1)
    
    def calculate_rewarded_exp(self, rewarded_exp:int=None):
        if rewarded_exp is not None:
            return rewarded_exp
        #calculate the mean of all the stats
        stats = [self.strength, self.endurance, self.focus, self.willpower, self.agility, self.luck, 
                        self.charisma]
        total_stats = sum(stats)
        mean_stats = total_stats/len(stats)
        exp = mean_stats * 10
        level_bonus = self.level*2
        exp += level_bonus
        return exp
    
    def receive_exp(self, exp_points):
        pass

    def add_status_effect(self, effect):
        self.status_effects.append(effect)

    def apply_status_effects(self, logger):
        for effect in self.status_effects:
            effect.apply(self, logger)
        current_effects = [effect for effect in self.status_effects if effect.duration > 0]
        removed_effects = [effect.remove(self, logger) for effect in self.status_effects if effect.duration <= 0]
        
        #check if passives are blocked
        passives_are_blocked = False
        for status_effect in self.status_effects:
            if status_effect.status_effect_type == 'passive_block':
                passives_are_blocked = True
        
        # if they are, remove them to banished list
        if passives_are_blocked:
            passive_list = []
            for effect in current_effects:
                if getattr(effect.source, 'is_passive', False):
                    #RARITY CHECK ON PASSIVES
                    # TODO - don't implement yet, too complicated

                    #banish passives
                    passive_list.append(effect)
                    effect.remove(self, logger)
                    current_effects.remove(effect)
            self.banished_passive_status_effects += passive_list
        else:
            #if passives become unblocked, add back banished passives to the status effects list
            if len(self.banished_passive_status_effects) > 0:
                current_effects += self.banished_passive_status_effects
                self.banished_passive_status_effects = []


        self.status_effects = current_effects

    # def tick_effects(self, logger):
    #     for effect in self.status_effects:
    #         effect.tick()
    #         logger.info(f'{effect.status_effect_type} duration: {effect.duration}')
    #     current_effects = [effect for effect in self.status_effects if effect.duration > 0]
    #     removed_effects = [effect.remove(self, logger) for effect in self.status_effects if effect.duration <= 0]
    #     self.status_effects = current_effects

    def apply_turn_effects(self, logger):
        self.apply_status_effects(logger)
        # Handle effects that occur after the character's turn
        self.recover_stamina()
        self.recover_mana()

    def equip(self, item, slot):
        self.equipment.equip(item, slot)

    def unequip(self, item, slot):
        self.equipment.unequip(item, slot)

    def add_to_inventory(self, item):
        self.inventory.append(item)
        item.assign_owner(self)

    def remove_from_inventory(self, item):
        self.inventory.remove(item)
        item.remove_owner(self)