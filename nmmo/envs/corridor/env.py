import nmmo
from os import path as osp


class Corridor(nmmo.Env):
    def __init__(self, config):
        config.PATH_MAPS = osp.join(osp.abspath(osp.dirname(__file__)), "../../../nmmo/envs/corridor/maps")
        super().__init__(config)
