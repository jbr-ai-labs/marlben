from nmmo.config.base.presets import Medium, Small, Large
from nmmo.config.systems.presets import AllGameSystems


class DefaultSmall(Small, AllGameSystems):
    pass


class Default(Medium, AllGameSystems):
    pass
