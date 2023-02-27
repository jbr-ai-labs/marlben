import numpy as np
from nmmo.core.terrain import Terrain


def _walk_and_paint(important_cells, mask, reached_cells):
    new_passed_cells = np.logical_and(reached_cells, mask)
    new_reached_cells = reached_cells
    while new_reached_cells.sum() > 0:
        new_reached_cells = np.logical_or(
            np.logical_or(np.roll(new_passed_cells, 1, 0), np.roll(new_passed_cells, -1, 0)),
            np.logical_or(np.roll(new_passed_cells, 1, 1), np.roll(new_passed_cells, -1, 1))
        )
        new_passed_cells = np.logical_and(np.logical_or(
            np.logical_or(np.roll(new_passed_cells, 1, 0), np.roll(new_passed_cells, -1, 0)),
            np.logical_or(np.roll(new_passed_cells, 1, 1), np.roll(new_passed_cells, -1, 1))
        ), mask)
        new_passed_cells = np.logical_and(new_passed_cells, np.logical_not(reached_cells))
        reached_cells = np.logical_or(reached_cells, new_reached_cells)

    return np.logical_and(important_cells, np.logical_not(reached_cells)).sum() == 0


def check_connectivity(map, start_points, connectivity_type):
    important_cells = np.logical_or(map[:, :, 0] == Terrain.FOREST, map[:, :, 0] == Terrain.WATER)
    mask = np.logical_and(map[:, :, 0] != Terrain.WATER, np.logical_and(map[:, :, 0] != Terrain.STONE, map[:, :, 0] != Terrain.LAVA))
    if connectivity_type == "STRONG":
        for pt in start_points:
            reached_cells = np.zeros_like(important_cells)
            reached_cells[pt[0], pt[1]] = 1
            if not _walk_and_paint(important_cells, mask, reached_cells):
                return False
        return True
    elif connectivity_type == "WEAK":
        reached_cells = np.zeros_like(important_cells)
        for pt in start_points:
            reached_cells[pt[0], pt[1]] = 1
        return _walk_and_paint(important_cells, mask, reached_cells)

    return True
