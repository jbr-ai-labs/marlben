def create_env(env_class, config):
    env = env_class(config)
    env.reset()
    return env


def random_interaction(env, steps):
    for _ in range(steps):
        actions = dict([(i, env.action_space(i).sample()) for i in env.realm.agents()])
        env.step(actions)