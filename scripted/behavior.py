import marlben
import numpy as np
from marlben import scripting
from marlben.systems.ai import move, attack, utils


def update(entity):
    '''Update validity of tracked entities'''
    if not utils.validTarget(entity, entity.attacker, entity.vision):
        entity.attacker = None
    if not utils.validTarget(entity, entity.target, entity.vision):
        entity.target = None
    if not utils.validTarget(entity, entity.closest, entity.vision):
        entity.closest = None

    if entity.__class__.__name__ != 'Player':
        return

    if not utils.validResource(entity, entity.food, entity.vision):
        entity.food = None
    if not utils.validResource(entity, entity.water, entity.vision):
        entity.water = None


def pathfind(config, ob, actions, rr, cc):
    actions[marlben.action.Move] = {marlben.action.Direction: move.pathfind(config, ob, actions, rr, cc)}


def explore(config, ob, actions, spawnR, spawnC):
    vision = config.NSTIM
    sz = config.TERRAIN_SIZE
    Entity = marlben.Serialized.Entity
    Tile = marlben.Serialized.Tile

    agent = ob.agent
    r = scripting.Observation.attribute(agent, Entity.R)
    c = scripting.Observation.attribute(agent, Entity.C)

    centR, centC = sz // 2, sz // 2

    vR, vC = centR - spawnR, centC - spawnC

    mmag = max(abs(vR), abs(vC))
    rr = int(np.round(vision * vR / mmag))
    cc = int(np.round(vision * vC / mmag))

    pathfind(config, ob, actions, rr, cc)


def meander(realm, actions, entity):
    actions[marlben.action.Move] = {marlben.action.Direction: move.habitable(realm.map.tiles, entity)}


def evade(realm, actions, entity):
    actions[marlben.action.Move] = {marlben.action.Direction: move.antipathfind(realm.map.tiles, entity, entity.attacker)}


def hunt(realm, actions, entity):
    # Move args
    distance = utils.distance(entity, entity.target)

    direction = None
    if distance == 0:
        direction = move.random()
    elif distance > 1:
        direction = move.pathfind(realm.map.tiles, entity, entity.target)

    if direction is not None:
        actions[marlben.action.Move] = {marlben.action.Direction: direction}

    attack(realm, actions, entity)


def attack(realm, actions, entity):
    distance = utils.distance(entity, entity.target)
    if distance > entity.skills.style.attackRange(realm.config):
        return

    actions[marlben.action.Attack] = {marlben.action.Style: entity.skills.style,
                                      marlben.action.Target: entity.target}


def forageDP(realm, actions, entity):
    direction = utils.forageDP(realm.map.tiles, entity)
    actions[marlben.action.Move] = {marlben.action.Direction: move.towards(direction)}


# def forageDijkstra(realm, actions, entity):
def forageDijkstra(config, ob, actions, food_max, water_max):
    direction = utils.forageDijkstra(config, ob, food_max, water_max)
    actions[marlben.action.Move] = {marlben.action.Direction: move.towards(direction)}
