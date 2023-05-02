from nmmo import Env, Agent
from nmmo.config.base.config import Config, PlayerGroupConfig
from nmmo.config.systems.config import Sharing
from nmmo.io import action
from .utils import build_map_generator

map = [
    [[2, 0, 0], [2, 0, 0]],
    [[2, 0, 0], [2, 0, 0]]
]


class TestPGCfg(PlayerGroupConfig):
    NENT = 1
    AGENTS = [Agent]


class TestCfg(Config, Sharing):
    MAP_PREVIEW_DOWNSCALE = 4
    test_name = 'sharing'
    MAP_GENERATOR = build_map_generator(map, test_name)
    RESOURCE_BASE_RESOURCE = 16
    PATH_MAPS = "./tmp_maps" + '/' + test_name

    TERRAIN_LOG_INTERPOLATE_MIN = 0
    TERRAIN_CENTER = 3
    MAP_HEIGHT = 2
    MAP_WIDTH = 2
    PLAYER_GROUPS = [TestPGCfg(), TestPGCfg()]


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

    assert player1.resources.water.val == w1
    assert player2.resources.water.val == w2