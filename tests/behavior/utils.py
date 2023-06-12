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
                assert player.resources.water.val > 0, player.resources.water.val
                assert player.resources.food.val > 0


def run_env_combat(env, steps):
    groups = env.realm.entity_group_manager.player_groups
    player_1 = groups[0].entities[1]
    player_2 = groups[1].entities[2]
    for current_step in range(steps):
        env.step({})
        if current_step > 15:            
            assert player_1.alive
            assert player_1.resources.water.val > 0, player_1.resources.water.val
            assert player_1.resources.food.val > 0
            assert player_2.dead


def _test_helper(env_class, cfg_class, cfg_args={}):
    env = create_env(env_class, cfg_class(**cfg_args))
    run_env(env, 100)


def _test_helper_combat(env_class, cfg_class, cfg_args={}):
    env = create_env(env_class, cfg_class(**cfg_args))
    run_env_combat(env, 100)
