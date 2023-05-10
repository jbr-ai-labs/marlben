from marlben import Task, Agent
from marlben.config import Combat
from marlben.config.base.config import PlayerGroupConfig
from marlben.envs.gathering.config import BaseGatheringConfig
from marlben.io.action import Range, Mage, Melee


class PreyKilledTask:
    __name__ = 'hunt'
    def __call__(self, realm, entity):
        if not entity.alive or realm.entity_group_manager.player_groups[entity.population].banned_attack_styles is not None:
            return 0

        # Amount of Prey died at this turn
        return sum(
            [len(group.dead) for group in realm.entity_group_manager.player_groups if group.group_id != entity.population]
        )

class PreyGroupConfig(PlayerGroupConfig):
    def __init__(self, agents, n_ent):
        super().__init__()
        self.NENT = n_ent
        self.AGENTS = agents

    BASE_HEALTH = 5
    BANNED_ATTACK_STYLES = [Range, Mage, Melee]


class PredatorGroupConfig(PlayerGroupConfig):
    def __init__(self, agents, n_ent):
        super().__init__()
        self.NENT = n_ent
        self.AGENTS = agents

    BASE_HEALTH = 10

class PredatorPreyConfig(BaseGatheringConfig, Combat):
    TASKS = [Task(PreyKilledTask(), 1, 10.)]
    PLAYER_GROUPS = [PreyGroupConfig([Agent], 10), PredatorGroupConfig([Agent], 3)]