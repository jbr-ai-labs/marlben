import marlben

"""
The base environment, implemented according to the single structure described in https://github.com/jbr-ai-labs/marlben/wiki#marlben. 
Suitable for testing and debugging algorithms before experiments in more complex environments. 
In addition, due to the sparse reward and random map generation, this environment is not trivial, and in itself may be suitable for comparing algorithms.

Expected behavior: 
All agents coordinate and share the resources available on the map, as a result of which they consistently survive until the end of the episode. 
In the event of a shortage of resources for all, there will be competition for resources and only a part of the agents will survive.

Implementation details are located in config file
"""
class Gathering(marlben.Env):
    pass
