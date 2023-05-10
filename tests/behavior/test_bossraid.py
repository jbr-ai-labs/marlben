import random

import numpy as np

from marlben.envs.raid import Raid, BossRaidConfig
from scripted.environments.bossfight import BossFightTankAgent, BossRaidFighterAgent, BossRaidHealerAgent
from scripted.baselines import Combat


class ScriptedBossRaidConfig(BossRaidConfig):
    def __init__(self, tank_agent, fighter_agent, healer_agent, n_tanks=2, n_fighters=2, n_healers=2):
        super().__init__(n_tanks, n_fighters, n_healers)
        self.PLAYER_GROUPS[0].AGENTS[0] = tank_agent
        self.PLAYER_GROUPS[1].AGENTS[0] = fighter_agent
        self.PLAYER_GROUPS[2].AGENTS[0] = healer_agent


def test_boss_raid_simple():
    random.seed(0)
    np.random.seed(0)
    env = Raid(ScriptedBossRaidConfig(Combat, Combat, Combat))
    obs = env.reset()
    timesteps = 500
    done = False
    while not done and timesteps > 0:
        _, _, _, _ = env.step({})
        timesteps -= 1
        done = done or len(env.realm.entity_group_manager.npc_groups[0].entities) == 0
        done = done or sum(len(pg.entities) for pg in env.realm.entity_group_manager.player_groups) == 0
    assert len(env.realm.entity_group_manager.npc_groups[0].entities) > 0


def test_boss_raid_scripted_tiny():
    random.seed(0)
    np.random.seed(0)
    env = Raid(ScriptedBossRaidConfig(BossFightTankAgent, BossRaidFighterAgent, BossRaidHealerAgent,
                                      n_tanks=1, n_fighters=1, n_healers=1))
    env.reset()
    timesteps = 500
    done = False
    while not done and timesteps > 0:
        _, _, _, _ = env.step({})
        timesteps -= 1
        done = done or len(env.realm.entity_group_manager.npc_groups[0].entities) == 0
        done = done or sum(len(pg.entities) for pg in env.realm.entity_group_manager.player_groups) == 0
    assert timesteps > 0
    boss_fight_condition = len(env.realm.entity_group_manager.npc_groups[0].entities) == 0
    if not boss_fight_condition:
        boss = env.realm.entity_group_manager.npc_groups[0].entities[-1]
        boss_fight_condition = (boss.resources.health.val / boss.resources.health.max) < 0.25
    assert boss_fight_condition


def test_boss_raid_scripted():
    random.seed(0)
    np.random.seed(0)
    env = Raid(ScriptedBossRaidConfig(BossFightTankAgent, BossRaidFighterAgent, BossRaidHealerAgent,
                                      n_tanks=2, n_fighters=2, n_healers=2))
    obs = env.reset()
    timesteps = 500
    done = False
    while not done and timesteps > 0:
        _, _, _, _ = env.step({})
        timesteps -= 1
        done = done or len(env.realm.entity_group_manager.npc_groups[0].entities) == 0
        done = done or sum(len(pg.entities) for pg in env.realm.entity_group_manager.player_groups) == 0
    assert timesteps > 0
    boss_fight_condition = len(env.realm.entity_group_manager.npc_groups[0].entities) == 0
    if not boss_fight_condition:
        boss = env.realm.entity_group_manager.npc_groups[0].entities[-1]
        boss_fight_condition = (boss.resources.health.val / boss.resources.health.max) < 0.25
    assert boss_fight_condition


def test_boss_raid_scripted_large():
    random.seed(0)
    np.random.seed(0)
    env = Raid(ScriptedBossRaidConfig(BossFightTankAgent, BossRaidFighterAgent, BossRaidHealerAgent,
                                      n_tanks=4, n_fighters=4, n_healers=4))
    obs = env.reset()
    timesteps = 500
    done = False
    while not done and timesteps > 0:
        _, _, _, _ = env.step({})
        timesteps -= 1
        done = done or len(env.realm.entity_group_manager.npc_groups[0].entities) == 0
        done = done or sum(len(pg.entities) for pg in env.realm.entity_group_manager.player_groups) == 0
    assert timesteps > 0
    boss_fight_condition = len(env.realm.entity_group_manager.npc_groups[0].entities) == 0
    if not boss_fight_condition:
        boss = env.realm.entity_group_manager.npc_groups[0].entities[-1]
        boss_fight_condition = (boss.resources.health.val / boss.resources.health.max) < 0.25
    assert boss_fight_condition


