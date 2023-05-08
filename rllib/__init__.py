import ray

from nmmo.config import Planting
from nmmo.envs import Corridor, BossFight, GatheringBuilding, GatheringExclusive, GatheringObscuredAndExclusive, \
    GatheringObscured
from nmmo.envs.arena.env import Arena
from nmmo.envs.deathmatch.env import Deathmatch
from nmmo.envs.gathering.env import Gathering
from nmmo.envs.predator_prey import PredatorPrey
from nmmo.envs.pve.env import Pve
from nmmo.envs.raid.env import Raid
from nmmo.envs.siege.env import Siege
from nmmo.envs.team_deathmatch.env import TeamDeathmatch
from .rllib_wrapper import RLlibEnv
from .neural import rllib_policy

env_factory = {
    'Corridor': Corridor,
    'Gathering': Gathering,
    'Arena': Arena,
    'Pve': Pve,
    'Deathmatch': Deathmatch,
    'TeamDeathmatch': TeamDeathmatch,
    'BossFight': BossFight,
    'Building': GatheringBuilding,
    'Colors': GatheringExclusive,
    'Exploring': GatheringObscuredAndExclusive,
    'Spying': GatheringObscured,
    'Raid': Raid,
    'Siege': Siege,
    'Planting': Planting,
    'PredatorPrey': PredatorPrey
}


for key in env_factory.keys():
    class CustomEnv(env_factory[key], RLlibEnv):
        pass
    ray.tune.registry.register_env(key, lambda config: CustomEnv(config))

ray.tune.registry.register_env('base', lambda config: RLlibEnv(config))
