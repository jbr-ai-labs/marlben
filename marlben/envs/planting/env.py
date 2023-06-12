import marlben

"""
Agents are granted an additional planting action. Its effect is that the cell where the agent was in the previous turn is replaced with a forest cell. 
This action is not free and costs the agent a large amount of food resources. In addition, initially there are fewer forest cells in the environment than in Gathering.

Expected behavior:
Since forest cells are in short supply at the beginning of the episode, all agents can only survive by using the plant action. 
However, since all agents can use the new forest tiles to obtain food, performing this action may be disadvantageous for a particular agent. 
Thus, providing enough food for everyone is an element of the Public Good.

Implementation details are located in config file
"""
class GatheringPlanting(marlben.Env):
    pass
