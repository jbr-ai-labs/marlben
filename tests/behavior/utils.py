def create_env(env_class, config):
    env = env_class(config)
    env.reset()
    return env


def run_env(env, steps):
    for _ in range(steps):
        env.step({})
        for group in env.realm.entity_group_manager.player_groups:
            for entID in group.entities:
                player = group.entities[entID]
                assert player.alive
                print(player.resources.water.val, player.resources.food.val)
                assert player.resources.water.val > 0, player.resources.water.val
                assert player.resources.food.val > 0


def _test_helper(env_class, cfg_class, cfg_args={}):
    env = create_env(env_class, cfg_class(**cfg_args))
    run_env(env, 100)
