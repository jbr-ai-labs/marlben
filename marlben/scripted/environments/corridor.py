import marlben
from marlben.scripted import move
from marlben.scripted.baselines  import Scripted


class CorridorAgent(Scripted):
    name = 'CorridorAgent_'
    '''Walks along the corridor and shares resources with another agent'''

    def __init__(self, config, idx):
        super().__init__(config, idx)
        self._current_target = "resource"
        self._resource_amount = 7
        if (self.iden + 1) % 2 == 0:
            self._direction = (0, -1)
            self._resource_pos = (10, 10) # (18, 13)
            self._mid_pos = (10, 13)
            self._resource_to_share = marlben.action.Water
        else:
            self._direction = (0, 1)
            self._resource_pos = (10, 17)
            self._mid_pos = (10, 14)
            self._resource_to_share = marlben.action.Food

    def _switch_direction(self, direction):
        return tuple([-1 * d for d in direction])

    def _manage_direction(self, r, c):
        if self._current_target == "resource" and (r, c) == self._resource_pos:
            self._direction = self._switch_direction(self._direction)
            self._current_target = "mid"
        elif self._current_target == "mid" and (r, c) == self._mid_pos:
            self._direction = self._switch_direction(self._direction)
            self._current_target = "resource"

    def _share(self):
        self.scan_agents()
        targetID = self.closestID
        if targetID is None:
            return None
        else:
            return {
                marlben.action.Resource: self._resource_to_share,
                marlben.action.Target: targetID,
                marlben.action.ResourceAmount: self._resource_amount
            }

    def __call__(self, obs):
        super().__call__(obs)

        agent = self.ob.agent
        Entity = marlben.Serialized.Entity
        Tile = marlben.Serialized.Tile

        r = marlben.scripting.Observation.attribute(agent, Entity.R)
        c = marlben.scripting.Observation.attribute(agent, Entity.C)
        self._manage_direction(r, c)
        direction = move.towards(self._direction)
        self.actions[marlben.action.Move] = {marlben.action.Direction: direction}
        if (r, c) == self._mid_pos:
            share_action = self._share()
            if share_action is not None:
                self.actions[marlben.action.Share] = share_action

        return self.actions
