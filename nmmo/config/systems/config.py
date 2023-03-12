class Resource:
    '''Resource Game System'''

    @property  # Reserved flag
    def Resource(self):
        return True

    RESOURCE_BASE_RESOURCE = 10
    '''Initial level and capacity for Hunting + Fishing resource skills'''

    RESOURCE_FOREST_CAPACITY = 1
    '''Maximum number of harvests before a forest tile decays'''

    RESOURCE_FOREST_RESPAWN = 0.025
    '''Probability that a harvested forest tile will regenerate each tick'''

    RESOURCE_HARVEST_RESTORE_FRACTION = 1.0
    '''Fraction of maximum capacity restored upon collecting a resource'''

    RESOURCE_HEALTH_REGEN_THRESHOLD = 0.5
    '''Fraction of maximum resource capacity required to regen health'''

    RESOURCE_HEALTH_RESTORE_FRACTION = 0.1
    '''Fraction of health restored per tick when above half food+water'''

    REGEN_HEALTH = 1.
    RESOURCE_COOLDOWN = 1


class Combat:
    '''Combat Game System'''

    @property  # Reserved flag
    def Combat(self):
        return True

    COMBAT_DICE_SIDES = 20
    '''Number of sides for combat dice

   Attacks can only hit opponents up to the attacker's level plus
   DICE_SIDES/2. Increasing this value makes attacks more accurate
   and allows lower level attackers to hit stronger opponents'''

    COMBAT_DEFENSE_WEIGHT = 0.3
    '''Fraction of defense that comes from the Defense skill'''

    COMBAT_MELEE_REACH = 1
    '''Reach of attacks using the Melee skill'''

    COMBAT_RANGE_REACH = 3
    '''Reach of attacks using the Range skill'''

    COMBAT_MAGE_REACH = 4
    '''Reach of attacks using the Mage skill'''

    COMBAT_HEAL_REACH = 2
    '''Reach of healing skill'''

    COMBAT_FREEZE_TIME = 3
    '''Number of ticks successful Mage attacks freeze a target'''
    
    STEALING_ENABLED = True
    '''Is attack allows to steal resources'''


class Progression:
    '''Progression Game System'''

    @property  # Reserved flag
    def Progression(self):
        return True

    PROGRESSION_BASE_RESOURCE = 10
    '''Initial level and capacity for Hunting + Fishing resource skills'''

    PROGRESSION_BASE_XP_SCALE = 10
    '''Skill level progression speed as a multiplier of typical MMOs'''

    PROGRESSION_CONSTITUTION_XP_SCALE = 2
    '''Multiplier on top of XP_SCALE for the Constitution skill'''

    PROGRESSION_COMBAT_XP_SCALE = 4
    '''Multiplier on top of XP_SCALE for Combat skills'''


class NPC(Combat):
    '''NPC & Equipment Game System'''

    @property  # Reserved flag
    def NPC(self):
        return True

    NPC_SPAWN_ATTEMPTS = 25
    '''Number of NPC spawn attempts per tick'''

    NPC_SPAWN_AGGRESSIVE = 0.80
    '''Percentage distance threshold from spawn for aggressive NPCs'''

    NPC_SPAWN_NEUTRAL = 0.50
    '''Percentage distance threshold from spawn for neutral NPCs'''

    NPC_SPAWN_PASSIVE = 0.00
    '''Percentage distance threshold from spawn for passive NPCs'''

    NPC_LEVEL_MIN = 1
    '''Minimum NPC level'''

    NPC_LEVEL_MAX = None
    '''Maximum NPC level'''

    NPC_LEVEL_SPREAD = None
    '''Level range for NPC spawns'''


class Sharing(Resource):
    @property
    def Sharing(self):
        return True

    SHARING_DISTANCE = 3
    SHARE_MIN = 10
    SHARE_MAX = 10


class Building:
    @property
    def Building(self):
        return True

class Planting:
    @property
    def Planting(self):
        return True