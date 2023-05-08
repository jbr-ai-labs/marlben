import nmmo
import numpy as np

import nmmo.lib.distance
from scripted import utils


def closestTarget(config, ob, npc_only=False):
    shortestDist = np.inf
    closestAgent = None

    Entity = nmmo.Serialized.Entity
    agent = ob.agent

    sr = nmmo.scripting.Observation.attribute(agent, Entity.R)
    sc = nmmo.scripting.Observation.attribute(agent, Entity.C)
    start = (sr, sc)

    for target in ob.agents:
        exists = nmmo.scripting.Observation.attribute(target, Entity.Self)
        if not exists:
            continue

        if npc_only and nmmo.scripting.Observation.attribute(target, Entity.ID) >= 0:
            continue

        tr = nmmo.scripting.Observation.attribute(target, Entity.R)
        tc = nmmo.scripting.Observation.attribute(target, Entity.C)

        goal = (tr, tc)
        dist = nmmo.lib.distance.l1(start, goal)

        if dist < shortestDist and dist != 0:
            shortestDist = dist
            closestAgent = target

    if closestAgent is None:
        return None, None

    return closestAgent, shortestDist


def attacker(config, ob):
    Entity = nmmo.Serialized.Entity

    sr = nmmo.scripting.Observation.attribute(ob.agent, Entity.R)
    sc = nmmo.scripting.Observation.attribute(ob.agent, Entity.C)

    attackerID = nmmo.scripting.Observation.attribute(ob.agent, Entity.AttackerID)

    if attackerID == 0:
        return None, None

    for target in ob.agents:
        identity = nmmo.scripting.Observation.attribute(target, Entity.ID)
        if identity == attackerID:
            tr = nmmo.scripting.Observation.attribute(target, Entity.R)
            tc = nmmo.scripting.Observation.attribute(target, Entity.C)
            dist = nmmo.lib.distance.l1((sr, sc), (tr, tc))
            return target, dist
    return None, None


def target(config, actions, style, targetID):
    actions[nmmo.action.Attack] = {
        nmmo.action.Style: style,
        nmmo.action.Target: targetID}
