import marlben

"""
As in the Spying environment, some of the resource cells are hidden from each agent and can only be revealed upon interaction.

An additional complexity is that agents and resources have colors. An agent of a certain color can only interact with resource tiles of the same color.
At the same time, among the resource cells visible to the agent from the beginning of the episode, there may not be cells of the color it needs.

Expected behavior:
The agent can bypass the map until it accidentally stumbles upon resources of the desired color.
But a more stable strategy is to exchange information with agents of other colors. 
That is, to send them information about the visible resources of the color they need in the hope of receiving useful information in return.
Since there is no competition for resources between agents of different colors, such an exchange is indeed mutually beneficial. 
Therefore, the environment is well-suited for testing communication approaches.

Implementation details are located in config file
"""
class GatheringObscuredAndExclusive(marlben.Env):
    pass
