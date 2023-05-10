import ray

from marlben.config import Planting
from marlben.envs import Corridor, BossFight, GatheringBuilding, GatheringExclusive, GatheringObscuredAndExclusive, \
    GatheringObscured
from marlben.envs.arena.env import Arena
from marlben.envs.deathmatch.env import Deathmatch
from marlben.envs.gathering.env import Gathering
from marlben.envs.predator_prey import PredatorPrey
from marlben.envs.pve.env import Pve
from marlben.envs.raid import Raid
from marlben.envs.siege.env import Siege
from marlben.envs.team_deathmatch.env import TeamDeathmatch
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
