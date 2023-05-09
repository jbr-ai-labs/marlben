import nmmo
from nmmo import Env, Agent
from nmmo.config.base.config import Config, PlayerGroupConfig
from nmmo.config.systems.config import Planting
from nmmo.io import action
import copy
from .utils import build_map_generator

map = [
    [[2, 0, 0], [2, 0, 0]]
]


class TestPGCfg(PlayerGroupConfig):
    NENT = 1
    AGENTS = [Agent]


class TestCfg(Config, Planting):
    MAP_PREVIEW_DOWNSCALE = 4
    MAP_GENERATOR = build_map_generator(map)
    RESOURCE_BASE_RESOURCE = 20
    PATH_MAPS = "./tmp_maps"
    RESOURCE_COOLDOWN = 2

    TERRAIN_LOG_INTERPOLATE_MIN = 0
    TERRAIN_CENTER = 6
    MAP_HEIGHT = 1
    MAP_WIDTH = 2
    PLAYER_GROUPS = [TestPGCfg()]


def test_planting():
    env = Env(TestCfg())
    env.reset()
    obs, _, _, _ = env.step({})

    assert len(obs) == 1

    player1 = list(env.realm.entity_group_manager.player_groups[0].entities.values())[0]

    move_action = {player1.entID: {action.Move: {
        action.Direction: (action.East if player1.pos[0] == env.config.TERRAIN_BORDER else action.West)
    }}}
    plant_action = {player1.entID: {action.Plant: {
        action.PlantDecision: True
    }}}

    env.step(move_action)
    env.step(plant_action)

    r, c = player1.history.lastPos
    assert env.realm.map.tiles[r, c].state == nmmo.lib.material.ScrubImpassible

    for i in range(TestCfg.RESOURCE_COOLDOWN):
        env.step({})
    assert env.realm.map.tiles[r, c].state == nmmo.lib.material.BalancedForest


    # move_action = {player1.entID: {action.Move: {
    #     action.Direction: (action.East if player1.pos[0] == env.config.TERRAIN_BORDER else action.West)
    # }}}
    # build_action = {player1.entID: {action.Build: {
    #     action.BuildDecision: True
    # }}}

    # env.step(build_action)
    # env.step(move_action)
    # env.step(build_action)

    # check = env.realm.map.tiles[env.config.TERRAIN_BORDER, env.config.TERRAIN_BORDER].impassible()
    # check = check or env.realm.map.tiles[env.config.TERRAIN_BORDER+1, env.config.TERRAIN_BORDER].impassible()
    # check2 = env.realm.map.tiles[env.config.TERRAIN_BORDER, env.config.TERRAIN_BORDER].impassible()
    # check2 = check2 and env.realm.map.tiles[env.config.TERRAIN_BORDER+1, env.config.TERRAIN_BORDER].impassible()

    # assert check and not check2