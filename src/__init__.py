from .environments import Corridor



def env_factory(env_name):
    if env_name == 'Corridor':
        return Corridor
    else:
        raise NotImplementedError


def make(env_name, config):
    return env_factory(env_name)(config)
