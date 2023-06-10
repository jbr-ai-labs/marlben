import marlben

"""
In addition to agents, non-playable characters (NPCs) periodically appear on specific map cells (spawners) with deterministic behavior:
chase the nearest agent and attack him if possible.
Agents are granted an additional NPC attack action, the effect of which is to reduce the health of a random NPC in a small radius around the agent. 
That is, after attacking the NPC several times, it disappears from the map.

Expected behavior:
If all agents are focused on collecting resources and do not keep the number of NPCs under control during the episode, then at some point the number of NPCs can become too much.
Therefore, in order to stably survive for everyone, one of the agents needs to constantly cope with the NPC. In fact, timely control of NPCs is an element of the Public Good.
That is, all agents are better off if there are no NPCs on the map, but no agent is willing to risk their health and resources to secure this goal.
With this element, the environment resembles, for example, CleanUp, first introduced in Hughes et al. (2018).

Implementation details are located in config file

Hughes, E., Leibo, J.Z., Phillips, M., Tuyls, K., Duenez-Guzman, E.,
Castaneda, A.G., Dunning, I., Zhu, T., McKee, K., Koster, R. and Roff, H., 2018,
Inequity aversion improves cooperation in intertemporal social dilemmas. In
Proceedings of the 32nd International Conference on Neural Information
Processing Systems (pp. 3330-3340)..
"""
class Pve(marlben.Env):
    pass
