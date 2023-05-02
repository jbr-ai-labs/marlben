"""Manual test for client connectivity"""

import nmmo

if __name__ == '__main__':
    env = nmmo.Env()
    env.config.RENDER = True

    env.reset()
    while True:
       env.render()
       _, _, dones, _ = env.step({})
       print(dones)
       if sum(dones.values()):
           break
