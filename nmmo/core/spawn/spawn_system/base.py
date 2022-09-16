import random
import numpy as np


def spawn_concurrent(player_manager, config, realm):
    if player_manager.spawned:
        return

    player_manager.spawned = True
    idx = 0

    left = config.TERRAIN_BORDER
    right = config.TERRAIN_CENTER + config.TERRAIN_BORDER
    rrange = np.arange(left + 2, right, 4).tolist()

    assert not config.TERRAIN_CENTER % 4
    per_side = config.TERRAIN_CENTER // 4

    lows = (left + np.zeros(per_side, dtype=np.int)).tolist()
    highs = (right + np.zeros(per_side, dtype=np.int)).tolist()

    s1 = list(zip(rrange, lows))
    s2 = list(zip(lows, rrange))
    s3 = list(zip(rrange, highs))
    s4 = list(zip(highs, rrange))

    for r, c in s1 + s2 + s3 + s4:
        idx += 1
        assert not realm.map.tiles[r, c].occupied
        player_manager.spawnIndividual(r, c)


def spawn_continuous(player_manager, config, realm):
    # MMO-style spawning
    for _ in range(config.PLAYER_SPAWN_ATTEMPTS):
        if len(player_manager.entities) >= config.NENT:
            break
        mmax = config.TERRAIN_CENTER + config.TERRAIN_BORDER
        mmin = config.TERRAIN_BORDER
        var = np.random.randint(mmin, mmax)
        fixed = np.random.choice([mmin, mmax])
        r, c = int(var), int(fixed)
        if np.random.rand() > 0.5:
            r, c = c, r

        if realm.map.tiles[r, c].occupied:
            continue
        print('spawning individual')
        player_manager.spawnIndividual(r, c)

    while len(player_manager.entities) == 0:
        spawn_continuous(player_manager, config, realm)


def spawn_in_range(player_manager, config, realm):
    if player_manager.spawned:
        return 
    player_manager.spawned = True
    top, left = config.TOP_LEFT_CORNER
    for _ in range(config.NENT):
        agent_idx = player_manager.idx - 1

        r_range = config.SPAWN_PARAMS['r_ranges'][agent_idx]
        r_range = [r + top for r in r_range]
            
        c_range = config.SPAWN_PARAMS['c_ranges'][agent_idx]
        c_range = [c + left for c in c_range]

        r = random.randint(*r_range)
        c = random.randint(*c_range)
        assert not realm.map.tiles[r, c].occupied
        player_manager.spawnIndividual(r, c)
