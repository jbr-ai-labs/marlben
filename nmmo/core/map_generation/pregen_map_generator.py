import json
import os
from os import path as osp

import numpy as np
from tqdm import tqdm

from nmmo import MapGenerator


class PregeneratedMapGenerator(MapGenerator):
    def __init__(self, config):
        super().__init__(config)

    def generate_all_maps(self):
        path_to_maps = osp.join(self.config.PATH_MAPS, 'maps.json')
        with open(path_to_maps, 'rb') as f:
            maps = json.load(f)
        height = self.config.MAP_HEIGHT
        width = self.config.MAP_WIDTH
        map_width = width + self.config.TERRAIN_BORDER * 2
        map_height = height + self.config.TERRAIN_BORDER * 2
        top, left = self.config.TERRAIN_BORDER, self.config.TERRAIN_BORDER
        for idx in tqdm(range(self.config.NMAPS)):
            map_template = np.zeros(shape=(map_height, map_width, 3), dtype=np.int32)
            tiles = np.array(maps[str(idx)], dtype=np.int32)
            map_template[top:top+height, left:left+width] = tiles
            # make rock border so the agent doesn't leave the main map
            map_template[[top-2, top+height+1], left-2:left+width+2, 0] = 5
            map_template[top-2:top+height+2, [left-2, left+width+1], 0] = 5
            path = osp.join(self.config.PATH_MAPS, 'map{}'.format(idx+1))
            os.makedirs(path, exist_ok=True)
            path = osp.join(path, "map.npy")
            np.save(path, map_template)
