from collections import defaultdict

import numpy as np
from ray.rllib import MultiAgentEnv
from ray.rllib.algorithms.callbacks import DefaultCallbacks
from ray.rllib.algorithms.ppo import PPOConfig, PPO
from ray.rllib.algorithms.appo import APPOConfig, APPO
from ray.rllib.algorithms.impala import ImpalaConfig, Impala
from tqdm import tqdm

import marlben
from marlben.lib import log


class RLlibEnv(marlben.Env, MultiAgentEnv):
    """Wrapper class for using Neural MMO with RLlib"""

    def __init__(self, config):
        self.config = config["config"]
        super().__init__(self.config)

    def render(self):
        # Patch for RLlib dupe rendering bug
        if not self.config.RENDER:
            return

        super().render()

    def step(self, decisions):
        obs, rewards, dones, infos = super().step(decisions)
        config = self.config
        ts = config.TEAM_SPIRIT

        if config.COOPERATIVE:
            # Union of task rewards across population
            team_rewards = defaultdict(lambda: defaultdict(int))
            populations = {}
            for entID, info in infos.items():
                pop = info.pop('population')
                populations[entID] = pop
                team = team_rewards[pop]
                for task, reward in info.items():
                    team[task] = max(team[task], reward)

            # Team spirit interpolated between agent and team summed task rewards
            for entID, reward in rewards.items():
                pop = populations[entID]
                rewards[entID] = ts * sum(team_rewards[pop].values()) + (1 - ts) * reward

        dones['__all__'] = False

        if config.EVALUATE:
            horizon = config.EVALUATION_HORIZON
        else:
            horizon = config.TRAIN_HORIZON

        hit_horizon = self.realm.tick >= horizon
        truncated = {'__all__': False}

        if (hit_horizon or len(self.realm.players()) == 0):
            dones['__all__'] = True
            truncated['__all___'] = True

        return obs, rewards, dones, truncated, infos

    def reset(self, seed=None, options=None, idx=None, step=True):
        self.has_reset = True

        self.actions = {}
        self.dead = []

        self.quill = log.Quill()

        if idx is None:
            idx = np.random.randint(self.config.NMAPS) + 1

        self.worldIdx = idx
        self.realm.reset(idx)

        if step:
            self.obs, _, _, _, infos = self.step({})

        return self.obs, infos


class RLlibOverlayRegistry(marlben.OverlayRegistry):
    """Host class for RLlib Map overlays"""

    def __init__(self, realm):
        super().__init__(realm.config, realm)

        self.overlays['values'] = Values
        self.overlays['attention'] = Attention
        self.overlays['tileValues'] = TileValues
        self.overlays['entityValues'] = EntityValues


class RLlibOverlay(marlben.Overlay):
    '''RLlib Map overlay wrapper'''

    def __init__(self, config, realm, trainer, model):
        super().__init__(config, realm)
        self.trainer = trainer
        self.model = model


class Attention(RLlibOverlay):
    def register(self, obs):
        '''Computes local attentional maps with respect to each agent'''
        tiles = self.realm.realm.map.tiles
        players = self.realm.realm.players

        attentions = defaultdict(list)
        for idx, playerID in enumerate(obs):
            if playerID not in players:
                continue
            player = players[playerID]
            r, c = player.pos

            rad = self.config.NSTIM
            obTiles = self.realm.realm.map.tiles[r - rad:r + rad + 1, c - rad:c + rad + 1].ravel()

            for tile, a in zip(obTiles, self.model.attention()[idx]):
                attentions[tile].append(float(a))

        sz = self.config.TERRAIN_SIZE
        data = np.zeros((sz, sz))
        for r, tList in enumerate(tiles):
            for c, tile in enumerate(tList):
                if tile not in attentions:
                    continue
                data[r, c] = np.mean(attentions[tile])

        colorized = marlben.overlay.twoTone(data)
        self.realm.register(colorized)


