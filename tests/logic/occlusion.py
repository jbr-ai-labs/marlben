import os
from os import path as osp
from nmmo import MapGenerator, Terrain

import numpy as np
from matplotlib import pyplot as plt
import nmmo
from nmmo import Env, Agent
from nmmo.config.base.config import Config, PlayerGroupConfig
from nmmo.config.systems.config import Resource
from nmmo.io import action
from nmmo.lib.material import Water, Forest, BalancedWater, BalancedForest
from .utils import build_map_generator

map = [
    [[1, 0, 0], [2, 0, 0], [2, 0, 0], [1, 1, 0]],
    [[2, 0, 0], [2, 0, 0], [2, 0, 0], [2, 0, 0]],
    [[2, 0, 0], [2, 0, 0], [2, 0, 0], [2, 0, 0]],
    [[1, 1, 0], [2, 0, 0], [2, 0, 0], [4, 2, 0]]
]


class TestPGCfg(PlayerGroupConfig):
    NENT = 1
    AGENTS = [Agent]

    def __init__(self, visibility_color):
        super().__init__()
        self.VISIBLE_COLORS = [visibility_color]


class TestCfg(Config, Resource):
    MAP_PREVIEW_DOWNSCALE = 4
    MAP_GENERATOR = build_map_generator(map)
    RESOURCE_BASE_RESOURCE = 20
    PATH_MAPS = "./tmp_maps"

    TERRAIN_LOG_INTERPOLATE_MIN = 0
    TERRAIN_CENTER = 6
    NUM_VISIBILITY_COLORS = 2
    NUM_ACCESSIBILITY_COLORS = 2
    MAP_HEIGHT = 4
    MAP_WIDTH = 4
    NSTIM = 3
    PLAYER_GROUPS = [TestPGCfg(1), TestPGCfg(2)]


def test_occlusion():
    cfg = TestCfg()
    env = Env(cfg)
    env.reset()
    obs, _, _, _ = env.step({})

    assert len(obs) == 2

    player1 = list(env.realm.entity_group_manager.player_groups[0].entities.values())[0]
    player2 = list(env.realm.entity_group_manager.player_groups[1].entities.values())[0]

    assert len(player1.visible_colors) == 2 and 0 in player1.visible_colors and 1 in player1.visible_colors
    assert len(player2.visible_colors) == 2 and 0 in player2.visible_colors and 2 in player2.visible_colors

    players = [player1, player2]

    resource_tiles = [tile for row in env.realm.map.tiles for tile in row if tile.mat in (Water, BalancedWater, Forest, BalancedForest)]
    base_coord = env.config.NSTIM

    for tile in resource_tiles:
        for player in players:
            dx, dy = base_coord + tile.pos[0] - player.pos[0], base_coord + tile.pos[1] - player.pos[1]
            if not (0 <= dx < env.config.WINDOW and 0 <= dy < env.config.WINDOW):
                continue
            if tile.visibility_color in player.visible_colors:
                assert obs[player.entID]["Tile"]["Discrete"][dx * env.config.WINDOW + dy][0] in ((1, 3) if tile.mat in (Water, BalancedWater) else (4, 3))
            else:
                assert obs[player.entID]["Tile"]["Discrete"][dx * env.config.WINDOW + dy][0] == 5
