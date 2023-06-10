import marlben

"""
Similar to Team Deathmatch, agents are divided into two teams. However, only one of the teams, called the Predators, is capable of attacking,
while the Prey team's only goal is to survive. Also, the Predators team is smaller than the Prey team to balance the power.
This environment is similar to the environment of the same name from the MPE set [1]. However, there is still competition for resources between all agents.

Expected behavior:
With successful coordination, the Predators successfully capture all of the Preys and survive until the end of the episode.

Implementation details are located in config file

[1] Lowe R. et al. Multi-agent actor-critic for mixed cooperative-competitive environments // Advances in neural information processing systems. - 2017. - P. 6379–6390.
"""
class PredatorPrey(marlben.Env):
    pass
