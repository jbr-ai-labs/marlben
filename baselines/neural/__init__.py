import ray

from baselines.neural.rllib_policy import RLlibPolicy

ray.rllib.models.ModelCatalog.register_custom_model('godsword', RLlibPolicy)
