import nmmo
from nmmo import scripting
from nmmo.lib import colors
from nmmo.core.agent import Agent

from scripted import move, attack


class Scripted(Agent):
    '''Template class for scripted models.
    You may either subclass directly or mirror the __call__ function'''
    scripted = True
    color = colors.Neon.SKY

    def __init__(self, config, idx):
        '''
        Args:
           config : A forge.blade.core.Config object or subclass object
        '''
        super().__init__(config, idx)
        self.food_max = 0
        self.water_max = 0

        self.spawnR = None
        self.spawnC = None

    @property
    def forage_criterion(self) -> bool:
        '''Return true if low on food or water'''
        min_level = 7
        return self.food <= min_level or self.water <= min_level

    def forage(self):
        '''Min/max food and water using Dijkstra's algorithm'''
        move.forageDijkstra(self.config, self.ob, self.actions,
                            self.food_max, self.water_max)

    def explore(self):
        '''Route away from spawn'''
        move.explore(self.config, self.ob, self.actions,
                     self.spawnR, self.spawnC)

    @property
    def downtime(self):
        '''Return true if agent is not occupied with a high-priority action'''
        return not self.forage_criterion and self.attacker is None

    def evade(self):
        '''Target and path away from an attacker'''
        move.evade(self.config, self.ob, self.actions, self.attacker)
        self.target = self.attacker
        self.targetID = self.attackerID
        self.targetDist = self.attackerDist

    def attack(self):
        '''Attack the current target'''
        if self.target is not None:
            assert self.targetID is not None
            attack.target(self.config, self.actions, self.style, self.targetID)

    def select_combat_style(self):
        '''Select a combat style based on distance from the current target'''
        if self.target is None:
            return

        if self.targetDist <= self.config.COMBAT_MELEE_REACH:
            self.style = nmmo.action.Melee
        elif self.targetDist <= self.config.COMBAT_RANGE_REACH:
            self.style = nmmo.action.Range
        else:
            self.style = nmmo.action.Mage

    def target_weak(self):
        '''Target the nearest agent if it is weak'''
        if self.closest is None:
            return False

        selfLevel = scripting.Observation.attribute(
            self.ob.agent, nmmo.Serialized.Entity.Level)
        targLevel = scripting.Observation.attribute(
            self.closest, nmmo.Serialized.Entity.Level)

        if targLevel <= selfLevel <= 5 or selfLevel >= targLevel + 3:
            self.target = self.closest
            self.targetID = self.closestID
            self.targetDist = self.closestDist

    def scan_agents(self):
        '''Scan the nearby area for agents'''
        self.closest, self.closestDist = attack.closestTarget(
            self.config, self.ob)
        self.attacker, self.attackerDist = attack.attacker(
            self.config, self.ob)

        self.closestID = None
        if self.closest is not None:
            self.closestID = scripting.Observation.attribute(
                self.closest, nmmo.Serialized.Entity.ID)

        self.attackerID = None
        if self.attacker is not None:
            self.attackerID = scripting.Observation.attribute(
                self.attacker, nmmo.Serialized.Entity.ID)

        self.style = None
        self.target = None
        self.targetID = None
        self.targetDist = None

    def adaptive_control_and_targeting(self, explore=True):
        '''Balanced foraging, evasion, and exploration'''
        self.scan_agents()

        if self.attacker is not None:
            self.evade()
            return

        if self.forage_criterion or not explore:
            self.forage()
        else:
            self.explore()

        self.target_weak()

    def __call__(self, obs):
        '''Process observations and return actions
        Args:
           obs: An observation object from the environment. Unpack with scripting.Observation
        '''
        self.actions = {}

        self.ob = scripting.Observation(self.config, obs)
        agent = self.ob.agent

        self.food = scripting.Observation.attribute(
            agent, nmmo.Serialized.Entity.Food)
        self.water = scripting.Observation.attribute(
            agent, nmmo.Serialized.Entity.Water)

        if self.food > self.food_max:
            self.food_max = self.food
        if self.water > self.water_max:
            self.water_max = self.water

        if self.spawnR is None:
            self.spawnR = scripting.Observation.attribute(
                agent, nmmo.Serialized.Entity.R)
        if self.spawnC is None:
            self.spawnC = scripting.Observation.attribute(
                agent, nmmo.Serialized.Entity.C)


