from nmmo.envs.team_deathmatch.config import TeamDeathmatchConfig
from nmmo.envs.team_deathmatch.env import TeamDeathmatch
from tests.envs.utils import _test_create_with_config_class, _test_interact_with_config_class


def test_gathering_env():
    _test_create_with_config_class(TeamDeathmatch, TeamDeathmatchConfig)
    _test_interact_with_config_class(TeamDeathmatch, TeamDeathmatchConfig)