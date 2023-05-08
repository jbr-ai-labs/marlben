import numpy as np

import nmmo
from nmmo import scripting
from nmmo.io.action import *
from nmmo.lib import colors
from scripted import move, attack
from scripted.baselines import Scripted


class BossFightTankAgent(Scripted):
    '''Simple Tank agent. Looks for a boss, then fights it until the end.'''
    name = 'TankAgent_'
    color = colors.Neon.GOLD

    def __call__(self, obs):
        super().__call__(obs)

        Entity = nmmo.Serialized.Entity

        self.scan_agents(True)
        if self.closestID is not None:
            self.style = Melee
            self.target = self.closest
            self.targetID = self.closestID
            self.targetDist = self.closestDist
            if self.closestDist > self.config.COMBAT_MELEE_REACH:
                move.pathfind(self.config, self.ob, self.actions,
                              nmmo.scripting.Observation.attribute(self.closest, Entity.R) - self.currR,
                              nmmo.scripting.Observation.attribute(self.closest, Entity.C) - self.currC)
            self.attack()
        else:
            self.explore()

        return self.actions


class BossRaidFighterAgent(Scripted):
    '''Simple Fighter agent. Looks for a boss, then fights it. Evades enemy if were attacked.'''
    name = 'FighterAgent_'
    color = colors.Neon.BLOOD
    is_evading = False

    def evade(self):
        move.evade(self.config, self.ob, self.actions, self.closest)

    def __call__(self, obs):
        super().__call__(obs)

        self.scan_agents(True)
        Entity = nmmo.Serialized.Entity

        if self.closestID is not None:
            if self.closestDist <= self.config.COMBAT_MELEE_REACH:
                self.style = nmmo.action.Melee
            else:
                self.style = nmmo.action.Range
            self.target = self.closest
            self.targetID = self.closestID
            self.targetDist = self.closestDist
            self.attack()

            if self.attacker is None and not self.is_evading:
                if self.closestDist > self.config.COMBAT_MELEE_REACH:
                    move.pathfind(self.config, self.ob, self.actions,
                                  nmmo.scripting.Observation.attribute(self.closest, Entity.R) - self.currR,
                                  nmmo.scripting.Observation.attribute(self.closest, Entity.C) - self.currC)
            else:
                self.evade()
                # Evade until out of melee attack range
                if self.is_evading and self.closestDist > self.config.COMBAT_MELEE_REACH + 1:
                    self.is_evading = False
                else:
                    self.is_evading = True
        else:
            self.is_evading = False
            self.explore()

        return self.actions


class BossRaidHealerAgent(Scripted):
    '''Simple Healer agent. Follows an ally with the lowest HP remaining and heals it. Tries to evade enemy's attacks.'''
    name = 'HealerAgent_'
    color = colors.Neon.GREEN
    is_evading = False

    def evade(self):
        move.evade(self.config, self.ob, self.actions, self.closest)

    def __call__(self, obs):
        super().__call__(obs)

        self.scan_agents(True)
        self.allies = []
        Entity = nmmo.Serialized.Entity
        for target in self.ob.agents:
            exists = nmmo.scripting.Observation.attribute(target, Entity.Self)
            if not exists:
                continue
            if not nmmo.scripting.Observation.attribute(target, Entity.ID) >= 0:
                continue
            self.allies.append(target)

        self.style = nmmo.action.Heal

        self.lowestHealthID = None
        self.lowestHealth = None
        self.lowestHealthTarget = None
        for target in self.allies:
            target_pop = nmmo.scripting.Observation.attribute(target, Entity.Population)
            curr_pop = nmmo.scripting.Observation.attribute(self.ob.agent, Entity.Population)
            if target_pop == curr_pop:
                continue  # Do not follow and heal other healers

            # TODO: is there a way to get max entity health? It seems like its better to heal one with the lowest health percentage
            current_health = nmmo.scripting.Observation.attribute(target, Entity.Health)
            if self.lowestHealthID is None or current_health < self.lowestHealth:
                self.lowestHealthID = nmmo.scripting.Observation.attribute(target, Entity.ID)
                self.lowestHealth = current_health
                self.lowestHealthTarget = target

        self.actions = {}
        if self.lowestHealthID is not None:
            self.actions[Attack] = {Style: self.style, Target: self.lowestHealthID}
            if self.attacker is not None or (self.is_evading and self.closest is not None):
                self.evade()
                if self.is_evading and self.closestDist > self.config.COMBAT_MELEE_REACH + 1:
                    self.is_evading = False
                else:
                    self.is_evading = True
            else:
                move.pathfind(self.config, self.ob, self.actions,
                              nmmo.scripting.Observation.attribute(self.lowestHealthTarget, Entity.R) - self.currR,
                              nmmo.scripting.Observation.attribute(self.lowestHealthTarget, Entity.C) - self.currC)
        else:
            self.explore()

        return self.actions
