def inRange(entity, stim, config, N):
    R, C = stim.shape
    R, C = R // 2, C // 2

    rets = set([entity])
    for r in range(R - N, R + N + 1):
        for c in range(C - N, C + N + 1):
            for e in stim[r, c].ents.values():
                rets.add(e)

    rets = list(rets)
    return rets


def l1(start, goal):
    sr, sc = start
    gr, gc = goal
    return abs(gr - sr) + abs(gc - sc)


def l2(start, goal):
    sr, sc = start
    gr, gc = goal
    return 0.5*((gr - sr)**2 + (gc - sc)**2)**0.5
