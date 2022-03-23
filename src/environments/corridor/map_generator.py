from nmmo.core.terrain import MapGenerator
import numpy as np
from tqdm import tqdm
import os
from os import path as osp


FIRST_MAP = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 5, 5, 5, 5, 5, 0, 0],
                      [0, 0, 1, 2, 2, 2, 4, 0, 0],
                      [0, 0, 1, 2, 2, 2, 4, 0, 0],
                      [0, 0, 1, 2, 2, 2, 4, 0, 0],
                      [0, 0, 5, 5, 5, 5, 5, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0]])


MAPS = [FIRST_MAP]


class CorridorMapGenerator(MapGenerator):
    def __init__(self, config):
        super().__init__(config)
    
    def generate_all_maps(self):
        for idx in tqdm(range(self.config.NMAPS)):
            path = osp.join(self.config.PATH_MAPS, 'map{}'.format(idx+1), 'map.npy')
            np.save(path, MAPS[idx])