def test_boss_raid_scripted_no_healers():
    random.seed(0)
    np.random.seed(0)
    env = Raid(ScriptedBossRaidConfig(BossFightTankAgent, BossRaidFighterAgent, BossRaidHealerAgent,
                                      n_tanks=2, n_fighters=2, n_healers=0))
    obs = env.reset()
    timesteps = 500
    done = False
    while not done and timesteps > 0:
        _, _, _, _ = env.step({})
        timesteps -= 1
        done = done or len(env.realm.entity_group_manager.npc_groups[0].entities) == 0
        done = done or sum(len(pg.entities) for pg in env.realm.entity_group_manager.player_groups) == 0
    assert timesteps > 0
    boss_fight_condition = len(env.realm.entity_group_manager.npc_groups[0].entities) == 0
    if not boss_fight_condition:
        boss = env.realm.entity_group_manager.npc_groups[0].entities[-1]
        boss_fight_condition = (boss.resources.health.val / boss.resources.health.max) < 0.30
    assert boss_fight_condition


def test_boss_raid_scripted_no_fighters():
    random.seed(0)
    np.random.seed(0)
    env = Raid(ScriptedBossRaidConfig(BossFightTankAgent, BossRaidFighterAgent, BossRaidHealerAgent,
                                      n_tanks=2, n_fighters=0, n_healers=2))
    obs = env.reset()
    timesteps = 500
    done = False
    while not done and timesteps > 0:
        _, _, _, _ = env.step({})
        timesteps -= 1
        done = done or len(env.realm.entity_group_manager.npc_groups[0].entities) == 0
        done = done or sum(len(pg.entities) for pg in env.realm.entity_group_manager.player_groups) == 0
    assert timesteps > 0
    boss_fight_condition = len(env.realm.entity_group_manager.npc_groups[0].entities) == 0
    if not boss_fight_condition:
        boss = env.realm.entity_group_manager.npc_groups[0].entities[-1]
        boss_fight_condition = (boss.resources.health.val / boss.resources.health.max) < 0.35
    assert boss_fight_condition


def test_boss_raid_scripted_no_tanks():
    random.seed(0)
    np.random.seed(0)
    env = Raid(ScriptedBossRaidConfig(BossFightTankAgent, BossRaidFighterAgent, BossRaidHealerAgent,
                                      n_tanks=0, n_fighters=2, n_healers=2))
    obs = env.reset()
    timesteps = 500
    done = False
    while not done and timesteps > 0:
        _, _, _, _ = env.step({})
        timesteps -= 1
        done = done or len(env.realm.entity_group_manager.npc_groups[0].entities) == 0
        done = done or sum(len(pg.entities) for pg in env.realm.entity_group_manager.player_groups) == 0
    assert timesteps > 0
    boss_fight_condition = len(env.realm.entity_group_manager.npc_groups[0].entities) == 0
    if not boss_fight_condition:
        boss = env.realm.entity_group_manager.npc_groups[0].entities[-1]
        boss_fight_condition = (boss.resources.health.val / boss.resources.health.max) < 0.50
    assert boss_fight_condition


def test_boss_raid_scripted_fighters_only():
    random.seed(0)
    np.random.seed(0)
    env = Raid(ScriptedBossRaidConfig(BossFightTankAgent, BossRaidFighterAgent, BossRaidHealerAgent,
                                      n_tanks=0, n_fighters=2, n_healers=0))
    obs = env.reset()
    timesteps = 500
    done = False
    while not done and timesteps > 0:
        _, _, _, _ = env.step({})
        timesteps -= 1
        done = done or len(env.realm.entity_group_manager.npc_groups[0].entities) == 0
        done = done or sum(len(pg.entities) for pg in env.realm.entity_group_manager.player_groups) == 0
    # It's expected that fighters can't survive on their own
    assert timesteps > 0
    assert len(env.realm.entity_group_manager.npc_groups[0].entities) > 0


def test_boss_raid_scripted_healers_only():
    random.seed(0)
    np.random.seed(0)
    env = Raid(ScriptedBossRaidConfig(BossFightTankAgent, BossRaidFighterAgent, BossRaidHealerAgent,
                                      n_tanks=0, n_fighters=0, n_healers=1))
    obs = env.reset()
    timesteps = 500
    done = False
    while not done and timesteps > 0:
        _, _, _, _ = env.step({})
        timesteps -= 1
        done = done or len(env.realm.entity_group_manager.npc_groups[0].entities) == 0
        done = done or sum(len(pg.entities) for pg in env.realm.entity_group_manager.player_groups) == 0
    # It's expected that healers can't survive on their own
    assert len(env.realm.entity_group_manager.npc_groups[0].entities) > 0