class Random(Scripted):
    name = 'Random_'
    '''Moves randomly'''

    def __call__(self, obs):
        super().__call__(obs)

        move.random(self.config, self.ob, self.actions)
        return self.actions


class CorridorAgent(Scripted):
    name = 'CorridorAgent_'
    '''Walks along the corridor and shares resources with another agent'''

    def __init__(self, config, idx):
        super().__init__(config, idx)
        self._current_target = "resource"
        self._resource_amount = 7
        if (self.iden + 1) % 2 == 0:
            self._direction = (0, -1)
            self._resource_pos = (18, 13)
            self._mid_pos = (18, 16)
            self._resource_to_share = nmmo.action.Water
        else:
            self._direction = (0, 1)
            self._resource_pos = (18, 20)
            self._mid_pos = (18, 17)
            self._resource_to_share = nmmo.action.Food

    def _switch_direction(self, direction):
        return tuple([-1 * d for d in direction])

    def _manage_direction(self, r, c):
        if self._current_target == "resource" and (r, c) == self._resource_pos:
            self._direction = self._switch_direction(self._direction)
            self._current_target = "mid"
        elif self._current_target == "mid" and (r, c) == self._mid_pos:
            self._direction = self._switch_direction(self._direction)
            self._current_target = "resource"

    def _share(self):
        self.scan_agents()
        targetID = self.closestID
        if targetID is None:
            return None
        else:
            return {
                nmmo.action.Resource: self._resource_to_share,
                nmmo.action.Target: targetID,
                nmmo.action.ResourceAmount: self._resource_amount
            }

    def __call__(self, obs):
        super().__call__(obs)

        agent = self.ob.agent
        Entity = nmmo.Serialized.Entity
        Tile = nmmo.Serialized.Tile

        r = nmmo.scripting.Observation.attribute(agent, Entity.R)
        c = nmmo.scripting.Observation.attribute(agent, Entity.C)
        self._manage_direction(r, c)
        direction = move.towards(self._direction)
        self.actions[nmmo.action.Move] = {nmmo.action.Direction: direction}
        if (r, c) == self._mid_pos:
            share_action = self._share()
            if share_action is not None:
                self.actions[nmmo.action.Share] = share_action

        return self.actions


class Meander(Scripted):
    name = 'Meander_'
    '''Moves randomly on safe terrain'''

    def __call__(self, obs):
        super().__call__(obs)

        move.meander(self.config, self.ob, self.actions)
        return self.actions


class ForageNoExplore(Scripted):
    '''Forages using Dijkstra's algorithm'''
    name = 'ForageNE_'

    def __call__(self, obs):
        super().__call__(obs)

        self.forage()

        return self.actions


class Forage(Scripted):
    '''Forages using Dijkstra's algorithm and actively explores'''
    name = 'Forage_'

    def __call__(self, obs):
        super().__call__(obs)

        if self.forage_criterion:
            self.forage()
        else:
            self.explore()

        return self.actions


class CombatNoExplore(Scripted):
    '''Forages using Dijkstra's algorithm and fights nearby agents'''
    name = 'CombatNE_'

    def __call__(self, obs):
        super().__call__(obs)

        self.adaptive_control_and_targeting(explore=False)

        self.style = nmmo.action.Range
        self.attack()

        return self.actions


class Combat(Scripted):
    '''Forages, fights, and explores'''
    name = 'Combat_'

    def __call__(self, obs):
        super().__call__(obs)

        self.adaptive_control_and_targeting()

        self.style = nmmo.action.Range
        self.attack()

        return self.actions


class CombatTribrid(Scripted):
    name = 'CombatTri_'
    '''Forages, fights, and explores.
    Uses a slightly more sophisticated attack routine'''

    def __call__(self, obs):
        super().__call__(obs)

        self.adaptive_control_and_targeting()

        self.select_combat_style()
        self.attack()

        return self.actions
