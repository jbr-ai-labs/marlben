import marlben


"""
Agents are granted an additional attack action compared to Gathering env. Its effect is that the health of another random agent in a small radius is reduced.
This environment is suitable for testing the propensity for cooperation between agents.

Expected behavior:
On the one hand, the attack of other agents obviously helps to reduce their health to zero and, as a result, reduce the competition for resources.
On the other hand, agents can be guided by the principle of reciprocity, that is, respond to an attack with an attack, in which case it may be more profitable not to attack.
To avoid aggression from other agents, the agent can also simply avoid them.

Implementation details are located in config file
"""
class Arena(marlben.Env):
    pass