class Values(RLlibOverlay):
    def update(self, obs):
        '''Computes a local value function by painting tiles as agents
      walk over them. This is fast and does not require additional
      network forward passes'''
        players = self.realm.realm.players
        for idx, playerID in enumerate(obs):
            if playerID not in players:
                continue
            r, c = players[playerID].base.pos
            self.values[r, c] = float(self.model.value_function()[idx])

    def register(self, obs):
        colorized = marlben.overlay.twoTone(self.values[:, :])
        self.realm.register(colorized)


def zeroOb(ob, key):
    for k in ob[key]:
        ob[key][k] *= 0


class GlobalValues(RLlibOverlay):
    '''Abstract base for global value functions'''

    def init(self, zeroKey):
        if self.trainer is None:
            return

        print('Computing value map...')
        model = self.trainer.get_policy('policy_0').model
        obs, ents = self.realm.dense()
        values = 0 * self.values

        # Compute actions to populate model value function
        BATCH_SIZE = 128
        batch = {}
        final = list(obs.keys())[-1]
        for agentID in tqdm(obs):
            ob = obs[agentID]
            batch[agentID] = ob
            zeroOb(ob, zeroKey)
            if len(batch) == BATCH_SIZE or agentID == final:
                self.trainer.compute_actions(batch, state={}, policy_id='policy_0')
                for idx, agentID in enumerate(batch):
                    r, c = ents[agentID].base.pos
                    values[r, c] = float(self.model.value_function()[idx])
                batch = {}

        print('Value map computed')
        self.colorized = marlben.overlay.twoTone(values)

    def register(self, obs):
        print('Computing Global Values. This requires one NN pass per tile')
        self.init()

        self.realm.register(self.colorized)


class TileValues(GlobalValues):
    def init(self, zeroKey='Entity'):
        '''Compute a global value function map excluding other agents. This
      requires a forward pass for every tile and will be slow on large maps'''
        super().init(zeroKey)


class EntityValues(GlobalValues):
    def init(self, zeroKey='Tile'):
        '''Compute a global value function map excluding tiles. This
      requires a forward pass for every tile and will be slow on large maps'''
        super().init(zeroKey)


class Trainer:
    def __init__(self, config, env=None, logger_creator=None):
        super().__init__(config, env, logger_creator)

    @classmethod
    def name(cls):
        return cls.__bases__[0].__name__

    def post_mean(self, stats):
        for key, vals in stats.items():
            if type(vals) == list:
                stats[key] = np.mean(vals)

    def train(self):
        stats = super().train()
        self.post_mean(stats['custom_metrics'])
        return stats

    def evaluate(self):
        return super().evaluate()


def PPOCustom(config):
    class PPOCustom(Trainer, PPO): pass

    ppoConfig = PPOConfig()
    ppoConfig.sgd_minibatch_size = config.SGD_MINIBATCH_SIZE
    return PPOCustom, ppoConfig


def APPOCustom(config):
    class APPOCustom(Trainer, APPO): pass

    return APPOCustom, APPOConfig()


def ImpalaCustom(config):
    class ImpalaCustom(Trainer, Impala): pass

    return ImpalaCustom, ImpalaConfig


###############################################################################
### Logging
class RLlibLogCallbacks(DefaultCallbacks):
    def on_episode_end(self, *, worker, base_env, policies, episode, **kwargs):
        assert len(base_env.envs) == 1, 'One env per worker'
        env = base_env.envs[0]

        stats = env.terminal()['Stats']
        policy_ids = stats.pop('PolicyID')

        for key, vals in stats.items():
            policy_stat = defaultdict(list)

            # Per-population metrics
            for policy_id, v in zip(policy_ids, vals):
                policy_stat[policy_id].append(v)

            for policy_id, vals in policy_stat.items():
                k = f'{policy_id}_{key}'
                episode.custom_metrics[k] = np.mean(vals)

        if not env.config.EVALUATE:
            return

        episode.custom_metrics['Raw_Policy_IDs'] = policy_ids
        episode.custom_metrics['Raw_Task_Rewards'] = stats['Task_Reward']
