from marlben import Env, Agent
from marlben.config.base.config import Config, PlayerGroupConfig
from marlben.config.systems.config import Combat
from marlben.io import action
import copy
from .utils import build_map_generator

"""
A testcase for healing logic
"""


# Configuring a toy env

map = [
    [[2, 0, 0], [2, 0, 0]]
]


class TestPGCfg(PlayerGroupConfig):
    NENT = 1
    AGENTS = [Agent]


class TestCfg(Config, Combat):
    MAP_PREVIEW_DOWNSCALE = 4
    MAP_GENERATOR = build_map_generator(map)
    RESOURCE_BASE_RESOURCE = 20
    PATH_MAPS = "./tmp_maps"

    TERRAIN_LOG_INTERPOLATE_MIN = 0
    TERRAIN_CENTER = 6
    MAP_HEIGHT = 1
    MAP_WIDTH = 2
    PLAYER_GROUPS = [TestPGCfg(), TestPGCfg()]


def test_healing():
    # Creating toy env
    env = Env(TestCfg())
    env.reset()
    obs, _, _, _ = env.step({})

    assert len(obs) == 2

    player1 = list(env.realm.entity_group_manager.player_groups[0].entities.values())[0]
    player2 = list(env.realm.entity_group_manager.player_groups[1].entities.values())[0]
    h2 = copy.deepcopy(player2.resources.health.val)

    # Making attack and heal actions
    attack_action = {player1.entID: {action.Attack: {
        action.Target: 1,
        action.Style: action.Melee.index
    }}}

    heal_action = {player1.entID: {action.Attack: {
        action.Target: 1,
        action.Style: action.Heal.index
    }}}

    # Check that after attack health of other agent is dropped
    env.step(attack_action)
    assert player2.resources.health.val < h2

    # Check that after healing health of other agent is restored
    for _ in range(4):
        env.step(heal_action)
    assert player2.resources.health.val == h2