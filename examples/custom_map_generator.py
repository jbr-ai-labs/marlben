from marlben.envs.raid.config import BossRaidConfig
from marlben.envs.raid.env import Raid
from marlben.core.map_generation.base import MapGenerator, Terrain
from marlben.core.map_generation.rock_patterns import generate_labyrinth

import numpy as np

"""
This example shows how to add a custom map generation to your environment.
Below you can find two simple examples.
First one shows how to create a custom map generator using predefined utils for map generation.
Second one shows how to create a custom map generator without using additional utils.
"""


class CustomMapGenerator1(MapGenerator):
    def generate_map(self, idx):
        config = self.config
        # Creating instance of np.random with specific seed
        # Using prime numbers to avoid seed repetition
        seed = (271 + idx * 193) % 479001599
        rnd = np.random.RandomState(seed)

        # Getting map parameters
        border = config.TERRAIN_BORDER
        width = config.MAP_WIDTH
        height = config.MAP_HEIGHT

        # Creating empty tiles. Should be (height + 2 * border) X (width + 2 * border) X 3
        tiles = np.zeros((height + 2 * border, width + 2 * border, 3), dtype=int)
        tiles[:, :, 0] = Terrain.LAVA  # Filling everything with lava by default

        # Getting playable part of the map
        map = tiles[border:height + border, border:width + border]

        # Making all tiles of playable map passable
        map[:, :, 0] = Terrain.GRASS

        # Creating mask of labyrinth walls and adding stones to the map according to it
        rocks = generate_labyrinth(height, width, 2, 16, rnd)
        map[:, :, 0][rocks] = Terrain.STONE

        # Create a heights map for better rendering. Can be zeroes as well.
        val = np.zeros((tiles.shape[0], tiles.shape[1]))
        val[tiles[:, :, 0] == Terrain.STONE] = np.random.rand(
        ) * (1 - self.config.TERRAIN_FOREST) + self.config.TERRAIN_FOREST
        val[tiles[:, :, 0] == Terrain.FOREST] = np.random.rand(
        ) * (self.config.TERRAIN_FOREST - self.config.TERRAIN_GRASS) + self.config.TERRAIN_GRASS
        val[tiles[:, :, 0] == Terrain.GRASS] = np.random.rand(
        ) * (self.config.TERRAIN_GRASS - self.config.TERRAIN_WATER) + self.config.TERRAIN_WATER
        val[tiles[:, :, 0] == Terrain.WATER] = np.random.rand(
        ) * (self.config.TERRAIN_WATER - self.config.TERRAIN_LAVA) + self.config.TERRAIN_LAVA
        val[tiles[:, :, 0] == Terrain.LAVA] = self.config.TERRAIN_LAVA
        return val, tiles


class CustomMapGenerator2(MapGenerator):
    def generate_map(self, idx):
        config = self.config
        # Creating instance of np.random with specific seed
        # Using prime numbers to avoid seed repetition
        seed = (271 + idx * 193) % 479001599
        rnd = np.random.RandomState(seed)

        # Getting map parameters
        border = config.TERRAIN_BORDER
        width = config.MAP_WIDTH
        height = config.MAP_HEIGHT

        # Creating empty tiles. Should be (height + 2 * border) X (width + 2 * border) X 3
        tiles = np.zeros((height + 2 * border, width + 2 * border, 3), dtype=int)
        tiles[:, :, 0] = Terrain.LAVA  # Filling everything with lava by default

        # Getting playable part of the map
        map = tiles[border:height + border, border:width + border]

        # Making all tiles of playable map passable
        map[:, :, 0] = Terrain.GRASS

        # Adding random rocks on the playable part of the map
        for _ in range(np.random.randint((height * width) // 10, (height * width) // 4)):
            x, y = np.random.randint(0, height), np.random.randint(0, width)
            map[x, y, 0] = Terrain.STONE

        # Create a heights map. To improve rendering, it's better to not leave empty (see example above).
        val = np.zeros((tiles.shape[0], tiles.shape[1]))

        return val, tiles


if __name__ == "__main__":
    config = BossRaidConfig()
    config.MAP_WIDTH = 20
    config.MAP_HEIGHT = 20
    config.TERRAIN_CENTER = 20
    config.MAP_GENERATOR = CustomMapGenerator1
    # Create an environment
    env = Raid(config)

    config2 = BossRaidConfig()
    config2.MAP_WIDTH = 20
    config2.MAP_HEIGHT = 20
    config2.TERRAIN_CENTER = 20
    config2.MAP_GENERATOR = CustomMapGenerator2
    # Create an environment
    env = Raid(config2)