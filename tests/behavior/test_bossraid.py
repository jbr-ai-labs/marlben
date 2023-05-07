from nmmo.envs.boss_raid import BossRaid, BossRaidConfig
from scripted.environments.bossfight import BossFightTankAgent, BossRaidFighterAgent, BossRaidHealerAgent
from scripted.baselines import Combat


class ScriptedBossRaidConfig(BossRaidConfig):
    def __init__(self, tank_agent, fighter_agent, healer_agent, n_tanks=2, n_fighters=2, n_healers=2):
        super().__init__(n_tanks, n_fighters, n_healers)
        self.PLAYER_GROUPS[0].AGENTS[0] = tank_agent
        self.PLAYER_GROUPS[1].AGENTS[0] = fighter_agent
        self.PLAYER_GROUPS[2].AGENTS[0] = healer_agent


def test_boss_fight_simple():
    env = BossRaid(ScriptedBossRaidConfig(Combat, Combat, Combat))
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
    env = BossRaid(ScriptedBossRaidConfig(BossFightTankAgent, BossRaidFighterAgent, BossRaidHealerAgent,
                                          n_tanks=1, n_fighters=1, n_healers=1))
    obs = env.reset()
    timesteps = 500
    done = False
    while not done and timesteps > 0:
        _, _, _, _ = env.step({})
        timesteps -= 1
        done = done or len(env.realm.entity_group_manager.npc_groups[0].entities) == 0
        done = done or sum(len(pg.entities) for pg in env.realm.entity_group_manager.player_groups) == 0
    assert len(env.realm.entity_group_manager.npc_groups[0].entities) == 0


def test_boss_raid_scripted():
    env = BossRaid(ScriptedBossRaidConfig(BossFightTankAgent, BossRaidFighterAgent, BossRaidHealerAgent,
                                          n_tanks=2, n_fighters=2, n_healers=2))
    obs = env.reset()
    timesteps = 500
    done = False
    while not done and timesteps > 0:
        _, _, _, _ = env.step({})
        timesteps -= 1
        done = done or len(env.realm.entity_group_manager.npc_groups[0].entities) == 0
        done = done or sum(len(pg.entities) for pg in env.realm.entity_group_manager.player_groups) == 0
    assert len(env.realm.entity_group_manager.npc_groups[0].entities) == 0


def test_boss_raid_scripted_large():
    env = BossRaid(ScriptedBossRaidConfig(BossFightTankAgent, BossRaidFighterAgent, BossRaidHealerAgent,
                                          n_tanks=4, n_fighters=4, n_healers=4))
    obs = env.reset()
    timesteps = 500
    done = False
    while not done and timesteps > 0:
        _, _, _, _ = env.step({})
        timesteps -= 1
        done = done or len(env.realm.entity_group_manager.npc_groups[0].entities) == 0
        done = done or sum(len(pg.entities) for pg in env.realm.entity_group_manager.player_groups) == 0
    assert len(env.realm.entity_group_manager.npc_groups[0].entities) == 0


def test_boss_raid_scripted_no_healers():
    env = BossRaid(ScriptedBossRaidConfig(BossFightTankAgent, BossRaidFighterAgent, BossRaidHealerAgent,
                                          n_tanks=2, n_fighters=2, n_healers=0))
    obs = env.reset()
    timesteps = 500
    done = False
    while not done and timesteps > 0:
        _, _, _, _ = env.step({})
        timesteps -= 1
        done = done or len(env.realm.entity_group_manager.npc_groups[0].entities) == 0
        done = done or sum(len(pg.entities) for pg in env.realm.entity_group_manager.player_groups) == 0
    assert len(env.realm.entity_group_manager.npc_groups[0].entities) == 0


def test_boss_raid_scripted_no_fighters():
    env = BossRaid(ScriptedBossRaidConfig(BossFightTankAgent, BossRaidFighterAgent, BossRaidHealerAgent,
                                          n_tanks=2, n_fighters=0, n_healers=2))
    obs = env.reset()
    timesteps = 500
    done = False
    while not done and timesteps > 0:
        _, _, _, _ = env.step({})
        timesteps -= 1
        done = done or len(env.realm.entity_group_manager.npc_groups[0].entities) == 0
        done = done or sum(len(pg.entities) for pg in env.realm.entity_group_manager.player_groups) == 0
    assert len(env.realm.entity_group_manager.npc_groups[0].entities) == 0


def test_boss_raid_scripted_no_tanks():
    env = BossRaid(ScriptedBossRaidConfig(BossFightTankAgent, BossRaidFighterAgent, BossRaidHealerAgent,
                                          n_tanks=0, n_fighters=2, n_healers=2))
    obs = env.reset()
    timesteps = 500
    done = False
    while not done and timesteps > 0:
        _, _, _, _ = env.step({})
        timesteps -= 1
        done = done or len(env.realm.entity_group_manager.npc_groups[0].entities) == 0
        done = done or sum(len(pg.entities) for pg in env.realm.entity_group_manager.player_groups) == 0
    assert len(env.realm.entity_group_manager.npc_groups[0].entities) == 0


def test_boss_raid_scripted_fighters_only():
    env = BossRaid(ScriptedBossRaidConfig(BossFightTankAgent, BossRaidFighterAgent, BossRaidHealerAgent,
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
    assert len(env.realm.entity_group_manager.npc_groups[0].entities) > 0


def test_boss_raid_scripted_healers_only():
    env = BossRaid(ScriptedBossRaidConfig(BossFightTankAgent, BossRaidFighterAgent, BossRaidHealerAgent,
                                          n_tanks=0, n_fighters=0, n_healers=2))
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