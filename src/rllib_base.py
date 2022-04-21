import os
from copy import deepcopy

import numpy as np
import ray
from src.environments import rllib_wrapper as wrapper
import torch
from ray import rllib, tune
from ray.tune import CLIReporter
from ray.tune.integration.wandb import WandbLoggerCallback

import nmmo


class ConsoleLog(CLIReporter):
    def report(self, trials, done, *sys_info):
        super().report(trials, done, *sys_info)


def setup_ray(config):
    torch.set_num_threads(1)
    os.environ['MKL_NUM_THREADS'] = '1'
    os.environ['OMP_NUM_THREADS'] = '1'
    os.environ['NUMEXPR_NUM_THREADS'] = '1'
    ray.init(local_mode=config.LOCAL_MODE)


def setup_polcies(mapPolicy, config):
    policies = {}
    env = nmmo.Env(config)
    for i in range(config.NPOLICIES):
        params = {"agent_id": i,
                  "obs_space_dict": env.observation_space(i),
                  "act_space_dict": env.action_space(i)}
        key = mapPolicy(i)
        policies[key] = (None, env.observation_space(i), env.action_space(i), params)
    return policies


def setup_wandb(callbacks):
    wandb_api_key = 'wandb_api_key'
    if os.path.exists(wandb_api_key):
        callbacks.append(WandbLoggerCallback(project='marlben', api_key_file='wandb_api_key', log_config=False))
    else:
        print('Running without WanDB. Create a file baselines/wandb_api_key and paste your API key to enable')


def get_restore(config, trainer_cls, config_name):
    restore = None
    algorithm = trainer_cls.name()
    if config.RESTORE:
        restore = '{0}/{1}/{2}/checkpoint_{3:06d}/checkpoint-{3}'.format(
            config.EXPERIMENT_DIR, algorithm, config_name, config.RESTORE_CHECKPOINT)
    return restore


def get_config_name(config):
    config_name = config.__class__.__name__
    if config.RESTORE and config.RESTORE_ID:
        config_name = '{}_{}'.format(config_name, config.RESTORE_ID)
    return config_name


def run_tune_experiment(config, env_name, trainer_wrapper):
    setup_ray(config)
    mapPolicy = lambda agentID: 'policy_{}'.format(agentID % config.NPOLICIES)
    policies = setup_polcies(mapPolicy, config)

    # Evaluation config
    eval_config = deepcopy(config)
    eval_config.EVALUATE = True
    eval_config.AGENTS = []

    trainer_cls, extra_config = trainer_wrapper(config)

    # Create rllib config
    rllib_config = {'num_workers': config.NUM_WORKERS,
                    'num_gpus_per_worker': config.NUM_GPUS_PER_WORKER,
                    'num_gpus': config.NUM_GPUS,
                    'num_envs_per_worker': 1,
                    'train_batch_size': config.TRAIN_BATCH_SIZE,
                    'rollout_fragment_length': config.ROLLOUT_FRAGMENT_LENGTH,
                    'num_sgd_iter': config.NUM_SGD_ITER,
                    'framework': 'torch',
                    'horizon': np.inf,
                    'soft_horizon': False,
                    'no_done_at_end': False,
                    'env': env_name,
                    'env_config': {'config': config},
                    'evaluation_config': {'env_config': {'config': eval_config}},
                    'multiagent': {'policies': policies,
                                   'policy_mapping_fn': mapPolicy,
                                   'count_steps_by': 'agent_steps'},
                    'model': {'custom_model': 'godsword',
                              'custom_model_config': {'config': config},
                              'max_seq_len': config.LSTM_BPTT_HORIZON},
                    'render_env': config.RENDER,
                    'callbacks': wrapper.RLlibLogCallbacks,
                    'evaluation_interval': config.EVALUATION_INTERVAL,
                    'evaluation_num_episodes': config.EVALUATION_NUM_EPISODES,
                    'evaluation_num_workers': config.EVALUATION_NUM_WORKERS,
                    'evaluation_parallel_to_training': config.EVALUATION_PARALLEL}

    rllib_config = {**rllib_config, **extra_config}

    callbacks = []
    setup_wandb(callbacks)
    config_name = get_config_name(config)

    tune.run(trainer_cls,
             config=rllib_config,
             name=trainer_cls.name(),
             verbose=config.LOG_LEVEL,
             stop={'training_iteration': config.TRAINING_ITERATIONS},
             restore=get_restore(config, trainer_cls, config_name),
             resume=config.RESUME,
             local_dir=config.EXPERIMENT_DIR,
             keep_checkpoints_num=config.KEEP_CHECKPOINTS_NUM,
             checkpoint_freq=config.CHECKPOINT_FREQ,
             checkpoint_at_end=True,
             trial_dirname_creator=lambda _: config_name,
             progress_reporter=ConsoleLog(),
             reuse_actors=True,
             callbacks=callbacks)
