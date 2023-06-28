from marlben import Agent
from marlben.core.spawn.spawn_system.position_samplers import UniformPositionSampler
from marlben.core.spawn.spawn_system.skill_samplers import CustomSkillSampler
from marlben.config.base.config import Config, PlayerGroupConfig, NPCGroupConfig
from marlben.config.systems.config import Combat, NPC, Progression
from marlben.io.action import Heal, Mage, Range
from marlben.core.map_generation.base import MapGenerator
from marlben.systems.achievement import Task
from marlben.core.env import Env

from typing import Callable

"""
An example of designing your own environment. Here you can find following code:
1. Creating Task conditions for giving a sparse reward to an agent 
2. Creating Player and NPC group configs
3. Creating Environment config from scratch
4. Creating an environment

Sometimes you would like to evaluate performance on some not-common-purpose tasks, that is not included in this library.
To do so, you would need to design your own environment using our library.

As an example, if you want to test an ability of your agents to maintain specific formation while moving to designated point,
you may do so by defining your own environment with reward function that penalize agents for breaking the formation while
rewards them for getting closer to the target.
"""


class NpcKilledTask(Callable):
    __name__ = "Kill NPC"

    def __init__(self, npc_group_id=0):
        self.frag_counter = 0
        self.npc_group_id = npc_group_id

    def __call__(self, realm, entity):
        # Amount of NPCs died at this turn
        for ent in realm.entity_group_manager.npc_groups[self.npc_group_id].dead:
            if ent.attacker is not None and ent.attacker.entID == entity.entID:
                self.frag_counter += 1
        return self.frag_counter


class PlayerDiedTask(Callable):
    __name__ = "Die"

    def __call__(self, realm, entity):
        return 0 if entity.alive else 1


class CustomPlayerGroupConfig(PlayerGroupConfig):
    # Make sure to add at least one agent to this list.
    # `marlben.Agent` corresponds to a trainable agent
    AGENTS = [Agent]
    NENT = 8


class CustomNPCGroupConfig(NPCGroupConfig):
    DANGER = 1.0  # Make all NPC aggressive
    NENT = 128
    BANNED_ATTACK_STYLES = {Heal, Range, Mage}  # NPC can only use melee attacks

    # Add spawn coordinates sampler.
    # Creating uniform sampler without parameters makes NPCs appear at all playable map uniformly
    SPAWN_COORDINATES_SAMPLER = UniformPositionSampler()

    # Create a skill level sampler.
    # Here levels of constitution and melee attack will be randomly sampled from list for each NPC
    SPAWN_SKILLS_SAMPLER = CustomSkillSampler(
        {"constitution": {"name": "choice", "level": [5 * i + 1 for i in range(16)]},
         "melee": {"name": "choice", "level": [2 * i + 1 for i in range(16)]}})


# Note: by default most of the systems are disabled. Include them in superclass list to enable them.
class CustomEnvConfig(Config, Combat, NPC, Progression):

    # System settings
    # Disable health regeneration and make damage reduction depend on defense stat only
    REGEN_HEALTH = 0.
    COMBAT_DEFENSE_WEIGHT = 1.

    # Setting base reward for completing achievements
    # Agent will receive reward for killing up to 16 monsters
    TASKS = [Task(NpcKilledTask, i+1, 5) for i in range(16)] + [Task(PlayerDiedTask, 1, -100)]

    # Map sizes
    MAP_HEIGHT = 64
    MAP_WIDTH = 64
    TERRAIN_CENTER = 64

    # Where to save generated maps
    PATH_MAPS = f'maps/example_maps'

    # Set the default NMMO map generator
    MAP_GENERATOR = MapGenerator


class CustomEnv(Env):
    def __init__(self):
        # Creating a new env with specified config
        super().__init__(CustomEnvConfig())

    def step(self, actions):
        # Here you can compute custom reward for an agent or change an observation
        # For sparse rewards you can use task system (see example above)
        # However, it might be useful to have more control over reward function and termination conditions
        return super().step(actions)

    def reset(self, idx=None, step=True):
        # Here you can make something after or before resetting an environment
        return super().reset(idx, step)


if __name__ == "__main__":
    env = CustomEnv()
