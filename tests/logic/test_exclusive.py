from nmmo import Env, Agent
from nmmo.config.base.config import Config, PlayerGroupConfig
from nmmo.config.systems.config import Resource
from nmmo.lib.material import Water, Forest, BalancedWater, BalancedForest
from .utils import build_map_generator


map = [
    [[4, 0, 1], [5, 0, 0], [5, 0, 0], [1, 0, 2]],
    [[2, 0, 0], [4, 0, 3], [4, 0, 0], [2, 0, 0]],
    [[1, 0, 2], [5, 0, 0], [5, 0, 0], [4, 0, 1]]
]


class TestPGCfg(PlayerGroupConfig):
    NENT = 1
    AGENTS = [Agent]

    def __init__(self, color):
        super().__init__()
        self.ACCESSIBLE_COLORS = [color]


class TestCfg(Config, Resource):
    MAP_PREVIEW_DOWNSCALE = 4
    MAP_GENERATOR = build_map_generator(map)
    RESOURCE_BASE_RESOURCE = 20
    PATH_MAPS = "./tmp_maps"

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

    assert len(player1.visible_colors) == 2 and 0 in player1.visible_colors and 1 in player1.visible_colors
    assert len(player2.visible_colors) == 2 and 0 in player2.visible_colors and 2 in player2.visible_colors

    players = [player1, player2]

    resource_tiles = [tile for row in env.realm.map.tiles for tile in row if tile.mat in (Water, BalancedWater, Forest, BalancedForest)]

    for tile in resource_tiles:
        for player in players:
            if abs(tile.r - player.r) + abs(tile.c - player.c) < 2:
                if tile._accessibility_color in player.accessible_colors:
                    assert tile.capacity == 0
                else:
                    assert tile.capacity == 1