from marlben.envs import TeamDeathmatchConfig
from marlben.envs import TeamDeathmatch
from tests.envs.utils import _test_create_with_config_class, _test_interact_with_config_class


def test_team_deathmatch_env():
    _test_create_with_config_class(TeamDeathmatch, TeamDeathmatchConfig)
    _test_interact_with_config_class(TeamDeathmatch, TeamDeathmatchConfig)