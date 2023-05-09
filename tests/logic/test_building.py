import nmmo
from nmmo import Env, Agent
from nmmo.config.base.config import Config, PlayerGroupConfig
from nmmo.config.systems.config import Building
from nmmo.io import action
import copy
import numpy as np
from .utils import build_map_generator

map = [
    [[2, 0, 0], [2, 0, 0]]
]


class TestPGCfg(PlayerGroupConfig):
    NENT = 1
    AGENTS = [Agent]


class TestCfg(Config, Building):
    MAP_PREVIEW_DOWNSCALE = 4
    MAP_GENERATOR = build_map_generator(map)
    RESOURCE_BASE_RESOURCE = 20
    PATH_MAPS = "./tmp_maps"

    TERRAIN_LOG_INTERPOLATE_MIN = 0
    TERRAIN_CENTER = 6
    MAP_HEIGHT = 1
    MAP_WIDTH = 2
    PLAYER_GROUPS = [TestPGCfg()]


def test_building():
    env = Env(TestCfg())
    env.reset()
    obs, _, _, _ = env.step({})

    assert len(obs) == 1

    player1 = list(env.realm.entity_group_manager.player_groups[0].entities.values())[0]

    move_action = {player1.entID: {action.Move: {
        action.Direction: (2 if player1.pos[1] == env.config.TERRAIN_BORDER else 3)
    }}}
    build_action = {player1.entID: {action.Build: {
        action.BuildDecision: True
    }}}

    env.step(move_action)
    env.step(build_action)

    last_r, last_c = player1.history.lastPos

    assert env.realm.map.tiles[last_r, last_c].mat == nmmo.lib.material.Stone

    move_action = {player1.entID: {action.Move: {
        action.Direction: (2 if player1.pos[1] == env.config.TERRAIN_BORDER else 3)
    }}}
    build_action = {player1.entID: {action.Build: {
        action.BuildDecision: True
    }}}

    env.step(move_action)

    assert player1.pos == player1.history.lastPos

    env.step(build_action)

    last_r, last_c = player1.history.lastPos

    assert env.realm.map.tiles[last_r, last_c].mat != nmmo.lib.material.Stone
