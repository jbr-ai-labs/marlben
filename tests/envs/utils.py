def create_env(env_class, config):
    env = env_class(config)
    env.reset()
    return env


def random_interaction(env, steps):
    for _ in range(steps):
        actions = dict([(i, env.action_space(i).sample()) for i in env.realm.agents()])
        env.step(actions)


def _test_create_with_config_class(env_class, cfg_class):
    for num_groups in (2, 4, 8, 16, 32):
        for num_agents_per_group in (2, 4, 8, 16, 64):
            try:
                create_env(env_class, cfg_class(num_groups, num_agents_per_group))
            except Exception as e:
                raise Exception(f"Params ({num_groups}, {num_agents_per_group})") from e


def _test_interact_with_config_class(env_class, cfg_class):
    for num_groups in (2, 4, 8, 16, 32):
        for num_agents_per_group in (2, 4, 8, 16, 64):
            try:
                env = create_env(env_class, cfg_class(num_groups, num_agents_per_group))
                random_interaction(env, 100)
            except Exception as e:
                raise Exception(f"Params ({num_groups}, {num_agents_per_group})") from e
