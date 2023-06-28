from rllib import rllib_wrapper
from rllib.rllib_base import run_tune_experiment
from rllib.config import get_config

"""
An example showing how to train your algorithm using RLLib.

This is is the most easiest way to test your multiagent algorithm in a controllable simulation.
Depending on which qualities your algorithm should have, chose an appropriate environment for it.

Specifically, provided environments allows an ability of your algorithm to:
1. Cooperate
2. Optimize tradeoff between personal tasks and "common good"
3. Share information with each other
4. Explore previously unseen field
5. Efficiently scale with a number of agents

Such qualities may be required in multiple tasks such as:
1. Indoor robotics
2. Industrial robotics
3. Automated delivery
4. Online logistic optimization
5. etc
As our environments are grid-based, solutions tasted on our environments can easily be scaled on complex real-world problems.

More specific example:
Suppose, you want to train an indoor robotic assistant that distributes something over the office.
For scalability purposes, it's better to assume that your agent will be not alone in the working place.
Therefore, you'll need to make sure that multiple agents are able to coordinate with each other to optimize their routines.
To test an ability to cooperate, you may use "Corridor" and "Gathering" environments.

Let's also assume that each agent have different specifications and therefore can only perform a subset of tasks.
In that case, you may also want to test your algorithm with "Colors", "Spying" or "Exploring" environments.

If your agents require more accurate cooperation in order to solve tasks, you may also use "Raid" and "BossFight" environments. 
"""

if __name__ == '__main__':
    EnvConfig = get_config("Corridor")

    run_tune_experiment(EnvConfig(), 'Corridor', rllib_wrapper.PPO)
