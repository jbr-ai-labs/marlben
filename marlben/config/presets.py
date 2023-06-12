from marlben.config.base.presets import Medium, Small, Large
from marlben.config.systems.presets import AllGameSystems


class DefaultSmall(Small, AllGameSystems):
    pass


class Default(Medium, AllGameSystems):
    pass
