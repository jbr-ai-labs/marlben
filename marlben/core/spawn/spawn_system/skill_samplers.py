import numpy as np
import abc
from .base_samplers import UniformSampler, RangeSampler, ListSampler, ConstantSampler, ChoiceSampler
from marlben.systems.skill import SkillsBalanced
from marlben.systems import combat
import random


class SkillsSampler:
    def __init__(self):
        self.config = None

    @abc.abstractmethod
    def get_next(self, pos):
        pass

    def reset(self, config):
        self.config = config


class DefaultSkillSampler(SkillsSampler):
    def get_next(self, pos):
        return SkillsBalanced(self.config)


class CustomSkillSampler(SkillsSampler):
    def __init__(self, skill2config: dict):
        super().__init__()
        self.skill2sampler = dict(
            [(k, self._sampler_by_config(skill2config[k])) for k in skill2config])

    def _sampler_by_config(self, skill_sampler_config):
        if skill_sampler_config["name"] == "const":
            return ConstantSampler(skill_sampler_config["level"])
        elif skill_sampler_config["name"] == "choice":
            return ChoiceSampler(skill_sampler_config["level"])
        elif skill_sampler_config["name"] == "list":
            return ListSampler(skill_sampler_config["level"])

    def get_next(self, pos):
        skills = SkillsBalanced(self.config)
        for k in self.skill2sampler:
            skills.__getattribute__(k).setExpByLevel(
                self.skill2sampler[k].get_next())
        return skills

    def reset(self, config):
        super().reset(config)
        for s in self.skill2sampler.values():
            s.reset()


class DefaultNPCSkillSampler(SkillsSampler):
    def __init__(self, level_min, level_max, level_spread):
        super().__init__()
        self.level_min = level_min
        self.level_max = level_max
        self.level_spread = level_spread

    def get_next(self, pos):
        danger = combat.danger(self.config, pos)

        lmin = self.level_min
        lmax = self.level_max

        lbase = danger*(lmax-lmin) + lmin
        lspread = self.level_spread

        lvlMin = int(max(lmin, lbase - lspread))
        lvlMax = int(min(lmax, lbase + lspread))

        lvls = [random.randint(lvlMin, lvlMax) for _ in range(5)]

        skills = SkillsBalanced(self.config)
        constitution, defense, melee, ranged, mage = lvls

        skills.constitution.setExpByLevel(constitution)
        skills.defense.setExpByLevel(defense)
        skills.melee.setExpByLevel(melee)
        skills.range.setExpByLevel(ranged)
        skills.mage.setExpByLevel(mage)

        return skills
