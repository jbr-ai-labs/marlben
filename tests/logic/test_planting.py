from distutils.command.config import config
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
    PLANTING_COST = 0.1


def test_plant_and_wait():
    env = Env(TestCfg())
    env.reset()
    obs, _, _, _ = env.step({})

    assert len(obs) == 1

    player1 = list(env.realm.entity_group_manager.player_groups[0].entities.values())[0]

    move_action = {player1.entID: {action.Move: {
        action.Direction: (2 if player1.pos[1] == env.config.TERRAIN_BORDER else 3)
    }}}
    plant_action = {player1.entID: {action.Plant: {
        action.PlantDecision: True
    }}}

    env.step(move_action)
    food_before = player1.resources.food.val
    env.step(plant_action)
    food_after = player1.resources.food.val

    last_r, last_c = player1.history.lastPos

    assert env.realm.map.tiles[last_r, last_c].state == nmmo.lib.material.ScrubImpassible
    assert env.realm.map.tiles[last_r, last_c].mat == nmmo.lib.material.BalancedForest
    assert abs(food_before - food_after - TestCfg.PLANTING_COST) < 1e-8

    for _ in range(TestCfg.RESOURCE_COOLDOWN):
        env.step({})

    assert env.realm.map.tiles[last_r, last_c].state == nmmo.lib.material.BalancedForest


def test_plant_two_times():
    env = Env(TestCfg())
    env.reset()
    obs, _, _, _ = env.step({})

    assert len(obs) == 1

    player1 = list(env.realm.entity_group_manager.player_groups[0].entities.values())[0]

    move_action = {player1.entID: {action.Move: {
        action.Direction: (2 if player1.pos[1] == env.config.TERRAIN_BORDER else 3)
    }}}
    plant_action = {player1.entID: {action.Plant: {
        action.PlantDecision: True
    }}}

    env.step(move_action)
    env.step(plant_action)

    last_r, last_c = player1.history.lastPos

    assert env.realm.map.tiles[last_r, last_c].state == nmmo.lib.material.ScrubImpassible
    assert env.realm.map.tiles[last_r, last_c].mat == nmmo.lib.material.BalancedForest

    move_action = {player1.entID: {action.Move: {
        action.Direction: (2 if player1.pos[1] == env.config.TERRAIN_BORDER else 3)
    }}}
    plant_action = {player1.entID: {action.Plant: {
        action.PlantDecision: True
    }}}

    env.step(move_action)

    assert player1.pos == player1.history.lastPos

    env.step(plant_action)

    last_r, last_c = player1.history.lastPos

    assert env.realm.map.tiles[last_r, last_c].mat != nmmo.lib.material.BalancedForest


def test_plant_expensive():
    class ExpensivePlantCfg(TestCfg):
        PLANTING_COST = 10000 
    env = Env(ExpensivePlantCfg())
    env.reset()
    obs, _, _, _ = env.step({})

    assert len(obs) == 1

    player1 = list(env.realm.entity_group_manager.player_groups[0].entities.values())[0]

    move_action = {player1.entID: {action.Move: {
        action.Direction: (2 if player1.pos[1] == env.config.TERRAIN_BORDER else 3)
    }}}
    plant_action = {player1.entID: {action.Plant: {
        action.PlantDecision: True
    }}}

    env.step(move_action)
    food_before = player1.resources.food.val
    env.step(plant_action)
    food_after = player1.resources.food.val

    last_r, last_c = player1.history.lastPos

    assert env.realm.map.tiles[last_r, last_c].mat != nmmo.lib.material.BalancedForest
    assert abs(food_before - food_after) < 1e-8
