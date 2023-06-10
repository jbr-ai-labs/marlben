import marlben

"""
The specificity of this environment lies in the fact that at the beginning of the episode, only a part of the forest and water cells is visible to each agent,
while the rest of the forest and water cells are hidden and look like stone cells.
At the same time, different agents see different cells of the forest and the water. 
However, agents can still interact with a hidden cell and receive resources from it, thus making it important to spy on other agents routes

Expected behavior:
If the location of the forest and water cells visible to the agent is successful (that is, close to each other and to the agent), he may not look for other resource cells.
However, if the visible resource tiles are far apart, it may be easier for the agent to find other resource tiles on the map.
To do this, the agent can bypass the map until it accidentally stumbles upon resources.
A more sophisticated strategy is to monitor the behavior of other agents in an attempt to figure out the locations of the resources they see.
If opponents use this strategy, it can also be advantageous to sometimes move in arbitrary directions to confuse opponents. 
This is an element of adversarial communication in the environment, in what way it resembles, for example, Adversary from the MPE set [1]. 
Also, the environment can be useful for testing communication channels between agents for mutually beneficial information exchange.

Implementation details are located in config file

[1] Lowe R. et al. Multi-agent actor-critic for mixed cooperative-competitive environments // Advances in neural information processing systems. - 2017. - P. 6379–6390.
"""
class GatheringObscured(marlben.Env):
    pass
