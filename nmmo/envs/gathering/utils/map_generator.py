from nmmo import MapGenerator, Terrain
from nmmo.core.map_generation.rock_patterns import generate_huge_rocks
from nmmo.core.map_generation.resources import generate_resources
from nmmo.core.map_generation.checks import check_connectivity
import numpy as np


class GatheringMapGenerator(MapGenerator):
    def __init__(self, config):
        super().__init__(config)
        self._seed = 0

    def generate_map(self, idx):
        seed = (271 * self._seed + idx * 193) % 479001599  # Using prime numbers to avoid seed repetition
        map = self._generate_with_seed(seed)
        st_pts = np.argwhere(map[:, :, 0] == Terrain.GRASS)
        np.random.shuffle(st_pts)
        while not check_connectivity(map, st_pts[:3], "STRONG"):
            seed += 117
            map = self._generate_with_seed(seed)
            st_pts = np.argwhere(map[:, :, 0] == Terrain.GRASS)
            np.random.shuffle(st_pts)


        val = np.zeros((map.shape[0], map.shape[1]))
        val[map[:, :, 0] == Terrain.STONE] = np.random.rand() * (1 - self.config.TERRAIN_FOREST) + self.config.TERRAIN_FOREST
        val[map[:, :, 0] == Terrain.FOREST] = np.random.rand() * (self.config.TERRAIN_FOREST - self.config.TERRAIN_GRASS) + self.config.TERRAIN_GRASS
        val[map[:, :, 0] == Terrain.GRASS] = np.random.rand() * (self.config.TERRAIN_GRASS - self.config.TERRAIN_WATER) + self.config.TERRAIN_WATER
        val[map[:, :, 0] == Terrain.WATER] = np.random.rand() * (self.config.TERRAIN_WATER - self.config.TERRAIN_LAVA) + self.config.TERRAIN_LAVA
        val[map[:, :, 0] == Terrain.LAVA] = self.config.TERRAIN_LAVA

        return val, map

    def seed(self, seed):
        self._seed = seed

    def _generate_with_seed(self, seed):
        config = self.config
        rnd = np.random.RandomState(seed)
        border = config.TERRAIN_BORDER
        width = config.MAP_WIDTH
        height = config.MAP_HEIGHT
        water_count = config.NENT
        food_count = 2*config.NENT
        rock_start_probability = 0.1  # config.ROCK_FREQ
        rock_growth_probability = 0.1  # config.ROCK_GROWTH
        privacy_colors_num = config.NUM_VISIBILITY_COLORS
        access_colors_num = config.NUM_ACCESSIBILITY_COLORS

        assert config.MAP_HEIGHT * config.MAP_WIDTH >= 6 * config.NENT

        tiles = np.zeros((height + 2*border, width + 2*border, 3), dtype=int)
        tiles[:, :, 0] = Terrain.LAVA
        map = tiles[border:height+border, border:width+border]
        map[:, :, 0] = Terrain.GRASS
        rocks = generate_huge_rocks(height, width, rock_start_probability, rock_growth_probability,
                                    max(1, (width + height) // 8), rnd)
        map[:, :, 0][rocks] = Terrain.STONE
        generate_resources(map, Terrain.WATER, water_count, privacy_colors_num, access_colors_num, "EQUAL", "EQUAL", rnd)
        generate_resources(map, Terrain.FOREST, food_count, privacy_colors_num, access_colors_num, "EQUAL", "EQUAL", rnd)

        return tiles