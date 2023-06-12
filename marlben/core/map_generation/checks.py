import random

import numpy as np
from marlben import Terrain
from marlben.lib import material


def _walk_and_paint(important_cells, mask, reached_cells):
    new_passed_cells = np.logical_and(reached_cells, mask)
    new_reached_cells = reached_cells
    while new_reached_cells.sum() > 0:

        new_reached_cells = np.logical_or(
            np.logical_or(np.roll(new_passed_cells, 1, 0),
                          np.roll(new_passed_cells, -1, 0)),
            np.logical_or(np.roll(new_passed_cells, 1, 1),
                          np.roll(new_passed_cells, -1, 1))
        )

        new_passed_cells = np.logical_and(new_reached_cells, mask)
        new_passed_cells = np.logical_and(new_passed_cells, np.logical_not(reached_cells))

        reached_cells[:] = np.logical_or(reached_cells, new_reached_cells)

    return np.logical_and(important_cells, np.logical_not(reached_cells)).sum() == 0


def check_connectivity(map, start_points, connectivity_type):
    important_cells = np.zeros_like(map[:, :, 0])
    for mat in material.Resource:
        important_cells = np.logical_or(important_cells, map[:, :, 0] == mat.index)

    passable_tiles = np.ones_like(map[:, :, 0])
    for mat in material.Impassible.materials:
        passable_tiles = np.logical_and(passable_tiles, map[:, :, 0] != mat.index)

    if connectivity_type == "FULL":
        reached_cells = np.zeros_like(important_cells)
        pt = random.choice(start_points)
        reached_cells[pt[0], pt[1]] = True
        if not _walk_and_paint(important_cells, passable_tiles, reached_cells):
            return False
        return np.min(reached_cells[passable_tiles])
    elif connectivity_type == "STRONG":
        total_reached_cells = np.zeros_like(important_cells, dtype=int)
        for pt in start_points:
            reached_cells = np.zeros_like(important_cells)
            reached_cells[pt[0], pt[1]] = 1
            if not _walk_and_paint(important_cells, passable_tiles, reached_cells):
                return False
            total_reached_cells += reached_cells
        if np.min(total_reached_cells[passable_tiles]) == 0:
            return False
        return True
    elif connectivity_type == "WEAK":
        reached_cells = np.zeros_like(important_cells)
        for pt in start_points:
            reached_cells[pt[0], pt[1]] = 1
        return _walk_and_paint(important_cells, passable_tiles, reached_cells)

    return True
