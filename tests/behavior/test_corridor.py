from .utils import _test_helper


from nmmo.envs import Corridor, ScriptedCorridorConfig

def test_corridor_scripted():
    _test_helper(env_class=Corridor, cfg_class=ScriptedCorridorConfig)
