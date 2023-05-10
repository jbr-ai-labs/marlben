from marlben import Task
from marlben.config import Combat
from marlben.envs.gathering.config import BaseGatheringConfig


class EnemyAgentKilledTask:
    def __call__(self, realm, entity):
        if entity.dead:
            return 0

        # Amount of Players died at this turn
        return sum(
            [len(group.dead) for group in realm.entity_group_manager.player_groups if group.group_id != entity.population]
        )
class TeamDeathmatchConfig(BaseGatheringConfig, Combat):
    TASKS = [Task(EnemyAgentKilledTask(), 1, 10.)]