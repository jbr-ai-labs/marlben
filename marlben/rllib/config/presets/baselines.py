import marlben

from . import scale
from . import bases


class Medium(scale.Baseline, bases.Medium, marlben.config.AllGameSystems):
    # Load 1000 epoch pretrained model
    RESTORE = True
    RESTORE_ID = '870d'

    @property
    def SPAWN(self):
        return self.SPAWN_CONCURRENT

    pass


class Debug(scale.Debug, bases.Small, marlben.config.AllGameSystems):
    RESTORE = False

    TRAINING_ITERATIONS = 2

    SGD_MINIBATCH_SIZE = 100
    TRAIN_BATCH_SIZE = 400
    TRAIN_HORIZON = 200
    EVALUATION_HORIZON = 50

    HIDDEN = 2
    EMBED = 2
