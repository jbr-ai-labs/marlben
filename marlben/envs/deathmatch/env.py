import marlben

"""
This environment is a more competitive version of the Arena environment. Agents have an additional attack action that has an effect equivalent to that action in Arena.
The specificity lies in the fact that the agent receives an additional reward every time the health of one of the opponents drops to zero in any way.

Expected behavior:
Depending on the priorities of the agent, he can focus on survival or on attacking opponents. 
With a full focus on the latter, the agent will not live long and will receive a small or negative reward in total.
A more profitable strategy is to provide itself with enough resources to regenerate health, and only then show aggression towards opponents.
In addition, some agents can completely focus on survival, receiving a reward for any outcome of the battle between other agents.

Implementation details are located in config file
"""
class Deathmatch(marlben.Env):
    pass
