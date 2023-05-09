from nmmo import MapGenerator
import numpy as np
import os
from os import path as osp


def build_map_generator(map):
    class SingleMapGenerator(MapGenerator):
        _map = map

        def __init__(self, config):
            super().__init__(config)

        def generate_all_maps(self):
            height = self.config.MAP_HEIGHT
            width = self.config.MAP_WIDTH
            map_width = width + self.config.TERRAIN_BORDER * 2
            map_height = height + self.config.TERRAIN_BORDER * 2
            top, left = self.config.TERRAIN_BORDER, self.config.TERRAIN_BORDER

            map_template = np.zeros(shape=(map_height, map_width, 3), dtype=np.int32)
            tiles = np.array(self._map, dtype=np.int32)
            map_template[top:top+height, left:left+width] = tiles

            # make rock border so the agent doesn't leave the main map
            os.makedirs(self.config.PATH_MAPS, exist_ok=True)
            map_template[[top-2, top+height+1], left-2:left+width+2, 0] = 5
            map_template[top-2:top+height+2, [left-1, left+width], 0] = 5
            path = osp.join(self.config.PATH_MAPS, 'map1')
            os.makedirs(path, exist_ok=True)
            path = osp.join(path, "map.npy")
            np.save(path, map_template)

    return SingleMapGenerator