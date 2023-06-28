from dataclasses import dataclass, field

import marlben


@dataclass
class RLlib:
    """Base config for RLlib Models

   Extends core Config, which contains environment, evaluation,
   and non-RLlib-specific learning parameters

   Configure NUM_GPUS and NUM_WORKERS for your hardware
   Note that EVALUATION_NUM_WORKERS cores are reserved for evaluation
   and one additional core is reserved for the driver process.
   Therefore, set NUM_WORKERS <= cores - EVALUATION_NUM_WORKERS - 1
    """

    # Run in train/evaluation mode
    EVALUATE: bool = False
    N_TRAIN_MAPS: int = 1

    @property
    def MODEL(self):
        return self.__class__.__name__

    @property
    def NMAPS(self):
        if not self.EVALUATE:
            return self.N_TRAIN_MAPS
        return super().NMAPS

    @property
    def TRAIN_BATCH_SIZE(self):
        if not hasattr(self, "_TRAIN_BATCH_SIZE") or self._TRAIN_BATCH_SIZE is None:
            self._TRAIN_BATCH_SIZE = 64 * 256 * self.NUM_WORKERS
        return self._TRAIN_BATCH_SIZE

    @TRAIN_BATCH_SIZE.setter
    def TRAIN_BATCH_SIZE(self, value):
        self._TRAIN_BATCH_SIZE = value

    # Checkpointing. Resume will load the latest trial, e.g. to continue training
    # Restore (overrides resume) will force load a specific checkpoint (e.g. for rendering)
    EXPERIMENT_DIR: str = 'experiments'
    RESUME: bool = False

    RESTORE: bool = False
    RESTORE_ID: str = 'Baseline'  # Experiment name suffix
    RESTORE_CHECKPOINT: int = 1000

    # Policy specification
    EVAL_AGENTS: list = field(default_factory=lambda: [marlben.Agent])
    AGENTS: list = field(default_factory=lambda: [marlben.Agent])
    TASKS: list = field(default_factory=lambda: [])

    # Hardware and debug
    NUM_GPUS_PER_WORKER: int = 0
    LOCAL_MODE: bool = False
    LOG_LEVEL: int = 1

    # Training and evaluation settings
    EVALUATION_INTERVAL: int = 1
    EVALUATION_PARALLEL: bool = False
    TRAINING_ITERATIONS: int = 1000
    KEEP_CHECKPOINTS_NUM: int = 3
    CHECKPOINT_FREQ: int = 1
    LSTM_BPTT_HORIZON: int = 16
    NUM_SGD_ITER: int = 1

    # Model
    SCRIPTED = None
    N_AGENT_OBS: int = 100
    NPOLICIES: int = 1
    HIDDEN: int = 64
    EMBED: int = 64

    # Reward
    COOPERATIVE: bool = False
    TEAM_SPIRIT: float = 0.0


class Small(RLlib, marlben.config.Small):
    '''Small scale Neural MMO training setting

   Features up to 64 concurrent agents and 32 concurrent NPCs,
   64 x 64 maps (excluding the border), and 128 timestep horizons'''

    # Memory/Batch Scale
    ROLLOUT_FRAGMENT_LENGTH: int = 128
    SGD_MINIBATCH_SIZE: int = 128

    # Horizon
    TRAIN_HORIZON: int = 128
    EVALUATION_HORIZON: int = 128


@dataclass
class Medium(RLlib, marlben.config.Medium):
    '''Medium scale Neural MMO training setting

   Features up to 256 concurrent agents and 128 concurrent NPCs,
   128 x 128 maps (excluding the border), and 1024 timestep horizons'''

    # Memory/Batch Scale
    ROLLOUT_FRAGMENT_LENGTH: int = 256
    SGD_MINIBATCH_SIZE: int = 128

    # Horizon
    TRAIN_HORIZON: int = 1024
    EVALUATION_HORIZON: int = 1024


@dataclass
class Large(RLlib, marlben.config.Large):
    """Large scale Neural MMO training setting

    Features up to 2048 concurrent agents and 1024 concurrent NPCs,
    1024 x 1024 maps (excluding the border), and 8192 timestep horizons
    """

    # Memory/Batch Scale
    ROLLOUT_FRAGMENT_LENGTH: int = 32
    SGD_MINIBATCH_SIZE: int = 128

    # Horizon
    TRAIN_HORIZON: int = 8192
    EVALUATION_HORIZON: int = 8192
