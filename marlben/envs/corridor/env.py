import marlben
from os import path as osp

"""
The environment is a narrow corridor of grass cells surrounded by stone cells. 
Agents starting the episode on opposite sides of the map can only move horizontally along this corridor. 
There is also a forest space on one side of the corridor, and a water space on the other.
Agents are also given an additional action - to share the selected resource with other agents if it is in the neighborhood.

Expected behavior:
This environment requires specific coordinated behavior from two agents. 
Since agents cannot move through each other, the only way to have both resources in abundance is to trade with another agent. 
Thus, for mutual survival, both agents must collect the resources available to them at their ends of the corridor and periodically meet in the center of the corridor for an exchange.

Implementation details are located in config file
"""
class Corridor(marlben.Env):
    def __init__(self, config):
        super().__init__(config)
