import marlben
import numpy as np

import marlben.lib.distance
from scripted import utils


def closestTarget(config, ob, npc_only=False):
    shortestDist = np.inf
    closestAgent = None

    Entity = marlben.Serialized.Entity
    agent = ob.agent

    sr = marlben.scripting.Observation.attribute(agent, Entity.R)
    sc = marlben.scripting.Observation.attribute(agent, Entity.C)
    start = (sr, sc)

    for target in ob.agents:
        exists = marlben.scripting.Observation.attribute(target, Entity.Self)
        if not exists:
            continue

        if npc_only and marlben.scripting.Observation.attribute(target, Entity.ID) >= 0:
            continue

        tr = marlben.scripting.Observation.attribute(target, Entity.R)
        tc = marlben.scripting.Observation.attribute(target, Entity.C)

        goal = (tr, tc)
        dist = marlben.lib.distance.l1(start, goal)

        if dist < shortestDist and dist != 0:
            shortestDist = dist
            closestAgent = target

    if closestAgent is None:
        return None, None

    return closestAgent, shortestDist


def attacker(config, ob):
    Entity = marlben.Serialized.Entity

    sr = marlben.scripting.Observation.attribute(ob.agent, Entity.R)
    sc = marlben.scripting.Observation.attribute(ob.agent, Entity.C)

    attackerID = marlben.scripting.Observation.attribute(ob.agent, Entity.AttackerID)

    if attackerID == 0:
        return None, None

    for target in ob.agents:
        identity = marlben.scripting.Observation.attribute(target, Entity.ID)
        if identity == attackerID:
            tr = marlben.scripting.Observation.attribute(target, Entity.R)
            tc = marlben.scripting.Observation.attribute(target, Entity.C)
            dist = marlben.lib.distance.l1((sr, sc), (tr, tc))
            return target, dist
    return None, None


def target(config, actions, style, targetID):
    actions[marlben.action.Attack] = {
        marlben.action.Style: style,
        marlben.action.Target: targetID}
