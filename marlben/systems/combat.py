# Various utilities for managing combat, including hit/damage

import numpy as np

from marlben.systems import skill as Skill


def level(skills):
    hp = skills.constitution.level
    defense = skills.defense.level
    melee = skills.melee.level
    ranged = skills.range.level
    mage = skills.mage.level

    base = 0.25*(defense + hp)
    final = np.floor(base + 0.5*max(melee, ranged, mage))
    return final


def attack(entity, targ, skillFn, stealing_enabled=True):
    config = entity.config
    entitySkill = skillFn(entity)
    targetSkill = skillFn(targ)

    targetDefense = targ.skills.defense.level + targ.loadout.defense

    dmg = damage(entitySkill.__class__, entitySkill.level)
    if dmg > 0:
        die = config.COMBAT_DICE_SIDES
        roll = np.random.randint(1, die+1)
        dc = accuracy(config, entitySkill.level, targetSkill.level, targetDefense)
        crit = roll == die

        if not crit and roll < dc:
            dmg = 1

    # Note: damage can be negative!
    dmg = min(dmg, entity.resources.health.val)
    entity.applyDamage(
        dmg, entitySkill.__class__.__name__.lower(), stealing_enabled)
    targ.receiveDamage(entity, dmg, stealing_enabled)
    return dmg

# Compute maximum damage roll


def damage(skill, level):
    if skill == Skill.Melee:
        return np.floor(7 + level * 63 / 99)
    if skill == Skill.Range:
        return np.floor(3 + level * 32 / 99)
    if skill == Skill.Mage:
        return np.floor(1 + level * 24 / 99)
    if skill == Skill.Heal:
        return -np.floor(3 + level * 32 / 99)

# Compute maximum attack or defense roll (same formula)
# Max attack 198 - min def 1 = 197. Max 198 - max 198 = 0
# REMOVE FACTOR OF 2 FROM ATTACK AFTER IMPLEMENTING WEAPONS


def accuracy(config, entAtk, targAtk, targDef):
    alpha = config.COMBAT_DEFENSE_WEIGHT

    attack = entAtk
    defense = alpha*targDef + (1-alpha)*targAtk
    dc = defense - attack + config.COMBAT_DICE_SIDES//2

    return dc


def danger(config, pos):
    border = config.TERRAIN_BORDER
    center = config.TERRAIN_CENTER
    r, c = pos

    # Distance from border
    rDist = min(r - border, center + border - r - 1)
    cDist = min(c - border, center + border - c - 1)
    dist = min(rDist, cDist)
    norm = 2 * dist / center

    return norm
