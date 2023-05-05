from nmmo import Env, Agent, Serialized
from nmmo.config.base.config import Config, PlayerGroupConfig
from nmmo.config.systems.config import Resource
from nmmo.core.spawn.spawn_system.position_samplers import PositionSampler
from nmmo.io import action
from nmmo.io.action import North, South
from nmmo.scripting import Observation
from .utils import build_map_generator

map = [
    [[4, 0, 1], [5, 0, 0], [5, 0, 0], [1, 0, 2]],
    [[2, 0, 0], [4, 0, 3], [4, 0, 0], [2, 0, 0]],
    [[1, 0, 2], [5, 0, 0], [5, 0, 0], [4, 0, 1]]
]


class FixedPositionSampler(PositionSampler):
    def __init__(self, color):
        super().__init__()
        self._color = color

    def get_next(self):
        if self._color == 1:
            return 9, 8
        else:
            return 9, 11


class TestPGCfg(PlayerGroupConfig):
    NENT = 1
    AGENTS = [Agent]

    def __init__(self, color):
        super().__init__()
        self.ACCESSIBLE_COLORS = [color]
        self.SPAWN_COORDINATES_SAMPLER = FixedPositionSampler(color)


class TestCfg(Config, Resource):
    MAP_PREVIEW_DOWNSCALE = 4
    test_name = 'exclusive'
    MAP_GENERATOR = build_map_generator(map, test_name)
    RESOURCE_BASE_RESOURCE = 20
    PATH_MAPS = "./tmp_maps" + '/' + test_name

    TERRAIN_LOG_INTERPOLATE_MIN = 0
    TERRAIN_CENTER = 5
    NUM_VISIBILITY_COLORS = 2
    NUM_ACCESSIBILITY_COLORS = 2
    MAP_HEIGHT = 3
    MAP_WIDTH = 4
    NSTIM = 3
    PLAYER_GROUPS = [TestPGCfg(1), TestPGCfg(2)]


def test_exclusive():
    cfg = TestCfg()
    env = Env(cfg)
    env.reset()
    for _ in range(2):
        obs, _, _, _ = env.step({})
        assert len(obs) == 2

    player1 = list(env.realm.entity_group_manager.player_groups[0].entities.values())[0]
    player2 = list(env.realm.entity_group_manager.player_groups[1].entities.values())[0]

    assert len(player1.accessible_colors) == 2 and 0 in player1.accessible_colors and 1 in player1.accessible_colors
    assert len(player2.accessible_colors) == 2 and 0 in player2.accessible_colors and 2 in player2.accessible_colors

    blocked_directions = [North, South]

    for direction in blocked_directions:
        move_action = {
            player1.entID: {
                action.Move: {
                    action.Direction: direction.index,
                }
            },
            player2.entID: {
                action.Move: {
                    action.Direction: direction.index,
                }
            }
        }
        new_obs, _, _, _ = env.step(move_action)
        for entId, new_obs in new_obs.items():
            new_obs_unwrapped = Observation(cfg, new_obs)
            new_r = new_obs_unwrapped.attribute(new_obs_unwrapped.agent, Serialized.Entity.R)
            new_c = new_obs_unwrapped.attribute(new_obs_unwrapped.agent, Serialized.Entity.C)
            old_obs_unwrapped = Observation(cfg, obs[entId])
            old_r = old_obs_unwrapped.attribute(old_obs_unwrapped.agent, Serialized.Entity.R)
            old_c = old_obs_unwrapped.attribute(old_obs_unwrapped.agent, Serialized.Entity.C)
            assert new_r == old_r and new_c == old_c
