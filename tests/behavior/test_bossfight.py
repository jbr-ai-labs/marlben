import random

from marlben.envs.boss_fight import BossFight, BossFightConfig
from scripted.environments.bossfight import BossFightTankAgent
from scripted.baselines import Combat
import numpy as np


class ScriptedBossFightConfig(BossFightConfig):
    def __init__(self, agent_class):
        super().__init__()
        self.PLAYER_GROUPS[0].AGENTS[0] = agent_class


def test_boss_fight_simple():
    random.seed(0)
    np.random.seed(0)
    env = BossFight(ScriptedBossFightConfig(Combat))
    _ = env.reset()
    timesteps = 300
    done = False
    while not done and timesteps > 0:
        _, _, _, _ = env.step({})
        timesteps -= 1
        done = done or len(env.realm.entity_group_manager.npc_groups[0].entities) == 0
        done = done or sum(len(pg.entities) for pg in env.realm.entity_group_manager.player_groups) == 0
    assert len(env.realm.entity_group_manager.npc_groups[0].entities) > 0


def test_boss_fight_scripted():
    random.seed(0)
    np.random.seed(0)
    env = BossFight(ScriptedBossFightConfig(BossFightTankAgent))
    _ = env.reset()
    timesteps = 300
    done = False
    while not done and timesteps > 0:
        obs, _, _, _ = env.step({})
        timesteps -= 1
        done = done or len(env.realm.entity_group_manager.npc_groups[0].entities) == 0
        done = done or sum(len(pg.entities) for pg in env.realm.entity_group_manager.player_groups) == 0
    assert timesteps > 0
    boss_fight_condition = len(env.realm.entity_group_manager.npc_groups[0].entities) == 0
    if not boss_fight_condition:
        boss = env.realm.entity_group_manager.npc_groups[0].entities[-1]
        boss_fight_condition = (boss.resources.health.val / boss.resources.health.max) < 0.35
    assert boss_fight_condition
