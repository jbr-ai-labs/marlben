from marlben import Env, Agent
from marlben.config.base.config import Config, PlayerGroupConfig
from marlben.config.systems.config import Sharing
from marlben.core.spawn.spawn_system.position_samplers import PositionSampler
from marlben.io import action
from .utils import build_map_generator

"""
A testcase for sharing mechanic
"""

map = [
    [[2, 0, 0], [2, 0, 0]],
    [[2, 0, 0], [2, 0, 0]]
]

class FixedPositionSampler(PositionSampler):
    def __init__(self, color):
        super().__init__()
        self._color = color

    def get_next(self):
        if self._color == 1:
            return 9, 9
        else:
            return 9, 8

class TestPGCfg(PlayerGroupConfig):
    NENT = 1
    AGENTS = [Agent]

    def __init__(self, color):
        super().__init__()
        self.SPAWN_COORDINATES_SAMPLER = FixedPositionSampler(color)

class TestCfg(Config, Sharing):
    MAP_PREVIEW_DOWNSCALE = 4
    test_name = 'sharing'
    MAP_GENERATOR = build_map_generator(map)
    RESOURCE_BASE_RESOURCE = 16
    PATH_MAPS = "./tmp_maps" + '/' + test_name

    TERRAIN_LOG_INTERPOLATE_MIN = 0
    TERRAIN_CENTER = 6
    MAP_HEIGHT = 2
    MAP_WIDTH = 2
    PLAYER_GROUPS = [TestPGCfg(1), TestPGCfg(2)]


def test_sharing_water():
    cfg = TestCfg()
    env = Env(cfg)
    env.reset(step=False)
    obs, _, _, _ = env.step({})

    assert len(obs) == 2

    player1 = list(env.realm.entity_group_manager.player_groups[0].entities.values())[0]
    player2 = list(env.realm.entity_group_manager.player_groups[1].entities.values())[0]
    w1 = cfg.RESOURCE_BASE_RESOURCE
    w2 = cfg.RESOURCE_BASE_RESOURCE

    # Check that amount of resource is decreasing
    for _ in range(5):
        obs, _, _, _ = env.step({})
        w1 -= 1
        w2 -= 1
        assert player1.resources.water.val == w1
        assert player2.resources.water.val == w2

    share_action = {player1.entID: {action.Share: {
        action.Target: 1,
        action.Resource: action.Water.index,
        action.ResourceAmount: 5
    }}}

    obs, _, _, _ = env.step(share_action)
    w1 -= 6
    w2 += 4

    # Check that resource shared successfully
    assert player1.resources.water.val == w1
    assert player2.resources.water.val == w2

    share_action = {player1.entID: {action.Share: {
        action.Target: 1,
        action.Resource: action.Water.index,
        action.ResourceAmount: -5
    }}}

    obs, _, _, _ = env.step(share_action)
    w1 -= 1
    w2 -= 1

    # Check that resource were not stolen
    assert player1.resources.water.val == w1
    assert player2.resources.water.val == w2

    share_action = {player1.entID: {action.Share: {
        action.Target: 1,
        action.Resource: action.Water.index,
        action.ResourceAmount: 100
    }}}

    obs, _, _, _ = env.step(share_action)
    w2 += (w1 - 1) - 1
    w1 = 0

    # Check that agent can't give more resources than it have
    assert player1.resources.water.val == w1
    assert player2.resources.water.val == w2