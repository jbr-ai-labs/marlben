import os
from copy import deepcopy

import ray
import torch
from ray import tune
from ray.tune import CLIReporter
from ray.air.integrations.wandb import WandbLoggerCallback

import marlben
from marlben.rllib import rllib_wrapper as wrapper


class ConsoleLog(CLIReporter):
    def report(self, trials, done, *sys_info):
        super().report(trials, done, *sys_info)


def setup_ray(config):
    torch.set_num_threads(1)
    os.environ['MKL_NUM_THREADS'] = '1'
    os.environ['OMP_NUM_THREADS'] = '1'
    os.environ['NUMEXPR_NUM_THREADS'] = '1'
    ray.init(local_mode=config.LOCAL_MODE)


def setup_policies(mapPolicy, config):
    policies = {}
    env = marlben.Env(config)
    for i in range(config.NPOLICIES):  # FIXME: Is it ok that we iterate through policies (not an agents)?
        params = {"agent_id": i,
                  "obs_space_dict": env.observation_space(i),
                  "act_space_dict": env.action_space(i)}
        key = mapPolicy(i, 0)
        policies[key] = (None, env.observation_space(i), env.action_space(i), params)
    return policies


def setup_wandb(callbacks):
    wandb_api_key = 'wandb_api_key'
    if os.path.exists(wandb_api_key):
        callbacks.append(WandbLoggerCallback(project='marlben', api_key_file='wandb_api_key', log_config=False))
    else:
        print('Running without WanDB. Create a file wandb_api_key in the project`s root folder and paste your API key to enable')


def get_restore(config, algorithm, config_name):
    restore = None
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
    mapPolicy = lambda agentId, episode, worker=0: 'policy_{}'.format(agentId % config.NPOLICIES)
    policies = setup_policies(mapPolicy, config)

    # Evaluation config
    eval_config = deepcopy(config)
    eval_config.EVALUATE = True
    eval_config.AGENTS = []

    algo, base_config = trainer_wrapper(config)

    # Create rllib config
    rllib_config = base_config\
        .multi_agent(policies=policies,
                     policy_mapping_fn=mapPolicy,
                     count_steps_by='agent_steps') \
        .environment(env=env_name,
                     clip_actions=True,
                     env_config={"config": config},
                     disable_env_checking=True,
                     render_env=config.RENDER) \
        .evaluation(evaluation_config={"config": eval_config},
                    evaluation_interval=config.EVALUATION_INTERVAL,
                    evaluation_num_episodes=config.EVALUATION_NUM_EPISODES,
                    evaluation_num_workers=config.EVALUATION_NUM_WORKERS,
                    evaluation_parallel_to_training=config.EVALUATION_PARALLEL) \
        .rollouts(num_rollout_workers=config.NUM_WORKERS,
                  rollout_fragment_length=config.ROLLOUT_FRAGMENT_LENGTH,
                  num_envs_per_worker=1) \
        .callbacks(wrapper.RLlibLogCallbacks) \
        .training(train_batch_size=config.TRAIN_BATCH_SIZE,
                  lr=2e-5,
                  gamma=0.99,
                  lambda_=0.9,
                  use_gae=True,
                  clip_param=0.4,
                  grad_clip=None,
                  entropy_coeff=0.1,
                  vf_loss_coeff=0.25,
                  sgd_minibatch_size=64,
                  num_sgd_iter=config.NUM_SGD_ITER,
                  model={'custom_model': 'godsword',
                         'custom_model_config': {'config': config},
                         'max_seq_len': config.LSTM_BPTT_HORIZON}) \
        .debugging(log_level="ERROR") \
        .framework(framework="torch") \
        .resources(num_gpus=int(os.environ.get("RLLIB_NUM_GPUS", config.NUM_GPUS)),
                   num_gpus_per_worker=config.NUM_GPUS_PER_WORKER)

    callbacks = []
    setup_wandb(callbacks)
    config_name = get_config_name(config)

    tune.run(algo,
             config=rllib_config,
             verbose=config.LOG_LEVEL,
             stop={'training_iteration': config.TRAINING_ITERATIONS},
             restore=get_restore(config, algo.__name__, config_name),
             resume=config.RESUME,
             local_dir=config.EXPERIMENT_DIR,
             keep_checkpoints_num=config.KEEP_CHECKPOINTS_NUM,
             checkpoint_freq=config.CHECKPOINT_FREQ,
             checkpoint_at_end=True,
             trial_dirname_creator=lambda _: config_name,
             progress_reporter=ConsoleLog(),
             reuse_actors=True,
             callbacks=callbacks)
