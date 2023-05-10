import marlben
from marlben import Env, Agent
from marlben.config.base.config import Config, PlayerGroupConfig
from marlben.config.systems.config import Building
from marlben.core.spawn.spawn_system.position_samplers import PositionSampler
from marlben.io import action
from .utils import build_map_generator

map = [
    [[2, 0, 0], [2, 0, 0]]
]

class FixedPositionSampler(PositionSampler):
    def get_next(self):
        return 8, 8

class TestPGCfg(PlayerGroupConfig):
    NENT = 1
    AGENTS = [Agent]
    SPAWN_COORDINATES_SAMPLER = FixedPositionSampler()


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
        action.Direction: (action.East.index if player1.pos[0] == env.config.TERRAIN_BORDER else action.West.index)
    }}}
    build_action = {player1.entID: {action.Build: {
        action.BuildDecision: True
    }}}

    env.step(move_action)
    env.step(build_action)


    last_r, last_c = player1.history.lastPos
    check = env.realm.map.tiles[env.config.TERRAIN_BORDER, env.config.TERRAIN_BORDER].impassible
    check = check or env.realm.map.tiles[env.config.TERRAIN_BORDER, env.config.TERRAIN_BORDER + 1].impassible
    check2 = env.realm.map.tiles[env.config.TERRAIN_BORDER, env.config.TERRAIN_BORDER].impassible
    check2 = check2 and env.realm.map.tiles[env.config.TERRAIN_BORDER, env.config.TERRAIN_BORDER + 1].impassible

    assert env.realm.map.tiles[last_r, last_c].mat == marlben.lib.material.Stone

    move_action = {player1.entID: {action.Move: {
        action.Direction: (action.East.index if player1.pos[0] == env.config.TERRAIN_BORDER else action.West.index)
    }}}
    build_action = {player1.entID: {action.Build: {
        action.BuildDecision: True
    }}}

    env.step(move_action)

    assert player1.pos == player1.history.lastPos

    env.step(build_action)

    last_r, last_c = player1.history.lastPos
    check = env.realm.map.tiles[env.config.TERRAIN_BORDER, env.config.TERRAIN_BORDER].impassible
    check = check or env.realm.map.tiles[env.config.TERRAIN_BORDER, env.config.TERRAIN_BORDER + 1].impassible
    check2 = env.realm.map.tiles[env.config.TERRAIN_BORDER, env.config.TERRAIN_BORDER].impassible
    check2 = check2 and env.realm.map.tiles[env.config.TERRAIN_BORDER, env.config.TERRAIN_BORDER + 1].impassible

    assert env.realm.map.tiles[last_r, last_c].mat != marlben.lib.material.Stone
