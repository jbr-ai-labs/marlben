import marlben

"""
Agents are given an additional building action. Its effect is that the cell where the agent was in the previous turn is replaced with a stone cell.

Expected behavior:
Agents can use their already collected resources to trap other agents in parts of the map, or fence themselves off on parts of the map with forest and water tiles.
Thus, the division of the territory between agents can occur.

Implementation details are located in config file
"""
class GatheringBuilding(marlben.Env):
    pass
