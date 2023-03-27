import numpy as np
from nmmo import Terrain


def generate_resources(tile_map, resource_type, resource_amount, visibility_colors, accessibility_colors,
                       visibility_distribution, accessibility_distribution, random: np.random.RandomState = None):
    visibility_colors_counts = np.zeros(visibility_colors) if visibility_colors > 0 else None
    accessibility_colors_counts = np.zeros(accessibility_colors) if accessibility_colors > 0 else None
    height = tile_map.shape[0]
    width = tile_map.shape[1]

    for i in range(resource_amount):
        attempts = 0
        x, y = random.randint(0, height-1), random.randint(0, width-1)
        while tile_map[x, y, 0] != Terrain.GRASS and attempts < 20:
            x, y = random.randint(0, height-1), random.randint(0, width-1)
            attempts += 1
        assert attempts < 20
        tile_map[x, y, 0] = resource_type
        if visibility_colors > 0:
            tile_map[x, y, 1] = _get_random_color(visibility_colors_counts, visibility_distribution, random)
        if accessibility_colors > 0:
            tile_map[x, y, 2] = _get_random_color(accessibility_colors_counts, accessibility_distribution, random)


def _get_random_color(colors_counts, distribution, random: np.random.RandomState):
    if distribution == "UNIFORM":
        c = random.randint(1, len(colors_counts)+1)
    elif distribution == "EQUAL":
        args = np.argwhere(np.array(colors_counts) == np.min(colors_counts))
        c = args[np.random.randint(0, len(args))] + 1
    elif distribution == "FAIR":
        logits = np.max(colors_counts) - colors_counts + 1
        logits = logits / np.sum(logits)
        c = np.argmax(random.multinomial(1, logits)) + 1

    colors_counts[c-1] += 1
    return c