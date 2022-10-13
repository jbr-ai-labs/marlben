from ray.rllib.models.torch.recurrent_net import RecurrentNetwork
from torch import nn
import torch
from rllib.neural.policy import Recurrent


class RLlibPolicy(RecurrentNetwork, nn.Module):
    '''Wrapper class for using our baseline models with RLlib'''

    def __init__(self, *args, **kwargs):
        self.config = kwargs.pop('config')
        super().__init__(*args, **kwargs)
        nn.Module.__init__(self)

        # self.space  = actionSpace(self.config).spaces
        self.model = Recurrent(self.config)

    # Initial hidden state for RLlib Trainer
    def get_initial_state(self):
        return [self.model.valueF.weight.new(1, self.config.HIDDEN).zero_(),
                self.model.valueF.weight.new(1, self.config.HIDDEN).zero_()]

    def forward(self, input_dict, state, seq_lens):
        logitDict, state = self.model(input_dict['obs'], state, seq_lens)

        logits = []
        # Flatten structured logits for RLlib
        # TODO: better to use the space directly here in case of missing keys
        for atnKey, atn in sorted(logitDict.items()):
            for argKey, arg in sorted(atn.items()):
                logits.append(arg)

        return torch.cat(logits, dim=1), state

    def value_function(self):
        return self.model.value

    def attention(self):
        return self.model.attn
