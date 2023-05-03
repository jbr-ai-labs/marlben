def create_env(env_class, config):
    env = env_class(config)
    env.reset()
    return env

def run_env(env, steps):
    for _ in range(steps):
        actions = dict([(i, {}) for i in env.realm.agents()])
        env.step(actions)
        for group in env.realm.entity_group_manager.player_groups:
            for entID in group.entities:
                player = group.entities[entID]
                assert player.alive

