import torch
from torch import nn
from torch.nn.utils import rnn

from . import io
from .utils import nn_blocks


class Base(nn.Module):
    def __init__(self, config):
        '''Base class for baseline policies

        Args:
          config: A Configuration object
        '''
        super().__init__()
        self.embed = config.EMBED
        self.config = config

        self.input = io.Input(config,
                              embeddings=io.MixedEmbedding,
                              attributes=nn_blocks.SelfAttention)
        self.output = io.Output(config)

        self.valueF = nn.Linear(config.HIDDEN, 1)

    def hidden(self, obs, state=None, lens=None):
        '''Abstract method for hidden state processing, recurrent or otherwise,
        applied between the input and output modules

        Args:
          obs: An observation dictionary, provided by forward()
          state: The previous hidden state, only provided for recurrent nets
          lens: Trajectory segment lengths used to unflatten batched obs
        '''
        raise NotImplementedError('Implement this method in a subclass')

    def forward(self, obs, state=None, lens=None):
        '''Applies builtin IO and value function with user-defined hidden
        state subnetwork processing. Arguments are supplied by RLlib
        '''
        entityLookup = self.input(obs)
        hidden, state = self.hidden(entityLookup, state, lens)
        self.value = self.valueF(hidden).squeeze(1)
        actions = self.output(hidden, entityLookup)
        return actions, state


class Simple(Base):
    def __init__(self, config):
        '''Simple baseline model with flat subnetworks'''
        super().__init__(config)
        h = config.HIDDEN
        w = config.WINDOW()
        w_final = (w - 2) // 2
        self.ent = nn.Linear(2*h, h)
        self.conv = nn.Conv2d(h, h, 3)
        self.pool = nn.MaxPool2d(2)
        self.fc = nn.Linear(h * w_final * w_final, h)

        self.proj = nn.Linear(2*h, h)
        self.attend = nn_blocks.SelfAttention(self.embed, h)

    def hidden(self, obs, state=None, lens=None):
        # Attentional agent embedding
        agentEmb = obs['Entity']
        selfEmb = agentEmb[:, 0:1].expand_as(agentEmb)
        agents = torch.cat((selfEmb, agentEmb), dim=-1)
        agents = self.ent(agents)
        agents, _ = self.attend(agents)
        #agents = self.ent(selfEmb)

        # Convolutional tile embedding
        tiles = obs['Tile']
        self.attn = torch.norm(tiles, p=2, dim=-1)

        w = self.config.WINDOW()
        batch = tiles.size(0)
        hidden = tiles.size(2)
        # Dims correct?
        tiles = tiles.reshape(batch, w, w, hidden).permute(0, 3, 1, 2)
        tiles = self.conv(tiles)
        tiles = self.pool(tiles)
        tiles = tiles.reshape(batch, -1)
        tiles = self.fc(tiles)

        hidden = torch.cat((agents, tiles), dim=-1)
        hidden = self.proj(hidden)
        return hidden, state


class Recurrent(Simple):
    def __init__(self, config):
        '''Recurrent baseline model'''
        super().__init__(config)
        self.lstm = nn_blocks.BatchFirstLSTM(input_size=config.HIDDEN,
                                             hidden_size=config.HIDDEN)

    # Note: seemingly redundant transposes are required to convert between
    # Pytorch (seq_len, batch, hidden) <-> RLlib (batch, seq_len, hidden)
    def hidden(self, obs, state, lens):
        # Attentional input preprocessor and batching
        lens = lens.cpu() if type(lens) == torch.Tensor else lens
        hidden, _ = super().hidden(obs)
        config = self.config

        TB = hidden.size(0)  # Padded batch of size (seq x batch)
        B = len(lens)  # Sequence fragment time length
        TT = TB // B  # Trajectory batch size
        H = config.HIDDEN  # Hidden state size

        # Pack (batch x seq, hidden) -> (batch, seq, hidden)
        hidden = rnn.pack_padded_sequence(
            input=hidden.view(B, TT, H),
            lengths=lens,
            enforce_sorted=False,
            batch_first=True)

        # Main recurrent network
        hidden, state = self.lstm(hidden, state)

        # Unpack (batch, seq, hidden) -> (batch x seq, hidden)
        hidden, _ = rnn.pad_packed_sequence(sequence=hidden,
                                            batch_first=True,
                                            total_length=TT)

        return hidden.reshape(TB, H), state
