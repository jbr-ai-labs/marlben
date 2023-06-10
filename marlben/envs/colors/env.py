import marlben

"""
This environment is a simplified version of the Exploring environment. In it, all information about resource cells is initially available to all agents. 
As a consequence, there is no need to exchange information. This environment is suitable for testing and debugging algorithms before moving on to a more complex Exploring environment.

Expected behavior:
Agents collect resources of their color to survive on the map.

Implementation details are located in config file
"""
class GatheringExclusive(marlben.Env):
    pass
