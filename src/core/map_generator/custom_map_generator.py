import json
from nmmo.core.terrain import MapGenerator, Save
import numpy as np
from tqdm import tqdm
import os
from os import path as osp
import matplotlib.pyplot as plt

FIRST_MAP = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 5, 5, 5, 5, 5, 0, 0],
                      [0, 0, 7, 2, 2, 2, 8, 0, 0],
                      [0, 0, 7, 2, 2, 2, 8, 0, 0],
                      [0, 0, 7, 2, 2, 2, 8, 0, 0],
                      [0, 0, 5, 5, 5, 5, 5, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0]])


MAPS = [FIRST_MAP]


class CustomMapGenerator(MapGenerator):
    def __init__(self, config):
        super().__init__(config)
    
    def generate_all_maps(self):
        path_to_maps = osp.join(self.config.PATH_MAPS, 'maps.json')
        with open(path_to_maps, 'rb') as f:
            maps = json.load(f)
        height = self.config.MAP_HEIGHT
        width = self.config.MAP_WIDTH
        top, left = self.config.TOP_LEFT_CORNER
        for idx in tqdm(range(self.config.NMAPS)):
            side = self.config.TERRAIN_CENTER + self.config.TERRAIN_BORDER * 2
            map_template = np.zeros(shape=(side, side), dtype=np.int32)
            tiles = np.array(maps[str(idx)], dtype=np.int32)
            map_template[top:top+height, left:left+width] = tiles
            # make rock border so the agent doesn't leave the main map
            map_template[[top-2, top+height+1], left-2:left+width+2] = 5 
            map_template[top-2:top+height+2, [left-2, left+width+1]] = 5
            path = osp.join(self.config.PATH_MAPS, 'map{}'.format(idx+1), 'map.npy')
            np.save(path, map_template)
