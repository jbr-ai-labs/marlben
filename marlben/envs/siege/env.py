import marlben

"""
As in the Building environment, agents are provided with an additional build action. Also, NPCs are implemented in the environment identical to the PVE environment.

Expected behavior:
In addition to using the build action to claim territory, agents can also fence off NPC spawners, thus making it impossible for NPCs to attack agents.
On the other hand, such a strategy requires resources and time, and therefore may not be beneficial to a particular agent in the absence of cooperation from other agents.

Implementation details are located in config file
"""
class Siege(marlben.Env):
    pass
