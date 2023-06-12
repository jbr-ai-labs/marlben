import numpy as np
from queue import PriorityQueue


def generate_huge_rocks(height, width, rock_seed_proba, rock_growth_proba,
                        max_growth_attempts=10, random: np.random.RandomState = None):
    prev_rocks = np.zeros((height, width))
    rocks = random.rand(height, width) < rock_seed_proba
    new_rocks = rocks
    attempts = 0
    while (prev_rocks != rocks).sum() > 0 and attempts < max_growth_attempts:
        candidates = np.logical_or(np.logical_or(np.roll(new_rocks, 1, 0), np.roll(new_rocks, -1, 0)),
                                   np.logical_or(np.roll(new_rocks, 1, 1), np.roll(new_rocks, -1, 1)))
        new_rocks = np.logical_and(candidates, random.rand(
            height, width) < rock_growth_proba)
        prev_rocks = rocks
        rocks = np.logical_or(rocks, new_rocks)
        attempts += 1

    return rocks


def generate_labyrinth(height, width, additional_links_min, additional_links_max, random: np.random.RandomState = None):
    assert height % 4 == 0 and width % 4 == 0
    h, w = height // 4, width // 4
    size = np.array([h, w])
    cells = np.zeros((h, w, 4))
    expandable_cells = PriorityQueue()
    expandable_cells.put(
        (random.random(), (random.randint(0, h), random.randint(0, w))))
    direction_helper = np.array([[1, 0], [0, 1], [0, -1], [-1, 0]])

    while expandable_cells.qsize() > 0:
        _, (x, y) = expandable_cells.get()
        directions = (size + direction_helper +
                      np.array([[x, y] for _ in range(4)])) % size
        available_directions = []
        for i, (tx, ty) in enumerate(directions):
            if cells[tx, ty].sum() == 0:
                available_directions.append(i)
        if len(available_directions) == 0:
            continue
        i = available_directions[random.randint(0, len(available_directions))]
        tx, ty = directions[i]
        cells[x, y, i] = 1
        cells[tx, ty, 3 - i] = 1
        expandable_cells.put((random.random(), (tx, ty)))
        if len(available_directions) > 1:
            expandable_cells.put((random.random(), (x, y)))

    for _ in range(random.randint(additional_links_min, additional_links_max + 1)):
        x, y, i = random.randint(0, h), random.randint(
            0, w), random.randint(0, 4)
        while cells[x, y, i] > 0:
            x, y = random.randint(0, h), random.randint(0, w),
            i = random.randint(0, 4)
        cells[x, y, i] = 1
        tx, ty = (size + direction_helper[i] + np.array([x, y])) % size
        cells[tx, ty, 3 - i] = 1

    map = np.zeros(height, width)
    for x in range(h):
        for y in range(w):
            map[4 * x:4 * (x + 1), 4 * y:4 * (y + 1)] = True
            map[4 * x + 1:4 * (x + 1) - 1, 4 * y + 1:4 * (y + 1) - 1] = False
            if cells[x, y, 3] > 0:
                map[4 * x, 4 * y + 1:4 * (y + 1) - 1] = False
            if cells[x, y, 0] > 0:
                map[4 * (x + 1) - 1, 4 * y + 1:4 * (y + 1) - 1] = False
            if cells[x, y, 2] > 0:
                map[4 * x + 1:4 * (x + 1) - 1, 4 * y] = False
            if cells[x, y, 1] > 0:
                map[4 * x + 1:4 * (x + 1) - 1, 4 * (y + 1) - 1] = False
    map[0] = True
    map[-1] = True
    map[:, 0] = True
    map[:, -1] = True

    return map
