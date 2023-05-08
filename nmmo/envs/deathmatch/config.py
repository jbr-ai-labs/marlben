from nmmo import Task
from nmmo.config import Combat
from nmmo.envs.gathering.config import BaseGatheringConfig


class AgentKilledTask:
    def __call__(self, realm, entity):
        if entity.dead:
            return 0

        # Amount of Players died at this turn
        return sum([len(group.dead) for group in realm.entity_group_manager.player_groups])
class DeathmatchConfig(BaseGatheringConfig, Combat):
    TASKS = [Task(AgentKilledTask(), 1, 10.)]