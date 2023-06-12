import marlben

"""
As the name suggests, this environment is the team version of the deathmatch environment. 
Agents are divided into multiple teams. The attack action has been modified so that its effect can only be applied to an agent from the other team.

Expected behavior: 
Naive agents can behave similarly to Arena or Deathmatch environments, ignoring team affiliation. 
A more profitable strategy is to coordinate with your team members to attack opponents, thus providing additional rewards and reducing competition for resources.

Implementation details are located in config file
"""
class TeamDeathmatch(marlben.Env):
    pass
